#!/usr/bin/env python
"""Author the hero's 16-bit layer: forest backdrop, ground, props, mascot sheet.

Everything is drawn on an exact pixel grid (no anti-aliasing) so it stays crisp
under `image-rendering: pixelated`.

    cd D:/Business/GetJogo && python scripts/pixel_art.py
"""
import math
import os

from PIL import Image

OUT = "public"

# ---------------------------------------------------------------- palettes
T = (0, 0, 0, 0)
# mascot: the logo hedgehog inverted - white quills split by dark cut lines
OUTL = (26, 38, 30, 255)
WHT = (255, 255, 255, 255)
SHD = (203, 214, 206, 255)
SHD2 = (168, 182, 172, 255)
EYE = (18, 26, 21, 255)
NOSE = (34, 44, 38, 255)
PINK = (233, 170, 170, 255)
LEG = (255, 255, 255, 255)        # near leg reads as body, not a grey stick
LEG_FAR = (196, 208, 199, 255)    # far leg only a shade back
FOOT = (176, 190, 180, 255)
ARM = (241, 247, 243, 255)        # a hair off white so the near arm separates

# ground
G_LIT = (139, 219, 94, 255)
G_MID = (85, 175, 57, 255)
G_DRK = (50, 126, 40, 255)
G_EDG = (29, 83, 32, 255)
D_LIT = (165, 112, 63, 255)
D_MID = (124, 78, 42, 255)
D_DRK = (88, 54, 29, 255)
D_OUT = (56, 34, 15, 255)
PEB = (194, 140, 87, 255)

# forest backdrop: dark, cool, brand-adjacent greens
SKY_HI = (9, 17, 16, 255)
SKY_LO = (16, 32, 26, 255)
MOON = (226, 240, 220, 255)
MOON_GLOW = (72, 112, 90, 255)
F_FAR = (28, 54, 43, 255)
F_MID = (20, 40, 32, 255)
F_NEAR = (12, 25, 19, 255)
F_TRUNK = (17, 30, 22, 255)
MIST = (30, 54, 45, 255)
STAR = (168, 198, 180, 255)


def img(w, h, fill=T):
    return Image.new("RGBA", (w, h), fill)


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


def _spike(im, bx, by, tx, ty, halfw, col, taper=1.0):
    """Filled triangle from a base segment to a tip.

    taper < 1 keeps the spike broad for most of its run before it points,
    which is what makes the quills read as a solid mass rather than hair.
    """
    dx, dy = tx - bx, ty - by
    ln = max(1.0, math.hypot(dx, dy))
    nx, ny = -dy / ln, dx / ln
    steps = int(ln) + 1
    for s in range(steps + 1):
        t = s / steps
        w = halfw * (1.0 - t) ** taper
        cx, cy = bx + dx * t, by + dy * t
        k = int(w) + 1
        for j in range(-k, k + 1):
            if abs(j) <= w + 0.35:
                put(im, round(cx + nx * j), round(cy + ny * j), col)


# ---------------------------------------------------------------- ground
GW, GH = 64, 24


def ground_tile():
    im = img(GW, GH)

    def top(x):
        return 2 + round(1.3 * math.sin(2 * math.pi * x / GW * 3)
                         + 0.9 * math.sin(2 * math.pi * x / GW * 7 + 1.1))

    for x in range(GW):
        t = top(x)
        rect(im, x, t, x, t + 1, G_LIT)
        rect(im, x, t + 2, x, 6, G_MID)
        rect(im, x, 7, x, 8, G_DRK)
        put(im, x, 9, G_EDG)
        rect(im, x, 10, x, GH - 1, D_MID)
        if x % 11 == 3:
            put(im, x, t + 2, G_LIT)

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
    rect(im, 0, GH - 2, GW - 1, GH - 1, D_DRK)
    rect(im, 0, GH - 1, GW - 1, GH - 1, D_OUT)
    return im


# ---------------------------------------------------------------- props
MUSH_CAP = (206, 74, 68, 255)
MUSH_SPOT = (242, 168, 158, 255)
MUSH_STEM = (238, 228, 206, 255)
ROCK_LIT = (120, 130, 124, 255)
ROCK_MID = (88, 98, 93, 255)
ROCK_DRK = (56, 66, 62, 255)
PETAL_A = (232, 92, 96, 255)
PETAL_B = (238, 196, 92, 255)
PETAL_C = (176, 154, 226, 255)
PROP_N = 6


def props_sheet():
    """32x24 cells: tuft, red flowers, yellow flowers, bush, mushrooms, rocks."""
    cw, ch = 32, 24
    im = img(cw * PROP_N, ch)

    def c(i):
        return i * cw

    ox = c(0)                                   # grass tuft
    for bx, hgt, lean in ((11, 6, 0), (14, 9, 1), (17, 11, 0), (20, 8, -1), (23, 5, 1)):
        for k in range(hgt):
            put(im, ox + bx + round(lean * k / 3), 21 - k, G_LIT if k > hgt - 3 else G_MID)

    for idx, petal in ((1, PETAL_A), (2, PETAL_B)):   # flowers
        ox = c(idx)
        rect(im, ox + 14, 13, ox + 14, 21, G_DRK)
        put(im, ox + 13, 17, G_MID)
        put(im, ox + 15, 15, G_MID)
        for dx, dy in ((0, -2), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 2)):
            put(im, ox + 14 + dx, 12 + dy, petal)
        put(im, ox + 14, 12, (252, 238, 176, 255))
        rect(im, ox + 20, 16, ox + 20, 21, G_DRK)
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            put(im, ox + 20 + dx, 15 + dy, PETAL_C if idx == 2 else petal)
        put(im, ox + 20, 15, (252, 238, 176, 255))

    ox = c(3)                                   # bush
    disc(im, ox + 12, 19, 4, G_DRK)
    disc(im, ox + 17, 17, 5, G_DRK)
    disc(im, ox + 22, 19, 4, G_DRK)
    disc(im, ox + 16, 16, 3, G_MID)
    disc(im, ox + 21, 18, 2, G_MID)
    for x, y in ((14, 15), (19, 13), (24, 17)):
        put(im, ox + x, y, G_LIT)
    rect(im, ox + 5, 22, ox + 27, 23, T)

    ox = c(4)                                   # mushrooms
    rect(im, ox + 13, 17, ox + 15, 21, MUSH_STEM)
    for w, y in ((5, 13), (7, 14), (7, 15), (5, 16)):
        rect(im, ox + 14 - w // 2, y, ox + 14 + w // 2, y, MUSH_CAP)
    put(im, ox + 12, 14, MUSH_SPOT)
    put(im, ox + 16, 15, MUSH_SPOT)
    rect(im, ox + 21, 19, ox + 22, 21, MUSH_STEM)
    for w, y in ((3, 17), (5, 18)):
        rect(im, ox + 21 - w // 3, y, ox + 21 + w // 2, y, MUSH_CAP)
    put(im, ox + 22, 18, MUSH_SPOT)

    ox = c(5)                                   # rocks
    for cx, cy, r in ((13, 19, 4), (21, 20, 3)):
        disc(im, ox + cx, cy, r, ROCK_MID)
        disc(im, ox + cx - 1, cy - 1, max(1, r - 2), ROCK_LIT)
        for x in range(ox + cx - r, ox + cx + r + 1):
            put(im, x, cy + r - 1, ROCK_DRK)
    rect(im, ox + 5, 22, ox + 28, 23, T)
    return im


# ---------------------------------------------------------------- landscape
# Four tiling layers so the sky can hold still while two cloud bands drift
# behind the peaks: sky -> clouds A -> clouds B -> land.
SW, SH = 384, 200

SKY_TOP = (9, 14, 32)
SKY_MID = (16, 26, 54)
SKY_LOW = (28, 44, 78)
SKY_HORIZON = (44, 64, 104)
STAR_HI = (204, 218, 242, 255)
STAR_LO = (108, 128, 168, 255)
WISP = (22, 36, 68, 255)

# atmospheric perspective: distant ranges sit lighter and bluer
RANGES = [
    # (base_y, height, lit, shade, snow, snow_shade)
    (150, 46, (58, 78, 118), (46, 62, 98), (128, 148, 184), (100, 120, 158)),
    (163, 62, (44, 60, 96), (32, 46, 78), (156, 176, 208), (118, 140, 176)),
    (176, 78, (32, 46, 76), (21, 32, 57), (186, 204, 230), (140, 162, 196)),
]
FOREST = [
    (181, (30, 56, 58), 26),
    (190, (22, 45, 47), 22),
    (200, (15, 33, 35), 18),
]
PINE_FG = (11, 26, 27, 255)
PINE_FG_LIT = (19, 41, 40, 255)
PINE_TRUNK = (16, 20, 19, 255)

# tuned against the generated plate: the sky at cloud altitude runs
# (0,7,61) to (0,23,93), so these sit just above it, cool and deep
CLOUD_LIT = (56, 82, 134, 255)
CLOUD_MID = (37, 57, 102, 255)
CLOUD_DARK = (23, 39, 76, 255)


def _vgrad(im, y0, y1, top, bot):
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        rect(im, 0, y, im.width - 1, y,
             tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))


def sky_layer():
    im = img(SW, SH)
    _vgrad(im, 0, 90, SKY_TOP, SKY_MID)
    _vgrad(im, 90, 150, SKY_MID, SKY_LOW)
    _vgrad(im, 150, SH, SKY_LOW, SKY_HORIZON)

    for i in range(120):                          # stars, two brightnesses
        n = (math.sin(i * 91.7) * 43758.5453) % 1
        m = (math.sin(i * 27.3 + 4.1) * 24634.6345) % 1
        b = (math.sin(i * 13.9 + 1.7) * 12543.2318) % 1
        y = round(m * 128)
        put(im, round(n * SW), y, STAR_HI if b > 0.72 else STAR_LO)

    for i in range(5):                            # very faint high haze
        wy = 42 + round(((math.sin(i * 5.1) + 1) / 2) * 62)
        wx = round(((math.sin(i * 2.7 + 1) + 1) / 2) * SW)
        wl = 70 + round(((math.sin(i * 3.3) + 1) / 2) * 90)
        for k in range(wl):
            x = (wx + k) % SW
            edge = min(k, wl - k) / (wl * 0.4)     # fade both ends
            if edge > 0.55 and (math.sin(k * 0.09 + i) + 1) / 2 > 0.5:
                base = im.getpixel((x, wy))
                put(im, x, wy, tuple(min(255, base[j] + 8) for j in range(3)) + (255,))
    return im


def _peak(im, x, base, h, half, lit, shade, snow, snow_sh, lean=1.0):
    """One mountain: lit left face, shadowed right face, snow cap with gullies."""
    for dy in range(h):
        y = base - h + dy
        if y < 0 or y >= im.height:
            continue
        prog = (dy / h) ** 0.92
        wl = int(half * lean * prog)                  # asymmetric flanks
        wr = int(half * (2.0 - lean) * prog)
        w = max(wl, wr)
        ridge = int(1.8 * math.sin(dy * 0.34) + 1.1 * math.sin(dy * 0.11 + 1.3))
        for dx in range(-wl, wr + 1):
            # snowline undulates gently across the face so the cap ends in a
            # few soft tongues rather than a comb of icicles
            cap = h * 0.26 * (1.0 + 0.34 * math.sin(dx * 0.15 + x * 0.5)
                              + 0.16 * math.sin(dx * 0.31 + 1.7))
            snowy = dy < cap
            left = dx < ridge
            if snowy:
                col = snow if left else snow_sh
            else:
                col = lit if left else shade
            put(im, (x + dx) % im.width, y, col + (255,))
        # a darker gully beside the ridge, plus faint rock mottling
        if w > 2:
            put(im, (x + ridge + 1) % im.width, y,
                tuple(round(c * 0.86) for c in shade) + (255,))
            if dy % 5 == 2:
                mx = int(w * 0.55 * math.sin(dy * 0.7 + x))
                if abs(mx) < w:
                    src = lit if mx < ridge else shade
                    put(im, (x + mx) % im.width, y,
                        tuple(round(c * 0.92) for c in src) + (255,))


def _pine(im, x, base, h, col, lit=None, trunk=None):
    """Layered conifer: stacked tiers, slight asymmetry, optional lit edge."""
    tiers = max(4, h // 7)
    for t in range(tiers):
        y0 = base - round(h * (t + 1) / tiers)
        y1 = base - round(h * t / tiers)
        for y in range(y0, y1 + 1):
            if y < 0 or y >= im.height:
                continue
            f = (y - y0) / max(1, y1 - y0)
            half = round((0.15 * h / tiers) * (1 + f * 3.0) + t * 0.62)
            half = max(1, half)
            for dx in range(-half, half + 1):
                put(im, (x + dx) % im.width, y, col)
            if lit:                                # light catches the left edge
                put(im, (x - half) % im.width, y, lit)
    if trunk:
        for y in range(base - 3, base + 2):
            for dx in (-1, 0, 1):
                put(im, (x + dx) % im.width, y, trunk)


def land_layer():
    """Mountains + forest bands + foreground pines, transparent above."""
    im = img(SW, SH)

    for ri, (base, h, lit, shade, snow, snow_sh) in enumerate(RANGES):
        n = (7, 6, 5)[ri]
        for i in range(n):
            jitter = math.sin(i * 3.1 + ri * 2.2)
            x = round((i + 0.5) * SW / n + 14 * jitter)
            ph = round(h * (0.72 + 0.42 * ((math.sin(i * 2.3 + ri) + 1) / 2)))
            half = round(ph * (0.78 + 0.24 * ((math.sin(i * 1.7 + ri * 3) + 1) / 2)))
            lean = 0.80 + 0.42 * ((math.sin(i * 4.1 + ri * 1.9) + 1) / 2)
            _peak(im, x, base, ph, half, lit, shade, snow, snow_sh, lean)

    for band, (base, col, hgt) in enumerate(FOREST):   # dense receding treelines
        step = 5 - band
        for x in range(0, SW, step):
            hh = hgt + round(6 * math.sin(x * 0.21 + band * 2.4)
                             + 4 * math.sin(x * 0.07 + band))
            _pine(im, x, base, hh, col + (255,))
        rect(im, 0, base, SW - 1, min(SH - 1, base + 3), col + (255,))

    for i in range(13):                                # detailed foreground pines
        x = round((i + 0.5) * SW / 13 + 9 * math.sin(i * 1.9 + 4))
        hh = 48 + round(30 * ((math.sin(i * 1.31 + 2) + 1) / 2))
        _pine(im, x, SH - 2, hh, PINE_FG, PINE_FG_LIT, PINE_TRUNK)
    return im


CLOUD_CELL_W, CLOUD_CELL_H, CLOUD_BASE = 64, 26, 20

# seven silhouettes: (dx, dy, radius) lobes, each a different shape and mass
CLOUD_SHAPES = [
    [(-4, 0, 3), (1, -1, 4), (6, 0, 3)],                                  # 0 wisp
    [(-7, 1, 4), (-1, -2, 5), (5, 0, 4), (10, 1, 3)],                     # 1 small
    [(-11, 1, 4), (-5, -2, 6), (2, -1, 5), (8, 0, 5), (14, 1, 4)],        # 2 wide low
    [(-6, 2, 4), (-1, -4, 6), (5, -1, 5), (10, 2, 4)],                    # 3 tall puff
    [(-2, 0, 3), (2, -1, 4)],                                             # 4 tiny
    [(-14, 2, 4), (-7, -2, 6), (0, -5, 7), (7, -2, 6), (14, 2, 4)],       # 5 large
    [(-5, -3, 5), (1, 0, 4), (6, 1, 3), (11, 2, 3), (15, 2, 2)],          # 6 trailing
]


def _lobe(im, cx, cy, r):
    disc(im, cx, cy, r, CLOUD_MID)
    disc(im, cx - max(1, r * 0.2), cy - max(1, r * 0.36), max(1, r * 0.72), CLOUD_LIT)


def clouds_sheet():
    """One row of seven cells, each holding a distinct cloud."""
    im = img(CLOUD_CELL_W * len(CLOUD_SHAPES), CLOUD_CELL_H)
    for i, lobes in enumerate(CLOUD_SHAPES):
        ox = i * CLOUD_CELL_W + CLOUD_CELL_W // 2
        for dx, dy, r in lobes:
            _lobe(im, ox + dx, CLOUD_BASE - 4 + dy, r)
        xs = [ox + dx for dx, _, _ in lobes]
        rs = [r for _, _, r in lobes]
        x0 = min(x - r for x, r in zip(xs, rs))
        x1 = max(x + r for x, r in zip(xs, rs))
        rect(im, x0, CLOUD_BASE - 1, x1, CLOUD_BASE, CLOUD_MID)       # flat base
        rect(im, x0, CLOUD_BASE + 1, x1, CLOUD_BASE + 1, CLOUD_DARK)  # shaded underside
        for x in range(x0, x1 + 1):                                   # soften the ends
            if x < x0 + 2 or x > x1 - 2:
                put(im, x, CLOUD_BASE + 1, T)
    return im


# ---------------------------------------------------------------- mascot
# Mascot proportions, not animal anatomy: the head and its quills are the
# character. The body is a small athletic wedge tucked underneath.
CW, CH = 48, 34
FEET = 31
HEAD_X, HEAD_Y, HEAD_R = 30.0, 14.0, 9.0
BODY_X, BODY_Y, BODY_RX, BODY_RY = 22.0, 21.0, 8.2, 5.0
HIP_Y = 25.0
HIP_BACK, HIP_FRONT = 17.0, 26.0

# Long quills fanning off the BACK OF THE HEAD, exactly like the logo mark.
# (angle as a fraction of pi, length, half-width)
QUILLS = [
    (0.38, 12.5, 3.8),
    (0.55, 15.5, 4.6),
    (0.72, 16.5, 4.8),
    (0.89, 14.5, 4.2),
    (1.06, 11.5, 3.4),
]
SWEEP = 0.26                     # extra backward lean on every quill
FLAT = 0.46                      # keeps the fan swept back rather than upright
DUST = (196, 210, 198, 255)


def _quill_set(im, cx, cy, r, phase=0.0, gust=0.0):
    """Each quill is drawn twice - a fatter dark pass, then white - so every
    spike keeps its own cut line, like the white separations in the logo."""
    for i, (frac, ln, hw) in enumerate(QUILLS):
        a = math.pi * frac
        bx = cx + math.cos(a) * r * 0.94
        by = cy - math.sin(a) * r * 0.94
        wob = 0.8 * math.sin(i * 1.7 + phase) + gust * (0.4 + 0.6 * i / len(QUILLS))
        sw = a + SWEEP
        tx = cx + math.cos(sw) * (r * 0.94 + ln + wob)
        ty = cy - math.sin(sw) * (r * 0.94 + (ln + wob) * FLAT)
        d = math.hypot(tx - bx, ty - by) or 1
        ex, ey = tx + (tx - bx) / d * 1.4, ty + (ty - by) / d * 1.4
        _spike(im, bx, by, ex, ey, hw + 1.2, OUTL, taper=0.72)
        _spike(im, bx, by, tx, ty, hw, WHT, taper=0.72)


def _face(im, hx, hy, tilt=0.0, blink=False, ear_up=False, smile=False):
    """Big head, short blunt snout, oversized eye."""
    hy -= tilt * 2.0
    disc(im, hx, hy, HEAD_R, WHT)
    step = 0.9 + tilt * 1.9                        # short blunt snout
    for i in range(4):
        yy = hy + 2 - i * step
        half = 4 - i
        rect(im, hx + 7 + i, round(yy) - half, hx + 7 + i, round(yy) + max(0, half - 2), WHT)
    nx, ny = hx + 11, round(hy + 2 - 3 * step)
    rect(im, nx, ny - 1, nx, ny, NOSE)

    ey = hy - HEAD_R - 1 - (1 if ear_up else 0)    # small swept ear
    _spike(im, hx - 1, hy - HEAD_R + 2, hx - 4, ey, 2.4, WHT)
    put(im, hx - 3, ey + 3, PINK)

    ex, ey2 = hx + 2, round(hy - 2 - tilt * 1.4)   # oversized mascot eye
    if blink:
        rect(im, ex - 2, ey2 + 1, ex + 2, ey2 + 1, EYE)
    elif smile:                                    # cheerful upturned arc
        for dx, dy in ((-2, 1), (-1, 0), (0, -1), (1, 0), (2, 1)):
            put(im, ex + dx, ey2 + dy, EYE)
            put(im, ex + dx, ey2 + dy + 1, EYE)
    else:
        rect(im, ex - 2, ey2 - 2, ex + 2, ey2 + 2, EYE)
        for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            put(im, ex + dx, ey2 + dy, WHT)
        rect(im, ex + 1, ey2 - 2, ex + 2, ey2 - 1, WHT)   # glint
    if smile:
        my = round(hy + 3 - tilt * 1.5)            # upward curve on the muzzle
        for dx, dy in ((2, 0), (3, 1), (4, 2), (5, 2), (6, 1), (7, 0)):
            put(im, hx + dx, my + dy, EYE)
            put(im, hx + dx, my + dy + 1, EYE)
        cy2 = round(hy + 1 - tilt * 1.2)           # delighted blush
        rect(im, hx - 3, cy2, hx - 2, cy2, PINK)


def _limb(im, x0, y0, x1, y1, w0, w1, col):
    """Thick tapered segment - a limb with weight, not a hairline."""
    d = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / d, (x1 - x0) / d
    steps = int(d) + 1
    for s in range(steps + 1):
        t = s / steps
        w = (w0 + (w1 - w0) * t) / 2.0
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        k = int(w) + 1
        for j in range(-k, k + 1):
            if abs(j) <= w + 0.25:
                put(im, round(cx + nx * j), round(cy + ny * j), col)


def _legs(im, phase, running=True):
    """Short, chunky, jointed legs. The foot pad plants flat on the ground
    and the knee leads the swing so the stride reads at a glance."""
    # far leg first in a darker tone, near leg over it with its own dark edge,
    # so the two limbs stay readable instead of merging into one grey mass
    for hip_x, off, near in ((HIP_BACK, math.pi, False), (HIP_FRONT, 0.0, True)):
        if running:
            swing = math.cos(phase + off)
            lift = max(0.0, math.sin(phase + off))
            foot_x = hip_x + swing * 3.4
            foot_y = FEET - round(lift * 3.2)
        else:
            swing, lift = 0.0, 0.0
            foot_x, foot_y = hip_x, FEET
        knee_x = (hip_x + foot_x) / 2 + 1.2 + swing * 0.7
        knee_y = (HIP_Y + foot_y) / 2 + 0.6 - lift * 0.8
        tone = LEG if near else LEG_FAR
        if near:                                                    # cut line
            _limb(im, hip_x, HIP_Y, knee_x, knee_y, 5.8, 5.2, OUTL)
            _limb(im, knee_x, knee_y, foot_x, foot_y - 1, 5.4, 4.6, OUTL)
        _limb(im, hip_x, HIP_Y, knee_x, knee_y, 5.2, 4.4, tone)     # thigh
        _limb(im, knee_x, knee_y, foot_x, foot_y - 1, 4.6, 3.8, tone)  # shin
        if near:                                                    # inner shading
            _limb(im, knee_x, knee_y + 1, foot_x, foot_y - 1, 2.0, 1.6, SHD)
        fx, fy = round(foot_x), round(foot_y)                       # planted pad
        if near:
            rect(im, fx - 3, fy - 2, fx + 3, fy + 1, OUTL)
        rect(im, fx - 3, fy - 2, fx + 2, fy, LEG if near else LEG_FAR)
        rect(im, fx - 3, fy, fx + 2, fy, FOOT)
        if running and lift < 0.12 and swing < -0.25:               # dust off the push
            put(im, round(hip_x - 6), FEET, DUST)
            put(im, round(hip_x - 9), FEET - 2, DUST)


SHOULDER = (23.0, 24.0)


def _arm(im, phase, running=True, pose=None):
    """One small near-side arm. Drawn after the head so a raised paw reads
    clearly instead of disappearing behind the big head."""
    sx, sy = SHOULDER
    if pose == "raise":                       # paw lifted toward the card
        ex, ey, px_, py = sx + 2.4, sy - 1.4, sx + 5.8, sy - 4.2
    elif pose == "chest":                     # paw tucked against the chest
        ex, ey, px_, py = sx + 2.4, sy + 0.4, sx + 4.2, sy - 2.0
    elif running:
        sw = math.sin(phase + 0.9)            # counter-swings the near leg
        ex, ey = sx + 1.4 + sw * 1.6, sy + 1.8
        px_, py = sx + 1.8 + sw * 3.0, sy + 3.4
    else:
        ex, ey, px_, py = sx + 1.2, sy + 2.0, sx + 1.6, sy + 3.6
    # a generous dark pass first: white-on-white needs a real cut line
    _limb(im, sx, sy, ex, ey, 5.8, 5.2, OUTL)
    _limb(im, ex, ey, px_, py, 5.2, 4.6, OUTL)
    rect(im, round(px_) - 2, round(py) - 2, round(px_) + 2, round(py) + 2, OUTL)
    _limb(im, sx, sy, ex, ey, 4.4, 3.8, ARM)
    _limb(im, ex, ey, px_, py, 3.8, 3.2, ARM)
    rect(im, round(px_) - 1, round(py) - 1, round(px_) + 1, round(py) + 1, ARM)
    _limb(im, sx, sy + 1.4, ex, ey + 1.4, 1.6, 1.4, SHD)          # underside
    put(im, round(px_) + 1, round(py) + 1, SHD)


def hog_stand(tilt=0.0, blink=False, ear_up=False, smile=False, arm=None,
              phase=0.0, running=False, bob=0, lean=0.0):
    im = img(CW, CH)
    bx, by = BODY_X + lean * 3, BODY_Y - bob
    hx, hy = HEAD_X + lean * 4, HEAD_Y - bob
    _legs(im, phase, running)                                       # hips hide under the body
    for y in range(int(by - BODY_RY - 1), int(by + BODY_RY + 2)):   # compact body
        for x in range(int(bx - BODY_RX - 1), int(bx + BODY_RX + 2)):
            sx = x - (by - y) * lean
            if ((sx - bx) / BODY_RX) ** 2 + ((y - by) / BODY_RY) ** 2 <= 1.0:
                put(im, x, y, WHT)
    disc(im, hx, hy, HEAD_R, WHT)                                   # head mass
    _quill_set(im, hx, hy, HEAD_R, phase, gust=lean * 3.2)          # cut lines on top
    _face(im, hx, hy, tilt, blink, ear_up, smile)
    _arm(im, phase, running, arm)                                   # in front of the head
    for x in range(int(bx - BODY_RX), int(bx + BODY_RX) + 1):       # belly shading
        for y in range(int(by), int(by + BODY_RY) + 1):
            d = ((x - bx) / BODY_RX) ** 2 + ((y - by) / BODY_RY) ** 2
            if d <= 0.98 and im.getpixel((x, y))[:3] == WHT[:3]:
                if d > 0.80:
                    put(im, x, y, SHD)
    outline(im)
    return im


def hog_ball(spin, streaks=True):
    im = img(CW, CH)
    cx, cy, r = 24, FEET - 12, 9.5
    disc(im, cx, cy, r, WHT)
    for i in range(11):
        a = spin + 2 * math.pi * i / 11
        qx, qy = cx + math.cos(a) * r * 0.92, cy - math.sin(a) * r * 0.92
        tx = cx + math.cos(a + 0.38) * (r + 6.0)
        ty = cy - math.sin(a + 0.38) * (r + 6.0)
        d = math.hypot(tx - qx, ty - qy) or 1
        _spike(im, qx, qy, tx + (tx - qx) / d * 1.4, ty + (ty - qy) / d * 1.4, 3.8, OUTL, taper=0.78)
        _spike(im, qx, qy, tx, ty, 2.8, WHT, taper=0.78)
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= (r - 1) ** 2:
                ang = math.atan2(cy - y, x - cx) - spin
                if math.cos(ang) < -0.30:
                    put(im, x, y, SHD)
                if math.cos(ang) < -0.75:
                    put(im, x, y, SHD2)
    outline(im)
    if streaks:                                    # speed lines trailing behind
        for k, sy in enumerate((cy - 5, cy, cy + 5)):
            ln = (6, 9, 5)[k]
            x0 = int(cx - r - 5 - (k % 2) * 3)
            for x in range(x0 - ln, x0):
                if (x + k) % 2 == 0:
                    put(im, x, int(sy), DUST)
    return im


def hog_uncurl(t):
    """Ball opens up: the head rises out and the body settles underneath."""
    im = img(CW, CH)
    cy = (FEET - 12) + (HEAD_Y - (FEET - 12)) * t
    cx = 24 + (HEAD_X - 24) * t
    r = 9.5 + (HEAD_R - 9.5) * t
    if t > 0.45:
        k = (t - 0.45) / 0.55
        by, brx, bry = BODY_Y, BODY_RX * k, BODY_RY * k
        for y in range(int(by - bry - 1), int(by + bry + 2)):
            for x in range(int(BODY_X - brx - 1), int(BODY_X + brx + 2)):
                if brx > 0 and ((x - BODY_X) / brx) ** 2 + ((y - by) / bry) ** 2 <= 1.0:
                    put(im, x, y, WHT)
    disc(im, cx, cy, r, WHT)
    _quill_set(im, cx, cy, r, phase=t * 3)
    if t > 0.45:
        _face(im, cx, cy)
    if t > 0.70:
        _legs(im, 0, running=False)
    outline(im)
    return im


def hog_sheet():
    """rows: 0 roll(12) 1 uncurl(6) 2 run(8) 3 idle(8)"""
    cols = 12
    sheet = img(CW * cols, CH * 4)
    for i in range(12):
        sheet.paste(hog_ball(-2 * math.pi * i / 12), (CW * i, 0))
    for i in range(6):
        sheet.paste(hog_uncurl((i + 1) / 6), (CW * i, CH))
    for i in range(8):                              # run: leaning, bobbing
        ph = 2 * math.pi * i / 8
        sheet.paste(hog_stand(phase=ph, running=True, lean=0.30,
                              bob=1 if i in (1, 2, 5, 6) else 0),
                    (CW * i, CH * 2))
    idle = [                                        # arrive, notice, warm up, settle
        dict(tilt=0.0),
        dict(tilt=0.4, arm="chest"),
        dict(tilt=0.8, arm="chest"),
        dict(tilt=0.8, arm="chest", ear_up=True),
        dict(tilt=0.8, arm="chest", blink=True),
        dict(tilt=1.0, arm="raise", smile=True),
        dict(tilt=1.0, arm="raise", smile=True, ear_up=True),
        dict(tilt=0.6, arm="chest", smile=True),
    ]
    for i, kw in enumerate(idle):
        sheet.paste(hog_stand(**kw), (CW * i, CH * 3))
    return sheet


# ---------------------------------------------------------------- build
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, im in (("px-clouds", clouds_sheet()), ("px-ground", ground_tile()),
                     ("px-props", props_sheet()), ("px-hog", hog_sheet())):
        p = f"{OUT}/{name}.png"
        im.save(p, "PNG", optimize=True)
        print("  %-20s %dx%d  %d bytes" % (p, im.width, im.height, os.path.getsize(p)))

    s = 6
    prev = Image.new("RGBA", (CW * 12 * s, (CH * 4 + 26) * s), (14, 20, 16, 255))
    prev.paste(hog_sheet().resize((CW * 12 * s, CH * 4 * s), Image.NEAREST), (0, 0))
    pr = props_sheet().resize((32 * PROP_N * s, 24 * s), Image.NEAREST)
    prev.paste(pr, (0, CH * 4 * s), pr)
    prev.convert("RGB").save(f"{OUT}/_px-preview.png")
    cs_ = clouds_sheet()
    prev2 = Image.new("RGBA", (cs_.width, cs_.height), (4, 12, 46, 255))
    prev2.alpha_composite(cs_)
    prev2.resize((cs_.width * 5, cs_.height * 5), Image.NEAREST).convert("RGB").save(f"{OUT}/_clouds-preview.png")
    print("  previews -> public/_px-preview.png, public/_clouds-preview.png")
