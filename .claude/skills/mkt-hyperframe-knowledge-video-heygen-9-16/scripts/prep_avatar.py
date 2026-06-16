#!/usr/bin/env python3
"""
Prep Brand Avatar — JPG → Circular Transparent PNG with Ring + Glow.
─────────────────────────────────────────────────────────────────────
One-time tool. Converts a portrait photo into a circular avatar with:
  - Center-cropped square
  - Circular alpha mask
  - Optional white ring border (subtle)
  - Optional outer drop shadow (soft, dark)
  - Optional inner glow

Output PNG has transparent corners and is sized for ffmpeg overlay at
1920×1080 (default 240px source → renders at ~120px composited).

Run this ONCE per avatar source image. The output PNG is what concat.sh
overlays on every scene.

Usage:
  python prep_avatar.py \
    --input  workspace/assets/brand/tony-avatar.jpg \
    --output workspace/assets/brand/tony-avatar-circle.png \
    --size   240 \
    --ring   2 \
    --shadow

Requires: Pillow (pip install Pillow).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def center_crop_square(img: Image.Image) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def circular_mask(size: int) -> Image.Image:
    """Return an L-mode mask: 255 inside circle, 0 outside, with antialiasing.

    We render at 4x then downsample for smooth edges.
    """
    big = size * 4
    m = Image.new("L", (big, big), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, big, big), fill=255)
    return m.resize((size, size), Image.LANCZOS)


def make_avatar(src_path: Path, size: int, ring_px: int, shadow: bool) -> Image.Image:
    src = Image.open(src_path).convert("RGB")
    src = center_crop_square(src)
    # Upsample target by 2x then mask + downsample for crisper edges
    work_size = size * 2
    src = src.resize((work_size, work_size), Image.LANCZOS)

    mask = circular_mask(work_size)
    out_rgba = Image.new("RGBA", (work_size, work_size), (0, 0, 0, 0))
    out_rgba.paste(src, (0, 0), mask)

    # Optional white ring
    if ring_px > 0:
        ring_canvas = Image.new("RGBA", (work_size, work_size), (0, 0, 0, 0))
        ring_draw = ImageDraw.Draw(ring_canvas)
        # Ring at outer edge — draw two circles and subtract
        ring_outer_w = ring_px * 2
        ring_draw.ellipse(
            (ring_outer_w // 2, ring_outer_w // 2,
             work_size - ring_outer_w // 2, work_size - ring_outer_w // 2),
            outline=(250, 249, 245, 200),  # cream low-opacity
            width=ring_outer_w,
        )
        out_rgba = Image.alpha_composite(out_rgba, ring_canvas)

    # Optional drop shadow — render shadow behind, then composite avatar on top
    final_size = size
    canvas_size = final_size + (40 if shadow else 0)  # leave room for shadow
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

    # Downsample avatar to final size
    avatar_final = out_rgba.resize((final_size, final_size), Image.LANCZOS)
    offset = (canvas_size - final_size) // 2

    if shadow:
        shadow_mask = circular_mask(final_size + 8)  # slightly larger
        shadow_layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        # Place shadow circle
        sh_off_x = offset - 4
        sh_off_y = offset + 2
        sh_solid = Image.new("RGBA", (final_size + 8, final_size + 8), (0, 0, 0, 0))
        ImageDraw.Draw(sh_solid).ellipse(
            (0, 0, final_size + 8, final_size + 8),
            fill=(0, 0, 0, 140),
        )
        shadow_layer.paste(sh_solid, (sh_off_x, sh_off_y), shadow_mask)
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=10))
        canvas = Image.alpha_composite(canvas, shadow_layer)

    # Composite avatar on top
    canvas.paste(avatar_final, (offset, offset), avatar_final)
    return canvas


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input",  required=True, help="Source portrait JPG")
    p.add_argument("--output", required=True, help="Destination circular PNG")
    p.add_argument("--size",   type=int, default=240, help="Avatar diameter in pixels (default 240)")
    p.add_argument("--ring",   type=int, default=2,   help="Ring border width in pixels (0 to disable)")
    p.add_argument("--shadow", action="store_true",   help="Add outer drop shadow")
    args = p.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    if not src.exists():
        sys.stderr.write(f"[prep_avatar] source not found: {src}\n")
        return 2
    dst.parent.mkdir(parents=True, exist_ok=True)

    img = make_avatar(src, args.size, args.ring, args.shadow)
    img.save(dst, "PNG")
    sys.stderr.write(f"[prep_avatar] wrote {dst} ({img.size[0]}x{img.size[1]})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
