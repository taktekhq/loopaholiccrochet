"""Game assets for the Stitch Book (run after make_images.py):
- assets/game/sil/<id>.webp: the "not met yet" silhouette, cut from the photo's flat lilac
  ground (make_images.py re-grounds every photo onto #F2ECF7), filled in a deeper lilac.
- assets/game/turn/<id>.webp: 18-frame turntable strips (±50°) rendered from the TripoSR
  models in taktekhq/loopaholic by tools/turntable/ (see its README). Not rebuilt here.

    ~/venvs/pw/bin/python make_game_assets.py
"""
import json, os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
GROUND = np.array([242, 236, 247], float)
SHADOW = (217, 204, 230)      # lilac 300-ish: reads as a shape on the tile, never as a product photo
S = 400


def silhouette(pid):
    im = Image.open(os.path.join(ROOT, f"assets/img/p/{pid}/w800.jpg")).convert("RGB").resize((S, S), Image.LANCZOS)
    a = np.asarray(im, float)
    fg = np.sqrt(((a - GROUND) ** 2).sum(-1)) > 14
    fg = ndimage.binary_opening(fg, iterations=1)
    lab, n = ndimage.label(fg)
    if n:
        sizes = ndimage.sum(fg, lab, range(1, n + 1))
        fg = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 120])
    fg = ndimage.binary_closing(fg, iterations=4)
    fg = ndimage.binary_fill_holes(fg)
    mask = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGB", (S, S), tuple(int(c) for c in GROUND))
    out.paste(Image.new("RGB", (S, S), SHADOW), (0, 0), mask)
    d = os.path.join(ROOT, "assets/game/sil")
    os.makedirs(d, exist_ok=True)
    out.save(os.path.join(d, f"{pid}.webp"), quality=60, method=6)


if __name__ == "__main__":
    for p in json.load(open(os.path.join(ROOT, "catalog.json")))["products"]:
        silhouette(p["id"])
    print("silhouettes done")
