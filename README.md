# Loopaholic Crochet

Static shop site for Loopaholic (Rana's handmade crochet business), generated
from `catalog.json`. No build step at runtime — `build.py` renders plain
HTML/CSS once; GitHub Pages serves the result as-is.

```
python3 build.py                          # regenerate every page from catalog.json (+ minified CSS)
~/venvs/pw/bin/python make_images.py [id] # re-ground photos onto the lilac tile, AVIF/WebP/JPEG + stitch close-up + OG
~/venvs/pw/bin/python make_brand_images.py # copy icons/og from the brand kit
```

Flags at the top of `build.py`:
- `WHATSAPP_NUMBER`: set it and the order buttons, `whatsapp_click` events and
  "WhatsApp or Instagram" copy come back on the next build.
- `SHOW_UNCONFIRMED_DETAILS = False`: sizes and making times (catalog.json) stay
  hidden on pages and JSON-LD, and the FAQ says "we confirm the making time when
  you message us", until Rana confirms them.
- The build fails if catalog or copy contains a material, safety or price claim
  (safe/آمن, certified, non-toxic, organic, hypoallergenic, wood/خشب, CE, 100%, $/USD prices).

Edit `assets/css/style.css`; pages load the generated, hash-versioned
`assets/css/site.min.css`. Design notes and review rounds live in `docs-design/`
(excluded from the published site by `_config.yml`).

- `catalog.json` — every product, EN + AR. No prices: the site shows "Ask for
  the price on Instagram" until Rana confirms real prices. Draft prices and
  pricing notes live in the private `monetization` repo
  (`private/loopaholic-draft-prices.json`, `private/loopaholic-pricing-notes.md`),
  not here — this repo is public.
- `assets/img/products/<id>/` — Rana's original product photos (no people/faces/home details).
- `assets/img/p/<id>/` — generated from those by `make_images.py` (what the pages use).
- `assets/img/custom/` — example custom-order pieces shown on `/custom-orders/`.
- Generated output: `/`, `/shop/`, `/shop/<slug>/`, `/custom-orders/`,
  `/shipping/`, `/about/`, `/faq/`, and the same under `/ar/`, plus
  `sitemap.xml`, `robots.txt`, `CNAME`.

## Editing

Edit `catalog.json` or the `T` dict in `build.py` (site copy, EN/AR), then
rerun `build.py` and commit the regenerated HTML alongside the source change.

## Payments

- Lebanon: WhatsApp/Instagram order → Whish transfer or cash on delivery.
- International: a Stripe Payment Link per product (`stripe_payment_link` in
  `catalog.json`), rendered only when that field is set. Empty until prices
  are confirmed — see workstream log.
