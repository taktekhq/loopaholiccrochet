# Round 2: designer response to the round-1 critic (2026-10-08)

Critic: `round-1-critic.md` (7.3 BLOCK, 404 auto-fail). Overseer decisions applied (AR plural address,
Instagram wording, no "checkout coming" copy, p207, halos, shop singles, GA on first interaction,
home 390 fold). Screens: `/home/taktekbot/design-work/r2/`, kept set in `../after/`.

## Measurements
- axe, 16 URLs × 390/1440 (EN, AR, 404, sushi PDP): 0 violations, no overflow.
- Lighthouse mobile, `LH_CPU=1` (stable on the loaded XPS): perf 99–100 on home, shop, product,
  custom, FAQ, AR home, AR product, 404; a11y/BP 100; SEO 100 (404: 66, it is `noindex` on purpose).
  LCP 1.7–2.1 s, TBT 0, CLS ≤ 0.006, 93–285 KiB.
- CTA bottom at 390: EN duck 765, sushi 789, tulip 765; AR duck/sushi 818 (viewport 844). Sticky bar
  shows whenever no inline order button is on screen, either direction.
- 404 fonts (CDP `getPlatformFontsForNode`): AR h2 Baloo Bhaijaan 2 (+ Nunito for Latin), AR handle
  Nunito; no system fallback.
- GA (real-browser UA, gtm stubbed): gtag.js not requested at DOMContentLoaded, requested on the first
  pointerdown; idle path also loads it; click queues `instagram_click {product}` after js/config.
- Plumbing: same 86 URLs + 404, sitemap identical, JSON-LD parses on every page.

## Critic item → what changed
| Critic item | Done |
|---|---|
| AF 404 AR heading in system font | `:root:lang(en) [lang="ar"]` now sets `--font-body/--font-display` (Baloo → Nunito); verified with CDP |
| Custom orders CTA below fold, right 45 % empty | CTA + note in the page head (in the fold at 390 and 1440), examples in a sticky right column at ≥ 52.5em, CTA repeated after the steps, sticky bar on mobile |
| PDP CTA below first screen / sticky only after scrolling past | loupe note removed (honesty label moved into the loupe `alt`); bar shows whenever no inline CTA is visible; CTA now in the first screen on EN and AR |
| p207 kitten: hand sliver, cut edge | can't be cropped clean (hand sits between the paws) → kept in shop + its page, excluded from home and related (`NOT_FEATURED`) |
| Panda (and white yarn) grey contour | `make_images.py`: matte eroded 1 px + light-yarn contour ≤ 3 px treated as ground; 3× edge crops checked on panda, duck, lamb, cow, daisy, bunny, cupcake, koala, teddy, puppy |
| Elephant cream pocket between legs | enclosed old-ground pockets found by smoothness (mean distance ≤ 4.5, ≥ 200 px) |
| Shop single-tile rows + plushies orphan | gift sets/seasonal/accessories → "Gifts & more" / «هدايا وأكثر» (tiles keep their real category label); 17 plushies → first one 2×2 at ≥ 75em, five full rows |
| Sushi box-in-box | scene photo cropped to its own photo, fills the tile; gift box is a real cut-out, kept |
| `.lang` heaviest in header | border → `--color-border`, size matched to the nav (`--text--1`, ×1.12 for the Arabic word); AR nav no longer bumped to `--text-0`; EN pages draw «العربية» with a 6 KB Baloo subset |
| Home 390 text-only fold | photo + loupe first (72 % width), h1 at `--text-4` below 52.5em; loupe bottom at y≈331 |
| "checkout coming" / "card payment coming" | removed EN+AR; shipping is quoted in the chat, payment arranged in the chat |
| Step 3 body about payment | "Once the price and colors are agreed, we crochet your piece and arrange delivery." (EN+AR) |
| Menu current page colour only | underline added |
| Sticky bar can cover focus | `html:has(body.has-sticky) { scroll-padding-block-end: 6rem }` |
| PDP alt repeats h1 | alt = catalog description (EN/AR) |
| Loupe soft (300 px) | 400 px crop at 1:1 pixels; panda/sushi/mouse/lily/gift box pinned to stitch areas |
| `.side` misaligned | `margin-block-start: 0` (aligns with the first question) |
| Nunito Fallback `local("Arial")` errors | `local()` list adds ArialMT, Roboto, Liberation Sans, Helvetica |
| Language switch under "Follow" | moved to the footer base row as "Language: العربية" |
| About thin | lead added + the "How ordering works" side panel; no invented bio, still no in-hand photo |
| "New pieces show up on Instagram first" | reverted to the live wording ("Follow the latest pieces and works in progress on Instagram") |
| ~200 px dead band under the hero at 1440 | hero bottom padding `--space-2xl` |
| Chips no "you are here" | IntersectionObserver marks the current section's chip (`aria-current`, ink fill) and scrolls it into view |
| AR feminine imperatives | all AR copy switched to the plural (اطلبوا، راسلونا، تصفّحوا…), incl. pronouns (لكم، طلبكم) |
| AR h1/nav reads heavier | Arabic strong weight 700 → 600 |
| FAQ invented reason for making time | now "We confirm the making time when you message us. Custom orders usually take a bit longer." |
| 404 brand moment | empty loupe ring above the bilingual block; "This page slipped a stitch" (EN) |

Not done: gift-occasion row and the interactive loupe (missed opportunities, not fixes); in-hand
photos (need Rana).
