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
| Generic BEAM 230W 7R | **Not verifiable online.** Generic 7R lamps ship with different layouts: one manual found (Rambo 230) puts Color on ch1, Gobo on ch4, Pan on ch10, while our definition starts at Pan. Needs the on-site probe |
| Vortex PC-64 LED S | No manual found anywhere. 5ch RGB + dimmer + strobe is the usual LED PAR layout, order unconfirmed |
| LED Beam Mini | Declares 16ch with channels 9-16 "No function". Generic unit, nothing online. The wasted eight channels suggest a mode where they do something |

### Settling the unverified ones

`qlctool probe <show> <fixture-id> --base "7=255" --buttons` builds one scene per
DMX channel of that fixture plus a walk chaser: press play and write down what
each channel does. `--base` holds a dimmer open, since a head with a mechanical
shutter shows nothing otherwise.
