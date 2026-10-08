# Stitch Book: before → after (8–9 Oct 2026)

Not served. Spec: `../GAME.md`. Concepts: `../game-concepts.md`. Live before: `../after/` (the 8 Oct redesign, scored 8.5 SHIP).

| Round | Critic verdict | What changed |
|---|---|---|
| Concepts | fun-council: B (Stitch Book) Ship, A Sharpen, C Kill. design-critic: B + A's meeting moment ≈ 8.6–8.8 possible | Picked the hybrid. No throwing or Pokémon look-alikes, no daily limits. |
| r1 | **7.0 BLOCK** (3 auto-fails) | Met book slots never showed photos (`[hidden]` beaten by `img{display:block}`). The 3D disclaimer slid under the sticky gallery at 1440. The AR share stamp collided with the ring. Header label mismatch. Grey 3D sketches. |
| r2 | **8.0 REVISE** | Stitch-clue encounter (the critic's 9.5 idea): the LCP is a real-craft image. Kept 11 colour-matched sketches. Remaining: axe label-in-name on EN, layout shift after Meet, wrong-state loupe hint. |
| r3 | **7.8 BLOCK as built** (8.5 projected) | All r2 items fixed, interaction CLS 0. The new footer column overflowed at 320 px. The zoom start was off-centre. |
| r4 | **8.5 SHIP**: home 8.6, book 8.6, product 8.5, guide 8.6, share card 8.6 (390 and 1440, EN and AR) | Footer reflow, pixel-exact zoom-out, US spelling, named unmet slots. "Beats the live site: yes, clearly." |
| after r4 | n/a | Sticky bar became `<aside aria-label>` (r4 fix 1). Share links land a friend on `/?meet=<id>` (r4's 9.5 idea). |

Files: `r1/ r2/ r3/` (screens per round: home-enc, home-met, book, book-closing, book-full, pdp, pdp-card, pdp-turn, pdp-turned, share-card, guide), `playtest-en-390.mp4` (15 s headless-Chromium play-test).
Measured locally on r4: axe 0 WCAG violations (2.0–2.2 A/AA) on 14 pages, EN and AR. No overflow at 320/390/1440. Lighthouse mobile 98–99 (indicative: the XPS was loaded).
