"""Open the saved rig with a window, listening to the console over Art-Net.

    Blender vibra.blend --python live.py

Two things the saved file cannot carry: BlenderDMX resets `artnet_enabled` in
its load handler, and a scene saved by a `--background` run has no window, so
the window Blender opens is its own startup layout in Solid shading, not the
Rendered-through-the-camera view the render script saved. This puts both back
once the file is loaded, and says on stdout whether the Art-Net socket bound.
"""

import bpy


def go_live() -> None:
    dmx = bpy.context.scene.dmx
    for universe in dmx.universes:
        universe.input = "ARTNET"
    dmx.artnet_enabled = True
    print("INFO artnet", dmx.artnet_enabled, dmx.artnet_status)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for space in area.spaces:
                if space.type != "VIEW_3D":
                    continue
                space.shading.type = "RENDERED"
                space.region_3d.view_perspective = "CAMERA"
                space.overlay.show_overlays = False
    print("INFO live view ready")


# The file is loaded before `--python` runs, but the load handler that resets
# Art-Net runs from a timer after that: wait one tick so this comes last.
bpy.app.timers.register(go_live, first_interval=1.0)
