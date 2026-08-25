# The rig

27 patched fixtures on **one universe**, DMX addresses 1-300 contiguous, zero
overlaps (verified by `qlctool patch`, which is a test). Output is the QLC+
**DMX USB** plugin with `UID="None"`, so it binds to whatever USB-DMX interface
is connected.

A naive scan reporting "369 fixtures" is wrong: 342 of those are fixture-ID
*references* inside scenes and groups.

| Qty | Fixture | Mode | ch | Moves |
| --- | --- | --- | --- | --- |
| 4 | Pro-Lights CromoWash100 | Advanced | 12 | yes |
| 2 | Stairville LED Bar 240/8 RGB | - | 24 | no |
| 2 | Stairville CLB2.4 PAR | - | 14 | no |
| 7 | Vortex PC-64 LED S | Default | 5 | no |
| 2 | Chauvet MiN Wash | 13 Channel | 13 | yes |
| 2 | LED Beam Mini Moving Head | 16 Channels | 16 | yes |
| 4 | Generic BEAM 230W 7R | 16 channel | 16 | yes |
| 2 | HYULIGHTS WX-60WPS-48PARTITION | A MODE 8CH | 8 | no |
| 1 | Stairville AF-150 (fog) | Generic Smoke / Amount | 1 | - |
| 1 | Generic Smoke | Normal | 2 | - |

**Twelve fixtures move**, not six: the CromoWash100 and the MiN Wash are moving
washes. Selecting movers by capability (a fixture with both pan and tilt)
returns exactly the twelve the hand-built "Movimiento Circulo" EFX drives, which
is the check the toolkit uses instead of a hardcoded list.

The rig has **not** been confirmed against the physical hardware. That check is
an on-site job.

## Where they stand

Neither has the *plot* - nobody has measured the venue. `qlctool stage` writes
a generated starting layout into `<Monitor>` on a 12 x 6 x 8 m stage: beams
upstage on the truss, washes downstage on the truss, the two LED bars on the
floor at the back, PARs and blinders at the front, smoke in the back corners.
It exists so the 2D and 3D views are readable at all - before it, the show
carried positions for four fixtures out of twenty-seven and drew the other
twenty-three on top of each other. Drag them where they really are in QLC+ and
save; the toolkit only rewrites the node when `stage` or `newshow` is run.

## Fixture groups

| ID | Name | Grid | Fixtures |
| --- | --- | --- | --- |
| 0 | BarrasLed | 8x2 | 2, 3, 20, 21, 22, 23, 24, 25 |
| 1 | Cabezas | 8x1 | 0, 1, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23 |
| 2 | PAR | 3x3 | 6-12 |

Groups are what an RGBMatrix paints onto, and what the colour banks are built
per.

## Smoke machines

Two, and they are handled apart from everything else: every generator skips
fixtures whose definition says `<Type>Smoke</Type>`, because a pump caught in an
"all dimmers to full" scene runs until the tank is empty. Only the smoke
generator drives them - a burst, then a long wait, on a loop.

## Fixture definitions

Seven custom `.qxf` in `QLC+ Fixtures/`, plus the QLC+ system library. QLC+ 5
ships `Pro-Lights-CromoWash100.qxf` itself, which is why that one fixture
resolves even when the custom definitions are not installed.

### Verification status

| Fixture | Status |
| --- | --- |
| Pro-Lights CromoWash100 | Verified against the repo manual (Basic 9ch, Advanced 12ch) |
| Audibax IOWA70 | Verified against the repo manual; orphan, not patched |
| Chauvet MiN Wash | **Verified online** (2026-08-24): the manufacturer manual's 13-channel mode matches channels 1-10 - Pan, Pan fine, Tilt, Tilt fine, Vector speed, Dimmer/Strobe, R, G, B, Color Macros - which is everything the toolkit drives. The manual edition found calls 11-13 "Reserved" where the definition says "Vector Speed (Color)" and "Movement Macros"; unused either way. **Its `5 Channel` mode is wrong** - it lists no Tilt - but the patch does not use it |
| HYULIGHTS WX-60WPS | Definition declares 10 channels, the used mode exposes 8, matching the patch. Not otherwise verified |
| Generic BEAM 230W 7R | **Verified on the hardware by the owner**, who states he tested the channel order when he wrote the definition (2026-08-25). The hand-built show corroborates the two channels that matter most: `Luz ON Cabezas` sends 255 to channel 6 and 255 to channel 7, `Luz OFF Cabezas` sends 0 to both - so channel 6 is the shutter, shut at 0, and channel 7 is the dimmer. No manual matches it (one found for a Rambo 230 puts Color on ch1 and Pan on ch10), so the hardware is the only reference there will be. Physical side: see [Where the beams came from](#where-the-beams-came-from) |
| Vortex PC-64 LED S | No manual found anywhere. 5ch RGB + dimmer + strobe is the usual LED PAR layout, order unconfirmed |
| LED Beam Mini | Declares 16ch with channels 9-16 "No function". Generic unit, nothing online. The wasted eight channels suggest a mode where they do something |

### Where the beams came from

The four beams were bought on AliExpress on **2024-08-20**, order
`3040202209874050`, four units for **1.070,34 €** (~267 € each). The listing is
`Haz de luz de escenario 7R ... 1PCS 230W 7R Beam`, and it has since been
delisted; its product image survives at
`https://ae01.alicdn.com/kf/S213c94a06db2438db482281ea8adc4089.jpg` and shows a
full-size Sharpy clone with the **8+16+24 prism**. The order mail is the only
record - AliExpress order mails link to the order page, never to the product, so
there is no item ID to go back to.

That image plus our own definition (17 gobos + open, 14 colours + open, pan 540,
tilt 270, 16 channels) matches the **ERA Lighting 230W 7R Sharpy Beam** spec
exactly, which is where the body dimensions now come from: **330 x 390 x 490 mm**,
mapped into the definition as `Width="390" Height="490" Depth="330"` (the tall
axis is the one that matters - QLC+ scales the 3D mesh to these numbers).

What was there before was `Height="40"`, which drew the four beams as flat
slivers in the 2D and 3D views. Sources that agree on the body shape for this
class: 350 x 320 x 505 mm / 20.1 kg, 410 x 290 x 510 mm / 15.7 kg, and beamZ's
lighter Tiger 7RC at 280 x 240 x 470 mm / 11.5 kg. Width and depth are within
60 mm of each other across all of them and are invisible at this scale; the
height is not.

### What the beam definition had wrong

The channel *order* is still only as good as the seller's chart, but everything
around it has been corrected against QLC+'s own schema and its Clay Paky Sharpy
definition, which is the same class of fixture:

- **`Height="40"`** in the physical block drew the four beams as flat slivers in
  the 2D and 3D views. Now 390 x 490 x 330 mm - see above.
- **The maintenance channel was machine-translated.** "Quench" is the lamp being
  put out and "Bubble" is it being struck: 100-105 is **lamp off**, 106-205 is
  lamp on, 206-255 is reset. Nothing on the console said that sending 100 to
  channel 16 kills a 230 W lamp mid-show. They now carry QLC+'s `LampOff`,
  `LampOn` and `ResetAll` presets and say so in words.
- **The gobo thumbnails pointed at `~/Desktop/Gobos/`**, a folder that no longer
  exists on either machine. The images live in
  `QLC+ Setups/Gobos/BEAM-LIGHT-230W-7R/`; the definition now names them
  relatively (`BEAM-230W-7R/Gobo1.png`), which QLC+ resolves against its own
  Gobos folder - see [qlcplus-environment.md](qlcplus-environment.md).
- **Presets that did not match their own labels**: prism rotation was
  `RotationIndexed` ("park at an angle") on a range labelled "forward slow to
  fast", the shutter's open and closed ranges carried no preset, and the gobo
  wheel's two rainbow ranges were unmarked where the colour wheel's were not.
- **`Res1="0"` on the prism** - that field is the facet count, and the unit has
  an 8-facet prism.
- **Lamp figures**: the Osram Sirius HRI 230W datasheet gives 9500 lm at 8000 K,
  not the 23000 lm / 8500 K that was there. Beam angle follows QLC+'s Sharpy:
  a fixed 3.8 degrees, not a 0-5 degree PC lens. `PowerConsumption` stays at the
  lamp's 230 W, which is the convention QLC+'s own definitions use.
- **"Invalid"** as a capability name became "No function", QLC+'s own word.

One thing deliberately *not* changed: **Prism Rotation stays in the `Speed`
group**, where QLC+'s Sharpy would put it in `Prism`. The toolkit resolves roles
from the channel group, and a second Prism-group channel with more labelled
ranges than the prism itself would capture the prism role and make
"Prisma Animacion" drive rotation instead of insertion.

The Vortex PC-64 also carried `Weight="0"`, which QLC+'s schema rejects; it is
now 3 kg, an estimate for a LED PAR of that size and used for nothing but the
fixture list.

### A dimmer at full is not a light that is on

The four beams have a **mechanical shutter on channel 6, shut at DMX 0**, and
the two MiN Wash keep their whole intensity on a shutter-style channel with no
separate dimmer at all. Raising the dimmer does nothing for either. The
hand-built show knew it - `Luz ON Cabezas` sends 255 to the beams' channel 6 and
`Luz OFF Cabezas` sends 0 - and the generators did not, so every generated
colour, gobo and dimmer scene left six of the twelve heads dark.

It stayed invisible because QLC+ could not tell either: the definition's
"Closed" range carried no preset, so the 3D view drew light the rig would never
have produced. Tagging it `ShutterClose` made the preview honest, and the
darkness it then showed was real.

`shutter_open_pairs` reads the open value out of the definition - the range
marked `ShutterOpen`, or failing that one named "open" - and every generator that
raises a dimmer to make a fixture visible now opens its shutter too. Fixtures
whose shutter channel is a strobe and nothing else, which is every LED PAR here,
are left alone.

### Settling the unverified ones

`qlctool probe <show> <fixture-id> --base "7=255" --buttons` builds one scene per
DMX channel of that fixture plus a walk chaser: press play and write down what
each channel does. `--base` holds a dimmer open, since a head with a mechanical
shutter shows nothing otherwise.
