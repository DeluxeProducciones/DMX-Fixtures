# M-VAVE / Sinco SMC-PAD — manual del fabricante

Transcripción del manual oficial, recuperada el 2026-08-29 de
<https://manuals.plus/sinco/smc-pad-midi-controller-manual>. El resto de esta
carpeta son PDF del fabricante; aquí no hay PDF porque el sitio no lo sirve a
una descarga directa, así que esto es el texto transcrito. Las frases entre
comillas son literales del manual; lo demás son encabezados de su propia
estructura.

**Por qué está guardado aquí.** El 2026-08-29 el pad dejó de disparar el show
entero. La causa fue que se pulsaron combinaciones de `SHIFT` sin saber qué
hacían: `SHIFT` no manda MIDI, **reconfigura el aparato**. Una pulsación
transportó el teclado un semitono y otra lo sacó de su preset, y ninguno de los
números del show volvió a coincidir. La tabla de `SHIFT` de más abajo es la
parte de este documento que hay que leer antes de tocar el pad.

---

## Contenido de la caja

- SMC-PAD
- Cable USB-C
- Manual de usuario

## Tipos de conexión

**USB:** "Plug the cable through the USB port to the Windows/Mac it will
automatic be recognized, When plug into Windows/Mac the SMC-PAD will be charging
at the same time; (Red light: charging, Green light: charging complete)"

**Inalámbrica:** "Press and hold the BT button, when the light flashing the
wireless function is activated, when the light stay on was connection
successfully"

**Adaptador inalámbrico:** "Plug Wireless Adapter B into Windows/Mac, connection
was successfully when both lights stay on"

**Bluetooth directo:** "Activated BT function of Windows/Mac/ios/Android, Select
SMC-PAD on the list (Wireless connection requires devices to support BT5.0. For
Windows, installation of the BLE MIDI driver is necessary)"

**MIDI OUT:**
- Por cable: "Utilize the 3.5mm MIDI OUT port located on the back of the device"
- Inalámbrico: "Use Five-Pin wireless MIDI adapter A connecting to device such
  as synthesizer"

"Wireless Adapter A and B are not within the package need to buy additionally"

**Batería baja:** "When the device has insufficient power, both the left and
right buttons will flash simultaneously."

## Panel

### Parte trasera

- **Power:** "Switch to turn on/off the device"
- **Power Indicator:** "The indicator light illuminates red while charging and
  turns green when fully charged"
- **USB:** "USB-C Connection port"
- **MIDI OUT:** "Enables MIDI output for further connectivity"

### Knobs

"Eight assignable 360-degrees rotary encoders; These eight knobs can also send
Aftertouch, Midi CC, Pitch information through setting inside software"

"Hold the 'Note Repeat' function button and simultaneously rotate Knobs 1-4 to
adjust the Note Repeat functionality."

"You can only change settings inside software (Scan the QR code on the back of
the machine to download the software)."

### Pads

"Sixteen RGB back-lit pads with velocity-sensitive & aftertouch; Include Note,
Midi CC, Program Change"

"You can only change settings inside software"

### Botones

| Botón | Manual |
| --- | --- |
| **BT** | "Long press the BT button to turn the BT function on or off." |
| **PAD BANK** | "Switches to the second bank of pads." |
| **KNOB BANK** | "Switches to the second bank of knobs." |
| **Left** (`<`) | "Switches to the previous group of eight tracks on the DAW." |
| **Right** (`>`) | "Switches to the next group of eight tracks on the DAW." |
| **PLAY** | "Initiates the play function in your DAW." |
| **STOP** | "Initiates the stop function in your DAW." |
| **RECORD** | "Initiates the record function in your DAW." |

"When using buttons associated with the DAW, you must select 'Mackie Control' as
the input/output option within the corresponding DAW's control surface."

### SHIFT — lo que reconfigura el aparato

**`SHIFT` no manda ningún mensaje MIDI.** Cada combinación cambia un ajuste
guardado en el pad, y el cambio sobrevive al apagado.

| Combinación | Manual |
| --- | --- |
| `SHIFT` + Note Repeat | "Transforms the 16 pads to modify note repeat settings." |
| `SHIFT` + PAD 1-8 | "Switch between different preset configurations. (Pad 1 is Performance preset, Pad 2 is DAW preset, The rest are user presets)" |
| `SHIFT` + PAD 9-12 | "Adjust the pad's velocity curve. Pad 12 equates to full velocity." |
| `SHIFT` + PAD 13-14 | "Transpose up or down." |
| `SHIFT` + PAD 15-16 | "Shift the pad's octave range up or down." |
| `SHIFT` + PAD15 + PAD16 | "Reset to the default Octave range." |

El manual **no** documenta ninguna combinación para el canal MIDI, ni para
`PAD BANK` o `KNOB BANK`, ni un reset de fábrica, ni un reset de transpose
(solo el de octava).

## NOTE REPEAT

"Either press the 'Note Repeat' button followed by the desired pad, or press the
desired pad and then the 'Note Repeat' button, to activate the note repeat
function."

Con `SHIFT` + Note Repeat activo:

- "Pads 1-8 (Rate): Modify the rate based on the tempo, ranging from 1/4 to
  1/32t."
- "Pads 9-13 (Swing): Set the deviation of notes. The greater the swing amount,
  the more rhythmically varied the repeating notes will be."
- "Pad 14 (Latch): When activated, notes will continue to repeat even after
  releasing the pad."
- "Pad 15 (Sync): Synchronizes the tempo with your DAW. Ensure that the external
  MIDI controller sync function is activated within your DAW"
- "Pad 16 (Tap Tempo): Tap this pad to manually adjust the tempo of the note
  repeat."

Manteniendo el botón Note Repeat:

- "Knob 1 (Rate): Rotate to switch between rates from 1/4 to 1/32t."
- "Knob 2 (Swing): Rotate to adjust the deviation of notes."
- "Knob 3 (Tempo): Rotate to modify the tempo within a range of 30 to 300 BPM."
- "Knob 4 (Latch): Rotate to toggle the latch on or off."

## Características técnicas

| | |
| --- | --- |
| Dimensiones | 227 mm (L) x 147 mm (W) x 38 mm (H) |
| Peso | 520 g |
| Pads | "16 RGB Back-Lit Pads with velocity-sensitive and after touch" |
| Knobs | "8 assignable endless 360 degree encoders" |
| Salidas | "USB-C port; Wireless connection with Windows/Mac/ios/Android; 3.5mm Midi Out Function" |
| Alimentación | "2000mAh Battery supplied or USB-bus-powered" |

## Android

"You need to open the software that supports Ble MIDI, such as FL studio. search
for a MIDI keyboard in your MIDI device and connect it."

---

## Lo que el manual no dice y este show sí necesita

Medido sobre el aparato el 2026-08-29 (`tools/smc-pad/midicap.swift`), porque el
manual no lo documenta:

- Los pads mandan en **canal MIDI 10**; los knobs y los cinco botones del borde
  en el **canal 1**. Por eso la entrada MIDI de QLC+ tiene que ir en omni
  ("1-16"): en un canal fijo se pierde media superficie.
- La nota de un pad dentro de un banco es **35 + número de pad**, contando PAD1
  abajo-izquierda y PAD13 arriba-izquierda, como está serigrafiado. `PAD BANK`
  sube toda la superficie 16 notas.
- `<` y `>` mandan CC 25 y 26 y **no** cambian de banco, así que se pueden usar
  para pasar de página sin mover los pads.
- Los knobs son CC 30-37 absolutos; los botones del borde CC 25-29.

El mapa que usa el show vive en
`tools/qlctool/qlctool/generate/smc_pad_device.py`, y de ahí salen tanto los
bindings como el perfil de entrada de QLC+. La configuración del propio aparato
(notas, canal, colores por pad) se edita con **MidiSuite**, la aplicación del
fabricante, no desde el panel.
