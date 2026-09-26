"""The pad palette that ships next to a show is the palette of that show.

The pad's LEDs and the console's buttons wear one palette, or they lie. Until
2026-09-26 the LED bridge carried Vibra's colours as Swift arrays and this test
compared them with the generator's pad by pad. The bridge now lives in
https://github.com/spectalive/smc-pad and reads `Vibra.pads.json`, which
`qlctool pad-palette` writes from the same bindings and colours the console is
painted with. So the one thing left to prove is that the shipped file is what
the pinned toolkit writes from the shipped workspace, byte for byte - the way
the tablet's map is pinned in `test_shipped_deskmap.py`.
"""

import argparse
import json

import pytest
from qlctool.cmd_pad_palette import cmd_pad_palette
from rig_root import RIG_ROOT

SETUPS = RIG_ROOT / "QLC+ Setups"
SHIPPED = sorted(SETUPS.glob("*.pads.json"))


def test_at_least_one_palette_ships():
    assert SHIPPED


@pytest.mark.parametrize("path", SHIPPED, ids=lambda p: p.name)
def test_the_shipped_palette_is_rewritten_byte_for_byte_from_its_workspace(path, tmp_path):
    shipped = json.loads(path.read_text(encoding="utf-8"))
    workspace_path = SETUPS / shipped["show"]["workspace"]
    rewritten = tmp_path / path.name
    cmd_pad_palette(argparse.Namespace(workspace=str(workspace_path), out=str(rewritten)))
    fresh = json.loads(rewritten.read_text(encoding="utf-8"))
    assert shipped["show"]["sha256"] == fresh["show"]["sha256"], (
        f"{path.name} was written from another {workspace_path.name}; "
        f"run `qlctool pad-palette --out '{path}' '{workspace_path}'`"
    )
    assert path.read_bytes() == rewritten.read_bytes()


# Only Vibra.qxw's palette ships, but the show Mac runs Vibra-split.qxw and the
# beats variant exists too: the pad must light the same way whichever of the
# three is loaded (review of the smc-pad split, 2026-09-26). Widget ids differ
# between the variants and the bridge never reads them: it paints by note.
@pytest.mark.parametrize("variant", ["Vibra-split.qxw", "Vibra-beats.qxw"])
def test_every_vibra_variant_lights_the_pad_like_the_shipped_palette(variant, tmp_path):
    shipped = json.loads((SETUPS / "Vibra.pads.json").read_text(encoding="utf-8"))
    rewritten = tmp_path / "variant.pads.json"
    cmd_pad_palette(argparse.Namespace(workspace=str(SETUPS / variant), out=str(rewritten)))
    fresh = json.loads(rewritten.read_text(encoding="utf-8"))
    painted = ("note", "control", "lit", "active", "idle")
    assert [{k: pad[k] for k in painted} for pad in fresh["pads"]] == [
        {k: pad[k] for k in painted} for pad in shipped["pads"]
    ]
