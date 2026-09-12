# How the show is run

**Almost nobody operates these lights.** The laptop is left alone at the venue
and the show has to keep changing colour, movement and gobos by itself. Most of
what follows comes from that.

The exception is a handful of moments a night, when somebody who is *not* a
lighting operator walks up to the laptop because something happened: a speaker
climbs on stage, the room goes quiet, the last track needs everything at once.
The console is built for those two audiences and nobody else - see "The
console" below.

## Consequences for how the show is built

- **One thing to press.** `AUTO` is a Collection of four things: the rig-wide
  colour wheel, the pixel groups' matrix cycle, the smoke timer, and
  `Ciclo Energia` - the chaser that walks the night through its energy levels.
- **One fixture, one colour source.** RGB channels mix HTP, so a fixture told
  red by one function and blue by another comes out magenta, and a third source
  makes it white. The bars and the panels belong to their matrix; the rig-wide
  wheel lights everything else and is generated with those fixtures excluded.
  That is why the matrix cycle sits in `AUTO` beside the colour wheel and not
  inside an energy level: a level that owns the bars' colour hands it back on
  every step, and two levels running at once put two colour sources on one
  fixture. Which is exactly what the old console let somebody press.
- **Nothing here is trusted to stay true by itself.** Every rule in this
  section is a rule `qlctool check` enforces over every button on the console -
  see [checks.md](checks.md). The show ran on luck until it had one.
- **A fixture with no RGB has to be written to on purpose.** The four BEAM
  230W 7R carry their colour on a wheel, so every generator built on
  `color_scene_values` skipped them: it looks for a red channel and moves on.
  `Blanco Total` and the two flashes left them black - not dimmed, never
  written to - until they were given the wheel position nearest the colour plus
  their dimmer *and their shutter*, which is what `wheel_color_values` does.
- **A colour bank colours its whole group, wheels included.** The beams sit in
  the Cabezas group, so "the heads are red" has to reach them too; a bank that
  colours the fixtures with red channels and skips the four with a colour wheel
  leaves them on last night's magenta.
- **A fixture that animates itself is left to.** The four panels carry 42
  built-in effects behind a mode channel; under `AUTO` and the lively moments
  they run `Ciclo Paneles` rather than taking the rig's colour, because in that
  mode they ignore red, green and blue anyway. Every colour look drives the mode
  channel back to off, so anything that means to colour them can.
- **A group is a picture, not a container.** An RGBMatrix paints one grid
  across every head of a group, so two kinds of light in one group are two
  halves of one picture - and the half that occupies fewer columns is dark
  whenever the sweep is elsewhere. The two LED bars, the four wall panels, the
  moving heads and the PARs each have their own group and their own grid, sized
  exactly to what is in it.
- **An effect gets time to finish.** An RGBMatrix walks a fixed number of
  frames that depends on the script and on the grid - a Fill over the eight-wide
  bars is eight of them, a Waves is twelve - so the cycle holds each one for a
  full pass at its own speed rather than for a flat two seconds. Cutting a Fill
  in half is what made the bars light halfway, jump colour, and light halfway
  again all night.
- **The unattended cycle carries no strobe.** The `Strobe` matrices are still
  generated and still on the console; they are simply not among the steps of
  `Ciclo Matrices`. A strobe is a button somebody holds - the same rule the
  shutter strobes already followed - and six of them rotating through a cycle
  is what the room read as "the pixels are off half the time".
- **A matrix writes RGB and nothing else.** The HYULIGHTS panels keep a master
  dimmer on their first channel and a shutter on their fifth, and no matrix
  touches either. The rig-wide wheel used to open them by accident, on every
  step; taking those fixtures off the wheel took that away too and left them
  coloured and dark, lit only under a flat scene like `Flash 100%`. `Pixeles
  ON` holds their intensity open and carries no colour at all, and it travels
  everywhere the pixel cycle travels - into `AUTO` and into every moment that
  runs one.
- **The night goes somewhere.** Every professional room is built as a handful of
  looks per energy level, and moves between them; strobes, fast movement, prism
  and big chases are held back for the peak, because a rig that spends
  everything in the first minute has nowhere to grow. `Ciclo Energia` steps
  `Nivel Ambiente` (4 min) -> `Nivel Fiesta` (8) -> `Nivel Peak` (40 s) ->
  `Nivel Fiesta` (8), a wave rather than a ramp - Peak is a burst, because two
  continuous minutes of fast movement and prism stop reading as a peak at all.
  The colour bed, the pixels and the haze stay **outside** the cycle, which is
  what keeps a level change from blacking the room out. A level carries
  movement, gobos, prism, the dimmer chase **and its own intensity base**
  (`Intensidad Ambiente` low, `Intensidad Total` full; since 2026-08-27 the
  colour scenes own no dimmers, so a level change really is a brightness
  change) - never colour.
- **A level is not a button.** `Nivel Ambiente`, `Nivel Fiesta` and `Nivel Peak`
  are what the cycle steps; they have no button at all. Pressing one by hand
  gave that level two owners and left the other one running underneath, which
  is how the room ended up on every colour at once. What a person presses
  instead is a *moment*.
- **A moment is a takeover, not a layer.** `Momento Charla`, `Momento
  Tranquilo`, `Momento Fiesta` and `Momento Locura` each bring their own colour
  bed, because the console stops `AUTO` the instant one starts and gives the
  room back when `AUTO` is pressed again. `Charla` is the one with nothing
  moving in it: warm white, heads parked, no wheel, no matrix - the state where
  change is the enemy.
- **Ambiente is alive, slowly.** The first cut parked every head at centre for
  four minutes, and pressing AUTO looked dead - "el auto es eso, como el modo
  auto de las cabezas en si" (owner, 2026-08-27). `Movimientos Suaves` is the
  Collection that starts both slow chasers: `Suaves Washes` carries the wide
  wash shapes and `Suaves Beams` keeps the needles moving too. The gobo wheel
  is parked open, and the room sits on the low intensity base. Total stillness
  belongs to `Charla`, on purpose.
- **Movement is per optics family.** A wash's soft wide beam and a 7R needle
  cannot share one geometry: `Movimientos Washes` runs bigger and slower than
  `Movimientos Beams` (which carries the fan as a rest step), and the Peak
  pair `Rapidos Washes` / `Rapidos Beams` doubles the pace, each at its own
  size. `Movimientos Cabezas` and `Movimientos Rapidos` remain the one-press
  names: Collections over the family chasers.
- **Everything that cycles is `RunOrder="Random"`.** A fixed order reads as a
  loop within a couple of minutes when nobody is intervening.
- **Smoke runs on its own timer** - a burst, then a long wait, forever - and is
  driven from nowhere else.
- **The rig changes colour together.** `Rueda Colores` is one wheel over every
  colour-capable fixture, not one wheel per group: three Random wheels never
  land on the same colour, and what the room saw was the heads on magenta while
  the PARs were on green. Most of its steps are the whole rig on one colour;
  five are the movers against everything else, so there is contrast on purpose
  rather than by drift.
- **A matrix cycle only runs under AUTO where a group is really pixels.** A
  matrix paints its own group's colour, so a cycle over the heads and another
  over the PARs desynchronises them again. The bars and panels keep theirs -
  they have cells to draw across - and the heads and the PARs take their colour
  from the wheel.
- **The beams' colour comes from the same wheel.** They have no RGB, so a colour
  scene could not reach them and `Color Beam Animacion` - which started after
  the colour wheel and therefore won their one colour channel - had them on a
  colour of their own all night. The rig-wide scenes now put that wheel on the
  position nearest the colour they paint (White, Yellow, Red, Blue, Green, UV,
  Orange, Pink), and the animation is a button rather than part of `AUTO`.
- **Colour range comes from mixing.** The strongest looks in the hand-built show
  are two-colour: odd fixtures on one colour, even on the other ("Rojo / Azul"),
  stepped through by a mix wheel. Solid washes alone look thin.
- **The palette is the show's own.** 18 colours, mined from every RGB triple the
  hand-built scenes drive plus its matrix colours - which is why values like
  (255, 0, 100) and (160, 0, 255) are in it.

## The generated show

`qlctool newshow` builds all of it on the existing patch. Structure:

- Base looks: `Blanco Total`, `Todo Negro`, `Flash 100%`, `Flash 50%`, and
  `Pixeles ON` - the intensity of the pixel groups, whose colour is their
  matrix's. One
  white, not three: `Luces ON`, `Todo Blanco` and `Flash 100%` were all full
  white on the same fixtures, which is why nobody could say what the difference
  was - there was none. What is left is a latched work light (`Blanco Total`)
  and a held hit (`Flash 100%`)
- Rig-wide colour: a scene per colour over the whole patch, five
  movers-against-the-rest contrasts, and two `Rig Multicolor` wild steps -
  every fixture its own palette colour, the beams on their colour wheel's
  rainbow scroll, the bars under a rainbow plasma - all on the Random
  `Rueda Colores`, so the crazy look appears now and then on the one clock
- The panels' phase cycle, `Ciclo Paneles Mixto`: their own 41 programmes for
  eight minutes, then four in manual listening to the wheel's RGB - the wheel
  writes their colour on every step all night, the cycle only decides whether
  they are hearing it (one colour clock, one mode owner)
- Per fixture group: a bank of solid colours, 30 two-colour mixes, a
  `Rueda Colores <group>` and a `Rueda Mezcla <group>`, both Random
- Matrix effects per group (algorithm x colour) with a cycle chaser
- Movement per family: wash EFX and beam EFX per shape, phases spread evenly,
  each family on its own Random chaser, plus the slow wash pair for Ambiente
  and the fast pair for Peak - the speed lives on the EFX, not on the chaser
  that steps it. The pro figures rotate among the shapes: `Ola Vertical`
  (the tilt wave - Line at width 0, Serial cascade), `Barrido Unison` (the
  synced push - every head in phase, the mirror making the sides meet), and
  the two beam rests, `Beams Abanico` (the fan) and `Beams Cruce` (the X)
- `Cabezas Centro`, `Intensidad Ambiente` / `Intensidad Total`, and the four
  energy levels with `Ciclo Energia` over them - the way down from the peak
  is `Nivel Fiesta Dinamico`, party movement with the dimmers taking turns
  between the running chase and the odd/even ping-pong (`Dimmer Programas`)
- `Luz Charla` and the four moments over the pieces above
- The beams' gobo wheel (20 positions), colour wheel (17) and prism, used the
  way a lit room uses them: gobos are texture in the haze from `Nivel Fiesta`
  up (parked open in the quiet levels), the shake bursts (`Gobo Shake`, the
  Pattern Jitter channel) are steps of the gobo wheel's own rotation, and the
  prism runs from `Nivel Fiesta` up - inserted spinning (every prism scene
  drives the rotation channel too) and parked out by `Prisma - None` in every
  level and moment that does not run its animation, so a prism never outlives
  the block that put it in. Since 2026-08-30 the wheel is used the way a
  professional room uses it rather than the way a generator can: the four
  heads are **dealt** different patterns (`Gobo Repartido 1-8`, one seat apart
  each, riding inside the gobo wheel's own rotation), every gobo scene states
  the **focus** channel that nothing had ever written - seventeen patterns
  projected at one end of its travel is most of what "se echaba en falta más
  variedad" was - and the prism dance ends on the other two things one
  rotation channel can do, `Prisma Giro Rapido` and `Prisma Giro Inverso`
- `Humo Auto`, and the three other rhythms beside it
- `Rueda Mezcla`, a collection over the per-group mix wheels, and `AUTO` over
  the colour wheel, the pixel cycle, the haze and the energy cycle

## Symmetry: one side runs backwards

With every head going the same way round a path, a circle sweeps the whole room
in parallel. The rig reads as designed when the pairs open and close together,
and the way to get that is to reverse the fixtures on one side of the centre
line - `x_rot` and pan invert are not involved, the EFX carries a `Direction`
per fixture. `house_right_fixture_ids` reads the sides off the plot's own
positions, so a re-hang changes the mirror by changing the plot. Today that is
CromoWash #2 and beams 21 and 23.

## Running on the music's beat

The show runs on the clock, and one dial re-times it. `Tempo Show` sits on
page 1: tap `M` to the music and the colour wheel, the gobo and colour-beam
animations, the prism and the dimmer pulse all follow. The dial's time is one
tap, and each layer carries its own **multiplier** - how many taps it is worth
(`VCSpeedDial::applyFunctionsTime` computes `duration = time x multiplier`).
That multiplier is the whole trick: give every layer the same one and a single
tap makes the wheel, the prism and the dimmer exactly as long as each other,
which is what "se vuelven todos los programas locos" was (owner, 2026-08-29).
`qlctool check` refuses a flattened dial (`tap que aplana los programas`).

The head movement has a **second dial**, `Vel. Movimiento` on page 3, bound to
the same `M`: a key press reaches every widget bound to it
(`VCPage::handleKeyEvent` walks all matches), which is how the hand-built
console drove three dials from one key. It is separate because its numbers
are - a shape is sixteen taps where a colour is eight - and because it has to
re-time three things at once: the rotation, the EFX under it, **and the
crossfade**. QLC+ subtracts a chaser's fade from its EFX's own duration to get
the figure it draws (`EFX::loopDuration`), so a fade left at fixed
milliseconds stops the figure being a proportion of its step. Both dials also
sit on the SMC-PAD's encoders 2 and 3.

`Movimientos Suaves` is off the dial on purpose: its two slow chasers hold
one shape for a minute, which is not something anybody taps.

Two traps found on the show Mac's own QLC+ 5.2.2 the same night, both now
rules:

- **`ControlBPM` does not exist in 5.2.2.** A speed dial that drives the
  global BPM instead of its functions is a QLC+ 5.3 feature; 5.2.2 says
  "Unknown speed dial tag: ControlBPM" when it loads one and ignores it, so
  the tap does nothing. A tap key needs functions under it
  (`tap que no re-tempa nada`).
- **A chaser in Beats hands its fade to its steps as a raw number.** An EFX
  subtracts that from its own millisecond duration
  (`EFX::loopDuration() = duration() - overrideFadeInSpeed()`), so a movement
  chaser on Beats with a 10-beat crossfade turned a 16 s head sweep into a
  6 s one: "las cabezas van super rapido y no completan los giros". Beats is
  therefore only for chasers whose steps are Scenes
  (`unidades de tempo cruzadas`), and a Collection may not carry a `<Tempo>`
  at all - it has none, and QLC+ says so (`tempo en una coleccion`).

### When a newer QLC+ arrives

`qlctool newshow --bpm-tap` builds the show the way it *should* be built once
QLC+ supports `ControlBPM`: every music-following layer in **Beats** tempo
over an Internal generator, and page 1's tap driving the global BPM instead of
writing durations. Then no layer needs a multiplier at all - each states its
own beat count and one clock moves them together. It is a separate build
because 5.2.2 loads it and silently does nothing (the dial's tag is unknown to
it, and a tap would re-time neither the BPM nor any function). Movement stays
on the clock even there: a Beats chaser corrupts an EFX, whatever version is
reading it.

`qlctool newshow --beats` builds the audio-driven variant: the layers whose
steps are Scenes, plus the matrix cycles, go on QLC+'s **Beats** tempo with
the beat generator set to **Audio**, so a laptop left alone in a venue runs
its chases on the room's own music (`Vibra-beats.qxw`). An audio input has to
be picked in QLC+'s Configuration - the device is an application setting, not
part of the workspace, and with no input selected the beat never ticks. The
energy cycle stays on the clock everywhere: it measures the night rather than
the song, and a beat that never arrives must not be able to freeze it.

## The console

Built to a fixed **1440x900** - the show laptop's screen - so nothing scrolls
and nothing is off the edge. It is one multipage frame with four pages, and
the pages answer four different questions. `PgDn` and `PgUp` change page; the
arrows in the frame header do the same.

### Page 1 - Show

The only page the person who is *not* a lighting operator ever needs, and the
only one built with big buttons and sentences on them.

| Frame | What is in it |
| --- | --- |
| `LA SALA ESTÁ ASÍ` (solo) | `AUTO` at a quarter of the screen, the four moments, `BLANCO TOTAL` (work light) and `TODO NEGRO`. Exactly one runs at a time |
| `GOLPES` (plain) | `FLASH`, `FLASH LENTO`, `FLASH COLOR`, `HUMO YA`, `STROBO`, `STROBO SUAVE`, `COLOR BEAM`. These add to whatever state is running |
| `SI ALGO VA MAL` | `PARAR TODO` - a `StopAll` button with a 1 s fade, driving no function of its own. `APAGON` - a `Blackout` action, and it latches: the first press forces every output to zero regardless of what is running underneath; the second press lifts it and gives that back. AUTO does nothing while the room is blacked out - it has to be pressed after the second `APAGON`, not instead of it |

Every button on this page carries its own key in its caption (`AUTO — el show
se lleva solo · Q`), and five lines of plain Spanish under the frames say what
the two halves of the page are for. Nobody reads a key map at a venue.

**The solo frame is the fix, not a detail.** A solo frame stops every other
widget's function as soon as one starts, so putting `AUTO`, the moments, the
work light and the blackout in one makes "Ambiente and Fiesta at the same time"
unpressable. `ExcludeMonitored` is on, so a button only stops its function when
that button started it or when the function is the workspace's startup function
- which is what lets an autostarted `AUTO` still be taken over by a moment.

### Page 2 - JUGAR

The operator's family picker: use it to take one part of the look without
building a new state. Its reset strip has `AUTO`, the four moments, `BLANCO
TOTAL`, `TODO NEGRO`, `Flash 100%`, `Flash Color`, `Humo ON` and `Strobo
Rapido`. `Escape` and `Backspace` are global controls rather than duplicated
here; use `AUTO` twice if it is already green, or `Backspace` then `Q`, to
return completely.

| Frame | Hook first | Picks |
| --- | --- | --- |
| `COLOR` | `AUTO colores`, `Rueda Mezcla`, `Luz Charla` | wheel colours and both rainbows |
| `PIXELES` | `AUTO paneles`, `Paneles Charla` | twelve panel effects and `Paneles Manual` |
| `CABEZAS` | `AUTO lento`, `AUTO normal`, `AUTO rapido`, `Centro` | movement figures, fan, cross and stage aim |
| `GOBOS` | `AUTO gobos`, `Reposo` | gobos, dealt gobos and shakes in two inner pages |
| `PRISMA` | `AUTO prisma`, `Reposo` | all prism positions and rotations |

Every family is a `SoloFrame`: pressing a pick stops that family's AUTO hook,
and pressing its hook releases the pick and gives the family back to the room
state. The hooks are the state-owned interfaces, not extra looks: `Luz Charla`
is a Collection over its warm base and the beams' white wheel position.
`Paneles Charla` is the separate PIXELES hook: it sets only the programmed
panels' manual/off programme mode. Its intensity bases (`Intensidad Total` and
`Intensidad Charla Pixeles`) belong directly to `Momento Charla`, outside the
COLOR and PIXELES frames, so pressing a pick cannot turn the talk look black.
`Pixeles ON` leaves programme mode to `Ciclo Paneles Mixto` on those panels,
while continuing to park the mode of other matrix-lit fixtures. A state change
(`Q`, `F1`-`F4`) also brings its own family choices back.

Pressing an active pick again stops it without restarting the hook, so that
family stays still until its AUTO or a room state retakes it. Stopping the rig
colour-wheel hook aborts its 800 ms crossfade; the pick enters over the outgoing
scene's fade-out rather than as a hard cut.

A Toggle button monitors its function whoever started it and reports the start
to its SoloFrame (`VCButton::slotFunctionRunning` ->
`VCSoloFrame::slotFunctionStarting`), while the button's own stop clears every
source (`Function::stop`, `ManualVCWidget`), so a pick takes one family away
from a running Collection without stopping that Collection.
Duplicate Toggle buttons for one function both light (starter green, monitor
orange), and `Blackout` is the only button that must not be duplicated, which
is the basis of the `consola` rule change.

The color and pixel picks are one-member Collection wrappers, rather than the
state-owned leaf functions themselves: the SoloFrame can stop the wrapper
without a room state later starting that same pick again. They stay until their
family hook or a new room state releases them. Under AUTO, a head, gobo or
prism pick can be recovered by the energy cycle at its next step (up to eight
minutes); take a Moment first for a long manual look. `TODO NEGRO` is a normal
Toggle Scene, so its zero values remain HTP and do not use `ForceLTP`; use the
global `Backspace` panic control when an immediate stop of every running
function is required. The seven global JUGAR hooks keep their letters; picks
and reset-strip duplicates have no keyboard keys. The colour hits above the families are held `Flash`
buttons with `Override` and `ForceLTP`; they replace the running colour only
while pressed and never mix red over cyan into white.

### Page 3 - Control

For somebody who does know the rig: the direct controls that remain useful
beside JUGAR. The colour bank per fixture group is on keys 1-0 (with the colour
named on the button), alongside the XY pad, `Vel. Movimiento`, the dimmer
looks, fixture strobes, the `Master General` slider (the workspace's own
GrandMaster, scaling every output under whatever is already running),
`Humo Vertical`, held beam-colour picks, and the audio triggers.

**The colour banks and held beam-colour picks are held, not latched**
(2026-09-02). Red, green and blue are Intensity channels and QLC+ mixes them
HTP, so a latched bank on top of a running state never showed its colour: AUTO
on cyan plus key `1` was *white* on twenty-seven fixtures. A Flash button with
**Override** puts its fader after every fader the state starts, and with
**ForceLTP** writes even RGB as LTP (`Scene::writeDMX`, `forceLTP=true` skips
the compare). Hold `1` and the heads are red - not red plus cyan - and release
it to restore the state's colour in the same frame.

### Page 4 - Librería

The material the show is built from, not buttons for a set: the two-colour
mixes, the matrix effects, the per-group wheels and matrix cycles, the
`MultiColor BEAM` looks (the beams' continuous half-colour channel - two
colours in one beam - per beam and per mirrored pair, the old console's
"Multi Color"), the panels' forty-two built-in effects, and beside those a
`Vel. Paneles` fader - a Level
slider over the four panels' speed channel, the hand-built console's "Strobo
LED Effect Speed". The channel is in the Speed group, so it is LTP, not HTP:
the fader *monitors* the running value (the cycle's 200) until somebody moves
it, and from then on its Override fader wins outright - at zero too, which is
the slowest, not "the cycle's" - until the red reset X hands the channel back
(`VCSlider::writeDMXLevel`, 2026-09-02). The two-colour mixes on this page
are held with ForceLTP like the banks, for the reason given on page 3. The two
multipage frames inside carry a label per page naming the group, because three
pages of identically captioned buttons is not a page count, it is a guess - and
the page carries a paragraph saying what it is for, because 180 buttons
otherwise read as something somebody is supposed to be using.

Two rules shape all four pages:

- **A function and the functions it starts never share a solo frame** - except
  where that is the point, above. A Toggle button reports its function starting
  however it was started, so a master in the same solo frame as its own members
  dies the instant it starts them. Masters and chasers live in plain frames.
- **What does not fit goes on a page, not below the fold.**

## Keyboard

The night-running looks keep the letters the hand-built show had, so muscle
memory carries over. The moments are on `F1`-`F4`: a row of their own, and the
only keys that cannot collide with a colour bank on 1-0.

| Key | Function | Where |
| --- | --- | --- |
| `Q` | AUTO | page 1 |
| `F1` | Momento Charla | page 1 |
| `F2` | Momento Tranquilo | page 1 |
| `F3` | Momento Fiesta | page 1 |
| `F4` | Momento Locura | page 1 |
| `X` | Blanco Total | page 1 |
| `º` | Todo Negro | page 1 |
| `Space` | Flash 100% (Flash - white, shutters strobing fast) | page 1 |
| `-` | Flash 50% (Flash - same white, half the strobe speed) | page 1 |
| `.` | Flash Color (Flash - strobe over the running colour) | page 1 |
| `H` | Humo ON (Flash - the burst, held) | page 1 |
| `F` / `T` | Strobo Rapido / Medio (Flash - every shutter strobing, fast / slow) | page 1 |
| `C` | Color Beam Animacion | page 1 |
| `Backspace` | PARAR TODO (StopAll) | page 1 |
| `W` / `E` | Rueda Colores / Rueda Mezcla | page 2 |
| `A` | Movimientos Cabezas | page 2 |
| `G` / `P` | Gobo Animacion / Prisma Animacion | page 2 |
| `'` / `¡` | Arcoiris Simultaneo / Arcoiris Pasos (relative RGB rainbows) | page 2 |
| `1`-`0` | held colour banks | page 3 |
| `J` | Humo Auto (the haze timer; the rhythm row is on page 1) | page 1 |
| `V` / `B` | Dimmer Chase / Dimmer Chase 2 (the sweep, each way) | page 3 |
| `Z` / `K` | Dimmer PingPong / Dimmer Secuencia (rotation of the three) | page 3 |
| `S` / `D` | Strobo ON / OFF (shutter) | page 3 |
| `M` | tap tempo on `Tempo Show` (tap the beat, every layer follows) | page 1 |
| `PgDn` / `PgUp` | next / previous page | anywhere |

Keys 1-0 are on every colour bank: every widget sees every key press, so `1`
lights red on the heads, the bars and the PARs at once - for as long as it is
held (the banks are Flash buttons with ForceLTP, see page 3). As on the hand-built
console, `9` and `0` are not solids: they are the alternating `Azul / Rojo`
and `Rojo / Azul` looks (restored 2026-08-28; Naranja and Rosa stay in the
bank as keyless buttons). **Every widget sees
every key press on every page too**, visible or not - which is why the page-1
keys keep working while page 4 is on screen, and why every button's key is
unique, checked by a test.

## The SMC-PAD

The hardware surface. Universe 0 carries its MIDI input patch, on the
`M-VAVE SMC-PAD` profile, in omni ("1-16") mode. Omni is not optional: on a
fixed MIDI channel QLC+ stops folding the channel into the input number and
every pad addresses the wrong control.

**Plugged into USB, the pad stops speaking Bluetooth.** Measured here
(`tools/smc-pad/README.md`): with the USB cable in, the pad routes its MIDI
over USB and the BLE side goes silent - so a workspace bound to `ble device`
hears nothing at all, and no amount of resetting the pad changes that. It cost
a whole show on 2026-08-29: "no pude usar el pad porque ni reseteándolo
reconocía las teclas", with the cable and Bluetooth both on. Either **unplug
USB** (which is also what the LED bridge wants - it holds the pad over BLE), or
point universe 1's input at the USB port in Inputs/Outputs and save the file.
`swift tools/smc-pad/midiports.swift` prints every port under the name QLC+
uses for it, next to the name macOS shows, which is the only way to tell which
line is which.

**Which port** is the machine's business, not the show's, and regenerating
leaves it alone. QLC+ names a MIDI port by its CoreMIDI `Model` property, which
is *not* the name macOS displays - so a port picked from a display name matches
nothing, QLC+ falls through to the saved line number, and the whole surface
goes dead. That happened on 2026-08-29, and it is why the generator now
preserves whatever port the file already names. Over Bluetooth the pad is
`ble device`, one port, unambiguous. Over USB it is three ports all named
`SINCO`, which QLC+ cannot tell apart by name - so on USB the saved line number
is doing the work and a re-pick in the Inputs/Outputs tab is the fix.

**If the pads do the wrong thing, reset the pad.** The show is bound to the
pad's *factory* map - MIDI channel 10, note 35 + pad number - so a factory reset
from MidiSuite puts the surface back exactly where the show expects it, with
nothing to configure afterwards. Verified 2026-08-29 by resetting and
re-measuring all four corners. That matters because `SHIFT` on this device is
not a modifier that sends MIDI: it edits settings that persist across a power
cycle. `SHIFT` + pads 1-8 changes preset, 13-14 transposes, 15-16 shifts the
octave - and a transposed or re-preset pad addresses controls the show has never
heard of, which looks exactly like a dead surface. The manual's full table is in
[`Manual/M-VAVE SMC-PAD - manual (transcripcion).md`](../Manual/M-VAVE%20SMC-PAD%20-%20manual%20(transcripcion).md).
Never press `SHIFT` on this pad to see what happens.

The pads are numbered as the panel prints them - PAD1 bottom-left, PAD13
top-left - and the layout is the owner's: the hits on the top two rows, the
room's states on the bottom two. The owner has also written it on the pads
themselves in marker (`Blan`, `Negro`, `Char`, `A`, `Fiest`, `Loc`, `Tran`,
`HV`, `H`, `ST`, `ST/SO`, `F`, `F/SO`, `F/C`, `C.B.A`), so the surface reads
correctly even with the LEDs dark. A photo of the panel is at
[`smc-pad-panel.jpg`](smc-pad-panel.jpg), and it is also where to check what
`SHIFT` does, because the device prints that above every pad too. Changing this
table means changing what is written on the hardware.

| | | | |
| --- | --- | --- | --- |
| **13** Flash | **14** Flash lento | **15** Flash color | **16** Color Beam |
| **9** Humo ya | **10** Humo | **11** Strobo | **12** Strobo suave |
| **5** AUTO | **6** Fiesta | **7** Locura | **8** Tranquilo |
| **1** Blanco | **2** Negro | **3** Charla | **4** *(libre)* |

The first column is the punch, the second the gentler version of the same
thing. Pad 4 is free on purpose, and the panic pair is deliberately **off** the
pads: `PARAR TODO` is the pause button and `APAGON` the record button, on the
right edge, where a missed hit cannot reach them. They are control changes, so
they answer on either bank. The arrows `<` and `>` page the console, and were
measured not to move the pads' bank while doing it. Knob 1 is the grand master,
knob 2 the tempo dial, knob 3 the movement dial.

**JUGAR lives on the second bank.** Press `PAD BANK` and the same top two rows
become the JUGAR hooks - Rueda Colores, Rueda Mezcla, Movimientos, Gobos on
the top row; Prisma, Humo Auto and the two rainbows under them. It was written
against `SHIFT` until a capture on 2026-08-29 proved SHIFT sends no MIDI at
all: it selects the functions silkscreened on the pads themselves (SWING,
LATCH, SYNC), which never leave the device, so those eight buttons had never
once fired from the hardware.

**The trap: the pad remembers its bank, the show does not.** A pad left on bank
2 at the end of a night comes back on bank 2, and the top rows will fire the
JUGAR layer where the page expects the hits. If the pads do the wrong thing,
press `PAD BANK`. `qlctool check` refuses a console bound to a control the pad
cannot send, but nothing in the file can see which bank the hardware is on.

The pad's LEDs are lit by a small daemon, over Bluetooth, in the same colours as
the console buttons - dim while idle, full-bright while the function runs. It is
separate from QLC+ because the LEDs are not MIDI at all; `docs/smc-pad-led.md`
is the whole story. On a machine that runs the show it is installed once with
`tools/smc-pad/install-bridge.sh` and starts at login, ahead of QLC+, which is
the order it needs: the daemon publishes a MIDI port and QLC+ binds to it when
the workspace loads.

Two consequences worth knowing at a venue. If the daemon is restarted, the pads
stop updating until the workspace is reloaded - the show itself is unaffected,
because the pad's *input* is a different path. And if the pads sit at a flat
colour instead of the show's palette, the daemon is not running: the LEDs are
its doing entirely, and a factory-reset pad is uniformly magenta.

## Intensity and strobes

Colour is not the only thing that moves. Four dimmer looks - the running chase
in both directions (an EFX in Dimmer mode, the fixtures spread around the path
so the peak runs along the rig; `Dimmer Chase 2` reverses every fixture, the
hand-built console's key B), an odd/even ping-pong, and `Dimmer Secuencia`
(key K - M went back to being the tap key, as on the hand-built console):
the old console's rotation of the three, twenty seconds of steady
full light between ten-second programmes, restored verbatim from
DeluxeEventos2's chaser - and four strobes.

The strobes come in two kinds because the rig does. A fixture with a shutter
strobes itself, and `Strobo ON` / `Strobo OFF` drive it. A labelled strobe
range is driven inside that range - guessing *within* a labelled channel is
how a head goes dark mid-set: a MiN Wash puts "Closed" at 1-7. A channel with
no labels at all whose whole job is the strobe - the Vortex PARs' and the
panels' channel 5 - is driven as a bare speed, because the hand-built show ran
exactly those channels at 250/255 for years and leaving them out is how
`Strobo ON` shipped strobing half the rig (2026-08-27). `Strobo Rapido` (`F`)
and `Strobo Medio` (`T`) are the held version of the same thing: a Flash scene
driving every strobe-capable channel fast or at the slow flash's speed, colour
and dimmers left to the state. They used to be chasers flipping the rig
between a white scene and a black one, and that never worked on a lit room:
the black step wrote zeros to dimmers and RGB, all Intensity channels, and
Intensity is HTP - under any state holding the dimmers at 255 the zeros lost
and the "strobe" was white over the room's colour with never a black between,
while the beams' colour wheel was sent to white and back every 125 ms
(cross-audit, 2026-09-02). The LED bars have no strobe channel of any kind,
and nothing in QLC+ can blink them to black on top of a lit state, so they sit
the strobes out.

The three flashes are the third kind: **a held flash is the strobe** on this
show. `Flash 100%` is full white with every shutter driven near the top of
its range, `Flash 50%` the same white at half the strobe speed - that is what
"50%" meant on the hand-built console - and `Flash Color` (`.`) raises every
dimmer and strobes every shutter *without writing a colour*, so the rig
strobes in whatever the running state has it wearing. The one flash that must
never strobe is `Golpe Graves`, the plain white twin the audio triggers'
bass bar presses: a strobe fired by whatever the PA does is a strobe nobody
chose, and `estrobo en manos del audio` checks it stays that way.

None of these is in `AUTO`. They are for somebody standing at the laptop: a
strobe running unattended all night is not a decision to make by default.

## Audio triggers

Five spectrum bands, one of them bound: the bass presses `Golpe Graves`, the
plain white flash on page 3 beside the triggers widget. A Flash button is the
right target for a bar, not the wrong one - a bar calls `pressFunction` on
the way up and `releaseFunction` on the way down, exactly how a Flash button
expects to be worked, so it lets go on its own the moment the level drops
rather than latching on for the rest of the night. It is its own scene rather
than one of the GOLPES for two reasons that both bit already: `Blanco Total`
sits in the room-state solo frame, so binding it there had the music killing
`AUTO` on every kick, and `Flash 100%` now strobes - a strobe fired by
whatever the PA does is a strobe nobody chose (`estrobo en manos del audio`).

The other four bands ship deliberately unbound - not a setting left for
somebody at the venue, an empty pairing the generator ships on purpose, so no
strobe or chase can be triggered by the room's own music with nobody
deciding when. Binding one is a decision to make at the venue with the real
music playing: the threshold and the target both need tuning by ear, and it
needs an audio input picked in QLC+'s Configuration first.

## Starting it without anyone there

QLC+ can do the last step itself: set a **startup function** (the green flag in
the Function Manager) to `AUTO`, and turn on **Project autostart** under
Configuration → System. Then powering the laptop on brings the show up with no
clicks. Command line does the kiosk half of that job too:
`qlcplus -k -f -o "QLC+ Setups/Vibra-split.qxw"` opens straight to the Virtual
Console (`-k`), fullscreen (`-f`), with the workspace loaded (`-o`) - no
clicks needed at the laptop. There is no `-p` to add to that on this build:
it was a v4-only operate flag, absent from the installed 5.2.2's option list
(confirmed against the real binary, see
[qlc5-verification.md](qlc5-verification.md)), and `-k` alone is what gets to
the console.

**Kiosk mode has no on-screen exit.** `App::createKioskCloseButton()` is an
empty stub in this build, so nothing on the screen closes the window; `Cmd+Q`
still does.

## The console on a phone

`-w` turns on QLC+'s own web server, on port 9999 unless `--wp <port>`
overrides it - `-w`/`--wp` confirmed on the installed 5.2.2, the default port
number read from the same engine source that grounds the rest of this repo's
QLC+5 claims (`webaccessbase.cpp`, `DEFAULT_PORT_NUMBER`). Add it to the
launch line: `qlcplus -k -f -w -o "QLC+ Setups/Vibra-split.qxw"`. Then, phone
and Mac on the same network, `http://<mac-ip>:9999` in a browser gets a touch
copy of the Virtual Console - useful for confirming a look while standing at
the rig instead of at the laptop, which is what most of the "confirm on site"
items in `TODO.md` are waiting on. The web build declares Button, Frame and
SpeedDial support (also Slider, XYPad, CueList, Clock, AudioTriggers), so page
1's frames and buttons, JUGAR's buttons, and page 3's two speed dials all come through - the
phone shows what the laptop shows, not a cut-down page.
