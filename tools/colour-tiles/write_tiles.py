#!/usr/bin/env python3
"""Write every tile in `tiles.toml` to `QLC+ Setups/Colores/<name>.png`.

The tiles are button backgrounds of the older DeluxeEventos workspaces. This
replaces the 62 MB `Colores/Colors.psd` they were exported from: to change a
colour, edit `tiles.toml` and run this again from the repository root.
"""

import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tile_png import tile_png  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "QLC+ Setups" / "Colores"


def main() -> None:
    tiles = tomllib.loads((HERE / "tiles.toml").read_text(encoding="utf-8"))["tiles"]
    for name, (first, second) in tiles.items():
        colours = [tuple(int(hex_colour[i : i + 2], 16) for i in (1, 3, 5)) for hex_colour in (first, second)]
        (OUT / f"{name}.png").write_bytes(tile_png(colours[0], colours[1]))
    print(f"wrote {len(tiles)} tiles to {OUT}")


if __name__ == "__main__":
    main()
