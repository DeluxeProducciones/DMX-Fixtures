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
  `Nivel Ambiente` (4 min) -> `Nivel Fiesta` (8) -> `Nivel Peak` (2) ->
  `Nivel Fiesta` (8), a wave rather than a ramp. The colour bed, the pixels and
  the haze stay **outside** the cycle, which is what keeps a level change from
  blacking the room out. A level carries movement, gobos, prism and the dimmer
  chase - never colour.
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
- **Ambiente is heads held still.** Stillness is a look, and a head nothing
  drives sits wherever the last effect abandoned it - often pointing at the
  ceiling - so the quiet level runs `Cabezas Centro` (mid pan, mid tilt) and the
  open position of the gobo wheel. Movement is a level, not a background.
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
- Rig-wide colour: a scene per colour over the whole patch and five
  movers-against-the-rest contrasts, on the Random `Rueda Colores`
- Per fixture group: a bank of solid colours, 30 two-colour mixes, a
  `Rueda Colores <group>` and a `Rueda Mezcla <group>`, both Random
- Matrix effects per group (algorithm x colour) with a cycle chaser
- Movement: one EFX per shape over the twelve moving heads, phases spread evenly
  around the path, on a Random 10s chaser - plus the same shapes at twice the
  speed (`Movimientos Rapidos`) for the peak, since the speed lives on the EFX
  and not on the chaser that steps it
- `Cabezas Centro`, and the three energy levels with `Ciclo Energia` over them
- `Luz Charla` and the four moments over the pieces above
- The beams' gobo wheel (20 positions), colour wheel (17) and prism
- `Humo Auto`
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

`qlctool newshow --beats` puts the layers that should feel the music on QLC+'s
**Beats** tempo - colour every 2 bars, matrices every bar, a movement shape
every 8 - and sets the workspace's beat generator to **Audio**, which derives
the beat from an audio input device. A laptop left alone in a venue then runs
its chases on the room's own music, with no operator and no MIDI cable.

Two things to know before using it:

- **An audio input has to be picked in QLC+'s Configuration.** The device is an
  application setting, not part of the workspace. With no input selected the
  beat never ticks and everything in Beats tempo waits forever, which is why the
  default build stays on real time and the beat-locked one is a separate file
  (`Vibra-beats.qxw`).
- **The energy cycle stays on the clock.** It measures the night rather than the
  song, and a beat that never arrives must not be able to freeze it.

## The console

Built to a fixed **1440x900** - the show laptop's screen - so nothing scrolls
and nothing is off the edge. It is one multipage frame with three pages, and
the pages answer three different questions. `PgDn` and `PgUp` change page; the
arrows in the frame header do the same.

### Page 1 - Show

The only page the person who is *not* a lighting operator ever needs, and the
only one built with big buttons and sentences on them.

| Frame | What is in it |
| --- | --- |
| `LA SALA ESTÁ ASÍ` (solo) | `AUTO` at a quarter of the screen, the four moments, `BLANCO TOTAL` (work light) and `TODO NEGRO`. Exactly one runs at a time |
| `GOLPES` (plain) | `FLASH`, `FLASH SUAVE`, `HUMO YA`, `STROBO`, `STROBO SUAVE`, `COLOR BEAM`. These add to whatever state is running |
| `SI ALGO VA MAL` | `PARAR TODO` - a `StopAll` button with a 1 s fade, driving no function of its own |

Every button on this page carries its own key in its caption (`AUTO — el show
se lleva solo · Q`), and five lines of plain Spanish under the frames say what
the two halves of the page are for. Nobody reads a key map at a venue.

**The solo frame is the fix, not a detail.** A solo frame stops every other
widget's function as soon as one starts, so putting `AUTO`, the moments, the
work light and the blackout in one makes "Ambiente and Fiesta at the same time"
unpressable. `ExcludeMonitored` is on, so a button only stops its function when
that button started it or when the function is the workspace's startup function
- which is what lets an autostarted `AUTO` still be taken over by a moment.

### Page 2 - Manual

For somebody who does know the rig: the layers, on top of whatever page 1 is
running. The colour bank per fixture group on keys 1-0 (now with the colour
named on the button), the wheels, the movement shapes, the beams' gobos and
colour-wheel positions, a pad over the twelve heads big enough to aim with, the
two speed dials, the dimmer looks, the fixture strobes, and the audio triggers.

The beams' wheels are here rather than in the library because picking a gobo is
a live decision: somebody does it while the show runs.

### Page 3 - Librería

The material the show is built from, not buttons for a set: 90 two-colour
mixes, 90 matrix effects, and the per-group wheels and matrix cycles. The two
multipage frames inside carry a label per page naming the group, because three
pages of identically captioned buttons is not a page count, it is a guess - and
the page carries a paragraph saying what it is for, because 180 buttons
otherwise read as something somebody is supposed to be using.

Two rules shape all three pages:

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
| `Space` | Flash 100% (Flash) | page 1 |
| `-` | Flash 50% (Flash) | page 1 |
| `H` | Humo ON (Flash - the burst, held) | page 1 |
| `F` / `T` | Strobo Rapido / Medio | page 1 |
| `C` | Color Beam Animacion | page 1 |
| `Backspace` | PARAR TODO (StopAll) | page 1 |
| `W` / `E` | Rueda Colores / Rueda Mezcla | page 2 |
| `A` | Movimientos Cabezas | page 2 |
| `G` / `P` | Gobos / prisma | page 2 |
| `J` | Humo Auto | page 2 |
| `V` / `Z` | Dimmer Chase / Dimmer PingPong | page 2 |
| `S` / `D` | Strobo ON / OFF (shutter) | page 2 |
| `PgDn` / `PgUp` | next / previous page | anywhere |

Keys 1-0 are on every colour bank: every widget sees every key press, so `1`
lights red on the heads, the bars and the PARs at once. **Every widget sees
every key press on every page too**, visible or not - which is why the page-1
keys keep working while page 3 is on screen, and why every button's key is
unique, checked by a test.

## Intensity and strobes

Colour is not the only thing that moves. Two dimmer looks - a chase (an EFX in
Dimmer mode, the fixtures spread around the path so the peak runs along the rig)
and an odd/even ping-pong - and four strobes.

The strobes come in two kinds because the rig does. A fixture with a shutter
strobes itself, and `Strobo ON` / `Strobo OFF` drive it - but **only where the
fixture definition labels a strobe range**. Guessing on an unlabelled shutter
channel is how a head goes dark mid-set: a MiN Wash puts "Closed" at 1-7. The
LED bars and PARs have no shutter, so `Strobo Rapido` and `Strobo Medio` do it
the way the hand-built show does - a chaser flipping the whole rig between
`Flash 100%` and `Todo Negro`, at 50 ms and 250 ms.

None of these is in `AUTO`. They are for somebody standing at the laptop: a
strobe running unattended all night is not a decision to make by default.

## Audio triggers

Five spectrum bands, one of them bound: the upper mids press `Strobo Rapido`.
Its target is a Toggle button on purpose - a band calls `pressFunction` on the
way up and again on the way down, so a Flash button would latch on and never
release - and it is a Toggle button **in a plain frame**, which the bass band's
old target was not: `Todo Blanco` now lives in the room-state solo frame, so
binding a bass line to it would have had the music killing `AUTO` on every kick.

It is inert until somebody enables it, and it needs an audio input picked in
QLC+'s Configuration first. The thresholds and the pairing are a decision to
make at the venue with the real music playing.

## Starting it without anyone there

QLC+ can do the last step itself: set a **startup function** (the green flag in
the Function Manager) to `AUTO`, and turn on **Project autostart** under
Configuration → System. Then powering the laptop on brings the show up with no
clicks. Command line does the same for a kiosk setup: `-o <file> -p` opens the
workspace and goes straight to operate mode, `-k` shows only the Virtual
Console.
