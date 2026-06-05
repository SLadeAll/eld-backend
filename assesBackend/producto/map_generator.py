"""
Static map image generation for individual route segments.

Primary:  staticmap library (OSM tiles — no API key required).
Fallback: Pillow — draws the actual route polyline on a styled coordinate-space
          canvas with grid, scale bar and DMS axis labels.  No tiles, but the
          geometry is correct and legible.
"""

import os
import math
import tempfile
import logging

logger = logging.getLogger(__name__)

MAP_WIDTH  = 800
MAP_HEIGHT = 400


def _safe_label(label: str) -> str:
    return (
        label.replace(' ', '_')
             .replace('/', '-')
             .replace(':', '')
             .replace('→', '-')
             .replace('>', '-')
    )[:80]


def _dms(decimal: float, pos: str, neg: str) -> str:
    """Convert decimal degrees to DMS string."""
    sign   = pos if decimal >= 0 else neg
    deg    = int(abs(decimal))
    m_frac = (abs(decimal) - deg) * 60
    mins   = int(m_frac)
    secs   = round((m_frac - mins) * 60)
    if secs == 60:
        secs = 0; mins += 1
    return f"{deg}°{mins:02d}'{secs:02d}\"{sign}"


def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    r = math.pi / 180
    dlat = (lat2 - lat1) * r
    dlon = (lon2 - lon1) * r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1 * r) * math.cos(lat2 * r) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_segment_map(
    start_coords: tuple,
    end_coords: tuple,
    segment_label: str,
    route_coords: list = None,
) -> str:
    """
    Generate a static map PNG for a single route segment and return the
    absolute path to the temp file.

    start_coords : (lat, lon)
    end_coords   : (lat, lon)
    segment_label: human-readable label, e.g. "Tramo 1"
    route_coords : list of {'lat': float, 'lon': float} dicts — the actual
                   road geometry; draws a proper polyline when provided.
    """
    tmp_path = os.path.join(
        tempfile.gettempdir(),
        f"segmap_{_safe_label(segment_label)}.png",
    )

    # ── Primary: staticmap (OSM tiles) ────────────────────────────────────────
    try:
        import urllib.request as _ur
        from staticmap import StaticMap, Line, CircleMarker

        m = StaticMap(
            MAP_WIDTH, MAP_HEIGHT,
            url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            headers={'User-Agent': 'ELD-RouteAnalysis/1.0'},
        )

        start_xy = (start_coords[1], start_coords[0])
        end_xy   = (end_coords[1],   end_coords[0])

        if route_coords and len(route_coords) >= 2:
            line_points = [(c['lon'], c['lat']) for c in route_coords]
        else:
            line_points = [start_xy, end_xy]

        m.add_line(Line(line_points, '#e63946', 3))
        m.add_marker(CircleMarker(start_xy, '#16a34a', 12))
        m.add_marker(CircleMarker(end_xy,   '#dc2626', 12))

        image = m.render()
        image.save(tmp_path)
        logger.info("staticmap OK: %s", tmp_path)
        return tmp_path

    except Exception as exc:
        logger.warning("staticmap failed (%s); using coordinate-diagram fallback.", exc)

    # ── Fallback: Pillow coordinate-space diagram ─────────────────────────────
    return _pil_route_diagram(
        start_coords, end_coords, segment_label, route_coords, tmp_path
    )


# ─────────────────────────────────────────────────────────────────────────────
# PIL fallback — draws a clean geographic coordinate diagram
# ─────────────────────────────────────────────────────────────────────────────

def _pil_route_diagram(
    start_coords, end_coords, segment_label, route_coords, out_path
):
    try:
        from PIL import Image, ImageDraw, ImageFont

        W, H = MAP_WIDTH, MAP_HEIGHT
        PAD_L, PAD_R, PAD_T, PAD_B = 68, 16, 36, 44   # pixels reserved for labels

        img  = Image.new('RGB', (W, H), color='#f8f9fa')
        draw = ImageDraw.Draw(img)

        # Build coordinate list (use route_coords when available)
        if route_coords and len(route_coords) >= 2:
            pts_geo = [(c['lat'], c['lon']) for c in route_coords]
        else:
            pts_geo = [start_coords, end_coords]

        lats = [p[0] for p in pts_geo]
        lons = [p[1] for p in pts_geo]

        # Expand bounds slightly so route doesn't touch the edges
        lat_margin = max((max(lats) - min(lats)) * 0.18, 0.005)
        lon_margin = max((max(lons) - min(lons)) * 0.18, 0.005)

        min_lat = min(lats) - lat_margin
        max_lat = max(lats) + lat_margin
        min_lon = min(lons) - lon_margin
        max_lon = max(lons) + lon_margin

        lat_span = max_lat - min_lat
        lon_span = max_lon - min_lon

        draw_w = W - PAD_L - PAD_R
        draw_h = H - PAD_T - PAD_B

        def to_px(lat, lon):
            x = PAD_L + (lon - min_lon) / lon_span * draw_w
            y = PAD_T + (1 - (lat - min_lat) / lat_span) * draw_h
            return int(x), int(y)

        # ── Background ──
        draw.rectangle([PAD_L, PAD_T, PAD_L + draw_w, PAD_T + draw_h],
                       fill='#eaf0fb', outline='#c7d5ea', width=1)

        # ── Grid lines ──
        n_grid = 4
        for i in range(1, n_grid):
            frac = i / n_grid
            # horizontal
            y = int(PAD_T + frac * draw_h)
            draw.line([(PAD_L, y), (PAD_L + draw_w, y)], fill='#d1d9e8', width=1)
            # vertical
            x = int(PAD_L + frac * draw_w)
            draw.line([(x, PAD_T), (x, PAD_T + draw_h)], fill='#d1d9e8', width=1)

        # ── Route polyline ──
        px_pts = [to_px(lat, lon) for lat, lon in pts_geo]
        if len(px_pts) >= 2:
            draw.line(px_pts, fill='#1d4ed8', width=3)

        # ── Elevation shading along route (subtle gradient dots) ──
        if len(px_pts) >= 4:
            for i in range(1, len(px_pts) - 1):
                x, y = px_pts[i]
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill='#3b82f6')

        # ── Start / End markers ──
        sx, sy = to_px(*start_coords)
        ex, ey = to_px(*end_coords)

        r = 9
        # Start: green circle with "A"
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill='#16a34a', outline='white', width=2)
        # End: red circle with "B"
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill='#dc2626', outline='white', width=2)

        # ── Fonts ──
        try:
            fnt_title  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  12)
            fnt_axis   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',       9)
            fnt_coord  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',       8)
            fnt_marker = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  9)
        except Exception:
            fnt_title = fnt_axis = fnt_coord = fnt_marker = ImageFont.load_default()

        # ── Axis labels ──
        # Y-axis (lat) — left side
        for i in range(n_grid + 1):
            frac = i / n_grid
            lat_val = min_lat + frac * lat_span
            y_px    = int(PAD_T + (1 - frac) * draw_h)
            label   = _dms(lat_val, 'N', 'S')
            bbox    = draw.textbbox((0, 0), label, font=fnt_axis)
            tw      = bbox[2] - bbox[0]
            draw.text((PAD_L - tw - 4, y_px - 5), label, fill='#475569', font=fnt_axis)
            draw.line([(PAD_L - 3, y_px), (PAD_L, y_px)], fill='#94a3b8', width=1)

        # X-axis (lon) — bottom
        for i in range(n_grid + 1):
            frac  = i / n_grid
            lon_v = min_lon + frac * lon_span
            x_px  = int(PAD_L + frac * draw_w)
            label = _dms(lon_v, 'E', 'O')
            bbox  = draw.textbbox((0, 0), label, font=fnt_axis)
            tw    = bbox[2] - bbox[0]
            draw.text((x_px - tw // 2, PAD_T + draw_h + 4), label, fill='#475569', font=fnt_axis)
            draw.line([(x_px, PAD_T + draw_h), (x_px, PAD_T + draw_h + 3)], fill='#94a3b8', width=1)

        # ── Title ──
        draw.text((PAD_L + 4, 8), segment_label, fill='#1e3a5f', font=fnt_title)

        # ── Coordinate labels next to markers ──
        s_label = f"{start_coords[0]:.4f}°N  {abs(start_coords[1]):.4f}°O"
        e_label = f"{end_coords[0]:.4f}°N  {abs(end_coords[1]):.4f}°O"

        # Place label to the right if room, else left
        off = r + 5
        sx_txt = sx + off if sx + off + 130 < W else sx - off - 130
        ex_txt = ex + off if ex + off + 130 < W else ex - off - 130
        draw.text((sx_txt, sy - 8), 'A ' + s_label, fill='#166534', font=fnt_coord)
        draw.text((ex_txt, ey - 8), 'B ' + e_label, fill='#991b1b', font=fnt_coord)

        # ── Scale bar ──
        approx_km = _haversine_km(min_lat, min_lon, min_lat, max_lon)
        nice_km   = _nice_km(approx_km * draw_w / W * 0.25)
        bar_px    = int(nice_km / (approx_km / (draw_w / W)) / 111)

        bar_x, bar_y = PAD_L + 6, PAD_T + draw_h - 12
        draw.rectangle([bar_x, bar_y, bar_x + bar_px, bar_y + 6],
                       fill='#1e3a5f', outline='#1e3a5f')
        draw.text((bar_x + bar_px + 4, bar_y), f'{nice_km} km', fill='#374151', font=fnt_axis)

        # ── Legend ──
        lx, ly = W - PAD_R - 108, PAD_T + 6
        draw.rectangle([lx - 4, ly - 4, lx + 104, ly + 24], fill='white', outline='#d1d5db')
        draw.ellipse([lx, ly + 2, lx + 10, ly + 12], fill='#16a34a', outline='white')
        draw.text((lx + 13, ly + 1), 'Inicio tramo', fill='#166534', font=fnt_marker)
        draw.ellipse([lx, ly + 14, lx + 10, ly + 24], fill='#dc2626', outline='white')
        draw.text((lx + 13, ly + 14), 'Fin tramo',    fill='#7f1d1d', font=fnt_marker)

        # ── Outer border ──
        draw.rectangle([0, 0, W - 1, H - 1], outline='#94a3b8', width=2)

        img.save(out_path)
        logger.info("PIL diagram saved: %s", out_path)
        return out_path

    except Exception as exc:
        logger.error("PIL diagram failed: %s", exc)
        return out_path


def _nice_km(raw_km: float) -> int:
    """Round raw_km down to a nice round number for the scale bar."""
    for nice in [200, 100, 50, 25, 20, 10, 5, 2, 1]:
        if raw_km >= nice:
            return nice
    return max(1, int(raw_km))
