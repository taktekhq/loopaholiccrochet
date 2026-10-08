# Design review, round 3: fixes + live stitch magnifier (independent critic)

**Site:** http://127.0.0.1:8765, branch `redesign`, commit `c1fbcfe`
**Date:** 2026-10-08
**Reviewer:** design-critic, scored from scratch against `brand/design/RUBRIC.md`, then a full pass of `brand/design/CHECKLIST.md`. I checked every round-2 item myself.

## Verdict

- **RUBRIC gate: met on every page.** Every template scores ≥ 8.5, no dimension is below 8, and there are no auto-fails. The lowest pages (shop, FAQ/shipping, About, 404) sit at 8.5.
- **Ship rule including CHECKLIST: NOT YET (REVISE).** 13 CHECKLIST boxes fail:
  - **8 are small build fixes** (an hour or two together; table A).
  - **3 need a ruling** from the overseer or the client (table B).
  - **2 can only be confirmed after deploy** (table C).
- **Recommendation:**
  1. Fix table A.
  2. Rule on table B.
  3. Deploy.
  4. Confirm table C on the live site.
  5. Ship. Nothing in the design itself still blocks.

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
| Interaction (1.2) | 9 | 9 | 8 | 9 | 9 | 9 | 9 |
| Accessibility (1.3) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Performance (1.0) | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Brand fit (1.0) | 9 | 8 | 9 | 8 | 8 | 8 | 9 |
| Copy (1.0) | 8 | 8 | 9 | 8 | 8 | 8 | 8 |
| Conversion (1.2) | 8 | 8 | 9 | 9 | n/a | n/a | n/a |
| **Overall** | **8.6** | **8.5** | **8.6** | **8.6** | **8.5** | **8.5** | **8.5** |
| RUBRIC verdict | SHIP | SHIP | SHIP | SHIP | SHIP | SHIP | SHIP |

The kitten PDP (`/shop/bee-costume-kitten/`) is now Imagery 8: a presentation crop to the head and paws with no hand, and the alt says it's cropped. It scores 8.6 like the product template.

**What moved since round 2:**
- **Shop:** the auto-fail is fixed. Interaction 7 → 9 (chip scrolling verified, see below). Consistency 8 → 9 (chip "current" now matches the nav; breadcrumbs say "Gifts & more"). Hierarchy 8 → 9 (one-line lead, first row of tiles in the 390 first screen).
- **About:** Hierarchy 7 → 9 (the duplicate primary is gone).
- **Custom orders:** Hierarchy 8 → 9 (the closing CTA is secondary at ≥ 52.5em).
- **404:** Consistency 8 → 9 (ring centred over both columns, AR line added).
- **Product:** Interaction 9 → 8. The new magnifier is good with mouse and touch, but its **keyboard focus state shows an empty lilac circle** (issue 1 below). Brand stays 9: the magnifier makes the signature interactive, and 10 would need the in-scale photography to go with it.

**Ceilings that are anchor rules, not judgement:**
- Imagery is 8 everywhere because there are no in-scale shots.
- Colour is 8 because the site is light-only by decision and has no second theme.
- Spacing is 8 because the rhythm is consistent but has no optical-alignment extras.

---

## Measurements

| Check | Result |
|---|---|
| axe (WCAG 2.2 AA + best practice), 17 URLs × 390/1440 (EN, AR, sushi, kitten, AR shipping, 404) | **0 violations** on 34 runs, no overflow |
| axe with the magnifier live | 0 violations: mouse-live 1440 EN/AR, touch-live 390 EN/AR, keyboard-live 390/1440 EN/AR |
| Lighthouse mobile `LH_CPU=1` | `/shop/duck-teether-ring/` **99**, LCP 2.0 s, CLS 0, 191 KiB · `/ar/shop/duck-teether-ring/` **98**, LCP 2.2 s, CLS 0.004, 224 KiB · `/` **99**, LCP 2.1 s, CLS 0, 247 KiB · a11y / BP / SEO 100 on all three. Below 0.9: local-server artefacts (cache TTL, no gzip, render-blocking CSS) plus `unminified-javascript` (`site.js` 8.5 KB, not minified, unlike the CSS) |
| Magnifier cost | `w1200` is **not requested at load** (0 requests before interaction), then fetched once on the first hover, tap or focus. CLS during use is 0. The AR page's 0.0026–0.004 is from page load, before any interaction |
| Console / failed requests (8 pages, scrolled) | none |
| Overflow | none at 320–1920 (round-2 sweep, layout unchanged except the 404 ring) |
| Shop chips, scripted scroll 0 → 5600 → 0, EN + AR | **no window jumps** (scrollY exactly as set at every step). Every section, including Baby and Fun & Novelty, gets marked. RTL row scroll works (negative `scrollLeft`). One stale state: **jumping** from the bottom straight to the top (Home key, `scrollTo(0,0)`) leaves "Fun & Novelty" marked (issue 3) |

### Magnifier test (`/tmp/critic/mag.py`; shots in `critic-r3/mag/`)

| Mode | EN | AR | Notes |
|---|---|---|---|
| Mouse (1440) | ✓ | ✓ | The ring follows the pointer, shows the full photo at 1 photo px per CSS px (about 2× at 1440), and returns to its corner on `pointerleave`. At the tile corner the ring centres on the cursor and hangs half outside the tile, showing empty lilac and running under the header (`mag/en-1440-mouse-corner.png`) |
| Touch (390, DPR 3, `hasTouch`) | ✓ | ✓ | Tap the photo and the ring jumps there. Dragging the ring moves it without scrolling the page (`scrollY` 0). **A vertical swipe on the photo still scrolls the page** (`scrollY` 320 / 340): no scroll trap. Tapping outside closes it. The view is soft at about 3.3× on a DPR-3 phone, the honest limit of a 1200 px source |
| Keyboard | ✓ | ✓ | The ring is a tab stop (8th at 390, 11th at 1440) between the crumbs and the CTA. It has `role="application"`, an `aria-roledescription` and a label in the page language with instructions. Arrows and Shift+arrows move it and don't scroll the page. Esc puts it back and keeps focus. Tab moves on to "Order on Instagram". **On focus the ring goes live at its resting corner, which is empty ground, so the focus state is a blank lilac circle** (`mag/en-390-kb-focus.png`) |
| Discoverability | ✓ desktop | ✓ desktop | The hint "Move over the photo: the ring shows the stitches up close." shows only with hover at ≥ 52.5em. Touch visitors get no cue that tapping does anything |

---

## Round-2 items: verified status

| Round-2 item | Status | Evidence |
|---|---|---|
| AF «لم تجدوا ما تريدين؟» | **Fixed** | `/ar/shop/` now «لم تجدوا ما تريدونه؟». A sweep of all AR pages for feminine-singular forms finds none |
| Chips scroll the window | **Fixed** | Scripted EN and AR: no window movement. `row.scrollBy` with a physical delta |
| Last sections never marked | **Fixed** | "Baby" at 4400–4800, "Fun & Novelty" at 5200–5600 |
| About duplicate primary | **Fixed** | One `.btn-primary` (side panel) |
| Kitten p207 | **Fixed (presentation crop)** | Head + paws, no hand, alt says it's cropped (`kitten-crop.png`). It's a tighter crop than the house margin, accepted. A reshoot is still worth asking for |
| Chip current = ink fill | **Fixed** | accent-subtle + 2 px underline |
| Breadcrumb labels | **Fixed** | "Shop / Gifts & more" |
| 404 ring/line EN-only | **Fixed** | Ring centred, «انحلّت غرزة: …» |
| GA early-tap loss | **Fixed (per code)** | `transport_type: 'beacon'`, idle-load capped at 1 s. Confirm in DebugView after deploy |
| Custom orders footer band | **Fixed** | `+ 4.5rem` |
| `.foot-lang` underline | **Fixed** | Underline on hover only. The label is now just «العربية» / "English" |
| Loupe 520 px | **Superseded** | Replaced by the live magnifier. The static 400 px crop is the no-JS view. Accepted |
| Custom closing CTA in the same viewport | **Fixed** | Secondary at ≥ 52.5em, implemented by restyling `.btn-primary` inside `.c-how` (see issue 7) |
| Shop lead too long | **Fixed** | One line, tiles in the first screen |

---

## CHECKLIST: end-to-end result

Checked on the built HTML/CSS (greps and parsers), with Playwright and CDP, and in the screenshots. Everything not listed passes or is n/a. The n/a items are:
- **No price or forms:** `tabular-nums`, async/loading, errors, inputs.
- **No WhatsApp channel yet:** the WhatsApp prefill box.
- **No overlays:** the menu is a non-modal `<details>`, so "modals trap focus" doesn't apply.
- **No full-height sections:** the `svh` box.

### A. Fails, fixable now (all small)

| # | CHECKLIST box | Evidence | Fix |
|---|---|---|---|
| A1 | Curly quotes | `shop/heart-bouquet-stand/`: "a Valentine's/gifting piece" with a straight `'` in visible text, meta description, og:description and JSON-LD (`&#x27;`) | `catalog.json`: `'` → `’`, and while there, "a Valentine’s gift" rather than "Valentine's/gifting piece" |
| A2 | Every colour is a token | `.foot-base { border-block-start: 1px solid rgb(241 235 246 / .2) }`, the only raw colour outside `:root` | add `--color-band-line: rgb(241 235 246 / .2)` and use it |
| A3 | Body ≥ 18 px AR at 360 | AR body at 360 = `16px × 1.12` = **17.92 px** | `:root:lang(ar) { --script-scale: 1.125 }` (18.0 px), or raise the `--text-0` floor for AR |
| A4 | `srcset` with 3–5 widths | AVIF has 400/800/1200, but the **WebP source has only 400w and 800w** (every product/tile `picture`) | add `w1200.webp 1200w` (or drop the WebP source, since every browser that matters takes AVIF and the JPEG is the fallback) |
| A5 | Meta description ≤ 155 chars | `/shipping/` = **171** chars (carried over from live) | "Order on Instagram. Pay by Whish or cash on delivery in Lebanon. We confirm delivery time when you order." (110) |
| A6 | Favicon set | **No `/favicon.ico`** at the root (browsers and crawlers request it blindly, so it will 404). `icon.svg` has no dark variant (it carries its own paper square, so it's still visible, but the box asks for one). The maskable 512 has the ring reaching radius 44 %, outside the 40 % safe zone, so launchers that mask will clip it | add `favicon.ico` (32), split `purpose: "any"` / `"maskable"` with a padded maskable PNG, add `@media (prefers-color-scheme: dark)` in `icon.svg` |
| A7 | OG image per template, EN **and** AR | Home, shop, custom, shipping, about, FAQ and the 404 share `/assets/img/og.jpg`, which carries English text ("Handmade crochet"), so the AR pages' WhatsApp preview is in English. Product OGs have no text and are fine for both | render `og-ar.jpg` with «كروشيه يدوي» and point the AR non-product pages at it |
| A8 | Latin brand names wrapped in `<bdi>`/`dir="ltr"` | "Whish" in AR running text (AR shipping, FAQ, PDP delivery, steps) and "Loopaholic" in the AR footer © line are unwrapped. They render correctly today because each is a single word, but the box is explicit | `<bdi dir="ltr">Whish</bdi>` in the AR strings in `build.py` |

### B. Fails that need a ruling (overseer or client)

| # | CHECKLIST box | Evidence | My recommendation |
|---|---|---|---|
| B1 | "No Arabic font downloaded on EN pages" | EN pages load `Baloo Switch`, a **6 KB** Arabic subset for the single word «العربية» (header + footer) | **Grant a written exception.** The box exists to stop the 38 KB Arabic body face loading on EN pages. Dropping the subset would show a system Arabic fallback in the header, which RUBRIC D2 auto-fails. Note the exception in `PLAN.md` |
| B2 | "Each product has an in-scale shot and a texture shot" | Texture: ✓ (static crop + live magnifier). In-scale: none (one photo per piece) | Client-dependent. Ask Rana for in-hand photos. Ship without them, recorded as a known gap, since no build change can satisfy it |
| B3 | "Arabic copy … checked by a native reader" | No native-reader sign-off exists. Round 2 shipped an agreement error that only a read-through caught | Have Rana (or a native Levantine reader) read the AR home, shop, PDP template, custom, shipping, FAQ, about and 404 once before ship. 15 minutes. Then tick the box |

**Accent count note (not counted as a fail):** "≤ 3 accent-coloured elements per viewport". I counted the logo ring as the brand mark, not UI colour. With it excluded, the home fold has 3 (loupe ring, CTA, "How ordering works") and the PDP fold has 3 (current "Shop", the loupe, which is now a control, and the CTA). If the overseer counts the logo, both folds have 4, and the cheapest fix is `.hero .text-link { color: var(--color-text) }` (keeping the underline).

### C. Fails or unknowns that can only be confirmed after deploy

| # | CHECKLIST box | Local evidence | Verify on live |
|---|---|---|---|
| C1 | LCP ≤ 2.0 s | 2.0 (product), 2.1 (home), 2.2 s (AR product) on `http.server` with **no gzip and no CDN** | Lighthouse mobile on the deployed URLs (default throttling, plus `LH_CPU=1` if the host is loaded). With gzip it should come in under 2.0. If AR product doesn't, preload its LCP AVIF |
| C2 | 404 returns HTTP 404 and is served for unknown paths | Local `http.server` serves its own page for unknown paths (`/ar/no-such-page/` showed the Python error page in round 2) | `curl -sI https://loopaholiccrochet.com/nope/` and `/ar/nope/` → 404 with the bilingual page |

---

## Remaining issues (non-CHECKLIST, severity-sorted)

| # | Sev | Where | Current → proposed | Dimension |
|---|---|---|---|---|
| 1 | 2 | `site.js` magnifier: `lp.addEventListener('focus', … fromRing())` | On keyboard focus the lens goes live at the ring's resting corner, which is empty ground, so the focused control shows a **blank lilac circle** and the static stitch close-up disappears → on focus, keep the static crop and only go live on the first arrow key, starting from the crop's own centre (emit `data-cx`/`data-cy` for the stitch crop from `make_images.py`) | Interaction (product 8 → 9) |
| 2 | 1 | magnifier, `at()` | The ring can be centred right at the tile edge, so half of it shows empty ground and it slides under the header → clamp `pos.x/y` to `[r/w, 1 − r/w]` (ring radius over tile size) so the lens always shows photo | Interaction |
| 3 | 1 | `site.js` chips, scroll handler | An **instant** jump from the bottom to the top leaves "Fun & Novelty" marked (verified EN and AR). Smooth scrolls are fine → in the `scroll` listener, also clear `aria-current` and reset the row when `cats[0].getBoundingClientRect().top > innerHeight * 0.3` | Interaction |
| 4 | 1 | PDP at < 52.5em or no-hover | No cue that the ring is interactive on touch → show a short `.loupe-hint` variant under touch ("Tap the photo to look closer." / «اضغطوا على الصورة لرؤية الغرز عن قرب.») | Interaction, Brand |
| 5 | 1 | `assets/js/site.js` | 8.5 KB unminified (Lighthouse `unminified-javascript`). The CSS is minified and hashed, the JS only hashed → minify in `build.py` like the CSS | Performance |
| 6 | 1 | `shop/heart-bouquet-stand/` description | "a Valentine's/gifting piece" is the one slash-phrase in the catalogue → "a Valentine’s gift" (fixes A1 too) | Copy |
| 7 | 0 | `.c-how .cta-block .btn-primary` | The secondary look is achieved by overriding `.btn-primary`, so the markup says primary and the CSS says secondary → emit `.btn-secondary` at ≥ 52.5em, or give that link both classes and let a media query switch them. Code hygiene only, nothing visible | Consistency |

---

## If tables A and B are closed: SHIP, then verify these on the live site
1. `curl -sI` a few unknown paths (EN and `/ar/…`) → **404** with the bilingual page (C2).
2. Lighthouse mobile on `/`, `/shop/`, `/shop/duck-teether-ring/`, `/ar/shop/duck-teether-ring/` → perf ≥ 90 and **LCP ≤ 2.0 s** (C1). CLS stays ≤ 0.05.
3. Asset caching: the HTML references the new `?v=` hashes for CSS, JS and fonts, and `curl -sI …site.min.css?v=<hash>` shows the fresh file (Cloudflare caches CSS and JS for 4 h).
4. GA4 DebugView: `instagram_click {product}` fires on a fast tap (within 1–2 s of landing) and a slow one. `custom-orders` clicks carry `page`.
5. The `ig.me/m/loopaholic.crochet` CTA opens the DM in the Instagram app on a real iPhone and a real Android, from both EN and AR pages.
6. Magnifier on a real iPhone (Safari) and Android (Chrome): tap, drag, page scroll over the photo, tap-outside close, and that the AVIF `background-image` renders in Safari's lens.
7. Link previews in WhatsApp for `/`, `/ar/`, a product, and an AR product (EN vs AR OG after A7).
8. Rich Results Test: Product + BreadcrumbList on a product, FAQPage on `/faq/` and `/ar/faq/`, Organization on home.
9. Search Console: sitemap (86 URLs) resubmitted, hreflang pairs reported without errors after the crawl.
10. `/favicon.ico` returns 200 (after A6), and the tab icon is visible in a dark browser theme.

---

## Evidence
`/home/taktekbot/design-work/critic-r3/`
- `*-390(-fold).png`, `*-1440(-fold).png`: home, shop, duck, panda, tulip, sushi, kitten, custom, shipping, about, FAQ, AR home/shop/duck/sushi/custom/FAQ/about/shipping, 404
- `axe.txt` (34 runs, 0 violations) · `lh_shop_duck-teether-ring_.json`, `lh_ar_shop_duck-teether-ring_.json`, `lh_.json`
- `mag/` + `mag.txt`: magnifier mouse/touch/keyboard EN and AR, axe in each live state, CLS, lazy-load requests
- `kb-chips_shop_top.png`, `kb-chips_ar_shop_top.png` (stale chip after a jump to top) · `kitten-crop.png`
- Scripts in `/tmp/critic/` (`mag.py`, `chips2.py`, `chips3.py`, `chips4.py`, `console.py`, `meas.py`)
