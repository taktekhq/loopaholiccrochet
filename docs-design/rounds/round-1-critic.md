# Design review, round 1: the redesign (independent critic)

**Site:** http://127.0.0.1:8765, branch `redesign`, commit `f7dd6d8`
**Date:** 2026-10-08
**Reviewer:** design-critic, scored against `brand/design/RUBRIC.md`. I read the designer's self-score (8.2–8.8) only after scoring, and did not use it.
**Goal:** Instagram visitors (Lebanon, Gulf, diaspora; 390 px first) see a handmade, made-to-order piece and DM on Instagram to order it. No public prices, no invented facts.
**Calibration:** refs `cuddleandkind`, `lalylala`, `saadeddin-ar`, `papier` (REFERENCES.md).

## Site verdict: **BLOCK**, site score **7.3** (lowest page: the 404)

One auto-fail holds the gate, and it is a one-rule CSS fix. On the bilingual 404, the Arabic heading renders in the **system fallback font** (`Noto Sans Arabic` on this machine) and the Arabic block's `@loopaholic.crochet` renders in `Liberation Sans` (the Arial fallback). The cause is that `h1, h2, h3 { font-family: var(--font-display) }` resolves to the Nunito stack at `:root` and beats the `font-family` that `:root:lang(en) [lang="ar"]` sets on the container. Measured with CDP `CSS.getPlatformFontsForNode`.

**Without the 404 auto-fail the site is a REVISE at about 7.8**, with custom orders the lowest page. This is a large step up from round 0's 4.6. The system, palette, type and Arabic edition are all sound now. What still holds the gate shut is conversion placement (the CTA misses the first screen on the AR product page, on longer EN products and on custom orders), photo-finishing artefacts, and a few thin or empty layouts at 1440.

---

## Per-template scores

Each dimension takes the lower of EN and AR. Overall = Σ(score×weight)/Σweight, rounded down. Imagery weighs 1.2 on shop and product. Conversion is left out on content pages and the 404, and Imagery is n/a on the 404 because it has no images.

| Dimension (wt) | Home | Shop | Product | Custom orders | Content (shipping/about/faq) | 404 |
|---|---|---|---|---|---|---|
| Hierarchy (1.5) | 8 | 8 | 8 | 7 | 8 | 8 |
| Typography (1.2) | 8 | 8 | 8 | 8 | 8 | **2 AF** |
| Spacing (1.2) | 8 | 7 | 8 | 7 | 8 | 8 |
| Colour (1.0) | 8 | 8 | 8 | 8 | 8 | 8 |
| Imagery (0.8 / 1.2) | 8 | 7 | 8 | 8 | 8 | n/a |
| Consistency (1.0) | 8 | 8 | 8 | 8 | 8 | 7 |
| Interaction (1.2) | 8 | 8 | 8 | 8 | 8 | 8 |
| Accessibility (1.3) | 9 | 9 | 9 | 9 | 9 | 9 |
| Performance (1.0) | 8* | 8* | 8* | 8* | 8* | 8* |
| Brand fit (1.0) | 8 | 8 | 8 | 8 | 8 | 7 |
| Copy (1.0) | 8 | 8 | 8 | 8 | 7 | 8 |
| Conversion (1.2) | 8 | 8 | 7 | 7 | n/a | n/a |
| **Overall** | **8.0** | **7.9** | **8.0** | **7.8** | **8.0** | **7.3** |
| Verdict | REVISE | REVISE | REVISE | REVISE | REVISE | **BLOCK** |

\* Performance is estimated, not measured with Lighthouse (see Measurements). The rubric says to take the lower anchor when unsure, so it stays at 8 until LCP is measured on a quiet machine or on the deploy.

EN vs AR splits that set a score: Typography EN 9 / AR 8 on home and product (the AR h1 at 45 px/1.35 in Baloo reads heavier than the EN h1, and the AR nav at 18 px bold outweighs the 13 px "English" switch). Conversion on product is EN 8 / AR 7 (the AR 390 CTA starts below the first screen).

---

## Measurements

| Check | Result |
|---|---|
| axe-core (WCAG 2.2 AA + best practice), 14 URLs × 390/1440, EN + AR + 404 | **0 violations** on every run |
| Horizontal overflow | none at 320, 390, 640 (≈200 % zoom at 1280), 768, 1024, 1440, 1920 on home, shop and AR product |
| WCAG 1.4.12 text-spacing override (AR product, EN product, AR home at 390) | no clipping. The only ellipsis is `.sticky-cta .name`, which truncates by design |
| Transfer, first view at 390 (Playwright CDP, local, no gzip/CDN) | home 203 KB / 16 req · shop 411 KB / 33 req (521 KB scrolled) · product 156 KB / 12 req · AR home 243 KB · AR product 195 KB · custom 106 KB · FAQ 83 KB |
| JS / CSS / fonts | JS 1.5 KB (`site.js`); gtag loads after `load` + idle. CSS 19.4 KB. 1 woff2 on EN (38 KB), 2 on AR (76 KB) |
| Cache-busting | `site.min.css?v=…`, `site.js?v=…`, fonts and lockup hashed ✓ |
| LCP image | `fetchpriority="high"`, AVIF/WebP `srcset`, `width`/`height` set ✓ |
| Lighthouse performance | **skipped on purpose.** Load average is ~57–60 on this machine, so TBT and LCP would measure the host, not the page |
| Type sizes in use (390 EN) | 13.4, 16.1, 18.0, 19.3, 27.9, 40.3 px: 6 steps, all on the fluid scale ✓ |
| Leading | EN body 1.5, h1 1.1. AR body 1.8, h1 1.35 ✓ |
| Fonts actually used | EN pages: Nunito. AR pages: Baloo Bhaijaan 2 + Nunito for Latin ✓. **404 AR h2: Noto Sans Arabic (system), AR handle: Liberation Sans** ✗. EN header/footer "العربية": system Arabic font (no Baloo `@font-face` on EN pages; acceptable for one word). `Nunito Fallback` reports `error` (`local("Arial")` is absent on Linux and Android, so the metric override does nothing there) |

**Keyboard** (product page, 390 and 1440, EN and AR; screenshots in `kb/`):
- The skip link is the first stop, visible and working (focus moves to `main`).
- The order runs logo → Shop → language → Menu → crumbs → **Order on Instagram** → Shipping details → related pieces → footer. In AR it runs right to left ✓.
- The ring is 2 px Loop purple with a 2 px offset on every stop, and switches to band-text on the footer ✓.
- Mobile menu: Enter opens it and sets `aria-expanded=true`, Tab lands on "Home" with a visible ring, and Esc closes it and returns focus to `summary` ✓ in both EN and AR.
- Sticky bar: hidden from the tab order until shown (`tabindex=-1`, `aria-hidden`), and it slides in after the inline CTA scrolls away ✓. It respects `safe-area-inset-bottom`. The AR product name truncates with an ellipsis ✓.

**Photo edges** (re-grounded `w1200.jpg`, cropped and zoomed 3–6×; `crops/`):
- Panda `p005`, the home hero and LCP image: a **1 px grey contour runs along the white yarn edge** (head and shoulders). You can see it at 1440 in the fold, and the loupe crop includes it at the top right.
- Kitten in a Bee Costume `p207`: the piece is **cut off by a straight horizontal edge** at the paws, with a sliver of skin or hand left at the bottom left. A thin dark outline runs around the white paws.
- Elephant plush `p003`: a cream (old-ground) pocket remains between the legs above the clear stand.
- Giraffe `p064`: slight light fringe on the dark feet. Acceptable at 1×.
- Kawaii Sushi Duo `p445`: a grey photo rectangle floats inside the lilac tile (box-in-box). Tulip gift box `p043`: the same with a white rectangle, less jarring.
- Duck, rose, lavender, octopus, bunny: clean.

---

## Template notes (key evidence)

### Home (`/`, `/ar/`): 8.0 REVISE
- **Hierarchy 8:** one solid CTA per view; the h1 says what and where. At 390 the fold is text only: the panda tile starts at y = 595 and the loupe, the site's signature, isn't in the first screen at all (cuddle+kind keeps product in the fold). In the header, the `.lang` pill (18 px Baloo with a 1 px `#8C7F96` border) outweighs "Shop" (13.4 px). The squint test lands on «العربية» before the nav. P1, P2.
- **Spacing 8:** on tokens, rhythm consistent. At 1440 there's about 200 px of dead band between the hero and "Some of the pieces" (`.hero` padding-block-end `--space-3xl` plus `.section` padding `--space-3xl`).
- **Imagery 8:** one ground, 1:1, `srcset` with AVIF. The hero has the grey contour described above. The loupe crop sits on the top edge of the head, so it shows the contour and the background instead of the densest stitches.
- **Colour 8:** in the home fold at 1440 there are 4 accent elements (button, text link, logo ring, loupe ring). The loupe ring is brand, but it's still accent spent on decoration. No dark mode, which is a documented decision but caps colour at 8.
- **Copy 8:** clear and honest. "New pieces show up on Instagram first" is a new claim the live site didn't make (it said "Follow the latest pieces…"). It's probably true, but confirm it with Rana or soften it.

### Shop (`/shop/`, `/ar/shop/`): 7.9 REVISE
- **Spacing 7:** at 1440, Gift Sets, Seasonal and Accessories are each a **single tile in a 4-up grid**, three orphan rows in a row, and Plushies ends with one orphan ("Kitten in a Bee Costume"). This is the CHECKLIST "orphan card on its own row" fail. The page is 6,250 px tall at 1440.
- **Imagery 7:** the truncated kitten and the box-in-box sushi sit in the same grid as clean cut-outs. The scale of the piece inside the tile varies a lot: the duck fills about 80 %, the sushi pieces about 15 %.
- **Hierarchy 8:** the sticky chips bar is good, but chips have no "current section" state while you scroll.
- **Conversion 8:** "Can't find it?" closes the page as one muted paragraph with an inline link. Fine, but it's the custom-order route and it's quiet.

### Product (`/shop/<slug>/`, `/ar/shop/<slug>/`): 8.0 REVISE
- **Conversion 7 (AR):** at 390 the AR duck CTA starts below the first screen (the price note sits at y ≈ 820). On EN, the CTA bottom is at 829 of 844 for the duck and is cut off for the sushi and tulip, whose descriptions are longer. The sticky bar only appears **after** the inline CTA has scrolled above the viewport (`rootMargin: 0 0 100000px 0`), so while the CTA is still below the fold there is no CTA on screen. The two-line `.loupe-note` (about 50 px) is what pushes it out.
- **Hierarchy 8:** one primary per view; meta is muted; the h1 is dominant.
- **Copy 8:** step 3 is titled "We make it by hand" but its body is about payment and shipping. "Whish or cash on delivery" appears **3 times** on one page (steps, delivery block, plus the shipping link target). The facts are carried over from live (48 h, Whish/COD) ✓.
- **Imagery 8:** the loupe is real and works well on the duck. On the sushi it's a soft crop (a 300 px source shown at about 130 CSS px, so under 1× on DPR-3 phones). The product `alt` is "Duck Teether Ring, handmade crochet", which repeats the h1 and doesn't describe the piece. The description is right there and would make a better `alt`.
- **1440:** the CTA and h1 are above the fold, and the sticky gallery is good.

### Custom orders (`/custom-orders/`, `/ar/custom-orders/`): 7.8 REVISE (lowest page after the 404 fix)
- **Hierarchy 7 / Conversion 7:** "Start a custom order" sits at the bottom, below the fold at 390 (y ≈ 1150) and at 1440. There's no sticky bar or side CTA, unlike /faq/ and /shipping/, which have `.side`.
- **Spacing 7:** at 1440 the content is one 65ch column with the **right ~45 % of the page empty**, and the examples are two tiles in a 34 rem box. The `.prose-layout` + `.side` component the content pages use isn't used here.

### Content (`/shipping/`, `/about/`, `/faq/` + AR): 8.0 REVISE
- **Copy 7:**
  - Shipping keeps "until our checkout can calculate it automatically", and FAQ keeps "online card payment is coming". Both promise features that don't exist and contradict the home page's new "There's no cart and no checkout". They're carried from live, but the redesign made the contradiction visible.
  - FAQ "It depends on the piece and on how many orders are in progress" adds a reason the client didn't give.
- **Hierarchy 8:** the `.side` card top (y = 307) aligns with neither the lead nor the first question (y = 260) at 1440.
- **About** is thin: no lead, three 110 px thumbnails, three paragraphs. A page about the person who makes the pieces never shows the person or the hands. That's a missed opportunity, not a fact to invent.

### 404 (`/404.html`): 7.3 BLOCK
- **Typography 2 (auto-fail):** the AR `h2` "الصفحة غير موجودة" is in Noto Sans Arabic (system fallback), while the paragraph and links below it are in Baloo. `@loopaholic.crochet` in the AR block is Liberation Sans.
- **Brand 7:** correct header and footer and a bilingual block (good), but it's plain text links. No photo and no ring, so it's the one template that doesn't look like Loopaholic (RUBRIC D10 9 asks for brand in states).
- HTTP status for an unknown path is 404 ✓. Three links plus an Instagram contact ✓.

---

## Auto-fails
1. `/404.html` `[lang="ar"] h2`: system fallback font (Noto Sans Arabic), measured with `CSS.getPlatformFontsForNode`. `[lang="ar"] bdi` renders in Liberation Sans.

## What works (keep)
- The kit is applied for real: paper `#FAF7FC`, ink, one Loop purple on actions, Nunito plus a rounded Arabic face that rhymes with it. Round 0's cream + serif + terracotta is gone.
- **The loupe** is an honest, ownable signature: a crop of Rana's own photo, labelled as such, and it mirrors correctly in RTL. Product and home are recognisable without the logo.
- Honesty engine: no prices, no sizes or making times without confirmation, the safety answer kept, the `check_claims()` build guard. Every fact I checked (48 h, Whish/COD, Gulf list, deposit, examples) traces to the live site.
- Accessibility is genuinely clean: 0 axe issues over 28 runs, a skip link, 44 px targets, focus ring on every stop, Esc + focus return on the menu, reflow and text-spacing pass.
- Weight discipline: 1.5 KB JS, 19 KB CSS, one font per script, hashed URLs, product page under 160 KB at first view.
- The sticky order bar is well built (out of the tab order until shown, safe-area, truncation).

---

## Top 3 fixes for the whole site (priority order)

1. **[Auto-fail · Typography · S]** `:root:lang(en) [lang="ar"]`: `font-family: "Baloo Bhaijaan 2", sans-serif` → `--font-body: "Baloo Bhaijaan 2", "Nunito", "Nunito Fallback", sans-serif; --font-display: var(--font-body); font-family: var(--font-body);`. Setting the variables, not just `font-family`, lets the AR `h2` (which uses `var(--font-display)`) and the Latin handle pick up the right faces. That lifts 404 Typography 2 → 8 and the 404 from 7.3 → about 8.0, and clears the BLOCK.
2. **[Sev 3 · Conversion + Hierarchy + Spacing · M, lowest page]** `/custom-orders/` `.wrap.section.flush`: change the layout from a single `.prose` column to the existing `.prose-layout` + `.side` (as on /faq/ and /shipping/). Put the "Start a custom order" `.btn-primary` (and its "Opens a direct message…" note) in `.side`, so it's in the 1440 fold and fills the empty right 45 %. At < 52.5em, `.cta-block` order: after `.examples` → directly after the first `.prose` (CTA at y ≈ 450 instead of ≈ 1150). That lifts custom orders H 7→8, S 7→8, Conv 7→8: 7.8 → about 8.2.
3. **[Sev 3 · Conversion · S]** `assets/js/site.js`, the `.sticky-cta` observer: `rootMargin: '0px 0px 100000px 0px'` → the default root, so the bar shows whenever `#order-cta` is off-screen in **either** direction (still correct on a fast scroll, because the state is read on every intersection change). Also move `.loupe-note` out of the fold: `margin-block-start: var(--space-m)` → put it in `figure.loupe` as a `figcaption.vh`, since the alt "Close-up of the stitches" already says it. That puts a CTA in the first screen on every PDP, in EN and AR. Product Conv 7→8 and product 8.0 → about 8.1. Reuse the same bar on custom orders.

After these three, the site would be around 7.9–8.0 (shop is then the lowest), still REVISE. The next lifts are the photo fixes and the shop orphans (issues 1–3 below).

## All other issues (severity-sorted)

| Sev | Selector / asset | Current → proposed | Dimension |
|---|---|---|---|
| 3 | `assets/img/p/p207/*` (Kitten in a Bee Costume) | piece cut by a straight horizontal edge, a sliver of hand bottom-left, dark rim on white paws → re-cut from the original with the full piece, or drop it from the grid until Rana sends a full shot | Imagery (shop 7→8) |
| 3 | `assets/img/p/p005/*` (panda, home LCP + shop + related) | 1 px grey contour along white yarn → erode the matte 1 px before the 2 px fringe blend (`make_images.py`), and check the other white-yarn pieces (p016 bunny, p066 daisy, p207) | Imagery |
| 3 | `.grid` on `/shop/` at ≥ 75em | Gift Sets / Seasonal / Accessories each 1 tile, plus a Plushies orphan → merge the single-item categories into one "Gifts, seasonal and accessories" section (the chips stay) or switch those rows to `grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr))` without the empty columns | Spacing (shop 7→8) |
| 2 | `.tile img` for `p445` sushi (and `p043` tulip) | grey or white photo rectangle floating on lilac → crop the photo's own margin and render `object-fit: cover` (e.g. a `.tile.scene` modifier), so the scene is the ground instead of a box-in-box | Imagery, Consistency |
| 2 | `.lang` (EN pages: `.lang:lang(ar)`) | 18 px Baloo + 1 px `--color-border-strong` pill, the heaviest thing in the header → `font-size: calc(var(--text--1) * 1.12)` and `border-color: var(--color-border)`; on AR pages, `.lang:lang(en)` 13.4 px → `var(--text-0)` so both switches match their nav | Hierarchy, Consistency |
| 2 | `.hero` at < 52.5em | text-only fold, signature off-screen → place `.gallery` before the copy, or cap the tile at `max-inline-size: 70%` and drop `.hero h1` to `--text-4` at 390 so the tile and loupe enter the fold | Hierarchy, Brand |
| 2 | `/shipping/` "until our checkout can calculate it automatically", FAQ "online card payment is coming" | promises of features that don't exist; contradicts home's "no cart and no checkout" → "Shipping cost is quoted on Instagram once we know your city" / "Internationally: message us and we'll arrange payment" (`[CLIENT TO CONFIRM]` if card payment is really planned) | Copy |
| 2 | `.steps li:nth-child(3)` (home, PDP, side) | heading "We make it by hand" with a payment/shipping body → body: "Once the price and colors are agreed, we crochet your piece and arrange delivery." Keep payment in the Delivery block only (it currently appears 3× on the PDP) | Copy |
| 2 | `.menu-sheet a[aria-current="page"]` | colour only → add `text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: .4em` as `.nav a[aria-current]` does | Colour (signal), Consistency |
| 2 | `.sticky-cta` vs focus | focused related tiles can sit under the 72 px bar → `html { scroll-padding-block-end: 6rem }` when `body.has-sticky` (WCAG 2.4.11) | Accessibility |
| 2 | `.pdp .tile img` `alt` | "Duck Teether Ring, handmade crochet" repeats the h1 → use the catalog description ("A crocheted duck head with an orange beak and feet, set on a pale lavender teether ring."), AR likewise | Accessibility, Imagery |
| 1 | `.loupe img` source `stitch.*` | 300 px crop shown at about 130–184 CSS px → export 600 px (`srcset 1x, 2x`) and centre the crop on the densest stitches, away from the silhouette edge (the panda loupe currently shows the halo) | Imagery |
| 1 | `.side` (FAQ, shipping) at ≥ 52.5em | `margin-block-start: var(--space-xl)` lands at y = 307, aligned with nothing → `0`, aligned to the first `h2` | Spacing |
| 1 | `@font-face "Nunito Fallback"` | `src: local("Arial")` errors on Android/Linux → add `local("Roboto"), local("Liberation Sans"), local("Helvetica")`, or the font swap can shift the hero h1 on Android | Performance (CLS) |
| 1 | `.foot-grid` "Follow" column | the language switch is listed under "Follow" → move it to `.foot-base` | Consistency |
| 1 | `/about/` | no lead, three 110 px thumbnails → a lead plus one large in-hand or work-in-progress photo **if Rana provides one** (no invented bio) | Brand, Imagery |
| 1 | home "New pieces show up on Instagram first" | new, unconfirmed claim → "See new pieces and works in progress on Instagram" (what live said) | Copy |
| 1 | `.hero` + first `.section` at ≥ 52.5em | about 200 px dead band → `.hero { padding-block-end: var(--space-2xl) }` | Spacing |
| 1 | `.chips` | no "you are here" while scrolling → optional `aria-current` via IntersectionObserver on `.cat` | Interaction |
| 1 | AR addressing | feminine imperatives only (تصفّحي، اطلبي، راسلينا) exclude male gift buyers. Carried from live and a defensible audience choice; confirm with Rana | Copy (AR) |

## Missed opportunities (non-blocking)
- **A gift-buyer entry point** (REFERENCES lesson 7). The self-check dropped it to avoid suitability claims. That's right for "for a new baby", but a neutral "Flowers that keep / Something to cuddle / Baby pieces" row maps directly onto the existing categories with no claim.
- **The 404 as a brand moment:** one lilac tile with a single piece and the loupe ring empty ("This page slipped a stitch") would make the error state recognisably Loopaholic.
- **In-scale shots** (a piece in a hand) remain the one thing that would push Imagery to 9. Ask Rana for even 5.

## The 9.5 idea
Make the loupe **interactive and site-wide as the "see the stitches" layer**: on every tile and PDP, the ring follows a tap or hover over Rana's full-resolution photo (a real 1:1 crop, no retouching). Pair it with one in-hand photo per piece, so each product carries scale (hand) and texture (loupe) as one gesture. That is the cuddle+kind "count the stitches" lesson, turned into the thing people remember the site for.

---

## Evidence
`/home/taktekbot/design-work/critic-r1/`
- `*-390.png`, `*-390-fold.png`, `*-1440.png`, `*-1440-fold.png`: home, shop, products (duck teether ring, panda, tulip gift box, sushi duo), custom orders, shipping, about, FAQ, AR home/shop/duck/sushi/custom/FAQ/about, 404
- `axe.txt`: axe output, 0 violations, no overflow
- `kb.txt`, `kb/`: keyboard tab stops with screenshots, menu open/Tab/Esc (EN/AR), sticky bar (EN/AR/sushi), skip link, 320/768/1024 views, text-spacing shots
- `crops/`: photo-edge zooms (`panda1440-head.png`, `kitten-low.png`, `elephant-feet.png`, `giraffe-6x.png`, `sushi-corner.png`, `montage.png`, `loupe1440.png`, `404-ar.png`)
- Transfer sizes and font checks: Playwright CDP scripts in `/tmp/critic/` (`meas.py`, `f404.py`, `ts.py`)
