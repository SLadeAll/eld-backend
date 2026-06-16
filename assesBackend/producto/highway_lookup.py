"""
Highway/carretera name and km-marker lookup via OSM Overpass API.

One combined Overpass query per route (cached 1 h) fetches:
  - way["highway"~"motorway|trunk|primary"]["ref"] → road name/ref geometry
  - node["highway"="milestone"]                   → km markers (hitos kilométricos)

Public API:
  get_route_highway_data(coordinates) → {'segments': [...], 'milestones': [...]}
  get_road_name_for_coords(lat, lon, segments) → "MEX-54D — Nombre" | None
  get_km_marker_for_coords(lat, lon, milestones) → float (km) | None

Both segments and milestones are also accessible via the legacy helper
get_highway_segments() which is kept for backwards compatibility.
"""

import math
import time
import threading
import requests
from typing import Dict, List, Optional, Tuple

OVERPASS_URL       = "https://overpass-api.de/api/interpreter"
CACHE_TTL_SECONDS  = 3600   # 1 hour
MAX_MATCH_KM       = 3.0    # max distance from tramo midpoint → road geometry
MAX_MILESTONE_KM   = 2.0    # max distance from tramo midpoint → km marker node

_cache: Dict[str, Tuple[float, Dict]] = {}
_cache_lock = threading.Lock()


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

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
    """Bounding box with ~5 km padding around the route."""
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    pad = 0.05
    return min(lats) - pad, min(lons) - pad, max(lats) + pad, max(lons) + pad


def _parse_milestone_km(tags: Dict) -> Optional[float]:
    """
    Extract the km value from OSM milestone tags.
    Tries 'distance', 'ref', then 'name'.  Strips alphabetic prefixes
    (e.g. "K234", "km 234", "234.5").
    """
    for key in ('distance', 'ref', 'name'):
        raw = (tags.get(key) or '').strip()
        if not raw:
            continue
        # Remove leading K/k/km prefix and any trailing text after the number
        cleaned = raw.lstrip('KkMm ').split()[0].replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            continue
    return None


def _overpass_query(min_lat: float, min_lon: float,
                    max_lat: float, max_lon: float) -> Tuple[List[Dict], List[Dict]]:
    """
    Single Overpass query fetching:
      - Major numbered road ways (geometry + tags)
      - Highway milestone nodes (lat/lon + tags)

    Returns (segments, milestones).  Network/parse failures return ([], []).
    """
    bbox = f"{min_lat},{min_lon},{max_lat},{max_lon}"
    query = f"""
    [out:json][timeout:30];
    (
      way["highway"~"motorway|trunk|primary"]["ref"]({bbox});
      node["highway"="milestone"]({bbox});
      node["milestone:type"]({bbox});
      node["distance"][!"boundary"]({bbox});
      node["ref"~"^[Kk][0-9]"]["highway"]({bbox});
    );
    out geom tags;
    """
    try:
        resp = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=25,
            headers={"User-Agent": "ELD-MappingApp/1.0"},
        )
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
    except Exception:
        return [], []

    segments: List[Dict]   = []
    milestones: List[Dict] = []

    for el in elements:
        tags    = el.get("tags", {})
        el_type = el.get("type", "")

        if el_type == "way":
            geometry = el.get("geometry") or []
            pts = [(g['lat'], g['lon']) for g in geometry if 'lat' in g and 'lon' in g]
            if pts:
                segments.append({
                    'ref':    (tags.get('ref')  or '').strip(),
                    'name':   (tags.get('name') or '').strip(),
                    'points': pts,
                })

        elif el_type == "node":
            lat = el.get("lat")
            lon = el.get("lon")
            if lat is None or lon is None:
                continue
            km_val = _parse_milestone_km(tags)
            if km_val is not None:
                milestones.append({'lat': lat, 'lon': lon, 'km': km_val})

    return segments, milestones


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_route_highway_data(coordinates: List[Dict]) -> Dict:
    """
    Return a dict {'segments': [...], 'milestones': [...]} for the route bbox.
    Results are cached in-memory for CACHE_TTL_SECONDS.

    segments  — [{'ref', 'name', 'points': [(lat, lon), ...]}, ...]
    milestones — [{'lat', 'lon', 'km': float}, ...]
    """
    if len(coordinates) < 2:
        return {'segments': [], 'milestones': []}

    min_lat, min_lon, max_lat, max_lon = _route_bbox(coordinates)
    key = _bbox_key(min_lat, min_lon, max_lat, max_lon)

    with _cache_lock:
        entry = _cache.get(key)
        if entry:
            ts, data = entry
            if time.monotonic() - ts < CACHE_TTL_SECONDS:
                return data

    segs, miles = _overpass_query(min_lat, min_lon, max_lat, max_lon)
    data = {'segments': segs, 'milestones': miles}

    with _cache_lock:
        _cache[key] = (time.monotonic(), data)

    return data


def get_highway_segments(coordinates: List[Dict]) -> List[Dict]:
    """Backwards-compatible wrapper — returns only the segments list."""
    return get_route_highway_data(coordinates)['segments']


def get_road_name_for_coords(lat: float, lon: float, segments: List[Dict]) -> Optional[str]:
    """
    Return "MEX-54D — Nombre" for the highway segment nearest to (lat, lon),
    or None if nothing is within MAX_MATCH_KM.
    """
    best_seg  = None
    best_dist = MAX_MATCH_KM
    for seg in segments:
        for plat, plon in seg['points']:
            d = _haversine_km(lat, lon, plat, plon)
            if d < best_dist:
                best_dist = d
                best_seg  = seg

    if not best_seg:
        return None

    ref, name = best_seg['ref'], best_seg['name']
    if ref and name:
        return f"{ref} — {name}"
    return ref or name or None


def get_km_marker_for_coords(lat: float, lon: float, milestones: List[Dict]) -> Optional[float]:
    """
    Return the km value (float) of the nearest highway milestone node within
    MAX_MILESTONE_KM, or None if no milestone is close enough.
    """
    best_km   = None
    best_dist = MAX_MILESTONE_KM
    for m in milestones:
        d = _haversine_km(lat, lon, m['lat'], m['lon'])
        if d < best_dist:
            best_dist = d
            best_km   = m['km']
    return best_km
