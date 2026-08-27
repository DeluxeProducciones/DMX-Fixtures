# TODO — Vibra Eventos (DMX / lighting)

The backlog for this repo: the rig, the fixture definitions, the QLC+
workspaces and `tools/qlctool`. It moved out of `~/p/TODO.md` on 2026-08-26 —
the work has a repo of its own now, and the owner asked for it to live beside
the thing it is about.

Status marks are the ones `~/p/CLAUDE.md` defines: `[ ]` pending, `[~]` partial
or unverified, `[!]` blocked, `[x]` verified complete, `[-]` obsolete. Closed
work goes to `~/p/TODO_LOG.md` with the date and the evidence, as before.

**Before finishing anything here**, see `CLAUDE.md`: find the cause, add a rule
to `qlctool check`, add a dated regression test, run it over all three
workspaces.

- [ ] **Run `qlctool check` before every show file leaves this repo.** It reads
  what the room will do rather than whether QLC+ can load the file, and it found
  four bugs on its first run. `cd tools/qlctool && .venv/bin/qlctool check
  "../../QLC+ Setups/Vibra-split.qxw"`. New rule when something misbehaves: find
  the cause, add a rule, add a dated regression test, run it over all three
  workspaces — written down in the repo's `CLAUDE.md`.
- [!] **Mirar los 42 efectos internos de los paneles y decir cuales valen.**
  Los WX-60WPS llevan 42 animaciones propias (canal 6 = modo, canal 7 = efecto,
  canal 8 = velocidad) que el show no tocaba: el canal 6 estaba en 0 = "No
  function", asi que solo se usaba el RGB. Ya estan los 42 generados como
  escenas (`Paneles - Effect 1..42`), en la pagina 3 de la consola, y
  `Ciclo Paneles` los recorre en Random cada 12 s dentro de AUTO. **Nadie los ha
  visto**: la definicion solo los llama "Effect N" y no hay manual del aparato
  en `Manual/`. Y no se pueden ver en el simulador: el 3D de QLC+ pinta lo que
  hay en los canales RGB, y en modo Auto el aparato genera el color por
  hardware con el RGB a 0 - por eso los paneles salen apagados en la preview de
  AUTO (owner, 2026-08-26) estando el fichero bien (ch1=255, ch6=128 Auto,
  ch7=efecto, ch8=128; verificado contra la definicion). Siguiente paso:
  pulsarlos uno a uno en sala, apuntar cuales valen, y dejar el ciclo solo con
  esos. Tambien queda por ajustar la velocidad (ahora 128, mitad de escala,
  elegido a ciegas) y decidir si interesan los otros dos modos que tiene el
  cacharro: Mixer Color (12 efectos de color) y Sound Mode (2, reactivo al
  sonido).
- [ ] **Comprobar en sala los 4 grupos nuevos (2026-08-26).** Los 4 paneles
  WX-60WPS salieron de `BarrasLed` a un grupo propio `PixelesLed` (4x1), porque
  compartir la rejilla 8x3 con las dos barras los dejaba a oscuras media
  animacion — ocupaban solo las columnas 4-7 de la fila de abajo. De paso, todas
  las rejillas ahora encajan exactamente: `BarrasLed` 8x2, `Cabezas` 12x1 (antes
  declaraba 8x1 sobre 12 heads, 4 inalcanzables), `PAR` 15x1. La consola pasa de
  288 a 361 botones (un banco de color, 30 mezclas y 30 matrices mas para el
  grupo nuevo). Verificar que el barrido cruza los 4 paneles y que la pagina 2
  sigue cabiendo en la pantalla del portatil.
- [ ] **Ver en el rig si las barras ya siguen el show (2026-08-26).** "Las
  barras led van con los colores a su bola, no siguen el show" (owner, con la
  preview: barras en magenta, sala en cyan). Causa: dos relojes de color -
  `Rueda Colores` rotando escenas sobre el rig y `Ciclo Matrices BarrasLed`
  rotando su propia paleta sobre las barras - y QLC+ no puede esclavizar un
  chaser a otro. Arreglo: cada paso de la rueda es ahora una Collection que
  arranca la escena y una matriz de barras *del mismo color* (algoritmo
  rotando Fill/Even-Odd/Waves/Solid, una pasada completa cabe en el paso); el
  ciclo independiente sale de AUTO y de los momentos pero sigue en la consola.
  Regla nueva `relojes de color` + test fechado. Confirmar en sala que barras y
  sala cambian de color a la vez. Refinamiento posible: QLC+ 5 si persiste
  `BlendMode="Mask"` como atributo de `<Function>` (function.cpp:918, mascara
  multiplicativa en universe.cpp) - permitiria una sola matriz continua sobre
  el color de la rueda, pero depende del orden de escritura del tick y el
  checker HTP no lo modela; solo si algun dia hace falta animacion continua.
- [ ] **Re-check the rig after the dark-fixture fixes (2026-08-26).** The
  owner found both on the real rig: `BLANCO TOTAL` left the four BEAM 230W 7R
  black (no RGB, so every colour generator skipped them) and the HYULIGHTS
  panels were colour-without-intensity in FIESTA (a matrix writes RGB only; the
  rig-wide wheel used to open their master dimmer by accident). Fixed by
  `wheel_color_values` on the base looks and a new `Pixeles ON` scene, verified
  in the generated DMX (beam ch6=248/ch7=255/ch8=4; panels ch1=255). Confirm on
  site, and check the LED bars too - they are pure RGB and should never have
  been affected.
- [ ] **Try the new operator page on the show Mac before the next gig.** The
  console is now three pages (`show` / `manual` / `librería`) built by
  `qlctool newshow`; page 1 is seven mutually exclusive room states plus six
  hits, and the energy levels are no longer buttons. Two things only a real
  screen can settle: whether the 28pt/15pt captions read across a dark room at
  1440x900, and whether `PgDn`/`PgUp` change page in operate mode without
  stealing focus. Files: `QLC+ Setups/Vibra-split.qxw` (current patch),
  `Vibra.qxw`, `Vibra-beats.qxw`.
- [ ] **`test_qlcplus_loads_the_show` is flaky under the full suite.** Failed
  once with `fixture 13 overlapping with fixture ...` while passing in
  isolation and on every re-run (2026-08-25); several tests launch the real
  QLC+ binary and appear to contend over its config. Smallest next step: give
  each `validate_workspace` call its own `QT_QPA_PLATFORM`/config dir, or
  serialise them with a session-scoped lock. `tools/qlctool/qlctool/validate.py`.
- [ ] **Rename the GitHub org `DeluxeProducciones` — the company is now "Vibra
  Eventos", not Deluxe Producciones** (owner, 2026-08-24). When renaming: the
  org and likely the `DMX-Fixtures` repo, then update every reference — brain
  `business/access-map.md` and `projects/vibra-dmx.md` (source URLs + prose),
  the local clone remotes (`~/p/DMX-Fixtures` and `~oficina/DMX-Fixtures` on the
  show Mac), and the `qlctool` branch's origin. GitHub keeps old-path redirects,
  but they silently spawn duplicate clones (same trap as the POIComb->POITools
  rename), so re-point remotes explicitly. The `.qxw` `Author` field ("Oficina")
  needs no change.
- [~] **Verify the remaining four undocumented fixtures on site.** Online search
  (2026-08-24) settled only the Chauvet MiN Wash: its 13-channel mode matches
  the manufacturer manual on channels 1-10 (Pan, Pan fine, Tilt, Tilt fine,
  Vector speed, Dimmer/Strobe, R, G, B, Color Macros), which is everything the
  toolkit drives. Generic BEAM 230W 7R, Vortex PC-64 LED S, HYULIGHTS
  WX-60WPS-48PARTITION and LED Beam Mini cannot be verified remotely - those
  names are shared by fixtures with different channel layouts (one 7R manual
  found puts Color on ch1 and Pan on ch10; our definition has Pan on ch1). The
  check is now a five-minute job on site: `qlctool probe <show> <fixture-id>
  --base "7=255" --buttons` builds one scene per channel plus a walk chaser -
  press play and write down what each channel does. Do it in the same session as
  the physical-rig confirmation.
- [ ] Fix the `5 Channel` mode in `QLC+ Fixtures/Chauvet-MiN-Wash.qxf`: it lists
  Pan, Pan fine, Dimmer/Strobe, Color Macro, Reserved - **no Tilt**, which
  cannot be right for a moving head. Harmless today (the patch uses the
  13-channel mode) but it will bite whoever switches modes. Either correct it
  against the manual or delete the mode.
- [~] **Review `QLC+ Setups/Vibra.qxw`** - the fresh canonical show built by the
  toolkit on branch `qlctool`. Rebuilt 2026-08-25 after the owner reported that
  pressing AUTO stopped the show and that the console was an unusable 2662px
  list. Both were real and are fixed (see `TODO_LOG.md`); it is now 288
  functions and a 284-button console laid out to 1440x900 (extent 1432x890),
  and QLC+ 5.2.2 loads it clean. Copies in `~/Demos-qlctool/` on both machines. Pending: owner runs
  it on the show laptop and says whether AUTO now holds and the layout works,
  then archiving the two DeluxeEventos workspaces and merging the branch.
- [ ] Put the two CLB2.4 grids in a fixture group. They are in none, so they get
  no colour bank and no matrix - only the rig-wide `Rueda Colores` scenes reach
  them (which is why AUTO no longer leaves them dark, 2026-08-25). `qlctool
  patch <file> --group` is the edit; the `PAR` group's 3x3 grid has two free
  cells.
- [ ] Check on site how the 50-degree truss PARs sit over the DJ. The measured
  angle lands them at z=6417 - 1,9 m past the deck - with the beam passing about
  35 cm over his head, against 2,8 m at the 60 degrees the plot carried before.
  Above him, but not by much: worth an eye at the get-in.
- [ ] Try the two generated shows on the laptop and say which one holds up:
  `QLC+ Setups/Vibra.qxw` (real time) and `QLC+ Setups/Vibra-beats.qxw` (chases
  on QLC+'s Beats tempo with the audio input as beat generator, 2026-08-25).
  The beat one needs an **audio input picked under QLC+ Configuration** or
  nothing advances - that is the whole risk of it, and the reason it is a
  separate file. What to watch: does the detected BPM track real music through
  the venue's PA, and does anything stall between tracks.
- [~] **AUTO is the full mix from second one - heads always moving** (owner,
  2026-08-27: "el auto es eso, como el modo auto de las cabezas en si").
  **Implemented 2026-08-27** after a Codex review of the plan (read-only +
  web) corrected four things before any code; all three workspaces
  regenerated, validated in headless QLC+, `qlctool check` clean, 230 tests
  green. What changed:
  - Six checker rules with dated regression tests (`docs/checks.md`):
    `estrobo demasiado rapido` (4 Hz cap; `Strobo Rapido` had shipped at
    10 Hz), `estrobo enganchado` (looping strobe behind a button; hits are
    SingleShot bursts now), `flash sin escena` (QLC+ only flashes Scenes),
    `intensidad tapada` (HTP shadow - the bug that sank "Ambiente = dimmer
    bajo" as first drawn), `acento sin dueño` (flashed LTP wheel no state
    restores), `familias de movimiento mezcladas` (one EFX over wash and
    beam optics).
  - Colour and intensity are separate owners: the rig-wide wheel, contrasts
    and wheel scenes state colour/position only; each level and moment
    carries `Intensidad Ambiente` (110) or `Intensidad Total` beside it.
  - Movement per family: washes get wide slow EFX (Ambiente breathes from
    second one), beams get smaller shapes plus a static `Beams Abanico` fan
    that doubles as their rest step in Fiesta; Peak cut from 2 min to 40 s.
  - Strobe out of the audio triggers; Flash buttons carry Override priority.
  **Still open on site**: do Ambiente's slow washes read as alive; fan
  pan/tilt values (guessed: pan 82-172, tilt 105) need aiming; `Intensidad
  Ambiente` 110 is a first guess; MiN Wash cannot dim (no dimmer channel -
  RGB is its intensity, stays full in Ambiente).
- [ ] **Highlight vocabulary, part 2 - deferred from 2026-08-27 on purpose.**
  Each needs channel work that is unverifiable off-site or a Script: beam
  chase one-head-at-a-time (needs shutter-close values; four fixtures still
  have unlabelled shutter ranges, see the probe item), snap positions on beat
  (closed-shutter travel steps), crowd sweep (calibrated tilt-down bounds),
  blackout-then-burst pre-drop (QLC+ Script with `Engine.setBlackout` +
  guaranteed cleanup - engine/src/scriptv4.cpp), gobo/prisma flash accents
  (need `Prism Off`/`Gobo Open` neutral owners running in every state), and
  the two-timescale scheduler (macro minutes / micro 16-32 bars inside each
  level). `Dimmer Chase` in Peak is still cosmetically shadowed by
  `Intensidad Total` at 255 (EFX dips can't win HTP) - visible fix needs the
  chase to own Peak's intensity alone.
- [ ] Judge the energy levels against a real night. `Ciclo Energia` walks
  Ambiente 4 min -> Fiesta 8 -> Peak 2 -> Fiesta 8, with the colour bed and the
  haze running underneath so a level change never blacks the room out. The
  numbers are a first guess: if the quiet level feels dead or the peak feels
  rationed, they are `AMBIENT_HOLD`, `PARTY_HOLD` and `PEAK_HOLD` in
  `tools/qlctool/qlctool/generate/canonical_show.py`.
- [ ] Check the mirrored movement from the floor. House-right movers (CromoWash
  #2, beams 21 and 23) now run the EFX backwards so the pairs open and close
  together instead of the rig sweeping in parallel. If it reads wrong it is the
  plot's sides, not the effect: `house_right_fixture_ids` compares against the
  middle of the stage grid.
- [ ] Decide on `QLC+ Setups/Vibra-split.qxw` (2026-08-25): the same rig with
  each CLB2.4 patched four times, one fixture per PAR head, so all eight can be
  aimed and coloured separately in the 3D view - which QLC+ cannot do for the
  four heads of one fixture (`Fixture3DItem.qml` keeps a single `lightColor`).
  Open it beside `Vibra.qxw` and say whether it replaces it. If it does, the
  plot to keep is `vibra-stage-plot-split.json` and the heads want fanning
  apart rather than all at `-35`.
- [ ] `qlctool patch --group-add` cannot move a head that is already in a cell -
  it refuses with "cell (x, y) already holds fixture n". That is why the split's
  `PAR` group is a 7x3 grid with the CLB2.4 heads bolted to the right of the
  PC-64 block instead of a clean 8x2 that reads like the rig. Either allow an
  explicit move or add a `--group-clear`.
- [ ] Set the audio-trigger thresholds on site. Two of the five bands are bound
  by default (bass presses `Todo Blanco`, upper mids press `Strobo Rapido`) but
  the thresholds are QLC+'s defaults and the pairing is a guess until it is
  heard over real music. QLC+ also needs an audio input picked under
  Configuration before the widget does anything.
- [ ] Confirm the strobe values on the fixtures whose shutter channel has **no
  labelled range** - the PC-64, the CLB2.4, the Mini Led Moving Head and the
  WX-60WPS. `qlctool` deliberately leaves them out of `Strobo ON`, because a
  guessed value closes a shutter instead of flashing it. The channel probe
  settles it in the same on-site session as the rest of the rig.
- [ ] `DeluxeEventos2.qxw`'s **"Velocidad Cabezas" slider does nothing** - it is
  a Level slider with an empty `<Level>`, no `<Channel>` under it, and QLC+ has
  no speed slider mode at all. The generated show uses a `<SpeedDial>` instead.
  Either fix or delete the slider before the old workspace is archived.
- [ ] Merge branch `qlctool` into `main` once the fresh show is accepted. It
  carries the whole toolkit plus three format variants of DeluxeEventos2 used as
  test material.
