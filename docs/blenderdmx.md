# BlenderDMX: the rig as a 3D previsualiser

QLC+ 5's own 3D view cannot show this show: no smoke plume, gobos as flat
textures, a four-head bar drawn as one light, the panels in Auto mode not drawn
at all ([rig.md](rig.md) measures each one). Since 2026-09-23 the visualiser is
[BlenderDMX](https://github.com/open-stage/blender-dmx), free and open, which
reads the industry's exchange formats: **GDTF** describes one fixture type
(geometry, wheels, DMX modes), **MVR** describes a rig (which fixture stands
where, patched to what). Neither exists for a QLC+ fixture, so `qlctool` writes
both from what this repo already has: the `.qxf` definitions and the positions
`qlctool stage` put in the workspace.

## The pipeline

```bash
cd tools/qlctool
.venv/bin/qlctool mvr "../../QLC+ Setups/Vibra-split.qxw"
# Wrote ../../QLC+ Setups/Vibra-split.mvr: 31 fixtures placed, 8 GDTF fixture types inside.
```

`--out` picks another file, `--gobos` another folder for the gobo images
(default: `Gobos/` next to the workspace). The package is committed, because
it is what the Mac mini consumes; it is regenerated whenever the patch, the
plot or a definition changes.

The importer is a headless Blender run on the machine that has the add-on:

```bash
Blender --background --python tools/blenderdmx/render_mvr.py -- \
    "QLC+ Setups/Vibra-split.mvr" vibra.png vibra.blend
```

It enables the add-on, imports the MVR, raises every fixture (dimmer up,
shutter open, one colour per fixture, movers spread across pan and tilt),
adds a floor, a camera and a smoke volume, renders one frame with Eevee and
saves the scene. The picture is a smoke test of the export, not a look: a
fixture facing the wrong way or a channel mapped to nothing shows in one
frame. The `.blend` is what you open with a window to walk around the rig.

## What the GDTF says about a QLC+ definition

One file per definition, `Manufacturer@Model@qlctool.gdtf`, schema-valid
against GDTF 1.2 (`tests/gdtf.xsd`, checked with `xmllint` for every
definition in the library by `tests/test_mvr_export.py`).

- **Geometry from `<Dimensions>` and the heads.** A static fixture is a box;
  a mover is base, yoke and head primitives (25/45/35 % of the height). One
  `Beam` geometry per head, laid out across the top from `<Layout>` or in one
  row, so an eight-pixel bar lights eight beams and a four-head bar four.
  Every fixture is modelled standing with the lenses pointing up. A smoke
  machine's "dimmer" is its pump: a box, no beam. No mesh files: the
  primitive is the model, and the model's `File` attribute must be empty,
  not `None`, or BlenderDMX fails to load it.
- **Attributes from roles**, never from channel names (`gdtf_attribute`):
  red/green/blue/white/amber/UV to `ColorAdd_*`, the wheels to `Color1` and
  `Gobo1`, strobe to `Shutter1`, and so on. A name GDTF's Annex B does not
  define is an error at export time.
- **A range is a function** (`channel_functions`). A shutter channel's
  closed, open, pulse and strobe ranges become separate functions under
  `Shutter1`, `Shutter1Strobe`, ..., each with its physical Hz from `Res1`
  and `Res2`; a wheel channel's slots become channel sets of one `Color1` or
  `Gobo1` function that indexes the wheel, its spin ranges a `WheelSpin`
  function after them. A preset-only strobe ("slow to fast" over the whole
  range) gets open at 0 and strobe from 1. The visualiser reads the attribute
  of the function the DMX value lands in, which is what makes a strobe strobe.
- **Fine channels fold into their coarse one** as a second offset, so 16-bit
  pan is one channel with two bytes, and the coarse-only fixtures are
  unchanged.
- **Wheels from the ranges**: a `ColorMacro` slot's colour comes from `Res1`
  as CIE xyY, a `GoboMacro` slot's image is found by file name under the gobo
  folder and packed into the archive. A shake range names the same gobo as
  the plain one, so slots are keyed by what they show.
- **Physical values** from `<Physical>` where QLC+ states them (pan and tilt
  travel, zoom degrees, lumens) and from GDTF's own conventions where it does
  not.

## Where a fixture stands

QLC+ draws with y up and z towards the audience, and stores a fixture by its
near corner in millimetres. MVR, GDTF and Blender put z up and y upstage, and
place a fixture by the origin of its model, the middle of its base. `mvr_matrix`
converts: the stage is centred on the origin, the fixture's centre is where
QLC+'s box centre was, and the rotation is `Rz(-y_rot) · Rx(a)` with

- `a = 180 - x_rot` for a fixture QLC+ draws with a mesh, which hangs and
  points at the floor at `x_rot = 0` while the GDTF stands and points up;
- `a = -x_rot` for a smoke machine and for the types QLC+ draws itself and
  lights from the top face (LED bars, strobes; `beam_landing.UPWARD_TYPES`).

The tests pin the consequences: a truss PAR at rest points down, a bar on the
floor points up, a MAC WASH standing beside the deck points up, and a positive
`x_rot` on a truss PAR leans it out over the audience. Hidden spares are left
out, as QLC+'s own views leave them out.

Fixture UUIDs derive from the fixture ID and the fixture type ID from
manufacturer and model, so a regenerated package updates what BlenderDMX has
instead of doubling it.

## Seeing it live from QLC+

Verified on the Mac mini on 2026-09-23 with QLC+ 5.2.2 and Blender on the
same machine: the console's *BLANCO TOTAL* held down lights the whole rig in
Blender, *ROJO* held down turns it red.

```bash
Blender ~/p/vibra-blender/vibra.blend --python tools/blenderdmx/live.py
```

`live.py` does what the saved file cannot carry: it enables Art-Net (BlenderDMX
resets `artnet_enabled` in its load handler, `linkFile` in `dmx.py`), and puts
every 3D view in Rendered shading through the camera, because a scene saved by
a `--background` run has no window and Blender opens it in its own Solid
layout. Leave the Art-Net address at `0.0.0.0`; a socket bound to one
interface's address does not receive broadcasts on macOS.

On the QLC+ side, the universe needs a second output next to the DMX USB one
(the engine allows several output patches per universe). The `.qxw` line is:

```xml
<Output Plugin="ArtNet" UID="" Line="0">
  <PluginParameters outputIP="192.168.1.255" outputUni="1" transmitMode="Full"/>
</Output>
```

- **`outputUni` is 1.** QLC+ universe 1 is Art-Net universe 0 by default
  (`outputUniverse` defaults to the universe index, `artnetcontroller.cpp`),
  while the MVR addresses are 1-based and BlenderDMX indexes its universe list
  with the Art-Net universe as it comes: the fixtures sit in `universes[1]`.
- **`Line` is the index into QLC+'s interface list, sorted by address**:
  `127.0.0.1` is 0 on the mini. `outputIP` overrides the line's broadcast
  address either way; the web page `/config` of a running QLC+ shows the list.
- **Send to the subnet broadcast, not to `127.0.0.1`, when both run on one
  machine.** Two sockets can share port 6454 only if both set `SO_REUSEPORT`
  (Qt does; BlenderDMX did not: `Address already in use`, patched in the
  checkout, commit `de60af6`, to be sent upstream). Once shared, a unicast to
  the machine's own address reached only one of the sockets, and never the
  visualiser; a listen-only third socket got nothing either. The broadcast
  reached every socket, measured at 295 frames in 3 s. From the show Mac to
  the mini, unicast to the mini's LAN address is fine: only one process there
  listens.

A running QLC+ with web access (`-w --wp 9998`, which the launcher uses) takes
the new workspace and the button presses without a restart, which is how the
test was driven: `curl -F "qlcprj=@file.qxw" http://127.0.0.1:9998/loadProject`
loads a workspace; on the websocket `/qlcplusWS`, `<widget id>|255` presses a
virtual console widget and `<widget id>|0` releases it;
`QLC+API|getChannelsValues|1|1|390` answers with `channel|value|type|0`
quadruples, the way to see what the console thinks it is sending.

Until QLC+ sends, the fixtures show whatever the last DMX was, which after a
load is nothing: the *Programmer* panel (select all with `A`, raise *Dimmer*,
pick a colour) lights them by hand.

## What no visualiser shows

The WX-60WPS panels in Auto mode (channel 7 an effect, RGB at 0) generate
their colour in the hardware; nothing downstream of the DMX can draw it.
That programme is still judged in the room.

## Traps, each one a lost iteration

- pygdtf writes `File="None"` on a model without a mesh; BlenderDMX reads a
  file called None and fails before its primitive fallback.
- The schema forbids `Default` on `DMXChannel` and requires it on every
  `ChannelFunction`; `ChannelSet`, slot and mode names must match the GDTF
  name pattern (`gdtf_name` sanitises them).
- A preset-only shutter opens at the exact `dmx_from` of its open set; one
  above is the strobe function.
- `dmx.artnet_enabled = True` starts a listener thread that keeps a
  `--background` Blender alive after the script returns; the render script
  saves and then `os._exit(0)`.
- Beams show as cones only inside a volume: `bpy.ops.dmx.create_volume()`
  and then `dmx.volume_density`.
