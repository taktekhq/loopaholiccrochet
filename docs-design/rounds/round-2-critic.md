# Design review, round 2: the redesign after fixes (independent critic)

**Site:** http://127.0.0.1:8765, branch `redesign`, commit `d308b70`
**Date:** 2026-10-08
**Reviewer:** design-critic, scored from scratch against `brand/design/RUBRIC.md`. I checked every round-1 item myself and didn't rely on `round-2-designer.md`.
**Goal:** Instagram visitors (390 px first, EN + AR) see a handmade, made-to-order piece and DM on Instagram to order it. No prices, no invented facts.

## Site verdict: **BLOCK**, site score **7.7** (lowest page: shop)

**Why it blocks:** one copy auto-fail, a one-word fix. The AR shop's closing heading reads «لم تجدوا ما تريدين؟». The round-2 switch to plural address left a feminine-singular verb inside a plural sentence, so the heading has a grammatical agreement error. RUBRIC D11 auto-fails "typos in headings or CTAs". Source: `build.py:214` `cant_find_h`.

**Without the auto-fail:**
- The shop is **8.1 REVISE**, held below the gate by a new interaction bug: the "current chip" code scrolls the whole page by about 36 px every time the section changes.
- About is **8.3 REVISE**, because it now has two identical solid "Browse the pieces" buttons in one viewport.
- Home, product, custom orders, FAQ/shipping and the 404 now clear the gate.

This is a big round: 22 of the 27 round-1 items are fixed and verified, three are partly fixed, and two of the fixes introduced the new problems above.

---

## Per-template scores

Each dimension takes the lower of EN and AR. Overall = Σ(score×weight)/Σweight, rounded down. Imagery weighs 1.2 on shop and product. Conversion is n/a on content pages and the 404. Imagery is n/a on the 404 (no photos).

| Dimension (wt) | Home | Shop | Product | Custom orders | FAQ / Shipping | About | 404 |
|---|---|---|---|---|---|---|---|
| Hierarchy (1.5) | 9 | 8 | 9 | 8 | 9 | **7** | 8 |
| Typography (1.2) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Spacing (1.2) | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Colour (1.0) | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Imagery (0.8 / 1.2) | 8 | 8 | 8 † | 8 | 8 | 8 | n/a |
| Consistency (1.0) | 9 | 8 | 9 | 9 | 9 | 9 | 8 |
| Interaction (1.2) | 9 | **7** | 9 | 9 | 9 | 9 | 9 |
| Accessibility (1.3) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Performance (1.0) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Brand fit (1.0) | 9 | 8 | 9 | 8 | 8 | 8 | 9 |
| Copy (1.0) | 8 | **2 AF** (AR) | 9 | 8 | 8 | 8 | 8 |
| Conversion (1.2) | 8 | 8 | 9 | 9 | n/a | n/a | n/a |
| **Overall** | **8.6** | **7.7** | **8.7** | **8.5** | **8.5** | **8.3** | **8.5** |
| Verdict | SHIP | **BLOCK** | SHIP | SHIP | SHIP | REVISE | SHIP |

† The template scores 8. One instance, `/shop/bee-costume-kitten/`, scores Imagery 7 (see below). That page alone is 8.6 overall but REVISE, because a dimension is under 8.

**Where a 9 is given, the positive evidence:**
- **Typography 9:** 6 sizes on the fluid scale, −0.02em on display, `text-wrap: balance`, no hero widows. Arabic is Baloo at 1.12× with 1.8 / 1.35 leading and now weight 600, so the AR hero and nav visibly match the EN weight.
- **Accessibility 9:** 0 axe issues on 32 runs, Lighthouse a11y 100, skip link, Esc plus focus return on the menu, `scroll-padding-block-end` clears the sticky bar, reflow at 320 / 640, text-spacing survives.
- **Performance 9:** Lighthouse 99, CLS ≤ 0.006, JS 1.5 KB, hashed assets. LCP is 2.0–2.1 s on the local server without gzip, so it is borderline for the 9 anchor's ≤ 2.0 s and should be lower on the gzip'd deploy.
- **Interaction 9 on PDP and custom orders:** sticky bar both ways, designed 404, no self-starting motion. Prefilled messages are n/a, because `ig.me` can't carry text, and I didn't count that against the score.
- **Brand 9:** the loupe ring now also carries the 404 state, and home and PDP are recognisable without the logo.
- **Product copy 9:** price, reply, delivery, returns and "how ordering works" sit next to the CTA, and the alt text is now the real description.

**Where the cap is a rubric anchor:** Imagery stays at 8 sitewide, because the 9 anchor requires in-scale shots and there are none. I haven't marked anything down further for that. Colour stays at 8: there's no dark mode or second theme (a documented decision), and the home fold has 4 accent elements.

---

## Measurements

| Check | Result |
|---|---|
| axe (WCAG 2.2 AA + best practice), 16 URLs × 390/1440 (EN, AR, sushi, kitten, 404) | **0 violations**, no overflow on any run |
| Overflow | none at 320, 360, 768, 1024, 1920 (home, AR home, shop, custom, AR sushi, 404) |
| Lighthouse mobile, `LH_CPU=1` (my spot checks; host load 6–10) | `/shop/duck-teether-ring/` **99** / a11y 100 / BP 100 / SEO 100, LCP 2.0 s, TBT 0, CLS 0, 184 KiB · `/ar/` **99**, LCP 2.1 s, CLS 0.006, 273 KiB · `/shop/` **99**, LCP 2.1 s, CLS 0, 358 KiB. Below 0.9: only cache TTL, text compression, render-blocking CSS (local `http.server` artefacts) and `uses-responsive-images` on `/ar/` |
| Fonts (CDP `getPlatformFontsForNode`) | 404 AR h2 → **Baloo Bhaijaan 2** ✓, AR handle → Nunito ✓. EN header and footer «العربية» → the Baloo subset (`Baloo Switch`, 6 KB) ✓. `Nunito Fallback` now `loaded` ✓ |
| Keyboard (product 390/1440 EN/AR) | Skip link first. Visual order, RTL in AR. 2 px ring everywhere. The AR CTA is scrolled clear of the sticky bar by `scroll-padding-block-end` ✓ |
| Mobile menu (EN/AR) | Opens with `aria-expanded`, Tab → "Home" with ring, current page now underlined, Esc closes and returns focus ✓ |
| Sticky bar | PDP EN/AR/sushi: shows after the inline CTA leaves, hidden while it's visible ✓. Custom orders: observes both inline CTAs and hides while either is on screen ✓ |
| CTA position at 390 (first screen = 844) | EN duck 700–748, AR duck 818 bottom (tabbing scrolls it clear), AR sushi ≈ 768–818, tulip/kitten EN ≈ 717–765 ✓ |
| Shop chips (scripted scroll, `chips2.py`) | **Window scroll jumps: 4000 → 3964, 4400 → 4364, 5200 → 5164, and 2700 → 2664 on the way up.** "Baby" and "Fun & Novelty" are never marked current at the page bottom |
| Photo edges (w1200 crops at 2–6×) | panda contour **gone** · elephant cream pocket **gone** (now lilac) · bunny/duck clean · sushi now its own photo full-tile (no box-in-box) · **p207 kitten unchanged** (straight cut through the paws, a sliver of hand/chair between them) |
| `/ar/` 404 path | Not reachable locally (`http.server` serves its own error page). On GitHub Pages every path gets the bilingual `/404.html`. No separate AR 404, which is fine |

---

## Round-1 items: verified status

| # | Round-1 item | Status | Evidence |
|---|---|---|---|
| 1 | 404 AR heading in system font (AF) | **Fixed** | CDP: Baloo Bhaijaan 2 on `h2`, Nunito on the handle |
| 2 | Custom orders CTA below fold, right 45 % empty | **Fixed** | CTA at y ≈ 285 (390) / 293 (1440). Examples in the right column. Repeated after the steps. Sticky bar |
| 3 | PDP CTA missing from the first screen, sticky only after passing | **Fixed** | See CTA positions above. Bar logic now covers both directions |
| 4 | p207 kitten: cut edge + hand sliver | **Partly fixed** | Removed from home and related. Still in the shop grid and on its own PDP, unchanged |
| 5 | Panda grey contour | **Fixed** | `crops/panda1440-head.png` |
| 6 | Elephant cream pocket | **Fixed** | `crops/elephant-feet.png` |
| 7 | Shop single-tile rows / orphan | **Fixed** | "Gifts & more" (3), plushies lead tile 2×2 at ≥ 75em, no single-tile rows |
| 8 | Sushi box-in-box | **Fixed** | The scene photo fills the tile |
| 9 | `.lang` heaviest in header | **Fixed** | `--color-border` hairline, nav-sized |
| 10 | Home 390 text-only fold | **Fixed** | Photo + loupe + h1 + CTA all in the first screen, EN and AR, also at 320 |
| 11 | "checkout" / "card payment coming" | **Fixed** | Grep: only "There's no cart and no checkout" remains |
| 12 | Step 3 body about payment | **Fixed** | "Once the price and colors are agreed, we crochet your piece and arrange delivery." |
| 13 | Menu current page colour-only | **Fixed** | Underlined |
| 14 | Sticky bar could cover focus | **Fixed** | `scroll-padding-block-end: 6rem` |
| 15 | PDP alt repeats h1 | **Fixed** | Alt = description, EN and AR |
| 16 | Loupe soft | **Fixed** (adequate) | 400 px crops. Fine at 2×, still a little soft at 3× |
| 17 | `.side` misaligned | **Fixed** | Aligns with the first question |
| 18 | `Nunito Fallback` local() error | **Fixed** | `document.fonts`: loaded |
| 19 | Language link under "Follow" | **Fixed** | Moved to the footer base row |
| 20 | About thin | **Partly fixed, introduced a new issue** | Lead + side panel added, but the side panel duplicates the solid "Browse the pieces" already in the prose |
| 21 | "New pieces show up on Instagram first" | **Fixed** | "On Instagram" + the live wording |
| 22 | Dead band under the hero at 1440 | **Improved** | About 130 px now |
| 23 | Chips have no "you are here" | **Partly fixed, introduced a new issue** | Current chip is marked, but `scrollIntoView` moves the page vertically. The last two sections are never marked |
| 24 | AR feminine-only address | **Fixed, introduced a new issue** | All plural now, except «لم تجدوا ما تريدين؟» (agreement error, the auto-fail) |
| 25 | AR reads heavier | **Fixed** | `--weight-strong: 600` under `:lang(ar)` |
| 26 | FAQ invented reason | **Fixed** | "We confirm the making time when you message us." |
| 27 | 404 brand moment | **Fixed** | Empty loupe ring + "This page slipped a stitch" |

---

## Template notes (what changed my scores)

- **Home 8.6 SHIP.** The 390 fold now carries the signature, the headline and the CTA. The squint order is photo → h1 → CTA. Spacing 8: the 390 gallery hangs left at 72 % with the loupe overshooting, which is deliberate but leaves a ragged right edge, and there's still about 130 px of air before "Some of the pieces" at 1440. Copy 8: honest and plain, but no verifiable proof (none exists yet, so nothing to add).
- **Shop 7.7 BLOCK (8.1 without the auto-fail).**
  - Interaction 7: each new section yanks the page by about 36 px while you scroll. `chip.scrollIntoView({block:'nearest'})` also scrolls the window, because the sticky chip bar sits inside `scroll-padding-block-start: var(--space-xl)`. This happens in both directions and in both languages.
  - Consistency 8: the current chip uses an ink fill, while the nav and menu mark "you are here" with accent + underline. The breadcrumbs on the three merged products still say "Gift Sets / Seasonal / Accessories" but land on "Gifts & more".
  - Imagery 8: grid fixed, but the kitten still has its hand sliver.
- **Product 8.7 SHIP.** The CTA is in the first screen at 390 in EN and AR, the sticky bar works both ways, and the gallery is sticky at 1440. Exception: **`/shop/bee-costume-kitten/` Imagery 7.** The hero photo is cut by a straight edge through the paws with a brown sliver of hand or chair between them, and the loupe sits right over that area.
- **Custom orders 8.5 SHIP (just).** Fixed properly. Hierarchy 8, not 9: the two identical "Start a custom order" primaries are 693 px apart at 1440, so one 900 px viewport can show both. That's acceptable as repetition at a decision point, but it's the reason this isn't a 9. Brand 8: a plain page apart from the two tiles.
- **FAQ / Shipping 8.5 SHIP.** Promises removed, side card aligned. Copy 8: correct and plain.
- **About 8.3 REVISE.** Hierarchy 7: two solid "Browse the pieces" buttons (`.prose .cta-block .btn-primary` and `.side .btn-primary`, same href) sit 127 px apart in the 1440 fold, and about 500 px apart at 390 so they share a scrolled viewport.
  - Read literally, this is D1's auto-fail ("2+ equal-weight primary buttons in one viewport"). I scored it 7 rather than 2 because it's the same action to the same place, so it creates no choice. It still needs to go.
- **404 8.5 SHIP.** Fonts fixed, ring brand moment. Consistency 8: the ring and the "slipped a stitch" line exist only on the EN side, and the AR column says plainly «هذه الصفحة غير موجودة هنا», so the two halves aren't the same composition.

---

## Auto-fails
1. `/ar/shop/` `.cant-find h2`: «لم تجدوا ما تريدين؟». The plural verb (تجدوا) and the feminine-singular verb (تريدين) don't agree, so it's a typo-class error in a heading (D11). Source `build.py:214` (`cant_find_h`).

## Top 3 fixes (priority order)

1. **[Auto-fail · Copy · S]** `build.py` `cant_find_h` (renders `/ar/shop/` `.cant-find h2`): «لم تجدوا ما تريدين؟» → «لم تجدوا ما تريدونه؟». Clears the BLOCK and takes shop Copy 2 → 8 (shop 7.7 → 8.1).
2. **[Sev 3 · Interaction · S]** `assets/js/site.js`, shop chips: `chip.scrollIntoView({ block: 'nearest', inline: 'nearest' })` → `row.scrollBy({ left: r.left - rr.left - (rr.width - r.width) / 2, behavior: 'smooth' })`. This uses a physical delta, so it works in RTL too, and the window no longer moves. Also, when no `.cat` is inside the band and `innerHeight + scrollY >= document.body.scrollHeight - 2`, mark the last `.cat`. Takes shop Interaction 7 → 9 (8.1 → 8.3).
3. **[Sev 3 · Hierarchy · S]** `/about/` `.prose .cta-block` (the inline `.btn-primary` "Browse the pieces"): delete it, since `.side` already carries the action, or turn it into `.text-link`. Same in `/ar/about/`. Takes About Hierarchy 7 → 9 (8.3 → 8.5 SHIP).

## All other issues (severity-sorted)

| Sev | Selector / asset | Current → proposed | Dimension |
|---|---|---|---|
| 2 | `assets/img/p/p207/*` (kitten PDP + shop tile) | straight cut through the paws and a sliver of hand/chair → ask Rana for one reshot photo. Until then, either (a) crop above the paws (head and chest only) and say so in the alt, or (b) accept REVISE on that one page | Imagery (kitten PDP 7 → 8) |
| 2 | `.chip[aria-current="true"]` | `background: var(--color-text); color: var(--color-surface)` is a new "current" language → `background: var(--color-accent-subtle); color: var(--color-text); text-decoration: underline 2px; text-underline-offset: .4em`, matching `.nav a[aria-current]` | Consistency (shop 8 → 9) |
| 2 | `.crumbs a[href="/shop/#cat-more"]` on the 3 merged products | text "Gift Sets / Seasonal / Accessories" → "Gifts & more" / «هدايا وأكثر», so the label matches the section it opens | Consistency |
| 1 | `.lost-grid` (404) | ring + "slipped a stitch" only in the EN column → put the ring above both columns (or centred over the grid) and give the AR block the same line («انحلّت غرزة: هذه الصفحة غير موجودة») | Consistency, Brand |
| 1 | inline `onclick="gtag('event','instagram_click',…)"` | if the visitor taps "Order on Instagram" within about 1–3 s of landing, gtag.js is only injected on that `pointerdown` and the page navigates away, so the event is likely lost → add `transport_type: 'beacon'` and inject gtag.js on `DOMContentLoaded + idle` with a 1 s timeout (still not render-blocking) | Plumbing (P19) |
| 1 | `body.has-sticky .site-footer` on `/custom-orders/` | `padding-block-end: calc(var(--space-xl) + 5rem)` leaves about 150 px of empty ink band whenever the bar is hidden → keep it (the bar does show at the very bottom), but use `+ 4.5rem` to match the bar's real 72 px | Spacing |
| 1 | `.foot-lang` | underlined, unlike every other footer link → `text-decoration: none` with underline on hover, like `.site-footer ul a` | Consistency |
| 1 | `.loupe img` `stitch.*` | 400 px source, about 166 CSS px at 390 → soft at DPR 3 → export 520 px | Imagery |
| 1 | `/custom-orders/` 2nd `.btn-primary` at ≥ 52.5em | can share a 900 px viewport with the head CTA → at ≥ 52.5em, render the closing one as `.btn-secondary` (keep it primary at 390, where they're 1,000 px apart) | Hierarchy (custom 8 → 9) |
| 1 | home fold accent count | button, text link, logo ring, loupe ring (4 > 3) → accepted as brand. Noted only because it caps Colour at 8 together with the light-only decision | Colour |

## What stands between each page and ≥ 8.5 with no dimension < 8

| Page | Now | Blocking items | After those |
|---|---|---|---|
| Home | 8.6 SHIP | none | stays 8.6 |
| Shop | 7.7 BLOCK | (1) AR heading auto-fail · (2) chip scroll jump (Interaction 7) · then it still sits at 8.3, so it also needs (3) chip "current" style and breadcrumb labels (Consistency 9) and (4) Hierarchy 9: at 390 the 3-line lead pushes the first tiles to y ≈ 440. Shorten the lead to one line («Every piece is made by hand when you order it.») so a full row of tiles shows in the first screen | 8.5 with (1)–(4) |
| Product (template) | 8.7 SHIP | none | 8.7 |
| Product: kitten p207 | 8.6, Imagery 7 → REVISE | a reshot or a cleanly cropped hero (Rana-dependent for a full fix) | 8.7 |
| Custom orders | 8.5 SHIP (on the line) | none. The closing CTA as secondary at ≥ 52.5em would add margin (Hierarchy 9 → 8.6) | 8.6 |
| FAQ / Shipping | 8.5 SHIP | none | 8.5 |
| About | 8.3 REVISE | the duplicate primary (Hierarchy 7) | 8.5 |
| 404 | 8.5 SHIP | none. Mirroring the ring and line in AR adds margin | 8.5–8.6 |

So the **site** needs fixes 1–3 plus the two shop consistency items and the shop lead trim to reach SHIP on every template except the kitten page. That page needs a photo decision (reshoot, crop, or accept it as the one REVISE page).

## The 9.5 idea (unchanged, now closer)
Make the loupe interactive: on PDP and tiles the ring follows a tap or hover over Rana's full-resolution photo (a 1:1 crop, never retouched). Pair it with one in-hand photo per piece, so every product shows texture and scale in one gesture. That would also lift Imagery, the one dimension still capped at 8 sitewide.

---

## Evidence
`/home/taktekbot/design-work/critic-r2/`
- `*-390(-fold).png`, `*-1440(-fold).png` for: home, shop, duck, panda, tulip, sushi, kitten, custom, shipping, about, FAQ, AR home/shop/duck/sushi/custom/FAQ/about/shipping, 404, `/ar/no-such-page/` (local server's own 404)
- `axe.txt` (0 violations, 32 runs) · `lh_shop_duck-teether-ring_.json`, `lh_ar_.json`, `lh_shop_.json`
- `kb.txt`, `kb/`: tab stops, menu EN/AR, sticky bar on PDP EN/AR/sushi and custom EN/AR, 320 AR/EN home, 1024 shop/custom
- `kb-chips*.png` and scripted chip scroll log (`/tmp/critic/chips2.py`)
- `crops/`: `montage.png`, `panda1440-head.png`, `panda-head-3x.png`, `elephant-feet.png`, `kitten-low.png`, `bunny-3x.png`, `home-loupe.png`, `foot-lang.png`
