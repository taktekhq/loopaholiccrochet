# Round 4: CHECKLIST closure after the round-3 critic (2026-10-08)

Critic: `round-3-critic.md` (RUBRIC gate met on every page; 13 CHECKLIST boxes open). Screens:
`/home/taktekbot/design-work/r4/`, kept set in `../after/`.

## Measurements
- axe, 15 URLs × 390/1440 (EN, AR, heart bouquet, 404): 0 violations, no overflow; 0 with the
  magnifier live (EN, AR).
- Lighthouse mobile `LH_CPU=1`: home 99, shop 99, duck 99, AR duck 98; a11y / BP / SEO 100;
  LCP 2.0–2.2 s (local, no gzip), TBT 0, CLS ≤ 0.005. `unminified-javascript` no longer reported.
- Build-wide greps: 0 straight `'` in visible text, meta or JSON-LD; every meta description ≤ 155.
- Touch (390, `hasTouch`): hint visible; CTA bottom EN 769 / AR 830 of 844; sticky bar hidden while the
  CTA shows. Keyboard: focus keeps the static close-up, first arrow goes live at the crop's centre.
  Mouse at the tile corner: the ring stays fully inside the photo. Chips: instant jump to the top
  clears the current chip and resets the row.

## Item → fix
| Item | Fix |
|---|---|
| A1 curly quotes | catalog: ‘cupcake’, ‘plant’, «نبتة», "a Valentine’s gift" (AR «هدية لعيد الحب»); build check finds no straight quote in text, meta or JSON-LD |
| A2 raw colour | `--color-band-line` token for the footer hairline |
| A3 AR body < 18 px at 360 | `--script-scale: 1.125` |
| A4 srcset widths | WebP now 400/800/1200 like AVIF (images regenerated) |
| A5 /shipping/ meta 171 chars | dedicated `meta_shipping_desc` EN (112) / AR |
| A6 favicon set | `/favicon.ico` (16+32), `icon.svg` with a dark-scheme variant, `icon-maskable-512.png` (ring inside the 40 % safe circle), manifest splits `any` / `maskable` |
| A7 OG per language | `og-ar.jpg` (kit card, «كروشيه يدوي» in Baloo, rendered in Chromium) on AR non-product pages |
| A8 Latin names in AR text | build wraps Whish / Loopaholic / the handle in `<bdi dir="ltr">` in AR text nodes |
| B1 Arabic subset on EN pages | kept; written exception in `PLAN.md` |
| B2 / B3 | client asks (overseer logs) |
| Accent count | `.hero .text-link` in ink (underline kept, accent on hover) |
| 1 magnifier focus = blank circle | focus keeps the static crop; first arrow / ring tap goes live at the crop's own centre (`stitch-centres.json` from `make_images.py`) |
| 2 ring at the edge | centre clamped one radius inside the photo |
| 3 stale chip after a jump | scroll handler clears it and resets the row above the first section |
| 4 no touch cue | "Tap the photo to look closer." / «اضغطوا على الصورة للتكبير.» under the photo on touch screens only |
| 5 site.js unminified | build writes hashed `site.min.js` (comments/indent stripped, line breaks kept) |
| 6 slash phrase | fixed with A1 |
| 7 closing CTA restyled primary | rendered as a real `.btn-secondary` |
