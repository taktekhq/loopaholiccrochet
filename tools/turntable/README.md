# Turntable strips for the Stitch Book

Renders `assets/game/turn/<id>.webp` (18 frames, ±50°, 360 px) from the TripoSR models in
`taktekhq/loopaholic/docs/triage/models/` with three.js in headless Chromium. No 3D runtime ships
to visitors: the page scrubs the strip.

```
mkdir -p /tmp/three && cd /tmp/three && npm i three@0.169.0
mkdir www && cp render.html www/ && ln -s ../node_modules/three www/three \
  && ln -s ~/taktekhq/loopaholic/docs/triage/models www/models
(cd www && python3 -m http.server 18931 &)
~/venvs/pw/bin/python turn.py p003,p005 /tmp/turn 18      # PNG strips
# then WebP q72 into assets/game/turn/ and add the id to TURN_IDS in build.py
```
Only add a model after looking at all 18 frames next to the photo (docs-design/GAME.md lists the kept ones).
