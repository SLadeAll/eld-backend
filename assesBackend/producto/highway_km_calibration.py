"""
Known highway km-marker reference points for Servimaniobras corridors.

Each entry is a physically verified point: a real km marker sign on the road
confirmed at those coordinates.  When the route passes near a calibration point,
the cumulative route distance is anchored to the real highway km at that point
and all other tramo km values are shifted accordingly.

Adding more reference points improves accuracy, especially for long routes that
cross multiple states.  One reference per ~200 km of corridor is enough.

Format: {'lat': float, 'lon': float, 'km': float, 'note': str}
"""

CALIBRATION_POINTS = [
    # ── MEX-110: Manzanillo → Tecomán → Colima ─────────────────────────────
    # Verified: 18°57'0.61"N  103°53'21.3"W  = km 38
    {
        'lat': 18 + 57/60 + 0.61/3600,          # 18.9502°N
        'lon': -(103 + 53/60 + 21.3/3600),      # -103.8892°W
        'km': 38.0,
        'note': 'MEX-110 Manzanillo–Colima, km 38 verificado',
    },
]

# Maximum distance (km) from a route coordinate to a calibration point for
# the calibration to be considered "on this route".
CALIBRATION_SNAP_KM = 5.0
