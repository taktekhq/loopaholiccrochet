# The Stitch Book: Loopaholic's game layer

Not served (`docs-design/` is excluded). Brief: Nizar, 8 Oct 22:10: "turn the website into something of a mobile experience… fun to play with… an emotional connection to the toys… then they can buy the actual toys. Think of this like a Pokémon game."
Concepts: `game-concepts.md` (A Yarn Basket, B Stitch Book, C Hatch a Loop). Reviewed by the fun-council and the design-critic on 8 Oct; both picked **B as the spine, A's meeting moment, C cut**.

## The idea in one line
Every one of Rana's 36 pieces is a character you meet. Meeting closes the kit's open loop around it, stitch by stitch, and the closed loop is the same ring that frames her real stitches on the product page. The game ends on her craft.

## Rules we keep (and why)
- **The shop is never behind the game.** `/shop/` and every `/shop/<slug>/` stay full static pages: photo, loupe, h1, Product JSON-LD, hreflang, canonical, sitemap and the one "Order on Instagram" button. The game is `assets/js/game.js` on top. Without JS: the book is a plain list of characters with photos and links.
- **Fiction is labelled as fiction** on every card ("The name and story are make-believe; the piece in the photo is real."). `creatures.json` holds names, types, a personality line, a favourite thing and a 2-sentence story, EN + AR (Arabic written natively, not transliterated). The build's claims guard walks it: no materials, safety, size, price or making facts. Teether rings get personality only.
- **No Pokémon anything:** no throwing, no ball, no wobble count, no "catch" wording on screen, no trademarks. The analytics event is called `catch`; the visitor sees "Meet them".
- **No pressure:** no daily limits, no random packs, no levels, no "they miss you". A met character stays in your book whether you buy or not. "Bring me home" is plain: the order block's heading becomes "Take Quincy home?" over the same button and copy.
- **Motion answers the visitor (P9):** the one orchestrated moment is the ring stitching shut (600 ms, 14 steps), then a squash, 8 sparks and `navigator.vibrate([12,40,18])`. Nothing moves on its own. Under `prefers-reduced-motion` the ring just appears closed and the colour fades in, with no squash, sparks, sweep or vibration.
- **Every gesture has a tap or key:** meeting is a `<button>` (or a link tap in the book), turning has ‹ › buttons and arrow keys (`role="slider"`), and Escape returns to the photo.

## Screens
| Screen | Where | What |
|---|---|---|
| Encounter | home hero (JS) | A random character you haven't met hides as a lilac shadow inside the open ring. "Meet them" closes the ring, the photo colours in, and you get "You met Sami!", a type stamp, the personality line, "1 of 36 in your Stitch Book", **See Sami's card** (to the product page `#creature`) and "Meet someone else". "Browse the pieces" steps down to the outline button while the encounter is on screen, so there's one solid button. |
| Stitch Book | `/book/`, `/ar/book/` | Progress line and bar, type chips with counts (Cozy, Sea, Garden, Nibbles, Darling, Storybook), sections of round slots. Unmet slots show a shadow and an open ring, and a tap meets them in place. Met slots link to the piece. Finishing a set shows "Complete". "Start the book over" asks to confirm first. |
| Creature card | every product page, after the order block | Name in a closed-ring badge, type stamp, personality line, favourite thing, story, **Turn X around** (11 models), **Share X's card**, and the fiction note. Scrolling it into view meets the character if you haven't already, with a toast. "This one's called X." sits under the h1 and links to the card. |
| Turn | product gallery (tap) | An 18-frame strip (±50°) rendered from the TripoSR model, scrubbed by drag, ‹ › or arrow keys, labelled "A 3D sketch made from the photo: colours and stitches differ from the real piece." It loads only on tap (about 55 KB) and has no WebGL at runtime. |
| Share card | canvas, 1080×1920 | A "friend card": the photo in the purple loop, the name, the line, Type, Favourite thing, "Born: Lebanon, stitch by stitch", "Status: Made when someone orders", a **"Hint."** stamp («حدا يجبلي ياه») and the page URL. It uses Web Share with the file where that's available, and a download otherwise. |
| Header | every page | Ring + "4/36" (the word "Stitch Book" shows from 840 px), a bump when it changes. The footer adds Stitch Book and Guides links. |

Name: **Stitch Book / دفتر الغُرَز**. The fun-council's first pick was "The Basket", but on a shop "basket" reads as the cart. "Rana's Basket" would put the maker's name on the site, which nobody has confirmed (see Asks).

## 3D models used
Kept (front ±50° holds up, colours pulled halfway back to the photo by tools/turntable/colour_match.py; critic round 1 dropped the sketches that lose their faces): p003 p013 p017 p063 p070 p072 p076 p077 p092 p251 p369.
Photo only: the other 25 (smeared faces, flat, wrong colour or broken backs).
Renderer: `tools/turntable/` (three.js in headless Chromium, unlit vertex colours with soft hemisphere light, 18 frames at 360 px, WebP q72).

## Measurement (GA4 G-EQ20EYFSY3)
`encounter` (creature), `catch` (creature, source home/book/product), `view_book` (met), `product_view` (product), `view_creature` (creature), `turn_3d`, `share_card` (creature, method share/download), `copy_name`, `bring_home_click` (creature, met), plus the existing `instagram_click`.

## Ideas parked
A starter companion on the book cover. Seasonal sets (Ramadan, Christmas). "Status: born" on a card once someone's order arrives (needs Rana). Sound (off by design).
