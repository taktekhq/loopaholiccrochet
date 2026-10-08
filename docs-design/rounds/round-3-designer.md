# Round 3: designer response to the round-2 critic (2026-10-08)

Critic: `round-2-critic.md` (7.7 BLOCK: AR agreement error on the shop). Screens:
`/home/taktekbot/design-work/r3/` (incl. `i-loupe-*` interaction shots), kept set in `../after/`.

## Measurements
- axe, 16 URLs × 390/1440 (EN, AR, kitten, tulip, 404): 0 violations, no overflow. Also 0 with the
  magnifier live and focused (EN + AR product).
- Lighthouse mobile `LH_CPU=1`: home 99, shop 99, duck 99, AR duck 99; a11y / BP / SEO 100;
  LCP 2.0–2.2 s, TBT 0, CLS ≤ 0.004, 191–292 KiB.
- Shop chips (scripted scroll 0 → 7000 → 0, EN + AR): **no window jumps**; every section, incl. Baby and
  Fun & Novelty, becomes current; nothing is current above the first section.
- Magnifier: full-res photo requested only on first interaction; CLS 0 during use; mouse follows,
  touch tap + drag, keyboard arrows / Shift+arrows / Escape, `role="application"` with a label in the
  page language.
- GA (real-browser UA, gtm stubbed): config carries `transport_type: 'beacon'`; gtag.js requested on
  first pointerdown, or after DOMContentLoaded + idle (1 s cap).

## Critic item → what changed
| Critic item | Done |
|---|---|
| AF «لم تجدوا ما تريدين؟» | «لم تجدوا ما تريدونه؟». Full AR proofread after the plural switch: also «قطعتك» → «قطعتكم» (shipping note). Every AR string re-read; first-person questions («هل يمكنني…», «كيف أدفع؟») are intentional |
| Chip code scrolls the window ~36 px | `row.scrollBy` with a physical delta (no `scrollIntoView`); last section marked at the page bottom; nothing marked above the first section |
| About: two solid "Browse the pieces" | inline one removed; the side panel carries it |
| p207 kitten hand sliver | presentation crop to the head and front paws (`make_images.py` `CROP`), no pixel of the piece altered; alt says the photo is cropped; still out of home/related; reshoot ask goes to Rana |
| Chip current = ink fill | accent-subtle + 2 px underline, like nav/menu current |
| Breadcrumb "Gift Sets/Seasonal/Accessories" → "Gifts & more" | breadcrumb shows the shop section it links to («هدايا وأكثر») |
| 404 ring/line only on the EN side | ring centred above both columns; AR line «انحلّت غرزة: …» |
| GA event lost on an early tap | `transport_type: 'beacon'`; gtag.js on DOMContentLoaded + idle (1 s) or first interaction |
| Custom orders: ~150 px empty ink band | sticky padding `+ 4.5rem` |
| `.foot-lang` underlined | no underline, underline on hover; label dropped, just «العربية» / "English" like the header (fixes the "Language:العربية" spacing too) |
| Loupe 520 px | not done as asked: the photos are 1200 px, so a 520 px static crop either upscales (no new detail) or covers a wider area (less close-up). Instead the product page loupe is now a live magnifier at 1 photo px per CSS px (below); the static 400 px crop stays as the no-JS view |
| Custom closing CTA can share a viewport with the head CTA | rendered as secondary at ≥ 52.5em, primary at 390 |
| Shop 390 lead pushes tiles down | one-line lead ("Every piece is made by hand when you order it." / «كل قطعة نحيكها باليد عند طلبها.»); first row of tiles in the first screen |
| Home fold accent count | accepted as brand (logo ring + loupe ring), no change |
| 9.5 idea: interactive loupe | done on the product page: hover/tap/drag/arrow keys, lazy full-res, transforms only, desktop hint "Move over the photo: the ring shows the stitches up close." |
