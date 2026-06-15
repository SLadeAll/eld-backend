"""
Highway/carretera name lookup via OSM Overpass API.

Queries major roads (motorway/trunk/primary with a 'ref' tag, e.g. "MEX-54D")
within the route's bounding box once per route and matches each tramo's
midpoint to the nearest road geometry, so the tramo can report which
carretera it runs along.

Results are cached in-memory per bounding box for CACHE_TTL_SECONDS, same
pattern as indication_extractor.py.
"""

import math
import time
import threading
import requests
from typing import Dict, List, Optional, Tuple

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
CACHE_TTL_SECONDS = 3600  # 1 hour
MAX_MATCH_KM = 3.0  # ignore road geometry further than this from the tramo midpoint

_cache: Dict[str, Tuple[float, List[Dict]]] = {}
_cache_lock = threading.Lock()


def _bbox_key(min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> str:
    """Quantise to 0.05° grid so adjacent bounding boxes share cache entries."""
    q = 0.05
    return (
        f"hwy:{math.floor(min_lat / q) * q:.2f},{math.floor(min_lon / q) * q:.2f},"
        f"{math.ceil(max_lat / q) * q:.2f},{math.ceil(max_lon / q) * q:.2f}"
    )


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    r = math.pi / 180.0
    dlat = (lat2 - lat1) * r
    dlon = (lon2 - lon1) * r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1 * r) * math.cos(lat2 * r) * math.sin(dlon / 2) ** 2
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def _route_bbox(coordinates: List[Dict]) -> Tuple[float, float, float, float]:
    """Compute bounding box with ~5 km padding around the route."""
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    pad = 0.05
    return min(lats) - pad, min(lons) - pad, max(lats) + pad, max(lons) + pad


def _overpass_highways(min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> List[Dict]:
    """Query Overpass for major numbered roads in the bbox. Network failures return []."""
    bbox = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    query = f"""
    [out:json][timeout:25];
    way["highway"~"motorway|trunk|primary"]["ref"]({bbox});
    out geom tags;
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

    segments: List[Dict] = []
    for el in elements:
        geometry = el.get("geometry") or []
        if not geometry:
            continue
        tags = el.get("tags", {})
        segments.append({
            'ref': (tags.get('ref') or '').strip(),
            'name': (tags.get('name') or '').strip(),
            'points': [(g['lat'], g['lon']) for g in geometry if 'lat' in g and 'lon' in g],
        })
    return segments


def get_highway_segments(coordinates: List[Dict]) -> List[Dict]:
    """
    Return (cached) list of {'ref', 'name', 'points': [(lat, lon), ...]}
    for major roads within the route's bounding box.
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

    segments = _overpass_highways(min_lat, min_lon, max_lat, max_lon)

    with _cache_lock:
        _cache[key] = (time.monotonic(), segments)

    return segments


def get_road_name_for_coords(lat: float, lon: float, segments: List[Dict]) -> Optional[str]:
    """
    Return a human-readable road name ("MEX-54D — Manzanillo-Guadalajara") for
    the highway segment nearest to (lat, lon), or None if nothing is within
    MAX_MATCH_KM.
    """
    best_seg = None
    best_dist = MAX_MATCH_KM
    for seg in segments:
        for plat, plon in seg['points']:
            d = _haversine_km(lat, lon, plat, plon)
            if d < best_dist:
                best_dist = d
                best_seg = seg

    if not best_seg:
        return None

    ref, name = best_seg['ref'], best_seg['name']
    if ref and name:
        return f"{ref} — {name}"
    return ref or name or None
