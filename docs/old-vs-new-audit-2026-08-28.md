# QLC+ old-versus-new semantic audit

**Audit date:** 2026-08-28  
**Old authority:** `QLC+ Setups/DeluxeEventos2.qxw`  
**Conversion cross-checks:** `DeluxeEventos2_qlc4143.qxw`, `DeluxeEventos2_qlcv5.qxw`  
**New workspaces:** `Vibra.qxw`, `Vibra-beats.qxw`, `Vibra-split.qxw`  
**Current patch used for DMX comparison:** `Vibra-split.qxw`

## Verdict

The generated show is structurally safer and much more complete as an operator console, but it is **not a behavior-preserving replacement** for the hand-built show. The strongest evidence of likely accidental loss is:

1. the advertised 18-colour source palette is present in Python but only 11 of those colours reach any generated Scene or RGBMatrix;
2. keys `9` and `0` changed meaning on every colour bank despite the operating guide's muscle-memory claim;
3. the old live automatic panel-speed sequence disappeared;
4. the two old whole-rig relative rainbow EFX disappeared;
5. two non-split workspaces retain a different USB-DMX interface binding from the current split file and documented generic binding.

Several advertised restorations are real but not byte-for-byte restorations. `Humo Vertical` and the outer `Dimmer Secuencia` schedule match exactly. Per-beam prism and MultiColor selections match. Flash and gobo values were deliberately moved to capability-safe values. The old prism animation, dimmer trajectories, and panel-speed automation were not restored by those changes.

## Impact-ranked findings

| Rank | Impact | Finding | Judgement |
| --- | --- | --- | --- |
| 1 | High, conditional blackout | `Vibra.qxw` and `Vibra-beats.qxw` retain USB-DMX UID `A50285BI`; current `Vibra-split.qxw` names `AB0PEY7F` with an empty UID and the rig guide requires generic binding | **UNCLEAR** |
| 2 | High, all-night visual vocabulary | 7 of the documented 18 palette colours never reach a generated function | **LIKELY FORGOTTEN** |
| 3 | High, live muscle memory | Colour-bank keys `9`/`0` changed from two-colour looks to orange/pink | **LIKELY FORGOTTEN** |
| 4 | High, beam aim | `Cabezas Reposo`'s 7R beam position `(pan=0, tilt=130)` became generic `(127,127)` | **UNCLEAR** |
| 5 | Medium-high, visible effect loss | Old relative whole-rig `Arcoiris Simultáneo` and `Arcoiris Pasos` EFX have no new equivalent | **LIKELY FORGOTTEN** |
| 6 | Medium, panel animation | Reachable `Strobo LED - Speed Auto` sequence and its four-value speed modulation are absent | **LIKELY FORGOTTEN** |
| 7 | Medium, beam texture | Old eight-step per-beam prism choreography became two steps: all out / all in | **UNCLEAR** |
| 8 | Medium, bar variety | Old 121-step Random bar-matrix cycle became a 28-step Loop; nine algorithm families disappeared from the cycle | **UNCLEAR** |
| 9 | Medium, fixed looks | Four deterministic four-colour head/beam scenes have no equivalent; the two new multicolour scenes use different distributions | **UNCLEAR** |
| 10 | Medium, intensity choreography | The restored dimmer schedule is exact, but its family-specific Serial Line EFX became two whole-rig Parallel Circle EFX | **UNCLEAR** |
| 11 | Medium-low, movement vocabulary | The seven main shapes survive for washes, but simultaneous variants, 5 s crossfades, and two shapes on beams do not | **UNCLEAR** |

## 1. Patch and fixture definitions

**Match summary:** the old physical patch is contiguous on Universe 1, DMX 1–300, with no fixture removed in `Vibra-split`; the current patch adds two real panels at 301–316 and represents the same CLB2.4 addresses with split per-head definitions.

| Old fixtures | Old IDs and DMX | Old mode | `Vibra-split` state |
| --- | --- | --- | --- |
| 4 × Pro-Lights CromoWash100 | 0/1 at 1–24; 13/14 at 136–159 | Advanced, 12 ch | Exact |
| 2 × Stairville LED Bar 240/8 RGB | 2/3 at 25–72 | 24 ch | Exact |
| 2 × Stairville CLB2.4 | 4/5 at 73–100 | 14 Channel | Replaced at the same DMX addresses by IDs 29–36: `Master + PAR` 4 ch, `PAR` 3 ch, `PAR` 3 ch, `PAR + Strobe` 4 ch per bar |
| 7 × Vortex PC-64 LED S | 6–12 at 101–135 | Default, 5 ch | Exact |
| 2 × Chauvet MiN Wash | 15/16 at 160–185 | 13 Channel | Exact |
| Generic Smoke | 17 at 186 | Amount, 1 ch | Exact |
| 2 × LED Beam Mini | 18/19 at 187–218 | 16 Channels | Exact |
| 4 × Generic BEAM 230W 7R | 20–23 at 219–282 | 16 channel | Exact |
| 2 × HYULIGHTS WX-60WPS | 24/25 at 283–298 | A MODE, 8 ch | Exact, plus two more panels IDs 27/28 at 301–316 |
| Generic Smoke | 26 at 299–300 | Normal, 2 ch | Exact |

### Patch differences

- **Category:** Patch and fixtures. **Old evidence:** 27 fixtures, DMX 1–300. **New state:** 35 logical fixtures, DMX 1–316: two added HYULIGHTS panels and eight logical CLB head fixtures replacing two compound fixtures. **Judgement: INTENTIONAL.** The split keeps identical cabling and addresses and exists to expose all eight PAR heads to QLC+ 3D (`docs/rig.md:233-264`); acceptance of the split as the permanent patch is still open (`TODO.md:214-220`). The two added panels are also documented as a new four-panel group (`TODO.md:57-65`).
- **Category:** Fixture definitions. **Old evidence:** every custom old reference resolves to a repo `.qxf` with the expected mode length: CromoWash Advanced 12, CLB2.4 14, Vortex 5, MiN Wash 13, Mini LED 16, BEAM 16, HYULIGHTS 8. **New state:** all remain available; the split adds `Stairville-CLB2.4-PAR-Strobe.qxf` modes 4/3/4 channels. The LED Bar and both Generic Smoke definitions are system-library dependencies rather than vendored files. **Judgement: INTENTIONAL.** Verification status is candidly recorded in `docs/rig.md:379-395`; Vortex, Mini LED, and HYULIGHTS remain only partly or not hardware-verified.

No old fixture, occupied DMX address, or old custom mode is silently missing from the current split patch.

## 2. Scenes and DMX values

**Match summary:** 190 old Scenes were compared with 296 new Scenes by Universe/address/value maps. Eighteen have an exact whole-map equivalent and another sixteen are exact subsets of broader ownership scenes. Primary solids, 30 two-colour permutations, smoke ON/OFF, all 42 panel programs, all 18 gobo positions, manual prism subsets, MultiColor subsets, and `Escenario` have functional counterparts. Material exceptions follow.

### 2.1 Seven documented colours never reach the show

- **Category:** Scenes / colour coverage.
- **Old evidence:** old Scenes and RGBMatrices collectively emit 26 RGB triples. All 18 entries in `qlctool.palette.PALETTE` occur in the old show. Concrete examples include Scene 36 `Amarillo LEDs` using `(255,20,0)` on one triple, Scene 28 `Cyan LEDs` using `(0,200,255)` and `(0,35,255)`, Scene 127 `Rosa/Cyan LEDs` using `(0,127,255)`, and old matrix families `VerdeMar`, `Violeta`, and `Rosa` using `(0,255,128)`, `(85,0,255)`, and `(255,0,176)`.
- **New state:** every new workspace emits only 13 RGB triples and only 11 of the canonical 18. Missing from all generated functions are `Rojo Fuego (255,20,0)`, `Verde Menta (0,255,128)`, `Celeste (0,200,255)`, `Azul Cielo (0,127,255)`, `Azul Profundo (0,35,255)`, `Morado (85,0,255)`, and `Fucsia (255,0,176)`. They exist only as unused Python constants. An unrelated new warm white `(255,214,170)` was added.
- **Judgement: LIKELY FORGOTTEN.** This contradicts the generator's own claim that it mined every old triple (`tools/qlctool/qlctool/palette.py:1-7`) and the operating guide's promise of an 18-colour palette (`docs/show-operation.md:127-132`).

### 2.2 Four fixed four-colour head looks are gone

- **Category:** Scenes / multi-fixture looks.
- **Old evidence:** Scenes 85–88 rotate four deterministic distributions over heads and beams. For example Scene 85 `4 Colores (Azul - Rojo - Verde - Blanco)` sends CromoWash IDs 0/1/13/14 respectively blue/red/green/white and sends BEAM colour-wheel values 40/9/32/0; Scenes 86–88 rotate that assignment.
- **New state:** no scene reproduces any of the four maps. Scenes 455/456 `Rig Multicolor 1/2` are different wild distributions over the whole rig; the ordinary mix scenes alternate only two colours.
- **Judgement: UNCLEAR.** The two wild steps are explicitly new (`docs/show-operation.md:145-149`), but no document says the four deterministic looks were intentionally retired.

### 2.3 Centre/rest position changed materially

- **Category:** Scenes / pan and tilt.
- **Old evidence:** Scene 7 `Cabezas Reposo` parks CromoWash and MiN heads at coarse `(128,128)` with fine zero, Mini head 19 at `(127,127)`, leaves Mini head 18 unwritten, and parks every BEAM 20–23 at `(pan=0, tilt=130)`.
- **New state:** Scene 382 `Cabezas Centro` writes every mover, but normalises every coarse pan/tilt to `(127,127)` and fine channels to zero. The four 7R pan values therefore change by 127 and tilt by 3.
- **Judgement: UNCLEAR.** The new scene fixes the unwritten Mini head, but `TODO.md:52-54` still requires `Centro` to be checked on the rig. A 7R beam at pan 127 is not semantically equivalent to pan 0.

By contrast, Scene 376 `Escenario` is restored exactly by Scene 383: CromoWash 0 `(161,49)`, CromoWash 1 `(176,43)`, and BEAMs 20–23 `(156,196)`, `(159,204)`, `(159,192)`, `(162,189)`, with only zero-valued fine channels added.

### 2.4 Flash restoration is functional, not literal

| Fixture family | Old Scene 43 / Scene 44 strobe value | New Scene 2 / Scene 3 value |
| --- | --- | --- |
| CromoWash | 240 / 70 | 218 / 120 |
| Vortex | 250 / 220 | 217 / 115 |
| CLB2.4 | 255 / 210 | 217 / 115 |
| MiN Wash | 220 / 175 | 223 / 182 |
| Mini LED | 255 / 200 | 217 / 115 |
| BEAM 7R | 190 / 120 | 212 / 136 |
| HYULIGHTS panels | 255 / 140 | 217 / 115, now on all four panels |

- **Category:** Scenes / strobe.
- **Old evidence:** Scenes 43/44 and Scene 276 `Flash 100% Colores` drive the values above.
- **New state:** Scenes 2/3/4 drive values derived from labelled capability ranges or the generator's bare-strobe rule, while also establishing white/intensity ownership. `Flash Color` deliberately leaves colour untouched.
- **Judgement: INTENTIONAL.** `TODO.md:41-56` records the old values and says restoration means restoring strobe behavior; `docs/show-operation.md:327-347` explains the range-safe values and the non-strobing audio hit. Hardware verification is still open, so “restored” is not yet an on-rig result.

### 2.5 Gobo, prism, and MultiColor restoration check

- **Gobos — INTENTIONAL:** old Scenes 287–304 write gobo channel values `0,9,14,21,28,35,42,49,56,63,70,77,84,91,98,105,112,119`. New Scenes 387–404 use range midpoints `3,10,17,24,31,38,45,52,59,66,73,80,87,94,101,108,115,123` and clear Pattern Jitter. Every pair lands in the same `.qxf` capability; the change is safer and agrees with the corrected presets (`docs/rig.md:454-464`).
- **Per-beam prism picks — INTENTIONAL, functionally matched:** old Scenes 305–312 use 255 for inserted and 0 for out; new Scenes 429–434 use 191/63. The exact selection masks `1`, `2`, `3`, `4`, `1+3`, `2+4` match. Both pairs lie in the `.qxf` ranges out `0–127`, in `128–255`. Global Scenes 426/427 add all-out/all-in and rotation ownership. This verifies the subset restoration claimed in `TODO.md:52-55`, but not the old animation sequence discussed below.
- **MultiColor — exact:** old Scenes 313–320 and new Scenes 435–442 have the same eight 255/0 masks on BEAM fixture channel 9: all, off, each single beam, 1+3, and 2+4.
- **Humo Vertical — schedule and selector exact:** old Chaser 367 (`Humo Auto`) and new Chaser 219 (`Humo Vertical`) are both Forward/Loop with Effect 1 for 60,000 ms and Effect 3 for 600,000 ms. Old selector values 2/14 are preserved. New scenes change mode 130 to 128, add master 255, strobe 0, speed 200, and expand from two to four panels. That is a capability-safe expansion, consistent with `docs/panel-effects.md:68-74`.

## 3. Chasers and sequences

**Match summary:** all 20 old Chasers have a recognisable new family counterpart; both generations use Forward direction throughout. Colour cycles remain Random, but several old choreographies were consolidated. The material order/timing losses are below.

### 3.1 Prism animation lost its per-beam choreography

- **Category:** Chasers / prism.
- **Old evidence:** Chaser 373 `Prisma Animacion`, Forward/Loop, common 63,000 ms, eight ordered steps: beam 4; beams 2+4; beam 1; beam 2; all; beam 3; beams 1+3; all off.
- **New state:** Chaser 428, Forward/Loop, contains only Scene 426 all out and Scene 427 all inserted, 8,000 ms each in `Vibra`/`Vibra-split` and 32,000 ms each in `Vibra-beats`.
- **Judgement: UNCLEAR.** The new peak design explicitly wants a spinning inserted prism and a neutral out owner (`docs/show-operation.md:169-175`), but it never states that the old per-beam animation was intentionally discarded. Restored manual subset buttons do not restore the chaser.

### 3.2 Bar matrix cycle is much smaller and no longer Random

- **Category:** Chasers / RGBMatrix.
- **Old evidence:** Chaser 135 `Animaciones Barras LED`, Forward/Random, common duration 10,000 ms, has 121 steps (holds 5,000 or 10,000 ms). Its algorithms cover Alternate, Even/Odd, Fill, Fill From Center, Fill Unfill, Gradient, One By One, Opposite, Random Column, Stripes From Center, Strobe, Waves, and solid scenes.
- **New state:** Chaser 254 `Ciclo Matrices BarrasLed`, Forward/**Loop**, has 28 steps. It rotates six colours through Fill, Even/Odd, Waves, and Solid, plus one each of Sine Wave, Lines, Marquee, and Plasma. The new bar library has 34 matrices, versus 121 old matrices used by the old chaser; its six Strobe matrices are not in the cycle.
- **Judgement: UNCLEAR.** The new curated scripts are documented as unverified (`TODO.md:208-213`), but removal of the old algorithm families is not. `RunOrder="Loop"` also conflicts with the broad rule that everything cycling is Random (`docs/show-operation.md:106-107`), though the independent matrix cycle was intentionally removed from AUTO (`TODO.md:67-74`).

### 3.3 Dimmer sequence schedule matches; trajectories do not

- **Category:** Chasers / intensity.
- **Old evidence:** Chaser 102 `Dimmer Secuencia` is Forward/Loop with six per-step holds: full 20 s, Collection 107 `Dimmer Chase 1` 10 s, full 20 s, Collection 113 `Dimmer PingPong` 10 s, full 20 s, Collection 109 `Dimmer Chase 2` 10 s. Collections 107/109 run separate fixture-family EFX, chiefly Serial `Line` paths with widths/heights and durations specific to Cromo, MiN, PC, panels, and beams.
- **New state:** Chaser 494 preserves the exact six-step order and 20/10-second holds. Its moving steps are EFX 446/447: whole-rig `Circle`, width/height 100/100, Parallel propagation, 6,000 ms, with 23 fixtures distributed around the path; reverse uses Backward direction. Chaser 450 provides a two-step 400 ms odd/even ping-pong.
- **Judgement: UNCLEAR.** The documented “restored verbatim” claim is true for the outer schedule (`docs/show-operation.md:319-325`) but not for the underlying motion. The new trajectories are coherent, but are not the old programs.

### 3.4 Other material chaser timing changes

- **Panel cycle — INTENTIONAL:** old Chaser 368 was a fixed Loop over all 41 effects except Effect 40 at 60,000 ms each. New Chaser 216 contains the same 41-effect keep-list but is Random at 12,000 ms each. The keep-list is explicitly owner-approved (`docs/panel-effects.md:59-66`); the faster random timing is a new aesthetic choice.
- **Strobes — INTENTIONAL safety change:** old Chasers 39/40 were unbounded Loop at 50/400 ms. New 453/454 are SingleShot eight-step bursts at 125/250 ms. This is the documented 4 Hz cap and latched-strobe fix (`TODO.md:161-168`).
- **Gobos — INTENTIONAL/UNCLEAR timing:** old Chaser 321 was a fixed 20-step Loop at 10 s; new 407 is Random, 23 steps including three jitter shakes, 4 s (`Vibra`) or 16 s (`Vibra-beats`). Random and jitter are deliberate (`docs/show-operation.md:106-107,169-175`); the exact speed remains an on-site judgement.
- **Colour wheels — INTENTIONAL architecture, changed timing:** old wheels were Random with 8–44 steps around 1,712 ms and no fades. New group wheels are Random with 10 solids or 30 mixes at 400 ms fade + 1,500 ms hold; the rig wheel is 17 steps at 800 ms fade + 2,500 ms hold. The one-clock rig-wide colour design is explicit (`docs/show-operation.md:110-126`).

### 3.5 Reachable Sequence behavior lost

- **Category:** Sequences / panel speed.
- **Old evidence:** Sequence 372 `Strobo LED - Random SPEED`, exposed by VC button 131 `Strobo LED - Speed Auto`, loops panel channel 8 through values `160 → 232 → 200 → 255`, with common FadeIn 45,000 ms, Duration 105,000 ms, and 60,000 ms holds on steps 2 and 4.
- **New state:** no Sequence or Script functions exist. A manual `Vel. Paneles` slider writes channel 8 on all four panels, but no function automates the old four-value modulation.
- **Judgement: LIKELY FORGOTTEN.** The new slider is explicitly awaiting a rig check (`TODO.md:52-55`), but no decision records retirement of the old live `Speed Auto` button.

The other old Sequences do not represent lost live behavior: Sequence 134 is a hidden six-step 500 ms bar experiment with no VC/function reference, and Sequence 375 is empty. Script 365 is also unreachable; its 1 s smoke-on / 2 s off loop was never bound to the old `HUMO AUTO` button. That button actually ran panel Chaser 367. The new smoke Chaser 445 deliberately provides a reachable 2 s burst / 60 s off loop (`docs/show-operation.md:108-109`).

## 4. EFX movement and dimmer effects

**Match summary:** the old seven principal absolute movement shapes survive for the wash family, and all old and new movement EFX are absolute. New EFX intentionally separate wash and beam optics and mirror house-right fixtures.

### 4.1 Whole-rig dynamic rainbow EFX are absent

- **Category:** EFX / colour.
- **Old evidence:** EFX 25 `Arcoiris Simultáneo` is relative, Circle, width 123, height 24, duration 13,696 ms, Parallel, Mode 2, over 39 fixture heads with all start offsets 0. EFX 26 `Arcoiris Pasos` is relative, Circle, width 127, height 10, duration 13,696 ms, with per-head offsets spread from 0 to 315 degrees. They are directly exposed on the old console with keys `'` and `¡`.
- **New state:** all 32 new EFX have `IsRelative=0`; none runs a continuous colour effect across the RGB heads. `Rig Multicolor 1/2` are static Scenes with beam rainbow/plasma companions, not behavioral equivalents.
- **Judgement: LIKELY FORGOTTEN.** No doc records their removal, and their direct key bindings prove they were operator-visible rather than dead experiments.

### 4.2 Main movement geometry is redesigned, not preserved

- **Category:** EFX / pan and tilt.
- **Old evidence:** EFX 0 and 48–53 provide Circle, Eight, Line, Diamond, Square, Leaf, and Lissajous over all 12 movers. Most use width/height 100/100, duration 6,848 ms, axes X `(offset=130, frequency=2, phase=90)` and Y `(130,3,0)`, Forward direction, with paired phase offsets. Chaser 23 is Random over 14 phased/simultaneous variants with 5,000 ms fade-in/out and 10,000 ms holds.
- **New state:** wash EFX 337–343 use 70×55 at 16,000 ms over eight washes; beam EFX 344–348 use 55×38 at 11,000 ms over four 7Rs. House-right wash 1 and beams 21/23 run Backward. New Chasers 369/370 are Random with 10,000 ms holds and no fades. Beams have no Square or Lissajous EFX. The old all-zero-start simultaneous variants and `Circle Loco` have no direct equivalents.
- **Judgement: UNCLEAR for the missing variants; INTENTIONAL for the family split, sizes, speed, and mirroring.** The design is explicit in `docs/show-operation.md:95-105,157-163` and `TODO.md:197-205`; loss of the simultaneous vocabulary and crossfades is not stated.

## 5. Virtual Console

**Match summary:** old console: 148 Buttons, one Frame, five Labels, two Sliders, three SpeedDials, one XYPad, one AudioTriggers widget. Each new console: 410 Buttons, seven Frames across three pages, 40 Labels, two Sliders, two SpeedDials, one XYPad, one AudioTriggers widget. The three new files have the same operator controls and function IDs; `Vibra-split` remaps CLB fixtures and `Vibra-beats` changes tempo behavior.

### 5.1 Keys 9 and 0 changed meaning

- **Category:** Virtual Console / key bindings.
- **Old evidence:** on heads, LEDs/PAR, and bars, key `9` invokes the alternating blue/red scene (for example Scene 30 `Azul / Rojo C`, Scene 123 `Azul/Rojo LEDs`, Scene 259 `Azul/Rojo Barra LEDs`) and key `0` invokes red/blue (Scenes 29, 122, 267).
- **New state:** on all four new banks, key `9` invokes Naranja (Scenes 14/56/98/140 by group) and `0` invokes Rosa (Scenes 15/57/99/141). The blue/red and red/blue scenes still exist on page 3, but have no numeric shortcut.
- **Judgement: LIKELY FORGOTTEN.** `palette.py:31-35` says the compact bank follows the original keys, then substitutes orange/pink. The operating guide says the night-running keys preserve muscle memory (`docs/show-operation.md:280-315`).

### 5.2 Other key and widget changes are deliberate

| Key | Old trigger | New trigger |
| --- | --- | --- |
| `Space` / `-` / `.` | Flash 100 / Flash 50 / Flash Color | Same intent |
| `H` | Held smoke | Held smoke |
| `Q` | `Rueda Colores` | `AUTO`; unified colour wheel moved to `W` |
| `W` / `E` / `R` | colours + bars / simple colours / colour mix | unified colours / unified mix / unbound |
| `A` | movement | movement |
| `S` / `D` | slow movement / both rest and `Escenario` | fixture strobe ON / OFF |
| `V` / `B` | forward/reverse dimmer chase (`B` also white) | forward/reverse dimmer chase, collision removed |
| `C` / `Z` / `M` | dimmer ping-pong / dimmer sequence / all three SpeedDials | beam colour / dimmer ping-pong / dimmer sequence |
| `J` | vertical-smoke panel-light chaser | automatic smoke; vertical-smoke light moved to `N` |
| `F`, `T`, `G`, `P`, `F1`–`F4` | unbound | bounded strobes, gobo, prism, and four room moments |

- Old `Space`, `-`, and `.` still trigger Flash 100%, Flash 50%, and Flash Color. `H` still provides held smoke. The XY pad contains the same 12 mover IDs; the new pad additionally benefits from the split fixture patch elsewhere.
- Old key collisions are removed: old `D` triggered both `Cabezas Reposo` and `Escenario`; `B` triggered both `Todo Blanco` and `Dimmer Chase 2`; all three SpeedDials used `M`. New keys are unique by design and `M` now runs `Dimmer Secuencia` (`docs/show-operation.md:286-315`). **Judgement: INTENTIONAL.**
- Old SpeedDials 23/38/54 had maximum 10,000 ms and shared tap key `M`; the colour dial also used multiply/divide/reset keys `K`/`L`/`Ñ`, while the chaser dial used `G`/`H`/`J`. New dials `Vel. Colores` (time 1,900, max 7,600) and `Vel. Movimiento` (time 10,000, max 40,000) have no keyboard key and target the consolidated wheels/chase families. **Judgement: INTENTIONAL architecture.**
- Old `Velocidad Cabezas` was a Level slider with no channels and did nothing. It is absent; the new movement SpeedDial is functional. **Judgement: INTENTIONAL**, documented in `TODO.md:238-241`.
- The old one-canvas layout became a three-page show/operator/library console, with StopAll, blackout, moments, library buttons, and a visible Grand Master. **Judgement: INTENTIONAL improvement.**

## 6. Audio, triggers, and other function types

**Match summary:** neither generation has a Show function. Old types were Scene 190, RGBMatrix 122, EFX 30, Chaser 20, Collection 11, Sequence 3, Script 1. New types are Scene 296, RGBMatrix 112, EFX 32, Chaser 30, Collection 38, with no Sequence or Script.

### Audio trigger semantics changed

- **Category:** Audio / triggers.
- **Old evidence:** AudioTriggers widget 25 has two type-3 `VCWidgetBar` bands: 0–1,000 Hz targets SpeedDial 38 `Duración Movimientos`; 1,000–2,000 Hz targets SpeedDial 23 `Duración Colores`; both use thresholds 12/51. QLC+ source confirms a type-3 bar targeting a SpeedWidget calls `speedDial->tap()` on threshold (`qmlui/virtualconsole/vcaudiotriggers.h:113-119`; `.cpp:537-550`). The old show therefore had two audio tap-tempo paths.
- **New state:** AudioTriggers widget 476 has one bound type-3 bar, `Graves`, thresholds 12/51, targeting Button 87, which flashes Scene 5 `Golpe Graves`. The other four bands are unbound. `Vibra-beats` additionally sets `BeatGenerator BeatType="Audio"` and marks 14 functions with `<Tempo>Beats</Tempo>`; the other two new files do not.
- **Judgement: INTENTIONAL.** The new non-strobing bass hit and deliberately unbound other bands are explicit (`docs/show-operation.md:352-370`); the separate Beats workspace is documented as requiring a selected audio input (`TODO.md:150-154`). The report nevertheless records the old tap-tempo behavior because it is not equivalent to the new hit.

### RGBMatrix and Collection types

- Old 122 matrices comprise one standalone head test plus 121 bar effects used by Chaser 135. New 112 comprise 34 bar, 33 head, 33 PAR, and 12 rig-colour companion matrices. This is broader fixture coverage but much less bar-specific content; see Finding 3.2.
- Collections rose from 11 to 38 and now express rig-wide colour ownership, moments, movement-family unions, and state composition. No old Collection has a material unique end behavior beyond the dimmer trajectory difference already reported.

## 7. Global settings and workspace variants

**Match summary:** Universe 1 remains the only universe, no passthrough is configured, Grand Master semantics remain `ChannelMode=Intensity`, `ValueMode=Reduce`, `SliderMode=Normal`, and the old SimpleDesk cue is preserved. Monitor geometry is intentionally expanded.

### 7.1 USB-DMX output binding differs among shipped files

- **Category:** Global settings / output mapping.
- **Old evidence:** original old workspace output is `Plugin="DMX USB"`, `UID="FT232R USB UART (S/N: A50285BI)"`, line 0.
- **New state:** `Vibra.qxw` and `Vibra-beats.qxw` keep that exact UID. `Vibra-split.qxw` instead stores `Name="FT232R USB UART (S/N: AB0PEY7F)"`, empty `UID`, line 0. The public rig guide says the output should use `UID="None"` so it binds to whichever USB-DMX interface is connected (`docs/rig.md:3-6`).
- **Judgement: UNCLEAR.** This may reflect different machines or QLC schema serialization, but the three files are not equivalent. If the non-split or Beats file is launched with only the current interface attached, output binding is the first show-night risk to test.

### 7.2 `UniverseChannels=300` in two new files is stale but self-correcting

- **Category:** Global settings / universe width.
- **Old evidence:** old output serializes `UniverseChannels="300"` for the DMX 1–300 patch.
- **New state:** `Vibra` and `Vibra-beats` still serialize 300 despite fixtures through 316; `Vibra-split` serializes 316.
- **Judgement: INTENTIONAL runtime behavior / stale serialization, not a fixture blackout.** QLC+ raises `m_totalChannels` whenever fixture capabilities reach a higher channel and marks the count changed (`engine/src/universe.cpp:845-850`); before output it pushes the recomputed value into the plugin (`engine/src/universe.cpp:722-737`). The saved 300 should still be normalised to 316 at runtime. It remains worth making the files consistent to avoid misleading audits.

### 7.3 Beat, input, monitor, and launch state

- Old original and `Vibra` have BeatGenerator Disabled/BPM 0; old v5 conversion and `Vibra-split` store Disabled/BPM 120; `Vibra-beats` uses Audio/BPM 0. **Judgement: INTENTIONAL variant.**
- Old original has no input. The 4.14.3 conversion stores a MIDI `ble device`; the v5 conversion stores MIDI `None`; all new workspaces have no input mapping. No VC key or function depends on that MIDI mapping. **Judgement: conversion residue / no demonstrated loss.**
- Old monitor: grid 5×3×5 with only BEAM IDs 20–23 positioned. New monitor: grid 12×6×8 with the whole rig and stage meshes positioned. **Judgement: INTENTIONAL improvement.**
- Old original, `Vibra`, and `Vibra-beats` save `CurrentWindow=VirtualConsole`; `Vibra-split` saves `IOMGR`. The documented launch uses `qlcplus -k -f -o ...`, which forces the Virtual Console (`docs/show-operation.md:372-384`), so this is not an operational loss under the runbook.

## Conversion and methodology notes

- The two converted old files preserve patch, function counts, Scene value maps, Chaser steps, EFX geometry, and console widget counts. Their only engine-semantic differences detected against the original are QLC conversion defaults replacing nine zero durations with small finite values (13, 26, or 208 ms), plus saved I/O/window metadata. Findings above use the original hand-built file as requested.
- Scene comparison used physical Universe/address maps, not names or function IDs. Fixture channel roles and capability equivalence were resolved through the repo `.qxf` files.
- Function reachability included VC Button references, Chaser steps, Collection steps, and bound Sequence behavior. That is why unreachable Sequence 134 and Script 365 are not reported as show-night losses.
- No repository file was written. Scripts, extracted JSON, rendered output, and this report live only in the requested scratchpad.

## Verification

Executed results:

- inventory, focused function evidence, scene matching, and colour coverage all reproduced byte-for-byte with the commands below;
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/ -q -p no:cacheprovider -k 'not test_qlcplus_loads_the_show'` — **276 passed, 1 deselected**;
- `PYTHONDONTWRITEBYTECODE=1 timeout 70 .venv/bin/python -m pytest tests/test_canonical_show.py::test_qlcplus_loads_the_show -q -p no:cacheprovider` — **1 passed**;
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/qlctool check '../../QLC+ Setups/Vibra-split.qxw'` — **408 operator buttons checked, no problem**;
- `git status --short` — empty before and after verification.

Run the inventory check from the repository so the stored relative path labels remain reproducible:

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
PYTHONDONTWRITEBYTECODE=1 python3 \
  '/private/tmp/claude-501/-Users-cristiandeluxe-p-DMX-Fixtures/7643e44f-f8c2-4969-bc29-f57febaa6684/scratchpad/semantic_inventory.py' \
  'QLC+ Setups/DeluxeEventos2.qxw' \
  'QLC+ Setups/DeluxeEventos2_qlc4143.qxw' \
  'QLC+ Setups/DeluxeEventos2_qlcv5.qxw' \
  'QLC+ Setups/Vibra.qxw' \
  'QLC+ Setups/Vibra-beats.qxw' \
  'QLC+ Setups/Vibra-split.qxw' \
  > '/private/tmp/claude-501/-Users-cristiandeluxe-p-DMX-Fixtures/7643e44f-f8c2-4969-bc29-f57febaa6684/scratchpad/inventory.recheck.json'

cmp \
  '/private/tmp/claude-501/-Users-cristiandeluxe-p-DMX-Fixtures/7643e44f-f8c2-4969-bc29-f57febaa6684/scratchpad/inventory.json' \
  '/private/tmp/claude-501/-Users-cristiandeluxe-p-DMX-Fixtures/7643e44f-f8c2-4969-bc29-f57febaa6684/scratchpad/inventory.recheck.json'
```

The focused scene, colour, and function-graph evidence is reproducible from the scratchpad with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_details.py inventory.json \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/DeluxeEventos2.qxw' \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/Vibra-split.qxw' \
  > audit-details.recheck.json

cmp audit-details.json audit-details.recheck.json

PYTHONDONTWRITEBYTECODE=1 python3 compare_scenes.py inventory.json 0 5 \
  > scene-matches.recheck.json
cmp scene-matches.json scene-matches.recheck.json

PYTHONDONTWRITEBYTECODE=1 python3 color_coverage.py \
  '/Users/cristiandeluxe/p/DMX-Fixtures' \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/DeluxeEventos2.qxw' \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/Vibra.qxw' \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/Vibra-beats.qxw' \
  '/Users/cristiandeluxe/p/DMX-Fixtures/QLC+ Setups/Vibra-split.qxw' \
  > color-coverage.recheck.json
cmp color-coverage.json color-coverage.recheck.json
```
