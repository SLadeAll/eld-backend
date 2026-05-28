"""
Automatic road indication extraction from OSM Overpass API.

Queries the Overpass API for traffic signals, speed bumps, toll booths,
fuel stations, rest areas, and other road features within the bounding
box of a given route.  Results are cached in-memory per bounding box to
avoid re-querying the same area within CACHE_TTL_SECONDS.
"""

import math
import time
import threading
import requests
from typing import Dict, List, Tuple

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
CACHE_TTL_SECONDS = 3600  # 1 hour

# Thread-safe in-memory cache: {bbox_key: (timestamp, [indication_dicts])}
_cache: Dict[str, Tuple[float, List[Dict]]] = {}
_cache_lock = threading.Lock()


def _bbox_key(min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> str:
    """Quantise to 0.05° grid so adjacent bounding boxes share cache entries."""
    q = 0.05
    return (
        f"{math.floor(min_lat / q) * q:.2f},{math.floor(min_lon / q) * q:.2f},"
        f"{math.ceil(max_lat / q) * q:.2f},{math.ceil(max_lon / q) * q:.2f}"
    )


def _route_bbox(coordinates: List[Dict]) -> Tuple[float, float, float, float]:
    """Compute bounding box with 0.02° (~2 km) padding around the route."""
    lats = [c["lat"] for c in coordinates]
    lons = [c["lon"] for c in coordinates]
    pad = 0.02
    return min(lats) - pad, min(lons) - pad, max(lats) + pad, max(lons) + pad


def _overpass_query(min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> List[Dict]:
    """
    Query Overpass for road-relevant OSM nodes in the bounding box.
    Returns raw indication dicts.  Network failures return an empty list.
    """
    bbox = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    query = f"""
    [out:json][timeout:25];
    (
      node["highway"="traffic_signals"]({bbox});
      node["highway"="stop"]({bbox});
      node["highway"="give_way"]({bbox});
      node["traffic_calming"~"bump|hump|speed_table|cushion"]({bbox});
      node["railway"="level_crossing"]({bbox});
      node["amenity"="fuel"]({bbox});
      node["amenity"="rest_area"]({bbox});
      node["barrier"="toll_booth"]({bbox});
      node["maxspeed"]({bbox});
      way["highway"="construction"]({bbox});
    );
    out center 300;
    """
    try:
        resp = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=20,
            headers={"User-Agent": "ELD-MappingApp/1.0"},
        )
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
    except Exception:
        return []

    indications: List[Dict] = []
    seen: set = set()

    for el in elements:
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue

        # Deduplicate positions rounded to ~100 m (3 decimal places)
        pos_key = (round(lat, 3), round(lon, 3))
        if pos_key in seen:
            continue
        seen.add(pos_key)

        tags = el.get("tags", {})
        highway = tags.get("highway", "")
        amenity = tags.get("amenity", "")
        barrier = tags.get("barrier", "")
        railway = tags.get("railway", "")
        calming = tags.get("traffic_calming", "")
        maxspeed = tags.get("maxspeed", "")

        if highway == "traffic_signals":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "traffic_signal",
                "label": tags.get("name", "Semáforo"),
            })
        elif highway in ("stop", "give_way"):
            indications.append({
                "lat": lat, "lon": lon,
                "type": "stop_sign",
                "label": "Señal de Alto",
            })
        elif calming:
            indications.append({
                "lat": lat, "lon": lon,
                "type": "speed_bump",
                "label": "Tope / Reductor de Velocidad",
            })
        elif railway == "level_crossing":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "level_crossing",
                "label": "Cruce Ferroviario",
            })
        elif amenity == "fuel":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "fuel_station",
                "label": tags.get("name") or tags.get("brand", "Gasolinera"),
            })
        elif amenity == "rest_area":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "rest_area",
                "label": tags.get("name", "Área de Descanso"),
            })
        elif barrier == "toll_booth":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "toll",
                "label": tags.get("name", "Caseta de Cobro"),
            })
        elif highway == "construction":
            indications.append({
                "lat": lat, "lon": lon,
                "type": "construction",
                "label": "Zona en Construcción",
            })
        elif maxspeed:
            indications.append({
                "lat": lat, "lon": lon,
                "type": "speed_limit",
                "label": f"Velocidad máx. {maxspeed} km/h",
                "metadata": {"maxspeed": maxspeed},
            })

    return indications


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    r = math.pi / 180.0
    dlat = (lat2 - lat1) * r
    dlon = (lon2 - lon1) * r
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1 * r) * math.cos(lat2 * r) * math.sin(dlon / 2) ** 2
    )
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def _filter_near_route(
    indications: List[Dict],
    coordinates: List[Dict],
    max_km: float = 3.0,
) -> List[Dict]:
    """Retain only indications within max_km of any sampled route point."""
    if not indications:
        return []
    # Sample every Nth point for performance (route is already downsampled)
    step = max(1, len(coordinates) // 100)
    check = coordinates[::step]
    return [
        ind for ind in indications
        if any(
            _haversine_km(ind["lat"], ind["lon"], c["lat"], c["lon"]) <= max_km
            for c in check
        )
    ]


def extract_indications(coordinates: List[Dict]) -> List[Dict]:
    """
    Extract road indications for the given route.

    coordinates — list of {lat, lon, elevation?} dicts (same format as
    the route-analysis /analyze/ endpoint).

    Returns indication dicts: {lat, lon, type, label, metadata?}.
    Queries Overpass API or returns cached results if available.
    """
    if len(coordinates) < 2:
        return []

    min_lat, min_lon, max_lat, max_lon = _route_bbox(coordinates)
    key = _bbox_key(min_lat, min_lon, max_lat, max_lon)

    with _cache_lock:
        entry = _cache.get(key)
        if entry:
            ts, data = entry
            if time.monotonic() - ts < CACHE_TTL_SECONDS:
                return data

    raw = _overpass_query(min_lat, min_lon, max_lat, max_lon)
    filtered = _filter_near_route(raw, coordinates)

    with _cache_lock:
        _cache[key] = (time.monotonic(), filtered)

    return filtered
