# TODO Log — Vibra Eventos (DMX / lighting)

> Searchable record of this repository's closed work: the rig, the fixture
> definitions, the QLC+ workspaces and `tools/qlctool`. Active work lives in
> [TODO.md](TODO.md).
>
> States: `[x]` verified complete · `[-]` obsolete or superseded. Every entry
> carries the evidence that closed it — a command result, a commit, a
> measurement — never a transcript.
>
> Entries before 2026-09-22 were moved here verbatim from `~/p/TODO_LOG.md`,
> which kept them while this repository had no log of its own. Nothing was
> rewritten in the move; the older prose entries and the newer bullet entries
> are both left as they were written.

## 2026

### 2026-09

#### 2026-09-23 - El escenario de QLC+ se ve en BlenderDMX

- [x] 2026-09-23 - **Visor 3D:** "quiero ver el escenario que tenemos en qlc
  pero en esta cosa nueva": GDTF para los 11 `.qxf`, escenario desde el plot,
  primera prueba en el mini.
  - Resultado: `qlctool mvr <workspace>` (`tools/qlctool/qlctool/mvr/`,
    pygdtf 1.4.5 y pymvr 1.0.7) escribe un paquete MVR con un GDTF 1.2
    generado de cada definicion del rig: geometria por primitivas (caja, o
    base/horquilla/cabeza para un movil) con un `Beam` por cabeza, ruedas de
    color y gobo con las imagenes del repo empaquetadas, un modo DMX por modo
    QLC+ con las funciones por rango (obturador cerrado/abierto/estrobo, ranuras
    de rueda como channel sets, giro) y los canales finos plegados en el
    grueso. La ruta OFL + GDTF Builder del backlog no hizo falta. Posiciones:
    `<Monitor>` leido de vuelta (`monitor_items`) y convertido a MVR
    (`mvr_matrix`: z arriba, y hacia el fondo, escenario centrado, media
    vuelta en X para los aparatos con malla y `-x_rot` para humo, barras y
    estrobos, que QLC+ pinta encendiendo por arriba). Los repuestos ocultos
    quedan fuera. `tools/blenderdmx/render_mvr.py` importa el MVR en
    BlenderDMX sin ventana, escribe DMX en sus buffers (dimmer, obturador
    abierto, un color por aparato, pan/tilt abiertos), pone suelo, camara y
    volumen de humo, y renderiza.
  - Evidencia: `pytest tests/ -q`: 491 passed (28 de ellos nuevos, en
    `test_mvr_export.py`, uno por definicion valida el GDTF contra
    `tests/gdtf.xsd` con xmllint); `qlctool check Vibra-split.qxw`: 522
    botones, ningun problema; `qlctool mvr "QLC+ Setups/Vibra-split.qxw"`:
    31 aparatos, 8 GDTF, 9 repuestos ocultos saltados. En el mini,
    `Blender --background --python render_mvr.py -- Vibra-split.mvr` importa
    los 31 y el render muestra la barra de PAR en el truss, los cuatro 7R, las
    CLB2.4 con sus cuatro cabezas, las barras de pixeles, los cuatro paneles,
    los cuatro spray fog y las dos MAC WASH de pie junto a la mesa
    (`~/p/vibra-blender/vibra.png`, `vibra.blend`; corrida final desde el
    checkout `~/p/DMX-Fixtures` en `9ef5d94`, 31 aparatos importados, 4 s,
    Blender sale solo). Gate: `codeality-py baseline check` 0
    nuevos con el paquete partido a una declaracion por modulo; ruff, mypy y
    ruff-format siguen con la deuda conocida, nada nuevo.
  - Trampas que costaron una iteracion cada una, escritas en
    `docs/blenderdmx.md`: pygdtf escribe `File="None"` en un modelo sin malla
    y BlenderDMX falla al cargarlo (`model.file_attr = ""`); el esquema
    prohibe `Default` en el canal y lo exige en la funcion; un obturador solo
    con preset "slow to fast" se abre con el `dmx_from` exacto del set
    abierto, no con `+1`; `artnet_enabled = True` arranca un hilo que impide
    salir a Blender sin ventana (`os._exit(0)` tras guardar).

#### 2026-09-23 - La suite de qlctool tiene presupuesto en el gate

- [x] 2026-09-23 - **Entorno:** subir `syntopica-codeality-py` a 0.2.3 y
  presupuestar la suite.
  - Resultado: `test-budget-seconds = 120` en `codeality-py.toml` y el pin
    `>=0.2.3,<1` en `pyproject.toml`. El gate marca la etapa pytest como
    `over-budget` si la suite vuelve a crecer; lo aprendido esta noche esta en
    codeality (`docs/standards/testing.md#suite-time-budget`).
  - Evidencia: `codeality-py gate`: pytest passed en 37,41 s con
    `--durations=10`; ruff, ruff-format y mypy siguen en findings con la deuda
    conocida de TODO.md, nada nuevo.

#### 2026-09-22 - La suite de qlctool baja de 2 minutos a 35 segundos

- [x] 2026-09-22 - **Entorno:** "genial hazlo todo": paralelizar la suite y
  acortar la espera de `validate`.
  - Resultado: `pytest-xdist` con `addopts = "-n auto"` en `pyproject.toml`
    (`-n 0` para depurar). Los arranques de QLC+ no se podian paralelizar
    porque la build QML comparte `~/QLC+.log`: dos validaciones a la vez se
    truncan el log y la ultima en leer hereda la sesion de la otra. Ahora
    `validate_workspace` toma un cerrojo `flock` (`validate.LAUNCH_LOCK`, en
    el tempdir del usuario) alrededor del arranque en segundo plano, asi que
    cualquier llamador queda serializado sin marcar tests. `quiet_period`
    baja de 2 s a 1 s: medido en nueve arranques, la queja de un aparato sale
    en la misma ventana de 20 ms que el primer marcador de carga y el log
    deja de crecer 0,2 s despues; 1 s es margen 5x. Un paso de chaser que
    apunta a una funcion inexistente no produce ninguna linea en QLC+ (eso
    lo ve `qlctool check`, no `validate`).
  - Evidencia: `test_two_validations_at_once_keep_their_own_verdicts`
    (show real y show truncado desde dos hilos) falla 3 de 3 sin cerrojo
    (el show real hereda "fixture 13 overlapping") y pasa 3 de 3 con el.
    Suite: 463 passed en 46,81 s con `-n 4` y 32,45 s con `-n auto` (12
    workers); 137,62 s en serie esa misma tarde. `pgrep -fl qlcplus-qml`
    vacio despues. `codeality-py baseline check`: 0 new; deptry limpio con
    `pytest-xdist` en DEP002 como plugin.

#### 2026-09-22 - La suite de qlctool baja de 4 minutos a 2

- [x] 2026-09-22 - **Entorno:** seguir apretando la suite ("lo mismo hay otros
  sitios donde optimizar").
  - Resultado: una pasada de `check_workspace` baja de 2,42 s a 0,83 s con
    los mismos hallazgos (comparados uno a uno en los tres shows y en dos
    shows mutados por los tests). Cinco causas: `find_local` / `findall_local`
    / `iter_local` filtraban por `localname` en Python (2,7 M llamadas por
    pasada) y ahora usan el comodin `{*}name` de lxml, que recorre en C;
    `ShowGraph.descendants` se memoiza (36 000 llamadas); la clave de
    `driven` / `reach` ya no reordena `groups` en cada llamada;
    `InstantEvaluator` memoiza por raices y la clave de `_node_states` usa
    `seen & descendants` en vez de `seen`, con lo que un nodo alcanzado por
    dos caminos se evalua una vez; `family_frames` memoiza el handoff y los
    problemas de cada marco (las reglas de capas releian el marco entero por
    cada boton); `offsets_for_role` se calcula una vez por aparato.
  - Evidencia: `pytest tests/ -q --durations=0`: 462 passed en 137,62 s con
    la maquina a carga 25 (240,59 s por la tarde). `test_check.py` son 89,8 s
    de los 133 s de tests (112 tests, 94 pasadas completas); los 14 tests que
    arrancan QLC+ suman 39,6 s y son el siguiente techo: `validate.py`
    espera 2 s de silencio por arranque y la build QML comparte `~/QLC+.log`,
    asi que no se pueden paralelizar sin serializarlos.
    `codeality-py baseline check`: 0 new, 1 resolved; mypy pasa de 100 a 91
    errores conocidos.

#### 2026-09-22 - La suite de qlctool baja de 19 minutos a 4

- [x] 2026-09-13 - **Entorno:** averiguar por que la suite tarda lo que tarda.
  - Resultado: no era la maquina, era el checker. Una pasada de
    `check_workspace` costaba 11,5 s y `test_check.py` la hace 94 veces (~18
    de los 19 min). Tres reglas se llevaban 9,4 s de los 11,5
    (`check_strobe_restore` 4,8 s, `check_accent_restore` 2,9 s,
    `check_pick_darkens` 1,7 s) porque `unowned_while_lit` creaba un
    `InstantEvaluator` nuevo por llamada (20.627 evaluadores) y cada uno
    reparseaba el texto `FixtureVal` de cada escena: 620.951 llamadas a
    `driven_channels` por pasada. Arreglo: `ShowGraph.driven()` parsea cada
    hoja una vez por grafo (`driven_cache`), `reach()` se memoiza igual
    (`reach_cache`, devuelve copia) y las dos reglas de flash comparten un
    evaluador por regla. Una pasada pasa a 1,9-2,0 s con los mismos 0
    hallazgos en los tres shows.
  - Evidencia: `pytest tests/ -q --durations=10`: 462 passed en 240,59 s
    (4m00s) contra 1175,31 s (19m35s) la pasada anterior de la misma noche;
    el test mas lento es ahora `test_qlcplus_loads_the_banks` a 4,38 s
    (carga real de QLC+), ninguna regresion de `test_check.py` pasa de 4,3 s.
    `codeality-py baseline check`: 0 new, 1 resolved.

#### 2026-09-22 - Colores: ni blanco ni feria en las ruedas, multicolor aparte, mezclas con regla

Tres quejas del dueño la misma noche ("los colores siguen siendo una feria",
"las luces blancas en las ruedas de colores automáticas no", "tiene que haber
alguna regla ... cuales casan mejor o usan los prods"), tres reglas nuevas en
`qlctool check`, tres tests de regresión fechados, los tres workspaces
regenerados y validados.

- [x] 2026-09-22 - **Blanco fuera de toda rotación.**
  - Resultado: `wheel_palette.py` (la paleta menos `Blanco`) alimenta la rueda
    general, la simple, la pastel, las ruedas por grupo, las mezclas y los
    ciclos de matrices; el blanco queda en `Blanco Total`, los flashes, la luz
    de charla y el pick 8 de cada banco. Las dos matrices curadas en blanco
    (Plasma Rainbow, que no lee el color, y 3D Starfield) pasan a cyan y
    celeste. Regla `blanco en la rueda`, test
    `test_2026_09_22_white_back_on_the_wheel`.
  - Evidencia: antes, 83 hallazgos por show; tras regenerar,
    `qlctool check` "522 botones revisados, ningun problema" en los tres.
- [x] 2026-09-22 - **Multicolor en rueda propia, los estados a dos colores.**
  - Resultado: `Rueda Multicolor` (tecla R, marco COLOR, glifo, dial de
    tempo) con `Rig Multicolor 1/2` y `Rig 4 Colores 1-4` (el asiento blanco
    del reparto pasa a amarillo); `Rueda Colores` queda en 17 sólidos y 5
    contrastes. Regla `mas de dos colores en un estado`, test
    `test_2026_09_22_the_multicolour_deal_back_in_the_state_wheel`.
  - Evidencia: antes, 6 hallazgos por show (los seis pasos salvajes en la
    rueda de AUTO); `test_the_multicolour_looks_rotate_on_a_wheel_no_state_starts`
    comprueba que ni AUTO ni los momentos llegan a ella.
- [x] 2026-09-22 - **Qué dos colores y dónde: la regla de los profesionales.**
  - Resultado: `complementary_pairs.py` (entre roles, cálido sobre frío:
    ámbar/azul, amarillo/azul, rojo/cyan, magenta/verde, más rojo/azul del
    show) alimenta los contrastes `Cabezas X / Resto Y`; `analogous_pairs.py`
    (vecinos, en ambos sentidos, más las teclas 9/0) alimenta `Rueda Mezcla`
    por grupo, 16 pasos en vez de 30. Regla `complementarios en un mismo
    lavado` (dos colores saturados a 150 grados o más alternando dentro de un
    grupo), test `test_2026_09_22_complementary_colours_split_across_one_wash`.
    Fuente: HARMAN vía `brain/topics/stage-lighting-design.md` -
    complementarios en la misma superficie se desaturan hacia blanco.
  - Evidencia: antes, 20 hallazgos por show (`Amarillo / Azul` y `Verde /
    Magenta` en cinco grupos, dos sentidos).

#### 2026-09-22 - Revision del backlog de DMX-Fixtures: cinco items cerrados y ocho con datos corregidos

Se comprobo cada item de `DMX-Fixtures/TODO.md` contra el arbol en vez de
contra lo que el propio item afirmaba. El backlog queda en 61 `[ ]`, 8 `[~]` y
ningun `[!]`, `[x]` ni `[-]`: los cerrados ya no se acumulan en el activo, que
es lo que pide el contrato de `brp-todo-work`. Cerrados y sacados del backlog:

- [x] 2026-09-13 - **Entorno:** el puntero al clon de QLC+ no estaba roto.
  - Resultado: `~/p/qlcplus` existe en esta maquina; el item lo daba por
    ausente desde el 2026-09-13.
  - Evidencia: `ls -d ~/p/qlcplus` devuelve la ruta.

- [x] 2026-08-29 - **SMC-PAD:** el mapa del pad ya sale de un solo sitio.
  - Resultado: `generate/smc_pad_device.py` genera el perfil
    (`qlctool input-profile`) y parchea el workspace (`input_binding.py`); la
    capa manual vive en el banco 2 y la regla
    `binding a un control que el pad no manda` lo vigila.
  - Evidencia: medido con `tools/smc-pad/midicap.swift` (PAD13 = 48, PAD1 = 36,
    PAD16 = 51); al 2026-09-22 el show trae 24 `<Input>` y 83 teclas.

- [-] 2026-08-27 - **Consola:** "MIDI controller for the operator".
  - Resolucion: superado por el M-VAVE SMC-PAD, que ya esta en el show con
    perfil generado, dos bancos y feedback de LED por BLE (`tools/smc-pad/`).
    El item pedia comprar un controlador; lo que queda son sus pruebas de sala,
    que siguen abiertas en `TODO.md`.

- [x] 2026-08-29 - **SMC-PAD:** el color de los pads por BLE GATT, desbloqueado
  y en produccion.
  - Resultado: el item seguia `[!]` "blocked on one physical step" (poner el pad
    en modo Bluetooth para que anuncie). Eso ocurrio: `qlc_led_bridge.swift`
    mantiene la sesion GATT, publica el puerto MIDI virtual y pinta cada pad, y
    se instala con `tools/smc-pad/install-bridge.sh` como agente de launchd.
  - Evidencia: `tools/smc-pad/README.md` seccion "The QLC+ bridge (working)",
    confirmado extremo a extremo (el puente registra `MIDI in ... -> pad addr`);
    el pulido que queda esta en el item `[~]` del pad, que sigue abierto.

- [x] 2026-08-27 - **Auditoria QLC+:** `PixelesLed` sin matrices no era un
  defecto.
  - Resultado: el generador salta la matriz RGB de los grupos que se animan
    solos (`generate/canonical_show.py`, `_all_self_animating()`); los paneles
    corren sus 42 efectos internos y en modo Auto ignorarian el RGB.

Corregido en items que siguen abiertos, porque afirmaban numeros que ya no son
ciertos: la consola no tiene 430 ni 503 botones sino 605 en cuatro paginas; el
show no tiene 288 funciones sino 1629; `Ciclo Energia` pone el Peak en 40 s, no
en 2 min; los blancos los reparte `rgbw_split`, no `white_level`; el plasma de
las barras y el boton COLOR BEAM ya no existen; de sliders hay dos, no cero; y
el gate compartido **ya no esta en verde** (3 hallazgos de ruff, 8 ficheros sin
formatear, y mypy, baseline-py, deptry, pip-audit y pytest salen
`failed-to-run` en 0,00 s desde `baseline-py gate` aunque a mano funcionan).
Los ratchets de calidad se remidieron: ruff 187/136/30 (antes 142/104/26),
`zip()` sin `strict=` 13 (antes 24), mypy 89 errores (antes 266), baseline-py
209 hallazgos contra 170 entradas registradas.

Tambien se arreglaron los dos hallazgos de ruff que eran mios del trabajo del
mismo dia (`qlctool/desk_policy.py` y `tests/test_desk_bursts.py`, ambos I001),
y `AGENTS.md` dejo de decir que la suite tarda "~5 min" (34-42 min) y que el
trabajo pasa por la rama `qlctool` (ya mezclada).

#### 2026-09-22 - The `qlctool` branch is merged into `main`

The owner's word: "mergea todo a main". `ca38195` merges the branch,
`a7dfb31` merges the two commits `main` carried on its own (untracking
`.serena`, the CocoIndex ignore line) - their `.gitignore` was the only
conflict, resolved as the union of both. `origin/main` is at `a7dfb31`, the
branch still exists and is fully merged, and `qlctool check` is clean on the
three workspaces from the merged tree: 592 buttons each.

#### 2026-09-22 - The owner's review of the Vibra show: four new rules, and the colour, movement and console fixes behind them

The owner went through the programme and reported fourteen things. Four of them
were one cause each, and each cause is now a rule in `qlctool check` with a
dated regression in `tests/test_check.py`, per this repository's own discipline.

`blanco pagado dos veces`. The white-emitter fix of 2026-09-02 wrote
`min(r,g,b)` to the White channel and left red, green and blue untouched, so
every tinted colour emitted its achromatic part twice. `Luz Charla`, the warm
(255, 214, 170), arrived as R255 G214 B170 plus W170 - white. That is why
"charla y blanco son lo mismo" and why the colour hits looked "mezclados con
blanco". `white_level.py` became `rgbw_split.py`, which subtracts the common
share when it hands it to the white LED and leaves an achromatic request
(r = g = b: the work light, the flashes, a white wheel step) on all four
emitters, so nothing loses output where there is no hue to protect. Proved on
the shipped `Vibra-split.qxw` before the fix: one finding, three fixtures.

`animacion de color sin la rueda`. Both rainbows are relative EFX in RGB mode
built over "every RGB head", and `rainbow_efx.py` counts red channels, of which
a BEAM 230W 7R has none - so the spectrum swept the room with the four beams
parked. The fixture's own answer was in its definition all along
(`RotationClockwiseFastToSlow`, 128-191 of the colour channel), so
`beam_rainbow_spin.py` generates that layer and each rainbow button is now the
EFX plus the spin. The rule reads EFX only, keeping `rueda de color`'s judgment
that a matrix speaks about pixels and not about fixtures.

`figura que deja cabezas quietas`. `Square` and `Lissajous` were wash-only
shapes, so those two buttons moved the six washes and left the four 7R standing:
"algunos movimientos de cabeza no incluyen las beam". The rule asks the question
of a console button rather than of the functions under it, because the
per-family pieces are meant to move one family and are stacked into one button
precisely so the room moves as a whole - a button whose EFX animate part of a
fixture group and leave capable fixtures of that group still is the fault.
Aiming Scenes are out: a rest position is not an animation.

`ritmo sin reloj`. The two intensity sweeps are Collections of one dimmer-mode
EFX per fixture family, and the tempo dial only ever listed functions carrying
a speed of their own - which a Collection does not - so "los barridos de
intensidad van a su bola" was literal: nothing could re-time them.
`_tempo_functions` now descends into a Collection's members, and the dial also
carries the two new colour wheels. The rule excuses long-step rotations (the
energy cycle, the haze) and the beats build, which has no dial because the BPM
generator is its clock.

The rest of the list, decided with the owner and implemented: the Plasma Rainbow
multicolour matrices are gone ("quitar multicolores muy feos"); the automatic
colour comes in three exclusive modes - completos (18 colours plus contrasts and
the wild steps, key W), simples (six primaries and white, C) and pastel tenue
(the palette blended 55% to white, L), with `pastel.py`, `simple_colors.py`,
`pastel_palette.py` and per-mode pixel-group matrices; the COLOR BEAM button is
gone and the beams take the rig's colour from the rig-wide scenes, which frees
key C; every shape button now moves both optics families (the beams gained
`Square` and `Lissajous`) and every one of the seven shapes gained a
`Simultaneo` and an `Alternado` twin as buttons, not only as steps inside the
rotation, which took the CABEZAS frame to 26 picks over fifteen columns; the beams'
figure time is half the washes' so the two families rhyme; the haze buttons went
from 28px under SMALL_FONT to 74px under BIG_FONT, paid for by the 86px of dead
space page 1 carried between the room states and the hits; and 134 of 600
buttons carry a glyph (`control_glyph`), with the tablet desk map splitting it
into an `icon` field of its own (`leading_glyph`).

Evidence: `qlctool check` clean on all three workspaces (592 buttons each), all
three regenerated and `--validate`d in headless QLC+, the four new regressions
passing and the whole suite green. What is left needs the rig or the desk's own repository and
is in `DMX-Fixtures/TODO.md` under the same date.

- [x] 2026-09-02 - **Vibra Eventos (DMX): the MAC WASH 1915Z zoom ran backwards,
      found in another program's fixture library.** The manual prints
      `Zoom 000-255` and nothing else; the definition guessed narrow-to-wide,
      so every look sent 255 and both washes ran at 6 degrees on the night of
      2026-08-29. The owner's idea was to look in other DMX programs' fixture
      libraries: ChamSys MagicQ's Fixture Finder personality for the MacMah
      MacWash1915Z (ids 46510/46511) says *Wide to Narrow 0-255*, and gives the
      strobe (0 open, 1-127 strobe, 128-159 sudden, 160-191 pulse, 192-255
      random - `Strobo ON` had been landing in the random band) and the reset
      (100-109). Same source settled the Mini Led Moving Head's eight
      "No function" channels (LM108 personality, agreeing with two OEM
      manuals). Definitions corrected, three shows regenerated and validated,
      the `cabezas paradas` rule taught that a Collection of nothing but EFX
      is a split movement and not a block. OFL, Freestyler, DMXControl,
      Avolites and Daslight were searched too and had none of it; Codex did
      the search (`gpt-5.6-terra`, the default model was at capacity).
      Later the same day, installing Lightkey and fingerprinting its 7,704
      profiles by channel order found the Algam MW19x15Z - Mac Mah's parent
      brand, the same head - whose manual settles it: zoom 0 = wide, strobe
      0-9 off / 10-255, macro 0-29 = DMX, reset 250-255. ChamSys was right on
      the zoom and wrong on strobe and reset; Lightkey the reverse.

- [x] 2026-09-01 - **Vibra Eventos (DMX): the real SMC-PAD manual PDF is in the
      repo.** `Manual/M-VAVE SMC-PAD - user manual EN-ZH (FCC 2ARCP-SMC-PAD, V04
      2024-01).pdf`, the manufacturer's own document as filed with the FCC
      (fccid.io, grantee So Intelligent Technology, internal model SK12). Every
      manual site is behind Cloudflare and answers 403 to `curl`, so it was
      fetched from inside the real Chrome. Compared against the transcription
      in `Manual/`: the English pages match verbatim; the PDF adds only the
      transpose limit (+-16 semitones, Chinese page), the BT LED states and the
      per-platform pairing notes. It carries **no** note or CC numbers, so
      everything the transcription's "lo que el manual no dice" section
      measured stays measured-only and uncontradicted.

#### 2026-09-02 — Vibra Eventos: the cross-audit, and the nine defects behind "ningun problema"

Two independent DMX-output simulators (Claude's in the session scratchpad,
Codex's under `codex exec`, neither importing `qlctool check`'s rules), crossed
over two rounds until they agreed, over the three shipped workspaces. The
checker reported nothing on all three. Engine facts everything rests on
(`~/p/qlcplus`): Intensity-group channels are HTP and zeroed every cycle,
everything else is LTP and holds; a new fader is appended after every fader
of its priority, so the function started last wins an LTP channel; a Flash
with Override sits after all of them, and ForceLTP skips the HTP compare.

- [x] **Colour layers added to the state instead of replacing it.** AUTO on
      `Rig Cyan` plus key `1` was 255,255,255 on 27 fixtures. Banks, mixes,
      gobo/prism/colour-beam picks and `Escenario` are Flash buttons now
      (Override; ForceLTP on the colour ones), colour-only, held. `Centro`
      button dropped. Rules `capa que se suma al estado`, `capa pisada por el
      ciclo`.
- [x] **STROBO / STROBO SUAVE could not reach black under a lit state** (the
      black step was all-HTP zeros). Now held shutter scenes at 0.97 / 0.785;
      rule `estrobo sin negro`.
- [x] **`MultiColor BEAM` latched the 7R half-colour channel at 255 for the
      night.** Every wheel colour writes it to 0 (`multicolor_off`); rule
      `capa que deja huella`.
- [x] **`Blanco Total` inherited gobo, prism, rotation, focus, position** from
      the last state. Park values folded into the scene (`park_work_light`);
      rule `estado que hereda`.
- [x] **Vertical fog machines' LEDs dark under Peak / Fiesta Dinamico /
      Locura** (`Intensidad Peak` never opened their dimmer; `rule_intensity`
      excluded every smoke fixture). Peak base opens them; rule `color sin
      dimmer en algun instante` (per instant, via `unowned_instant`).
- [x] **`Rueda Colores` faded the 7R colour wheel 800 ms through every detent.**
      `<ExcludeFade>` pinned on every wheel channel (`exclude_fade`); rule
      `rueda fundida`.
- [x] **White looks never used the White emitters** (Mini Led ch7, MAC WASH
      ch12/16/20; Codex's finding). `color_scene_values` writes
      `white_level` = min(r,g,b); rule `blanco sin emisor blanco`. Closes the
      2026-09-01 "canales de blanco" backlog item.
- [x] **`Vel. Paneles` label and docs said HTP; the channel is Speed (LTP).**
      Text fixed; the slider overrides outright once moved.
- [x] `flash sin estrobo` now judges only Flash scenes that raise light; the
      held colour and wheel accents are exempt by shape.
- [-] `HUMO VERT` column in the room's colour is the owner's decision of
      2026-08-30, not a defect; the montage note was stale.
- Second reviewer: Codex confirmed all seven findings it had not reported
  itself, with two corrections taken (Rig Azul is 43 not 44; the fog LEDs are
  dark 28% of the cycle, not half; the gobo/prism reveal is Todo Negro ->
  Blanco Total, not AUTO).
- Evidence: `pytest tests/ -q` -> 364 passed (8 new regression tests, 4
  adapted); three workspaces regenerated and loaded clean in headless QLC+
  5.2.2 (`<ExcludeFade>` and `ForceLTP="1"` accepted); `qlctool check` on each
  -> `502 botones revisados, ningun problema`, while the same 52 rules report
  8 rule families on the previous commit's files. Left for the room in
  DMX-Fixtures/TODO.md: watch the held banks, the shutter strobes, the 7R
  wheel snapping, and the white balance.

#### 2026-09-02 - DMX-Fixtures' one new structural finding is split

`qlctool/install_plan.py` landed with three declarations (ff42d6c) and put the
DMX-Fixtures gate on red; its two helpers are `install_state.py` and
`gobo_folder.py` now, `baseline-py baseline check` reads `0 new, 170 known` and
the gate is green again (DMX-Fixtures, branch `qlctool`, 2026-09-02).


### 2026-08

- [x] 2026-08-28 - **Vibra Eventos (DMX):** five show-design upgrades, Codex
      design review first ("proceed with amendments", all applied).
  - Panels join the rig's colours: the wheel writes their RGB on every step,
    `Ciclo Paneles Mixto` (Loop, 8 min effects / 4 min manual) owns the mode
    channel - one colour clock, one mode owner. `rule_internal_program`
    extended: colour without mode-off is excused only when every lighting
    state owns the mode channel (ownership, not amnesty; dated test proves
    it still bites without the owner).
  - `Rig Multicolor 1/2` wheel steps: every fixture its own palette colour,
    beams on the colour wheel's rainbow scroll, bars under a Plasma Rainbow
    matrix - all inside `Rueda Colores`, so no second clock.
  - Movement: `Ola Vertical` per family (tilt wave - QLC+ Line is x=y, so
    Width 0, Serial), `Barrido Unison` (StartOffset 0, mirror kept so the
    sides meet), `Beams Cruce` (reversed-fan X) - all as chaser steps, never
    concurrent members.
  - `Nivel Fiesta Dinamico` in the energy wave: dimmers owned by `Dimmer
    Programas` (chase 2 and ping-pong serialized in one chaser - HTP makes
    concurrent "ownership" a lie); `Intensidad Peak` now writes strobe-offs
    for the whole rig, closing the flash-latch window during chase levels.
  - Gobo/prism as the pros: prism scenes drive the rotation channel (spin 25
    in, 0 out), `Prisma - None` parked in every non-peak level/moment (ends
    the latent prism latch), `Gobo Shake` bursts (Pattern Jitter 64) as gobo
    wheel steps with every plain gobo scene parking the jitter. New roles
    `prism_rotation`, `gobo_shake`.
  - Evidence: suite 277 green (incl. 2 new dated tests in test_check.py and
    4 updated contracts in test_canonical_show.py); three shows regenerated,
    `--validate`d, `qlctool check` "ningun problema" on all three; docs
    (show-operation.md, checks.md) and TODO.md updated (on-site tuning +
    per-level rule extension pending).

- [x] 2026-08-28 - **Vibra Eventos (DMX):** the FLASH strobe no longer latches
      ("se queda el estrobo para siempre", owner, on the four pixel panels).
  - Cause: strobe channels are LTP and QLC+ restores nothing on Flash release
    (`Scene::handleFadersEnd` dismisses the fader; `Universe::processFaders`
    zeroes intensity channels only). Fixtures whose lit states rewrite their
    shutter each tick recovered; the WX panels, the seven PC-64 and the two
    mini heads have strobe-only channels that `shutter_open` deliberately
    left untouched, so no scene ever wrote them back to 0.
  - Fix: new `strobe_off_pairs` (`qlctool/strobe_off.py`) written beside every
    `shutter_open_pairs` in the scenes that own a fixture's light
    (colour, split-colour, pixel base, intensity levels, panel effects); new
    check rule `estrobo pegado` (`checks/rule_strobe_restore.py`, ERROR),
    sibling of `acento sin dueño`.
  - Evidence: dated test
    `tests/test_check.py::test_a_flashed_strobe_no_state_switches_off`; the
    rule found 39 latches on the old show and none after; suite 275 green;
    `qlctool check` "ningun problema" on the three regenerated `--validate`d
    workspaces.

- [x] 2026-08-28 - **Vibra Eventos (DMX):** `Humo Vertical` restored "como el
      antiguo" (owner's words).
  - Result: a `Humo Vertical` chaser (key N, page 2, latched on purpose) -
    the panels hold Effect 1 for 60 s then Effect 3 for 600 s, looping: the
    hand-built console's misnamed HUMO AUTO chaser (DeluxeEventos2 ID 367)
    carried verbatim, multicolour cycles and all - the owner chose the real
    old behaviour over the remembered white.
    `generate/vertical_smoke_light.py`.
  - Evidence: dated test
    `tests/test_internal_program.py::test_the_vertical_smoke_light_is_the_old_chaser_verbatim`;
    suite 274 green; `qlctool check` "ningun problema" (406 buttons) on the
    three regenerated `--validate`d workspaces.

- [x] 2026-08-28 - **Vibra Eventos (DMX):** the panels' 42 built-in effects
      are catalogued and the cycle pruned - the blocked item is closed.
  - Result: the owner ran all 42 at home over the FT232R and sent the
    catalogue material (Effects 1-3 by text - full-panel colour cycles -,
    4-21 as one video frame each; 22-42 without footage yet, not blocking).
    Verdict "estaban todos menos uno que va como con un contador de
    numeros": Effect 40 is the counter, and the hand-built chaser's own 41
    steps confirm it structurally (covers 1-42 minus exactly 40).
    `Ciclo Paneles` now cycles 41 of 42 (`EXCLUDED_FROM_CYCLE` in
    `generate/builtin_effects.py`); the scene stays on the library page.
    Catalogue: `~/p/DMX-Fixtures/docs/panel-effects.md`.
  - Evidence: dated test
    `tests/test_internal_program.py::test_the_number_counter_stays_out_of_the_cycle`;
    suite 273 green; `qlctool check` "ningun problema" on the three
    regenerated `--validate`d workspaces.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** the useful hand-built inventory is
      restored - the owner confirmed those functions were used ("esas
      funciones eran útiles").
  - Result, across three pushed commits on `qlctool` (c36fa3d, d4dbe03, and
    the beam-subsets one): `Escenario` (heads aimed at the stage, pan/tilt
    carried verbatim as measured data keyed by DMX address,
    `generate/stage_aim.py`) plus a `Centro` button in the movement solo
    frame; `Vel. Paneles` (Level slider over the panels' speed channel,
    `vc/level_slider.py`); `Dimmer Chase 2` (key B, every EFX fixture
    reversed) and `Dimmer Secuencia` (key M, the old 20s-breath/10s-programme
    rotation, holds verbatim from chaser ID 102); per-beam Prisma subsets
    (`1/2/3/4/1y3/2y4` in the prism frame) and `MultiColor BEAM` scenes (the
    half-colour channel, found as "the Colour channel that is not the
    wheel"). `Cabezas Reposo`/`Lento` deliberately not duplicated -
    `Cabezas Centro` and `Ola Suave` + speed dial cover them. Dimmer and
    subsets blocks implemented by Codex CLI against written specs
    (scratchpad prompts), reviewed line by line before commit.
  - Evidence: 266 tests green, `qlctool check` "ningun problema" on the three
    regenerated `--validate`d workspaces (405 buttons);
    `tests/test_beam_subsets.py`, `tests/test_stage_aim.py`, dimmer tests
    dated 2026-08-27.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** the flashes strobe again - the
      owner's live regression report, fixed same session.
  - Result: the owner, testing at home over the show's FT232R interface (Open
    DMX clone, Open TX @ 30Hz - settings verified correct against
    `~/p/qlcplus/plugins/dmxusb/src/`): "esto no hace estrobo y antes lo
    hacia". Audit of `DeluxeEventos2.qxw` confirmed it: the hand-built
    `Flash 100%`/`Flash 50%` drove every strobe channel (240/250/255 fast,
    70-220 slow - "50%" was half the *speed*, same brightness) and the
    generated flashes parked shutters "Open". Restored: all three flashes
    strobe (`Flash Color` on `.` is the old `Flash 100% Colores` - strobe
    over the running colour, RGB untouched, new `generate/flash_color.py`);
    `Strobo ON/OFF` now also drive bare unlabelled strobe-speed channels
    (Vortex ch5, panels ch5 - it was skipping 9 of 25 fixtures); panel
    internal-effect speed 200 (old show ran 160-255, not the blind 128); the
    bass audio bar moved off the now-strobing flash onto `Golpe Graves`, a
    plain white twin (a strobe fired by the PA is a strobe nobody chose).
    Three new checker rules with dated regression tests: `flash sin estrobo`,
    `estrobo en manos del audio`, `estrobo incompleto`; `intensidad` now
    accepts a labelled strobing shutter as lit. Old-show gaps that are real
    but not restored (Escenario, Cabezas Reposo/Lento, Dimmer Chase 2,
    Secuencia, prisma/multicolor subsets, panel-speed slider) recorded in the
    repo TODO; the old `HUMO AUTO` chaser turned out to fire panel effects,
    not smoke. (Correction, owner 2026-08-27: not broken - it was the light
    for the *vertical* smoke, panels on a white effect so the column reads.
    Recreating that look is tracked in the repo TODO.)
  - Evidence: `tools/qlctool` suite 260 green; `qlctool check` "ningun
    problema" on the three regenerated, `--validate`d workspaces;
    `tests/test_check.py::test_a_flash_that_lights_the_room_without_strobing_it`
    et al., dated 2026-08-27.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** EFX variety - rotation and serial
      cascades (Task 6, `~/p/DMX-Fixtures/TODO.md`).
  - Result: two new Serial-propagation figures - `Ola Suave` (washes, Line,
    28000ms Suave duration class) and `Cascada Beams` (beams, Circle,
    Rotation 45) - plus `Beam Diamante` (Rotation 90) and `Beam Hoja`
    (Rotation 45), new beam-family figures since the beam envelope had no
    Diamond/Leaf to rotate before this task (it was scoped to Circle/Eight/
    Line in the prior optics-family split). All three shipped workspaces
    regenerated (`qlctool newshow ... --validate`) and pass `qlctool check`
    clean; full pytest suite (261 tests) green.
  - Evidence: `tools/qlctool/tests/test_movement_families.py` (new, TDD:
    written red against the un-changed generator, confirmed failing, then
    made to pass); `qlctool check "QLC+ Setups/Vibra-split.qxw"` reports
    "ningun problema".
  - Engine-semantics check: read `~/p/qlcplus/engine/src/efx.cpp` and
    `efxfixture.cpp` before committing to Serial+Line for `Ola Suave`. Serial
    only delays a fixture's start via a modulo-wrapped elapsed timer
    (efxfixture.cpp:462-496) - no fixture gets stuck. Line's own direction
    handling (efx.cpp:337-347) phase-shifts a reversed (mirrored) fixture by
    PI instead of flipping the iterator like other algorithms, but since
    Line's path is `x=y=cos(iterator)`, `cos(t+PI) = -cos(t)`: the mirrored
    fixture lands exactly opposite the leader at every instant, the same
    result the 2*PI-iterator flip gives other shapes. No deviation needed;
    the literal spec (Line + Serial) works correctly.
  - Console: the "Figura que dibujan las cabezas" solo frame's per-button
    width is now computed from the shape count
    (`tools/qlctool/qlctool/generate/live_console.py`) instead of a fixed 88px
    step, so 9 buttons fit the existing 628px frame with no resize and no
    `rule_console` `_parent_bounds` containment violation.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** Peak's intensity becomes visible -
      the Dimmer Chase owns it (Task 7, `~/p/DMX-Fixtures/TODO.md`).
  - Result: `Nivel Peak`'s Collection no longer carries `Intensidad Total`
    beside `Dimmer Chase` - that pairing held every dimmer at 255 via HTP, so
    the chase's dips could never win and it ran all night for nothing
    (cosmetic since it shipped). Peak now hands its dimmers to the chase
    alone. A new capability-walk generator, `generate_dimmerless_intensity`
    (`tools/qlctool/qlctool/generate/dimmerless_intensity.py`), covers the
    fixtures the chase cannot reach at all (no dimmer role - found by
    `offsets_for_role(roles.DIMMER)`, never by name) with a static
    `Intensidad Peak` scene, so nothing goes dark. Verified on the shipped
    `Vibra-split.qxw`: `Nivel Peak` = {Rapidos Washes, Rapidos Beams, Gobo
    Animacion, Prisma Animacion, Dimmer Chase, Intensidad Peak}; `Intensidad
    Peak` lights fixtures 15/16 (MiN Wash shutter, offset 5 = 247, inside its
    Open range) and 32/36 (a shutter whose Open range is 0). Fiesta and every
    moment (including `Momento Locura`, which pairs the same chase with
    `Intensidad Total` on purpose) are untouched.
  - Rule decision: did NOT touch `checks/rule_shadowed_intensity.py`
    (`intensidad tapada`). It deliberately excludes EFX writes
    (`_dimmer_writes` only counts Scene/Sequence) because an EFX's output
    isn't one knowable value - confirmed this is why the bug shipped clean
    through the gate for months. Sharpening it to treat a Dimmer-mode EFX as
    a writer would also fire on `Momento Locura`'s identical shape, which is
    explicitly out of scope and still shadowed on purpose - a real false
    positive on a shipped workspace, not a missed catch. Fixed at the
    generator level instead, per the task's own fallback guidance.
  - Evidence: `tools/qlctool/tests/test_canonical_show.py::
    test_dimmer_chase_owns_peak_and_nothing_is_left_dark` (new, dated
    2026-08-27) reproduces the old shape via `driven_channels` and proves
    analytically that a static 255 (the DMX ceiling) shadowed every channel
    the chase drove, then confirms the fixed Peak has no such contest and
    that the no-dimmer fixtures still have an owner; updated the existing
    `test_auto_is_a_colour_bed_a_haze_and_an_energy_cycle` assertion (RED
    confirmed via `git stash` on just the generator change, then GREEN after
    restoring it). All three workspaces regenerated (`qlctool newshow ...
    --validate`) and pass `qlctool check` clean ("ningun problema" x3); full
    pytest suite (256 tests) green in the foreground.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** AudioTriggers widget bound - the
      bass band drives a Flash hit instead of shipping inert (Task 4,
      `~/p/DMX-Fixtures/TODO.md`).
  - Result: the bass band ("Graves") of the AudioTriggers widget is now bound
    to `Flash 100%`, one of the GOLPES hits (a Scene, Flash mode, Override,
    momentary, outside any solo frame) - not the `Blanco Total` room-state
    scene, which shares AUTO's solo frame and would have stopped AUTO with
    nothing to restart it (a ruling made mid-task when the original plan's
    premise turned out stale). Checker rule `disparador de audio vacio`
    extended with behavior (c): an audio-bound widget must not sit in a solo
    frame alongside other monitored functions.
  - Evidence: commits abfeedc..a4ed141 (`show: the bass gets a hand back, and
    an empty ear is now a finding` / `show: the bass hits a Flash, not a room
    state, and the check sees why`); `tools/qlctool/tests/test_check.py`;
    `qlctool check` on all three shipped workspaces reports "ningun problema"
    (re-verified 2026-08-27 after the Task 9 regen).

- [x] 2026-08-27 - **Vibra Eventos (DMX):** GrandMaster reachable from the
      console - a slider added (Task 3, `~/p/DMX-Fixtures/TODO.md`).
  - Result: a GrandMaster-mode Slider widget was added to the console, giving
    the operator a control over the workspace's existing
    `<GrandMaster ChannelMode="Intensity" ValueMode="Reduce">`, which no VC
    widget reached before.
  - Evidence: commit a1527af (`console: the grand master gets a handle`);
    `qlctool check "QLC+ Setups/Vibra-split.qxw"` clean.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** Blackout button added beside
      StopAll (Task 2, `~/p/DMX-Fixtures/TODO.md`).
  - Result: "SI ALGO VA MAL" now carries a second panic button using the
    existing-but-unused `Blackout` VC button action (`vc/button.py:23`),
    distinct from StopAll (stops functions vs. forces every DMX output to
    zero).
  - Evidence: commit edaee93 (`console: a second panic - blackout, not
    stop`); `qlctool check` clean on all three shipped workspaces.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** RGB script repertoire curated past
      Fill/Even-Odd/Waves/Strobe (Tasks 5/6, `~/p/DMX-Fixtures/TODO.md`).
  - Result: 10 curated matrix scripts across the three grid shapes
    (BarrasLed 8x2, Cabezas 12x1, PAR 15x1), each with deliberate
    `<Property>` parameters and multi-colour via indexed Color where it
    reads. Matrices per group went from 90 to 100 in the shipped shows.
  - Evidence: commits 3d7b80d, 213ca2f (`rig: the matrix library learns nine
    new tricks` / `console: a widget can spill past its own frame, not just
    the canvas`); `tools/qlctool/tests/test_rgbmatrix_generation.py`,
    `test_matrix_step_count.py`; `qlctool check` clean on all three, full
    pytest suite green.

- [x] 2026-08-27 - **Vibra Eventos (DMX):** Web-interface-for-on-site-sessions
      audit item folded into the ops runbook (Task 8,
      `~/p/DMX-Fixtures/TODO.md`).
  - Result: `docs/show-operation.md` now documents `qlcplus -w` (port 9999,
    phone-on-the-rig operation) and `-k -f -o show.qxw` kiosk startup for the
    show Mac. The caveats (kiosk mode has no on-screen exit; `-p`/`-c` are
    v4-only) were independently confirmed against the installed 5.2.2 binary
    in Task 1's verification pass, not just asserted.
  - Evidence: commit fa9ebdb (`docs: how the show starts itself and fits in a
    pocket`); `docs/qlc5-verification.md` (Task 1, commits 30b142b..4394dae).

- [x] 2026-08-26 - **Vibra Eventos (DMX):** The LED bars now change colour with
  the show instead of "a su bola", and the dark panels in the 3D preview turned
  out to be the simulator, not the file.
  - Owner, over the 3D preview: bars magenta while the rig was cyan, and the
    WX-60WPS panels showing nothing under AUTO. Two separate causes.
  - Bars: two colour clocks - `Rueda Colores` rotating scenes over the rig and
    `Ciclo Matrices BarrasLed` rotating its own six-colour palette over the
    bars - and QLC+ cannot slave one chaser's steps to another's. Fixed by
    making each wheel step a Collection that starts the rig scene *and* a bars
    matrix of the same colour (algorithm rotating Fill/Even-Odd/Waves/Solid,
    paced so a full pass fits the 2500 ms step); the standalone cycle left
    AUTO and the moments but stays on the console. New rule `relojes de color`
    (`rule_colour_clocks.py`) recognises the shape - a room state starting two
    chasers whose steps state different colours - and fired on AUTO plus three
    moments in all three shipped shows before the fix, on none after. Dated
    regression test `test_two_colour_clocks_ticking_in_one_room_state`.
  - Panels: the file was right all along (`Paneles - Effect N` writes ch1=255,
    ch6=128 = Auto Mode 86-171, ch7=effect, ch8=128, checked against the
    definition), but in Auto Mode the fixture makes its colours in hardware
    with RGB at 0, and QLC+'s 3D renders RGB channels - nothing to show.
    Only the venue can judge the 42 effects; noted on the blocked TODO item.
  - A wrong turn worth keeping: a WebFetch summary of `rgbmatrix.cpp` said
    QLC+ 5 does not persist blend modes; the local clone at `~/p/qlcplus`
    shows `BlendMode` is a `<Function>` attribute (`function.cpp:918`) with
    MaskBlend implemented multiplicatively (`universe.cpp`). Not used - mask
    depends on tick write order and the checker's HTP model cannot see it -
    but recorded on the TODO item, and the clone is now in the repo CLAUDE.md
    as the place to read QLC+ behaviour from.
  - Evidence: `qlctool check` clean on the three regenerated workspaces
    (`Vibra.qxw`, `Vibra-beats.qxw`, `Vibra-split.qxw`, each `--validate`d in
    headless QLC+ 5.2.2), 224 tests passing in `tools/qlctool`.

- [x] 2026-08-25 - **Vibra Eventos (DMX):** Found why the generated show stopped
  the moment AUTO was pressed, and rebuilt the console for the show laptop.
  - Root cause 1, the one that killed AUTO: every generated Virtual Console
    frame was a `SoloFrame` grouped by UI folder, so AUTO sat next to buttons
    for the very functions it starts. A Toggle button emits `functionStarting`
    whenever its function starts - including when another function started it
    (`VCButton::slotFunctionRunning`) - and `VCSoloFrame` answers by stopping
    every other widget's function. Press AUTO, AUTO starts `Rueda Colores`,
    that button reports it, the frame stops AUTO. 16 such clashes in the old
    file, verified by replaying the rule over `git show HEAD:Vibra.qxw`;
    identical code in the 4.x and 5.x sources.
  - Root cause 2, independent: `build_chaser` wrote
    `<Speed Duration="0">` with `<SpeedModes Duration="Common"/>`, and Common
    means every step lasts the chaser's duration, not its own `Hold`. QLC+
    advances when `elapsed >= duration` (`ChaserRunner::write`), so duration 0
    walks a step per engine tick - all 1500/10000/60000 ms holds, the smoke
    burst included, were dead. Now Common with a real duration where the steps
    are uniform, `PerStep` only where they differ (the smoke burst/pause),
    because a Speed Dial and `Chaser::tap()` only reach a Common chaser.
  - Console rebuilt: `generate/live_console.py` replaces the two-pass
    `vc_layout` (which also emitted every button twice). Fixed 1440x900, three
    columns, colour banks on keys 1-0, mixes and the 90 matrices in multipage
    frames, XY pad over the twelve movers, two speed dials, audio triggers.
    272 -> 278 buttons, extent 1432x876, canvas no longer 2662px tall.
  - Also: macOS validation now launches QLC+ with `open -g` and reads
    `~/QLC+.log` (`-g`), so a generate-and-validate run no longer steals focus;
    falls back to the foreground launch when `open` refuses.
  - Evidence: `cd ~/p/DMX-Fixtures/tools/qlctool && .venv/bin/python -m pytest
    tests/ -q` -> `87 passed`, including new tests
    `test_no_chaser_walks_itself_at_engine_speed`,
    `test_the_smoke_chaser_bursts_then_waits` and the five in
    `tests/test_live_console.py`; and
    `qlctool newshow "QLC+ Setups/DeluxeEventos2.qxw" --validate` ->
    `Validated: QLC+ loaded it with no complaints`.
  - Console parity finished the same day: `generate/dimmer_chases.py` (an EFX in
    Dimmer mode with the fixtures phase-spread, plus an odd/even ping-pong),
    `generate/strobe_effects.py` (shutter strobes only where the fixture
    definition labels a strobe range - a MiN Wash puts "Closed" at 1-7 - plus
    two flash chasers over `Flash 100%`/`Todo Negro` at 50 and 250 ms), and
    `vc/matrix_control.py` (the `<Matrix>` widget; QLC+ 5 renamed the class to
    VCAnimation but kept the tag). Audio bands bound to Toggle buttons only:
    a bar calls `pressFunction` up *and* down, so a Flash target would latch.
    Final: 288 functions, 284 buttons, extent 1432x890.
  - Reference: shallow clone of `mcallegari/qlcplus` at `~/p/qlcplus`, kept for
    reading `engine/src/chaserrunner.cpp` and both `virtualconsole/` trees.

- [x] 2026-08-24 - **Vibra Eventos (DMX):** Pointed the brain's show-Mac access
  section at the SSH alias instead of the drifting DHCP address.
  - Result: `business/access-map.md` "Vibra show MacBook (Oficina)" now leads
    with `ssh vibra-oficina` (alias added to `~/.ssh/config` 2026-08-24,
    resolves `MacBook-Pro-de-Oficina.local`), keeps the IP only as context, and
    gained two traps found while using the machine: `/usr/bin/git`, `strings`
    and friends die there with `xcrun: error: invalid active developer path`
    (no Command Line Tools) so a non-interactive `ssh vibra-oficina git ...`
    needs `export PATH=/usr/local/bin:$PATH` for Homebrew git 2.37.3; and QLC+
    5.2.2 reads its custom fixture definitions from
    `~/Library/Application Support/QLC+/Fixtures`.
  - Evidence: brain commit "access-map: vibra-oficina alias leads, brew git and
    QLC+ paths on the show Mac".

#### 2026-08-26 — Vibra Eventos (DMX / lighting)

Backlog moved to `~/p/DMX-Fixtures/TODO.md`, the repo that owns the work.
Closed on the way out:

- Decide where the four BEAM 230W 7R take their colour from — owner chose
  taking them out of the `BarrasLed` group (2026-08-26). Done: `qlctool patch
  --group-remove`, both patches, cells left empty. All three workspaces now
  report zero findings.
- Centralize the `qlctool` toolkit inside the `DMX-Fixtures` repo rather than
  a separate repo (owner leaning yes 2026-08-24 — "así lo tenemos todo
  centralizado"). Built there under `tools/qlctool/` on branch `qlctool`; moves
  with the repo when the org is renamed.

#### 2026-08-29 — Vibra Eventos: the 7R under AUTO

Two faults the owner reported live, with nothing pressed but AUTO ("solo he
pulsado el auto"). Both were the show, not the fixture definition.

- [x] "Las 7R no se abren del todo, están como una media luna." Cause:
  `Rig Multicolor 1` and `Rig Multicolor 2` - two of the twenty steps of the
  colour clock, hence "a veces" - sent the BEAM 230W 7R's colour wheel to 186,
  inside its `RotationClockwiseFastToSlow` range and near the slow end. A
  rotation range is not a colour: the wheel creeps between detents and a
  2-degree beam shows half of one colour and half of the next.
  - Fix: `generate/multicolor_scene.py` deals the wheel fixtures a real detent
    from the palette, the way `Rig 4 Colores` already did (new
    `generate/dealt_wheel_color.py` walks the deal forward to a colour the
    wheel actually carries). Rotation now survives only on the two explicit
    `Color Beam - Rainbow ...` buttons.
  - Check: `checks/rule_wheel_rotation.py` (`rueda de color girando`), plus
    `test_a_rig_colour_that_spins_the_beams_wheel_instead_of_naming_one`.
- [x] "Las 7R no se mueven." Cause: `Nivel Ambiente`, the first and longest
  step of `Ciclo Energia`, started the washes' slow shapes beside the *static*
  `Beams Abanico` scene, so the four beams held one position for the level's
  whole four-minute hold.
  - Fix: a slow beam family (`BEAM_SLOW`, chaser `Movimientos Suaves Beams`)
    now owns the beams at that level and in `Momento Tranquilo`; the fan stays
    as one step of the normal beam rotation.
  - Check: `checks/rule_parked_movers.py` (`cabezas paradas en el ciclo`), plus
    `test_a_level_of_the_cycle_that_parks_half_the_movers`.
- Evidence: all three workspaces regenerated and validated in headless QLC+;
  `qlctool check` reports `427 botones revisados, ningun problema` on each;
  `pytest tests/ -q` -> 320 passed in 327.68s.

#### 2026-08-29 — Vibra Eventos: the beams were aimed at nothing

- [x] "Está todo el rato haciendo un circulo pequeño en el suelo." Cause: every
  movement EFX the generator has ever written carried QLC+'s own axis default,
  `<Axis Name="Y"><Offset>127` - the raw middle of the tilt channel - because
  `EFXAxis.offset` defaults there and no caller had overridden it. Mid-travel
  is not an aim; on this rig it is the floor. The hand-built show was no better
  aimed (offset 130) and got away with it by drawing every figure 100 wide.
  The beams' ambient envelope, 26x18 that afternoon, was small enough to keep
  the whole figure inside that spot.
  - Axis evidence, all measured: tilt 0 = ceiling (`docs/rig.md`, a CromoWash
    stuck at coarse zero), 127 = floor (owner watching the cycle), ~196 = the
    stage (the hand-built `Escenario` aiming the four 7R). Up is a *smaller*
    number.
  - Fix: `generate/movement_aim.py:BEAM_TILT_AIM = 88`, threaded through
    `generate_movement_efx(tilt_offset=...)` into the EFX Y axis; every beam
    envelope carries it. `BEAM_SLOW` resized 26x18 -> 45x30. `Beam Circulo`
    now sweeps tilt 50..126 instead of 89..165.
  - Check: `checks/rule_unaimed_movement.py` (`movimiento sin apuntar`), plus
    `test_a_beam_figure_centred_on_mid_travel`. Scoped to the beam family: a
    wash's wide cone survives mid-travel, a 2-degree needle does not.
  - Open: 88 is a first aim in raw DMX, like the fan's. `TODO.md` carries the
    on-site confirmation.
- Evidence: three workspaces regenerated and validated in headless QLC+;
  `qlctool check` clean on each; `pytest tests/ -q` -> 318 passed in 325.74s
  (the count moved from 320 because the glob-parametrised roundtrip tests
  follow QLC+'s `.autosave.qxw` files, one of which QLC+ removed).

#### 2026-08-29 — Vibra Eventos: the crescent was the blade, and the aim was backwards

The owner corrected both diagnoses live, from the desk. Recorded because both
of my first answers were wrong in the same way: reasoning about the show
instead of asking what the channel does.

- [x] **The media luna was never the colour wheel.** "El canal 7 de cada 7R
  está a la mitad en vez de abierto del todo" (owner, reading the DMX).
  Channel 7 is the 7R's dimmer, and on a 7R that is a mechanical blade across
  the aperture, not a fader: at 110 - what `Intensidad Ambiente` wrote to every
  dimmer in the rig, held for the quiet level's four minutes - it covers half
  the lens. The colour-wheel rotation I fixed earlier that day was a real
  fault, but it was not this one.
  - Fix: the `.qxf` now declares the dimmer in three ranges (closed / partial
    blade / open), `stepped_dimmer.py` reads "a dimmer described in steps is
    not a fader" off that, `energy_intensity` gives such a dimmer full instead
    of the level value, `dimmer_chases` leaves those fixtures out (an EFX
    sweeping a blade is a chase of half-moons) and `dimmerless_intensity`
    owns them at full in the peak level instead.
  - Check: `checks/rule_stepped_dimmer.py` (`dimmer a medias`), two dated
    regressions - the fraction and the sweeping EFX.
  - Verified in the regenerated file: the 7R dimmer now carries only 0 and 255
    across all 566 functions, and no Dimmer-mode EFX touches them.
- [x] **The beams' aim was 180 degrees out.** The first fix moved them from
  tilt 127 to 88 and the owner reported "ahora los 7R apuntan a la pared". So
  on a 7R the room is *above* mid-travel, not below - which the hand-built
  show had already said, aiming them at 189-204. `BEAM_TILT_AIM` is 170 now,
  and `fan_position.TILT` follows it instead of its old 105 guess.
  - The washes are the other way round on their own scale: 128 is the wall
    ("los washes apuntan para atrás a la pared, que no me interesa iluminar"),
    ~46 is the room (the hand-built `Escenario` on CromoWash #1/#2, tilt 49/43).
    `WASH_TILT_AIM` is 88, and the wash figures lost height (55/50 -> 30/32)
    so a shape centred in that band no longer climbs back onto the wall.
  - Both numbers, and which way each scale runs, are in
    `generate/movement_aim.py`. Guessing the direction cost a pass.
- Evidence: three workspaces regenerated and validated in headless QLC+;
  `qlctool check` clean on each; `pytest tests/ -q` -> 323 passed in 327.78s.

#### 2026-08-29 — Vibra Eventos: the audience window, and the pump that never stopped

- [x] **The beams' aim, third and last pass.** Guessing the direction failed
  twice (floor, then wall). The owner ended it by putting BEAM 230W 7R #1 on
  the desk and sending the corners of where the people are: **pan 62-103, tilt
  207-234**. That is now `qlctool/audience_window.py`, read by both the
  generator and the check. Aims come off its centre, figures are sized by its
  half-width; `Beam Circulo` draws pan 62-102, tilt 207-233, and the fan and
  cross open across the same window.
  - Check: `checks/rule_beam_window.py` (`figura fuera del publico`), with a
    dated regression. Only head #1 is measured - the other three sit elsewhere
    on the truss and share this window until somebody reads them.
- [x] **The vertical fog never stopped.** "Le doy y nunca se para, se supone
  que solo debe tirar cuando le de." `Humo Vertical YA` is a Flash, and a
  Flash restores nothing on release: the Fog channel is LTP and no room state
  ever wrote it, so the first press fogged until the workspace was reloaded.
  Same latch as `rule_strobe_restore`, on the channel that empties a tank.
  - Fix: `fog_off.py`, wired into both intensity levels, the blackout and the
    flat work-light scenes - every room state now holds the pump at zero.
  - Check: `checks/rule_smoke_restore.py` (`humo pegado`), which reported the
    shipped file before the fix and is silent after it.
- Evidence: three workspaces regenerated and validated in headless QLC+;
  `qlctool check` clean on each; `pytest tests/ -q` -> 322 passed.

#### 2026-08-31 — Vibra Eventos: the backlog's repo-side work, cleared

Seven items closed. Everything left in `TODO.md` needs the rig, the owner, or
somebody outside this machine; the disposition is written at the top of that
file.

- [x] **A dying QLC+ handed its complaints to the next workspace.**
      `test_qlcplus_loads_the_show` failed once under the full suite with
      "fixture 13 overlapping with fixture ..." while passing in isolation
      (2026-08-25). Cause: QLC+'s `-g` log has one hard-coded path
      (`~/QLC+.log`) opened in **append** mode, so every validation shares it,
      and a QLC+ still shutting down from the previous test keeps writing -
      including the complaint a neighbouring test had deliberately built.
  - Fix: `validate.py` slices the log from the last
    `QLCFixtureDefCache::load(const QDir &)` (the signature spelled out because
    `loadMap` is the very next line and wins a prefix match), and remembers
    processes it could not reap so the next launch waits for them.
  - Evidence: `tests/test_validate.py`, three dated regressions; the full suite
    run three times in a row, green each time.
- [x] **`estrobo pegado` and `acento sin dueño` merged a state's steps.** From
      the 2026-08-28 Codex review: both rules unioned everything a room state
      reaches at any step, so the level that parks a strobe or a prism parked it
      on behalf of every level that does not.
  - Fix: `checks/unowned_instant.py` answers "is there an instant where the
    fixture is lit and this channel unwritten" with two booleans per node -
    `any` over a chaser's steps, `all` over a collection's members - so no
    instant is ever enumerated. It over-approximates (it assumes concurrent
    chasers can be caught in any combination of their steps) and says so; the
    union it replaces erred the other way, silently.
  - Evidence: dated regression in `test_check.py` that keeps the panels'
    strobe-off in exactly one step of `Ciclo Paneles`, asserts the old merged
    reach still covered every lit state, and asserts the rule now bites. Proved
    to fail against the old union logic before being kept.
- [x] **The Chauvet MiN Wash's `5 Channel` mode was invented.** No Tilt on a
      moving head, and an `ActsOn` pointing at "Reserved". No manual for this
      fixture in `Manual/`, none in QLC+'s own library, so there was nothing to
      correct it against - and a guessed channel order drives the wrong channels
      in silence. Deleted; the patch only ever used the 13-channel mode.
- [x] **`qlctool patch` could not move a head already in a group.** Which is why
      the split's `PAR` group is a 7x3 with the CLB2.4 heads bolted to the side.
      New `repatch/group_head_move.py` and `--group-move "GROUP=FIXTURE[:HEAD]@X,Y"`;
      the head number matters because `BarrasLed` is sixteen heads of two
      fixtures. Refuses an occupied cell, an off-grid cell, and a head that is
      not in the group. Five tests; re-laying the group itself stays in `TODO.md`
      because it changes what every matrix paints.
- [x] **`docs/smc-pad-led.md` still said the LED colour encoding was unsolved**,
      months after the bridge shipped. Rewritten to lead with what runs today
      and keep the dead ends as dead ends. The same stale tail was in
      `tools/smc-pad/README.md` (two sections contradicting the "SOLVED" above
      them, an `ON_COLOR`/`OFF_COLOR` pair that no longer exists, and a
      "unplug USB" instruction the device had already disproved) - removed.
- [x] **`tools/qlctool/README.md`'s `newshow` example did not run.** It
      regenerated from `DeluxeEventos2.qxw`, two fixtures behind the plot
      ("the plot places fixtures that are not patched: [27, 28]"). Now
      regenerates `Vibra.qxw` from itself; the corrected command was run.
- [x] **`DeluxeEventos2.qxw`'s "Velocidad Cabezas" slider did nothing** - a
      Level slider with no `<Channel>` under it and a `<Playback>` pointing at
      no function, and QLC+ has no speed-slider mode at all. Deleted; the
      workspace still loads clean in headless QLC+.
- Second reviewer: one read-only `codex exec` over the whole diff. It found
  three real defects - the prefix-matching log marker, the head-0-only
  `--group-move`, and the exactness claim in `unowned_instant.py` - all three
  verified against the code and fixed before the commit.
- Evidence: `pytest tests/ -q` -> 338 passed; `qlctool check` clean on
  `Vibra.qxw`, `Vibra-beats.qxw` and `Vibra-split.qxw` (430 buttons each);
  `qlctool validate` clean on `DeluxeEventos2.qxw`.

#### 2026-08-31 — Vibra Eventos: the grids, and what pulling that thread found

The owner authorised changing the grid ("si tenemos que cambiar la rejilla o lo
que sea habrá que hacerlo"). Two backlog items; the first one turned out to be
stale and the second one was hiding three real defects.

- [x] **The fixture groups were in cabling order.** A matrix paints the cells a
      group declares and half of QLC+'s scripts mean a direction, so cell 0 has
      to be at one side of the room. Nothing enforced it: a group is built in
      DMX address order, so `Cabezas` walked its four rigged beams 1916, 9694,
      4405, 7205 mm across the stage and the split's `PAR` jumped twice. Every
      sweep over those groups went left, far right, back to the middle - and it
      is invisible in the XML and in the 3D view, which draws each fixture where
      it really stands.
  - Fix: `repatch/group_sort.py` and `qlctool patch --group-sort GROUP`, laying
    a group out by the `<Monitor>` positions the plot writes. Ties break on the
    cell the head already had, so a bar's eight segments keep the bar's order.
  - Check: `checks/rule_grid_order.py` (`rejilla fuera de orden`), which
    reported both shipped patches before the fix. It also reports a not-rigged
    spare sitting among the rigged cells: eight of `Cabezas`' twelve members are
    spares in flight cases, and a cell the matrix paints with nothing in it is a
    hole in every sweep.
- [x] **The two MAC WASH had no group, and their definition had no heads.**
      Grouping them is what gives them a colour bank and a matrix. Their
      23-channel mode is three concentric RGBW rings and declared no `<Head>`:
      QLC+ then builds one head holding every channel and keeps the *last*
      channel of each colour (`QLCFixtureHead::cacheChannels`), so a matrix
      would have painted the outer ring and left the other two on whatever was
      written last.
  - Fix: three `<Head>` blocks in the `.qxf`, one per ring. RGBW only - pan and
    tilt fall back to the mode's channels and the dimmer is resolved separately.
  - Check: `checks/rule_undeclared_heads.py` (`cabezas sin declarar`), counting
    the heads that hold a red, a green and a blue rather than the elements.
  - The group is `Lyres`, 3x2: ring across, fixture down.
- [x] **`Pixeles ON` owned half of a matrix-lit fixture.** It is what holds one
      open, since a matrix writes RGB and nothing else, and it wrote dimmer,
      shutter and strobe-off but neither the zoom nor the mode channel. An
      unwritten zoom is 0 - the narrowest beam these heads have - and an
      unwritten mode channel leaves the head free to run its own programme under
      a matrix that believes it is painting it. That last one is the owner's own
      report from the night of 2026-08-29, "cambios de colores muy rapidos".
  - Caught by `zoom sin declarar` and by
    `test_every_colour_look_takes_the_washes_off_their_own_programme`, both the
    moment the group existed.
- [x] **The fifth group pushed the console off the screen.** The manual page's
      left column is one frame per group at a hard-coded 128px pitch, so the
      dimmer frame, four chases and both strobe buttons went below a 900px
      screen - unreachable, while the generator's summary still claimed it
      fitted. `vc/bank_pitch.py` derives the pitch from the room available;
      `consola` measures the result.
- [-] **"Re-lay the split's PAR group as 8x2"** was stale: it is a flat 15x1 and
      has been for some time. What was actually wrong with it was the order, now
      fixed above.
- Second reviewer: two read-only `codex exec` runs over the diffs. The first
  found three defects (a prefix-matching log marker, a head-0-only
  `--group-move`, an exactness claim in `unowned_instant.py`); the second found
  three more (the sort tie-breaking on head index and interleaving co-located
  fixtures, the grid rule ignoring hidden fixtures its own fixer would move, and
  the head rule counting `<Head>` elements rather than heads holding a colour).
  All six verified against the code and fixed, with tests, before the commits.
- Evidence: `pytest tests/ -q` -> 352 passed; three workspaces regenerated and
  loaded clean in headless QLC+; `qlctool check` silent on each (503 buttons).

