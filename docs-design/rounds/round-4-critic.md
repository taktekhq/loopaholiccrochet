# Design review, round 4: final pre-ship verification (independent critic)

**Site:** http://127.0.0.1:8765, branch `redesign`, commit `1a655f2`
**Date:** 2026-10-08
**Reviewer:** design-critic, re-scored from scratch against `brand/design/RUBRIC.md` and the amended `CHECKLIST.md`. I checked every round-3 A-item and remaining issue myself. Rulings applied:
- **B1:** accepted as a written exception (an Arabic subset of 10 KB or less for the «العربية» label).
- **B2 and B3:** logged as client asks, not ship blockers.

## Verdict: **SHIP**

Every template is at or above 8.5. No dimension is below 8, there is no auto-fail, and no CHECKLIST box fails once the B rulings are applied. Two items still need the live site to confirm: LCP ≤ 2.0 s with gzip and the CDN, and a real HTTP 404 for unknown paths. See the post-deploy checklist.

Two small polish items remain. Neither blocks shipping:
1. On hover-capable screens under 52.5em, the PDP loupe ring sits 3–13 px inside the h1's line box (about 5 px from the glyphs, so nothing touches).
2. At 390, the custom-orders closing CTA is now an outline button, and the sticky bar hides while it is on screen. The mobile decision point therefore has no filled button.

---

## Per-template scores

Each dimension takes the lower of EN and AR. Overall = Σ(score×weight)/Σweight, rounded down. Imagery weighs 1.2 on shop and product. Conversion is n/a on content pages and the 404. Imagery is n/a on the 404.

| Dimension (wt) | Home | Shop | Product | Custom orders | FAQ / Shipping | About | 404 |
|---|---|---|---|---|---|---|---|
| Hierarchy (1.5) | 9 | 9 | 9 | 9 | 9 | 9 | 8 |
| Typography (1.2) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Spacing (1.2) | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Colour (1.0) | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Imagery (0.8 / 1.2) | 8 | 8 | 8 | 8 | 8 | 8 | n/a |
| Consistency (1.0) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Interaction (1.2) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Accessibility (1.3) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Performance (1.0) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Brand fit (1.0) | 9 | 8 | 9 | 8 | 8 | 8 | 9 |
| Copy (1.0) | 8 | 8 | 9 | 8 | 8 | 8 | 8 |
| Conversion (1.2) | 8 | 8 | 9 | 8 | n/a | n/a | n/a |
| **Overall** | **8.6** | **8.5** | **8.7** | **8.5** | **8.5** | **8.5** | **8.5** |
| Verdict | SHIP | SHIP | SHIP | SHIP | SHIP | SHIP | SHIP |

### Changes since round 3
- **Product Interaction 8 → 9:**
  - Keyboard focus keeps the stitch close-up.
  - The first arrow key goes live at the crop's own centre.
  - The ring stays clamped inside the photo.
  - There's a touch hint.
- **Product 8.6 → 8.7.**
- **Custom orders Conversion 9 → 8:** the mobile closing CTA is now secondary (see issue 2). The page is still 8.5.
- **Unchanged ceilings:**
  - Imagery stays at 8 because there are no in-scale shots (a logged client ask).
  - Colour stays at 8 because the site is light-only by decision.
  - Spacing stays at 8 because there are no optical-alignment extras.

---

## Round-3 items: verified

| Item | Status | Evidence |
|---|---|---|
| A1 curly quotes | **Fixed** | Build-wide parse finds 0 straight `'` in visible text, meta or JSON-LD. Heart bouquet now reads "a Valentine’s gift" |
| A2 raw colour | **Fixed** | `--color-band-line` token. No raw colour remains outside `:root` |
| A3 AR body ≥ 18 px at 360 | **Fixed** | Computed **18.0 px** at 360 (`--script-scale: 1.125`) |
| A4 srcset widths | **Fixed** | WebP 400/800/1200w, matching AVIF |
| A5 meta ≤ 155 | **Fixed** | All 87 pages are ≤ 155 |
| A6 favicon set | **Fixed** | `/favicon.ico` (16 + 32 PNG-in-ICO). `icon.svg` has a `prefers-color-scheme: dark` style. The manifest splits `any` and `maskable`. The maskable ring sits fully inside the 40 % safe circle (`maskable-safe.png`) |
| A7 OG per language | **Fixed** | `og-ar.jpg` (1200×630, 23 KB, «كروشيه يدوي» in Baloo) is used on AR home, shop and content pages. Product OGs have no text and serve both languages. The 404 uses EN `og.jpg`, which is fine for a bilingual, noindex page |
| A8 Latin names in AR | **Fixed** | 0 unwrapped "Whish" or "Loopaholic" in AR body text |
| B1 / B2 / B3 | **Per ruling** | Exception recorded in `PLAN.md`. B2 and B3 are logged client asks |
| Accent count | **Fixed** | `.hero .text-link` is in ink, so the home fold has 2 UI-accent elements plus the logo |
| 1 magnifier focus = blank circle | **Fixed** | Tab to the ring: static close-up, `is-live` false (`mag/*-kb-focus.png`). Arrows go live from the crop centre. Esc restores it. Tab moves on to the CTA. EN + AR, 390 + 1440 |
| 2 ring at the edge | **Fixed** | A mouse at the tile corner keeps the whole ring inside the tile (`mag/en-1440-mouse-corner.png`). At the corner it shows lilac ground, which is the photo's own background, so that's fine |
| 3 stale chip after a jump | **Fixed** | Bottom → `scrollTo(0,0)`: no chip current, row reset, in EN and AR |
| 4 touch cue | **Fixed** | "Tap the photo to look closer." / «اضغطوا على الصورة للتكبير.» shows only on touch (`hasTouch`) |
| 5 JS unminified | **Fixed** | `site.min.js?v=…` is 6.9 KB. Lighthouse no longer reports `unminified-javascript` |
| 6 slash phrase | **Fixed** | See A1 |
| 7 restyled primary | **Fixed, but on mobile too** | It's a real `.btn-secondary` now, at every width (issue 2) |

## Measurements

| Check | Result |
|---|---|
| axe (WCAG 2.2 AA + best practice), 19 URLs × 390/1440 (EN, AR, heart bouquet EN/AR, sushi, kitten, AR shipping, 404) | **0 violations** on 38 runs, no overflow |
| axe with the magnifier live (mouse 1440, touch 390, keyboard 390/1440; EN + AR) | 0 violations in every state |
| Lighthouse mobile `LH_CPU=1` (local, no gzip/CDN) | `/ar/shop/duck-teether-ring/` **98**, LCP 2.2 s, TBT 20 ms, CLS 0.005, 223 KiB · `/custom-orders/` **100**, LCP 1.8 s, CLS 0, 123 KiB · a11y / BP / SEO 100. Only local-server audits are below 0.9 |
| Magnifier cost | `w1200` isn't requested before interaction, and the magnifier adds 0 CLS |
| Touch | Tap goes live, the ring drags without scrolling the page, a vertical swipe on the photo scrolls the page (235 / 343 px) and is not trapped, a tap outside closes it |
| Console, failed requests, ≥ 400 responses (8 pages, scrolled) | none |
| Regression sweep | Fold shots of every template at 390 and 1440, EN + AR (`crops-sheet390.png`, `crops-sheet1440.png`). Nothing broke except issue 1 below |

### Is the mobile closing CTA on custom orders clear enough?
**Mostly, but it's weaker than it should be.**
- At 390 the closing "Start a custom order" is a full-width outline pill with the Instagram glyph and ink text, and it reads as a button (`closing-cta_custom-orders_390.png`).
- Because it's one of the observed inline CTAs, the sticky bar hides while it's on screen.
- So at the moment of decision, right after "How it works", the only order action is an outline button. The filled one is about 1,000 px back up.
- My round-2 fix asked for secondary only at ≥ 52.5em, where the two CTAs can share a viewport. At 390 they never do.

That costs Conversion one point (9 → 8). The page still ships, but issue 2 is a 3-line fix.

---

## Remaining issues (non-blocking, severity-sorted)

| # | Sev | Where | Current → proposed | Dimension |
|---|---|---|---|---|
| 1 | 2 | `.pdp { gap: var(--space-s) }` (changed this round from `--space-l`) on hover-capable screens < 52.5em, where `.loupe-hint` is hidden | The loupe hangs `--space-m` below the tile into a 16 px gap, so its circle sits **3–13 px inside the h1's line box** on 15/37 EN and 26/37 AR products. The tightest is the AR heart bouquet, with a ring halo about 5 px above «باقة» (`crops-ar-heart-zoom.png`). Glyphs don't touch, and real phones (touch) are clear because the hint pushes the h1 down. Narrow desktop windows and the standard 390 evidence shot show it → `@media (hover: hover) and (max-width: 52.49em) { .pdp { gap: var(--space-l); } }` | Spacing |
| 2 | 2 | `/custom-orders/` + `/ar/custom-orders/` `.c-how .cta-block a.btn` at < 52.5em | `.btn-secondary` everywhere, and the sticky bar hides on it → emit `btn-primary` below 52.5em and `btn-secondary` at ≥ 52.5em (two classes plus a media query, or two elements with `hidden` per breakpoint), or exclude the closing CTA from `[data-order-cta]` so the filled sticky bar stays up beside it | Conversion (custom 8 → 9) |
| 3 | 1 | `.loupe-hint .hint-touch` at 390 | The touch hint's box runs under the ring (the 40 % end padding keeps the text clear). Fine now. Check it with the longest AR hint if it's ever lengthened | Spacing |

---

## Post-deploy checklist (live site)
1. **404:** `curl -sI https://loopaholiccrochet.com/nope/` and `/ar/nope/` → `HTTP/2 404` with the bilingual Loopaholic page (not GitHub's).
2. **Performance:** Lighthouse mobile (default throttling, and `LH_CPU=1` if the host is busy) on `/`, `/shop/`, `/shop/duck-teether-ring/`, `/ar/shop/duck-teether-ring/` → perf ≥ 90, **LCP ≤ 2.0 s**, CLS ≤ 0.05. If the AR PDP stays above 2.0 s, preload its LCP AVIF.
3. **Cache-busting:** the live HTML references the new `site.min.css?v=`, `site.min.js?v=`, `icon.svg?v=` and font `?v=` hashes, and each URL returns the new file (Cloudflare caches CSS/JS for 4 h). Hard-refresh a PDP and check that the magnifier works, which proves the new JS is live.
4. **Favicon and manifest:** `/favicon.ico` 200, `/site.webmanifest` 200, the tab icon is visible in a dark browser theme, and "Add to Home Screen" on Android shows the ring uncropped.
5. **Link previews:** paste `/`, `/ar/`, `/shop/duck-teether-ring/`, `/ar/shop/duck-teether-ring/` into WhatsApp. EN shows "Handmade crochet", AR shows «كروشيه يدوي», products show the product photo. Use the Facebook Sharing Debugger to refresh the cached OG.
6. **Instagram DM:** "Order on Instagram" and «اطلبوا على إنستغرام» open the DM to @loopaholic.crochet in the app on a real iPhone and a real Android, from the inline CTA and from the sticky bar.
7. **GA4 DebugView:** `instagram_click {product}` fires on a tap within 1–2 s of landing and on a later tap. Custom-orders clicks carry `page`. Language-switch links behave normally.
8. **Magnifier on real devices:** iPhone Safari and Android Chrome. Check tap, drag, vertical page scroll over the photo, tap-outside close, and that the AVIF lens background renders in Safari (with JPEG fallback on older iOS).
9. **Structured data:** Rich Results Test passes Product + BreadcrumbList on a product (EN + AR), FAQPage on `/faq/` and `/ar/faq/`, Organization on home.
10. **Search Console:** resubmit `sitemap.xml` (86 URLs). After the next crawl, check hreflang reports no errors and none of the old URLs 404.
11. **Client asks:** confirm the overseer has logged B2 (in-hand photos) and B3 (native Arabic read). Re-score Imagery when the photos arrive; 9 needs them.

---

## Evidence
`/home/taktekbot/design-work/critic-r4/`
- Full and fold shots at 390/1440 for: home, shop, duck, heart bouquet, sushi, kitten, custom, shipping, about, FAQ, AR home/shop/duck/heart/custom/FAQ/about/shipping, 404. Also `crops-sheet390.png` and `crops-sheet1440.png`
- `axe.txt` (38 runs, 0 violations) · `lh_ar_shop_duck-teether-ring_.json`, `lh_custom-orders_.json`
- `mag/` + `mag.txt`: magnifier mouse/touch/keyboard EN and AR, axe per live state, CLS and lazy-load checks
- `closing-cta_custom-orders_390.png`, `overlap-ar-heart.png`, `crops-ar-heart-zoom.png`, `overlap-en-kitten-touch.png`, `maskable-safe.png`
- Scripts in `/tmp/critic/` (`mag4.py`, `chips5.py`, `console.py`, `r4misc.py`, `overlap.py`)
