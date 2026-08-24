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
| `B` / `º` | Todo Blanco / Todo Negro |
| `Space` | Flash 100% (Flash, not Toggle) |
| `-` | Flash 50% (Flash) |

The hand-built console also had per-colour keys 1-0 on each bank, speed dials on
`M`, an XY pad for the heads, dimmer chases on V/B/C/Z and strobe effects. Those
are **not generated yet**.

## Starting it without anyone there

QLC+ can do the last step itself: set a **startup function** (the green flag in
the Function Manager) to `AUTO`, and turn on **Project autostart** under
Configuration → System. Then powering the laptop on brings the show up with no
clicks. Command line does the same for a kiosk setup: `-o <file> -p` opens the
workspace and goes straight to operate mode, `-k` shows only the Virtual
Console.
