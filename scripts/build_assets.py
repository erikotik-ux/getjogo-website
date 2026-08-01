#!/usr/bin/env python
"""Rebuild every shipped hero asset from the kie.ai masters.

    python scripts/build_assets.py

masters (assets/masters/, generated once via scripts/kie.py)
  hero-forest.jpg    6048x2592 forest plate
  hog-*-raw.jpg      1024x1024 mascot renders on a magenta backdrop

ships (public/)
  hero-forest.webp / hero-forest-sm.webp
  hog-ball.webp / hog-stand.webp / hog-look.webp
"""
import os

from PIL import Image

from key_alpha import key

M, OUT = "assets/masters", "public"
ALPHA_FLOOR = 28
# night grade so the mascot sits in the moonlit plate instead of on top of it
GAIN = (0.62, 0.72, 0.70)


def clean(path):
    im = Image.open(path).convert("RGBA")
    im.putalpha(im.getchannel("A").point(lambda v: 0 if v < ALPHA_FLOOR else v))
    box = im.getbbox()
    return im.crop(box) if box else im


def sprite(name, height=320, square=False):
    raw, tmp = f"{M}/{name}-raw.jpg", f"{OUT}/_{name}.png"
    key(raw, tmp, height=None)
    im = clean(tmp)
    if square:
        side = max(im.size)
        pad = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        pad.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
        im = pad
    im = im.resize((max(1, round(im.width * height / im.height)), height), Image.LANCZOS)
    r, g, b, a = im.split()
    im = Image.merge("RGBA", (r.point(lambda v: int(v * GAIN[0])),
                              g.point(lambda v: int(v * GAIN[1])),
                              b.point(lambda v: int(v * GAIN[2])), a))
    dst = f"{OUT}/{name}.webp"
    im.save(dst, "WEBP", quality=86, method=6)
    os.remove(tmp)
    print("  %-22s %dx%d  %d bytes" % (dst, im.width, im.height, os.path.getsize(dst)))


def plate():
    src = Image.open(f"{M}/hero-forest.jpg").convert("RGB")
    for w, tag in ((2560, ""), (1280, "-sm")):
        r = src.resize((w, round(src.height * w / src.width)), Image.LANCZOS)
        dst = f"{OUT}/hero-forest{tag}.webp"
        r.save(dst, "WEBP", quality=72, method=6)
        print("  %-22s %dx%d  %d bytes" % (dst, r.width, r.height, os.path.getsize(dst)))


# NOTE: the hero is now entirely pixel art from scripts/pixel_art.py.
# plate()/sprite() and the kie.ai masters are kept only so the earlier
# photoreal forest and 3D mascot can be rebuilt if we ever go back to them.
if __name__ == "__main__":
    print("nothing to build - the hero uses scripts/pixel_art.py")
