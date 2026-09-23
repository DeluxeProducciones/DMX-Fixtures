"""Import an MVR package into BlenderDMX without a window, light it, render it.

    Blender --background --python render_mvr.py -- rig.mvr out.png [out.blend]

The picture is a smoke test of the export, not a look: every fixture gets its
dimmer up, its shutter open, a colour by its place in the list, and the movers
a spread of pan and tilt, so a fixture facing the wrong way or a channel mapped
to nothing shows up in one frame. The DMX is written straight into BlenderDMX's
universe buffers, the way its Art-Net receiver would.
"""

import math
import os
import sys
from importlib import import_module

import bpy

ADDON = "bl_ext.user_default.open_stage_blender_dmx"
COLOURS = [(255, 0, 0), (0, 40, 255), (255, 0, 160), (0, 255, 255), (255, 120, 0), (0, 255, 0)]
STAGE = (12.0, 8.0)  # metres, x across and y deep, centred on the origin


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1 :]
    mvr, png = args[0], args[1]
    blend = args[2] if len(args) > 2 else None

    if ADDON not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module=ADDON)
    load_mvr = import_module(f"{ADDON}.mvr").load_mvr
    data = import_module(f"{ADDON}.data").DMX_Data

    dmx = bpy.context.scene.dmx
    dmx.new()
    load_mvr(
        dmx,
        mvr,
        import_focus_points=False,
        import_fixtures=True,
        import_trusses=True,
        import_scene_objects=True,
        import_projectors=False,
        import_supports=True,
        import_video_screens=False,
        use_high_mesh=False,
    )
    print("INFO FIXTURES", len(dmx.fixtures))
    for index, fixture in enumerate(dmx.fixtures):
        light(fixture, index, data)
    dmx.render()
    for fixture in dmx.fixtures:
        fixture.render(skip_cache=True)

    dress_the_room()
    try:
        bpy.ops.dmx.create_volume()
        dmx.volume_density = 0.08
        print("INFO volume created")
    except Exception as error:
        print("INFO no volume:", error)
    try:
        # Saved into the .blend, so the file opens listening for the show.
        dmx.artnet_enabled = True
        print("INFO Art-Net enabled")
    except Exception as error:
        print("INFO no Art-Net:", error)

    render(png)
    if blend:
        bpy.ops.wm.save_as_mainfile(filepath=blend)
    print("INFO DONE", png)
    sys.stdout.flush()
    # The Art-Net listener is a thread Blender waits for on exit; the picture
    # and the file are on disk, so leave without waiting.
    os._exit(0)


def light(fixture, index: int, data) -> None:
    red, green, blue = COLOURS[index % len(COLOURS)]
    breaks = {b.dmx_break: b for b in fixture.dmx_breaks}
    first = next(iter(breaks.values()), None)
    if first is None:
        return
    for channel in fixture.channels:
        dmx_break = breaks.get(channel.dmx_break, first)
        offset = channel.offsets[0]
        if offset <= 0:
            continue
        address = dmx_break.address + offset - 1
        value = value_for(channel, index, red, green, blue)
        if value is None:
            continue
        universe = dmx_break.universe
        while len(data._universes) <= universe:
            data._universes.append(bytearray(512))
        if 1 <= address <= 512:
            data._universes[universe][address - 1] = max(0, min(255, int(value)))
    print(
        "INFO lit", fixture.name, [(c.attribute, list(c.offsets)[:2]) for c in fixture.channels][:6]
    )


def value_for(channel, index: int, red: int, green: int, blue: int):
    attribute = channel.attribute
    if attribute == "Dimmer":
        return 255
    if attribute == "ColorAdd_R":
        return red
    if attribute == "ColorAdd_G":
        return green
    if attribute == "ColorAdd_B":
        return blue
    if attribute == "ColorAdd_W":
        return 0
    if attribute == "Shutter1":
        return shutter_open(channel)
    if attribute == "Pan":
        return 128 + ((index % 5) - 2) * 18
    if attribute == "Tilt":
        return 128 + 28
    if attribute in ("Zoom", "Focus1"):
        return 128
    if attribute in ("Gobo1", "Color1"):
        return 0
    return None


def shutter_open(channel) -> int:
    """The lowest DMX value at which this shutter is plainly open, not strobing."""
    for function in channel.channel_functions:
        if function.attribute != "Shutter1" or function.physical_to <= 0:
            continue
        sets = [s for s in function.channel_sets if s.physical_to > 0]
        return sets[0].dmx_from if sets else function.dmx_from
    return 255


def dress_the_room() -> None:
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.scale = (STAGE[0] + 4, STAGE[1] + 6, 1)
    material = bpy.data.materials.new("Floor")
    material.diffuse_color = (0.08, 0.08, 0.09, 1)
    floor.data.materials.append(material)

    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 24
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (0.0, -STAGE[1] / 2 - 7.0, 4.2)
    camera.rotation_euler = (math.radians(74), 0.0, 0.0)
    bpy.context.scene.camera = camera


def render(png: str) -> None:
    scene = bpy.context.scene
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    print("INFO engine", scene.render.engine)
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = png
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 32
    bpy.ops.render.render(write_still=True)


main()
