"""
Static map image generation for individual route segments.
Uses the staticmap library (OSM tiles — no API key required).
Falls back to a blank placeholder if the library is unavailable.
"""

import os
import tempfile
import logging

logger = logging.getLogger(__name__)

# Map dimensions (px)
MAP_WIDTH  = 800
MAP_HEIGHT = 400


def _safe_label(label: str) -> str:
    """Convert segment label to a filesystem-safe string."""
    return (
        label.replace(' ', '_')
             .replace('/', '-')
             .replace(':', '')
             .replace('→', '-')
             .replace('>', '-')
    )[:80]


def get_segment_map(
    start_coords: tuple,
    end_coords: tuple,
    segment_label: str,
    route_coords: list = None,
) -> str:
    """
    Generate a static map image for a single road segment and save it to a
    temp file.  Returns the absolute path to the PNG file.

    start_coords:  (lat, lon)
    end_coords:    (lat, lon)
    segment_label: human-readable label, e.g. "Tramo 1"
    route_coords:  optional list of {'lat': float, 'lon': float} dicts that
                   define the actual road geometry; when provided a proper
                   polyline is rendered instead of a straight start→end line.
    """
    tmp_path = os.path.join(
        tempfile.gettempdir(),
        f"segmap_{_safe_label(segment_label)}.png",
    )

    # ── Primary: staticmap (OSM tiles) ────────────────────────────────────────
    try:
        from staticmap import StaticMap, Line, CircleMarker

        m = StaticMap(MAP_WIDTH, MAP_HEIGHT, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')

        # staticmap uses (lon, lat) order
        start_xy = (start_coords[1], start_coords[0])
        end_xy   = (end_coords[1],   end_coords[0])

        # Use actual route polyline when available, otherwise draw a straight line
        if route_coords and len(route_coords) >= 2:
            line_points = [(c['lon'], c['lat']) for c in route_coords]
        else:
            line_points = [start_xy, end_xy]

        m.add_line(Line(line_points, '#e63946', 4))
        m.add_marker(CircleMarker(start_xy, '#2dc653', 14))   # green = start
        m.add_marker(CircleMarker(end_xy,   '#e63946', 14))   # red   = end

        image = m.render()
        image.save(tmp_path)
        logger.info("Map saved via staticmap: %s", tmp_path)
        return tmp_path

    except Exception as exc:
        logger.warning("staticmap failed (%s); using PIL fallback.", exc)

    # ── Fallback: Pillow plain image ───────────────────────────────────────────
    try:
        from PIL import Image, ImageDraw, ImageFont

        img  = Image.new('RGB', (MAP_WIDTH, MAP_HEIGHT), color='#f0f4f8')
        draw = ImageDraw.Draw(img)

        # Draw border
        draw.rectangle([0, 0, MAP_WIDTH - 1, MAP_HEIGHT - 1], outline='#9ca3af', width=2)

        if route_coords and len(route_coords) >= 2:
            # Normalise geographic coordinates to pixel space with padding
            lats = [c['lat'] for c in route_coords]
            lons = [c['lon'] for c in route_coords]
            min_lat, max_lat = min(lats), max(lats)
            min_lon, max_lon = min(lons), max(lons)
            lat_range = max_lat - min_lat or 0.01
            lon_range = max_lon - min_lon or 0.01
            pad = 0.12

            def _to_px(lat, lon):
                x = int(pad * MAP_WIDTH + (lon - min_lon) / lon_range * (1 - 2 * pad) * MAP_WIDTH)
                y = int((1 - pad) * MAP_HEIGHT - (lat - min_lat) / lat_range * (1 - 2 * pad) * MAP_HEIGHT)
                return x, y

            pts = [_to_px(c['lat'], c['lon']) for c in route_coords]
            draw.line(pts, fill='#e63946', width=4)
            sx, sy = pts[0]
            ex, ey = pts[-1]
        else:
            sx, sy = int(MAP_WIDTH * 0.15), int(MAP_HEIGHT * 0.75)
            ex, ey = int(MAP_WIDTH * 0.85), int(MAP_HEIGHT * 0.25)
            draw.line([sx, sy, ex, ey], fill='#e63946', width=4)

        # Markers
        r = 10
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill='#2dc653', outline='white')
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill='#e63946', outline='white')

        # Labels
        try:
            font  = ImageFont.truetype("arial.ttf", 13)
            small = ImageFont.truetype("arial.ttf", 11)
        except Exception:
            font = small = ImageFont.load_default()

        draw.text((sx + 14, sy - 8),  f"Inicio\n{start_coords[0]:.4f}, {start_coords[1]:.4f}", fill='#111827', font=small)
        draw.text((ex + 14, ey - 8),  f"Fin\n{end_coords[0]:.4f}, {end_coords[1]:.4f}",        fill='#111827', font=small)
        draw.text((20, 16), segment_label, fill='#374151', font=font)
        draw.text((20, 36), '(Mapa de referencia — sin mosaicos OSM)', fill='#9ca3af', font=small)

        img.save(tmp_path)
        logger.info("Map saved via PIL fallback: %s", tmp_path)
        return tmp_path

    except Exception as exc:
        logger.error("PIL fallback also failed: %s", exc)
        # Return an empty temp path; pdf_generator will skip the image gracefully
        return tmp_path
