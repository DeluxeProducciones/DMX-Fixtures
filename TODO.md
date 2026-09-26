# TODO — Vibra Eventos (DMX / lighting)

> The backlog for this repo: the rig, the fixture definitions, the QLC+
> workspaces and the show's tests. The toolkit, `qlctool`, is
> https://github.com/spectalive/qlctool since 2026-09-25; its debt is in
> that repository's `TODO.md`. Last reviewed: 2026-09-26. History coverage:
> Complete.
>
> States: `[ ]` pending · `[~]` partial or unverified · `[!]` blocked · `[x]`
> verified complete · `[-]` obsolete or superseded. Closed work moves to
> [TODO_LOG.md](TODO_LOG.md) in this repo.

Este backlog salio de `~/p/TODO.md` el 2026-08-26, para vivir al lado de la
cosa de la que habla; su log llego detras el 2026-09-22, con la historia DMX
entera que estaba en `~/p/TODO_LOG.md`.

**Ultima revision, 2026-09-22.** Se comprobo item por item contra el arbol (no
contra lo que decia el propio item): cinco se cerraron y estan en el log, y a
ocho se les corrigieron numeros o afirmaciones que ya no eran verdad. Quedan 61
`[ ]` y 7 `[~]`, y ningun cerrado en este fichero.

**Before finishing anything here**, see `CLAUDE.md`: find the cause, add a rule
to `qlctool check`, add a dated regression test, run it over all three
workspaces.

**Disposicion, 2026-08-31, recontada el 2026-09-22.** Se cerro todo lo que se
podia cerrar sin el rig (nueve items, en `TODO_LOG.md`), incluida la
rejilla: los grupos van ya en orden de escenario y las dos MAC WASH tienen
grupo propio. Hoy quedan 61 `[ ]` y 7 `[~]`, y casi ninguno espera a que
alguien escriba codigo — las excepciones son la seccion de calidad del codigo,
al final, que si es trabajo de teclado:

- **La mayoria espera al rig o al dueño** - humo, el RunMode de las lyres, la
  rejilla nueva, el tilt de las cabezas, el foco de los beams, los flashes, los
  niveles de energia, los thresholds de audio, el probe de los cuatro fixtures
  sin documentar y el pad en sala. Un valor DMX adivinado
  desde aqui es exactamente el fallo que este repo persigue.
- **Tres esperan a algo externo**: renombrar la org de GitHub, `xcode-select`
  en el Mac del show (fuera de red), y comprar el reemplazo del dongle DMX.
- **Una espera una decision del dueño**: quedarse con `Vibra-split.qxw`.
- **La auditoria de capacidades de QLC+** (sliders, MIDI, paletas, XY pad,
  ControlMode, VC Clock) no son defectos: son cosas que el show podria adoptar,
  y cada una cambia como se opera. Se deciden, no se implementan de oficio.

## Reorganizacion: show vivo, licencias, orgs, nombre y cliente tactil (2026-09-24)

Una sesion que empezo por "en AUTO salen colores que no pegan" y acabo
replanteando como se reparte todo esto. Lo decidido por el dueño esta marcado
como tal; lo demas es propuesta pendiente de su si. El trabajo de brand-finder
vive en `~/p/brand-finder/TODO.md`.

### A. El show vivo (primero: el mini y la tablet siguen con el show viejo)

- [~] **La tablet con el show de `main` (firmware v90).** Flasheada el
  2026-09-26 con dmxdesk v0.1.1 (mapa 4da61399..., show 12a75704...): arranca
  en el escritorio, cuatro reinicios y glcube al quinto, y vuelve al escritorio
  tras reiniciar (ver `TODO_LOG.md` de `~/p/taq102`). Falta: abrir QLC+ Vibra
  en el mini y que el dueño toque AUTO en la tablet y diga que ve.
- [ ] **El Mac del show (`vibra-oficina`) tiene el show del 2026-08-29.** No
  respondia por Bonjour el 2026-09-24. Siguiente: cuando este en red,
  sincronizar como en `docs/show-operation.md` y comprobar el hash.
- [ ] **Historial reescrito el 2026-09-25: los demas clones no pueden hacer
  `git pull`.** Se quito la linea de sesion de 179 mensajes y las menciones a
  herramientas de IA de otros 11 (regla del dueño); los arboles no cambian,
  todos los SHA desde el 2026-08-25 si. Mini (`~/p/DMX-Fixtures` y el
  worktree `qlctool`) y MacBook (`ssh macbook`, estaba limpio en `f8385ff`,
  qlctool reinstalado) ya reseteados. Falta el Mac del show, fuera de red el
  2026-09-25 (ni Bonjour ni `192.168.1.56`). Siguiente, cuando este en red:
  `git status` (guardar lo local), luego `git fetch origin && git reset
  --hard origin/main` y `qlctool install --check`. Copia previa y mapa viejo->nuevo en
  `~/Backups/vibra-lighting-pre-trailer-rewrite-2026-09-25.bundle` y
  `~/Backups/vibra-lighting-commit-map-2026-09-25.txt` (mini).
  **Segunda reescritura, 2026-09-26** (decision del dueño): la foto
  `docs/smc-pad-panel.jpg` llevaba GPS en el EXIF; se sustituyo en todo el
  historial por la misma foto sin metadatos (solo orientacion y perfil de
  color), 189 SHA cambian desde `fd397da` (2026-08-29), el arbol final es
  identico. Mini (`main` y worktree `qlctool`, en `3e9370f`) y MacBook ya
  reseteados; el Mac del show sigue igual que arriba. Copia y mapa:
  `~/Backups/vibra-lighting-pre-gps-rewrite-2026-09-26.bundle` y
  `~/Backups/vibra-lighting-commit-map-2026-09-26-gps.txt` (mini). GitHub
  puede seguir sirviendo los commits viejos por SHA hasta que su cache los
  purgue; para borrarlos del todo hay que pedirselo a GitHub Support.
  **Tercera reescritura, 2026-09-26** ("Si, purgar ya"): el blob de
  `Colors.psd` (64,7 MB, `6029d23c`, bajo `Colors/` y `Colores/` desde
  2024-08-31) quitado de todo el historial con `--strip-blobs-with-ids`; 320
  SHA cambian, arbol final identico; `main` en `6f9f555`. Mini, worktree y
  MacBook ya reseteados. Copia y mapa:
  `~/Backups/vibra-lighting-pre-psd-purge-2026-09-26.bundle` y
  `~/Backups/vibra-lighting-commit-map-2026-09-26-psd.txt`. El Mac del show
  sigue necesitando un solo `fetch` + `reset --hard origin/main` para las tres.

### B. Licencias y lo que se publica

El dueño quiere todo abierto, show incluido: "prefiero que alguien las use".


### C. Orgs y nombre

- [ ] **Asegurar el nombre Spectalive** (elegido por el dueño 2026-09-24;
  busqueda cerrada en `TODO_LOG.md`). Libres: `spectalive.com`, `.io`, `.app`,
  `.dev`, `spectalivecontrol.com`, GitHub `spectalive`, npm, Bluesky, App
  Store. Ocupados: YouTube `@spectalive`, y X, Instagram y Facebook
  `spectalive` (una marca de gafas "Specta"). TMview (busqueda aproximada) sin
  marca SPECTALIVE ni SPECTRALIVE; las mas cercanas son Spectalite (DPMA
  3020182100434, clases 1/17/42; India, clases 17/22/24/42) y SPECTRALITE (lentes
  Zeiss/Sola, clase 9). Hecho 2026-09-24: `spectalive.com`
  registrado en Cloudflare Registrar, cuenta BusiRocket, via el MCP de
  Cloudflare ($10.46/año, auto-renew activo, privacidad, zona activa con NS
  abby/gabe, expira 2027-09-24). Creadas por el dueño el mismo dia: org
  GitHub `spectalive` (https://github.com/spectalive, `CristianDeluxe`
  admin) y org npm `@spectalive`. Bluesky `@spectalive.com` creado 2026-09-25 (DID
  `did:plc:kgphqczajrhzs7mpetwuf76v`, TXT `_atproto` en Cloudflare, acceso en el
  access-map del brain). Decidido 2026-09-26 (dueño: "prefiero spectralive.com como nombre en
  redes"; `spectralive.com` con r es de otro desde 2015, NameBright, asi que se
  lee como el dominio propio): en redes el nombre es `spectalive.com` donde se
  admite el punto (Instagram, TikTok, YouTube) y `spectalive_com` en X, que no
  lo admite. Siguiente: que el dueño cree esas cuentas (piden su login y su
  telefono). Pendiente de decidir: la marca UE en clases 9 y 42.
- [ ] **Re-apuntar el clon del Mac del show** (`~oficina/DMX-Fixtures`) a
  `git@github.com:Vibra-Lab/vibra-lighting.git` cuando este en red; hoy
  funciona por la redireccion de GitHub, que se rompe si alguien crea otro
  `DeluxeProducciones/DMX-Fixtures`.
- [ ] **Pedir el nombre `vibra` a GitHub** (decidido 2026-09-24): hoy es una
  cuenta personal de 2015 sin repos. Siguiente: redactar la solicitud para que
  la envie el dueño por support.github.com.
- [!] **`BusiRocket/tieneslavibra` no se puede transferir a `Vibra-Lab`.**
  Es un fork privado de `dovaldev/tieneslavibra` (usuario), y GitHub responde
  `422 Repository can't be transferred`, tambien con los forks privados
  permitidos en `Vibra-Lab` (se probo y se volvio a dejar en `false`). Los
  otros cinco ya se movieron (ver `TODO_LOG.md`). Siguiente: pedir a GitHub
  Support que lo desvincule de la red de forks ("detach fork") y transferirlo
  despues; sus 4 secretos de despliegue y su deploy key viajan con el repo, y
  el clon local `~/p/tieneslavibra` pasa a `Vibra-Lab` con un `remote set-url`.

### D. Partir este repo (cada parte con su propio diseño)

Reparto propuesto, cada parte a la org `spectalive` (salvo el show, que se
queda en `Vibra-Lab/vibra-lighting`).

- [ ] **Objetivo del dueño (2026-09-24): "la idea es que cualquiera pueda usar
  la herramienta para generar sus shows".** El generador (`generate/`) pasa
  al toolkit y se alimenta de una descripcion del rig (fixtures, grupos,
  paginas, controlador, estilo), guiado por capacidades; Vibra queda como un
  ejemplo (su descripcion + lo unico suyo) en `vibra-lighting`. Paso 1,
  aprobado: desenredar dentro de este repo (checks de escritorio/pad como
  plugins por entry points, rutas de la libreria sin suponer este repo - hecho
  2026-09-25, Plan B Task 3, ver `TODO_LOG.md`), con
  los tres workspaces identicos. Hecho 2026-09-25 (spec steps 7 y 8, Plan C,
  ver `TODO_LOG.md`): un segundo rig de ejemplo, `git filter-repo` a
  https://github.com/spectalive/qlctool, tag `v0.1.0`, y este repo depende del
  tag (`requirements.txt`).
- [~] **Fixtures**: `QLC+ Fixtures/` e `InputProfiles/` se quedan aqui; las
  verificadas estan en PRs abiertos el 2026-09-26 (qlcplus #2166-#2167, OFL
  #6164-#6165, ver `TODO_LOG.md`); el perfil del SMC-PAD (#2168) lo fusiono
  el mantenedor el mismo dia. Siguiente: atender las revisiones; si el
  mantenedor de QLC+ pide ficheros guardados con QLC+, abrir y guardar la MiN
  Wash en su editor. Las retenidas se mandan cuando
  se confirmen en sala.
- **Pad**: movido el 2026-09-26, con historia, a
  https://github.com/spectalive/smc-pad (`v0.1.0`). El puente ya no lleva los colores de
  Vibra: lee `QLC+ Setups/Vibra.pads.json`, que escribe `qlctool pad-palette`
  y fija `tests/test_pad_palette.py`. Lo que queda del puente (instalarlo y
  verificarlo con el pad delante) esta en su `TODO.md`.
- **Host**: movido el 2026-09-26, con historia, a
  https://github.com/spectalive/qlc-launcher (`v0.1.0`), con el show y QLC+ en
  una config; lo que queda (mDNS/QR, elegir show al lanzar) esta en su
  `TODO.md`.
- [ ] **El show** se queda aqui: workspaces, la receta que genera este show
  (los generadores propios de Vibra) sobre el toolkit como dependencia, rig y
  operacion.

### E. Cliente tactil multiplataforma y multi-backend

Plan del dueño: la UI de la tablet es la buena, asi que pasa a la consola
virtual de QLC+, y la tablet muestra lo que QLC+ muestre, con todos los
widgets, para portarla despues a otros dispositivos. Decidido: QLC+ parcheado
desde el principio; nucleo en C portable reutilizando `dmxdesk`.

- [~] **Separar `dmxdesk` en `core/` y `platform/linux-fb/`.** Ya vive en
  spectalive/dmxdesk con su historia (v0.1.0, 2026-09-26; `taq102` lo
  empaqueta fijado a esa version, ver `TODO_LOG.md`), pero sigue plano en
  `src/`. Falta partirlo: `core/` (sesion, `/vc.json`, layout, pintado,
  fuentes, busqueda del master) y `platform/linux-fb/` (DRM, tactil, power,
  Wi-Fi, brillo). Siguiente: hacerlo en dmxdesk cuando empiece el
  multi-backend.
- [ ] **Multi-backend**: modelo de superficie propio y un adaptador por
  programa; QLC+ primero, luego libres y de pago (Onyx, MagicQ, Lightkey,
  Daslight...) por API, OSC o MIDI.
- [ ] **Fork de QLC+ con `/vc.json` ampliado**: atajos de teclado,
  `stopAllFadeOutTime`, `functionsList` y multiplicadores del Speed Dial, mas
  de un color por widget; y PR a upstream. Hallazgos: se construye en
  `WebAccessQml::getVCJson` (`webaccess/src/webaccess-qml.cpp:1356`); `type`
  llega traducido ("Botón"), hay que usar `typeId` (1 Button ... 11 Clock);
  el websocket maneja los 11 tipos salvo Label.
- [ ] **Invertir la UI**: la receta del show genera la consola virtual con la
  forma de la tablet, y el cliente pinta `/vc.json` de forma generica.
  Entonces desaparecen `qlctool deskmap`, `Vibra.desk.json` y el mapa dentro
  del firmware, y un show nuevo ya no pide reflashear.
- [ ] **Otras plataformas despues**: SDL (Raspberry, portatil Linux), iOS,
  Android, ESP32.
- [ ] **Ideas de UX de otras apps** (investigadas 2026-09-24): zonas fijas de
  movimiento / color / flash con velocidad y tap siempre a mano (Light Rider);
  estado real en cada control, no el ultimo toque (Luminair, iHog); emparejar
  por QR o mDNS (G3Link). La web de QLC+ no pinta el Speed Dial: soportar
  todos los widgets ya diferencia.

## Development environment

- [ ] **Reinstall on the show Mac (AGENTS.md, 2026-09-25).** The toolkit left
  this repository for https://github.com/spectalive/qlctool (`v0.1.3`);
  every checkout installs it from `requirements.txt` into a repo-root
  `.venv`. Done on the Mac mini and on the MacBook (both on `v0.1.3`, 30
  passed, `install --check` 0). Next: the steps in AGENTS.md "Reinstalling
  after the extraction" on the show Mac (`vibra-oficina`, off the network on
  2026-09-25: no Bonjour, `192.168.1.56` silent). The Mac mini's launcher
  (spectalive/qlc-launcher in `~/p/qlc-launcher` since 2026-09-26) opens the
  workspace in the worktree `~/p/DMX-Fixtures-qlctool` (branch `qlctool`),
  which does not use the toolkit; its remote branch was deleted on 2026-09-25
  (merged, `80261d0`), the local branch stays until the launcher is pointed
  at another checkout (`install.py --workspace`).
- [ ] **`QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi` still names the toolkit's old
  in-repo path in its generated header comment (2026-09-25).** It is
  byte-tested against `qlctool input-profile` of the pinned release, so it is
  left as generated. Smallest next step: when a toolkit release changes the
  header, bump the tag here and regenerate the profile.

## Visor 3D: BlenderDMX en el Mac mini (2026-09-23)

Decision del dueño, 2026-09-23: el 3D de QLC+ 5 no vale como visor del show
(sin pluma de humo, gobos planos, una barra de cuatro cabezas es una sola luz,
los paneles en modo Auto no se pintan; todo medido en `docs/rig.md`). Se
adopta **BlenderDMX** (gratis, GDTF/MVR, Art-Net y sACN, haces volumetricos,
gobos con rotacion, fixtures multipixel) y, si aparecen cosas que mejorar, se
contribuye al proyecto. Capture 2026 (Solo, 395 EUR) queda como plan B si
Blender va lento en el mini.

Instalado el 2026-09-23 en el Mac mini (`ssh macmini`, M1 16 GB, Blender
5.2.2 LTS de brew): checkouts en `~/p/blender-dmx`, `~/p/python-gdtf` y
`~/p/python-mvr` (upstream `open-stage`, main en `569040f`), extension
construida con `Blender --command extension build` e instalada en el
repositorio `user_default`, y la carpeta instalada sustituida por un symlink
al checkout, como pide `DEVELOPMENT.md`. Verificado en headless: habilitada
tras reinicio, `scene.dmx` registra `artnet_enabled`, `sacn_enabled`,
`universes` y `fixtures`. Los mismos tres repos estan clonados en el MacBook
(`~/p`) para desarrollar; ahi no esta instalada. Trampa de `DEVELOPMENT.md`:
desinstalar desde Blender puede borrar el directorio, es decir el checkout;
quitar el symlink a mano antes. El `ValueError: list.remove(x)` que Blender
5.2 imprime al cerrar es suyo (`copy_global_transform.unregister`), salio
antes de instalar nada.

El escenario ya se ve en BlenderDMX desde el 2026-09-23: `qlctool mvr`
escribe `QLC+ Setups/Vibra-split.mvr` con un GDTF generado de cada `.qxf`
dentro, y `render_mvr.py` de [spectalive/qlc-blenderdmx](https://github.com/spectalive/qlc-blenderdmx) lo importa sin
ventana en el mini, lo enciende y lo renderiza (`docs/blenderdmx.md` alli;
cerrado en `TODO_LOG.md`).

- [ ] **Mirar el render y el `.blend` en el mini.** `~/p/vibra-blender/vibra.png`
  y `vibra.blend` (abrirlo con Blender con ventana: `open -a Blender
  ~/p/vibra-blender/vibra.blend`). Lo que se decide mirando: si las
  primitivas (caja, base/horquilla/cabeza) bastan o hace falta malla por
  aparato, si el humo (`volume_density` 0.08) y el angulo de los haces
  convencen, y si algun aparato mira a donde no debe.
- [ ] **Segunda salida en QLC+.** El motor admite varios output patches por
  universo (`m_outputPatchList`, `engine/src/universe.h`): DMX USB al rig y
  Art-Net al mini a la vez. Probado el 2026-09-23 con el `.qxw` editado a mano
  (la linea exacta esta en `docs/blenderdmx.md` de spectalive/qlc-blenderdmx). Falta decidir si la escribe
  `qlctool` (con la IP del mini como parametro) o se pone a mano en el Mac
  del show. Mientras, la copia probada no esta en el repo.
- [ ] **Subir el parche de `SO_REUSEPORT` a BlenderDMX.** Commit `de60af6` en
  `~/p/blender-dmx` (main local sobre `569040f` de upstream): sin el, Blender
  no puede escuchar en 6454 si QLC+ ya esta en la misma maquina. Hace falta un
  fork en GitHub y un PR a `open-stage/blender-dmx`.
- [ ] **Decidir: arreglar el 3D de QLC+ o seguir con BlenderDMX.** Medido en
  el codigo de QLC+ (`~/p/qlcplus`, master `82e541d`) el 2026-09-23, esfuerzo
  para alguien nuevo en ese codigo, sin medir en pantalla:
  - Barra de varias cabezas: 0,5-1 dia como barra de haces sin malla
    (`MultiBeams3DItem`), 1,5-3 dias con una luz por cabeza en
    `Fixture3DItem.qml:163-171`, que es donde se pierde la cabeza.
  - Humo local que sigue al DMX de la maquina: 3-5 dias, visible solo dentro de
    un haz; +3-5 dias para verlo salir de la maquina sin luz.
  - Gobos: ya se proyectan en haz y suelo; mas nitidos y con color, 1-2 dias.
  - GPU del Mac: ya usa la GPU, por OpenGL 3.3 que macOS traduce a Metal
    (Qt 6.10.3; `qmlui/main.cpp:53-56` fuerza OpenGL). Metal nativo: 1-2
    semanas reescribiendo 16 shaders para el backend RHI de Qt3D, modulo
    deprecado desde Qt 6.8. Paso barato primero, 1-3 dias:
    `renderPolicy: OnDemand` esta comentado en `DeferredRenderer.qml:27`, asi
    que pinta cada fotograma aunque nada cambie.
  - Nada de esto pinta los paneles en modo Auto.
  - Probado el mismo dia en el mini, rama local `multihead-colorchanger` de
    `~/p/qlcplus` (commits `f067a79`, `e67caf2`, sin subir), compilado con Qt
    6.11.2 de brew y lanzado desde `~/p/qlcplus-test` sin E/S:
    - Cabezas: una CLB2.4 con cabezas roja, verde, azul y blanca pinta cuatro
      haces; sin el cambio, un solo haz blanco (`multihead-before.png`,
      `multihead-after.png`). Unas dos horas con la compilacion.
    - Redibujado a peticion: escena quieta, GPU 100 % -> 12 % y CPU del
      proceso ~72 % -> 10 %; con colores cambiando cada 0,3 s sigue
      redibujando (GPU ~65 %). Estrobo (brillo alterna 142 / 220) y barrido
      de pan redibujan bien a peticion. Sin probar: EFX.
    - Gobos (`55faf9e`): el color del gobo tine el haz y el suelo, y la
      textura lleva mipmaps y filtro anisotropico; antes el shader solo leia
      el alfa, asi que un gobo de color salia blanco (`gobo-before-final.png`,
      `gobo-after-final.png`).
    - Humo (`ec41617`): cada maquina Smoke/Hazer pinta su chorro segun su
      canal de salida, en el color de sus propios LEDs, sube en 1,5 s y se
      va en 3 s (chorro) o 30 s (hazer); un haz que lo cruza se ve mas
      denso. Con humo en el aire la GPU sube a ~85 %; sin humo vuelve a 10 %
      a los 5 s (`smoke-after.png`). Unas tres horas.
    - Rendimiento, medido con Metal System Trace (Xcode 27 ya estaba en el
      mini; `xctrace` se usa directo en
      `/Applications/Xcode.app/Contents/Developer/usr/bin/`, sin aceptar la
      licencia). QLC+ renderiza a 50-60 fps en cuanto algo se mueve (cada
      tick DMX de 50 Hz y las animaciones de pan/tilt redibujan):
      - El humo costaba 9,5 ms por fotograma: marchaba una esfera de 8,7 m
        alrededor de cada chorro. Con un cilindro ajustado al chorro
        (`75c7ebe`) la pasada mas cara baja a 4 ms (GPU 105 % -> 82 %).
      - Texturas RGBA32F -> RGBA16F (`6bcd3c8`): cuatro haces moviendose,
        15,9 -> 9,9 ms por fotograma, 26 -> 57 fps, GPU 77 % -> 61 %. Imagen
        igual. La prueba anterior (84 -> 80 %) estaba tapada por el humo.
      - Lo que queda por fotograma, ~9,5 ms: G-buffer 1,8, luces 1,9, cada
        haz encendido ~0,9 (ray-march), gamma/FXAA 1,3. Crece con cada haz
        encendido; `Calidad` media en los ajustes del 3D baja los pasos.
      - No eran: las 34 cabezas apagadas (no generan pasadas en GPU), ni los
        pixeles de la ventana (los targets son 1024x1024 fijos).
      - 2026-09-24, mas en la rama: sin MSAA en el Scene3D (`0903b6a`, ya
        hay FXAA; 11,1-11,7 -> 10,0-10,3 ms) y FXAA pinta directo en pantalla
        sin la copia final (`531276f`, 9,4-10,1 ms, poco). Banco repetible:
        `~/p/qlcplus-test/bench.sh <tag>` (`LOOP=dmxloop.py` para un fundido
        de color sin movimiento).
      - Limitar el 3D a 30 Hz agrupando cambios DMX: probado y deshecho. Con
        un fundido a 50 Hz el 3D ya pinta solo ~20-25 fps (GPU 18-28 % sin
        limite, 18-23 % con el; ruido). El freno es la CPU, no la GPU.
      - CPU (Time Profiler, fundido de color): ~58 % de un nucleo; el hilo
        principal hace todo el render de Qt Quick y Qt3D. El 11,4 % es
        `StringToInt::lookupId` dentro de
        `RenderView::updateLightUniforms` (Qt3D 6.11.2,
        `src/plugins/renderers/opengl/renderer/renderview.cpp`, ultima linea
        de la funcion): busca `"envLightCount"` sin `static` en cada comando
        de cada fotograma, con un lock global, desde varios hilos. Es un bug
        de Qt3D, no de QLC+. Probado el 2026-09-24: Qt3D 6.11.2 compilado en
        `~/p/qt3d` (sin assimp) y cargado solo en la instancia de prueba con
        `DYLD_FRAMEWORK_PATH=~/p/qt3d/build/lib` y
        `QT_PLUGIN_PATH=~/p/qt3d/build/share/qt/plugins`; el parche (hacer
        `static` esa busqueda) esta en
        `~/p/qlcplus-test/qt3d-envlightcount.patch`. Mismo build, una linea
        de diferencia, `cpubench.sh`: sin parche 6,30 / 6,70 s de CPU en 8 s
        (lookupId 16-20 %), con parche 5,23 / 6,23 s (lookupId desaparece);
        ~12 % menos CPU. Verificado el 2026-09-24: sigue igual en `dev`,
        6.12, 6.11 y 6.10, y el renderer RHI tiene lo mismo
        (`rhi/renderer/renderview.cpp:1546`); es la unica busqueda sin cachear
        por comando en los dos renderers. Sin reporte previo: el JIRA de Qt
        (ahora `qt-project.atlassian.net`) solo nombra `envLightCount` en
        errores de shader, y Gerrit no tiene cambios sobre esa linea (los dos
        que salen, 186545 y 204665, son de 2017). El cambio para Gerrit esta
        enviado el 2026-09-24 como
        https://codereview.qt-project.org/c/qt/qt3d/+/773761 (rama
        `cache-envlightcount-id` de `~/p/qt3d`, commit `0b8bb46` sobre `dev`,
        los dos renderers, `Pick-to: 6.11 6.10`), autor Cristian Deluxe
        `me@cristiandeluxe.dev`, CLA individual firmado. Cuenta de Qt y
        Atlassian en 1Password (boveda Cristian); accesos en el brain
        (`access-map`, seccion Qt Project). Reportado como
        https://qt-project.atlassian.net/browse/QTBUG-150764 (Qt3D, 6.11.2),
        enlazado en el change con `Fixes: QTBUG-150764` (patchset 2). Falta:
        lo que diga la revision.
      - [~] 2026-09-24, enviado a QLC+ desde el fork `CristianDeluxe/qlcplus`
        (autor `me@cristiandeluxe.dev`): #2159 multicabeza, #2160 gobos, #2161
        rendimiento (a peticion, RGBA16F, sin MSAA, FXAA sin copia), #2162
        humo con el cilindro (encima de #2160, tocan la misma linea). Cada
        rama compila sola desde `master` (`82e541d`); solo probado en macOS.
        Tests de QLC+: `ninja check` necesita `lxml` en el PATH o da verde
        sin correr nada; con el, engine pasa salvo
        `InputOutputMap_Test::profileDirectories` (ruta de bundle macOS,
        engine sin tocar) y el script para ahi. Falta: lo que diga el autor.
      - Ojo con `xctrace record`: una grabacion de 8 s se quedo colgada 8
        minutos; lanzarlo siempre con `timeout`.
  - **Las LED Spray Fog echan el humo en horizontal en el 3D.** `smoke.dae` echa el humo
    por su frente (+Z de la malla, el disco `emitter` en z=0,516), y el parche
    las deja sin rotar, asi que el chorro sale horizontal hacia el publico.
    Para que suban hace falta `x_rot 90` (QLC+ gira -90 sobre X: +Z pasa a
    +Y); probado a mano en `Vibra-offline.qxw`. Siguiente paso: regla en
    `qlctool check` que vea una maquina de humo vertical sin rotar, test, y
    el generador.
  - **`qlctool install --check` se salta los gobos en silencio si no encuentra
    la carpeta `Gobos`.** Desde la Task 1 del Plan B (2026-09-25)
    `qlc_gobo_dir()` resuelve el bundle instalado que descubre
    (`qlcplus_candidates`); en el mini es `QLC+ 5.2.2.app/Contents/Resources/Gobos`,
    que ya tiene `BEAM-230W-7R`, y `--check` dice "30 file(s)" con los 18
    gobos `synced` (verificado 2026-09-25). Lo que queda: si no hay carpeta de
    gobos, `install_plan` los omite sin avisar. Siguiente paso: que `--check`
    falle en ese caso, test de regresion, y que los gobos vayan a cada bundle
    instalado (el 5.x es el del show; la validacion prefiere el 4.x cuando
    puede correr).
- [ ] **Lo que ningun visor pinta**: los paneles WX-60WPS en modo Auto (ch7
  efecto, RGB a 0) generan el color en el hardware. Sigue siendo "en sala".

## Repaso del dueño sobre la programación (2026-09-22)

El dueño revisó el show entero y pasó una lista de catorce cosas. Lo que se
cerró ese día está en `TODO_LOG.md` con la evidencia (cuatro reglas nuevas,
cuatro tests de regresión, los tres workspaces regenerados y validados). Lo que
queda espera al rig o a otro repositorio:

- [ ] **Ver en sala los cuatro modos de color automáticos.** `Colores
  completos` (W, los 17 de la paleta sin blanco más cinco contrastes de dos
  colores), `Colores simples` (C, seis primarios), `Pastel tenue` (L, los 17
  mezclados un 55% hacia el blanco) y `Multicolor` (R, los seis pasos salvajes,
  "solo por si acaso", que ningún estado arranca). Desde la noche del
  2026-09-22 ninguna rueda pisa el blanco ("en directo se ve todo iluminado")
  y las que arranca un estado no ponen más de dos colores a la vez; los
  contrastes son complementarios entre roles (ámbar/azul, amarillo/azul,
  rojo/cyan, magenta/verde, rojo/azul) y las mezclas dentro de un grupo,
  vecinos (rojo/amarillo, magenta/azul...). Los cuatro están en el marco COLOR
  de JUGAR, que es solo: elegir uno para los otros. Siguiente paso: mirar si
  el pastel se distingue del blanco en la sala encendida - si no, subir
  `SHARE` en `qlctool/pastel.py` - y si los cinco contrastes se leen como dos
  colores y no como "feria".
- [ ] **Ver en sala los movimientos nuevos.** Cada figura tiene ahora tres
  botones: fase repartida (el de siempre), `Simultaneo` (todas las cabezas a
  la vez) y `Alternado` (cada cabeza al lado contrario, `every_other`). Los
  beams han ganado `Square` y `Lissajous`, así que ya no se quedan quietos con
  esos dos. Y la figura de los beams dura ahora la mitad que la de los washes
  (8 s contra 16), para que rimen; confirmar que no queda demasiado rápido para
  una 7R. Son 26 picks en el marco CABEZAS, a 15 columnas y dos filas: el marco
  no puede crecer porque GOBOS empieza 148 px por debajo, así que los botones
  son estrechos - mirar en la tablet si el texto se lee.
- [ ] **Confirmar que los golpes de color salen del mismo color en toda la
  sala.** El dueño vio "los rgb salen como mezclados con blanco". La mitad era
  el emisor White sumándose al RGB (cerrado, `blanco pagado dos veces`) y la
  otra mitad puede ser la tabla de nombres de la rueda de las 7R, que sigue sin
  confirmar - ver el item del 2026-09-02 sobre `color_wheel_match`. Con la
  rueda mal nombrada, un golpe rojo manda a los beams un color vecino.
- [ ] **Decidir en sala la matriz de dos colores sobre Cabezas.** `Alternate
  Verde Menta/Azul Profundo` pinta pares e impares de dos colores sobre los
  ocho cabezas RGB y deja los cuatro beams en una posición fija de rueda. La
  regla nueva no la mira (una matriz habla de píxeles, no de fixtures, como en
  `rueda de color`), así que es una decisión: o se reparten los dos colores
  entre los beams por su rueda, o se acepta.
- [ ] **"Quitar y poner un color no apaga las beam" - probar la hipótesis en
  sala antes de tocar nada.** Un pick de color en JUGAR es un Toggle en un marco
  solo: al repetirlo se para y deja la familia quieta. Al pararse, el RGB se
  suelta y esos aparatos se apagan, pero la rueda de color de las 7R es LTP -
  nadie la reescribe - así que los beams se quedan con el color puesto y
  encendidos por el nivel de energía. Es asimetría, no capricho. El arreglo
  candidato es una escena base que corra siempre y sea dueña de la rueda: su
  fader queda por debajo del pick (`Universe::requestFader` encola por
  prioridad y orden), así que al soltar el pick la rueda volvería a la base.
  Antes de implementarlo hay que verlo: con AUTO parado, pulsar un pick de
  color, volver a pulsarlo, y apuntar qué hacen los cuatro beams. Si se quedan
  encendidos, hace falta la base; si se apagan, el fallo era el botón COLOR BEAM
  que ya no existe. Hay una segunda lectura, y es decisión del dueño: puede que
  lo que sobre no sea el color de los beams sino que soltar un pick deje la sala
  a oscuras en vez de devolverla a AUTO. Eso se decide, no se adivina.
- [ ] **El desk de la tablet tiene que dibujar el campo `icon`.** `Vibra.desk.json`
  lleva desde hoy un `icon` por control (111 de 138), separado del `caption`
  (`leading_glyph`); el esquema sigue siendo 2 porque añadir un campo es
  compatible. La app vive en otro repositorio: hasta que lo pinte, la tablet
  sigue sin iconos aunque el mapa ya los traiga.
- [ ] **Iconos en el resto de la consola.** 134 de 600 botones llevan glifo:
  los estados, los golpes, el humo, las capas y los picks de las cinco
  familias. Los bancos de color (teclas 1-0), la librería de matrices y la
  rueda de los BEAM siguen sin marca. Decidir si hace falta o si el color del
  botón ya lo dice.

## Auditoria cruzada de los programas (2026-09-02, Claude + Codex)

Dos simuladores independientes de la salida DMX (ninguno usa las reglas de
`qlctool check`), cruzados en dos rondas hasta coincidir, sobre los tres
workspaces. `qlctool check` decia `503 botones revisados, ningun problema` en
los tres. Encontraron diez cosas; nueve eran defectos y se cerraron el mismo
dia con ocho reglas nuevas, ocho tests de regresion y el generador corregido
(evidencia en `TODO_LOG.md`, 2026-09-02). Lo que queda de aquella lista:

- [ ] **Confirmar en sala los bancos y los picks mantenidos.** Desde
  2026-09-02 los bancos de color (teclas 1-0), las mezclas, los gobos, el
  prisma, el color de los beams y `Escenario` son Flash con `Override` (y
  `ForceLTP` los de color): van mientras se mantiene la tecla y el estado
  vuelve al soltar. El motor lo garantiza (`Scene::writeDMX` con
  `forceLTP=true` salta el HTP; el fader Flashing va detras de todos), pero
  nadie lo ha visto con el rig delante. Siguiente paso: con `AUTO` en cyan,
  mantener `1` y comprobar que los cabezas salen rojos, no blancos, y que al
  soltar vuelven a cyan sin salto.
- [ ] **Confirmar `STROBO` / `STROBO SUAVE` mantenidos** (ahora escenas de
  shutter, como `Flash Color`): las barras LED no estroban porque no tienen
  shutter, y eso es fisica, no un fallo - si el dueño quiere las barras en el
  estrobo, la unica forma sobre una sala encendida es una matriz `Strobe` en
  su grupo, que suma HTP con el color de la rueda.
- [ ] **`<ExcludeFade>` en las ruedas: mirar la rueda de color de los 7R
  durante `AUTO`.** Debe saltar de color a color; si sigue barriendo los
  intermedios, QLC+ 5.2.2 no honra el tag y hay que poner fade 0 en las
  escenas que escriben ruedas (`rueda fundida` lo veria).
- [ ] **Los blancos usan ahora el emisor White** (Mini Led ch7, MAC WASH
  ch12/16/20). Desde el 2026-09-22 el reparto lo hace `rgbw_split`, no
  `white_level`: la parte acromatica sale del emisor blanco y se **resta** de
  R, G y B, salvo cuando la peticion ya es acromatica (r = g = b: luz de
  trabajo, flashes), que va a los cuatro emisores. Queda decidir en sala si el
  blanco resulta mas frio o mas brillante que el RGB de antes.
- [ ] **`HUMO VERT` saca la columna del color de la sala, no blanca** - es
  decision del dueño del 2026-08-30 ("la luz solo salia la blanca, no hacia
  las transiciones de colores"), no un fallo; el item del montaje del
  2026-08-29 que pedia "columna blanca" esta desfasado.
- [ ] **Confirm JUGAR on site.** Under AUTO, pick red and verify the entire
  rig, including the 7R heads and bars, turns red; press F1 and verify the
  pick releases; press AUTO colores and verify the wheel returns.

Descartado en la auditoria (para no repetirlo): el `<Mode>` numerico de los
EFX es correcto (`efxfixture.cpp:291` usa `toInt()`); no hay sombra HTP dentro
de los niveles; el dimmer de los paneles bajo AUTO lo abren las escenas
`Paneles - Effect N` (no `Pixeles ON`, como dice la doc); pan 0 / tilt 130 de
los beams es deliberado; una escena en marcha reescribe sus LTP cada ciclo
(AutoRemove solo en fade-out), asi que la logica de `estrobo pegado` y
`acento sin dueño` es correcta.

## Revision de manuales y aprovechamiento del rig (2026-09-01)

Se buscó manual para todo lo parcheado y se midió, fixture por fixture, qué
canales escribe el show y cuáles no toca nunca (script de cobertura sobre
`checks/driven_channels.py`, los tres workspaces dan lo mismo). Lo cerrado está
en `docs/rig.md` (tabla de verificación) y en `TODO_LOG.md`; esto es lo
que queda.

- [ ] **Los nombres de los colores de la rueda de las 7R, confirmar en sala
  (2026-09-02).** El perfil `Beam 230 SC-295-16CH` de Daslight es nuestra
  definición rango por rango (estrobo, pasos de color y gobo, prisma, reset,
  lámpara), pero nombra los catorce colores como la rueda Sharpy que copian
  los clones: blanco, rojo, naranja, aguamarina, verde, verde claro, lavanda,
  rosa, amarillo, magenta, cyan, CTO 2, CTO 1, CTB, azul oscuro. La nuestra
  dice rojo, naranja, amarillo, verde, azul, rosa, ice, rosa claro, blanco
  claro, azul claro, blanco cálido, UV, gris, amarillo claro. Como
  `color_wheel_match` elige el color del beam **por el nombre**, si la tabla
  tiene razón `Azul` manda 40-47 (verde claro) y `Amarillo` 24-31
  (aguamarina). En sala: `qlctool probe` sobre el canal 8 de una 7R, apuntar
  el color real de cada posición de 8 en 8, y corregir los nombres en
  `BEAM-LIGHT-230W-7R.qxf` (los rangos no se tocan). Regenerar después: las
  escenas de rueda cambian de valor si cambian los nombres.
- [ ] **El zoom de las MAC WASH solo se usa abierto.** Es el único fixture del
  rig con el ancho del haz en un canal (6-50 grados) y el show manda el extremo
  abierto en todos los looks (`zoom_wide_pairs`; desde 2026-09-02 es 0, no
  255, ver el item de las MAC WASH). Cerrado da un haz tipo beam que en humo
  se ve; un pulso de zoom al ritmo es un efecto que no cuesta nada. Decisión
  del dueño, y después generador + regla (la regla `zoom sin declarar` hoy
  exige justamente lo contrario, habría que darle una excepción con dueño).
- [ ] **El frost ("Atomization", canal 12) de las 7R no se usa nunca.** Siempre
  a 0. Con frost el beam pasa a wash suave para el modo "tranquilo" o "charla".
  Probar en sala qué hace el canal (la definición solo tiene un rango 0-255) y
  decidir.
- [ ] **Velocidad de pan/tilt (canal 5) sin escribir en las cuatro cabezas con
  ese canal.** CromoWash, MAC WASH y 7R declaran `FastSlow` (0 = rápido) y la
  MiN Wash, ya corregida contra su manual, también: a 0 siguen el EFX sin
  retardo, que es lo que queremos. No hay nada que cambiar mientras nadie lo
  escriba; si un día se quiere movimiento "suave" es este canal y no el tempo
  del EFX.
- [ ] **Mini Led Moving Head: confirmar en sala los canales 9-16 (adoptados
  el 2026-09-02).** Tres fuentes que coinciden en los ocho primeros canales
  (manual Betopper/Big Dipper LM108, manual SHEHDS 12x12W, personalidad
  ChamSys LM108) dan 9-16 como `velocidad pan/tilt, macro de color, velocidad
  macro, programa, velocidad programa, pan fine, tilt fine, reset (150-255)`,
  y la definición ya lo declara así (detalle en `docs/rig.md`). El show
  escribe a 0 el programa (con cada color) y los fine (con cada aim); nada
  más. En sala: `qlctool probe` sobre 18 o 19, subir el canal 10 por encima
  de 10 (debería pisar el color), el 16 a 150 (debería resetear), y ver si el
  8 a 0 es shutter abierto. Si algo no cuadra, volver esos canales a
  `NoFunction` y regenerar.
- [ ] **Vortex PC-64: solo lo decide un banco de pruebas.** Búsqueda del
  2026-09-01 sin resultado (la marca no existe en internet; es etiqueta del
  dueño sobre un PAR genérico). Los PAR64 de 5 canales vienen en tres mapas
  incompatibles y uno de ellos (Stairville, 290x260 mm, muy parecido a este de
  292x266) no tiene ni dimmer ni strobe: canal 1 modo, 2-4 RGB, 5 velocidad.
  Un PAR solo, `qlctool probe`, y mirar (a) si el canal 4 a 0 apaga con RGB
  arriba, (b) si el 5 estroba y en qué valor para.
- [ ] **En el Mac del show, después de cada `git pull`: `qlctool install
  --check`.** En este Mac cuatro de las once definiciones instaladas llevaban
  una semana de retraso (rangos del blade de las 7R, grupo Intensity de la
  bomba de humo vertical, las tres cabezas de la MAC WASH). Casi seguro que el
  Mac del show está igual o peor. El comando copia definiciones, perfil y gobos
  y avisa del drift; reiniciar QLC+ después.

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
     de 122 px de alto a 102. Confirmar que se sigue leyendo a 13". (Al
     2026-09-22 son 605 botones en cuatro paginas, y el marco CABEZAS baja a
     15 columnas para meter sus 26 picks en dos filas: mirar eso tambien.)

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
  `beam_focus = 127` (`qlctool/vibra/tuning.py` in spectalive/qlctool, y
  `[fixture_tuning] beam_focus` en los tres `QLC+ Setups/vibra*.toml`), que es
  el medio del recorrido y una primera pasada, no una medida. En sala: poner un
  gobo, subir/bajar ese canal a mano hasta que el dibujo este nitido a la
  distancia real, y dejar ese numero en los cuatro sitios, en este orden:
  `tuning.py` y los `vibra*.toml` del rig congelado en spectalive/qlctool (su
  test de igualdad `tests/test_load_show_description.py` falla si solo se
  cambia una copia), release y tag, subir el tag en `requirements.txt`, los
  tres `vibra*.toml` de aqui, y re-grabar `tests/vibra_baseline.json` con el
  visto bueno del dueño. Mientras tanto tambien hay
  `Gobo Repartido 1-8` (cada cabeza un gobo distinto) y el prisma girando en
  tres velocidades: mirar si el reparto se lee bien o marea.

- [ ] **El pad, la proxima vez: USB o Bluetooth, no los dos (2026-08-30).** La
  noche del 29 "no pude usar el pad porque ni reseteandolo reconocia las
  teclas", con el cable y el BT puestos a la vez. Causa, ya medida y escrita en
  el README de spectalive/smc-pad: **con USB conectado el pad manda su MIDI por USB y
  el lado BLE se queda mudo**, y el workspace escucha el puerto `ble device`.
  Resetear el pad no arregla eso. Comprobar en sala: quitar el USB (que es
  ademas lo que quiere el puente de LEDs, que sostiene el BLE), o dejar el USB
  y en Entradas/Salidas apuntar el universo 1 al puerto USB y **guardar el
  fichero** — `newshow` respeta el puerto que el fichero ya trae.
  `swift midiports.swift` (spectalive/smc-pad) lista los puertos con el nombre que usa
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

- [ ] **Las dos MAC WASH 1915Z: confirmar en sala lo que dice el manual de
  su gemela (2026-08-29, actualizado 2026-09-02).** Llegaron en lugar de las
  CromoWash, parcheadas en 23 CH en DMX 345 y 368, en el sitio de las
  CromoWash del back truss (4 y 7); las CromoWash siguen parcheadas y
  aparcadas como spares en el plano. El manual de Mac Mah sólo da la tabla de
  canales; el de la **Algam MW19x15Z** (misma cabeza, misma matriz, manualslib
  3158887) da lo que faltaba y la definición ya lo lleva:
  1. **Zoom: 0 = abierto, 255 = cerrado.** Lo teníamos al revés: el show mandó
     255 en todo look hasta el 2026-09-02, o sea las dos lyres a 6 grados toda
     la noche del 29. Ahora manda 0. **Si en sala salen cerradas**, volver el
     preset a `SmallToBig` en el `.qxf` y regenerar.
  2. **Estrobo: 0-9 sin estrobo, 10-255 lento a rápido** (el manual). ChamSys
     lo partía en cuatro bandas y ponía el reset en 100-109; el manual dice
     reset 250-255. Manda el manual.
  3. **Function mode: 0-29 = control DMX**, ya no es suposición: el manual da
     la tabla entera (colores fijos, cambios de color y cuatro efectos auto).
  Y confirmar en el 3D que las dos caben donde estaban las CromoWash (son algo
  más grandes: 325x188 mm contra 296x184).

- [~] **SMC-PAD LED feedback en QLC+ — funcionando, con pulido pendiente
  (2026-08-29).** Todo el protocolo resuelto y documentado en
  https://github.com/spectalive/smc-pad (README + decompile; hasta el 2026-09-26 en
  `tools/smc-pad/`). El puente `qlc_led_bridge.swift`
  mantiene la sesión GATT del pad, publica el puerto MIDI virtual
  "SMC-PAD LED Bridge" y pinta cada pad con su color de paleta
  (`QLC+ Setups/Vibra.pads.json`, de `qlctool pad-palette`): atenuado en reposo, full al activarse el
  botón en QLC+. Los botones de la consola llevan el mismo color. Verificado:
  QLC+ feedback -> pad enciende. **Se instala una vez con
  `~/p/smc-pad/install-bridge.sh ~/p/DMX-Fixtures-qlctool/"QLC+ Setups/Vibra.pads.json"`**
  (hoy no esta instalado en el mini: pide el pad delante y aceptar el
  permiso de Bluetooth; en el `TODO.md` de smc-pad) y arranca solo en cada inicio de sesión
  (agente de launchd, `.app` firmada, se resucita si se cae — verificado
  2026-08-29 matándolo). Cargar `Vibra.qxw` después del puente, no antes. En
  Entradas/Salidas el universo 1 debe tener Input "ble device" (omni "1-16") y
  el bridge como Output **y Feedback** (el `<Feedback>` es el truco: el ojo de
  QLC+ no lo crea solo; ya está en el .qxw). Pendiente:
  1. Afinar la paleta y el brillo de reposo en sala. Los dos los calcula
     qlctool (`smc_pad_colors.py`, `idle` = `active // 6`): cambiar alli,
     regenerar `Vibra.pads.json` y reinstalar el puente.
  2. **Probar la capa manual (banco 2) con el pad delante.** El remapeo de
     2026-08-29 la movió de SHIFT (que no manda MIDI) a `PAD BANK`, y el
     puente ya pinta las notas 52-67; falta pulsar `PAD BANK` en sala y
     confirmar que los ocho botones de la página 2 disparan y encienden.
  3. Si se reinicia el puente hay que recargar el workspace (el puerto MIDI
     virtual se recrea con identidad nueva). Movido al `TODO.md` de
     spectalive/smc-pad el 2026-09-26.
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
  four bugs on its first run. `.venv/bin/qlctool check
  "QLC+ Setups/Vibra-split.qxw"` from the repository root. New rule when something misbehaves: find
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
  `tests/test_old_show_recovery.py` de spectalive/qlctool (10 tests fechados). Todo
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
  `Rig Multicolor 1/2` en la rueda (beams en rainbow scroll ~186; el plasma de
  las barras salio el 2026-09-22 y en su sitio va una matriz de color plano),
  `Ciclo Paneles Mixto` (8 min efectos / 4 min manual siguiendo
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
  pulsado por otra funcion` + test. (3) **COLOR BEAM (`C`) ya no existe**: animaba
  la rueda de color de los 4 BEAM 230W y no tocaba las PAR, pero parecia un
  on/off y se comportaba como un pick ("el boton color beam parece un on of
  pero realmente cambia como la rueda", dueño, 2026-09-22). Los beams toman el
  color del rig y la tecla `C` es ahora el modo de colores simples.
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
  console is now four pages (`show` / `JUGAR` / `control` / `librería`) built by
  `qlctool newshow`; page 1 is seven mutually exclusive room states plus the
  hits, and the energy levels are no longer buttons. Two things only a real
  screen can settle: whether the 28pt/15pt captions read across a dark room at
  1440x900, and whether `PgDn`/`PgUp` change page in operate mode without
  stealing focus. Files: `QLC+ Setups/Vibra-split.qxw` (current patch),
  `Vibra.qxw`, `Vibra-beats.qxw`.
- [~] **Verify the remaining undocumented fixtures on site.** Online search
  (2026-08-24) settled the Chauvet MiN Wash, and on 2026-09-01 its manual was
  recovered into `Manual/` and the definition corrected against it; the same
  pass verified the LED Bar 240/8 against its manual and filed the AF-150's.
  What paper cannot settle: Generic BEAM 230W 7R (owner-verified on the
  hardware, no manual matches), Vortex PC-64 LED S (no such brand online;
  three incompatible OEM layouts), HYULIGHTS WX-60WPS-48PARTITION and the
  LED Beam Mini (a strong OEM candidate for channels 9-16 - see the 2026-09-01
  section above). The check is a five-minute job on site: `qlctool probe
  <show> <fixture-id> --base "7=255" --buttons` builds one scene per channel
  plus a walk chaser - press play and write down what each channel does. Do it
  in the same session as the physical-rig confirmation.
- [~] **Review `QLC+ Setups/Vibra.qxw`** - the canonical show built by the
  toolkit. Rebuilt 2026-08-25 after the owner reported that pressing AUTO
  stopped the show and that the console was an unusable 2662px list. Both were
  real and are fixed (see `TODO_LOG.md`). Al 2026-09-22 son 1629 funciones y
  605 botones en 1440x900, y QLC+ 5.2.2 lo carga limpio. Copias en
  `~/Demos-qlctool/` en las dos maquinas. La rama ya esta mezclada
  (2026-09-22). Queda: que el dueño lo corra en el portatil del show y diga si
  AUTO aguanta y si la disposicion funciona, y despues archivar los dos
  workspaces DeluxeEventos - hoy siguen en `QLC+ Setups/` y
  `DeluxeEventos2.qxw` es el material de prueba de `tests/test_play_generators.py`
  y `tests/test_old_show_recovery.py`; desde 2026-09-25 esos tests viven en
  spectalive/qlctool y leen su copia congelada del rig, asi que archivarlo
  aqui ya no los toca.
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
  - Six checker rules with dated regression tests (`docs/checks.md` in spectalive/qlctool):
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
  Ambiente 4 min -> Fiesta 8 -> Peak 40 s -> Fiesta 8 (`ambient_ms`,
  `party_ms`, `peak_ms` measured 2026-09-22), with the colour bed and the
  haze running underneath so a level change never blacks the room out. The
  numbers are a first guess: if the quiet level feels dead or the peak feels
  rationed, they are `ambient_ms`, `party_ms` and `peak_ms` in
  `qlctool/vibra/timing.py` in spectalive/qlctool and `[timing] levels` (`ambient_s`,
  `party_s`, `peak_s`) in the three `QLC+ Setups/vibra*.toml`. Change all four
  in order: `timing.py` and the frozen rig's tomls in spectalive/qlctool (its
  equality test `tests/test_load_show_description.py` fails if only one copy
  is edited), release and tag, bump the tag in `requirements.txt`, the three
  tomls here, and re-record `tests/vibra_baseline.json` with the owner's
  consent.
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

## QLC+ feature audit (2026-08-27)

Findings from a full scan of the QLC+ source clone (`~/p/qlcplus`, master =
5.3.0-git of 2026-08-22 — **newer than the installed 5.2.2**, so every QLC+5
feature below gets verified against the real binary before we build on it),
the official docs (docs.qlcplus.org v5 + release notes), and the generated
`Vibra-split.qxw`. The show used 5 of 10 function types, 4 of 39 RGB scripts,
0 sliders and 0 MIDI/OSC inputs when this was written; al 2026-09-22 son dos
sliders y 24 bindings MIDI del SMC-PAD. A Codex cross-check of these findings ran the
same day; anything it refutes gets corrected here.

### Unused QLC+ capability worth adopting (priority order)

- [ ] **Casi ningun slider en la consola** (dos al 2026-09-22: `Master
  General` y el GrandMaster; el texto original decia cero). Three concrete
  uses: (a) Submaster
  slider scaling Peak's frame — `Dimmer Chase` being HTP-shadowed by
  `Intensidad Total` there is fixed a different way now (TODO_LOG.md,
  2026-08-27: the chase owns Peak's dimmers outright), so this would be a
  live-adjust nicety, not a correctness fix; (b) Adjust-mode sliders driving
  live function attributes — EFX Width/Height/
  Rotation and RGBMatrix Color 1-5 / Pattern / script properties are all
  registered live attributes (`rgbmatrix.cpp` registerScriptPropertyAttributes).
  The GrandMaster slider (c) shipped separately — Task 3, TODO_LOG.md
  2026-08-27.
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

## Calidad del codigo

La deuda de calidad del toolkit vive en el `TODO.md` de spectalive/qlctool
desde el 2026-09-26 (ronda G): ratchets de ruff y mypy, baseline estructural
de codeality y el siguiente fichero a partir (`live_console.py`). Este repo ya
no tiene codigo de toolkit propio.
