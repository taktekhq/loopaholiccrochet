# Loopaholic game: 3 concepts (draft for fun-council + design-critic)

Brief (Nizar, 8 Oct): loopaholiccrochet.com becomes a playful, mobile-first, Pokémon-like experience. People meet Rana's crochet toys as creatures, bond with them, collect them, then buy the real ones. No Pokémon names, balls, art, sounds or trademarks. Character fiction only: never claims about materials, safety, size or price (no public prices until Rana signs off). Orders today go to an Instagram DM (no WhatsApp number yet). Arabic + English, RTL. 36 real pieces (plushies, dolls, flowers, baby teether rings, fun food). Each has a real photo on a lilac tile and a TripoSR 3D model from that photo (fronts look good, backs are guessed: show ±60° of turn, not a full spin). SEO pages per product must stay; the game is a JS layer on top. Lighthouse mobile ≥ 90. Current site: calm, lilac, Nunito, purple ring ("loop") logo, the "loop loupe" stitch magnifier as signature.

Constraints that shape every concept: 36 creatures (a finite, small set, so the collection can actually be finished), no accounts (localStorage), one-handed 390×844, no sound by default.

---

## Concept A: "The Yarn Basket" (daily encounter + catch)

- Home screen = a wicker basket at the bottom of the screen, a creature peeking out of a yarn tangle at the top. Once a day (and once on first visit), a new **stray** appears: its silhouette wobbles behind the yarn.
- **Catch**: you flick a yarn ball upward (swipe) or tap-and-hold to "unravel" a loop around it. The ball squashes on release, arcs, wraps the creature in a loop (the brand ring!), wobbles 1–3 times (tension), then a sparkle burst + `navigator.vibrate([12,40,18])`. A miss rolls the ball back: try again, no penalty.
- After the catch: the **Hello card** flips in: name, a type (Cozy / Sunny / Sea / Garden / Sweet / Tiny), a one-line personality, "favourite thing", then the real 3D model you can turn with your thumb.
- Collection = **"The Basket"** grid of 36 slots; unmet ones are lilac silhouettes. Completion counter "12 of 36 friends".
- Bring-me-home: on every creature card: "Bring Pip home" → product page / Instagram DM prefilled with the piece's name.
- Loop: 1 free daily stray + 3 "yarn balls" a day to catch extra wanderers in the "Garden" (scroll the shop as an overworld).
- Risk: daily limiter frustrates a one-time visitor from Instagram; we must let a first visit meet 3.

## Concept B: "Loopadex / The Stitch Book" (collection-first, no catching skill)

- The shop IS the book: the 36 pieces shown as a sticker album. Each tile is a silhouette until you "meet" it by tapping and holding (the loop draws around it, stitch by stitch, 600 ms) → it pops to colour with a squash + sparkle.
- Each creature page = a trading card: big photo with tilt-parallax (gyro or drag), name, type stamp, personality, a tiny story (3 lines), favourite thing, "stitched by Rana in Lebanon".
- Stickers for sets: "the whole Sea gang" (octopus, shark, turtle), "Teether trio", "Flower shop". Finishing a set unlocks a printable/shareable set poster.
- Share: every card exports a 1080×1350 image ("I met Mellow the elephant 🐘 at loopaholiccrochet.com").
- Pro: zero skill, fastest to the product; con: thin "game", nothing to come back for.

## Concept C: "Hatch a Loop" (one companion you raise)

- First visit: you pick one creature from 3 random ones (starter choice). It lives on your home screen; you can poke it (squash), feed it its favourite thing (drag), it reacts. Each day it "wants to meet a friend" → it brings a new creature (the encounter), which you add to your Book.
- Your companion levels up with friendships (stitches: 5, 10, 20…). Levels unlock card frames and its "story chapters".
- Bring-me-home: "Adopt the real Mellow", and a gentle nudge at milestones ("You've been friends for 7 days").
- Pro: strongest emotional bond (tamagotchi); con: biggest build, needs return visits, risk of feeling manipulative (we shouldn't guilt).

---

Questions for reviewers: which concept (or hybrid) creates the strongest emotional bond AND the shortest honest path to "message Rana to order"? What's the one signature moment? What should we kill?
