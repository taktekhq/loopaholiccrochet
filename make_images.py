#!/usr/bin/env python3
"""Re-grounds Rana's product photos onto the Loopaholic lilac tile and writes
responsive files. The product itself is never edited: only the flat cream
ground the photos were delivered on (#FAF3E9) is replaced.

    ~/venvs/pw/bin/python make_images.py        # needs numpy, scipy, pillow (AVIF)

For every photo in catalog.json (+ the two custom-order examples) it writes
assets/img/p/<id>/
  w400|w800|w1200 .avif/.webp   the re-grounded square photo
  w800.jpg, w1200.jpg           JPEG fallback / JSON-LD / OG source
  stitch.avif/.webp/.jpg        400 px crop of the piece at full resolution (1:1 pixels),
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


def box_mean(x, size):
    return ndimage.uniform_filter(x.astype(np.float32), size=size, mode="nearest")


def reground(src):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    d = np.abs(a - OLD).max(axis=2)
    near = d <= 10
    lab, n = ndimage.label(near)
    idx = np.arange(n + 1)
    keep = np.zeros(n + 1, bool)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    keep[border] = True
    # Enclosed pockets of the old ground (inside a teether ring, between legs and arms).
    # The ground is a smooth flat fill: its mean distance from the cream is ~2-4, while
    # cream or white yarn is textured and sits at 6+. Size floor keeps tiny specks alone.
    sizes = ndimage.sum(np.ones_like(d), lab, idx)
    mean_d = ndimage.mean(d, lab, idx)
    keep |= (sizes >= 200) & (mean_d <= 4.5)
    keep[0] = False
    bg = keep[lab]

    # Matte clean-up, outside the piece only:
    # 1) erode the matte by 1 px everywhere (the cut-out's own edge pixel);
    # 2) on light yarn, the cut left a grey contour up to 3 px wide. A pixel within 3 px
    #    of the ground that is much darker than the yarn 4-7 px further in is that contour,
    #    not yarn, so it becomes ground too.
    bg = ndimage.binary_dilation(bg, iterations=1)
    lum = a.mean(axis=2)
    dist = ndimage.distance_transform_edt(~bg)
    inner = (dist >= 4) & (dist <= 7)
    w_in = box_mean(inner, 9)
    ref = np.where(w_in > 0, box_mean(np.where(inner, lum, 0), 9) / np.maximum(w_in, 1e-6), 0)
    halo = (~bg) & (dist <= 3) & (ref > 130) & (lum < ref - 20) & (lum > 60)
    # only contour that actually touches the ground (grow from the edge inward)
    halo = ndimage.binary_propagation(halo & (dist <= 1.5), mask=halo)
    bg |= halo
    # specks: loose bits of the old cut (dust, stray matte) not attached to the piece
    plab, pn = ndimage.label(~bg)
    if pn > 1:
        psz = ndimage.sum(np.ones_like(d), plab, np.arange(pn + 1))
        bg |= (psz < 60)[plab] & (plab > 0)

    out = a.copy()
    out[bg] = NEW
    # antialiased fringe: 2 px band next to the ground, shifted only as far as it is
    # still ground-coloured (w=1 at cream, w=0 once it looks like yarn).
    band = ndimage.binary_dilation(bg, iterations=2) & ~bg
    w = np.clip(1 - d / 48.0, 0, 1)[..., None]
    shift = (w * (NEW - OLD)).astype(np.int16)
    out[band] = np.clip(a[band] + shift[band], 0, 255)
    return Image.fromarray(out.astype(np.uint8)), bg


# Where the most textured window isn't crochet (the gift box's ribbons) or hugs the
# silhouette, pin the crop by hand: (x, y) of the top-left corner in the 1200 px photo.
STITCH_AT = {"p043": (390, 710), "p012": (490, 230), "p005": (430, 200), "p445": (260, 330), "p251": (470, 450, 300)}
# Photos that are a scene (their own backdrop), not a cut-out: crop to the photo itself
# and let it fill the tile, instead of a photo-in-a-box on the lilac ground.
SCENE = {"p445"}
# Presentation crops (box in the 1200 px photo), applied after re-grounding. p207: the
# original frame has a sliver of a hand between the lower paws; cropping to the head and
# front paws removes it without touching the piece. A reshoot is requested from Rana.
CROP = {"p207": (235, 100, 985, 850)}


def scene_crop(src):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    off = np.abs(a - OLD).max(axis=2) > 10
    rows, cols = np.where(off.mean(axis=1) > 0.5)[0], np.where(off.mean(axis=0) > 0.5)[0]
    y0, y1, x0, x1 = rows.min(), rows.max(), cols.min(), cols.max()
    side = min(y1 - y0, x1 - x0) - 8          # inset 4 px so no cream edge survives
    cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
    im = Image.open(src).convert("RGB").crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2))
    im = im.resize((1200, 1200), Image.LANCZOS)
    return im, np.zeros((1200, 1200), bool)


def stitch_crop(img, bg, size=400, pid=None):
    """The most textured size x size window that lies wholly on the piece."""
    if pid in STITCH_AT:
        x, y, s = (STITCH_AT[pid] + (size,))[:3]
        return img.crop((x, y, x + s, y + s)).resize((size, size), Image.LANCZOS)
    g = np.asarray(img.convert("L")).astype(np.float32)
    lap = np.abs(ndimage.laplace(ndimage.gaussian_filter(g, 1.0)))
    off = ndimage.binary_dilation(bg, iterations=6).astype(np.float32)
    for s in (size, 340, 300, 260, 220):
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
        img, bg = scene_crop(os.path.join(ROOT, src)) if pid in SCENE else reground(os.path.join(ROOT, src))
        if pid in CROP:
            box = CROP[pid]
            img = img.crop(box).resize((1200, 1200), Image.LANCZOS)
            bg = np.asarray(Image.fromarray(bg[box[1]:box[3], box[0]:box[2]]).resize((1200, 1200), Image.NEAREST))
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
