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


def get_segment_map(start_coords: tuple, end_coords: tuple, segment_label: str) -> str:
    """
    Generate a static map image for a single road segment and save it to a
    temp file.  Returns the absolute path to the PNG file.

    start_coords: (lat, lon)
    end_coords:   (lat, lon)
    segment_label: human-readable label, e.g. "Tramo 1"

    The function tries staticmap first, then falls back to a plain PIL image
    with coordinate text so the PDF still has something to show.
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

        m.add_line(Line([start_xy, end_xy], '#e63946', 4))
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

        # Route line (diagonal from start to end area)
        sx, sy = int(MAP_WIDTH * 0.15), int(MAP_HEIGHT * 0.75)
        ex, ey = int(MAP_WIDTH * 0.85), int(MAP_HEIGHT * 0.25)
        draw.line([sx, sy, ex, ey], fill='#e63946', width=4)

        # Markers
        r = 10
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill='#2dc653', outline='white')
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill='#e63946', outline='white')

        # Labels
        try:
            font = ImageFont.truetype("arial.ttf", 13)
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
