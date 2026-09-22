# The play page: attribute families with an AUTO of their own

Date: 2026-09-02. Owner's request: keep page 1 as it is (the automatic show)
and add a page for when "we feel like playing with the program" - colours
(the wheel first, then the whole palette, combinations and multicolour),
pixel effects, gobos, head movement, each section with an AUTO button in
case nobody wants to be in charge of it, and a "back to normal" strip on
top so that, while the show runs, the room can be put on red, or blacked
out and hit with colour flashes.

Adjudicated with Codex (gpt-5.6-sol, read-only, 2026-09-02): "adopt with
changes". Every engine claim below was read in `~/p/qlcplus`; the files that
matter are byte-identical between `QLC+_5.2.2` and master.

## The mechanism: one solo frame per attribute family

A professional desk groups parameters into families - intensity, position,
colour, beam (gobo, prism), effects - each with a playback running underneath
and a manual override on top that a *release* hands back. QLC+ 5.2.2 has no
release primitive, so the page emulates it with what a solo frame does:

- A **hook** is a Toggle button over *exactly* the function a room state
  starts for that family (`Rueda Colores`, `Gobo Animacion`, ...). A Toggle
  monitors its function whoever started it: `VCButton::slotFunctionRunning`
  emits `functionStarting`, `VCSoloFrame::slotFunctionStarting` notifies
  every sibling, and each Toggle sibling stops its own function. So whenever
  AUTO, a moment or an energy-cycle step retakes the family, **the latched
  pick is released**. Pressing the hook by hand is the section's AUTO button.
- A **pick** is a latched Toggle button. Starting it makes the solo frame stop
  the hook (`Function::stop` from a `ManualVCWidget` clears every source,
  `function.cpp:1184`); the state's Collection only drops that child
  (`Collection::slotChildStopped`) and keeps running the rest. The pick is
  then the family's only writer: no HTP mixing, nothing steps over it. That
  is why it may be latched where the manual page's layers must be held.
- A pick must **not** be reachable from any state: a chaser stepping onto it
  would make its button report a start and kill the hook. Every pick is
  therefore a one-member **wrapper Collection** over the original function,
  under a new ID (Codex's change; no duplicated data). Buttons monitor only
  their own function ID, so the original starting elsewhere is invisible.
- `MasterTimer::timerTickFunctions` runs stops before starts, and a function
  stopped and restarted in one tick gets `postRun` then `preRun`, so a pick
  that shares leaves with the wheel's step restarts cleanly.

## Page 2 - JUGAR

Top to bottom, 1440x900, nothing below the fold.

1. **VOLVER AL SHOW** (plain frame): keyless duplicates of `AUTO`, the four
   moments, `Blanco Total`, `Todo Negro`, and the held hits `Flash 100%`,
   `Flash Color`, `Humo ON`, `Strobo Rapido`. Two Toggle buttons on one
   function both light (the starter green, the monitor orange,
   `VCButtonItem.qml`), so the `consola` rule's "one always looks off" is
   false and is relaxed for function-backed buttons; it stays for Blackout,
   whose state is local to the button. `APAGON` and `PARAR TODO` are not
   duplicated: `Escape` and `Backspace` reach every page. A label states the
   honest total reset: if AUTO is already lit, press it twice, or
   `Backspace` then `Q`. Beside them a row of **GOLPES DE COLOR**: new held
   Scenes, one per palette solid, colour + full dimmer + the strobe
   `Flash 100%` carries, as Flash with Override and ForceLTP - under `Todo
   Negro` the dimmer wins HTP and the colour wins ForceLTP.
2. **COLOR** (solo): hooks `Rueda Colores` (captioned AUTO), `Rueda Mezcla`,
   `Luz Charla` (Charla's bed, so `F1` releases the pick). Picks: wrappers
   over the wheel's 21 steps (`Rig X + Pixeles`: ten solids, five
   heads/rest contrasts, four `Rig 4 Colores`, two `Rig Multicolor`) and the
   two `Arcoiris`. Each step already colours the whole rig - bars, Lyres
   rings and the 7R colour wheel.
3. **PIXELES** (solo): hook `Ciclo Paneles Mixto`. Picks: wrappers over
   twelve of the panels' 42 built-in effects, spread across the range, and a
   wrapper over `Paneles Manual` ("panels follow the colour"). The bars need
   no picks: the wheel's steps carry their matrix.
4. **CABEZAS** (solo): hooks `Movimientos Suaves`, `Movimientos Cabezas`,
   `Movimientos Rapidos` (also the AUTO lento / normal / rapido choice) and
   `Cabezas Centro`. The slow wash chaser is renamed `Suaves Washes` and the
   slow beam chaser `Suaves Beams`, like the fast pair, and `Movimientos
   Suaves` becomes the Collection over both; `Nivel Ambiente` and `Momento
   Tranquilo` start that Collection, and `Nivel Fiesta`, `Nivel Peak` and
   `Nivel Fiesta Dinamico` start `Movimientos Cabezas` / `Movimientos
   Rapidos` instead of the two family chasers. Picks: wrappers over the
   shape Collections the wash and beam chasers step (`Wash Circulo`, `Beam
   Ocho`, `Ola Vertical`, `Barrido Unison`, `Beams Abanico`, `Beams Cruce`
   ...) and `Escenario`, latched.
5. **GOBOS** (solo): hooks `Gobo Animacion` and a new `Gobo Reposo` scene
   (same values as `Gobo - White Light`) which the quiet states park with
   instead of the animation's own step. Picks: wrappers over the 17 gobos,
   the 8 dealt patterns and the shakes, in an inner multipage frame if they
   do not fit at a legible size.
6. **PRISMA** (solo): hooks `Prisma Animacion` and a new `Prisma Reposo`
   (same values as `Prisma - None`), same reason. Picks: wrappers over the
   nine prism scenes.

The beams' colour-wheel picks stay off this page: latched, they would stop
the rig wheel and leave every RGB fixture dark. They remain held on page 3.

Pages become four: **Show / Jugar / Control / Libreria**. Control is what is
left of the manual page: the held colour banks on keys 1-0, the XY pad, the
movement dial, the grand master, the dimmer chases, `Golpe Graves`, `Humo
Vertical`, the beam-colour picks, the audio triggers. The SMC-PAD's bank-2
bindings follow their functions to the hooks on Jugar (one widget per
function keeps them).

## What the operator has to know (goes on the page and in the docs)

- There is no one-button total reset in QLC+ 5.2.2. Return is per family
  (its AUTO) or by changing state; with AUTO already lit, press it twice.
- Under AUTO a movement, gobo or prism pick is released at the energy
  cycle's next step (8 minutes at most), because that step starts the hook.
  Colour and pixel picks persist: they sit outside the cycle. To play for
  long, put the room in a Momento first.
- Pressing an active pick again stops it without restoring the auto: the
  family goes still. AUTO is the first and biggest button of every section.
- The wheel's 800 ms crossfade is aborted when its hook stops; the pick
  enters over the scene's fade-out, not as a hard cut.

## Checker

New rule **`familia con dueño`**, reasoning about capabilities and the graph:
in every solo frame that holds a hook (a Toggle whose function some room
state reaches and that writes a family's channels), every function any state
starts that writes those channels has a Toggle button in that frame; no pick's
function is reachable from any state; and a hook's function is not reachable
from another button's function in the frame. Regression test, dated
2026-09-02: put the wheel's own step `Rig Rojo + Pixeles` on a pick and
assert the checker bites; remove `Luz Charla`'s hook and assert it bites.

The 2026-09-02 layer rules - `capa que se suma al estado`, `capa pisada por
el ciclo`, `capa que deja huella` - read through wrapper Collections to the
leaves they reach, and exempt only a latched button that sits in a family
frame whose hooks are complete. Without that, a wrapper bypasses them.

`consola`'s double-button finding applies to Blackout buttons only.

## Out of scope

Beam colour picks on Jugar; bars' algorithm picks; a strobe latched anywhere
(`estrobo enganchado` stands); any change to page 1.
