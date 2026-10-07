#!/usr/bin/env python3
"""Generates og.jpg and favicon/touch icons from brand colors (no external assets)."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
BG = (251, 244, 236)
INK = (58, 46, 39)
ACCENT = (193, 97, 63)
FONT = "/System/Library/Fonts/Supplemental/Georgia.ttf"

def wordmark(size, draw_dot=True):
    im = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(im)
    text = "Loopaholic"
    fsize = int(size[1] * 0.22)
    font = ImageFont.truetype(FONT, fsize)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    dot_r = int(fsize * 0.12)
    gap = int(fsize * 0.25)
    total_w = tw + (dot_r * 2 + gap if draw_dot else 0)
    x = (size[0] - total_w) // 2
    y = (size[1] - th) // 2 - bbox[1]
    if draw_dot:
        cy = size[1] // 2
        d.ellipse([x, cy - dot_r, x + dot_r * 2, cy + dot_r], fill=ACCENT)
        x += dot_r * 2 + gap
    d.text((x, y), text, font=font, fill=INK)
    return im

def icon(size):
    im = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(im)
    r = int(size * 0.3)
    cx = cy = size // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
    inner = int(r * 0.45)
    d.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], fill=BG)
    return im

def main():
    os.makedirs(OUT, exist_ok=True)
    wordmark((1200, 630)).save(os.path.join(OUT, "og.jpg"), quality=88)
    for size, name in [(512, "icon-512.png"), (180, "icon-180.png"), (32, "icon-32.png")]:
        icon(size).save(os.path.join(OUT, name))
    print("brand images written")

if __name__ == "__main__":
    main()
