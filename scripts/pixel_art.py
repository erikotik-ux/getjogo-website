#!/usr/bin/env python
"""Author the hero's 16-bit layer: ground platform, props, tree band, mascot sheet.

Everything is drawn on an exact pixel grid (no anti-aliasing) so it stays crisp
under `image-rendering: pixelated`. Run:  python scripts/pixel_art.py
"""
import math
import os

from PIL import Image

OUT = "public"

# ---------------------------------------------------------------- palettes
T = (0, 0, 0, 0)
# mascot: mostly white, per the logo, with a dark forest outline
OUTL = (34, 48, 38, 255)
WHT = (255, 255, 255, 255)
SHD = (201, 211, 204, 255)
SHD2 = (170, 183, 174, 255)
EYE = (13, 20, 16, 255)
NOSE = (42, 100, 54, 255)
PINK = (232, 168, 168, 255)

# ground: Yoshi's Island / Link to the Past greens and dirt
G_LIT = (139, 219, 94, 255)
G_MID = (85, 175, 57, 255)
G_DRK = (50, 126, 40, 255)
G_EDG = (29, 83, 32, 255)
D_LIT = (165, 112, 63, 255)
D_MID = (124, 78, 42, 255)
D_DRK = (88, 54, 29, 255)
D_OUT = (56, 34, 15, 255)
PEB = (194, 140, 87, 255)


def img(w, h):
    return Image.new("RGBA", (w, h), T)


def put(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((int(x), int(y)), c)


def rect(im, x0, y0, x1, y1, c):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            put(im, x, y, c)


def disc(im, cx, cy, r, c):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(im, x, y, c)


def outline(im, c=OUTL):
    """Wrap every opaque run in a 1px dark border."""
    src = im.copy()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            if src.getpixel((x, y))[3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src.getpixel((nx, ny))[3]:
                    put(im, x, y, c)
                    break


# ---------------------------------------------------------------- ground
GW, GH = 64, 24          # tile art size; grass 0..8, dirt 9..23


def ground_tile():
    im = img(GW, GH)
    # periodic so the tile repeats seamlessly
    def top(x):
        return 2 + round(1.3 * math.sin(2 * math.pi * x / GW * 3)
                         + 0.9 * math.sin(2 * math.pi * x / GW * 7 + 1.1))

    for x in range(GW):
        t = top(x)
        rect(im, x, t, x, t + 1, G_LIT)          # lit blade tips
        rect(im, x, t + 2, x, 6, G_MID)
        rect(im, x, 7, x, 8, G_DRK)
        put(im, x, 9, G_EDG)
        rect(im, x, 10, x, GH - 1, D_MID)        # dirt body
        # a little sparkle on the grass
        if x % 11 == 3:
            put(im, x, t + 2, G_LIT)

    # dirt mottling + pebbles, kept off the seam so nothing is cut in half
    for x in range(GW):
        for y in range(10, GH):
            n = (math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1
            if n > 0.86:
                put(im, x, y, D_DRK)
            elif n < 0.10:
                put(im, x, y, D_LIT)
    for cx, cy, r in ((9, 15, 2), (26, 19, 2), (45, 14, 2), (56, 20, 1), (35, 22, 1)):
        disc(im, cx, cy, r, D_DRK)
        put(im, cx - 1, cy - 1, PEB)
    rect(im, 0, GH - 2, GW - 1, GH - 1, D_DRK)   # base shadow
    rect(im, 0, GH - 1, GW - 1, GH - 1, D_OUT)
    return im


# ---------------------------------------------------------------- props
def props_sheet():
    """32x24 cells: flower, tuft, question block, bush."""
    cw, ch, n = 32, 24, 4
    im = img(cw * n, ch)

    def cell(i):
        return i * cw

    # 0 flower
    ox = cell(0)
    rect(im, ox + 15, 14, ox + 15, 21, G_DRK)
    put(im, ox + 14, 17, G_MID); put(im, ox + 16, 16, G_MID)
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        put(im, ox + 15 + dx, 12 + dy, (232, 92, 96, 255))
    put(im, ox + 15, 12, (250, 214, 96, 255))

    # 1 grass tuft
    ox = cell(1)
    for i, (bx, hgt) in enumerate(((12, 5), (15, 8), (18, 6), (21, 4))):
        for k in range(hgt):
            put(im, ox + bx + (k // 3), 21 - k, G_MID if k < hgt - 2 else G_LIT)

    # 2 question block
    ox = cell(2)
    rect(im, ox + 8, 4, ox + 23, 19, (226, 160, 46, 255))
    rect(im, ox + 9, 5, ox + 22, 18, (247, 199, 74, 255))
    for c in (ox + 8, ox + 23):
        rect(im, c, 4, c, 19, (150, 92, 18, 255))
    rect(im, ox + 8, 4, ox + 23, 4, (150, 92, 18, 255))
    rect(im, ox + 8, 19, ox + 23, 19, (150, 92, 18, 255))
    for x, y in ((11, 6), (20, 6), (11, 17), (20, 17)):
        put(im, ox + x, y, (150, 92, 18, 255))
    q = ["..###..", ".#...#.", ".....#.", "...##..", "...#...", ".......", "...#..."]
    for r, row in enumerate(q):
        for c, ch_ in enumerate(row):
            if ch_ == "#":
                put(im, ox + 12 + c, 7 + r, (150, 92, 18, 255))

    # 3 bush
    ox = cell(3)
    disc(im, ox + 12, 19, 4, G_DRK)
    disc(im, ox + 17, 18, 5, G_DRK)
    disc(im, ox + 22, 20, 4, G_DRK)
    disc(im, ox + 16, 17, 3, G_MID)
    rect(im, ox + 6, 22, ox + 26, 23, T)
    return im


# ---------------------------------------------------------------- tree band
def tree_band():
    """Tiling pixel-pine silhouette that sits between plate and platform."""
    w, h = 128, 56
    im = img(w, h)
    dark = (18, 34, 24, 255)
    lite = (26, 48, 33, 255)
    for base, scale, tone in ((10, 1.0, dark), (46, 0.75, lite), (84, 1.15, dark), (116, 0.8, lite)):
        th = int(38 * scale)
        top = h - th
        tiers = 4
        for t in range(tiers):
            y0 = top + int(th * t / tiers)
            y1 = top + int(th * (t + 1) / tiers) + 1
            for y in range(y0, y1):
                half = int((y - top) * 0.42) - int(t * 1.2) + 2
                half = max(1, half)
                for x in range(base - half, base + half + 1):
                    put(im, x % w, min(y, h - 1), tone)
        rect(im, base - 1, h - 5, base + 1, h - 1, (30, 22, 14, 255))
    return im


# ---------------------------------------------------------------- mascot
CW, CH = 32, 26          # cell size; feet rest on y = 23
FEET = 23


def _spike(im, bx, by, tx, ty, halfw, col=WHT):
    """Filled triangle from a base segment to a tip - reads as one quill."""
    dx, dy = tx - bx, ty - by
    ln = max(1.0, math.hypot(dx, dy))
    nx, ny = -dy / ln, dx / ln          # perpendicular
    steps = int(ln) + 1
    for s_ in range(steps + 1):
        t = s_ / steps
        w = halfw * (1.0 - t)
        cx_, cy_ = bx + dx * t, by + dy * t
        k = int(w) + 1
        for j in range(-k, k + 1):
            if abs(j) <= w + 0.35:
                put(im, round(cx_ + nx * j), round(cy_ + ny * j), col)


def _ridge(im, cx, cy, rx, ry, phase=0.0, n=8):
    """Chunky spiked ridge sweeping back over the top of the body."""
    for i in range(n):
        a = math.pi * (0.06 + 0.90 * i / (n - 1))        # right -> over the top -> left
        bx = cx + math.cos(a) * rx * 0.72
        by = cy - math.sin(a) * ry * 0.72
        ln = 6.0 + 1.2 * math.sin(i * 1.9 + phase)
        tx = cx + math.cos(a + 0.34) * (rx * 0.72 + ln)
        ty = cy - math.sin(a + 0.34) * (ry * 0.72 + ln)
        _spike(im, bx, by, tx, ty, 2.3)


def _head(im, hx, hy, tilt=0.0, blink=False, ear_up=False):
    """Head, short snout, eye. tilt (0..1) lifts the muzzle to look up."""
    hy = hy - tilt * 1.4
    disc(im, hx, hy, 5, WHT)
    # short wedge snout, angled up with tilt
    for i in range(4):
        yy = hy + 1 - i * (0.30 + tilt * 1.05)
        half = 2 - (i // 2)
        rect(im, hx + 4 + i, round(yy) - half, hx + 4 + i, round(yy) + half - 1, WHT)
    nx_, ny_ = hx + 7, round(hy + 1 - 3 * (0.30 + tilt * 1.05)) - 1
    put(im, nx_, ny_, NOSE); put(im, nx_, ny_ + 1, NOSE)
    # ear
    ey = hy - 5 - (1 if ear_up else 0)
    rect(im, hx - 2, ey, hx, ey + 1, WHT)
    put(im, hx - 1, ey + 1, PINK)
    # eye: 2x2 with a glint so it reads at small size
    ex, ey2 = hx + 1, round(hy - 1 - tilt * 1.2)
    if blink:
        rect(im, ex - 1, ey2, ex + 1, ey2, EYE)
    else:
        rect(im, ex, ey2 - 1, ex + 1, ey2, EYE)
        put(im, ex + 1, ey2 - 1, WHT)


def _legs(im, phase, walking=True):
    if walking:
        f, b = math.sin(phase), math.sin(phase + math.pi)
        front, back = 16 + round(f * 2), 6 + round(b * 2)
        fh, bh = 4 - abs(round(f * 1.2)), 4 - abs(round(b * 1.2))
    else:
        front, back, fh, bh = 16, 6, 4, 4
    rect(im, front, FEET - fh, front + 1, FEET, SHD)
    rect(im, back, FEET - bh, back + 1, FEET, SHD)
    put(im, front, FEET - fh, WHT); put(im, back, FEET - bh, WHT)


def hog_stand(tilt=0.0, blink=False, ear_up=False, phase=0.0, walking=False, bob=0):
    im = img(CW, CH)
    cx, cy = 11, 15 - bob
    rx, ry = 8.0, 6.0
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                put(im, x, y, WHT)
    _ridge(im, cx, cy, rx, ry, phase)
    _head(im, 21, cy + 1, tilt, blink, ear_up)
    _legs(im, phase, walking)
    for x in range(int(cx - rx), int(cx + rx) + 1):     # underside shading, curved
        for y in range(int(cy), int(cy + ry) + 1):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 0.98 and im.getpixel((x, y))[:3] == WHT[:3]:
                if d > 0.74:
                    put(im, x, y, SHD2)
                elif d > 0.42:
                    put(im, x, y, SHD)
    outline(im)
    return im


def hog_ball(spin):
    im = img(CW, CH)
    cx, cy, r = 15, FEET - 8, 8
    disc(im, cx, cy, r, WHT)
    for i in range(12):
        a = spin + 2 * math.pi * i / 12
        bx, by = cx + math.cos(a) * r * 0.85, cy - math.sin(a) * r * 0.85
        tx, ty = cx + math.cos(a) * (r + 3.4), cy - math.sin(a) * (r + 3.4)
        _spike(im, bx, by, tx, ty, 1.7)
    for y in range(cy - r, cy + r + 1):             # orbiting shade sells the spin
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= (r - 1) ** 2:
                ang = math.atan2(cy - y, x - cx) - spin
                if math.cos(ang) < -0.30:
                    put(im, x, y, SHD)
                if math.cos(ang) < -0.75:
                    put(im, x, y, SHD2)
    outline(im)
    return im


def hog_uncurl(t):
    """t 0..1 : the ball flattens out and the head and legs emerge."""
    im = img(CW, CH)
    cx = 12
    rx = 8.0
    ry = 8 - 2.0 * t
    cy = FEET - 8 + t * 1.0
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                put(im, x, y, WHT)
    _ridge(im, cx, cy, rx, ry, phase=t * 3)
    if t > 0.40:
        _head(im, 21, cy + 1, 0, False, False)
    if t > 0.62:
        _legs(im, 0, walking=False)
    outline(im)
    return im


def hog_sheet():
    """rows: 0 roll(12) 1 uncurl(6) 2 walk(8) 3 idle(8)"""
    cols = 12
    sheet = img(CW * cols, CH * 4)

    for i in range(12):                                   # roll
        sheet.paste(hog_ball(-2 * math.pi * i / 12), (CW * i, 0))
    for i in range(6):                                    # uncurl
        sheet.paste(hog_uncurl((i + 1) / 6), (CW * i, CH))
    for i in range(8):                                    # walk
        ph = 2 * math.pi * i / 8
        sheet.paste(hog_stand(phase=ph, walking=True, bob=1 if i in (1, 2, 5, 6) else 0),
                    (CW * i, CH * 2))
    idle = [                                              # look up, blink, ear twitch
        dict(tilt=0.0), dict(tilt=0.35), dict(tilt=0.7), dict(tilt=0.7, ear_up=True),
        dict(tilt=0.7, blink=True), dict(tilt=0.7), dict(tilt=0.7, ear_up=True), dict(tilt=0.35),
    ]
    for i, kw in enumerate(idle):
        sheet.paste(hog_stand(**kw), (CW * i, CH * 3))
    return sheet


# ---------------------------------------------------------------- build
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, im in (("px-ground", ground_tile()), ("px-props", props_sheet()),
                     ("px-trees", tree_band()), ("px-hog", hog_sheet())):
        p = f"{OUT}/{name}.png"
        im.save(p, "PNG", optimize=True)
        print("  %-20s %dx%d  %d bytes" % (p, im.width, im.height, os.path.getsize(p)))

    # contact sheet for eyeballing
    s = 6
    prev = Image.new("RGBA", (CW * 12 * s, (CH * 4 + 34) * s), (14, 20, 16, 255))
    prev.paste(hog_sheet().resize((CW * 12 * s, CH * 4 * s), Image.NEAREST), (0, 0))
    g = ground_tile().resize((GW * s, GH * s), Image.NEAREST)
    for i in range(6):
        prev.paste(g, (GW * s * i, CH * 4 * s), g)
    pr = props_sheet().resize((32 * 4 * s, 24 * s), Image.NEAREST)
    prev.paste(pr, (0, (CH * 4 + 24) * s), pr)
    prev.convert("RGB").save(f"{OUT}/_px-preview.png")
    print("  preview -> public/_px-preview.png")
