# Loopaholic redesign plan (round 1)

Not served (excluded in `_config.yml`). Reference: `brand/design/` PRINCIPLES, TOKENS, CHECKLIST, RUBRIC;
brand kit `brand/products/loopaholic/`; critic round 0 (`rounds/round-0-live.md`, 4.6 BLOCK).

## Who it's for, and the one action per page
Visitors arrive on a 390 px phone from Instagram (Lebanon, Gulf, diaspora). Most are buying a gift:
a plush for a new baby or a birthday, a flower that keeps. They want to see the piece, trust that a
real person makes it, and know how to order without a cart or a public price.

| Page | Job | One primary action |
|---|---|---|
| Home | What it is, who it's for, how ordering works | Browse the pieces (→ Shop) |
| Shop | Find a piece | Open a piece |
| Product | Decide and ask | **Order on Instagram** (DM, `ig.me/m/loopaholic.crochet`) |
| Custom orders | Ask for a commission | Start a custom order (DM) |
| Shipping / About / FAQ | Answer the objection | none (text links to Shop / DM) |
| 404 | Get back | Shop link |

Same label for the same action everywhere: EN "Order on Instagram", AR «اطلبي على إنستغرام».
When `HAS_WHATSAPP` turns on, the primary becomes "Order on WhatsApp" and Instagram drops to an
outline button; nothing else changes.

## Colour (kit values; one accent)
| Name | Hex | Role | Contrast |
|---|---|---|---|
| Paper | `#FAF7FC` | page | |
| Lilac tile | `#F2ECF7` | the one photo ground, chips, sunken bands | ink 13.1:1, ink-2 5.0:1 |
| White | `#FFFFFF` | menu sheet, sticky bar | |
| Ink | `#2B2233` | text, footer ground | 14.3:1 on paper |
| Ink-2 | `#6D6177` | meta, captions | 5.5:1 on paper |
| Line | `#E4DBEB` | hairlines (decorative only) | |
| Loop purple | `#7B4FA6` | actions, links, focus, current page, the logo ring | white on it 6.0:1, as text 5.6:1 |
| Loop purple deep | `#5E3A82` | hover/pressed | white 8.7:1 |

Extension to the kit, written down: the kit's focus `#B388DD` is 2.6:1 on paper, so the focus ring
uses Loop purple (2 px + 2 px offset, ≥ 3:1 on every surface). Light-only site
(`color-scheme: light`): the photos are baked onto a light tile, so a dark theme would put light
squares on a dark page; a dark mode is deferred, not faked.

## Type
- Latin: **Nunito** (kit), self-hosted variable woff2, Latin subset, one file. Body 400, headings 700,
  wordmark 800 (SVG). Display tracked −0.02em ≥ 40 px.
- Arabic: **Baloo Bhaijaan 2** (Google Fonts, OFL), self-hosted variable woff2, Arabic subset, one
  file, loaded and preloaded on `/ar/` only. Rounded terminals that rhyme with Nunito; set 1.12×,
  body leading 1.8, headings 1.35, no letter-spacing, no italics.
- One fluid scale (TOKENS `--text--1 … --text-5`), 6 steps used: −1 meta, 0 body, 1 lead/card,
  2 product name/h3, 3 h2, 4 h1 (5 only for the home hero).

## Space
TOKENS scale `--space-3xs … --space-4xl` (4/8 base, fluid big steps). Sections 48–64 px mobile,
64–96 px desktop. Inside-group gap ≤ half the between-group gap. Radii (round personality, toys):
10 / 16 / 24 + pill; buttons and chips pill, photo tiles 16 (24 on the product hero). Two shadows.

## The signature: the loop loupe
The kit's mark is a single open ring, "one crochet loop". It becomes a **loupe**: a circle cut from
the full-resolution photo, framed by the ring in Loop purple, sitting on the corner of the product
tile so you can count the stitches (Baymard: texture shots sell handmade; round 0's "9.5 idea").
It is a crop of Rana's own photo at 1:1 pixels, labelled "Close-up of the stitches", never a new or
retouched image. Spent in exactly two places of one template family: the product gallery and the
home hero. Everything else is quiet: no ornaments, no dividers, no icons beyond the order glyph.

The photography system around it: every photo re-grounded from the delivered cream `#FAF3E9` onto the
one lilac tile `#F2ECF7` (flood fill from the borders + flat enclosed holes, 2 px fringe blend; the
piece is untouched), 1:1, `object-fit: contain`, no card chrome. The gift-box and sushi-slate photos
aren't cut-outs; their own photo sits on the same tile with the same margin, so the grid stays one
surface (Papier's "one repeated ground" principle).

## Layouts
```
HOME 390                         HOME 1440
[o Loopaholic   Shop  ع  Menu]   [o Loopaholic  Shop Custom Shipping About FAQ   العربية]
H1 Handmade crochet gifts,       | H1 (text-5)              |  [ lilac tile, elephant ] |
   made to order in Lebanon      | lead                     |        (loupe)  ◯         |
lead (2 lines)                   | [Browse the pieces] How ordering works            |
[Browse the pieces]  how→link    ----------------------------------------------------
[ tile + loupe ]                 Gift ideas: 4 photo tiles (a new baby / a birthday / flowers / just for fun)
Gift ideas  2x2 tiles            Pieces: 8 tiles, 4-up
Pieces  2-up x 8                 How ordering works: 3 steps in a row
How ordering works 1-2-3         Made by hand in Lebanon (prose) | Instagram follow link
Made by hand / Instagram         [ink footer]
[ink footer]

SHOP                             PRODUCT 390                      PRODUCT 1440
H1 Shop + one line               Shop / Plushies (crumb)          | tile 7/12 + loupe | H1          |
chips (scroll, sticky, 44px)     [ tile 1:1 ]  ◯ loupe            |                   | desc        |
h2 Plushies                      H1 name                          |                   | colours     |
grid 2 / 3 / 4-up, 1:1           desc / shown in: colours         |                   | price note  |
...                              Price on request (muted)         |                   | [Order on IG]|
"Can't find it?" custom link     [ Order on Instagram ] full      |                   | 1-2-3 steps |
                                 opens a DM note                  |                   | delivery/ret|
                                 How ordering works 1-2-3         related 4-up
                                 Delivery & returns summary
                                 related 2-up
                                 [sticky bar once CTA scrolls away]
```
Custom orders: H1 + lead, two example tiles, 1-2-3 steps, one DM CTA. Shipping/About/FAQ: one prose
column ≤ 65ch (AR 60ch), h2 per region / question. 404: header + bilingual block + 3 links + DM.

Nav at 390: logo, "Shop", language switch, "Menu" (a `<details>` sheet with all pages, Esc closes).
At ≥ 52.5em the full nav is inline. Language switch and menu ≥ 44 px.

## Honesty switches
- `SHOW_UNCONFIRMED_DETAILS = False`: hides size and making time (cards, product page, JSON-LD) and
  rewrites the FAQ making-time answer and the shipping note to "we confirm the making time when you
  message us". Data stays in catalog.json.
- `check_claims()` fails the build on safe/آمن, certified, non-toxic, organic, hypoallergenic,
  wood/wooden/خشب, CE, 100%, or a $/USD price, in catalog, copy and rendered HTML (owner R2b).
- Teether rings are material-neutral ("Duck Teether Ring", colours from the photo); the shark stand
  is "a display stand". No reply-time, size, stat, review or occasion claim is added.

## Generic tells avoided (checked against PRINCIPLES 15)
- Not cream + serif + terracotta: cool kit paper, rounded sans, purple only on actions.
- No identical-card kit: tiles have no border/shadow/white body; name sits under the photo.
- No ALL-CAPS eyebrows, no "A · B · C" meta strings, no `→` on buttons, no emoji icons.
- 1-2-3 numbering only on the real 3-step ordering sequence.
- No scroll fade-ups; the only motion is button press, menu open and the sticky bar slide.
- One expressive thing (the loupe); dropped from the plan before building: a stitch-pattern divider between home
  sections (one accessory too many).
