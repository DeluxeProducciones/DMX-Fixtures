"""The button tiles in `QLC+ Setups/Colores/` are what `tiles.toml` says (2026-09-26).

They replaced the 62 MB `Colores/Colors.psd` they were exported from; the
owner: "lo de los colores mira a ver si se puede hacer de otra manera".
"""

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "colour-tiles"
sys.path.insert(0, str(TOOL))

from tile_png import tile_png  # noqa: E402


def test_every_tile_regenerates_byte_for_byte():
    tiles = tomllib.loads((TOOL / "tiles.toml").read_text(encoding="utf-8"))["tiles"]
    assert len(tiles) == 50
    for name, pair in tiles.items():
        first, second = (tuple(int(c[i : i + 2], 16) for i in (1, 3, 5)) for c in pair)
        shipped = (ROOT / "QLC+ Setups" / "Colores" / f"{name}.png").read_bytes()
        assert tile_png(first, second) == shipped, name
