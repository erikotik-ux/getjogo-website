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
LEG = (178, 191, 182, 255)
LEG_FAR = (146, 160, 151, 255)
FOOT = (126, 140, 131, 255)

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


# ---------------------------------------------------------------- forest
FW, FH = 384, 200        # tiles horizontally; sky above is filled by CSS


def _pine(im, x, base, h, col, trunk=None):
    """Stepped pixel pine: tiers of decreasing width."""
    tiers = max(3, h // 12)
    for t in range(tiers):
        y0 = base - round(h * (t + 1) / tiers)
        y1 = base - round(h * t / tiers)
        for y in range(y0, y1 + 1):
            spread = (y - y0) / max(1, (y1 - y0))
            half = round((0.16 * h / tiers) * (1 + spread * 2.4) + t * 0.5)
            for dx in range(-half, half + 1):
                put(im, (x + dx) % im.width, y, col)
    if trunk:
        for y in range(base - 2, base + 4):
            for x2 in range(x - 1, x + 2):
                put(im, x2 % im.width, y, trunk)


def forest_bg():
    im = img(FW, FH)
    for y in range(FH):                       # night sky
        t = y / (FH - 1)
        c = tuple(round(SKY_HI[i] + (SKY_LO[i] - SKY_HI[i]) * t) for i in range(3))
        rect(im, 0, y, FW - 1, y, c + (255,))

    for i in range(46):                       # stars
        n = (math.sin(i * 91.7) * 43758.5453) % 1
        m = (math.sin(i * 27.3 + 4.1) * 24634.6345) % 1
        put(im, round(n * FW), round(m * 78), STAR)

    mx, my = 306, 34                          # moon with a soft glow
    for r in range(16, 9, -1):
        a = int(26 * (17 - r) / 7)
        for y in range(my - r, my + r + 1):
            for x in range(mx - r, mx + r + 1):
                if (x - mx) ** 2 + (y - my) ** 2 <= r * r:
                    px = im.getpixel((x % FW, y))
                    im.putpixel((x % FW, y), tuple(
                        min(255, px[j] + (MOON_GLOW[j] - px[j]) * a // 255) for j in range(3)) + (255,))
    disc(im, mx, my, 9, MOON)
    disc(im, mx - 3, my - 3, 3, (232, 244, 230, 255))

    for i in range(26):                       # far band
        x = round(i * FW / 26 + 5 * math.sin(i * 2.1))
        _pine(im, x, 132, 26 + round(14 * ((math.sin(i * 3.7) + 1) / 2)), F_FAR)
    for y in range(126, 142):                 # mist between bands
        for x in range(FW):
            if (math.sin(x * 0.11 + y * 0.7) + 1) / 2 > 0.86:
                put(im, x, y, MIST)

    for i in range(18):                       # mid band
        x = round(i * FW / 18 + 7 * math.sin(i * 1.3 + 2))
        _pine(im, x, 166, 40 + round(22 * ((math.sin(i * 2.3 + 1) + 1) / 2)), F_MID, F_TRUNK)

    for i in range(12):                       # near band
        x = round(i * FW / 12 + 9 * math.sin(i * 0.9 + 5))
        _pine(im, x, 200, 56 + round(30 * ((math.sin(i * 1.7 + 3) + 1) / 2)), F_NEAR, F_TRUNK)

    for y in range(FH - 22, FH):              # haze so it meets the platform
        a = (y - (FH - 22)) / 22
        for x in range(FW):
            px = im.getpixel((x, y))
            im.putpixel((x, y), tuple(round(px[j] + (F_NEAR[j] - px[j]) * a) for j in range(3)) + (255,))
    return im


# ---------------------------------------------------------------- mascot
# Mascot proportions, not animal anatomy: the head and its quills are the
# character. The body is a small athletic wedge tucked underneath.
CW, CH = 48, 34
FEET = 31
HEAD_X, HEAD_Y, HEAD_R = 30.0, 14.0, 9.0
BODY_X, BODY_Y, BODY_RX, BODY_RY = 22.0, 21.0, 8.2, 5.0
HIP_Y = 24.0
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
    elif smile:                                    # logo crescent: content
        rect(im, ex - 1, ey2 - 1, ex + 1, ey2 - 1, EYE)
        put(im, ex - 2, ey2, EYE)
        put(im, ex + 2, ey2, EYE)
        rect(im, ex - 1, ey2 + 1, ex + 1, ey2 + 1, EYE)
    else:
        rect(im, ex - 2, ey2 - 2, ex + 2, ey2 + 2, EYE)
        for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
            put(im, ex + dx, ey2 + dy, WHT)
        rect(im, ex + 1, ey2 - 2, ex + 2, ey2 - 1, WHT)   # glint
    if smile:
        put(im, hx + 6, round(hy + 4 - tilt * 1.4), NOSE)
        put(im, hx + 7, round(hy + 3 - tilt * 1.6), NOSE)


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
            foot_x = hip_x + swing * 3.8
            foot_y = FEET - round(lift * 3.6)
        else:
            swing, lift = 0.0, 0.0
            foot_x, foot_y = hip_x, FEET
        knee_x = (hip_x + foot_x) / 2 + 1.2 + swing * 0.7
        knee_y = (HIP_Y + foot_y) / 2 + 0.6 - lift * 0.8
        tone = LEG if near else LEG_FAR
        if near:                                                    # cut line
            _limb(im, hip_x, HIP_Y, knee_x, knee_y, 5.8, 5.2, OUTL)
            _limb(im, knee_x, knee_y, foot_x, foot_y - 1, 5.4, 4.6, OUTL)
        _limb(im, hip_x, HIP_Y, knee_x, knee_y, 4.4, 3.8, tone)     # thigh
        _limb(im, knee_x, knee_y, foot_x, foot_y - 1, 4.0, 3.2, tone)  # shin
        fx, fy = round(foot_x), round(foot_y)                       # planted pad
        if near:
            rect(im, fx - 3, fy - 2, fx + 3, fy + 1, OUTL)
        rect(im, fx - 2, fy - 2, fx + 2, fy, FOOT if near else LEG_FAR)
        rect(im, fx - 2, fy - 2, fx + 1, fy - 2, LEG if near else LEG_FAR)
        if running and lift < 0.12 and swing < -0.25:               # dust off the push
            put(im, round(hip_x - 6), FEET, DUST)
            put(im, round(hip_x - 9), FEET - 2, DUST)


def hog_stand(tilt=0.0, blink=False, ear_up=False, smile=False,
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
    idle = [                                        # look up at the card
        dict(tilt=0.0), dict(tilt=0.4), dict(tilt=0.8), dict(tilt=0.8, ear_up=True),
        dict(tilt=0.8, blink=True), dict(tilt=0.8, smile=True),
        dict(tilt=0.8, smile=True, ear_up=True), dict(tilt=0.4, smile=True),
    ]
    for i, kw in enumerate(idle):
        sheet.paste(hog_stand(**kw), (CW * i, CH * 3))
    return sheet


# ---------------------------------------------------------------- build
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, im in (("px-forest", forest_bg()), ("px-ground", ground_tile()),
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
    forest_bg().resize((FW * 3, FH * 3), Image.NEAREST).convert("RGB").save(f"{OUT}/_forest-preview.png")
    print("  previews -> public/_px-preview.png, public/_forest-preview.png")
