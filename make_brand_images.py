#!/usr/bin/env python3
"""Copies the Loopaholic brand-kit icons, logo and link preview into assets/img.

Source of truth is the kit (brand/products/loopaholic in the brand repo); this
site only mirrors it. Re-run after the kit changes.
"""
import os
import shutil

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
KIT = os.environ.get("LOOPAHOLIC_KIT", os.path.expanduser("~/taktekhq/brand/products/loopaholic"))


def og_ar():
    """og-ar.jpg: the kit's link-preview card with the Arabic line, set in the site's own
    Baloo Bhaijaan 2 and rendered by headless Chromium (Arabic shaping needs a browser)."""
    from playwright.sync_api import sync_playwright
    fonts = os.path.join(ROOT, "assets", "fonts")
    html = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:B;src:url("file://{fonts}/baloo-bhaijaan2-arabic.woff2");font-weight:400 800}}
@font-face{{font-family:N;src:url("file://{fonts}/nunito-latin.woff2");font-weight:200 1000}}
html,body{{margin:0}}
body{{width:1200px;height:630px;background:radial-gradient(60% 45% at 50% 0%,#F2ECF7 0%,#FAF7FC 70%);
display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:B,N,sans-serif;color:#2B2233}}
img{{width:600px;height:auto;direction:ltr}}
p{{margin:28px 0 0;font-size:40px;font-weight:500;color:#6D6177}}
.h{{position:absolute;top:44px;left:56px;font-family:N;font-weight:700;font-size:20px;color:#7B4FA6;
background:#F2ECF7;border-radius:999px;padding:10px 20px;direction:ltr}}
</style></head><body><div class="h">@loopaholic.crochet</div>
<img src="file://{os.path.join(KIT, 'logo/svg/lockup-on-light.svg')}" alt=""><p>كروشيه يدوي</p></body></html>"""
    tmp = os.path.join(ROOT, ".og-ar.html")
    open(tmp, "w", encoding="utf-8").write(html)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            pg.goto("file://" + tmp)
            pg.wait_for_timeout(500)
            pg.screenshot(path=os.path.join(OUT, "og-ar.png"))
            b.close()
    finally:
        os.remove(tmp)
    png = os.path.join(OUT, "og-ar.png")
    Image.open(png).convert("RGB").save(os.path.join(OUT, "og-ar.jpg"), quality=86, optimize=True)
    os.remove(png)


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

    # icon.svg: the kit favicon, with a dark-scheme variant (kit dark tokens)
    svg = open(os.path.join(KIT, "icons/favicon.svg")).read()
    svg = svg.replace('<rect', '<style>@media (prefers-color-scheme: dark){rect{fill:#17131B}circle{stroke:#B48AE0}}</style><rect', 1)
    open(os.path.join(OUT, "icon.svg"), "w").write(svg)

    # favicon.ico (16 + 32) at the site root: browsers and crawlers ask for it blindly
    ico = Image.open(os.path.join(KIT, "icons/icon-512.png")).convert("RGBA")
    ico.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32)])

    # maskable icon: full-bleed paper, the ring's outer edge at 36 % of the size, so it sits
    # inside the 40 % safe circle that launchers keep (kit ring: stroke 16 on radius 36)
    S = 512
    m = Image.new("RGB", (S * 4, S * 4), (250, 247, 252))
    d = ImageDraw.Draw(m)
    outer = 0.36 * S * 4
    stroke = outer * 16 / 44
    c = S * 2
    d.ellipse([c - outer, c - outer, c + outer, c + outer], fill=(123, 79, 166))
    inner = outer - stroke
    d.ellipse([c - inner, c - inner, c + inner, c + inner], fill=(250, 247, 252))
    m.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, "icon-maskable-512.png"), optimize=True)
    og_ar()
    print("brand images copied from", KIT)


if __name__ == "__main__":
    main()
