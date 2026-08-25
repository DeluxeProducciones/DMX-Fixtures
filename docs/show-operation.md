# How the show is run

**Nobody operates these lights.** The laptop is left alone at the venue and the
show has to keep changing colour, movement and gobos by itself. Everything below
follows from that.

## Consequences for how the show is built

- **One thing to press.** `AUTO` is a Collection, and a collection starts all of
  its members at once: the colour wheels, movement, gobos, the beams' colour
  wheel, the matrix effects and the smoke timer.
- **Everything that cycles is `RunOrder="Random"`.** A fixed order reads as a
  loop within a couple of minutes when nobody is intervening.
- **Smoke runs on its own timer** - a burst, then a long wait, forever - and is
  driven from nowhere else.
- **Colour range comes from mixing.** The strongest looks in the hand-built show
  are two-colour: odd fixtures on one colour, even on the other ("Rojo / Azul"),
  stepped through by a mix wheel. Solid washes alone look thin.
- **The palette is the show's own.** 18 colours, mined from every RGB triple the
  hand-built scenes drive plus its matrix colours - which is why values like
  (255, 0, 100) and (160, 0, 255) are in it.

## The generated show

`qlctool newshow` builds all of it on the existing patch. Structure:

- Base looks: `Luces ON`, `Todo Blanco`, `Todo Negro`, `Flash 100%`, `Flash 50%`
- Per fixture group: a bank of solid colours, 30 two-colour mixes, a
  `Rueda Colores <group>` and a `Rueda Mezcla <group>`, both Random
- Matrix effects per group (algorithm x colour) with a cycle chaser
- Movement: one EFX per shape over the twelve moving heads, phases spread evenly
  around the path, on a Random 10s chaser
- The beams' gobo wheel (20 positions), colour wheel (17) and prism
- `Humo Auto`
- `Rueda Colores` and `Rueda Mezcla` collections over the per-group wheels, and
  `AUTO` over everything

## The console

Built to a fixed **1440x900** - the show laptop's screen - so nothing scrolls
and nothing is off the edge. Three columns:

| Where | What |
| --- | --- |
| Left | `Show` (AUTO, the two wheels, Luces ON, Blanco, Negro), `Efectos` (movement, gobos, beam colour, prism, humo, the two flashes), a colour bank per fixture group on keys 1-0, and the two-colour mixes in a 3-page frame |
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
