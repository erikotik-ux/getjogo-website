#!/usr/bin/env python
"""Clean the generated 4K backdrop and export the shipped sizes.

    cd D:/Business/GetJogo && python scripts/bg_finish.py

- paints out two stray glowing markers the model added to the main peak
- cools the warm cream cast off the lit snow so the scene stays moonlit
- exports 3840x1646 (desktop) and 1920x823 (mobile) WebP
"""
import colorsys
import os

from PIL import Image

SRC = "assets/masters/bg-4k-raw.jpg"
OUT = "public"

# stray glowing markers on the main peak, plus one lone cloud on the right
# (the drifting cloud layers are the only clouds the scene should have)
ARTIFACTS = [(2640, 900, 2770, 1060), (3560, 1090, 3690, 1240), (5240, 960, 5800, 1160)]


def inpaint(im, box):
    """Rebuild a box by interpolating each row between its outside neighbours."""
    px = im.load()
    x0, y0, x1, y1 = box
    span = x1 - x0
    for y in range(y0, y1):
        left = px[max(0, x0 - 2), y]
        right = px[min(im.width - 1, x1 + 1), y]
        for i, x in enumerate(range(x0, x1)):
            t = i / max(1, span - 1)
            px[x, y] = tuple(round(left[c] + (right[c] - left[c]) * t) for c in range(3))


def cool_snow(im):
    """Rotate the warm cream highlights back toward cool moonlit white."""
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if r <= b:                       # already cool, leave it
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if not (0.01 < h < 0.17 and s > 0.04):
                continue
            mix = min(1.0, s * 6.0)          # the warmer it is, the harder we pull
            nh = 0.58                        # cool blue
            ns = s * (1.0 - 0.55 * mix)
            r2, g2, b2 = colorsys.hsv_to_rgb(nh, ns, v)
            px[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255))


if __name__ == "__main__":
    im = Image.open(SRC).convert("RGB")
    for box in ARTIFACTS:
        inpaint(im, box)
    cool_snow(im)
    im.save("assets/masters/bg-4k-clean.jpg", quality=95)

    for w, tag in ((3840, ""), (1920, "-sm")):
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        dst = f"{OUT}/px-bg{tag}.webp"
        r.save(dst, "WEBP", quality=86, method=6)
        print("  %-24s %dx%d  %d bytes" % (dst, r.width, r.height, os.path.getsize(dst)))
