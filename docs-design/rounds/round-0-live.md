# Design review, round 0: live site as found

**Site:** https://loopaholiccrochet.com (GitHub Pages, repo HEAD `0912b67`)
**Date:** 2026-10-08
**Reviewer:** design-critic, scored against `brand/design/RUBRIC.md`
**Goal:** Instagram/WhatsApp visitors in Lebanon and the Gulf (390px first) see a made-to-order crochet piece and DM to order it. No public prices, on purpose.

## Site verdict: **BLOCK**, site score **4.6** (lowest page: product). Gate is 8.5 with no dimension under 8.

Four auto-fails hold the gate shut. Three of them are cheap fixes in `assets/css/style.css`:

1. **Colour, contrast.** `.btn-primary` is white on `#c1613f`, which measures **4.16:1** (needs 4.5:1 at 15.2px/600). axe flags it as serious on home, product and custom-orders at 390 and 1440. The AR home wasn't flagged, but it uses the same CSS and the same ratio.
2. **Typography in Arabic, fallback font.** No Arabic face is declared. Headings use `ui-serif, Georgia, "Times New Roman", serif` and body uses `-apple-system … Arial`, so Arabic text renders in whatever the OS has (Noto Sans Arabic on this Linux box, Geeza or SF Arabic on Apple, Segoe or Tahoma on Windows). Arabic also gets Latin settings: line-height 1.55, the same size, and headings at 1.2.
3. **Brand fit, off-palette primary and logo.** The kit (`brand/products/loopaholic/README.md`) says ink `#2B2233`, accent `#7B4FA6` on paper `#FAF7FC`, Nunito 800 wordmark with a ring mark. The live site uses cream `#fbf4ec`, Georgia/Times serif and a terracotta `#c1613f` accent, with an orange dot and a serif wordmark. That is the P15 default (cream + serif + terracotta), and it is also the look the kit reserves for the sibling brand **Ghazl** ("Loopaholic stays in cool purple/lavender … so the two read as separate brands").
4. **Consistency on the product page.** One action ("DM us on Instagram", same `href`) appears three ways: an accent text link "Ask for the price on Instagram", a solid `.btn-primary` "Message on Instagram", and a `.btn-outline` "Message on Instagram".

What's good: the copy is honest and careful. No prices, no fake reviews. The FAQ says plainly that the pieces aren't safety-tested for babies. Lead times are on every product, Lebanon payment (Whish / cash) is stated, and the "baby-safe" claim was correctly removed. The photography is real, cut out on one ground at 1:1. There's no horizontal overflow at 320, 390 or 1440. `lang`/`dir`, hreflang, canonical, Product and Organization JSON-LD are all in place. Lighthouse SEO and Best Practices are 100.

---

## Per-template scores

Each dimension takes the lower of EN and AR. Overall = Σ(score×weight)/Σweight, rounded down. Imagery weighs 1.2 on shop and product. Content pages have no conversion goal, so Conversion is left out there.

| Dimension (wt) | Home | Shop listing | Product | Custom orders | Content (shipping/about/faq) |
|---|---|---|---|---|---|
| Hierarchy (1.5) | 6 | 6 | 6 | 7 | 7 |
| Typography (1.2) | **2 AF** | **2 AF** | **2 AF** | **2 AF** | **2 AF** |
| Spacing (1.2) | 5 | 5 | 6 | 6 | 6 |
| Colour (1.0) | **2 AF** | 5 | **2 AF** | **2 AF** | 6 |
| Imagery (0.8 / 1.2) | 6 | 6 | 6 | 6 | 6 |
| Consistency (1.0) | 6 | 6 | **2 AF** | 6 | 6 |
| Interaction (1.2) | 5 | 5 | 5 | 5 | 5 |
| Accessibility (1.3) | 5 | 7 | 5 | 5 | 6 |
| Performance (1.0) | 7 | 6 | 8 | 7* | 7* |
| Brand fit (1.0) | **2 AF** | **2 AF** | **2 AF** | **2 AF** | **2 AF** |
| Copy (1.0) | 6 | 6 | 5 | 8 | 8 |
| Conversion (1.2) | 6 | 6 | 6 | 7 | n/a |
| **Overall** | **4.8** | **5.3** | **4.6** | **5.2** | **5.5** |
| Verdict | BLOCK | BLOCK | BLOCK | BLOCK | BLOCK |

AF = auto-fail, so the dimension is capped at 2. \* = not measured with Lighthouse. These pages use the same stack and assets as home, so they're estimated from it.

### Measurements
| URL | LH Perf | LH A11y | LCP | TBT | CLS | Weight | axe (390 + 1440) |
|---|---|---|---|---|---|---|---|
| `/` | 91 | 94 | 1.9 s | 310 ms | 0 | 414 KiB | serious: color-contrast `.btn-primary`; moderate: landmark-unique `.main` |
| `/shop/` | **84** | 100 | **3.4 s** | 310 ms | 0 | 650 KiB | moderate: landmark-unique |
| `/shop/duck-teether-ring/` | 97 | **89** | 1.4 s | 200 ms | 0 | 320 KiB | serious: color-contrast `.btn-primary`, link-in-text-block `.breadcrumb > a` ×2 |
| `/ar/` | 92 | 100 | 1.8 s | 320 ms | 0 | 415 KiB | moderate: landmark-unique |
| `/custom-orders/` | n/a | n/a | n/a | n/a | n/a | n/a | serious: color-contrast `.btn` |

Overflow: none at 320, 390 or 1440 (`scrollWidth == innerWidth`) on EN and AR home and product.
Computed text sizes on one page: 13.6, 14.4, 15.2, 16, 16.8, 17.6, 20.8, 24, 25.6, 33.6px, all from ad-hoc rem values with no scale. Pills and breadcrumb are 13.6px.
Focus: browser default (`outline: auto 1px`). No `:focus-visible` rule in the CSS. No skip link, and `main` has no `id`.
Targets: `.lang-switch a` is 57×25 (needs 44 high). `nav.main a` is 24 high.
Images: product `main.jpg` is a 1200px, 100 KB JPEG shown at about 350px at 390. No `srcset`, no WebP/AVIF, no `fetchpriority`. On home and shop the LCP image is `loading="lazy"` (LH `lcp-lazy-loaded`).
Caching: GitHub Pages `max-age=600`, `style.css` has no version hash.
404: GitHub's default 404 (unbranded, English only).
OG: one shared `og.jpg` for every page and both languages.

---

## Template notes

### Home (`/`, `/ar/`): 4.8 BLOCK
| Dimension | EN | AR | Score | Key evidence | Heuristic |
|---|---|---|---|---|---|
| Hierarchy | 6 | 6 | 6 | The h1 is just "Loopaholic", repeating the header logo, so the biggest type carries no offer. One solid CTA (good), but the showcase tiles have no labels and the badge strip is small and grey | P1, P2 |
| Typography | 5 | 2 AF | 2 | AR: no Arabic face, line-height 1.55, Latin size. EN: system sans + Georgia/Times serif, 10 sizes off any scale, no `text-wrap: balance`, "worldwide." widow in the 390 lead | P3, P11 |
| Spacing | 5 | 5 | 5 | `section { padding: 36px 0 }` is under 48 on mobile and under 64 on desktop. At 1440 `.badge-row` sits left of centre (its `margin: 28px 0` overrides `.wrap`'s `margin: 0 auto`). At 390 the nav wraps with "FAQ" alone on a second line. Raw px throughout | P4 |
| Colour | 2 AF | 2 AF | 2 | `.btn-primary` 4.16:1 | P5, P10 |
| Imagery | 6 | 6 | 6 | Real pieces, one cut-out ground, 1:1 + `object-fit` (good). Cut-out halos on the kitten and the elephant. No `srcset` or WebP. Emoji 🧶🧵📦 used as UI icons | P6 |
| Consistency | 6 | 6 | 6 | `footer.site .brand` loses the header's serif and dot styling (it's a `div`, so it gets no `header.site` rules). `.btn-ig` hard-codes `#fff`, which breaks in dark mode. Inline `style=` | P7 |
| Interaction | 5 | 5 | 5 | Default focus ring. `:hover` isn't inside `@media (hover:hover)`. No `:active`. GitHub default 404 | P8 |
| Accessibility | 5 | 6 | 5 | One serious axe issue. No skip link. Two unlabelled `nav`s (landmark-unique). Language switch 25px high | P10 |
| Performance | 7 | 7 | 7 | LH 91/92, LCP 1.9 s, CLS 0 (good). The LCP image is lazy-loaded, gtag adds about 310 ms TBT, CSS has no hash | P12 |
| Brand fit | 2 AF | 2 AF | 2 | Off-kit palette, type and logo. Cream + serif + terracotta is the P15 default and it's Ghazl's look | P15 |
| Copy | 6 | 7 | 6 | The lead is clear and true, but the h1 doesn't say what or who. The AR copy reads naturally | P14 |
| Conversion | 6 | 6 | 6 | The primary goes to the shop, and nothing on home explains how ordering by DM works, the lead time or payment | P1 |

### Shop listing (`/shop/`, `/ar/shop/`): 5.3 BLOCK
- **Hierarchy 6:** every card repeats "Ask for the price on Instagram" in accent bold (`.card .price`). At 1440 that's 8 accent strings per view, so the accent stops meaning "act here" and fights the product names.
- **Spacing 5:** about 100px of empty space between `.chips` and the first category heading at 1440. Card text padding is `12px 14px 16px`.
- **Colour 5:** no contrast failure, but the accent is overused (more than 3 per view).
- **Accessibility 7:** axe clean apart from landmark-unique, LH 100. Chips are 35px high, and the default focus, missing skip link and small language switch still apply.
- **Performance 6:** LH **84**, LCP **3.4 s**, because the first card image is `loading="lazy"` and 650 KiB of thumbnails are JPEG with no `srcset`.
- **Copy and conversion 6:** "Ask for the price on Instagram" ×50 is honest but noisy. One line under the h1 already says it.

### Product (`/shop/duck-teether-ring/`, AR): 4.6 BLOCK, the lowest page
- **Consistency 2 (auto-fail):** three treatments for one action: `.price-block a`, `.order-actions .btn-primary` and the following `.btn.btn-outline`. All link to the Instagram **profile**, not a DM (`ig.me/m/loopaholic.crochet`), so "Message on Instagram" doesn't open a message.
- **Hierarchy 6:** the accent price link and two buttons compete. At 390 the primary CTA is at about 1,040px, in the second screen (allowed), with no sticky bar.
- **Colour 2 (auto-fail):** `.btn-primary` 4.16:1. `.breadcrumb a` is distinguished by colour only (axe link-in-text-block).
- **Imagery 6:** one photo per product. No in-scale (in-hand) or macro stitch shot, no gallery, no `srcset`.
- **Copy 5:**
  - AR `.pill` values are English ("cm ring 11~", "yellow, orange, natural wood"), and the bidi ordering is broken.
  - "International checkout is almost ready" is internal status, not customer copy.
  - **[CLIENT TO CONFIRM]** The product is named "Duck *Wooden* Teether Ring" with colours "natural wood", but the photo shows a pale lavender/white ring. If the ring isn't wood, this is an untrue fact (a P13 auto-fail). Confirm with Rana before the next round.
- **Conversion 6:** good: lead time, size and payment sit next to the CTA. Missing: a single "How ordering works", a DM link, a sticky mobile CTA.
- **Performance 8:** LH 97, LCP 1.4 s, CLS 0. Not 9: no `fetchpriority="high"`, a 1200px JPEG for a 350px slot, unversioned CSS.
- **Plumbing:** the Product JSON-LD `Offer` has no `price`/`priceCurrency`, which Rich Results flags as invalid. Drop `offers` while there are no prices.

### Custom orders: 5.2 BLOCK
Copy 8 and conversion 7: "How it works" in 3 real steps with the deposit and progress photos is the best content on the site. Same `.btn` contrast auto-fail. The "D" letter photo is on a different ground from the keychain photo (mixed backgrounds). The CTA only appears at the end.

### Content pages (shipping, about, FAQ): 5.5 BLOCK
Honest, plain and useful. The FAQ answers the safety, returns and price objections, and the AR FAQ reads natively. They fail only on the shared auto-fails (AR font, brand). Prose `.prose` max-width 680px works out to about 75ch EN, which is acceptable. AR line-height 1.55 is too tight for Arabic paragraphs. The footer renders the handle as "loopaholic.crochet@" in AR because it isn't wrapped in `<bdi>` / `dir="ltr"`.

---

## Top 3 fixes for the whole site (priority order)

Auto-fails come first. All three are in the shared CSS or template, so each one lifts every page.

1. **[Sev 4 · Brand fit + Colour · M]** `:root`: re-token to the brand kit. This clears two auto-fails at once.
   `--accent: #c1613f → #7B4FA6` (white text 5.98:1 ✓)
   `--accent-dark: #9c4a2e → #5E3A82`
   `--bg: #fbf4ec → #FAF7FC`
   `--bg-alt: #f3e6d3 → #F2ECF7`
   `--card: #fff` (kept)
   `--ink: #3a2e27 → #2B2233`
   `--ink-soft: #6b5b4e → #6D6177` (5.5:1 on paper ✓)
   `--border: #e8d9c5 → #E4DBEB`
   Also add `--focus: #B388DD` and the kit's dark set.
   `h1, h2, h3, header.site .brand`: `font-family: ui-serif, Georgia… → "Nunito"` (self-hosted WOFF2, weights 400/800, Latin subset).
   `header.site .brand .dot` → the kit's `logo/svg/lockup.svg`, and the same in `footer.site .brand`.
   Effect: Brand 2 → 7, Colour 2 → 7. Fixing the primary contrast also lifts a11y on home, product and custom orders 5 → 6.
   If Rana actually wants the warm palette, update the kit first and pick a terracotta that passes, at least `#A9502F`. Don't ship the generic default.
2. **[Sev 4 · Typography (AR) · S]** `[lang="ar"] body, [lang="ar"] h1, [lang="ar"] h2, [lang="ar"] h3`: `font-family: system fallback → "Readex Pro"` (self-hosted, Arabic subset, 400/700). It's rounded and geometric, so it pairs optically with Nunito. Load it on `/ar/` only.
   `[lang="ar"] body`: `font-size: 16px → 1.12em`, `line-height: 1.55 → 1.8`.
   `[lang="ar"] h1, h2, h3`: `line-height: 1.2 → 1.35`.
   In `catalog.json`, translate the AR `size`/`colors` values so `.pill` stops showing English.
   Effect: Typography 2 → 6 site-wide. It reaches 7–8 once the EN sizes move onto a 6-step scale.
3. **[Sev 4 · Consistency + Conversion · S]** On the product template, the `.price-block a` is an accent link → plain text "Price on request, we reply on Instagram" (`color: var(--ink-soft)`, no link). Remove the second `.btn.btn-outline`, leaving one `.order-actions .btn-primary`. Change the `href`: `https://instagram.com/loopaholic.crochet → https://ig.me/m/loopaholic.crochet` (opens a DM). Merge "Order in Lebanon" and "Order internationally" into one 3-step "How ordering works".
   Effect: product Consistency 2 → 7, Hierarchy 6 → 8, Conversion 6 → 7.

Next after these: `a:focus-visible, .btn:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px }`, plus a skip link and `main#main` (Interaction and A11y 5 → 7).

## Other issues (severity-sorted)
| Sev | Selector | Current → proposed | Dimension |
|---|---|---|---|
| 3 | `.breadcrumb a` | `text-decoration: none → underline` (axe link-in-text-block) | A11y |
| 3 | `.lang-switch a` | `padding: 4px 10px → 12px 16px; min-height: 44px` | A11y |
| 3 | `.showcase img:first-child`, first `.card img` | `loading="lazy" → eager + fetchpriority="high"` (shop LCP 3.4 s) | Performance |
| 3 | `section` | `padding: 36px 0 → clamp(48px, 8vw, 96px) 0` | Spacing |
| 2 | `.badge-row` | `margin: 28px 0 → 28px auto` (re-centres at 1440). Replace emoji `.ic` with one SVG icon set | Spacing, Imagery |
| 2 | `.card .price` | `color: var(--accent-dark); font-weight: 700 → var(--ink-soft); 400`, or drop it from cards | Hierarchy, Colour |
| 2 | `<img>` (build.py) | single JPEG → `<picture>` WebP + `srcset` 400/800/1200 + `sizes` | Performance, Imagery |
| 2 | `link[rel=stylesheet]` | `/assets/css/style.css → style.css?v=<hash>` | Performance |
| 2 | footer handle (AR) | wrap `@loopaholic.crochet` in `<bdi dir="ltr">` | Typography, A11y |
| 2 | `nav.main` (390) | 6 links wrap to 2 lines → move FAQ, About and Shipping into the footer only, or use a menu | Spacing, Hierarchy |
| 1 | 404 | GitHub default → a branded bilingual `404.html` | Interaction, Brand |

## Missed opportunities (non-blocking)
- Per-product OG images (the product photo on brand paper), EN and AR. These are the WhatsApp/Instagram preview, and they're the real storefront.
- An in-hand (in-scale) shot and a macro stitch shot per product. Baymard: scale is the top question for plush and toys.
- A designed dark mode from the kit's dark tokens. The current dark set leaves `.btn-ig` white.
- `REFERENCES.md`, which the critic brief refers to, doesn't exist in `brand/design/`. So "would it stand next to the references" was judged against the RUBRIC calibration profiles only.

## What would make it a 9.5
Make the stitch the signature. Every product gets the same lavender-paper cut-out plus a tight macro of its own stitches, framed in the kit's open-ring mark. Carry that one crop system through grid, product, OG previews and Instagram, so you'd recognise a Loopaholic page with the logo hidden.

## Evidence
- Screenshots: `/home/taktekbot/design-work/before/*` (home, shop, shop-duck-teether-ring, custom-orders, shipping, about, faq; ar, ar-shop, ar-shop-duck-teether-ring, ar-custom-orders, ar-faq; 390 + 1440, full + fold)
- axe: `/tmp/lp-review/axe.txt`
- Lighthouse: `/tmp/lp-review/lh-home.json`, `lh-homeshop-.json`, `lh-homeshop-duck-teether-ring-.json`, `lh-homear-.json` (+ `.txt` summaries)
- Computed-style probe: `/tmp/lp-review/probe.py`
