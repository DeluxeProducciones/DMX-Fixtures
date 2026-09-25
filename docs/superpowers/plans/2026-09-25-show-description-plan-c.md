# Show Description, Plan C: a second example rig, and qlctool as its own repository

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the description is enough by generating, checking and
validating a show for a second rig that shares nothing with Vibra's patch and
has no controllers, then move `tools/qlctool` and the toolkit docs, with their
history, to the public repository `spectalive/qlctool`, tag `v0.1.0`, and make
this repository depend on that tag.

**Architecture:** Four tasks in this repository and three around the
extraction. The suite first stops assuming it lives three folders below a rig
(`tests/rig_root.py`); `newshow` learns to build on a rig without gobos, prism
or haze machines; one checker false positive that such a rig exposes is fixed
under a dated regression test; the small-club example is added under
`tools/qlctool/examples/`. Then a fresh clone is cut down with `git filter-repo`
to the toolkit's paths, given a frozen copy of the rig data its tests read,
verified, published with `gh repo create spectalive/qlctool --public`, and
tagged; finally `vibra-lighting` removes `tools/qlctool`, installs the tag
through a git URL, and keeps its own byte-identity check against it.

**Tech Stack:** Python >= 3.11, the toolkit as it stands after Plan B, pytest +
pytest-xdist, headless QLC+ 5.2.2, `git filter-repo` a40bce548d2c
(`/opt/homebrew/bin/git-filter-repo`), `gh` logged in as `CristianDeluxe` with
`repo` and `read:org` scopes, `uv` for the moved CI workflow.

**Spec:** `docs/superpowers/specs/2026-09-24-show-description-design.md`
(binding), "Order" steps 7 and 8. **Depends on Plan B**
(`docs/superpowers/plans/2026-09-25-show-description-plan-b.md`): the example
is English, which needs Plan B's catalogue-driven generator, and its fixtures
are found through Plan B's `[rig] fixtures`. Do not start Task 1 before Plan
B's Task 12 is pushed.

---

## Global Constraints

Read these before every task. A task that breaks one is not done.

1. **Byte identity, in both repositories.** `Vibra.qxw`, `Vibra-beats.qxw`,
   `Vibra-split.qxw` regenerate byte-identical to
   `tests/vibra_baseline.json` after every task, and `Vibra.desk.json` stays
   byte-identical (`test_shipped_deskmap.py`). After Task 5 the toolkit repo
   checks this against its frozen copy of the rig; after Task 7 vibra-lighting
   checks it against the pinned `v0.1.0`. A changed byte is a failed task.
2. **Gates in this repository (Tasks 1-4)**, from
   `/Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool`:
   ```bash
   .venv/bin/python -m pytest tests/ -q
   .venv/bin/python tests/vibra_compare.py --validate
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-beats.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
   ```
   The suite runs in the foreground and is **never piped through `tail` or
   `head`** (the exit code is lost, and a stopped suite leaves a headless QLC+
   behind that makes later validation pass). After Plan B, QLC+ 5.2.2 is found
   without `QLCTOOL_QLCPLUS` and no test skips; if one skips, say so and why.
   Each `check` prints `522 botones revisados, ningun problema`.
   `vibra_compare.py --validate` prints three `identical, 0 finding(s), QLC+
   loaded it` lines. Record the suite's pass count at the start of Task 1 as
   this plan's baseline; every later count is that plus the tests the plan adds.
   Gates in the new repository (Task 5-6) and in vibra-lighting after the
   extraction (Task 7) are spelled out in those tasks.
3. **One exported unit and one responsibility per file**; new files under 150
   lines, test files under 300 (`tests/test_check.py` is already over and the
   repo's rule puts regression tests there: add to it, do not split it in this
   plan). `ruff check` and `ruff format --check` on touched `.py` files.
4. **No new runtime dependency.**
5. **Checks reason about capabilities and the function graph, never a
   function's display name.**
6. **A malfunction needs a check before its fix** (`CLAUDE.md`): rule,
   dated regression test in `tests/test_check.py`, gate over every shipped
   workspace, then the generator fix.
7. **Commits.** English, conventional, stage only the task's paths, no AI
   attribution and no `Claude-Session:` or co-author trailer (owner,
   2026-09-25), using the existing git identity (`Cristian Deluxe <me@cristiandeluxe.dev>`).
   This repository: commit on `main` and push after Tasks 4 and 7. The new
   repository: its own `main`, pushed in Task 6.
8. **Destructive steps name their target and what protects it.** Task 5 works
   only in a fresh clone at `/Users/cristiandeluxe/p/qlctool`, never in
   `/Users/cristiandeluxe/p/DMX-Fixtures`; `git filter-repo` refuses a
   non-fresh clone and must not be forced. Task 7 deletes `tools/qlctool` from
   this repository only after the tag exists and installs, and after checking
   `git status --ignored tools/qlctool` for anything not in git (the venv and
   caches are expected; anything else is copied out first).
9. **External writes.** `gh repo create spectalive/qlctool --public`, the push
   and the tag are authorised by the owner (2026-09-25) for exactly that
   repository. Nothing else on GitHub is created or changed by this plan.

**Rulings this plan makes where the spec is silent or ambiguous:**

- C1. *The suite reads its rig through one module.* `tests/rig_root.py`
  exports `RIG_ROOT`: `QLCTOOL_TEST_RIG` if set, else `tests/data/rig` if it
  exists (the extracted toolkit), else the repository root (vibra-lighting
  before the extraction). `tests/conftest.py` sets `QLCTOOL_FIXTURES` to the
  rig's `QLC+ Fixtures` when unset, so `FixtureLibrary.load()` finds the
  definitions wherever pytest is started.
- C2. *A rig without a wheel, a prism or a haze machine still gets a show.*
  `newshow` skips the gobo, beam-colour-wheel and prism generators when no
  patched fixture has the role, and the haze timer when there is no fog-only
  machine; the members that would have come from them drop out of AUTO, the
  levels and the moments. `generate_wheel_scenes` itself still raises on a
  missing role (`test_a_missing_wheel_is_an_error_not_an_empty_chaser`): the
  guard is at the call site.
- C3. *A chaser whose every step is a level Collection is a structural
  cycle*, even when it only writes one family. The small club's energy cycle
  moves only position (its pars have no pan/tilt, its dimmer levels live in
  Collections under the steps), and the family-owner rule mistook it for the
  position family's owner. Fixed in the checker, because the show is right.
- C4. *The example lives in the toolkit*, at `tools/qlctool/examples/small-club/`
  (moving with the extraction to `examples/small-club/`): its three fixture
  definitions copied from `QLC+ Fixtures/`, the patch, an English `show.toml`
  with `[rig] fixtures = ["fixtures"]` and no `[controllers]`, and the
  generated `club.qxw`, held byte-identical by a test.
- C5. *What moves to `spectalive/qlctool`:* `tools/qlctool/**` (package,
  tests, `tools/qlctool/docs/`, `README.md`, `TODO.md`, `pyproject.toml`,
  `uv.lock`, quality configuration), the toolkit docs `docs/toolkit.md`,
  `docs/checks.md`, `docs/qxw-format.md`, `docs/qlcplus-environment.md`,
  `docs/qlc5-verification.md`, the workflow
  `.github/workflows/quality-qlctool.yml` (renamed `quality.yml`), and
  `LICENSE`, `LICENSE-CC-BY-4.0`, `NOTICE`. What stays in vibra-lighting:
  everything else - the rig (`QLC+ Setups/`, `QLC+ Fixtures/`,
  `QLC+ InputProfiles/`), the show docs, `Manual/`, `Colores/`, and the other
  tools (`smc-pad`, `qlc-launcher`, `blenderdmx`, `daslight`, `lightkey`),
  which the spec leaves to their own designs.
- C6. *Byte identity lives in both.* The toolkit keeps
  `vibra_baseline.json`, `vibra_regen.py`, `vibra_compare.py`,
  `test_vibra_byte_identity.py` and `test_shipped_deskmap.py` against a frozen
  copy of the rig in `tests/data/rig` (a regression net for the toolkit's own
  changes). vibra-lighting keeps its own copies of those five plus
  `test_input_profile.py`, `test_definition_schema.py` and
  `test_pad_palette.py` in a root `tests/`, run against the installed tag (the
  guarantee the show needs: the pinned release still builds this show).
  `test_pad_palette.py` leaves the toolkit: it reads
  `tools/smc-pad/qlc_led_bridge.swift`.
- C7. *vibra-lighting installs the toolkit from a root `requirements.txt`*
  (`qlctool[dev] @ git+https://github.com/spectalive/qlctool.git@v0.1.0`) into
  a root `.venv`; a root `pytest.ini` runs `tests/`. Commands that were
  `cd tools/qlctool && .venv/bin/qlctool ... "../../QLC+ Setups/..."` become
  `.venv/bin/qlctool ... "QLC+ Setups/..."` from the repository root.
- C8. *History is not rewritten beyond the path filter.* Commit authors keep
  their addresses (`info@busirocket.com`, `me@cristiandeluxe.dev`); both are
  already public in `Vibra-Lab/vibra-lighting`, which is a public repository
  (`gh api repos/Vibra-Lab/vibra-lighting --jq .private` prints `false`).
- C9. *Licences travel as they are.* The toolkit's code is Apache-2.0 and its
  docs keep CC BY 4.0 (vibra-lighting's README licence section, carried into
  the toolkit's README); `NOTICE` is reworded for the toolkit (vendored QLC+
  schema and system definitions now at `qlctool/library/`).
- C10. *`[show] language` still defaults to `"es"` in `v0.1.0`* (Plan B's
  B11). The example states `language = "en"`. Changing the default is a
  behaviour change for every existing description and is left to the owner.

---

## File map

This repository, Tasks 1-4 (relative to `tools/qlctool` unless absolute):

```
tests/rig_root.py                               Task 1  RIG_ROOT
tests/conftest.py                               Task 1  QLCTOOL_FIXTURES default
tests/*.py (54 files)                           Task 1  parents[3] -> RIG_ROOT
qlctool/generate/haze_machines.py               Task 2  fog-only machines
qlctool/generate/rig_has_role.py                Task 2  any patched fixture with a role
qlctool/generate/canonical_show.py              Task 2  guards and optional members
qlctool/generate/smoke_auto.py                  Task 2  uses haze_machines
tests/data/empty-workspace.qxw                  Task 2  a workspace with no patch
tests/small_rig.py                              Task 2  builds the small-club patch
tests/test_small_rig.py                         Task 2
qlctool/checks/steps_are_levels.py              Task 3
qlctool/checks/family_frames.py                 Task 3
tests/test_check.py                             Task 3  dated regression
examples/small-club/                            Task 4  fixtures/, club-patch.qxw, show.toml, club.qxw
tests/test_small_club_example.py                Task 4
```

New repository `/Users/cristiandeluxe/p/qlctool` (Tasks 5-6): the filtered
history plus `tests/data/rig/`, `tests/rig_root.py` (no repo-root fallback),
README, NOTICE, `pyproject.toml` description, `.github/workflows/quality.yml`.

This repository, Task 7: delete `tools/qlctool/` and the five moved docs;
create `requirements.txt`, `pytest.ini`, `tests/` (eight files moved from the
toolkit's suite plus `rig_root.py`, `conftest.py`, `vibra_regen.py`,
`vibra_compare.py`, `vibra_baseline.json`); edit `.gitignore`, `AGENTS.md`,
`CLAUDE.md`, `README.md`, `NOTICE`, `docs/README.md`, the docs that link the
moved ones, `QLC+ Setups/vibra*.toml` (their "Regenerate:" comment line),
`QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi` is NOT edited (generated; see Task 7),
`tools/smc-pad/README.md`, `tools/smc-pad/qlc_led_bridge.swift` (comment
paths), `TODO.md`, `TODO_LOG.md`; delete `.github/workflows/quality-qlctool.yml`.

---

### Task 1: The suite finds its rig through one module

**Files:**
- Create: `tests/rig_root.py`, `tests/conftest.py`
- Modify: the 54 files under `tests/` that contain
  `Path(__file__).resolve().parents[3]` (`grep -l "parents\[3\]" tests/*.py`)

**Interfaces:**
- Produces: `RIG_ROOT: Path` (importable as `from rig_root import RIG_ROOT`,
  the way `tests/test_vibra_byte_identity.py` imports `vibra_regen`).

- [ ] **Step 1: Record the baseline**

Run: `.venv/bin/python -m pytest tests/ -q`
Write the pass count down (Plan B's final count). No test may skip.

- [ ] **Step 2: Write the module and the conftest**

`tests/rig_root.py`:

```python
"""Where the suite finds a rig: its workspaces, stage plots, definitions and input profile.

In vibra-lighting the rig is the repository itself, three folders up. In the
extracted toolkit it is the frozen copy in tests/data/rig. QLCTOOL_TEST_RIG
points the suite at any other rig laid out the same way (ruling C1).
"""

import os
from pathlib import Path


def _default() -> Path:
    here = Path(__file__).resolve().parent
    frozen = here / "data" / "rig"
    return frozen if frozen.is_dir() else here.parents[2]


RIG_ROOT = Path(os.environ["QLCTOOL_TEST_RIG"]) if os.environ.get("QLCTOOL_TEST_RIG") else _default()
```

`tests/conftest.py`:

```python
"""Suite-wide set-up: the fixture library reads the test rig's definitions.

`FixtureLibrary.load()` resolves its folders from QLCTOOL_FIXTURES or the
nearest qlctool.toml above the current directory; pytest can be started from
anywhere, so the suite names the rig's folder explicitly unless the caller did.
"""

import os

from rig_root import RIG_ROOT

os.environ.setdefault("QLCTOOL_FIXTURES", str(RIG_ROOT / "QLC+ Fixtures"))
```

- [ ] **Step 3: Replace the 54 expressions**

Run this once from `tools/qlctool` (it edits only the matching files; review
the diff afterwards):

```bash
.venv/bin/python - <<'PY'
import re
from pathlib import Path

for path in sorted(Path("tests").glob("*.py")):
    text = path.read_text(encoding="utf-8")
    if "Path(__file__).resolve().parents[3]" not in text:
        continue
    text = text.replace("Path(__file__).resolve().parents[3]", "RIG_ROOT")
    lines = text.splitlines(keepends=True)
    last_import = max(
        i for i, line in enumerate(lines) if re.match(r"(from \S+ import |import )", line)
    )
    lines.insert(last_import + 1, "from rig_root import RIG_ROOT\n")
    path.write_text("".join(lines), encoding="utf-8")
    print(path)
PY
.venv/bin/ruff check --fix --select I tests/
.venv/bin/ruff format tests/
```

(`ruff` may live at `/opt/homebrew/bin/ruff` if the venv has none.) Then
remove `from pathlib import Path` where the file no longer uses `Path`
(`ruff check tests/ --select F401` lists them). A multi-line import block whose
last line is a `)` gets the new import after the `)`: check the files the
script printed with `git diff --stat` and read any whose import block looks
wrong.

- [ ] **Step 4: Prove nothing reads the old way, and that the variable works**

```bash
grep -rn "parents\[3\]" tests/ ; echo "exit $?"
```

Expected: `exit 1` (no match).

```bash
.venv/bin/python -m pytest tests/ -q
QLCTOOL_TEST_RIG=/Users/cristiandeluxe/p/DMX-Fixtures .venv/bin/python -m pytest tests/test_vibra_byte_identity.py tests/test_shipped_deskmap.py -q
```

Expected: the Step 1 count, then both files pass.

- [ ] **Step 5: Gates, commit**

Five gates; commit:

```text
test(qlctool): the suite reads its rig through tests/rig_root.py

Fifty-four test files computed the repository root as parents[3]; they
now import RIG_ROOT, which the extracted toolkit points at a frozen copy
of the rig, and conftest names the rig's definitions for the library.
```

---

### Task 2: `newshow` builds on a rig with no gobo, prism or haze machine

**Files:**
- Create: `qlctool/generate/haze_machines.py`, `qlctool/generate/rig_has_role.py`,
  `tests/data/empty-workspace.qxw`, `tests/small_rig.py`, `tests/test_small_rig.py`
- Modify: `qlctool/generate/canonical_show.py`, `qlctool/generate/smoke_auto.py`

**Interfaces:**
- Consumes: `FixtureCapabilities.is_smoke`, `.has_role(role)`, `roles.RED`,
  `roles.GOBO`, `roles.PRISM`, `GeneratedWheel(scene_ids, chaser_id)`,
  `qlctool.cli.main`.
- Produces:
  - `haze_machines(capabilities: Iterable[FixtureCapabilities]) -> list[FixtureCapabilities]`
  - `rig_has_role(capabilities: Iterable[FixtureCapabilities], role: str) -> bool`
  - `tests/small_rig.py`: `build_small_rig_patch(folder: Path) -> Path` - writes
    `club-patch.qxw` into `folder` and returns its path. Task 3 and Task 4
    use it.

- [ ] **Step 1: The test rig and the failing test**

`tests/data/empty-workspace.qxw` (verbatim; a QLC+ 5.2.2 workspace with one
empty universe and an empty console):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Workspace>
<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VC">
  <Creator>
    <Name>Q Light Controller Plus</Name>
    <Version>5.2.2</Version>
    <Author>qlctool</Author>
  </Creator>
  <Engine>
    <InputOutputMap>
      <BeatGenerator BeatType="Internal" BPM="120"/>
      <Universe Name="Universe 1" ID="0"/>
    </InputOutputMap>
  </Engine>
  <VirtualConsole>
    <Frame Caption="">
      <Appearance>
        <FrameStyle>None</FrameStyle>
        <ForegroundColor>Default</ForegroundColor>
        <BackgroundColor>Default</BackgroundColor>
        <BackgroundImage>None</BackgroundImage>
        <Font>Default</Font>
      </Appearance>
    </Frame>
    <Properties>
      <Size Width="1440" Height="900"/>
      <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>
    </Properties>
  </VirtualConsole>
  <SimpleDesk>
    <Engine/>
  </SimpleDesk>
</Workspace>
```

`tests/small_rig.py`:

```python
"""A small club, patched through the CLI: nothing in it is Vibra's.

Six Vortex PC-64 RGB pars, two LED Beam moving heads with no gobo or prism
wheel, two Chauvet MiN Wash - no haze machine, no controllers. Two groups:
the pars in a row, the four heads in a row. Verified by hand on 2026-09-25:
the patch loads, and before Task 2 `newshow` stopped at "no fixture in this
workspace has a gobo channel".
"""

import shutil
from pathlib import Path

from qlctool.cli import main

EMPTY = Path(__file__).resolve().parent / "data" / "empty-workspace.qxw"


def build_small_rig_patch(folder: Path) -> Path:
    """Write club-patch.qxw into `folder` and return it."""
    empty = folder / "empty.qxw"
    shutil.copy(EMPTY, empty)
    adds, address = [], 1
    for index in range(1, 7):
        adds += ["--add", f"Vortex|PC-64 LED S|Default|0|{address}|Par {index}"]
        address += 5
    for index in range(1, 3):
        adds += ["--add", f"LED Beam|Mini Led Moving Head|16 Channels|0|{address}|Beam {index}"]
        address += 16
    for index in range(1, 3):
        adds += ["--add", f"Chauvet|MiN Wash|13 Channel|0|{address}|Wash {index}"]
        address += 13
    patched = folder / "patched.qxw"
    groups = ["--group-new", "Pars=6x1", "--group-new", "Heads=4x1"]
    assert main(["patch", str(empty), *adds, *groups, "--out", str(patched)]) == 0
    cells = [arg for i in range(6) for arg in ("--group-add", f"0={i}@{i},0")]
    cells += [arg for i in range(6, 10) for arg in ("--group-add", f"1={i}@{i - 6},0")]
    out = folder / "club-patch.qxw"
    assert main(["patch", str(patched), *cells, "--out", str(out)]) == 0
    empty.unlink()
    patched.unlink()
    return out
```

`tests/test_small_rig.py`:

```python
"""2026-09-25: a rig with no gobo, prism or haze machine gets a show (ruling C2).

`newshow` stopped at the gobo wheel ("no fixture in this workspace has a gobo
channel"), then at the haze timer, then at AUTO's members: every generator
assumed Vibra's beams and fog.
"""

from pathlib import Path

import pytest

from qlctool.cli import main
from qlctool.workspace import Workspace
from qlctool.xmlutil import iter_local
from small_rig import build_small_rig_patch


@pytest.fixture(scope="module")
def club(tmp_path_factory) -> Path:
    folder = tmp_path_factory.mktemp("club")
    patch = build_small_rig_patch(folder)
    out = folder / "club.qxw"
    assert main(["newshow", str(patch), "--out", str(out)]) == 0
    return out


def test_the_show_is_built(club):
    functions = list(iter_local(Workspace.load(club).root, "Function"))
    assert len(functions) > 100


def test_nothing_is_generated_for_what_the_rig_lacks(club):
    names = {f.get("Name") for f in iter_local(Workspace.load(club).root, "Function")}
    assert "Humo Auto" not in names
    assert "Gobo Animacion" not in names
    assert "Prisma Animacion" not in names
    assert "AUTO" in names
```

Run: `.venv/bin/python -m pytest tests/test_small_rig.py -q -n 0`
Expected: FAIL with `ValueError: no fixture in this workspace has a gobo channel`.

- [ ] **Step 2: The two units**

`qlctool/generate/haze_machines.py`:

```python
"""The fog-only machines: the haze a timer may fire, never a lit column.

A smoke machine that also carries lights is a show machine - a vertical
column somebody fires on purpose - and a timer that fires it all night is a
wrong show and an empty tank. `smoke_auto` and `newshow` both ask this.
"""

from collections.abc import Iterable

from .. import roles
from ..capability import FixtureCapabilities


def haze_machines(capabilities: Iterable[FixtureCapabilities]) -> list[FixtureCapabilities]:
    """Every smoke machine without a red channel, in patch order."""
    return [c for c in capabilities if c.is_smoke and not c.has_role(roles.RED)]
```

`qlctool/generate/rig_has_role.py`:

```python
"""Whether any patched fixture drives a role - the question before a wheel generator."""

from collections.abc import Iterable

from ..capability import FixtureCapabilities


def rig_has_role(capabilities: Iterable[FixtureCapabilities], role: str) -> bool:
    """True when at least one fixture has a channel for `role`."""
    return any(capability.has_role(role) for capability in capabilities)
```

(Check the capability class's module and name with
`grep -n "^class" qlctool/capability.py`; `checks/rule_held_column.py` reads
`capability.is_smoke` without calling it, so it is a property.)

In `qlctool/generate/smoke_auto.py`, replace the list comprehension that
filters `c.is_smoke and not c.has_role(roles.RED)` with
`smoke = haze_machines(capabilities_of(workspace.root, library))` and drop
the now-unused `roles` import if nothing else uses it.

- [ ] **Step 3: Guard the generators and make their members optional**

In `qlctool/generate/canonical_show.py` (`V` is `vocabulary`, `caps` the
capabilities list already computed near the top):

- `gobos = generate_wheel_scenes(... role=roles.GOBO ...)` becomes
  `gobos = generate_wheel_scenes(...) if rig_has_role(caps, roles.GOBO) else GeneratedWheel([], None)`.
- `beam_colors = generate_wheel_scenes(... fixture_ids=beams ...)` becomes
  `... if beams else GeneratedWheel([], None)`.
- `prisms = generate_wheel_scenes(... role=roles.PRISM ...)` becomes
  `... if rig_has_role(caps, roles.PRISM) else GeneratedWheel([], None)`.
- `smoke = generate_smoke_auto(workspace, library)` becomes
  `smoke = generate_smoke_auto(...) if haze_machines(caps) else None`, and the
  two lines after it (`master.update(smoke.interval_ids)` and
  `master[V.display("smoke_on")] = smoke.on_id`) go under
  `if smoke is not None:`.
- Every `master[V.display(x)]` read of a function the rig may lack becomes
  `master.get(V.display(x))`: `gobo_animation`, `dimmer_chase`,
  `head_movements`, `colour_wheel`, `smoke_auto`, `talk_light` (in the three
  levels, AUTO, and the four moments). The level and AUTO lists already
  filter `None` in their comprehensions or, for AUTO, must be written as

  ```python
  auto_members = [
      f for f in (master.get(V.display("colour_wheel")), master.get(V.display("smoke_auto")))
      if f is not None
  ] + [*pixel_layer]
  ```

  and the `else` branch as
  `auto_members += [f for f in (master.get(V.display("head_movements")), master.get(V.display("gobo_animation"))) if f is not None]`.
  `generate_moments` already drops `None` members.
- `master.get(V.display("fast_movements"), master[V.display("head_movements")])`
  becomes `master.get(V.display("fast_movements"), master.get(V.display("head_movements")))`.

These are the exact changes verified in a scratch copy on 2026-09-25 (the
small club's check came out clean at 214 buttons once Task 3 was in, and `Vibra.qxw` came out at
its baseline hash `10c12af2...b706f8`).

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/python -m pytest tests/test_small_rig.py tests/test_smoke_auto.py tests/test_wheel_scenes.py tests/test_canonical_show.py -q`
(`ls tests/test_smoke*.py` for the smoke test's name.)
Expected: all pass. Then `.venv/bin/python tests/vibra_compare.py`: three
`identical`.

- [ ] **Step 5: Gates, commit**

```text
fix(qlctool): newshow builds on a rig with no gobo, prism or haze machine

The gobo, beam-wheel and prism generators run only where a fixture has
the role, the haze timer only where there is a fog-only machine, and
AUTO, the levels and the moments leave out what was not built.
```

---

### Task 3: A one-family energy cycle of level Collections is a structural cycle

**Files:**
- Create: `qlctool/checks/steps_are_levels.py`
- Modify: `qlctool/checks/family_frames.py`
- Test: `tests/test_check.py`

**Interfaces:**
- Consumes: `ShowGraph.kind(id)`, `ShowGraph.members`, `build_small_rig_patch`.
- Produces: `steps_are_levels(graph: ShowGraph, function_id: int) -> bool`.

- [ ] **Step 1: The dated regression test**

Append to `tests/test_check.py` (add the imports it needs at the top of the
file, next to the existing ones: `from small_rig import build_small_rig_patch`
and whatever of `main`, `check_workspace`, `FixtureLibrary`, `Workspace` the
file does not import yet):

```python
def test_a_single_family_energy_cycle_is_not_a_family_owner(tmp_path):
    """2026-09-25, the small club (Plan C): a false positive, not a show bug.

    The club's energy cycle steps through level Collections that only move the
    heads - its pars have no pan/tilt and its dimmer levels sit inside the
    steps - so it writes one family. `family_frames` counted a Chaser as a
    structural cycle only when it wrote two or more families, took this one
    for the position family's owner, and reported "familia con dueño: <energy
    cycle>: no tiene su Toggle en el marco" and "capa pisada por el ciclo:
    <heads centre>". Vibra's own cycle writes several families, which is why
    no shipped workspace showed it.
    """
    patch = build_small_rig_patch(tmp_path)
    out = tmp_path / "club.qxw"
    assert main(["newshow", str(patch), "--out", str(out)]) == 0
    findings = check_workspace(Workspace.load(out), FixtureLibrary.load())
    assert [f for f in findings if f.rule in ("familia con dueño", "capa pisada por el ciclo")] == []
```

(Confirm the two rule names with
`grep -rn "RULE = " qlctool/checks/rule_family_owner.py qlctool/checks/rule_layer_trace.py qlctool/checks/rule_pick_overridden.py`
and use the exact strings the module constants hold.)

Run: `.venv/bin/python -m pytest tests/test_check.py -q -n 0 -k single_family_energy_cycle`
Expected: FAIL, listing the two findings.

- [ ] **Step 2: The unit**

`qlctool/checks/steps_are_levels.py`:

```python
"""Whether a chaser steps through levels: Collections that start other programmes.

An energy cycle is a Chaser whose steps are level Collections, each starting
chasers or collections of its own. It coordinates the room even when the only
family it writes directly is one - the small club's cycle moves only the heads
(2026-09-25) - so the family-owner rules must look through it, not at it.
"""

from .show_graph import ShowGraph


def steps_are_levels(graph: ShowGraph, function_id: int) -> bool:
    """True when every step is a Collection containing a Chaser, Collection or Sequence."""
    members = graph.members.get(function_id, ())
    return bool(members) and all(
        graph.kind(member) == "Collection"
        and any(
            graph.kind(inner) in ("Chaser", "Collection", "Sequence")
            for inner in graph.members.get(member, ())
        )
        for member in members
    )
```

- [ ] **Step 3: Use it in `family_frames.py`**

Import it (`from .steps_are_levels import steps_are_levels`) and change:

- In `_owner_families`, the condition
  `graph.kind(function_id) in ("Chaser", "Sequence") and len(families) > 1`
  becomes
  `graph.kind(function_id) in ("Chaser", "Sequence") and (len(families) > 1 or steps_are_levels(graph, function_id))`.
- `_nested_owner_frontier` gains a last parameter `level_step: bool = False`;
  its two predicates become

  ```python
  is_cycle = kind in ("Chaser", "Sequence") and (
      len(families) > 1 or steps_are_levels(graph, function_id)
  )
  is_level = kind == "Collection" and inside_structural_cycle and (
      len(families) > 1 or level_step
  )
  ```

  and the recursion passes
  `is_cycle and steps_are_levels(graph, function_id)` as `level_step`.
- The `_owner_frontier` docstring gains one sentence: "A Chaser whose steps
  are all level Collections is structural too, even with one family
  (`steps_are_levels`, 2026-09-25)."

Two narrower fixes were tried on 2026-09-25 and are wrong: treating any
Chaser with Collection steps as structural (findings on Vibra:
"Rueda Multicolor" steps through Collections that are colour looks, not
levels), and dropping the family guard on `is_level` (breaks Vibra).

- [ ] **Step 4: Run the tests, then every shipped workspace**

Run: `.venv/bin/python -m pytest tests/test_check.py tests/test_solo_handoff.py tests/test_play_generators.py -q`
Expected: all pass.
Then the three `qlctool check` gates: each `522 botones revisados, ningun
problema`.

- [ ] **Step 5: Commit**

```text
fix(qlctool): a chaser of level collections is a structural cycle

The small club's energy cycle writes one family, and family_frames took
it for that family's owner. A chaser whose steps are all level
Collections is now looked through like a multi-family cycle.
```

---

### Task 4: The small-club example, in English, generated, checked and validated

**Files:**
- Create: `examples/small-club/fixtures/{Vortex-PC-64-LED-S,LED-Beam-Mini-Led-Moving-Head,Chauvet-MiN-Wash}.qxf`
  (copies of `QLC+ Fixtures/`), `examples/small-club/club-patch.qxw`,
  `examples/small-club/show.toml`, `examples/small-club/club.qxw` (generated),
  `tests/test_small_club_example.py`
- Modify: `docs/toolkit.md` (repo root), `pyproject.toml`
  (`codeality-py.toml` too if it scans `examples/`)

**Interfaces:**
- Consumes: `build_small_rig_patch`, `[rig] fixtures` (Plan B Task 3),
  `language = "en"` (Plan B Task 12).

- [ ] **Step 1: Write the example's source files**

```bash
mkdir -p examples/small-club/fixtures
cp "../../QLC+ Fixtures/Vortex-PC-64-LED-S.qxf" "../../QLC+ Fixtures/LED-Beam-Mini-Led-Moving-Head.qxf" "../../QLC+ Fixtures/Chauvet-MiN-Wash.qxf" examples/small-club/fixtures/
.venv/bin/python -c "import sys; sys.path.insert(0, 'tests'); from pathlib import Path; from small_rig import build_small_rig_patch; print(build_small_rig_patch(Path('examples/small-club')))"
```

`examples/small-club/show.toml`:

```toml
# A small club: six RGB pars, two beam moving heads, two washes, no haze
# machine and no controllers. Nothing here is the Vibra show's: the patch is
# its own and every other choice falls back to the toolkit's defaults.
# Regenerate from the toolkit's root:
#   qlctool newshow --description examples/small-club/show.toml --validate

[show]
name = "Small Club"
language = "en"

[rig]
workspace = "club-patch.qxw"
output = "club.qxw"
fixtures = ["fixtures"]
```

- [ ] **Step 2: Generate, check, validate**

```bash
.venv/bin/qlctool newshow --description examples/small-club/show.toml --validate
.venv/bin/qlctool --fixtures examples/small-club/fixtures check examples/small-club/club.qxw
```

Expected: `newshow` prints its summary and QLC+ loads the file; `check`
reports no problem (its message is Spanish, ruling B10: `... botones
revisados, ningun problema`). If `check` finds anything, it is either a
toolkit assumption this rig breaks (fix it the Task 3 way: rule, dated test,
fix) or a real show bug (fix the generator): never edit `club.qxw`.

- [ ] **Step 3: The test that keeps it true**

`tests/test_small_club_example.py`:

```python
"""Spec step 7 (2026-09-25): a second rig, described in English, with no controllers.

The example is regenerated from its description and must match the committed
file byte for byte, pass every check and load in QLC+ - the proof that a
description and a patch are enough, with nothing of Vibra's.
"""

import hashlib
from pathlib import Path

import pytest

from qlctool.checks.run import check_workspace
from qlctool.cli import main
from qlctool.library import FixtureLibrary
from qlctool.validate import qlcplus_binary, validate_workspace
from qlctool.workspace import Workspace

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "small-club"


@pytest.fixture(scope="module")
def regenerated(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("club") / "club.qxw"
    assert main(["newshow", "--description", str(EXAMPLE / "show.toml"), "--out", str(out)]) == 0
    return out


def test_the_example_regenerates_byte_for_byte(regenerated):
    digest = hashlib.sha256(regenerated.read_bytes()).hexdigest()
    assert digest == hashlib.sha256((EXAMPLE / "club.qxw").read_bytes()).hexdigest()


def test_the_example_passes_every_check(regenerated):
    library = FixtureLibrary.load([EXAMPLE / "fixtures"])
    assert check_workspace(Workspace.load(regenerated), library) == []


def test_the_example_has_no_controller(regenerated):
    text = regenerated.read_text(encoding="utf-8")
    assert "<Input " not in text
    assert "Desk · " not in text


@pytest.mark.skipif(qlcplus_binary() is None, reason="QLC+ is not installed on this machine")
def test_qlcplus_loads_the_example(regenerated):
    assert validate_workspace(regenerated).errors == []
```

(If `<Input ` appears in a controller-free show for another reason - for
example the audio trigger widget's own input - replace that assertion with
the one Plan A's `test_a_show_without_controllers_has_no_pad_binding_and_no_desk`
uses, reading `tests/test_controllers.py`.)

Run: `.venv/bin/python -m pytest tests/test_small_club_example.py -q -n 0`
Expected: `4 passed`.

- [ ] **Step 4: Package and docs**

- `pyproject.toml`: nothing to add to the wheel (examples are repository
  content, not package data). If `codeality-py.toml` has an include list that
  would scan `examples/`, exclude it.
- `docs/toolkit.md` (repo root): an "Examples" section: the small club, what
  it contains, the regenerate command above, and that it is tested
  byte-for-byte.

- [ ] **Step 5: Gates, commit, push**

Five gates; then

```text
feat(qlctool): the small-club example, a second rig described in English

Six pars, two beams and two washes with no haze machine and no
controllers, described in English: generated, checked with no finding,
loaded in QLC+, and held byte-identical by a test.
```

`git pull --rebase origin main && git push origin main` (Task 5 clones from
`origin`, so this must be on GitHub first).

---

### Task 5: Cut `spectalive/qlctool` out of a fresh clone, and make it stand alone

**Files (all in `/Users/cristiandeluxe/p/qlctool`, the new clone):**
- Create: `tests/data/rig/` (frozen rig), `tests/data/rig/qlctool.toml`
- Modify: `tests/rig_root.py`, `README.md`, `NOTICE`, `pyproject.toml`,
  `.github/workflows/quality.yml`, docs links
- Delete: `tests/test_pad_palette.py`

**Interfaces:**
- Consumes: Tasks 1-4 pushed to `origin/main`.
- Produces: a local repository whose suite passes with no reference to
  vibra-lighting's layout; nothing is pushed yet.

- [ ] **Step 1: The fresh clone**

```bash
test ! -e /Users/cristiandeluxe/p/qlctool && echo free
git clone git@github.com:Vibra-Lab/vibra-lighting.git /Users/cristiandeluxe/p/qlctool
git -C /Users/cristiandeluxe/p/qlctool log --oneline -1
```

Expected: `free`, then the clone, whose head equals this repository's pushed
`main` (`git -C /Users/cristiandeluxe/p/DMX-Fixtures rev-parse origin/main`).
If the path is not free, stop and ask: never reuse or delete it.

- [ ] **Step 2: Filter the history**

```bash
cd /Users/cristiandeluxe/p/qlctool
git filter-repo \
  --path tools/qlctool/ \
  --path docs/toolkit.md --path docs/checks.md --path docs/qxw-format.md \
  --path docs/qlcplus-environment.md --path docs/qlc5-verification.md \
  --path .github/workflows/quality-qlctool.yml \
  --path LICENSE --path LICENSE-CC-BY-4.0 --path NOTICE \
  --path-rename tools/qlctool/: \
  --path-rename .github/workflows/quality-qlctool.yml:.github/workflows/quality.yml
git log --oneline | wc -l
ls
git remote -v
```

Expected: about 150 commits (146 touched `tools/qlctool` on 2026-09-24, plus
the docs'), the package at the root (`qlctool/`, `tests/`, `docs/`,
`examples/`, `pyproject.toml`, `README.md`, `TODO.md`, `uv.lock`, `LICENSE`,
`LICENSE-CC-BY-4.0`, `NOTICE`), and no remote (filter-repo removes `origin`,
which is what keeps this from ever pushing to vibra-lighting). The old
`tools/qlctool/docs/` files land in `docs/` beside the moved toolkit docs;
no name collides (checked 2026-09-25).

- [ ] **Step 3: The frozen rig**

Copy what the suite reads from vibra-lighting at the commit the clone was
taken from:

```bash
SRC=/Users/cristiandeluxe/p/DMX-Fixtures
RIG=tests/data/rig
mkdir -p "$RIG/QLC+ Setups"
cp -R "$SRC/QLC+ Fixtures" "$SRC/QLC+ InputProfiles" "$RIG/"
cp -R "$SRC/QLC+ Setups/Gobos" "$RIG/QLC+ Setups/"
for f in Vibra.qxw Vibra-beats.qxw Vibra-split.qxw Vibra.desk.json \
         vibra.toml vibra-beats.toml vibra-split.toml \
         vibra-stage-plot.json vibra-stage-plot-split.json \
         DeluxeEventos.qxw DeluxeEventos2.qxw DeluxeEventos2_qlcv5.qxw DeluxeEventos2_qlc4143.qxw Pantera.qxw; do
  cp "$SRC/QLC+ Setups/$f" "$RIG/QLC+ Setups/"
done
cat > "$RIG/qlctool.toml" <<'TOML'
# The rig the test suite reads: a frozen copy of vibra-lighting's, 2026-09-25.
fixtures = ["QLC+ Fixtures"]
input_profiles = ["QLC+ InputProfiles"]
gobos = ["QLC+ Setups/Gobos"]
TOML
cat > "$RIG/README.txt" <<'TXT'
A frozen copy of the Vibra rig from github.com/Vibra-Lab/vibra-lighting
(CC BY 4.0 for the workspaces, Apache-2.0 for the fixture definitions and
input profile), used only by this repository's tests. Update it by copying
the same files again; the byte-identity hashes in tests/vibra_baseline.json
change only when the generator's output is meant to change.
TXT
```

Before copying, confirm `git -C "$SRC" status --short "QLC+ Setups" "QLC+ Fixtures" "QLC+ InputProfiles"`
prints nothing (the copy must equal the committed rig).

In `tests/rig_root.py`, `_default()` becomes `return here / "data" / "rig"`
and the docstring drops the vibra-lighting sentence; the file no longer
mentions `parents`.

`git rm tests/test_pad_palette.py` (it reads `tools/smc-pad/`, which stays in
vibra-lighting; ruling C6).

- [ ] **Step 4: Make the repository describe itself**

- `pyproject.toml`: `description = "Generate, check and validate QLC+ lighting shows from a patched workspace and a TOML description"`;
  add `license = "Apache-2.0"`, `readme = "README.md"`, and
  `[project.urls] Homepage = "https://github.com/spectalive/qlctool"`.
  Leave `version = "0.1.0"`.
- `README.md`: the first paragraph says what the toolkit is without Vibra
  ("... for any rig; the Vibra show it was built for is at
  github.com/Vibra-Lab/vibra-lighting"); the `docs/` link becomes
  `docs/toolkit.md`; add "Install" (`pip install
  "qlctool @ git+https://github.com/spectalive/qlctool.git@v0.1.0"`, or
  `python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'` in a clone),
  "Example" (`examples/small-club/`), and "Licence" (code Apache-2.0, docs CC
  BY 4.0, QLC+'s vendored files under QLC+'s Apache-2.0; ruling C9).
- `NOTICE`:

  ```text
  qlctool
  Copyright 2024-2026 Cristian Deluxe

  This product includes software developed as part of Q Light Controller Plus
  (QLC+), https://github.com/mcallegari/qlcplus, licensed under the Apache
  License, Version 2.0: the fixture schema and the system fixture definitions
  vendored in qlctool/library/.
  ```

- `.github/workflows/quality.yml`: delete the `defaults.run.working-directory`
  block and its comment, change `path: tools/qlctool/pyrefly.json` to
  `path: pyrefly.json`, and change `branches: [qlctool]` to `branches: [main]`.
- Every relative link that pointed into vibra-lighting (`../../docs/...`,
  `../../QLC+ Setups/...`): `grep -rn "\.\./\.\./" --include=*.md .` and
  rewrite each to the moved doc or to an absolute
  `https://github.com/Vibra-Lab/vibra-lighting/blob/main/...` URL.
- `AGENTS.md`-style instructions that were in vibra-lighting's AGENTS.md do
  not move; `TODO.md` (the toolkit's own) does.

- [ ] **Step 5: Verify the repository stands alone**

```bash
cd /Users/cristiandeluxe/p/qlctool
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest tests/ -q
.venv/bin/python tests/vibra_compare.py --validate
.venv/bin/qlctool check "tests/data/rig/QLC+ Setups/Vibra.qxw"
grep -rn "DMX-Fixtures\|vibra-lighting/tools\|parents\[3\]" qlctool tests ; echo "exit $?"
uv lock --check
```

Expected: the suite passes with Task 4's count minus `test_pad_palette.py`'s
tests; three `identical ... QLC+ loaded it` lines; `522 botones revisados,
ningun problema`; `exit 1` from the grep; `uv lock --check` succeeds (if the
description or URL change requires it, run `uv lock` and commit `uv.lock`).

- [ ] **Step 6: Commit (locally, in the new repository)**

```bash
git add tests/data/rig tests/rig_root.py README.md NOTICE pyproject.toml .github/workflows/quality.yml docs uv.lock
git rm --cached -q tests/test_pad_palette.py 2>/dev/null || true
git commit -F- <<'MSG'
chore: stand alone as spectalive/qlctool

A frozen copy of the Vibra rig for the tests, the suite pointed at it,
the README, NOTICE, package metadata and CI workflow rewritten for a
repository of its own, and the SMC-PAD LED test left with the show.
MSG
git log --format='%an <%ae>' -1
```

Expected: the author line is `Cristian Deluxe <me@cristiandeluxe.dev>`; if the
clone has no local identity, set it with `git config user.name "Cristian Deluxe"`
and `git config user.email me@cristiandeluxe.dev` in this repository only,
and amend.

---

### Task 6: Publish `spectalive/qlctool` and tag `v0.1.0`

**Files:** none changed; this task writes to GitHub (authorised, Global
Constraint 9).

**Interfaces:**
- Produces: `https://github.com/spectalive/qlctool`, public, `main` pushed,
  annotated tag `v0.1.0`, and a GitHub release for it. Task 7 installs
  `git+https://github.com/spectalive/qlctool.git@v0.1.0`.

- [ ] **Step 1: Check the target is still free**

```bash
gh repo view spectalive/qlctool 2>&1 | head -1
```

Expected: `GraphQL: Could not resolve to a Repository ...`. If the repository
exists, stop and ask the owner: never push into an existing repository.

- [ ] **Step 2: Create and push**

```bash
cd /Users/cristiandeluxe/p/qlctool
gh repo create spectalive/qlctool --public \
  --description "Generate, check and validate QLC+ lighting shows from a patched workspace and a TOML description" \
  --source . --remote origin --push
git remote -v
git status -sb
```

Expected: `origin` is `https://github.com/spectalive/qlctool.git` (or the SSH
form) and `main` tracks `origin/main` with nothing ahead.

- [ ] **Step 3: Tag and release**

```bash
git tag -a v0.1.0 -m "qlctool 0.1.0: the first release as its own repository"
git push origin v0.1.0
gh release create v0.1.0 --repo spectalive/qlctool --title "qlctool 0.1.0" \
  --notes "First release as a standalone repository, extracted with its history from Vibra-Lab/vibra-lighting. Generates a QLC+ show from a patched workspace and a TOML description (English or Spanish), checks it, and validates it in headless QLC+. Example: examples/small-club."
```

- [ ] **Step 4: Prove the tag installs**

```bash
TMP=$(mktemp -d)
python3 -m venv "$TMP/venv"
"$TMP/venv/bin/pip" install "qlctool @ git+https://github.com/spectalive/qlctool.git@v0.1.0"
"$TMP/venv/bin/qlctool" --help | head -3
"$TMP/venv/bin/python" -c "from qlctool.checks.rule_providers import rule_providers; print(sorted(p.name for p in rule_providers()))"
```

Expected: the help text, and `['smc-pad', 'tablet_desk']` (entry points
survive a non-editable install; `declared_rule_providers` returns `()` there,
ruling B2). Leave `$TMP` for the OS to clear; it is under the system temp dir.

- [ ] **Step 5: Record it**

The CI workflow runs on the push: `gh run list --repo spectalive/qlctool --limit 3`.
Report its state; a red run is a finding for `TODO.md` in the new repository
(not a reason to move the tag).

---

### Task 7: vibra-lighting depends on `v0.1.0`

**Files (in `/Users/cristiandeluxe/p/DMX-Fixtures`):**
- Create: `requirements.txt`, `pytest.ini`, `tests/` (`rig_root.py`,
  `conftest.py`, `vibra_baseline.json`, `vibra_regen.py`, `vibra_compare.py`,
  `test_vibra_byte_identity.py`, `test_shipped_deskmap.py`,
  `test_input_profile.py`, `test_definition_schema.py`, `test_pad_palette.py`)
- Delete: `tools/qlctool/`, `docs/toolkit.md`, `docs/checks.md`,
  `docs/qxw-format.md`, `docs/qlcplus-environment.md`,
  `docs/qlc5-verification.md`, `.github/workflows/quality-qlctool.yml`
- Modify: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `NOTICE`,
  `docs/README.md`, `docs/blenderdmx.md`, `docs/smc-pad-led.md`,
  `docs/old-vs-new-audit-2026-08-28.md`, `QLC+ Setups/vibra.toml`,
  `QLC+ Setups/vibra-beats.toml`, `QLC+ Setups/vibra-split.toml`,
  `tools/smc-pad/README.md`, `tools/smc-pad/qlc_led_bridge.swift`,
  `Manual/M-VAVE SMC-PAD - manual (transcripcion).md` (its link only),
  `TODO.md`, `TODO_LOG.md`

**Interfaces:**
- Consumes: the `v0.1.0` tag.
- Produces: `.venv/bin/qlctool` at the repository root, installed from the tag.

- [ ] **Step 1: Move the show's own tests out before anything is deleted**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
mkdir -p tests
for f in rig_root.py conftest.py vibra_baseline.json vibra_regen.py vibra_compare.py \
         test_vibra_byte_identity.py test_shipped_deskmap.py test_input_profile.py \
         test_definition_schema.py test_pad_palette.py; do
  git mv "tools/qlctool/tests/$f" "tests/$f" 2>/dev/null || cp "tools/qlctool/tests/$f" "tests/$f"
done
```

(`git mv` for the files only this repository needs; the toolkit already has
its own copies from the extraction. `rig_root.py` here keeps the fallback to
`parents[1]`: edit `_default()` to `return Path(__file__).resolve().parents[1]`,
the repository root, and drop the `data/rig` branch - this repository is the
rig.) Fix the docstring usage line in `vibra_compare.py`
("cd tools/qlctool && ..." -> ".venv/bin/python tests/vibra_compare.py ...").

`requirements.txt`:

```text
# The toolkit this show is generated with, pinned to a release (ruling C7).
# Reinstall after changing the tag: .venv/bin/pip install -r requirements.txt
qlctool[dev] @ git+https://github.com/spectalive/qlctool.git@v0.1.0
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -n auto
```

- [ ] **Step 2: Install the tag and run the show's tests against it**

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python tests/vibra_compare.py --validate
.venv/bin/qlctool check "QLC+ Setups/Vibra.qxw"
.venv/bin/qlctool check "QLC+ Setups/Vibra-beats.qxw"
.venv/bin/qlctool check "QLC+ Setups/Vibra-split.qxw"
.venv/bin/qlctool install --check
```

Expected: every moved test passes; three `identical ... QLC+ loaded it`;
three `522 botones revisados, ningun problema`; install check exits 0. The
repo-root `qlctool.toml` (Plan B Task 3) is what lets the installed toolkit
find `QLC+ Fixtures/` from here. Only after this passes, continue.

- [ ] **Step 3: Remove what moved**

```bash
git status --ignored --short tools/qlctool | grep -v "^!! tools/qlctool/\(.venv\|.pytest_cache\|.ruff_cache\|qlctool.egg-info\|.coverage\)" | grep "^!!"
```

Expected: no output (nothing ignored besides the venv and caches). If
anything else is listed, copy it to
`/private/tmp/claude-501/-Users-cristiandeluxe-p-DMX-Fixtures/<session>/scratchpad/qlctool-leftovers/`
and report it before deleting. Then check nothing runs from the old venv
(`pgrep -fl "tools/qlctool/.venv"` prints nothing; the Mac mini launcher
runs its own worktree on another machine, see Step 5), and:

```bash
git rm -r -q tools/qlctool docs/toolkit.md docs/checks.md docs/qxw-format.md docs/qlcplus-environment.md docs/qlc5-verification.md .github/workflows/quality-qlctool.yml
rm -rf tools/qlctool
```

`.gitignore`: replace `tools/qlctool/.venv/` with `.venv/`.

- [ ] **Step 4: Point every reference at the new home**

`git grep -n "tools/qlctool"` lists them; each becomes one of:

- a command: `cd tools/qlctool && .venv/bin/qlctool X "../../QLC+ Setups/Y"`
  -> `.venv/bin/qlctool X "QLC+ Setups/Y"` from the repository root (AGENTS.md
  environment, regeneration recipe, gates; CLAUDE.md "Before finishing";
  the "Regenerate:" comment line in the three `vibra*.toml`);
- a source path (`tools/qlctool/qlctool/generate/smc_pad_colors.py` in
  `tools/smc-pad/README.md`, `qlc_led_bridge.swift`, the SMC-PAD manual
  note) -> `qlctool/generate/smc_pad_colors.py in
  https://github.com/spectalive/qlctool`;
- a doc link (`docs/toolkit.md`, `docs/checks.md`, ... in `README.md`,
  `docs/README.md`, `docs/blenderdmx.md`, `docs/smc-pad-led.md`,
  `docs/old-vs-new-audit-2026-08-28.md`) ->
  `https://github.com/spectalive/qlctool/blob/v0.1.0/docs/<name>.md`.

`QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi` mentions the generator's path in its
generated header comment; it is byte-tested against `qlctool input-profile`,
so leave it until the next toolkit release regenerates it, and add a
`TODO.md` line saying so.

`NOTICE`: drop the QLC+ paragraph (those files left with the toolkit) unless
`git grep -l "qlcplus.org" -- ':!Manual'` still finds vendored QLC+ files
here. `README.md` "Licence": `tools/` now means the other tools.

`CLAUDE.md`: "What lives where" - `tools/qlctool/` becomes "the toolkit,
installed from `spectalive/qlctool` (pinned in `requirements.txt`)"; "Before
finishing" uses the new commands; "A malfunction is not fixed until a check
can see it" points rule and test locations at the toolkit repository
("`qlctool/checks/` and `tests/test_check.py` in spectalive/qlctool; then
bump the tag here").

`AGENTS.md`: add a "Reinstalling after the extraction (2026-09-25)" section:

```text
Every checkout that had tools/qlctool/.venv:
  git pull
  rm -rf tools/qlctool            # only the ignored venv and caches are left there
  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  .venv/bin/qlctool install --check
Machines: this MacBook; the show Mac (vibra-oficina); the Mac mini, whose
qlc-launcher runs a qlctool worktree of its own - point the launcher at the
repo-root .venv or reinstall its worktree from the tag.
Changing the toolkit: work in spectalive/qlctool, tag a release, bump the tag
in requirements.txt, reinstall, and run the show's tests here.
```

`TODO.md`: close spec steps 7 and 8 (log them in `TODO_LOG.md` with the
dates, the tag, the repository URL and the test evidence); move open items
that belong to the toolkit into `spectalive/qlctool`'s `TODO.md` in a follow-
up commit there (list which in this repository's log entry); add the open
item "Reinstall on the show Mac and the Mac mini (AGENTS.md, 2026-09-25)".

- [ ] **Step 5: Gates, commit, push**

Run Step 2's commands again after the deletions; all pass. Then

```bash
git add -A tests requirements.txt pytest.ini .gitignore AGENTS.md CLAUDE.md README.md NOTICE docs "QLC+ Setups/vibra.toml" "QLC+ Setups/vibra-beats.toml" "QLC+ Setups/vibra-split.toml" tools/smc-pad Manual TODO.md TODO_LOG.md
git status --short
```

Check the list contains only the paths above and the deletions from Step 3,
then commit:

```text
refactor: take qlctool from spectalive/qlctool v0.1.0

The toolkit and its docs moved, with their history, to
github.com/spectalive/qlctool. This repository keeps the rig, the show
and the tests that prove the pinned release still generates it byte for
byte.
```

`git pull --rebase origin main && git push origin main`.

- [ ] **Step 6: Durable knowledge**

- `~/p/wiki/brain/projects/vibra-dmx.md`: a dated section "qlctool extracted
  (2026-09-25)": the repository URL, the tag, rulings C5-C10, the reinstall
  procedure, and the open reinstall item for the other two machines; commit
  and push `~/p/wiki` (its own repository and rule).
- `~/p/PROJECT-MAP.md`: one line for `qlctool` ("public QLC+ show toolkit,
  github.com/spectalive/qlctool, extracted from vibra-dmx 2026-09-25"), and
  the vibra-dmx line no longer says "planned Python toolkit"; commit and push
  `~/p` (standing instruction in `~/p/CLAUDE.md`).

---

## Self-review against the spec

- Spec "Order" step 7 ("a second example rig with a different patch and no
  controllers, generated, checked and validated, to prove the description is
  enough"): Tasks 2-4. The patch shares no fixture instance with Vibra (six
  PC-64 pars, two LED Beam heads, two MiN Wash, two groups of its own); the
  description has no `[controllers]` and is English; the test regenerates,
  checks and validates it.
- Spec step 8 ("extract `tools/qlctool` and the toolkit docs to
  `spectalive/qlctool` with `git filter-repo`; this repository depends on a
  tagged release"): Tasks 5-7, with the owner's constraints: fresh clone,
  `gh repo create spectalive/qlctool --public`, `v0.1.0`, a git-URL
  dependency, Apache-2.0 carried (LICENSE, NOTICE), the byte-identity check's
  home settled (C6), AGENTS.md, README and TODO.md updated, reinstall
  instructions for the other checkouts.
- "The three Vibra workspaces come out byte-identical at every step":
  Global Constraint 1 in both repositories.
- The spec's rule for malfunctions: Task 3 is a checker false positive and
  carries its dated regression test before the fix; Task 2 is a generator
  crash on a new rig and carries its test.
- Placeholder scan: every new file has its content; commands have expected
  output; the only look-ups left to the executor are exact names the plan
  cannot know without running (the two rule constants in Task 3, the smoke
  test file name in Task 2), each with the command that finds it.
- Names used across tasks: `RIG_ROOT`, `build_small_rig_patch`,
  `haze_machines`, `rig_has_role`, `steps_are_levels`; each is defined once in
  the task the file map names.
