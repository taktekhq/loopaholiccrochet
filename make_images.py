#!/usr/bin/env python3
"""Re-grounds Rana's product photos onto the Loopaholic lilac tile and writes
responsive files. The product itself is never edited: only the flat cream
ground the photos were delivered on (#FAF3E9) is replaced.

    ~/venvs/pw/bin/python make_images.py        # needs numpy, scipy, pillow (AVIF)

For every photo in catalog.json (+ the two custom-order examples) it writes
assets/img/p/<id>/
  w400|w800|w1200 .avif/.webp   the re-grounded square photo
  w800.jpg, w1200.jpg           JPEG fallback / JSON-LD / OG source
  stitch.avif/.webp/.jpg        300 px crop of the piece at full resolution,
                                shown in the ring "loupe" (a crop, not a new shot)
  og.jpg                        1200x630 link preview
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = np.array([250, 243, 233])          # the cream ground baked into the source JPGs
NEW = np.array([242, 236, 247])          # kit surface-2 #F2ECF7, the house tile
PAPER = (250, 247, 252)                  # kit paper #FAF7FC
KIT = os.path.expanduser("~/taktekhq/brand/products/loopaholic")
OUT = os.path.join(ROOT, "assets", "img", "p")


def reground(src):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    d = np.abs(a - OLD).max(axis=2)
    near = d <= 10
    lab, n = ndimage.label(near)
    keep = np.zeros(n + 1, bool)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    keep[border] = True
    # enclosed holes (the inside of a teether ring, gaps between legs): the ground is
    # a synthetic flat fill, so a big component that is mostly the exact colour is ground.
    exact = (d == 0)
    sizes = ndimage.sum(np.ones_like(d), lab, range(n + 1))
    exacts = ndimage.sum(exact, lab, range(n + 1))
    for i in range(1, n + 1):
        if sizes[i] >= 1500 and exacts[i] / sizes[i] >= 0.5:
            keep[i] = True
    keep[0] = False
    bg = keep[lab]
    out = a.copy()
    out[bg] = NEW
    # antialiased fringe: 2 px band next to the ground, shifted only as far as it is
    # still ground-coloured (w=1 at cream, w=0 once it looks like yarn).
    band = ndimage.binary_dilation(bg, iterations=2) & ~bg
    w = np.clip(1 - d / 48.0, 0, 1)[..., None]
    shift = (w * (NEW - OLD)).astype(np.int16)
    out[band] = np.clip(a[band] + shift[band], 0, 255)
    return Image.fromarray(out.astype(np.uint8)), bg


# Where the most textured window isn't crochet (the gift box's ribbons), pin the crop
# to the crocheted part by hand: (x, y) of the top-left corner in the 1200 px photo.
STITCH_AT = {"p043": (440, 760), "p012": (540, 280), "p005": (480, 175)}


def stitch_crop(img, bg, size=300, pid=None):
    """The most textured size x size window that lies wholly on the piece."""
    if pid in STITCH_AT:
        x, y = STITCH_AT[pid]
        return img.crop((x, y, x + size, y + size))
    g = np.asarray(img.convert("L")).astype(np.float32)
    lap = np.abs(ndimage.laplace(ndimage.gaussian_filter(g, 1.0)))
    off = ndimage.binary_dilation(bg, iterations=6).astype(np.float32)
    for s in (size, 260, 220, 180):
        ii_e = np.pad(lap.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
        ii_b = np.pad(off.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
        H, W = g.shape

        def box(ii):
            return ii[s:, s:] - ii[:-s, s:] - ii[s:, :-s] + ii[:-s, :-s]
        e, b = box(ii_e), box(ii_b)
        e[b > 0] = -1
        # don't hug the frame edge, and prefer the middle of the piece
        y, x = np.unravel_index(np.argmax(e), e.shape)
        if e[y, x] > 0:
            return img.crop((x, y, x + s, y + s)).resize((size, size), Image.LANCZOS)
    c = g.shape[0] // 2
    return img.crop((c - size // 2, c - size // 2, c + size // 2, c + size // 2))


def save_set(img, base, widths=(400, 800, 1200), jpeg=(800, 1200)):
    for wd in widths:
        im = img if img.width == wd else img.resize((wd, wd), Image.LANCZOS)
        im.save(f"{base}w{wd}.avif", quality=62, speed=4)
        if wd < 1200:  # AVIF covers ~95%; WebP is the fallback for older Safari at 400/800
            im.save(f"{base}w{wd}.webp", quality=80, method=6)
        if wd in jpeg:
            im.save(f"{base}w{wd}.jpg", quality=82, optimize=True, progressive=True)


def og(img, path):
    canvas = Image.new("RGB", (1200, 630), PAPER)
    tile = img.resize((630, 630), Image.LANCZOS)
    canvas.paste(tile, (570, 0))
    lock = Image.open(os.path.join(KIT, "logo/png/lockup-1024.png")).convert("RGBA")
    lw = 440
    lock = lock.resize((lw, round(lock.height * lw / lock.width)), Image.LANCZOS)
    canvas.paste(lock, (65, 315 - lock.height // 2), lock)
    canvas.save(path, quality=84, optimize=True)


def main():
    cat = json.load(open(os.path.join(ROOT, "catalog.json"), encoding="utf-8"))
    jobs = [(p["id"], p["image"]["main"]) for p in cat["products"]]
    jobs += [("custom-letter-d", "assets/img/custom/letter-d.jpg"),
             ("custom-daisy-keychain", "assets/img/custom/daisy-keychain.jpg")]
    only = set(sys.argv[1:])
    jobs = [j for j in jobs if not only or j[0] in only]
    with ProcessPoolExecutor() as ex:
        for line in ex.map(one, jobs):
            print(line)


def one(job):
    pid, src = job
    if True:
        d = os.path.join(OUT, pid)
        os.makedirs(d, exist_ok=True)
        img, bg = reground(os.path.join(ROOT, src))
        save_set(img, d + "/")
        st = stitch_crop(img, bg, pid=pid)
        st.save(f"{d}/stitch.avif", quality=62, speed=4)
        st.save(f"{d}/stitch.webp", quality=80, method=6)
        st.save(f"{d}/stitch.jpg", quality=82, optimize=True)
        if not pid.startswith("custom-"):
            og(img, f"{d}/og.jpg")
        return f"{pid} ground {bg.mean():.0%}"


if __name__ == "__main__":
    main()
