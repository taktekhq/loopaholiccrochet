# Round 1: designer self-check before the critic (2026-10-08)

Branch `redesign`. Plan: `../PLAN.md`. Screens: `../after/` (fold shots of every template, full shots of
home + product, 390 and 1440, EN + AR), `../before/` (the live site, same set).

## Measurements (local `python3 -m http.server`, no CDN, no gzip)
- axe (WCAG 2.2 AA + best practice), 15 URLs × 390/1440, EN + AR + 404: **0 violations**, no overflow.
  Overflow also clean at 320 / 768 / 1024 / 1920 on home, AR home, shop, AR product.
- Lighthouse mobile: **A11y 100, Best practices 100, SEO 100** on home, shop, product, AR home, AR product.
  Performance is not measurable on the XPS right now: load average 60–80 on 12 cores, Lighthouse
  `benchmarkIndex` 115–260 (a normal machine is ~1000+), so TBT is the host, not the page.
  Same-load A/B on the product page: live site perf 70–75 / TBT 1.3–3.5 s / 328 KiB / a11y 89;
  redesign perf 76–82 / TBT 0.7–0.9 s / 171 KiB / a11y 100, LCP 1.7–2.3 s, CLS 0.
  Page JS is 1.4 KB (`site.js`); gtag.js loads after `load` + idle and never appeared in the
  Lighthouse window. First view 170–280 KiB. Re-measure on a quiet machine or against the deploy.
- Keyboard: skip link is the first stop (EN + AR), menu opens/closes with Enter/Esc and returns
  focus to its button, the focus ring is visible, sticky order bar is out of the tab order until shown.
- GA: clicking "Order on Instagram" queues `['event','instagram_click',{product:'duck-teether-ring'}]`
  into `dataLayer` before gtag.js has loaded.
- Plumbing: 86 URLs identical to `main` (+ `404.html`), sitemap identical, robots/CNAME/IndexNow key
  identical, every page parses its JSON-LD (Product 74, BreadcrumbList 76, FAQPage 2, Organization 2).
  Titles/descriptions unchanged except the deliberate ones (teether titles/descriptions, shark
  description, FAQ description now that the day ranges are hidden).

## Self-score against RUBRIC (lower of EN/AR)
| Dimension | Home | Shop | Product | Custom | Content | 404 |
|---|---|---|---|---|---|---|
| Hierarchy 1.5 | 9 | 8 | 9 | 8 | 8 | 8 |
| Typography 1.2 | 8 | 8 | 8 | 8 | 9 | 8 |
| Spacing 1.2 | 8 | 8 | 8 | 8 | 8 | 8 |
| Colour 1.0 | 8 | 8 | 8 | 8 | 8 | 8 |
| Imagery 0.8/1.2 | 9 | 8 | 9 | 8 | 8 | n/a |
| Consistency 1.0 | 9 | 9 | 9 | 9 | 9 | 9 |
| Interaction 1.2 | 8 | 8 | 9 | 8 | 8 | 9 |
| Accessibility 1.3 | 9 | 9 | 9 | 9 | 9 | 9 |
| Performance 1.0 | 8* | 8* | 9* | 8* | 8* | 8* |
| Brand fit 1.0 | 9 | 8 | 9 | 8 | 8 | 8 |
| Copy 1.0 | 9 | 8 | 9 | 9 | 9 | 8 |
| Conversion 1.2 | 8 | 8 | 9 | 8 | n/a | n/a |
| **Overall (est.)** | **8.5** | **8.2** | **8.8** | **8.3** | **8.4** | **8.3** |

\* estimated from weight/JS/LCP/CLS; Lighthouse perf couldn't be measured cleanly (see above).

## Known gaps (honest)
- No in-scale (in-hand) or second-angle photos: Rana's catalogue has one photo per piece. The loupe is
  a crop of that photo, labelled as such. Asking for an in-hand shot per piece would lift Imagery to 9.
- No dark mode (light-only by decision, PLAN.md).
- Shop listing is long at 390 (37 pieces, 8 sections); chips are sticky to compensate.
- Gift/occasion entry (taste study) not added: mapping occasions onto categories would imply
  suitability claims (e.g. teethers "for a new baby") that the FAQ explicitly doesn't make.
- Product OG images carry no text, so one image serves EN and AR; home/listing use the kit OG.

## Checklist exceptions
- `tabular-nums` on prices: n/a, no prices.
- WhatsApp prefill: wired (`wa.me/<digits>?text=` in the page language, with the product URL) but off
  until `WHATSAPP_NUMBER` exists.
- Async/loading/error states: n/a, no forms.
- Accessory removed: a stitch-pattern section divider (Okhtein-style) was planned and dropped before it was built; the loupe is the only ornament.
