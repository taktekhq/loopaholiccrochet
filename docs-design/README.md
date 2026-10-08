# Loopaholic redesign, 8 Oct 2026: before → after

Not served (excluded in `_config.yml`). Reviewed against Taktek's design reference (`taktekhq/brand/design/`: PRINCIPLES, TOKENS, CHECKLIST, RUBRIC) by an independent design-critic agent, four rounds.

| | Before (live until 8 Oct 19:33) | After (live since 8 Oct 19:35, commit da114d3) |
|---|---|---|
| Rubric, site (lowest page) | **4.6 BLOCK** (4 auto-fails) | **8.5 SHIP**; pages 8.5–8.7, no dimension < 8 |
| Look | Generic cream + Georgia serif + terracotta (the stock "AI" default, not Loopaholic's kit) | Loopaholic kit: purple ring mark, Nunito, lilac photo ground; Baloo Bhaijaan 2 for Arabic |
| Signature | none (emoji icons) | the "loop loupe": the ring frames a close-up of Rana's stitches; live magnifier on product pages (mouse, touch, keyboard) |
| Order path | the same Instagram link 3 ways, to the profile | one "Order on Instagram" button that opens a DM (ig.me), "how ordering works" beside it, sticky bar on phones |
| Arabic | no Arabic font, Latin sizes, feminine-only address | designed Arabic: own face, 1.125× size, 1.8 leading, gender-neutral plural |
| Lighthouse mobile (live) | perf 73–93, a11y 89–94 | perf 99–100, a11y/BP/SEO 100, LCP 1.3–1.5 s, CLS 0 |
| axe (WCAG 2.2 AA) | contrast fail on the main button, landmark issues | 0 violations |
| Honesty | unconfirmed sizes/making times, "wooden"/"natural wood" | hidden behind `SHOW_UNCONFIRMED_DETAILS` until Rana confirms; build fails on claim words |

Kept: every URL (86 + new 404), titles/descriptions (except deliberate copy fixes), canonical, hreflang, JSON-LD (+ BreadcrumbList), sitemap, IndexNow key, GA4 events (`instagram_click`, `whatsapp_click`, `buy_click`).

Files: `before/` and `after/` (390 and 1440, EN and AR), `PLAN.md` (the design plan and its rounds), `rounds/` (each critic and designer round).
