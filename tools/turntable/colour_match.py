"""Pull a turntable strip's colours back toward the real photo's (the TripoSR vertex colours and
render shading come out greyer). Gentle per-channel mean/std transfer in RGB, foreground only,
blended halfway so the sketch never pretends to be a photo.
    ~/venvs/pw/bin/python tools/turntable/colour_match.py /tmp/turn/p003.png p003 out.webp"""
import sys
import numpy as np
from PIL import Image

GROUND = np.array([242, 236, 247], float)
strip, pid, out = sys.argv[1:4]
pa = np.asarray(Image.open(f"assets/img/p/{pid}/w800.jpg").convert("RGB"), float)
fg = pa[np.sqrt(((pa - GROUND) ** 2).sum(-1)) > 14]
im = np.asarray(Image.open(strip).convert("RGBA"), float)
rgb, alpha = im[..., :3], im[..., 3]
sm = rgb[alpha > 200]
k = np.clip(fg.std(0) / (sm.std(0) + 1e-6), 0.85, 1.35)
new = (rgb - sm.mean(0)) * k + fg.mean(0)
new = 0.5 * rgb + 0.5 * new
res = np.dstack([np.clip(new, 0, 255), alpha]).astype(np.uint8)
Image.fromarray(res, "RGBA").save(out, quality=72, method=6)
