# The panels' built-in effects, as actually seen (2026-08-27)

The four HYULIGHTS WX-60WPS-48PARTITION carry 42 built-in programmes the
definition only calls "Effect 1..42". Nobody had watched them until the owner
ran them one by one at home (over the FT232R interface) and sent back video
frames, in chronological order. This file is the catalogue those frames give
us; it is the input for pruning `Ciclo Paneles` down to the effects worth
cycling all night.

**Mapping (owner, 2026-08-28):** Effects 1-3 are described by text - they are
full-panel colour cycles, which a still cannot show - and the 18 video frames
that follow are the next effects in chronological order, so **frame k is
Effect k+3**: the frames cover Effects 4 through 21. Effects 22-42 have no
footage yet. A single still is one instant of an animation, so every
description below is the pattern, not the motion.

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

## Effects 4-21, one video frame each (chronological)

| Effect | What the still shows |
| --- | --- |
| 4 | Green base, white 2x3 pixel blocks at top and bottom corners (block chase over green) |
| 5 | Split panel: top red with white blocks stepping down, bottom green with white blocks |
| 6 | Blue top / green bottom, white block pairs across the top rows |
| 7 | Multicolour regions (red, blue, green) with white block groups - block chase over colour zones |
| 8 | Red/cyan/blue plaid mosaic with white clusters |
| 9 | Full red with a single white 4x6 block in the centre |
| 10 | Full blue, white block clusters along the top rows |
| 11 | Full blue, white block pairs on a descending diagonal |
| 12 | Full green with a single white 4x6 block in the centre |
| 13 | Full red, many white block clusters scattered |
| 14 | Full red, left half swept white (vertical wipe) |
| 15 | Concentric rings: green frame, red ring, blue/cyan, white centre |
| 16 | Full green, all pixels lit |
| 17 | Smooth gradient blue -> green -> yellow (rainbow wash) |
| 18 | Thirds: white-over-green top, white/yellow columns bottom-left, red bottom-right |
| 19 | Top half white over green, bottom half red (two-band split with white) |
| 20 | Concentric: blue frame, green, red ring, cyan/white centre |
| 21 | Green/red mosaic with white and warm-white clusters |

With this mapping the old vertical-smoke pair reads: Effect 1 (Rueda Multi
Color Jump) and Effect 3 (fade through black) - full-panel colour cycles,
still not white. Effect 14 is the closest thing to a white sweep seen so far.

## The keep-list (owner, 2026-08-28)

"Estaban todos menos uno que va como con un contador de números" - the
hand-built programming cycled every effect except the number counter. The
old chaser confirms it structurally: its 41 steps cover Effects 1-42 minus
exactly one, **Effect 40**. `Ciclo Paneles` now cycles 41 of the 42
(`EXCLUDED_FROM_CYCLE` in `generate/builtin_effects.py`); Effect 40's scene
stays on the library page for whoever wants to see a counter once.

## Still pending from the owner

1. Footage of Effects 22-42, when convenient - the catalogue above stops at 21.
2. Whether `Humo Vertical` uses Effects 1/3 (the old values, multicolour) or
   plain manual-mode white.
