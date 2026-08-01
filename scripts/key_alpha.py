#!/usr/bin/env python
"""Chroma-key a magenta-backed render to a cropped RGBA PNG.

The kie.ai renders come back on a soft magenta gradient (hue ~326-331,
sat 0.67-0.81). The mascot's warmest pixel is the belly at hue ~7, so a
hue-band key separates them cleanly. Edge pixels get a soft alpha ramp
plus a despill pass so no magenta fringe survives on the quills.

  python key_alpha.py in.jpg out.png [--height 420]
"""
import argparse
import colorsys

from PIL import Image, ImageFilter

BG_HUE = 330.0 / 360.0
HUE_TOL = 22.0 / 360.0     # how far from magenta still counts as background
SAT_LO, SAT_HI = 0.20, 0.46  # score ramp -> soft edges
# the magenta backdrop bounces pink onto the fur; rotate those hues back to tan
WARM_TARGET = 30.0 / 360.0


def smoothstep(lo, hi, x):
    if x <= lo:
        return 0.0
    if x >= hi:
        return 1.0
    t = (x - lo) / (hi - lo)
    return t * t * (3 - 2 * t)


def hue_dist(h):
    d = abs(h - BG_HUE)
    return min(d, 1.0 - d)


def key(src, dst, height, warm=True):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    out = Image.new("RGBA", (w, h))
    op = out.load()

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            hh, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            # how much this pixel looks like the magenta backdrop
            score = s * (1.0 - min(1.0, hue_dist(hh) / HUE_TOL))
            a = 1.0 - smoothstep(SAT_LO, SAT_HI, score)
            if a <= 0.0:
                op[x, y] = (0, 0, 0, 0)
                continue
            # despill: magenta spill shows as R and B above G
            if r > g and b > g:
                spill = min(r - g, b - g) * (1.0 - a) * 0.9
                r = int(max(0, r - spill))
                b = int(max(0, b - spill))
            if warm:
                hh2, s2, v2 = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                deg = hh2 * 360.0
                # salmon/pink bounce sits either side of 0 deg; tan does not
                if (deg >= 334.0 or deg <= 19.0) and s2 > 0.18:
                    edge = min(1.0, (deg - 334.0) / 12.0 if deg >= 334.0
                               else (19.0 - deg) / 12.0)
                    mix = min(1.0, edge)
                    nh = (WARM_TARGET * mix) + (hh2 * (1.0 - mix))
                    ns = s2 * (1.0 - 0.45 * mix)
                    r2, g2, b2 = colorsys.hsv_to_rgb(nh, ns, v2)
                    r, g, b = int(r2 * 255), int(g2 * 255), int(b2 * 255)
            op[x, y] = (r, g, b, int(round(a * 255)))

    # tidy the matte: nibble 1px of fringe, then soften
    alpha = out.getchannel("A")
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
    out.putalpha(alpha)

    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    if height:
        ratio = height / out.height
        out = out.resize((max(1, round(out.width * ratio)), height), Image.LANCZOS)
    out.save(dst, "PNG", optimize=True)
    print("%s -> %s  %dx%d" % (src, dst, out.width, out.height))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--height", type=int, default=420)
    ap.add_argument("--no-warm", action="store_true")
    a = ap.parse_args()
    key(a.src, a.dst, a.height, warm=not a.no_warm)
