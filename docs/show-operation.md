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
  auto de las cabezas en si" (owner, 2026-08-27). Now the washes breathe
  through `Movimientos Suaves` (two wide shapes at 28 s a lap), the beams hold
  the static `Beams Abanico` fan - a needle's rest is a look - the gobo wheel
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
  prism is a peak-only multiplier - inserted spinning (every prism scene
  drives the rotation channel too) and parked out by `Prisma - None` in every
  level and moment that does not run its animation, so a peak's prism never
  outlives the peak
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

Every generated show puts the layers that should feel the music on QLC+'s
**Beats** tempo - colour every 2 bars, a movement shape every 8 - with the
beat generator set to **Internal** at 120 BPM, so the show advances out of
the box and one clock times every layer (since 2026-08-29; the owner found
the BPM setting and asked for it). The `Tempo Show` dial on page 1 controls
that BPM: tap `M` to the music and colour, movement, gobos and prism follow
together, each keeping its own beat count. The dial lists no functions on
purpose - a tap dial with functions writes the raw tap interval into every
one of their durations (`VCSpeedDial::tap -> applyFunctionsTime`), which is
how the old speed dials drove "todos los programas locos". `qlctool check`
refuses that shape (`tap que pisa duraciones`).

`qlctool newshow --beats` builds the same show with the beat generator on
**Audio** instead, deriving the beat from an audio input device: a laptop
left alone in a venue runs its chases on the room's own music
(`Vibra-beats.qxw`). An audio input has to be picked in QLC+'s
Configuration - the device is an application setting, not part of the
workspace, and with no input selected the beat never ticks.

Two things stay on the clock everywhere:

- **The energy cycle.** It measures the night rather than the song, and a
  beat that never arrives must not be able to freeze it.
- **The matrix cycles (except under `--beats`).** An RGBMatrix animation's
  frame clock is milliseconds, so a flat beat-held cycle cuts animations
  short at fast tempos - the 2026-08-26 half-painted bars, wearing beats -
  and the `efecto cortado` rule cannot see a beats hold.

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

### Page 2 - Manual

For somebody who does know the rig: the layers, on top of whatever page 1 is
running. The colour bank per fixture group on keys 1-0 (now with the colour
named on the button), the wheels, the movement shapes - with `Escenario` (the
heads aimed at the stage, pan/tilt carried verbatim from the hand-built show's
own scene, colour left to the running state) and `Centro` (parked) in the same
solo frame, because a fixed aim and a drawn figure are exclusive - the beams'
gobos and colour-wheel positions, a pad over the twelve heads big enough to
aim with, the two speed dials, the dimmer looks, the fixture strobes, the
`Master General` slider (the workspace's own GrandMaster, scaling every output
under whatever is already running), and the audio triggers. The prism frame
carries the hand-built console's per-beam picks beside all-on and all-off:
`1`-`4`, `1 y 3`, `2 y 4`, the beams numbered by DMX address.

The beams' wheels are here rather than in the library because picking a gobo is
a live decision: somebody does it while the show runs.

### Page 3 - Librería

The material the show is built from, not buttons for a set: the two-colour
mixes, the matrix effects, the per-group wheels and matrix cycles, the
`MultiColor BEAM` looks (the beams' continuous half-colour channel - two
colours in one beam - per beam and per mirrored pair, the old console's
"Multi Color"), the panels' forty-two built-in effects, and beside those a
`Vel. Paneles` fader - a Level
slider over the four panels' speed channel, the hand-built console's "Strobo
LED Effect Speed". At zero the cycle's own value (200) rules, because Level
mixes HTP; pushed up it paces the running effect live. The two
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
| `Space` | Flash 100% (Flash - white, shutters strobing fast) | page 1 |
| `-` | Flash 50% (Flash - same white, half the strobe speed) | page 1 |
| `.` | Flash Color (Flash - strobe over the running colour) | page 1 |
| `H` | Humo ON (Flash - the burst, held) | page 1 |
| `F` / `T` | Strobo Rapido / Medio | page 1 |
| `C` | Color Beam Animacion | page 1 |
| `Backspace` | PARAR TODO (StopAll) | page 1 |
| `W` / `E` | Rueda Colores / Rueda Mezcla | page 2 |
| `A` | Movimientos Cabezas | page 2 |
| `G` / `P` | Gobos / prisma | page 2 |
| `J` | Humo Auto | page 2 |
| `'` / `¡` | Arcoiris Simultaneo / Arcoiris Pasos (relative RGB rainbows) | page 2 |
| `V` / `B` | Dimmer Chase / Dimmer Chase 2 (the sweep, each way) | page 2 |
| `Z` / `K` | Dimmer PingPong / Dimmer Secuencia (rotation of the three) | page 2 |
| `S` / `D` | Strobo ON / OFF (shutter) | page 2 |
| `M` | tap tempo on `Tempo Show` (tap the beat, the show's BPM follows) | page 1 |
| `PgDn` / `PgUp` | next / previous page | anywhere |

Keys 1-0 are on every colour bank: every widget sees every key press, so `1`
lights red on the heads, the bars and the PARs at once. As on the hand-built
console, `9` and `0` are not solids: they are the alternating `Azul / Rojo`
and `Rojo / Azul` looks (restored 2026-08-28; Naranja and Rosa stay in the
bank as keyless buttons). **Every widget sees
every key press on every page too**, visible or not - which is why the page-1
keys keep working while page 3 is on screen, and why every button's key is
unique, checked by a test.

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
`Strobo ON` shipped strobing half the rig (2026-08-27). The LED bars have no
strobe channel of any kind, so `Strobo Rapido` and `Strobo Medio` do it the
way the hand-built show does - a bounded chaser flipping the rig between
white and `Todo Negro` at 125 ms and 250 ms a step.

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
plain white flash on page 2 beside the triggers widget. A Flash button is the
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
1's frames and buttons and page 2's two speed dials all come through - the
phone shows what the laptop shows, not a cut-down page.
