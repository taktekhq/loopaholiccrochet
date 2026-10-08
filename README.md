# Loopaholic Crochet

Static shop site for Loopaholic (Rana's handmade crochet business), generated
from `catalog.json`. No build step at runtime — `build.py` renders plain
HTML/CSS once; GitHub Pages serves the result as-is.

```
python3 build.py              # regenerate every page from catalog.json
python3 make_brand_images.py  # regenerate og.jpg / favicon / touch icon
```

- `catalog.json` — every product, EN + AR. No prices: the site shows "Ask for
  the price on WhatsApp" until Rana confirms real prices. Draft prices and
  pricing notes live in the private `monetization` repo
  (`private/loopaholic-draft-prices.json`, `private/loopaholic-pricing-notes.md`),
  not here — this repo is public.
- `assets/img/products/<id>/` — product photos (no people/faces/home details).
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
