"""Where the suite finds a rig: its workspaces, stage plots, definitions and input profile.

This repository is the rig: the root, one folder up. QLCTOOL_TEST_RIG points
the suite at any other rig laid out the same way (ruling C1).
"""

import os
from pathlib import Path


def _default() -> Path:
    return Path(__file__).resolve().parents[1]


RIG_ROOT = (
    Path(os.environ["QLCTOOL_TEST_RIG"]) if os.environ.get("QLCTOOL_TEST_RIG") else _default()
)
