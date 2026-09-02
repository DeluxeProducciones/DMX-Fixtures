# The rig

29 patched fixtures on **one universe**, DMX addresses 1-390 contiguous, zero
overlaps (verified by `qlctool patch`, which is a test). Output is the QLC+
**DMX USB** plugin with `UID="None"`, so it binds to whatever USB-DMX interface
is connected.

A naive scan reporting "369 fixtures" is wrong: 342 of those are fixture-ID
*references* inside scenes and groups.

| Qty | Fixture | Mode | ch | Moves |
| --- | --- | --- | --- | --- |
| 4 | Pro-Lights CromoWash100 | Advanced | 12 | yes |
| 2 | Mac Mah MAC WASH 1915Z | 23 Channel | 23 | yes |
| 2 | Stairville LED Bar 240/8 RGB | - | 24 | no |
| 2 | Stairville CLB2.4 PAR | - | 14 | no |
| 7 | Vortex PC-64 LED S | Default | 5 | no |
| 2 | Chauvet MiN Wash | 13 Channel | 13 | yes |
| 2 | LED Beam Mini Moving Head | 16 Channels | 16 | yes |
| 4 | Generic BEAM 230W 7R | 16 channel | 16 | yes |
| 2 | HYULIGHTS WX-60WPS-48PARTITION | A MODE 8CH | 8 | no |
| 1 | Stairville AF-150 (fog) | Generic Smoke / Amount | 1 | - |
| 4 | Generic LED Spray Fog (humo vertical) | 7 Channel | 7 | - |

**Fourteen fixtures move**, not six: the CromoWash100, the MiN Wash and the MAC
WASH 1915Z are moving washes. Selecting movers by capability (a fixture with
both pan and tilt) returns exactly the twelve the hand-built "Movimiento
Circulo" EFX drove plus the two new washes, which is the check the toolkit uses
instead of a hardcoded list.

**The two MAC WASH 1915Z came on 2026-08-29**, patched at DMX 345 and 368, in
place of the two CromoWash100 that hang at back truss 4 and 7 and did not make
it to that show. The CromoWash stay patched and park with the other spares in
the plot. The MAC WASH is the first fixture in this rig whose **beam width is a
DMX channel**: `zoom_wide_pairs` writes it wide in every look that lights it,
`rule_zoom_narrow` fails any scene that forgets, and which end is wide comes
from the definition's capability preset. **That preset was wrong until
2026-09-02.** The manual prints `Zoom 000-255` and nothing else, the first
definition guessed `SmallToBig`, and the show sent 255 to every look - which
on this unit is the 6-degree end, so both washes ran as pencils. ChamSys
MagicQ's own personality for the MacMah MacWash1915Z (Fixture Finder ids
46510 and 46511, edited 2023-07-24) says *Wide to Narrow 0-255*, and it also
gives the strobe (0 open, 1-127 strobe slow to fast, 128-159 sudden, 160-191
pulse, 192-255 random) and the reset (100-109) the manual leaves out. The
definition carries all three now, `zoom_wide_pairs` writes 0, and `Strobo ON`
lands inside 1-127 instead of in the random band. What stays a platform
guess: that 0 on the Function mode channel is DMX control - ChamSys calls the
channel `Macro` and gives it no ranges either.

The rig has **not** been confirmed against the physical hardware. That check is
an on-site job.

## Where they stand - the montage we always build

Described by the owner on 2026-08-25 from a video of a get-in, and written down
in [`QLC+ Setups/vibra-stage-plot.json`](../QLC+%20Setups/vibra-stage-plot.json)
so it never has to be described again. `qlctool stage --plot` applies it
verbatim; `newshow --plot` builds the show on it.

**Back truss, ten positions, house left to house right:**

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAR | **7R** | PAR | **wash** | PAR | PAR | **wash** | PAR | **7R** | PAR |

PARs are Vortex PC-64, 7R are BEAM 230W, washes are MAC WASH 1915Z since
2026-08-29 (CromoWash100 before that). Symmetric: beams at 2 and 9, washes at 4
and 7.

**Front truss, seven positions, the same way round:**

| 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- |
| **grid** | pixel | pixel | **bar** | pixel | pixel | **grid** |

The two CLB2.4 grids at the ends aim *back at the DJ*; the four pixel panels and
the LED bar dead centre aim *out at the audience*.

**The rest:**

| Where | What |
| --- | --- |
| Either side of the DJ deck | the other two BEAM 230W, one on a flightcase each, **aimed up and out over the room** |
| Over the DJ booth | the second Stairville LED Bar 240/8 |
| One side, upstage | the smoke machine |

The DJ deck is the usual 1 x 2 m stage top on legs, with a flightcase either
side of it. Deck, legs, cases and a blocky stand-in for the DJ are `props` in
the plot: QLC+ `MeshItem` entries built from its own bundled primitives
(`generic/cube.obj`, `cylinder.obj`, `sphere.obj`). They are scenery, not
fixtures, and exist so the preview looks like the room.

**Which way is the audience.** `z` grows **towards** them. QLC+'s 3D camera
starts at `(0, 3, 7.5)` looking at the origin
(`MainView3D::resetCameraPosition`), so it sits on the +Z side: the far end of
the stage is small z and the front edge is large z. This plot had it backwards
once and the whole rig came out mirrored, with the back truss hanging over the
crowd.

**Which way things point, and it is not one rule.** `x_rot` is degrees about the
horizontal axis, and QLC+ turns the fixture by **minus** the stored angle -
`MonitorProperties::fixtureRotationMatrix` builds it as
`fromAxisAndAngle(QVector3D(1, 0, 0), -rot.x())`, matching
`Qt3DCore::QTransform::fromAxesAndAngles` in the 3D view. What that does to the
light depends on **how QLC+ draws the fixture**:

| Drawn as | Emits | Aimed at the audience with |
| --- | --- | --- |
| a mesh - PAR, moving head, smoke | `(0, -1, 0)`, down | **positive** `x_rot` |
| QLC+'s own geometry - `LED Bar (Pixels)`, `LED Bar (Beams)`, `Strobe` | `(0, +1, 0)`, up | **negative** `x_rot` |

The second row is not a quirk of this rig: `PixelBar3DItem.qml` puts each head's
`PlaneMesh` at `+(phySize.y / 2)` and a Qt3D plane faces `+Y`, so a pixel bar
lights out of its top face. `Strobe3DItem.qml` and `MultiBeams3DItem.qml` do the
same.

Both halves of this were wrong on 2026-08-25, one after the other. The plot
started with the sign inverted for everything, and the landing arithmetic, its
tests and this page all agreed with it - so every check passed while the six
truss PARs lit the wall behind the stage. Flipping it uniformly fixed the PARs
and turned the pixel panels and the LED bars around, which had been right all
along. Both were caught in the 3D view, by the owner, in minutes. A sign
convention comes out of the renderer's source, per fixture type - never out of
what one fixture looks like in a preview.

**A moving head is mounted, not aimed.** Its rotation says how the body hangs -
`0` from a truss, `180` standing on the floor - and where the light goes is pan
and tilt, which the show drives. Tilting the mounting of a mover does not aim
it; it leaves it sitting crooked on its clamp and the beam still sweeps wherever
the EFX sends it. `test_a_moving_head_is_mounted_never_aimed` holds the rule.

For everything else the rotation *is* the aim, and it is worked out rather than
eyeballed. `qlctool stage --plot` prints where each beam meets the floor, and
`beam_landing` is the arithmetic behind it:

| Fixture | `x_rot` | Where the beam lands |
| --- | --- | --- |
| Six truss PARs | `50` | z = 6417, 1,9 m past the DJ deck, passing 35 cm over his head |
| Four pixel panels, both LED bars | `-90` | never - level, straight at the room (top-face emitter: the sign is inverted) |
| Two downstage grids | `-35` | z = 4749, on the DJ deck |
| Two beams on flightcases | `180` | mover: standing upright, base down |
| Four truss movers | `0` | mover: hanging |

The PARs were at 35 degrees first, which looked like "tilted towards the
audience" and landed at **z = 4485** - the DJ deck is at 4500. They were
lighting him in the face. That is the whole reason the landing calculation
exists. 50 is the angle the owner measured on the real truss on 2026-08-25; 60,
which the plot carried before, threw them 2,2 m further out than the rig
actually does.

### Why the wash heads would not move

They received the movement EFX like everything else, and the EFX geometry
matched the hand-built one node for node. What arrived was the problem. With
AUTO running, the DMX view read:

| | ch1 Pan | ch2 Pan fine | ch3 Tilt | ch4 Tilt fine |
| --- | --- | --- | --- | --- |
| CromoWash100 #1 | **0** | 0 -> 31 | **0** | 57 -> 21 |
| BEAM 230W 7R #1 | 92 -> 127 | - | 227 -> 28 | - |

The wash's *coarse* channels never left zero and only the fine ones moved, so
the head travelled one 256th of its range - and, being stuck at zero rather than
merely frozen, parked at one end of 270 degrees of tilt and sat pointing at the
ceiling. The manual prices the movement exactly: *Pan Fine = 0,008 degrees*, so
a full sweep of the fine channel alone is **2,05 degrees out of 540**.

**It was our EFX, not QLC+ and not the definition.** `EFXFixture` caches its pan
and tilt channels when an EFX starts and, if a fine channel is not directly
after its coarse one, calls `fader->setHandleSecondary(false)`. That fader
belongs to the **EFX**, not to the fixture - so one badly ordered fixture turns
16 bit off for every fixture sharing that EFX.

| Fixture | Channel order | Pairs |
| --- | --- | --- |
| CromoWash100 | `Pan, Pan fine, Tilt, Tilt fine` | yes |
| MiN Wash | `Pan, Pan fine, Tilt, Tilt fine` | yes |
| LED Beam Mini | `Pan, Tilt`, no fine channels | never trips it |
| **BEAM 230W 7R** | `Pan, Tilt, Pan fine, Tilt fine` | **no - two apart** |

All twelve movers were in one EFX, so the four beams switched 16 bit off for the
four washes and the two MiN Wash, whose coarse channels were then written as
part of a 16-bit value that nothing split.

The generator now puts them in separate EFX and runs the pair from a Collection,
so the Virtual Console and the chaser still see one function per shape. Measured
after the split, with AUTO running:

| | ch1 Pan | ch2 Pan fine | ch3 Tilt | ch4 Tilt fine |
| --- | --- | --- | --- | --- |
| CromoWash100 #1 | **30** | 95 | **30** | 95 |
| CromoWash100 #2 | **40** | 116 | **40** | 116 |
| BEAM 230W 7R #1 | 30 | - | 30 | - |

Both kinds move, in Advanced 12-channel mode, on QLC+ 5.2.2, with nothing
changed on the fixtures.

**The Dimmer-mode EFX has the identical hazard** on the *intensity* channels
instead, and is now split the same way. Nothing in this rig has a 16-bit dimmer,
so nothing is split today and `Dimmer Chase` is a plain EFX - but patch a
fixture that does and it will divide rather than take the rest down with it.

### Two things that were ruled out, with evidence

- **`Basic` 9-channel mode works but is not needed.** A throwaway copy with the
  four CromoWash switched to it read full travel on the coarse channels. It was
  the right diagnosis of the symptom and the wrong cure - and it would have
  meant changing the mode on every fixture from its own panel.
- **A newer QLC+ changes nothing.** 5.2.2 is the latest release, so the only
  newer thing is a nightly; the macOS artifact for 5.3.0 GIT was downloaded and
  run against this show and read exactly what 5.2.2 reads. The engine symbols
  say why: `FadeChannel::primaryChannel`, `addChannel` and `channelCount` are
  all already exported by 5.2.2, so the secondary-channel machinery is not new
  and `updateChannel` is a refactor of `getChannelFader`, not a fix.

### Smoke does not show in the 3D view

There is nothing to fix. QLC+ 5 draws no plume: `smokeAmount` is a single
scene-wide haze density that the spotlight scattering shader multiplies by, and
it is what makes the beams visible at all. It sits at 0.8 and there is a slider
for it under the 3D view's settings button. The smoke machine's own mesh is
drawn where the plot puts it; it just does not emit.

### Two pixel panels were missing from the patch

There are four HYULIGHTS WX-60WPS-48PARTITION on the front truss and the patch
had two. AliExpress order `3040390036254050`, 2024-08-22, says
`WX-60WPS-48PARTITION x4` for 88,69 € - four were bought. The other two are now
patched at DMX 301 and 309, continuing the universe, as fixtures 27 and 28.

They also had to be **put into the `BarrasLed` group**. Colour banks and matrices
are both generated per group, so a fixture in no group gets only the handful of
rig-wide scenes: the two new panels came out with 7 scene values against their
neighbours' 47. See [Fixture groups](#fixture-groups).

**The current patch is `Vibra.qxw`, not `DeluxeEventos2.qxw`.** The hand-built
original stays as the reference the builders are tested against, but it is two
fixtures behind the rig now, so `newshow` runs from `Vibra.qxw` itself.

### The four vertical fog machines replaced the spare (2026-08-29)

The 2-channel "Generic Smoke" parked at 299 was a placeholder; the real
machines are four unbranded vertical LED fog machines ("tipo CO2"), 7 fixed
DMX channels each: fog, LED master dimmer, R, G, B, LED strobe, LED colour
cycle. The scanned leaflet and its clean twin (the Audibax Geyser 2000 RGB
manual, same OEM map) are in `Manual/`. They are patched at **317, 324, 331
and 338** - the placeholder's 2-channel footprint at 299 would have put the
real machine's RGB under the WX panel at 301, driving the fog machine's LED
with panel data.

Two facts shape everything generated for them:

- **DMX priority.** With a controller plugged in, the machine's own timer,
  remote and colour program are dead. Nothing lights the column unless the
  show writes dimmer + colour; `qlctool check`'s `humo-luz` rule fails any
  show where the pump fires and no function does.
- **The pump is a role of its own.** The fog channel is typed with the smoke
  role (never as a dimmer), which is what lets the LED half live as an
  ordinary RGB fixture - on the colour wheel, in the blackout, under the
  energy levels, a floor PAR - while only the smoke scenes can reach the
  pump. `Humo Auto` stays with the fog-only AF-150; the verticals fire from
  the held `Humo Vertical YA` button (key U), white while the column is up,
  back to the room's colour on release.

### A four-head bar is one light in the 3D view

The CLB2.4 is a T-bar with **four PAR heads on adjustable brackets**, and its
14-channel mode drives each one's RGB separately. The 3D view cannot show that:
`MainView3D::createFixtureItems` builds **one item per fixture** (only a
`Dimmer` pack is split, one item per channel), and a meshed fixture's item
ignores the head index outright - `Fixture3DItem.qml`'s `setHeadIntensity` and
`setHeadRGBColor` assign to a single `dimmerValue`/`lightColor`, so the four
heads collapse into one light showing whichever head was written last. The
`linked fixture` feature duplicates a whole fixture, colour and all, so it does
not help either.

Only the fixture types QLC+ draws itself - `LED Bar (Pixels)`, `LED Bar (Beams)`,
`Strobe` - render per head, which is why the pixel panels light cell by cell.

So a four-head bar can only be emulated by **patching each head as its own
fixture**: four 3-channel RGB fixtures on the head triples, plus something to
hold the bar's master dimmer at full. That is a patch decision, not a plot one -
it does not change a cable, only how QLC+ sees the same 14 channels.

### The split, as a copy to look at (2026-08-25)

`QLC+ Setups/Vibra-split.qxw` is the same rig with each CLB2.4 patched **four
times, one per head**, so all eight can be aimed and coloured separately. The
cabling does not change: the bar still sees the same 14 channels, and the split
works because the two channels that are not a head's RGB sit next to one.

| DMX (bar 1) | Fixture | Mode |
| --- | --- | --- |
| 73-76 | CLB2.4 1 PAR 1 (master) | `Master + PAR` - the bar's dimmer plus head 1 |
| 77-79 | CLB2.4 1 PAR 2 | `PAR` |
| 80-82 | CLB2.4 1 PAR 3 | `PAR` |
| 83-86 | CLB2.4 1 PAR 4 (strobe) | `PAR + Strobe` - head 4 plus the bar's strobe |

Bar 2 repeats it at 87-100. The master dimmer riding with head 1 is what keeps
the bar lit: that fixture has RGB, so every colour scene raises its dimmer, and
`Todo Negro` takes it down again. The strobe riding with head 4 is what puts the
CLB2.4 into `Strobo ON` / `Strobo OFF` for the first time - the manufacturer
definition's shutter channel carries no labelled range, so the generator
deliberately left it alone.

**The definition is repo-local and says so.** `CLB2.4 PAR head (split)` is not a
manufacturer mode - the bar's six live in `Stairville-CLB2.4-CompactLED.qxf` -
and its header comment says as much, because in two years the name alone would
not. Each mode declares its own `<Head>` over the three colour channels rather
than leaning on the default QLC+ builds when a mode declares none
(`fixture.cpp:685` inserts one head with *all* channels, strobe included).

Its physical block is per head and derived, not measured: the manual gives the
bar as 1007 x 305 x 63 mm with the spots and 982 x 55 x 55 without, so a can
hangs about 250 mm below the bar and is 63 mm deep; 230 mm of width is read off
the product photo against the 252 mm spacing. Weight and power are the bar's
divided by four, so a rig total still adds up, and `Lumens` is 0 because the
manual gives **lux at 2 m**, not lumens - a distinction QLC+'s own definition
loses when it writes `Lumens="1364"`.

Built with the toolkit, not by hand:

```bash
qlctool patch Vibra.qxw --remove 4 --remove 5 --out step1.qxw
qlctool patch step1.qxw --add "Stairville|CLB2.4 PAR (split)|Master + PAR|0|73|CLB2.4 1 PAR 1 (master)" ... --out step2.qxw
qlctool patch step2.qxw --group-size "2=7x3" --group-add "2=29@3,0" ... --out split-patch.qxw
qlctool newshow split-patch.qxw --plot "QLC+ Setups/vibra-stage-plot-split.json" \
  --out "QLC+ Setups/Vibra-split.qxw" --validate
```

The plot for it is `vibra-stage-plot-split.json`: each head sits at the centre
of its quarter of the 1007 mm bar, aimed back at the DJ at `-35` like the bar
was. Fan them apart there and each head goes its own way.

That `PAR` group was a 7x3 grid with the CLB2.4 heads bolted to the right of the
PC-64 block, rather than the 8x2 that reads like the rig, because at the time
`--group-add` refused a head it had already placed and there was no way to say
"the same head, somewhere else". There is now:
`--group-move "GROUP=FIXTURE[:HEAD]@X,Y"` moves a placed head to a free cell (a
swap is two moves with a free cell in between). Name the head for a bar or a
panel, whose heads are all one fixture - `BarrasLed` is sixteen heads of two
fixtures. Re-laying the group is a matrix change - every pattern paints the
cells the group declares. It is a flat 15x1 now, laid out in stage order by
`--group-sort` (2026-08-31).

**It found a real bug in the strobe generator.** The new definition labels DMX 0
`No strobe` and marks it `ShutterOpen`, with the strobe on 1-255. The generator
picked its strobe range **by name**, matched "No strobe" first, and wrote
`Strobo ON` as a zero - the one value that guarantees no strobe. It reads the
`Strobe*` **preset** now and falls back to the name only when a definition
carries none, which is how the BEAM and the MiN Wash still work.

### They looked like PAR cans in 3D

The pixel panels were `<Type>Color Changer</Type>`, and the 3D view picks the
mesh from the type: Color Changer loads `par.dae`, a PAR can. A flat panel is
`LED Bar (Pixels)`, which QLC+ draws procedurally from the fixture's own heads
and physical size instead of loading a mesh at all - a 250 x 130 mm rectangle,
which is what they are.

That needed a `<Head>` as well. A pixel bar is drawn one cell per head and this
definition declared none, so as an LED bar it would have been drawn as nothing.
The panel is 48 LEDs but a single addressable RGB, so it gets the one head it
really has.

## Fixture groups

| ID | Name | Grid | Fixtures |
| --- | --- | --- | --- |
| 0 | BarrasLed | 8x2 | 2, 3 |
| 1 | Cabezas | 12x1 | 0, 1, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23 |
| 2 | PAR | 15x1 (7x1 on the pre-split patch) | 6-12, 29-36 |
| 3 | PixelesLed | 4x1 | 24, 25, 27, 28 |
| 4 | Lyres | 3x2 | 41, 42 (33, 34 on the pre-split patch) - one cell per ring |

Groups are what an RGBMatrix paints onto, and what the colour banks are built
per - so a fixture in no group gets neither, and a fixture in *two* gets two of
each. That second half is not obvious and cost a night: see the beams below.

**The cells are in stage order, not patch order (2026-08-31).** A matrix paints
the cells a group declares and half of QLC+'s scripts mean a direction, so cell
0 has to be at one side of the room and the last cell at the other. Nobody had
ever said so: a group is built in DMX address order, which is cabling order, and
`Cabezas` walked its four rigged beams 1916, 9694, 4405, 7205 mm across the
stage. Every sweep started house-right, jumped house-left, walked back and
jumped again. `qlctool patch --group-sort GROUP` lays a group out by the
`<Monitor>` positions the plot writes, and `qlctool check`'s
`rejilla fuera de orden` says when one has drifted. Fixtures the plot marks as
not rigged go last - eight of `Cabezas`' twelve members are spares in cases, and
a spare cannot be anywhere in a sweep.

**`Lyres` is one cell per ring (2026-08-31).** The MAC WASH 1915Z is three
concentric RGBW rings on one DMX footprint, and its definition declared no
`<Head>` at all. QLC+ does not read that as "no heads": it builds a single head
holding every channel, keeping the *last* channel of each colour, so a matrix
would have painted the outer ring and left the other two on whatever was written
last. Three `<Head>` blocks in the definition fixed it, `cabezas sin declarar`
is the rule that sees it, and the group is 3x2 - ring across, fixture down.

**`BarrasLed` declared 8x2 over three rows of heads.** An RGBMatrix paints the
cells a group *declares*, not the heads it holds, so row 2 - the four beams and
the pixel panels - was unreachable by every matrix in the show. The grid is now
8x3 and the panels are reachable.

**The panels animate themselves, and the show ignored it until 2026-08-26.**
Their eight-channel mode carries three channels nothing was driving: a *mode*
channel (0 "No function", 1-85 Mixer Color, 86-171 **Auto Mode**, 172-255 Sound
Mode), a channel choosing one of **42 built-in effects**, and a speed. Left at
zero, as an untouched channel is, the fixture is four RGB cells - which is all
this rig ever asked of it. `Ciclo Paneles` now walks the 42 under `AUTO` and in
the lively moments, and all 42 are on the console because nobody has watched
them: the definition names them "Effect 1" to "Effect 42" and there is no
manual for them in `Manual/`.

Two consequences, both traps. In Auto Mode the fixture **ignores red, green and
blue**, so the panels came off the rig-wide colour wheel and their matrices are
no longer generated - a four-cell chase over a fixture with 42 animations of
its own was never worth having. And the mode channel is **sticky**: every scene
that states a colour now drives it back to "No function", the same way it drives
the shutter open, or the panel keeps running last night's effect through a
speech. `qlctool check`'s `programa interno` rule is what keeps that true.

**The four wall panels left the group on 2026-08-26 as well**, into a
`PixelesLed` group of their own, and the owner is the one who saw it: "los 4
pixel led no tienen que ir con las 2 barras led, son luces diferentes". A group
is not a container, it is a *picture*: an RGBMatrix paints one grid across
every head in it, so four single-cell panels sharing the bars' 8x3 grid were
four cells of the bars' picture, sitting in columns 4-7 of the bottom row and
therefore dark through the first half of every horizontal sweep. Now they have
a 4x1 grid, their own colour bank and their own matrices.

**Every grid is now exactly the size of its group.** A cell with no head is a
frame of every sweep where part of the group is dark for nothing; a head
outside the grid is a fixture no effect can reach. Both were present at once -
`BarrasLed` had four empty cells and `Cabezas` declared 8x1 over twelve heads,
four of them unreachable. `qlctool patch --group-reshape` re-lays a group's
heads in reading order into a grid that fits, and `qlctool check`'s `rejilla`
rule refuses to let it happen again.

**The four beams left the group on 2026-08-26**, and `qlctool check` is why.
Being in a group is not only being in its grid: colour banks are generated per
group too, so the beams were in the bars' colour bank *and* the heads', and
`Rueda Mezcla` - a Collection over the three groups' mix wheels - started two
of them writing the beams' colour wheel at once. A matrix does nothing on a
fixture with no RGB, so the grid loses nothing. Their four cells in row 2 stay
empty rather than being closed up: a matrix paints the grid the group declares,
and shuffling the survivors would move every remaining head in every pattern.

## Smoke machines

Two, and they are handled apart from everything else: every generator skips
fixtures whose definition says `<Type>Smoke</Type>`, because a pump caught in an
"all dimmers to full" scene runs until the tank is empty. Only the smoke
generator drives them - a burst, then a long wait, on a loop.

## Fixture definitions

Eleven custom `.qxf` in `QLC+ Fixtures/`, plus the QLC+ system library. QLC+ 5
ships `Pro-Lights-CromoWash100.qxf` itself, which is why that one fixture
resolves even when the custom definitions are not installed. The CLB2.4 is
QLC+'s own definition, vendored here with one correction - see below.

### Verification status

| Fixture | Status |
| --- | --- |
| Pro-Lights CromoWash100 | **Fully verified** against `Manual/ProLights - CromoWash 100.pdf` on 2026-08-25: both modes channel for channel (3.12), every capability range of the colour macro, strobe and control channels, and the whole physical block (1.3). Three things were wrong and are fixed - see [What the manual corrected](#what-the-manual-corrected). The 12-channel Advanced order is `Pan, Pan fine, Tilt, Tilt fine, Pan/tilt speed, ...`, which is what used to stop it moving: see [Why the wash heads would not move](#why-the-wash-heads-would-not-move) |
| Audibax IOWA70 | Verified against the repo manual; orphan, not patched |
| Chauvet MiN Wash | **Verified against the manufacturer manual, now in `Manual/`** (2026-09-01; the 2008 edition, recovered through the Wayback Machine because Chauvet's own page is gone and the product was discontinued around 2012). All 13 channels match, every range of the colour macro and movement macro channels matches, and four small things were wrong and are fixed: the shutter's `Closed` range started at 1 and left DMX 0 undefined (manual: 0-7), the last movement macro was labelled `Sound Active 9` (manual: 8), the pan/tilt speed channel's preset read backwards - the manual says *Vector Speed: Normal -> Slow*, so 0 is the quick end and `SpeedPanTiltFastSlow` is right - and the power figure was the 82 W inrush rather than the 61 W the unit draws. Two facts worth knowing: the show never writes channel 5, and at 0 that is the *fast* end, so the heads track the EFX; and channel 6 is dimmer and shutter in one, with the dimmer segment inverted (8 = full, 134 = dark) and 240-255 open - the show writes 255. Its `5 Channel` mode was **deleted on 2026-08-31** because it had been written by hand; the manual's 5-channel mode is Pan, Tilt, Dimmer/Strobe, Colour Macro, Vector Speed, should anyone need it |
| HYULIGHTS WX-60WPS | Definition declares 10 channels, the used mode exposes 8, matching the patch. No manual online (searched 2026-09-01: every listing of the `48PARTITION` variant - 288 SMD5050 RGB LEDs, 48 segments, 60 W, 250 x 130 x 70 mm - says **"8 channel"** and nothing else, so 8 is the only DMX mode and there is no per-segment mode on this unit; the factory's 48-segment pixel mode (144 channels) exists only on the 250 W HYU-200PS). The remote's key chart on one listing confirms the definition's shape - Auto `CC01`-`CC42` (01 fast auto, 02 colour gradient, 03 colour jump, the rest unnamed), Sound `SU01`-`SU02`, strobe `FH01`-`FH99`, seven static colours - so the definition was read off the paper leaflet in the box, which is the only chart there is. The sibling HYU-60PS manual (8 RGB + 4 white segments, modes 4/6/12/24/30) is a useful template and not this unit |
| Stairville CLB2.4 | **Fully verified** against `Manual/Stairville-CLB2.4-Compact-LED-PAR-System-manual-es.pdf` on 2026-08-25. All six modes match the manual channel for channel (7.5-7.10), including the 14-channel one the patch uses - `Dimmer, R/G/B x PAR 1..4, Strobe` - and the four heads it declares. Every range of the auto-show and fixed-colour channels matches (14 programs then Sound; 15 colours ending in Amber), and the physical block matches the technical data (1007x305x63 mm, 5,6 kg, 50 W, 1364 lux, 3-pin). **One thing was wrong: the lens** - see [The CLB2.4's beam angle was missing](#the-clb24s-beam-angle-was-missing) |
| Generic BEAM 230W 7R | **Verified on the hardware by the owner**, who states he tested the channel order when he wrote the definition (2026-08-25). The hand-built show corroborates the two channels that matter most: `Luz ON Cabezas` sends 255 to channel 6 and 255 to channel 7, `Luz OFF Cabezas` sends 0 to both - so channel 6 is the shutter, shut at 0, and channel 7 is the dimmer. No manual matches it (one found for a Rambo 230 puts Color on ch1 and Pan on ch10), so the hardware is the only reference there will be. A second search on 2026-09-01 over a dozen Sharpy-clone manuals found none whose 16-channel mode matches ours past channel 7: the closest is the official BeamZ Panther 7R manual, identical on channels 1-7 (`Pan, Tilt, Pan fine, Tilt fine, speed, strobe, dimmer`) and permuted from 8; the rest of the family (Ridgeyard, ETC/Hong Yi/Halo/YF) carries our exact *function set* - separate colour-effect and gobo-shake channels - in yet another order, with one shared value table for strobe, colour, gobo and prism. That shared table is the best guess for our unlabelled ranges (strobe `0-3 closed, 4-103 slow-fast, 104-107 open, 108-207 pulse, 213-251 random, 252-255 open`; prism `0-127 out, 128-255 in`; prism rotation `0-127 index, 128-190 one way, 191-192 stop, 193-255 the other`; reset above 128) and is only a guess until the probe says so. Physical side: see [Where the beams came from](#where-the-beams-came-from) |
| Vortex PC-64 LED S | No manual found anywhere - searched again on 2026-09-01 (manufacturer, Spanish shops, manual sites, second-hand ads, all spellings): "Vortex" as a stage-lighting brand has no web presence, so the name is the owner's label on a rebadged can. Generic 5-channel PAR64s come in **three incompatible layouts** - `R, G, B, Dimmer, Strobe` (what the definition says), `R, G, B, Dimmer, Strobe` plus macros in an 8-channel mode, and Stairville's `Mode, R, G, B, Speed` with no dimmer or strobe at all, whose 290 x 260 mm body is uncomfortably close to this one's 292 x 266 - so paper cannot settle it. The hand-built show strobed them on channel 5 and the owner saw them flicker, which fits the first layout and not the last. Only the channel probe on one can settles it |
| Stairville LED Bar 240/8 RGB | **Verified against `Manual/Stairville Led Bar 240.pdf`** on 2026-09-01 (7.7 and 8): the 24-channel mode is red, green, blue per segment, eight segments in order, exactly as QLC+'s own definition declares it, and the technical data matches - 240 LEDs in eight segments, 30 degrees, 36 W, 1064 x 88 x 65 mm, 2,6 kg. The other three modes (2, 3, 5 channels) are the bar's own programmes or one colour for the whole bar; 24 is the only one that gives the matrices eight cells. The definition is QLC+'s, not vendored |
| Stairville AF-150 (fog) | **Manual in `Manual/`** since 2026-09-01 (Thomann's v7 of 2023, EN and ES). One DMX channel, 0-255 fog output, nothing else - so patching it as QLC+'s `Generic Smoke / Amount` is exact, and QLC+'s own `Stairville AF-150 / 1ch` differs only in the name and the physical block. The manual gives no dead band and no ready signal over DMX: 0 is "no fog", and whether it is warm is a green LED on the wired remote |
| Mac Mah MAC WASH 1915Z | Manual in `Manual/` (official, six languages): channel table and menu, no ranges. **Zoom, strobe and reset ranges verified against ChamSys MagicQ's personality on 2026-09-02** (Fixture Finder ids 46510/46511 - the search of other programs' fixture libraries was the owner's idea, and it was the only place that had this unit). The zoom ran backwards in the first definition; see the MAC WASH paragraph at the top of this page. The Function mode channel's "0 = DMX" is still a platform guess |
| Generic LED Spray Fog (humo vertical) | Verified against the scanned leaflet and its clean twin, the Audibax Geyser 2000 RGB manual (same OEM map), both in `Manual/` - see [the four vertical fog machines](#the-four-vertical-fog-machines-replaced-the-spare-2026-08-29) |
| LED Beam Mini | **Channels 9-16 settled on 2026-09-02 off three agreeing sources** - the Betopper/Big Dipper LM108 manual, the SHEHDS 12x12W manual and ChamSys MagicQ's LM108 personality (id 10327), all of which share our first eight channels exactly - as `Pan/Tilt speed, Colour macro, Macro speed, Built-in program, Program speed, Pan fine, Tilt fine, Reset (150-255)`, with the strobe 0 = open and 1-255 slow to fast. The body in the definition (310 x 210 x 365 mm, 6,7 kg) is an Oukaning 36x3W RGBW listing to the millimetre, so the "single 70 W LED" is a placeholder and the unit is not a mini. The show writes the programme channel to 0 with every colour (`mode_park`) and the fine channels to 0 with every aim; nothing else of 9-16 is written, and 0 is the inert band on all of them. The fine channels sit at 14 and 15, not beside the coarse ones, so the Mini is on the 8-bit side of `efx_16bit` with the beams and every wash figure is now a 16-bit EFX plus an 8-bit one under a Collection. The channel probe on site is what promotes this from "the OEM's chart" to "this unit's": walk 9 to 16, 10 above 10 should override the colour, 16 at 150 should reset |

### The CLB2.4's beam angle was missing

QLC+'s own definition carries `<Lens Name="Other" DegreesMin="0" DegreesMax="0"/>`
and the manual gives the beam angle as **30 degrees** (8, Datos tecnicos). Zero
is not "unknown" to the 3D view: `MainView3D` reads
`focusMin = phy.lensDegreesMin() ? phy.lensDegreesMin() : 10` and
`focusMax = ... : 30`, so a fixture with no lens data is drawn as if it had a
10-30 degree zoom. The bar came out with a narrow, zoomable-looking cone instead
of the fixed 30 it really has.

Fixed by vendoring the definition into `QLC+ Fixtures/` with
`DegreesMin="30" DegreesMax="30"` and nothing else changed - the user fixture
folder takes precedence over the bundled library, so installing it is the same
step as for the other seven. Worth sending upstream.

### Where the beams came from

The four beams were bought on AliExpress on **2024-08-20**, order
`3040202209874050`, four units for **1.070,34 €** (~267 € each). The listing is
`Haz de luz de escenario 7R ... 1PCS 230W 7R Beam`, and it has since been
delisted; its product image survives at
`https://ae01.alicdn.com/kf/S213c94a06db2438db482281ea8adc4089.jpg` and shows a
full-size Sharpy clone with the **8+16+24 prism**. The order mail is the only
record - AliExpress order mails link to the order page, never to the product, so
there is no item ID to go back to.

That image plus our own definition (17 gobos + open, 14 colours + open, pan 540,
tilt 270, 16 channels) matches the **ERA Lighting 230W 7R Sharpy Beam** spec
exactly, which is where the body dimensions now come from: **330 x 390 x 490 mm**,
mapped into the definition as `Width="390" Height="490" Depth="330"` (the tall
axis is the one that matters - QLC+ scales the 3D mesh to these numbers).

What was there before was `Height="40"`, which drew the four beams as flat
slivers in the 2D and 3D views. Sources that agree on the body shape for this
class: 350 x 320 x 505 mm / 20.1 kg, 410 x 290 x 510 mm / 15.7 kg, and beamZ's
lighter Tiger 7RC at 280 x 240 x 470 mm / 11.5 kg. Width and depth are within
60 mm of each other across all of them and are invisible at this scale; the
height is not.

### What the beam definition had wrong

The channel *order* is still only as good as the seller's chart, but everything
around it has been corrected against QLC+'s own schema and its Clay Paky Sharpy
definition, which is the same class of fixture:

- **`Height="40"`** in the physical block drew the four beams as flat slivers in
  the 2D and 3D views. Now 390 x 490 x 330 mm - see above.
- **The maintenance channel was machine-translated.** "Quench" is the lamp being
  put out and "Bubble" is it being struck: 100-105 is **lamp off**, 106-205 is
  lamp on, 206-255 is reset. Nothing on the console said that sending 100 to
  channel 16 kills a 230 W lamp mid-show. They now carry QLC+'s `LampOff`,
  `LampOn` and `ResetAll` presets and say so in words.
- **The gobo thumbnails pointed at `~/Desktop/Gobos/`**, a folder that no longer
  exists on either machine. The images live in
  `QLC+ Setups/Gobos/BEAM-LIGHT-230W-7R/`; the definition now names them
  relatively (`BEAM-230W-7R/Gobo1.png`), which QLC+ resolves against its own
  Gobos folder - see [qlcplus-environment.md](qlcplus-environment.md).
- **Presets that did not match their own labels**: prism rotation was
  `RotationIndexed` ("park at an angle") on a range labelled "forward slow to
  fast", the shutter's open and closed ranges carried no preset, and the gobo
  wheel's two rainbow ranges were unmarked where the colour wheel's were not.
- **`Res1="0"` on the prism** - that field is the facet count, and the unit has
  an 8-facet prism.
- **Lamp figures**: the Osram Sirius HRI 230W datasheet gives 9500 lm at 8000 K,
  not the 23000 lm / 8500 K that was there. Beam angle follows QLC+'s Sharpy:
  a fixed 3.8 degrees, not a 0-5 degree PC lens. `PowerConsumption` stays at the
  lamp's 230 W, which is the convention QLC+'s own definitions use.
- **"Invalid"** as a capability name became "No function", QLC+'s own word.

One thing deliberately *not* changed: **Prism Rotation stays in the `Speed`
group**, where QLC+'s Sharpy would put it in `Prism`. The toolkit resolves roles
from the channel group, and a second Prism-group channel with more labelled
ranges than the prism itself would capture the prism role and make
"Prisma Animacion" drive rotation instead of insertion.

The Vortex PC-64 also carried `Weight="0"`, which QLC+'s schema rejects; it is
now 3 kg, an estimate for a LED PAR of that size and used for nothing but the
fixture list.

### A dimmer at full is not a light that is on

The four beams have a **mechanical shutter on channel 6, shut at DMX 0**, and
the two MiN Wash keep their whole intensity on a shutter-style channel with no
separate dimmer at all. Raising the dimmer does nothing for either. The
hand-built show knew it - `Luz ON Cabezas` sends 255 to the beams' channel 6 and
`Luz OFF Cabezas` sends 0 - and the generators did not, so every generated
colour, gobo and dimmer scene left six of the twelve heads dark.

It stayed invisible because QLC+ could not tell either: the definition's
"Closed" range carried no preset, so the 3D view drew light the rig would never
have produced. Tagging it `ShutterClose` made the preview honest, and the
darkness it then showed was real.

`shutter_open_pairs` reads the open value out of the definition - the range
marked `ShutterOpen`, or failing that one named "open" - and every generator that
raises a dimmer to make a fixture visible now opens its shutter too. Fixtures
whose shutter channel is a strobe and nothing else, which is every LED PAR here,
are left alone.

### Settling the unverified ones

`qlctool probe <show> <fixture-id> --base "7=255" --buttons` builds one scene per
DMX channel of that fixture plus a walk chaser: press play and write down what
each channel does. `--base` holds a dimmer open, since a head with a mechanical
shutter shows nothing otherwise.

Before the probe, the fixture libraries of other programs are worth an hour
(2026-09-02, the owner's idea): a personality is somebody's reading of the
manufacturer's chart, ranges included. ChamSys MagicQ's Fixture Finder
(`secure.chamsys.co.uk/fixturefinder`, an open JSON endpoint at `lib.php`
taking `manufacturers` and `fixturename`) had the MAC WASH 1915Z and the Mini's
OEM; Open Fixture Library (722 fixtures), Freestyler (2,040 profiles),
DMXControl's DDF API (1,536 devices), Avolites (metadata only, binaries behind
a 404) and Daslight/Sunlite (no public search) had neither. Match on channel
*order*, never on a name - these units are sold under a dozen names each.
