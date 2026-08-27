# The panels' built-in effects, as actually seen (2026-08-27)

The four HYULIGHTS WX-60WPS-48PARTITION carry 42 built-in programmes the
definition only calls "Effect 1..42". Nobody had watched them until the owner
ran them one by one at home (over the FT232R interface) and sent back video
frames, in chronological order. This file is the catalogue those frames give
us; it is the input for pruning `Ciclo Paneles` down to the effects worth
cycling all night.

**Status: frame-to-effect-number mapping pending owner confirmation.** 18
frames arrived for 42 effects, so either several effects share a video or only
part of the list is covered; a single still also cannot show motion, so each
description below is one instant of an animation.

## Named by the owner

| Effect | Name (owner) |
| --- | --- |
| 1 | Rueda Multi Color (Jump) - full-panel colour wheel, hard cuts |
| 2 | Multi color fade - full-panel colour fade |
| 3 | Multi color fade a negro entre colores - fade through black between colours |

Note for `Humo Vertical`: the hand-built show's smoke-light chaser drove
values 2 and 14 on the effect channel - which land in Effect 1 and Effect 3's
ranges. Per this catalogue those are *multicolour* cycles, not white, so the
"todo blanco para el humo vertical" memory does not match the values the old
file carries. Decision needed (see TODO): build `Humo Vertical` on guaranteed
white (the manual-mode white scene) rather than copying the old values blind.

## Frames, in the order received (chronological by capture date)

| # | What the still shows |
| --- | --- |
| 1 | Green base, white 2x3 pixel blocks at top and bottom corners (block chase over green) |
| 2 | Split panel: top red with white blocks stepping down, bottom green with white blocks |
| 3 | Blue top / green bottom, white block pairs across the top rows |
| 4 | Multicolour regions (red, blue, green) with white block groups - block chase over colour zones |
| 5 | Red/cyan/blue plaid mosaic with white clusters |
| 6 | Full red with a single white 4x6 block in the centre |
| 7 | Full blue, white block clusters along the top rows |
| 8 | Full blue, white block pairs on a descending diagonal |
| 9 | Full green with a single white 4x6 block in the centre |
| 10 | Full red, many white block clusters scattered |
| 11 | Full red, left half swept white (vertical wipe) |
| 12 | Concentric rings: green frame, red ring, blue/cyan, white centre |
| 13 | Full green, all pixels lit |
| 14 | Smooth gradient blue -> green -> yellow (rainbow wash) |
| 15 | Thirds: white-over-green top, white/yellow columns bottom-left, red bottom-right |
| 16 | Top half white over green, bottom half red (two-band split with white) |
| 17 | Concentric: blue frame, green, red ring, cyan/white centre |
| 18 | Green/red mosaic with white and warm-white clusters |

## Pending from the owner

1. Which effect number each frame belongs to (or which numbers the 18 frames
   cover, if several frames share one video).
2. The keep-list: which effect numbers stay in `Ciclo Paneles`.
3. Whether `Humo Vertical` uses one of these or plain manual-mode white.
