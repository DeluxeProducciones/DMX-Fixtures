# How the show is run

**Nobody operates these lights.** The laptop is left alone at the venue and the
show has to keep changing colour, movement and gobos by itself. Everything below
follows from that.

## Consequences for how the show is built

- **One thing to press.** `AUTO` is a Collection of three things: the rig-wide
  colour wheel, the smoke timer, and `Ciclo Energia` - the chaser that walks the
  night through its energy levels.
- **The night goes somewhere.** Every professional room is built as a handful of
  looks per energy level, and moves between them; strobes, fast movement, prism
  and big chases are held back for the peak, because a rig that spends
  everything in the first minute has nowhere to grow. `Ciclo Energia` steps
  `Nivel Ambiente` (4 min) -> `Nivel Fiesta` (8) -> `Nivel Peak` (2) ->
  `Nivel Fiesta` (8), a wave rather than a ramp. The colour bed and the haze
  stay **outside** the cycle, which is what keeps a level change from blacking
  the room out.
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

- Base looks: `Luces ON`, `Todo Blanco`, `Todo Negro`, `Flash 100%`, `Flash 50%`
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
- The beams' gobo wheel (20 positions), colour wheel (17) and prism
- `Humo Auto`
- `Rueda Mezcla`, a collection over the per-group mix wheels, and `AUTO` over
  the colour wheel, the haze and the energy cycle

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
and nothing is off the edge. Three columns:

| Where | What |
| --- | --- |
| Left | `Show` (AUTO, the energy cycle and its three levels, the two wheels, Luces ON, Blanco, Negro), `Efectos` (movement, gobos, beam colour, prism, humo, the two flashes), a colour bank per fixture group on keys 1-0, and the two-colour mixes in a 3-page frame |
| Middle | movement shapes, the beams' 20 gobos and 17 colour-wheel positions, prism, the 90 matrix effects in a 3-page frame, and the per-group colour wheels and matrix cycles |
| Right | an XY pad over the twelve moving heads, speed dials for the colour wheels and the movement, the dimmer looks, the strobes, one live matrix control, and the audio triggers |

Two rules shape it:

- **A function and the functions it starts never share a solo frame.** A solo
  frame stops every other widget's function as soon as one starts, and a Toggle
  button reports its function starting however it was started - so AUTO in the
  same solo frame as `Rueda Colores` dies the instant it starts it. Masters and
  chasers live in plain frames; only leaf looks are grouped solo.
- **What does not fit goes on a page, not below the fold.** The mixes and the
  matrices are multipage frames with the page arrows in their header.

## Keyboard

Taken from the hand-built console, so muscle memory carries over:

| Key | Function |
| --- | --- |
| `Q` | AUTO |
| `W` / `E` | Rueda Colores / Rueda Mezcla |
| `A` | Movimientos Cabezas |
| `G` / `C` / `P` | Gobos / colores de beam / prisma |
| `J` | Humo Auto |
| `X` | Luces ON |
| `V` / `Z` | Dimmer Chase / Dimmer PingPong |
| `S` / `D` | Strobo ON / OFF (shutter) |
| `F` / `T` | Strobo Rapido / Medio (flash) |
| `B` / `º` | Todo Blanco / Todo Negro |
| `Space` | Flash 100% (Flash, not Toggle) |
| `-` | Flash 50% (Flash) |

Keys 1-0 are on every colour bank, as in the hand-built console: every widget
sees every key press, so `1` lights red on the heads, the bars and the PARs at
once.

The hand-built console has the dimmer chases on V/B/C/Z; `B` and `C` are
already Todo Blanco and Color Beam here, so they moved rather than clash. Every
button's key is unique, checked by a test, because every widget sees every key
press - two buttons on one letter would fire both.

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

Five spectrum bands, two of them bound: the bass presses `Todo Blanco` and the
upper mids press `Strobo Rapido`. Both targets are Toggle buttons on purpose - a
band calls `pressFunction` on the way up and again on the way down, so a Flash
button would latch on and never release.

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
