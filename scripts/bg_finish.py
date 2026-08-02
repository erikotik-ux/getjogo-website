#!/usr/bin/env python
"""Clean the generated 4K backdrop and export the shipped sizes.

    cd D:/Business/GetJogo && python scripts/bg_finish.py

- paints out stray marks the model leaves in the sky
- deepens the mid blues a touch so the plate stays calm and moody
- exports 3840x1646 (desktop) and 1920x823 (mobile) WebP
"""
import colorsys
import os

from PIL import Image

SRC = "assets/masters/bg2-raw.jpg"
OUT = "public"

# a thin bright streak the model drew across the sky on the right, ending
# where the right-hand ridge begins
ARTIFACTS = [(5200, 1134, 5868, 1178)]


def inpaint(im, box):
    """Rebuild a box column by column, blending the sky above it into the sky
    below. Vertical works where horizontal cannot: the mark is a long thin
    horizontal line, so its own pixels would otherwise be sampled as the
    right-hand reference and simply painted back in."""
    px = im.load()
    x0, y0, x1, y1 = box
    span = y1 - y0
    for x in range(x0, x1):
        top = px[x, max(0, y0 - 2)]
        bot = px[x, min(im.height - 1, y1 + 1)]
        for i, y in enumerate(range(y0, y1)):
            t = i / max(1, span - 1)
            px[x, y] = tuple(round(top[c] + (bot[c] - top[c]) * t) for c in range(3))


def deepen(im, gain=0.94, desat=0.12):
    """Pull the vivid blues down slightly - moodier, and kinder to the copy."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.25 and v > 0.20:                 # only the saturated mid-tones
                s *= (1.0 - desat)
            r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v * gain)
            px[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255))


if __name__ == "__main__":
    im = Image.open(SRC).convert("RGB")
    for box in ARTIFACTS:
        inpaint(im, box)
    deepen(im)
    im.save("assets/masters/bg2-clean.jpg", quality=95)

    for w, tag in ((3840, ""), (1920, "-sm")):
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        dst = f"{OUT}/px-bg{tag}.webp"
        r.save(dst, "WEBP", quality=86, method=6)
        print("  %-24s %dx%d  %d bytes" % (dst, r.width, r.height, os.path.getsize(dst)))
