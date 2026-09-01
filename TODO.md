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

**Disposicion, 2026-08-31.** Se cerro todo lo que se podia cerrar sin el rig
(nueve items, en `~/p/TODO_LOG.md`), incluida la rejilla: los grupos van ya en
orden de escenario y las dos MAC WASH tienen grupo propio. De lo que queda,
ninguno de los 38 `[ ]` y 7 `[~]` esta esperando a que alguien escriba codigo:

- **La mayoria espera al rig o al dueño** - humo, el RunMode de las lyres, la
  rejilla nueva, el tilt de las cabezas, el foco de los beams, los flashes, los
  niveles de energia, los thresholds de audio, el probe de los cuatro fixtures
  sin documentar y el pad en sala. Un valor DMX adivinado
  desde aqui es exactamente el fallo que este repo persigue.
- **Cuatro esperan a algo externo**: renombrar la org de GitHub, el PDF del
  SMC-PAD (el sitio da 403 a `curl`), `xcode-select` en el Mac del show (fuera
  de red), y comprar el reemplazo del dongle DMX.
- **Dos esperan una decision del dueño**: quedarse con `Vibra-split.qxw`, y
  mezclar la rama `qlctool` en `main`.
- **La auditoria de capacidades de QLC+** (sliders, MIDI, paletas, XY pad,
  ControlMode, VC Clock) no son defectos: son cosas que el show podria adoptar,
  y cada una cambia como se opera. Se deciden, no se implementan de oficio.

- [ ] **Ver en sala lo que cambio la rejilla (2026-08-31).** Tres cosas nuevas,
  todas correctas sobre el papel y ninguna vista todavia:
  1. **Las dos MAC WASH ya tienen grupo propio, `Lyres`, 3x2** — una celda por
     anillo (son tres anillos RGBW concentricos). Traen banco de color propio y
     matrices propias. Mirar que los anillos pinten los tres, no solo el de
     fuera, y que el patron sobre 3x2 se lea como algo y no como parpadeo.
  2. **Las celdas de todos los grupos van ahora en orden de escenario**, no de
     patch. `Cabezas` iba 1916, 9694, 4405, 7205 mm: un barrido salia a la
     derecha, saltaba a la izquierda y volvia. Ahora barre de verdad. Mirar un
     Fill o un Stripes sobre `Cabezas` y sobre `PAR` y confirmar que cruza la
     sala en una direccion.
  3. **La consola crecio de 430 a 503 botones** con el banco nuevo, y la columna
     de bancos de la pagina manual se encoge para que quepan. Los marcos pasan
     de 122 px de alto a 102. Confirmar que se sigue leyendo a 13".

- [ ] **Humo, las dos cosas nuevas, verlas en sala (2026-08-30).** (1) La
  columna vertical ya no se pinta de blanco: `Humo Vertical YA` escribe solo la
  bomba y el master del LED, y el color lo pone la sala — "salia humo bien pero
  la luz solo salia la blanca, no hacia las transiciones de colores". Con AUTO
  corriendo la columna deberia salir del color de la rueda; con `Todo Negro`
  saldra a oscuras, que es lo correcto pero conviene verlo. (2) El humo de
  ambiente tiene su ritmo en la pagina 1, abajo: `cada 1 / 2 / 4 / 8 min`, marco
  solo (uno a la vez), y `J` sigue siendo el de 1 min que arranca AUTO. Elegir
  el que pida la sala. La columna **nunca** se dispara sola y la regla
  `columna automatica` lo impide.

- [ ] **Las dos MAC WASH: mirar el menu RunMode en la lyre (2026-08-30).** La
  noche del 29 "se quedaban mirando para abajo y hacian cosas raras como una
  especie de cambios de colores muy rapidos", con el workspace ya recargado y
  con la ventana medida (tilt 221) puesta. Ninguna funcion del show hace eso:
  el color va en una rueda de ocho tiempos y el movimiento estaba apuntado, o
  sea que la lyre no estaba obedeciendo DMX. El manual (`Manual/Mac Mah MAC
  WASH 1915Z`, seccion V, MENU) da `RunMode: DMX / AUTO / SOUND` — en SOUND
  cambia de color con la musica, que es exactamente lo que se vio. **En sala,
  en el display de cada cabeza:** `RunMode = DMX`, `Channel = 23CH`,
  `DMX Addr = 345` y `368`. Del lado del fichero ya esta hecho lo que se podia
  hacer: cada look que da color escribe ahora el canal `Function Mode` a 0
  (`mode_park.py`) y la regla `modo sin dueño` no deja que ningun fixture se
  quede con ese canal sin escribir. Si con el menu en DMX sigue pasando, lo
  siguiente es la cadena: las dos van al final del universo (345-390) detras de
  las cuatro maquinas de humo, con el FT232R sin buffer y sin terminador.

- [ ] **Medir el foco de los beam en sala (2026-08-30).** Nada escribia el
  canal `Focus` de las 7R, o sea que los diecisiete gobos se han proyectado
  siempre con el foco en un extremo de su recorrido — la mitad de por que "se
  echaba en falta mas variedad". Ahora todas las escenas de gobo escriben
  `BEAM_FOCUS = 127` (`generate/canonical_show.py`), que es el medio del
  recorrido y una primera pasada, no una medida. En sala: poner un gobo,
  subir/bajar ese canal a mano hasta que el dibujo este nitido a la distancia
  real, y dejar ese numero en la constante. Mientras tanto tambien hay
  `Gobo Repartido 1-8` (cada cabeza un gobo distinto) y el prisma girando en
  tres velocidades: mirar si el reparto se lee bien o marea.

- [ ] **El pad, la proxima vez: USB o Bluetooth, no los dos (2026-08-30).** La
  noche del 29 "no pude usar el pad porque ni reseteandolo reconocia las
  teclas", con el cable y el BT puestos a la vez. Causa, ya medida y escrita en
  `tools/smc-pad/README.md`: **con USB conectado el pad manda su MIDI por USB y
  el lado BLE se queda mudo**, y el workspace escucha el puerto `ble device`.
  Resetear el pad no arregla eso. Comprobar en sala: quitar el USB (que es
  ademas lo que quiere el puente de LEDs, que sostiene el BLE), o dejar el USB
  y en Entradas/Salidas apuntar el universo 1 al puerto USB y **guardar el
  fichero** — `newshow` respeta el puerto que el fichero ya trae.
  `swift tools/smc-pad/midiports.swift` lista los puertos con el nombre que usa
  QLC+ (propiedad `Model`), que es lo unico que permite saber cual es cual.

- [ ] **Afinar el tilt al que apuntan las lyres en sala (2026-08-29).**
  Segunda pasada: el primer intento mandó las 7R a tilt 88 y salieron a la
  pared, o sea que en una 7R la sala está **por encima** de 127, no por debajo
  (el show a mano ya lo decía: su `Escenario` las pone en 189-204). Ahora
  `BEAM_TILT_AIM = 170` y el abanico va con ellas. Los washes corren al revés
  en su propia escala: 128 es la pared, ~46 es la sala (el `Escenario` a mano
  pone las CromoWash en 49 y 43), y `WASH_TILT_AIM = 88`. Falta confirmar los
  dos en sala. Todo
  el movimiento generado iba centrado en tilt 127 - el centro del recorrido,
  que es lo que escribe QLC+ cuando nadie apunta - y en este rig eso es el
  suelo: "está todo el rato haciendo un circulo pequeño en el suelo". Ahora
  hay un solo número, `generate/movement_aim.py:BEAM_TILT_AIM = 88`, y todas
  las figuras de beam se dibujan alrededor de él (recorrido 50..126 en
  `Beam Circulo`). Los tres puntos conocidos del eje: **0 = techo**
  (`docs/rig.md`, una CromoWash clavada en 0), **127 = suelo** (el dueño
  mirando el ciclo), **~196 = escenario** (el `Escenario` del show a mano).
  O sea que **subir es bajar el número**. Falta mirarlo en sala y decir si 88
  cae donde se quiere: si sale demasiado alto subir el número, si sigue bajo
  bajarlo, y regenerar. Los washes siguen en 127 a propósito - nadie se ha
  quejado de ellos y un cono ancho aguanta el centro del recorrido.

- [ ] **Las dos MAC WASH 1915Z, tres cosas que hay que ver en sala
  (2026-08-29).** Llegaron en lugar de las CromoWash, parcheadas en 23 CH en
  DMX 345 y 368, en el sitio de las CromoWash del back truss (4 y 7); las
  CromoWash siguen parcheadas y aparcadas como spares en el plano. El manual
  oficial de Mac Mah está en `Manual/` y sólo da la tabla de canales: tres
  cosas no las dice y están puestas por cómo funciona la plataforma:
  1. **Qué extremo del zoom es abierto.** La definición declara `SmallToBig`,
     así que el show manda 255 en todo look que las enciende
     (`zoom_wide_pairs`). Si en sala salen cerradas, es cambiar el preset de
     esa capacidad a `BigToSmall` en el `.qxf` y regenerar.
  2. **El estrobo.** Declarado 0-10 sin estrobo, 11-255 de lento a rápido.
  3. **El canal Function mode.** Declarado 0 = control DMX. Si en 0 la lyre
     corre un programa propio, ignorará el RGB del show.
  Y confirmar en el 3D que las dos caben donde estaban las CromoWash (son algo
  más grandes: 325x188 mm contra 296x184).

- [~] **SMC-PAD LED feedback en QLC+ — funcionando, con pulido pendiente
  (2026-08-29).** Todo el protocolo resuelto y documentado en
  `tools/smc-pad/` (README + decompile). El puente `qlc_led_bridge.swift`
  mantiene la sesión GATT del pad, publica el puerto MIDI virtual
  "SMC-PAD LED Bridge" y pinta cada pad con su color de paleta
  (`generate/smc_pad_colors.py`): atenuado en reposo, full al activarse el
  botón en QLC+. Los botones de la consola llevan el mismo color. Verificado:
  QLC+ feedback -> pad enciende. **Se instala una vez con
  `tools/smc-pad/install-bridge.sh`** y arranca solo en cada inicio de sesión
  (agente de launchd, `.app` firmada, se resucita si se cae — verificado
  2026-08-29 matándolo). Cargar `Vibra.qxw` después del puente, no antes. En
  Entradas/Salidas el universo 1 debe tener Input "ble device" (omni "1-16") y
  el bridge como Output **y Feedback** (el `<Feedback>` es el truco: el ojo de
  QLC+ no lo crea solo; ya está en el .qxw). Pendiente:
  1. Afinar la paleta y el brillo de reposo (`DIM` en el puente) en sala.
  2. **Probar la capa manual (banco 2) con el pad delante.** El remapeo de
     2026-08-29 la movió de SHIFT (que no manda MIDI) a `PAD BANK`, y el
     puente ya pinta las notas 52-67; falta pulsar `PAD BANK` en sala y
     confirmar que los ocho botones de la página 2 disparan y encienden.
  3. Si se reinicia el puente hay que recargar el workspace: el puerto MIDI
     virtual se recrea con identidad nueva y QLC+ solo lo resuelve al cargar.
     Molesto si pasa en mitad de una noche; no hay arreglo desde nuestro lado.
- [~] **SHIFT reconfigura el pad, y lo descubrimos pulsándolo a ciegas
  (2026-08-29).** El pad dejó de disparar nada a media tarde: PAD1 pasó de
  ch10 nota 36 a ch10 nota 35, PAD13 de ch10 nota 48 a ch1 nota 47, knobs y
  botones intactos. Acusé al puente de LEDs de corromper la flash; **era
  falso** y la acusación está retirada. La causa está en el manual, que no
  teníamos delante ([manuals.plus](https://manuals.plus/sinco/smc-pad-midi-controller-manual)):

  | combinación | qué hace |
  | --- | --- |
  | SHIFT + PAD 1-8 | cambia de preset (1 = Performance, 2 = DAW, 3-8 usuario) |
  | SHIFT + PAD 9-12 | curva de velocidad (12 = velocidad máxima) |
  | SHIFT + PAD 13-14 | **transpose** arriba / abajo |
  | SHIFT + PAD 15-16 | octava arriba / abajo |
  | SHIFT + PAD15 + PAD16 | reset de octava |
  | SHIFT + NOTE REPEAT | los 16 pads pasan a editar el note repeat |

  O sea que las pruebas de SHIFT que pedí transportaron el teclado y lo sacaron
  de su preset. Nada de esto fue daño permanente. **Resuelto el 2026-08-29 con
  un reset de fábrica desde MidiSuite**, y midiendo las cuatro esquinas justo
  después: abajo-izq ch10 nota 36, abajo-der 39, arriba-izq 48, arriba-der 51,
  knob 1 CC 30 y pause CC 28 en canal 1. Es exactamente el mapa que genera
  `smc_pad_device.py`, así que **el mapa del show es el de fábrica y el pad no
  necesita configurarse**. Queda escrito en `docs/show-operation.md`: si los
  pads hacen lo que no toca, resetear el pad, no reconfigurarlo.
- [ ] **Conseguir el PDF real del manual del SMC-PAD.** Lo que hay en `Manual/`
  es una transcripción hecha desde
  <https://manuals.plus/sinco/smc-pad-midi-controller-manual>; ese sitio
  responde 403 a una descarga directa (`curl`), así que el PDF hay que sacarlo
  a mano desde el navegador, o de m-vave.com, o del QR de la parte de atrás del
  aparato. El resto de `Manual/` son PDF del fabricante y este debería serlo
  también: una transcripción se puede haber comido una tabla o un diagrama.
- [x] **El mapa del pad estaba escrito tres veces y las tres discrepaban
  (2026-08-29).** El perfil `QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi` declaraba
  las notas de fábrica 4-19 mientras el workspace estaba atado a 36-51, ocho
  bindings de la página 2 vivían en notas que ningún control manda (SHIFT es
  interno del aparato: elige SWING/LATCH/SYNC y no sale al cable), y ningún
  workspace declaraba `<Input>`, así que QLC+ abría el show sin nadie
  escuchando. Causa: el mapa vivía a mano en tres sitios. Ahora sale de
  `generate/smc_pad_device.py`; el perfil se genera (`qlctool input-profile`),
  el workspace se parchea solo (`input_binding.py`), la capa manual está en el
  banco 2 (`PAD BANK`, medido: PAD1 = nota 52) y la regla
  `binding a un control que el pad no manda` lo ve. Medido con
  `tools/smc-pad/midicap.swift`: PAD13 = 48, PAD1 = 36, PAD16 = 51; `<`/`>`
  **no** cambian de banco.
- [!] **SMC-PAD pad RGB: proprietary BLE GATT, mechanism reverse-engineered
  (2026-08-29).** Full writeup in `docs/smc-pad-led.md`. In short: plain MIDI
  (full note sweep + CC, all three ports, owner watching) lights nothing.
  Decompiling `MidiSuite.apk` with Blutter (Dart 3.9.2) shows colour is a
  **Bluetooth LE GATT** write, not MIDI: `BleManager.sendColorData` ->
  `writeData(list, cmd:5)` -> `makeWritePacket` frames `[0xB2, 0x44] + payload`
  and writes it over `flutter_blue_plus`. GATT service `0xAE40`, characteristics
  `0xAE41`/`0xAE42`. The Mac can be the BLE central directly (CoreBluetooth,
  `blescan.swift` in scratch confirmed BLE works and is authorized) - no phone
  or official app needed. Blocked on **one physical step**: put the pad in
  Bluetooth mode (BT button) so it advertises; on USB alone it does not. Then:
  connect, confirm the `B2 44 05 ...` colour packet byte-for-byte against the
  lit pad, and write the bridge daemon (subscribes to QLC+ note/CC feedback ->
  emits GATT colour writes; QLC+ cannot do GATT itself). Pad stays USB-MIDI in
  to QLC+ and BLE out from the daemon at once.
  Refs: github.com/worawit/blutter, github.com/cbix/mvave-chocolate-sysex.
- [ ] **The USB-DMX dongle randomly flashes the rig (2026-08-29).** Owner: "de
  vez en cuando pega un flash como si mandara 255 a todos los canales". Cause:
  the FT232R clone has no frame buffer — a USB hiccup corrupts the DMX frame
  on the wire and fixtures latch garbage as high values. Not fixable in any
  workspace; full writeup and the researched replacement in
  `docs/usb-dmx-interface.md`. For tonight's gig: dongle on a direct USB port
  (no hub), nothing heavy beside QLC+, 120 Ω terminator on the last fixture
  (still unconfirmed on this rig), real 110 Ω DMX cable on the long runs,
  and a 30-second check in QLC+ (Input/Output → gear on the output plugin):
  mode **Open TX**, output frequency **30** — the only valid mode for this
  clone and the plugin's own default; doc explains why the others cannot
  work. Not verifiable remotely today (show Mac unreachable from this
  network).
  Next steps: (1) order a MAX485 module (~2 €) and mount the owner's spare
  Raspberry Pi 3/4 as an OLA Art-Net node to prove the diagnosis; (2) build
  the permanent replacement — Pico + MAX485 + our firmware emulating the
  Enttec DMX USB Pro API (Pico-DMX + dmxusb, glue ~100 lines, QLC+ detects it
  as a Pro); fallback firmware rp2040-dmxsun (Art-Net over USB, no code).
  Shopping list and wiring table in the doc.
- [ ] **Run `qlctool check` before every show file leaves this repo.** It reads
  what the room will do rather than whether QLC+ can load the file, and it found
  four bugs on its first run. `cd tools/qlctool && .venv/bin/qlctool check
  "../../QLC+ Setups/Vibra-split.qxw"`. New rule when something misbehaves: find
  the cause, add a rule, add a dated regression test, run it over all three
  workspaces — written down in the repo's `CLAUDE.md`.
- [~] **Momento Locura ya no abre como pared blanca plana (2026-08-29 —
  pendiente solo de verlo en el rig).** "cuando ponemos el modo locura empieza
  todo blanco y normal" (dueño). Causa: `Intensidad Total` (255 fijo) junto a
  `Dimmer Chase` en la misma Collection — HTP, 255 gana siempre y el chase era
  cosmético; la misma trampa que Nivel Peak ya evitaba con `Intensidad Peak`.
  Fix en el generador: Locura lleva la base sin dimmers; `Intensidad Peak`
  abre ahora el shutter de *todos* los fixtures (el shutter no es el dimmer,
  no pisa al chase) y los paneles/grupos con dueño propio de intensidad salen
  del chase. Regla nueva `efx de dimmer tapado` + test fechado
  (`test_a_dimmer_effect_flattened_by_a_full_scene_beside_it`); destapó
  también a los paneles WX clavados a 255 bajo AUTO. Tres workspaces
  regenerados, `--validate` y check limpios, 298 pass.
- [~] **Recuperado lo que el show viejo hacía y el generado perdió (auditoría
  2026-08-28, implementado 2026-08-29 — pendiente solo de verlo en el rig).**
  Informe completo en `docs/old-vs-new-audit-2026-08-28.md`; regresiones en
  `tools/qlctool/tests/test_old_show_recovery.py` (10 tests fechados). Todo
  el generador, regenerados los tres workspaces, `--validate` y `qlctool
  check` limpios, suite 288 pass. Lo recuperado:
  los 7 colores de paleta que nada emitía (van en matrices curadas nuevas:
  Rojo Fuego, Verde Menta, Celeste, Azul Cielo, Azul Profundo, Morado,
  Fucsia); teclas `9`/`0` de cada banco vuelven a ser `Azul / Rojo` y
  `Rojo / Azul` (Naranja/Rosa quedan sin tecla); `Arcoiris Simultaneo` y
  `Arcoiris Pasos` (EFX relativos RGB, teclas `'` y `¡`); `Vel. Paneles
  Auto` (160-232-200-255, fade 45 s, botón en página 3); salida DMX USB
  `UID="None"` en los tres ficheros (y `UniverseChannels` 316 real);
  `Cabezas Centro` aparca los beams en pan 0 / tilt 130; `Prisma Animacion`
  vuelve a la coreografía de 8 pasos (4; 2y4; 1; 2; todos; 3; 1y3; fuera —
  hold 8 s, el viejo iba a 63 s/paso: afinar en sala); ciclos de matrices en
  Random con los algoritmos viejos (Alternate con duales, Opposite, Fill
  From Center, Fill Unfill, One By One, Random Column, Stripes From Center);
  `Rig 4 Colores 1-4` como pasos de la rueda; Dimmer Chase por familia de
  fixture (Line Serial W0 H127 en Collection, ambos sentidos); variantes
  `Simultaneo` (7 wash + 3 beam) y crossfade 5 s en los chasers de
  movimiento. En sala: pacing del prisma, holds de los arcoiris, y que el
  banco de 12 botones se lea bien en 13".
- [ ] **Montaje 2026-08-29: las 4 máquinas de humo vertical LED.** Patcheadas
  como `Generic / LED Spray Fog` (7ch) en **317, 324, 331 y 338**; el placeholder
  `Generic Smoke` 2ch de 299 fuera. El Mac del show quedó preparado por SSH
  (2026-08-29): repo sincronizado a `e8595eb` con el git de brew, todos los
  `.qxf` instalados en `~/Library/Application Support/QLC+/Fixtures/` y en
  `QLC+ 5/Fixtures/`, QLC+ reiniciado, `Vibra-split.qxw` cargado allí con
  **cero errores** en el log de arranque (definición nueva reconocida), y
  dejado abierto listo para mañana. Queda solo lo físico, en orden:
  1. Menú de cada máquina: `A001` = 317 / 324 / 331 / 338 (una cada una, el
     orden físico da igual mientras se apunte cuál es cuál).
  2. `HUMO VERT · U` mantenido: columna blanca + humo en las 4; al soltar, sus
     LED vuelven al color de la sala (rueda). `HUMO YA · H` solo debe mover la
     AF-150 (ambiente).
  3. Con `AUTO` en marcha: las 4 deben ir del color de la sala como PARs de
     suelo, apagarse con `Todo Negro`, y subir/bajar con los niveles.
  4. Confirmar en la máquina real que CH6 (strobe) y CH7 (ciclo color) a 0 son
     "apagado" — el manual no lo jura; si 0 arranca el ciclo, corregir el
     `.qxf` y regenerar.
  5. Posiciones del plot (fila frontal z=6400, provisional) contra dónde se
     monten de verdad; ajustar el JSON y regenerar si interesa el 3D.
  6. Si la bomba no dispara con `U`: comprobar `O` (protección sin líquido) en
     el menú y que el tanque cebó el tubo.
  7. **La máquina de ambiente puede ser la Mark MF 1500 DMX MKII** en vez de
     la AF-150 (owner, 2026-08-29; manual en
     `Manual/MF_1500_DMX_MKII_v1_2.pdf`). Mismo footprint DMX — 1 canal, solo
     humo — así que el patch (`Generic Smoke / Amount` en la **186**) vale para
     cualquiera de las dos sin regenerar. Solo cambia la dirección física:
     la Mark va por dip-switches, dip 10 SIEMPRE ON y los dips 1-9 codifican
     `dirección - 1` en binario (dip 1 = 1 ... dip 9 = 256). Para la 186:
     **ON = 1, 4, 5, 6, 8 y 10; OFF = 2, 3, 7, 9** (185 = 1+8+16+32+128).
     Contrastar con los diagramas de la página 4 del manual al ponerlos.
- [ ] **Apple git sigue sin CommandLineTools en el Mac del show** (2026-08-29):
  `/usr/bin/git` muere con `xcrun: error: invalid active developer path`. NO
  bloquea nada — el git de Homebrew funciona (`export
  PATH=/usr/local/bin:$PATH` en sesiones no interactivas, trampa ya documentada
  en brain/access-map), y así se sincronizó hoy. Arreglo de fondo opcional:
  `xcode-select --install` con sesión gráfica delante.
- [ ] **Probar con el rig el contenido nuevo del 2026-08-28.** Cinco piezas,
  todas con valores DMX de primera pasada que se afinan mirando la sala:
  `Ola Vertical` (onda de tilt, Line a Width 0 + Serial), `Barrido Unison`
  (empuje en fase, el espejo hace que los lados se encuentren), `Beams Cruce`
  (la X estática, espejo del abanico — mismo TILT, ajustar en sala),
  `Rig Multicolor 1/2` en la rueda (beams en rainbow scroll ~186, plasma en
  las barras), `Ciclo Paneles Mixto` (8 min efectos / 4 min manual siguiendo
  la rueda), `Nivel Fiesta Dinamico` (chase 30 s / ping-pong 8 s),
  `Gobo Shake` (jitter a 64) y el prisma girando a 25. Los holds y
  velocidades son opiniones hasta que alguien los vea.
- [ ] **Probar en casa los flashes recuperados (2026-08-27).** El dueño, con la
  FT232R en casa: "esto no hace estrobo y antes lo hacia cuando le daba al
  espacio". Era real: el show viejo estrobaba en `Flash 100%`/`Flash 50%`
  (CromoWash 240, Vortex 250, paneles 255; el 50% era mitad de *velocidad*, no
  de brillo) y el generado dejaba los shutters en "Open". Restaurado: los tres
  flashes estroban (`Space`/`-`/`.` — el `.` es el `Flash Colores` viejo,
  estrobo sobre el color que corra), `Strobo ON` cubre ya los canales sin
  rangos (Vortex, paneles), y los graves del audio pasan a `Golpe Graves`, un
  blanco SIN estrobo (regla nueva `estrobo en manos del audio`). Reglas
  `flash sin estrobo` + `estrobo incompleto`, tests fechados, los tres
  workspaces regenerados y validados. Falta probar con los aparatos delante:
  Espacio, `-` y `.` (estroban como el show viejo), `B` (barrido inverso),
  `M` (rotación de barridos), `Escenario`/`Centro` en el marco de figuras,
  los subsets de prisma `1/2/3/4/1y3/2y4`, los `MultiColor BEAM` de la
  página 3, el fader `Vel. Paneles`, y `HUMO VERTICAL · N` (página 2,
  paneles a los ciclos del humo vertical, calcado del show viejo).
  2026-08-29: el dueño, viendo las PAR: "el flash es entre 246-248, como lo
  tenemos ahora es muy lento" — el 0.85 daba 217 en las CLB2.4. Subido a 0.97
  (CLB 247, CromoWash 248), regla nueva `flash lento` (el flash mas rapido de
  la consola tiene que vivir arriba de la carrera slow-to-fast), test fechado,
  los tres workspaces regenerados y validados. Misma noche, el lento: "el
  flash slow para los par es unos 200" — 0.45 daba 115; subido a 0.785 (CLB
  200, CromoWash 202) y la regla gana suelo: ningun flash pulsado a mano
  escribe estrobo por debajo del 70% de la carrera. Queda verificar en sala.
  Tambien del 2026-08-29: (1) **tap tempo recuperado** — `M` tapea el dial
  `Tempo Show` de la pagina 1 y arrastra rueda de color, gobos, color beam,
  prisma y dimmer. Cada capa lleva su propio **multiplicador** (cuantos taps
  dura): el mismo multiplicador para todas es lo que volvia "locos los
  programas" — regla `tap que aplana los programas`. Tres trampas verificadas
  en el QLC+ 5.2.2 del Mac del show, leyendo su propio log: **`ControlBPM` no
  existe en 5.2.2** ("Unknown speed dial tag"), asi que un tap que gobierne el
  BPM global no es posible en esta version — el tap tiene que escribir en
  funciones (`tap que no re-tempa nada`); **un chaser en Beats le pasa su
  fundido crudo a los pasos** y un EFX se lo resta a su duracion en ms
  (`EFX::loopDuration`), que es por que las cabezas iban a 6 s en vez de 16 y
  no cerraban la figura (`unidades de tempo cruzadas`); y **una Collection no
  admite `<Tempo>`** ("Unknown collection tag: Tempo") — `Dimmer Chase` se
  quedaba en el reloj sin avisar (`tempo en una coleccion`). El show por
  defecto vuelve al reloj entero; `--beats` (variante Audio) solo pone en
  Beats los chasers cuyos pasos son escenas mas los ciclos de matrices. El
  movimiento no va al dial a proposito: 15 s por figura no caben en los
  multiplicadores (topan en 16 taps). `Dimmer Secuencia` pasa de `M` a `K`.
  Ojo: el `<Key>` suelto que escribia el builder no lo carga qmlui — el tap
  va como `<Input ID="1" Key="M"/>`.
  El movimiento tiene ya su propio dial (`Vel. Movimiento`, pagina 2) con la
  MISMA tecla `M` — una tecla llega a todos los widgets que la tengan
  (VCPage::handleKeyEvent), como en la consola vieja. Re-tempa la rotacion, sus
  EFX y el crossfade a la vez, porque QLC+ le resta el fundido del chaser a la
  duracion del EFX. `Movimientos Suaves` queda fuera aposta (60 s por figura).
- [ ] **Cuando salga la version nueva de QLC+, pasar el show a `--bpm-tap`.**
  Ya esta implementado y probado (`qlctool newshow --bpm-tap`, test fechado):
  todas las capas que siguen la musica en tempo **Beats** sobre generador
  Internal, y el tap de la pagina 1 gobernando el **BPM global** (ControlBPM)
  en vez de escribir duraciones — asi ninguna capa necesita multiplicador,
  cada una dice sus beats y un solo reloj las mueve. No se usa todavia porque
  el **5.2.2 del Mac del show no tiene ControlBPM** («Unknown speed dial tag»
  en su propio log) y cargaria el fichero sin hacer nada. Al actualizar:
  comprobar en el log que ya no sale ese aviso, regenerar los tres workspaces
  con `--bpm-tap` y verificar en sala. El movimiento se queda en el reloj
  incluso entonces: un chaser en Beats le corrompe el EFX en cualquier version.
  (2) **Strobo/Strobo Suave mataban el show**: sus chasers pisaban
  `Blanco Total`/`Todo Negro`, botones del solo frame de estados — un boton
  Toggle "oye" arrancar su funcion la arranque quien la arranque
  (VCButton::slotFunctionRunning) y el solo frame paraba AUTO. Ahora pisan
  gemelas propias (`Strobo Blanco`/`Strobo Negro`); regla nueva `estado
  pulsado por otra funcion` + test. (3) **COLOR BEAM (`C`) no esta roto**:
  anima la rueda de color de los 4 BEAM 230W, no toca las PAR — probado en
  casa solo con PARs delante era invisible por diseño. Verificar con los
  beams montados.
- [ ] **Comprobar en sala los 4 grupos nuevos (2026-08-26).** Los 4 paneles
  WX-60WPS salieron de `BarrasLed` a un grupo propio `PixelesLed` (4x1), porque
  compartir la rejilla 8x3 con las dos barras los dejaba a oscuras media
  animacion — ocupaban solo las columnas 4-7 de la fila de abajo. De paso, todas
  las rejillas ahora encajan exactamente: `BarrasLed` 8x2, `Cabezas` 12x1 (antes
  declaraba 8x1 sobre 12 heads, 4 inalcanzables), `PAR` 15x1. La consola pasa de
  288 a 361 botones (un banco de color y 30 mezclas mas para el grupo nuevo;
  matrices no — el generador excluye a proposito los grupos self-animating,
  `canonical_show.py:197-217`, verificado 2026-08-27). Verificar que el barrido cruza los 4 paneles y que la pagina 2
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
  patch <file> --group-add` is the edit; the `PAR` group's grid needs a free
  cell (`--group-size` first). **Only `Vibra.qxw` still has this** (checked
  2026-08-31): the split patches each CLB2.4 four times, one fixture per head,
  and all eight are in `PAR`. So it dies with `Vibra.qxw` if the split wins.
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
  level). `Dimmer Chase` owning Peak's intensity is done - see TODO_LOG.md,
  2026-08-27.
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
  middle of the stage grid. **Added 2026-08-27**: the two new Serial-figure
  movements, `Ola Suave` and `Cascada Beams` (Task 6), are a deliberate
  exception — Serial propagation gives mirrored pairs different
  `serialNumber`s, so the pairs cascade rather than move in wall-clock
  lockstep; judge on site whether the traveling wave reads well. Also eyeball
  the `Cascada Beams` caption (13 characters on a 63px button) — unverifiable
  from the XML alone.
- [ ] **New generated content needs an eyeball pass (2026-08-27).** The 10
  curated matrix scripts (Task 5/6) and the 4 new movement figures (`Beam
  Diamante`, `Beam Hoja`, `Ola Suave`, `Cascada Beams`, Task 6) have never
  been seen running — check them in the 3D preview and, when possible, on the
  rig. In particular the plasma/noise script durations are chosen windows,
  guessed rather than measured against real music.
- [ ] Decide on `QLC+ Setups/Vibra-split.qxw` (2026-08-25): the same rig with
  each CLB2.4 patched four times, one fixture per PAR head, so all eight can be
  aimed and coloured separately in the 3D view - which QLC+ cannot do for the
  four heads of one fixture (`Fixture3DItem.qml` keeps a single `lightColor`).
  Open it beside `Vibra.qxw` and say whether it replaces it. If it does, the
  plot to keep is `vibra-stage-plot-split.json` and the heads want fanning
  apart rather than all at `-35`.
- [ ] Set the audio-trigger thresholds on site. **Updated 2026-08-27**: the
  bass band ("Graves") is now bound to `Flash 100%`, one of the GOLPES hits
  (a Scene, Flash mode, Override, outside any solo frame) — not the
  `Blanco Total` room-state scene, which shares AUTO's solo frame and would
  have stopped AUTO with nothing to restart it. The bound band's threshold is
  still QLC+'s default and needs tuning over real music; QLC+ also needs an
  audio input picked under Configuration before the widget does anything.
- [ ] Confirm the strobe values on the fixtures whose shutter channel has **no
  labelled range** - the PC-64, the CLB2.4, the Mini Led Moving Head and the
  WX-60WPS. `qlctool` deliberately leaves them out of `Strobo ON`, because a
  guessed value closes a shutter instead of flashing it. The channel probe
  settles it in the same on-site session as the rest of the rig.
- [ ] Merge branch `qlctool` into `main` once the fresh show is accepted. It
  carries the whole toolkit plus three format variants of DeluxeEventos2 used as
  test material.

## QLC+ feature audit (2026-08-27)

Findings from a full scan of the QLC+ source clone (`~/p/qlcplus`, master =
5.3.0-git of 2026-08-22 — **newer than the installed 5.2.2**, so every QLC+5
feature below gets verified against the real binary before we build on it),
the official docs (docs.qlcplus.org v5 + release notes), and the generated
`Vibra-split.qxw`. The show uses 5 of 10 function types, 4 of 39 RGB scripts,
0 sliders, 0 MIDI/OSC inputs. A Codex cross-check of these findings ran the
same day; anything it refutes gets corrected here.

### Possible defects found by the audit

- [x] ~~`PixelesLed` (group 3) missing matrices~~ — **not a bug**: the
  generator deliberately skips matrix RGB for self-animating groups
  (`generate/canonical_show.py:197-217`, `_all_self_animating()` at 598-604);
  the panels run their 42 internal effects instead, and a matrix's RGB would
  be ignored in Auto mode anyway (see the internal-program rule). The stale
  "30 matrices más" claim in the 2026-08-26 item above is corrected there.

### Unused QLC+ capability worth adopting (priority order)

- [ ] **Zero sliders on the console.** Three concrete uses: (a) Submaster
  slider scaling Peak's frame — `Dimmer Chase` being HTP-shadowed by
  `Intensidad Total` there is fixed a different way now (TODO_LOG.md,
  2026-08-27: the chase owns Peak's dimmers outright), so this would be a
  live-adjust nicety, not a correctness fix; (b) Adjust-mode sliders driving
  live function attributes — EFX Width/Height/
  Rotation and RGBMatrix Color 1-5 / Pattern / script properties are all
  registered live attributes (`rgbmatrix.cpp` registerScriptPropertyAttributes).
  The GrandMaster slider (c) shipped separately — Task 3, TODO_LOG.md
  2026-08-27.
- [ ] **MIDI controller for the operator.** 0 `<Input>` bindings; only 64 of
  374 buttons have a key. QLC+5 has input autodetect, profiles with LED
  feedback (APC colour tables in the MIDI docs), soft-takeover. An APC mini or
  similar = operating in the dark without hunting keyboard keys. Blocked on:
  owner picks/buys a controller.
- [ ] **Beat-locked matrices**: RGBMatrix in Beats tempo defers a step change
  when within 1/16 beat to stay locked (`rgbmatrix.cpp` beat resync), and 5.2
  enabled audio BPM detection (BeatTracker, 50-240 BPM with confidence). Folds
  into the existing `Vibra-beats.qxw` trial above: beats on musical layers
  only, energy clock stays on time — `beat_tempo.py` already draws that line.
- [ ] **Position palettes with fanning** (QLC+5): Linear/Sine/Square/Saw fan
  over X/Y/Z — the calibrated way to build `Beams Abanico` instead of guessed
  pan values. **Updated 2026-08-27**: Task 1 confirmed `<Palette>` load on the
  installed 5.2.2 binary (not just master's `doc.cpp:1270-1288`) — that gate
  is closed. Remaining gate: VC buttons cannot fire a palette directly
  (palette → Scene → button still needed), and the fan itself needs
  calibrated aiming on the rig.
- [ ] **XY Pad presets and floor control**: the pad ships bare; QLC+5 supports
  Position/EFX/Scene/FixtureGroup presets and aiming at a 3D floor point
  (`vcxypad.cpp`) — useful for the fan aiming and the crowd-sweep bounds in
  the deferred highlight item.
- [ ] **RGBMatrix ControlMode Dimmer/Shutter + BlendMode**: a matrix can paint
  dimmers instead of RGB — any of the 39 scripts becomes an intensity chase
  over the grid, an alternative to the shadowed `Dimmer Chase` EFX. BlendMode
  Mask is already noted in the barras item above; Additive also exists.
- [ ] **VC Clock in Schedule mode**: start AUTO at opening time, per weekday.
  One widget, zero risk.

Looked at and deliberately skipped: Show Manager timeline (show is
DJ-reactive, not timecoded), Cue List + crossfader (theatrical), Audio/Video/
Sequence functions (no use case), OS2L (only if the DJ runs Virtual DJ),
Simple Desk (no cue stacks in v5; keypad covered by `qlctool probe`), channel
modifiers, passthrough, extra universes.

## Calidad del codigo (baseline adoptado 2026-09-01)

`tools/qlctool` corre el gate compartido (`uv run baseline-py gate`), hoy en
verde. Lo que queda es deuda anotada con fecha, y cada lista solo puede
encoger:

- [ ] Reducir el ratchet de ruff en `tools/qlctool/ruff.toml`: 142 simbolos
      publicos sin docstring, 104 generadores con mas parametros de la cuenta
      y 26 valores magicos (numeros de canal DMX y constantes de QLC+).
- [ ] Decidir uno por uno los 24 `zip()` sin `strict=` (B905). No es cosmetico
      aqui: dos listas que dejan de cuadrar en silencio son exactamente el
      fallo que las reglas de `qlctool check` existen para cazar, asi que cada
      sitio necesita saber si un desajuste de longitud es un bug o un recorte
      esperado.
- [ ] Vaciar el ratchet de mypy en `tools/qlctool/mypy.ini`: 73 modulos con
      `ignore_errors`, 266 errores casi todos por anotaciones que faltan.
      `lxml-stubs` ya se instalo y quito 67 de golpe.
- [ ] Bajar los 170 hallazgos estructurales de
      `tools/qlctool/.baseline-py-baseline.json`: 100 modulos con mas de una
      unidad, 62 nombres de fichero que no dicen lo que declaran y 8 ficheros
      por encima del limite de lineas (`live_console.py` con 1160,
      `canonical_show.py` con 813, `cli.py` con 695). Tras cada arreglo,
      `uv run baseline-py baseline update` reescribe el registro.
- [ ] `tools/smc-pad/reference` tiene tres scripts de Python fuera de todo
      esto: no hay `pyproject.toml` ahi y no entran en ningun gate. Decidir si
      se integran en `qlctool` o se quedan como referencia suelta.
