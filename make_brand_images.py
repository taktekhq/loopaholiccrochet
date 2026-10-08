#!/usr/bin/env python3
"""Copies the Loopaholic brand-kit icons, logo and link preview into assets/img.

Source of truth is the kit (brand/products/loopaholic in the brand repo); this
site only mirrors it. Re-run after the kit changes.
"""
import os
import shutil

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
KIT = os.environ.get("LOOPAHOLIC_KIT", os.path.expanduser("~/taktekhq/brand/products/loopaholic"))


def main():
    os.makedirs(OUT, exist_ok=True)
    copies = {
        "icons/favicon.svg": "icon.svg",
        "icons/favicon-32.png": "icon-32.png",
        "icons/apple-touch-icon.png": "icon-180.png",
        "icons/icon-192.png": "icon-192.png",
        "icons/icon-512.png": "icon-512.png",
    }
    for src, dst in copies.items():
        shutil.copy(os.path.join(KIT, src), os.path.join(OUT, dst))
    Image.open(os.path.join(KIT, "social/og-1200x630.png")).convert("RGB").save(
        os.path.join(OUT, "og.jpg"), quality=86, optimize=True)
    print("brand images copied from", KIT)


if __name__ == "__main__":
    main()
