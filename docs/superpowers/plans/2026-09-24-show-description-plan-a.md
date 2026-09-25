# Show Description, Plan A: baseline, description, names, controllers, loader

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take every Vibra-specific choice out of `qlctool newshow`'s code and
into a `ShowDescription` that a TOML file can supply, with names resolved
through English/Spanish catalogues and the SMC-PAD and tablet desk turned into
optional controller profiles, while the three shipped Vibra workspaces keep
coming out byte for byte what they are today.

**Architecture:** A language-neutral `ShowDescription` (identifier-keyed
tables: colours, curated matrices, timing, fixture tuning, console, controllers)
is the generator's only source of show choices. `vibra_description()` is the
default; `load_show_description()` reads a `.toml` and validates it against the
patch the way `stage_plot.load_stage_plot` does. At the top of
`build_canonical_show` the description is localised through a `Names` resolver
(catalogues in `qlctool/locales/<lang>.toml` plus the description's
`[names.<lang>]` overrides) into the display names the generators write.
Controller checks leave `checks/run.py` and come back through a registry of
`RuleProvider`s discovered from the `qlctool.rules` entry-point group.

**Tech Stack:** Python >= 3.11 (venv 3.14.7), stdlib `tomllib`, `dataclasses`,
`importlib.metadata`, `difflib`; lxml; pytest + pytest-xdist; headless QLC+
5.2.2 for `--validate`.

**Spec:** `docs/superpowers/specs/2026-09-24-show-description-design.md`
(binding). This plan covers its "Order" steps 1-5 only. Steps 6-8 (library
paths, second example rig, `git filter-repo` extraction) are out of scope.

---

## Global Constraints

Read these before every task. A task that breaks one is not done.

1. **Byte identity.** `Vibra.qxw`, `Vibra-beats.qxw` and `Vibra-split.qxw`
   must regenerate byte-identical to the Task 1 baseline hashes after every
   task. A changed byte is a failed task: stop, find the cause, and do not
   commit until the difference is explained and accepted by the owner.
2. **Gates, every task, from `/Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool`:**
   ```bash
   .venv/bin/python -m pytest tests/ -q
   .venv/bin/python tests/vibra_compare.py --validate
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-beats.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
   ```
   The suite takes ~40 s on `-n auto`: run it in the foreground and **never
   pipe it through `tail`/`head`** (the exit code is lost, and a stopped suite
   leaves a headless QLC+ behind that makes later validation pass). Baseline on
   2026-09-24 at `c782f17`: `477 passed, 10 skipped`; each `check` prints
   `522 botones revisados, ningun problema` and exits 0. `vibra_compare.py
   --validate` (Task 1) regenerates all three into a temp dir, compares hashes,
   runs every check on them and loads each in headless QLC+; it must print three
   `identical, 0 finding(s), QLC+ loaded it` lines and exit 0. Before the first
   `--validate`, run `.venv/bin/qlctool install --check`; if it exits 1, run
   `.venv/bin/qlctool install` (AGENTS.md), then continue. Without QLC+ the
   validation cannot run - never claim it passed.
3. **One exported unit and one responsibility per file.** Helpers, constants,
   types and compound operations go in their own files with explicit imports
   (`~/.claude/CLAUDE.md`, repo `AGENTS.md` "Conventions"). `codeality-py.toml`
   caps source files at 150 lines and test files at 300. New pure-data modules
   (`qlctool/vibra/*.py`) are added to `[roles] data` in `codeality-py.toml`.
   Match the existing style: `ruff.toml` (line length 100, google docstrings),
   `mypy.ini` strict for every new module (no new `ignore_errors` sections).
   `ruff` is on the machine (`/opt/homebrew/bin/ruff`); run
   `ruff check <touched .py files>` and `ruff format --check <touched .py files>`
   in each task (the tree has 3 pre-existing findings and 7 unformatted files -
   do not touch those). `mypy` and `codeality-py` are not installed in the venv
   (the `quality` dependency group): do not claim they passed.
4. **No new runtime dependency.** `tomllib`, `importlib.metadata` and
   `difflib` are stdlib; `requires-python = ">=3.11"` already holds.
5. **Checks reason about capabilities and the function graph, never a
   function's display name.** The desk map and the controller checks resolve
   widgets by catalogue identifier, never by comparing against a Spanish
   string.
6. **Commits.** One commit per task, English, conventional style as in
   `git log --oneline -20` (`feat(qlctool): ...`, `refactor(qlctool): ...`,
   `test(qlctool): ...`), stage only the task's paths, no AI attribution in
   subject or body, and every message ends with the line
   `Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw`.
   Commit on `main`. After Task 8, push `main` to `origin` (AGENTS.md: finished,
   verified work is pushed).
7. **Never hand-edit a `Vibra*.qxw`**, and never write regenerated output over
   the shipped files during this plan: every regeneration goes to a temp dir
   (`vibra_compare.py`, `tmp_path`). The shipped files are the baseline.

**Rulings this plan makes where the spec is silent or ambiguous** (each is
repeated where it bites):

- R1. *Generator vocabulary stays Spanish in Plan A.* The generators write
  hundreds of Spanish literals (`"Colores {group}"`, `"Ciclo Paneles Mixto"`,
  help lines, check messages, `GLYPHS`, `FUNCTION_COLORS`, `SMC_PAD_BINDINGS`,
  `WHEEL_NAMES`, `SHORT_COLOR`, `MIX_CODE`...). Plan A routes the description's
  own names (colours, function names in keys/flash/beat timings) through the
  catalogue and makes the desk and controller lookups identifier-based, but
  `build_canonical_show` refuses (clear `ValueError`) any description whose
  effective vocabulary differs from the `es` catalogue: `language != "es"` or an
  override that changes a display name. The catalogues, `identify`, `display`
  and overrides are complete and tested; making the generators' literals come
  from the catalogue is the first task of the next plan, logged in `TODO.md`.
- R2. *Vibra's values keep one source.* The existing Spanish tables
  (`palette.py`, `simple_colors.py`, the pair modules, `CURATED_MATRICES`, and
  the constants moved out of `canonical_show.py`) remain the in-code values;
  `vibra_description()` turns them into identifiers through the `es` catalogue,
  and `QLC+ Setups/vibra.toml` is tested equal to it.
- R3. *Controller code is put behind profiles, not moved between packages.*
  `smc_pad_*`, `input_binding`, `desk_*` stay where they are; the new
  `qlctool/controllers/` package holds the profiles and rule providers. The
  physical split belongs to the `smc-pad`/`dmxdesk` designs the spec lists as
  out of scope.
- R4. *Desk map keys stay slugs.* `Vibra.desk.json` is the tablet's wire
  contract and is byte-tested (`tests/test_shipped_deskmap.py`); its control
  keys remain slugs of the display captions. Identifiers are used to find
  frames and to key burst durations and notes.
- R5. *Variants.* The beats variant is its own file, `vibra-beats.toml`, with
  `[timing] beats = true`. Because its patch source (`Vibra.qxw`) and its output
  (`Vibra-beats.qxw`) differ, `[rig]` gains an optional `output` key (default:
  the workspace itself, regenerated in place like the verified recipe). Three
  complete files, no include mechanism; a test holds each equal to
  `vibra_description()` apart from `[rig]` and `beats`.
- R6. *Defaults.* A TOML table replaces the default table wholesale (no deep
  merge); an omitted key keeps the Vibra default, except `[controllers]`, whose
  omission means no controllers (spec). `[show] language` defaults to `"es"` in
  Plan A (R1). Durations are seconds (`*_s`, as in the spec's `levels`), beat
  timings are beats.
- R7. *Curated matrices are stored per fixture group*
  (`matrices: Mapping[str, tuple[CuratedScript, ...]]`), which is the only
  order the generator reads (`canonical_show.py:439` filters by group).
- R8. *Only the spec's tables move* (palette, primaries, simple, white, pairs,
  matrix colours, curated matrices, timings incl. BPM, fixture tuning, canvas,
  keys, flash functions). Other generator constants (`QUAD_COLORS`, bank and
  wheel hold/fade, console geometry beyond the canvas size, `BURST_MS` values)
  stay put.
- R9. *A palette name must be catalogued.* A colour not in the catalogues is an
  error in Plan A (custom colours need R1's migration first).
- R10. *The toolkit's own providers are required.* `rule_providers()` raises
  when `smc-pad` or `tablet_desk` is not registered, so a checkout that was
  pulled without `pip install -e` fails loudly instead of skipping desk and pad
  checks.

---

## File map

New:

```
tools/qlctool/tests/vibra_baseline.json            Task 1  recipes + hashes
tools/qlctool/tests/vibra_regen.py                 Task 1  regenerate_vibra
tools/qlctool/tests/vibra_compare.py               Task 1  the compare script
tools/qlctool/tests/test_vibra_byte_identity.py    Task 1
tools/qlctool/qlctool/description/                 Tasks 2,3,5,7,8  dataclasses + transforms
tools/qlctool/qlctool/description/reading/         Task 8  TOML section readers
tools/qlctool/qlctool/vibra/                       Tasks 2,3,5,7  Vibra's values
tools/qlctool/qlctool/locales/{en,es}.toml         Task 4
tools/qlctool/qlctool/names/                       Tasks 4,5  catalogue + resolver
tools/qlctool/qlctool/controllers/                 Task 7  profiles + rule providers
QLC+ Setups/vibra.toml, vibra-beats.toml, vibra-split.toml   Task 8
```

Modified: `generate/canonical_show.py`, `generate/live_console.py`,
`generate/play_page.py`, `generate/color_banks.py`, `generate/matrix_effects.py`,
`generate/quad_color_scenes.py`, `generate/desk_bursts.py`, `desk_policy.py`,
`desk_burst_sources.py`, `desk_burst_buttons.py`, `desk_burst_note.py`,
`deskmap.py`, `checks/run.py`, `checks/rule_desk_bursts.py`,
`checks/valid_desk_bursts.py`, `checks/rule_pad_input.py`, `cli.py`,
`pyproject.toml`, `codeality-py.toml`, tests that imported moved constants,
`AGENTS.md`, `tools/qlctool/README.md`, `TODO.md`.

All paths below are relative to `/Users/cristiandeluxe/p/DMX-Fixtures` unless
they start with `qlctool/` or `tests/`, which are relative to
`/Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool`.

---

### Task 1: Baseline hashes and a regenerate-and-compare script

Verified on 2026-09-24 at `c782f17`: regenerating each workspace with the
AGENTS.md recipe into a scratch directory reproduces the committed file byte
for byte, so **the committed files are the baseline**:

| workspace | sha256 |
|---|---|
| `Vibra.qxw` | `10c12af24a1c72718906f77698f447998ddcdc7ef01b934fdf9ad90f35b706f8` |
| `Vibra-beats.qxw` | `10fff86ffa3d062c982db89c97aa33a451f54fa7eb8dca0a40808d5cc6dea882` |
| `Vibra-split.qxw` | `c7f73cd621914a44f671ea02b06bc733187e14e10eca369f3f6a592f075d862e` |

**Files:**
- Create: `tests/vibra_baseline.json`
- Create: `tests/vibra_regen.py`
- Create: `tests/vibra_compare.py`
- Create: `tests/test_vibra_byte_identity.py`

**Interfaces:**
- Consumes: `qlctool.cli.main(argv: list[str] | None) -> int` (the `newshow`
  subcommand, in-process); `qlctool.checks.run.check_workspace`;
  `qlctool.validate.validate_workspace(path) -> ValidationResult` (`.ok`,
  `.errors`).
- Produces: `regenerate_vibra(out_dir: Path, use_descriptions: bool = False) -> dict[str, str]`
  (workspace file name -> sha256 of the regenerated file); the script
  `tests/vibra_compare.py [--descriptions] [--validate]` (exit 0 or 1); the
  baseline file `tests/vibra_baseline.json` (`{name: {source, plot, beats, sha256}}`;
  Task 8 adds `description`). pytest's default `prepend` import mode puts
  `tests/` on `sys.path`, which is how the test imports `vibra_regen`
  (`tests/` has no `__init__.py`).

- [ ] **Step 1: Confirm the baseline on this checkout**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git status --short   # must be clean
shasum -a 256 "QLC+ Setups/Vibra.qxw" "QLC+ Setups/Vibra-beats.qxw" "QLC+ Setups/Vibra-split.qxw"
```
Expected: the three hashes in the table above. If `main` has moved and they
differ, use the new values everywhere below (the Step 4 test proves the
regenerated files equal the shipped ones either way).

- [ ] **Step 2: Write the failing test** - `tests/test_vibra_byte_identity.py`

```python
"""The three Vibra workspaces regenerate byte for byte (2026-09-24).

The show-description refactor (docs/superpowers/specs/
2026-09-24-show-description-design.md) moves every table the generator reads.
The rule that governs it: a changed byte in Vibra.qxw, Vibra-beats.qxw or
Vibra-split.qxw is a failed step until the owner accepts the difference.
"""

import hashlib
import json
from pathlib import Path

from vibra_regen import regenerate_vibra

SETUPS = Path(__file__).resolve().parents[3] / "QLC+ Setups"
BASELINE = json.loads(Path(__file__).with_name("vibra_baseline.json").read_text(encoding="utf-8"))


def test_the_baseline_is_what_the_repository_ships():
    for name, entry in BASELINE.items():
        assert hashlib.sha256((SETUPS / name).read_bytes()).hexdigest() == entry["sha256"], name


def test_the_three_vibra_workspaces_regenerate_byte_for_byte(tmp_path):
    assert regenerate_vibra(tmp_path) == {name: entry["sha256"] for name, entry in BASELINE.items()}
```

- [ ] **Step 3: Run it and watch it fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_vibra_byte_identity.py -q -n 0
```
Expected: collection error, `FileNotFoundError: ... vibra_baseline.json` (or
`ModuleNotFoundError: No module named 'vibra_regen'`).

- [ ] **Step 4: Write the baseline, the regenerator and the compare script**

`tests/vibra_baseline.json`:

```json
{
  "Vibra.qxw": {
    "source": "Vibra.qxw",
    "plot": "vibra-stage-plot.json",
    "beats": false,
    "sha256": "10c12af24a1c72718906f77698f447998ddcdc7ef01b934fdf9ad90f35b706f8"
  },
  "Vibra-beats.qxw": {
    "source": "Vibra.qxw",
    "plot": "vibra-stage-plot.json",
    "beats": true,
    "sha256": "10fff86ffa3d062c982db89c97aa33a451f54fa7eb8dca0a40808d5cc6dea882"
  },
  "Vibra-split.qxw": {
    "source": "Vibra-split.qxw",
    "plot": "vibra-stage-plot-split.json",
    "beats": false,
    "sha256": "c7f73cd621914a44f671ea02b06bc733187e14e10eca369f3f6a592f075d862e"
  }
}
```

`tests/vibra_regen.py`:

```python
"""Regenerate the three Vibra workspaces into a directory and hash them.

The recipes are the verified ones in AGENTS.md ("Regenerating the show"), read
from vibra_baseline.json so the recipe and the hash it must produce sit side by
side. Output never touches QLC+ Setups/: the shipped files are the baseline.
"""

import hashlib
import json
from pathlib import Path

from qlctool.cli import main


def regenerate_vibra(out_dir: Path, use_descriptions: bool = False) -> dict[str, str]:
    """Workspace name -> sha256 of the file `qlctool newshow` writes for it."""
    setups = Path(__file__).resolve().parents[3] / "QLC+ Setups"
    recipes = json.loads(Path(__file__).with_name("vibra_baseline.json").read_text(encoding="utf-8"))
    hashes: dict[str, str] = {}
    for name, recipe in recipes.items():
        out = out_dir / name
        if use_descriptions:
            argv = ["newshow", "--description", str(setups / recipe["description"])]
        else:
            argv = ["newshow", str(setups / recipe["source"]), "--plot", str(setups / recipe["plot"])]
            if recipe["beats"]:
                argv.append("--beats")
        if main([*argv, "--out", str(out)]) != 0:
            raise RuntimeError(f"qlctool {' '.join(argv)} failed for {name}")
        hashes[name] = hashlib.sha256(out.read_bytes()).hexdigest()
    return hashes
```

`tests/vibra_compare.py`:

```python
"""Regenerate the three Vibra workspaces and prove nothing moved.

    cd tools/qlctool && .venv/bin/python tests/vibra_compare.py [--descriptions] [--validate]

Exit 0 only when every regenerated workspace hashes to its baseline, every
`qlctool check` rule finds nothing in it, and - with --validate - headless QLC+
loads it without a complaint. --descriptions regenerates from the .toml
descriptions (Task 8 of the show-description plan) instead of the CLI flags.
"""

import argparse
import json
import tempfile
from pathlib import Path

from vibra_regen import regenerate_vibra

from qlctool.checks.run import check_workspace
from qlctool.library import FixtureLibrary
from qlctool.validate import validate_workspace
from qlctool.workspace import Workspace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptions", action="store_true", help="regenerate from the .toml files")
    parser.add_argument("--validate", action="store_true", help="also load each in headless QLC+")
    args = parser.parse_args(argv)
    baseline = json.loads(Path(__file__).with_name("vibra_baseline.json").read_text(encoding="utf-8"))
    library = FixtureLibrary.load()
    failed = False
    with tempfile.TemporaryDirectory() as scratch:
        out_dir = Path(scratch)
        hashes = regenerate_vibra(out_dir, use_descriptions=args.descriptions)
        for name, entry in baseline.items():
            same = hashes[name] == entry["sha256"]
            findings = check_workspace(Workspace.load(out_dir / name), library)
            line = f"{name}: {'identical' if same else 'CHANGED ' + hashes[name]}, {len(findings)} finding(s)"
            failed = failed or not same or bool(findings)
            if args.validate:
                result = validate_workspace(out_dir / name)
                line += ", QLC+ loaded it" if result.ok else f", QLC+ reported {len(result.errors)} problem(s)"
                failed = failed or not result.ok
            print(line)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the test and the script**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_vibra_byte_identity.py -q -n 0
.venv/bin/qlctool install --check
.venv/bin/python tests/vibra_compare.py --validate
```
Expected: `2 passed`; `install --check` exit 0 (else run `.venv/bin/qlctool install` and repeat);
the script prints `Vibra.qxw: identical, 0 finding(s), QLC+ loaded it` and the
same for the other two, exit 0.

- [ ] **Step 6: Run the full gates** (Global Constraint 2) and
  `ruff check tests/vibra_regen.py tests/vibra_compare.py tests/test_vibra_byte_identity.py`
  plus `ruff format --check` on the same three files. Expected: suite `479 passed, 10 skipped`
  (baseline + 2), every gate exit 0.

- [ ] **Step 7: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/tests/vibra_baseline.json tools/qlctool/tests/vibra_regen.py \
  tools/qlctool/tests/vibra_compare.py tools/qlctool/tests/test_vibra_byte_identity.py
git commit -m "test(qlctool): pin the three Vibra workspaces to their bytes before the description refactor" \
  -m "The refactor that moves the show's tables into a description must not change a byte of Vibra.qxw, Vibra-beats.qxw or Vibra-split.qxw. The baseline is the committed files, which the AGENTS.md recipe reproduces exactly; tests/vibra_compare.py regenerates, compares, checks and optionally validates them." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 2: `ShowDescription` for timing, tuning, console and curated matrices

Spec step 2, first half. The constants block of `canonical_show.py` (lines
108-263, and `PRISM_STEP_HOLD_MS` at 1179) moves verbatim - comments included -
into `qlctool/vibra/`, and the generator reads a `ShowDescription` instead.
Colours follow in Task 3. Line numbers below are **before** this task's edits.

**Files:**
- Create: `qlctool/description/__init__.py`, `qlctool/description/show_timing.py`,
  `qlctool/description/fixture_tuning.py`, `qlctool/description/console_settings.py`,
  `qlctool/description/show_description.py`, `qlctool/description/matrices_by_group.py`
- Create: `qlctool/vibra/__init__.py`, `qlctool/vibra/timing.py`, `qlctool/vibra/tuning.py`,
  `qlctool/vibra/keys.py`, `qlctool/vibra/flash_functions.py`, `qlctool/vibra/console.py`,
  `qlctool/vibra/description.py`
- Create: `tests/test_show_description.py`
- Modify: `qlctool/generate/canonical_show.py` (imports; delete 108-263 and 1178-1179's
  `PRISM_STEP_HOLD_MS`; signature 281-290; sites listed in Step 4)
- Modify: `qlctool/generate/live_console.py` (signature 323-343, `_page_show` 534-545,
  `_page_control` 746-759, lines 454-464, 481-494, 530, 726, 981, `_set_canvas` 1405-1414)
- Modify imports in: `tests/test_play_generators.py:12`, `tests/test_old_show_recovery.py:15`,
  `tests/test_night_2026_08_30.py:30`, `tests/test_live_console.py:16` and `:744`,
  `tests/test_canonical_show.py:17`
- Modify: `codeality-py.toml` (`[roles] data`)

**Interfaces:**
- Produces:
  - `ShowTiming(bpm: int, ambient_ms: int, party_ms: int, peak_ms: int, dynamic_ms: int, dynamic_chase_ms: int, dynamic_pingpong_ms: int, panel_effects_ms: int, panel_manual_ms: int, prism_step_ms: int, beat_timings: Mapping[str, BeatTiming], matrix_beats: BeatTiming, beats: bool = False)` with property `beat_ms -> int` (`60_000 // bpm`).
  - `FixtureTuning(beam_focus: int, prism_spin_slow: int, strobe_fast: float, strobe_slow: float, talk_white: tuple[int, int, int])`.
  - `ConsoleSettings(canvas: tuple[int, int], keys: Mapping[str, str], flash_functions: tuple[str, ...])`.
  - `ShowDescription(matrices: Mapping[str, tuple[CuratedScript, ...]], timing: ShowTiming, tuning: FixtureTuning, console: ConsoleSettings)` (Task 3 prepends `colours`).
  - `matrices_by_group(scripts: Iterable[CuratedScript]) -> dict[str, tuple[CuratedScript, ...]]`.
  - `VIBRA_TIMING`, `VIBRA_TUNING`, `KEYS` (moved, same name), `FLASH_FUNCTIONS` (moved, same name), `VIBRA_CONSOLE`, `vibra_description() -> ShowDescription`.
  - `build_canonical_show(..., description: ShowDescription | None = None)` (new last keyword).
  - `generate_live_console(..., canvas: tuple[int, int] = (CANVAS_WIDTH, CANVAS_HEIGHT), tempo_beat_ms: int = TEMPO_BEAT_MS)`.
- Consumes: `BeatTiming` (`qlctool/generate/beat_tempo.py`), `CuratedScript` and `CURATED_MATRICES` (`qlctool/matrix_algorithms.py`).

- [ ] **Step 1: Write the failing test** - `tests/test_show_description.py`

```python
"""The show's own choices live in one description (2026-09-24, spec step 2)."""

from dataclasses import replace
from pathlib import Path

from qlctool.generate.beat_tempo import BeatTiming
from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.vibra.description import vibra_description
from qlctool.workspace import Workspace
from qlctool.xmlutil import find_local

REPO = Path(__file__).resolve().parents[3]
SHOW = REPO / "QLC+ Setups" / "Vibra.qxw"


def _generated(description):
    workspace = Workspace.load(SHOW)
    build_canonical_show(workspace, FixtureLibrary.load(), description=description)
    return workspace.root


def test_vibra_is_the_default_description():
    show = vibra_description()
    assert (show.timing.bpm, show.timing.beat_ms, show.timing.peak_ms) == (120, 500, 40_000)
    assert show.timing.beat_timings["Rueda Colores"] == BeatTiming(hold=8, fade=1)
    assert show.tuning.beam_focus == 127
    assert (show.tuning.strobe_fast, show.tuning.strobe_slow) == (0.97, 0.785)
    assert show.console.canvas == (1440, 900)
    assert show.console.keys["AUTO"] == "Q"
    assert "Escenario" in show.console.flash_functions
    assert [s.algorithm for s in show.matrices["Cabezas"]] == [
        "One By One", "Fill Unfill", "Noise", "Alternate", "Opposite", "Random Column",
    ]


def test_the_description_sets_the_console_canvas_and_the_clock():
    vibra = vibra_description()
    root = _generated(
        replace(
            vibra,
            console=replace(vibra.console, canvas=(1600, 1000)),
            timing=replace(vibra.timing, bpm=100),
        )
    )
    size = find_local(find_local(find_local(root, "VirtualConsole"), "Properties"), "Size")
    assert (size.get("Width"), size.get("Height")) == ("1600", "1000")
    generator = next(e for e in root.iter() if e.tag.endswith("}BeatGenerator"))
    assert generator.get("BPM") == "100"
```

- [ ] **Step 2: Run it and watch it fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_show_description.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.vibra'`.

- [ ] **Step 3: Create the dataclasses and Vibra's values**

`qlctool/description/__init__.py`:

```python
"""A show's own choices - palette, matrices, timing, tuning, console, controllers - apart from its patch."""
```

`qlctool/description/show_timing.py`:

```python
"""How long the night spends where, and the beat its chases count in."""

from collections.abc import Mapping
from dataclasses import dataclass

from ..generate.beat_tempo import BeatTiming


@dataclass(frozen=True)
class ShowTiming:
    """Every duration the generated show is written against: milliseconds, or beats."""

    bpm: int
    ambient_ms: int
    party_ms: int
    peak_ms: int
    dynamic_ms: int
    dynamic_chase_ms: int
    dynamic_pingpong_ms: int
    panel_effects_ms: int
    panel_manual_ms: int
    prism_step_ms: int
    beat_timings: Mapping[str, BeatTiming]
    matrix_beats: BeatTiming
    beats: bool = False

    @property
    def beat_ms(self) -> int:
        """One beat at `bpm`: what the tap dials start on and count multipliers in."""
        return 60_000 // self.bpm
```

`qlctool/description/fixture_tuning.py`:

```python
"""Values a show sets on fixture channels that no capability decides for it."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FixtureTuning:
    """Beam focus, prism spin, flash strobe speeds and the talk light's white."""

    beam_focus: int
    prism_spin_slow: int
    strobe_fast: float
    strobe_slow: float
    talk_white: tuple[int, int, int]
```

`qlctool/description/console_settings.py`:

```python
"""The console a show is operated from: its screen, its keys, its held buttons."""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ConsoleSettings:
    """Canvas size in pixels, one keyboard key per function, and the functions held not latched."""

    canvas: tuple[int, int]
    keys: Mapping[str, str]
    flash_functions: tuple[str, ...]
```

`qlctool/description/show_description.py`:

```python
"""One show, described: everything the generator used to hard-code for Vibra."""

from collections.abc import Mapping
from dataclasses import dataclass

from ..matrix_algorithms import CuratedScript
from .console_settings import ConsoleSettings
from .fixture_tuning import FixtureTuning
from .show_timing import ShowTiming


@dataclass(frozen=True)
class ShowDescription:
    """A show's choices apart from the patch, which QLC+ keeps.

    `matrices` holds each fixture group's hand-tuned RGB scripts, in the order
    that group's cycle steps them; a group the patch lacks is simply unused.
    """

    matrices: Mapping[str, tuple[CuratedScript, ...]]
    timing: ShowTiming
    tuning: FixtureTuning
    console: ConsoleSettings
```

`qlctool/description/matrices_by_group.py`:

```python
"""Curated matrix scripts, grouped by the fixture group they were tuned for."""

from collections.abc import Iterable

from ..matrix_algorithms import CuratedScript


def matrices_by_group(scripts: Iterable[CuratedScript]) -> dict[str, tuple[CuratedScript, ...]]:
    """Group name -> its scripts, each group keeping the order it was given in."""
    grouped: dict[str, list[CuratedScript]] = {}
    for script in scripts:
        grouped.setdefault(script.group_name, []).append(script)
    return {group: tuple(entries) for group, entries in grouped.items()}
```

`qlctool/vibra/__init__.py`:

```python
"""The Vibra show's own values: the default description every other show starts from."""
```

`qlctool/vibra/timing.py` - carry the comment blocks from `canonical_show.py`
verbatim above the matching fields: lines 124-128 above `ambient_ms`, 132-135
above `dynamic_ms`, 137-139 above `dynamic_chase_ms`, 143-147 above
`panel_effects_ms`, 151-157 above `beat_timings`, 159-160 above `bpm`, and the
two comment lines inside `BEAT_TIMINGS` (165-166) inside the dict:

```python
"""The Vibra night's clock: how long each level holds, and the beats its chases count."""

from ..description.show_timing import ShowTiming
from ..generate.beat_tempo import BeatTiming

VIBRA_TIMING = ShowTiming(
    bpm=120,
    ambient_ms=4 * 60 * 1000,
    party_ms=8 * 60 * 1000,
    peak_ms=40 * 1000,
    dynamic_ms=4 * 60 * 1000,
    dynamic_chase_ms=30 * 1000,
    dynamic_pingpong_ms=8 * 1000,
    panel_effects_ms=8 * 60 * 1000,
    panel_manual_ms=4 * 60 * 1000,
    prism_step_ms=8000,
    beat_timings={
        "Rueda Colores": BeatTiming(hold=8, fade=1),
        "Movimientos Suaves": BeatTiming(hold=64, fade=10),
        "Movimientos Washes": BeatTiming(hold=32, fade=10),
        "Movimientos Beams": BeatTiming(hold=32, fade=10),
        "Rapidos Washes": BeatTiming(hold=16),
        "Rapidos Beams": BeatTiming(hold=16),
        "Gobo Animacion": BeatTiming(hold=16),
        "Prisma Animacion": BeatTiming(hold=32),
        "Dimmer Chase": BeatTiming(hold=4),
        "Dimmer PingPong": BeatTiming(hold=2),
    },
    matrix_beats=BeatTiming(hold=4),
)
```

`qlctool/vibra/tuning.py` - comments from `canonical_show.py` 108-109 above
`talk_white`, 112-113 above `prism_spin_slow`, 115-121 above `beam_focus`,
250-261 above `strobe_fast`:

```python
"""Where the Vibra show sets the channels no capability decides."""

from ..description.fixture_tuning import FixtureTuning

VIBRA_TUNING = FixtureTuning(
    beam_focus=127,
    prism_spin_slow=25,
    strobe_fast=0.97,
    strobe_slow=0.785,
    talk_white=(255, 214, 170),
)
```

`qlctool/vibra/keys.py`: move `canonical_show.py` lines 178-229 (the comment
and the `KEYS = {...}` dict, unchanged) under this docstring:

```python
"""The Vibra console's keyboard: one key per function, as the owner's hands know it."""
```

`qlctool/vibra/flash_functions.py`: move `canonical_show.py` lines 230-248 (the
comment and `FLASH_FUNCTIONS = (...)`, unchanged) under:

```python
"""The Vibra functions held while pressed rather than latched."""
```

`qlctool/vibra/console.py`:

```python
"""The console the Vibra show is operated from."""

from ..description.console_settings import ConsoleSettings
from .flash_functions import FLASH_FUNCTIONS
from .keys import KEYS

# One 1440x900 screen: the show laptop's, and what live_console's layout is drawn for.
VIBRA_CONSOLE = ConsoleSettings(canvas=(1440, 900), keys=KEYS, flash_functions=FLASH_FUNCTIONS)
```

`qlctool/vibra/description.py`:

```python
"""The Vibra show as a description: the default the generator falls back to."""

from ..description.matrices_by_group import matrices_by_group
from ..description.show_description import ShowDescription
from ..matrix_algorithms import CURATED_MATRICES
from .console import VIBRA_CONSOLE
from .timing import VIBRA_TIMING
from .tuning import VIBRA_TUNING


def vibra_description() -> ShowDescription:
    """Today's Vibra values, exactly as the generator used to hard-code them."""
    return ShowDescription(
        matrices=matrices_by_group(CURATED_MATRICES),
        timing=VIBRA_TIMING,
        tuning=VIBRA_TUNING,
        console=VIBRA_CONSOLE,
    )
```

- [ ] **Step 4: Make the generator read the description**

`qlctool/generate/canonical_show.py`:
- Imports: delete `from ..matrix_algorithms import CURATED_MATRICES`; add
  `from ..description.show_description import ShowDescription` and
  `from ..vibra.description import vibra_description` (isort order).
- Delete lines 108-263 (moved in Step 3) and line 1179 `PRISM_STEP_HOLD_MS = 8000`.
  Keep 97-106 (`SHOW_PATH`, `MATRIX_ALGORITHMS`, `CYCLE_ALGORITHMS`, `MATRIX_COLORS`).
- Signature (281-290): add a last parameter `description: ShowDescription | None = None`.
- First statements of the body, before `strip_to_skeleton(workspace)`:
  ```python
      described = description if description is not None else vibra_description()
      beats = beats or described.timing.beats
  ```
- Replace, keeping everything else on each line:
  - 343 `strobe=FLASH_STROBE_FAST` -> `strobe=described.tuning.strobe_fast`
  - 351 `strobe=FLASH_STROBE_SLOW` -> `strobe=described.tuning.strobe_slow`
  - 355 `fraction=FLASH_STROBE_FAST` -> `fraction=described.tuning.strobe_fast`
  - 360 `FLASH_STROBE_FAST,` -> `described.tuning.strobe_fast,`
  - 390 `holds=[PANEL_EFFECTS_HOLD, PANEL_MANUAL_HOLD],` -> `holds=[described.timing.panel_effects_ms, described.timing.panel_manual_ms],`
  - 439 `curated=[c for c in CURATED_MATRICES if c.group_name == group.name],` -> `curated=list(described.matrices.get(group.name, ())),`
  - 536, 544, 553: every `BEAM_FOCUS` -> `described.tuning.beam_focus`
  - 596 `PRISM_SPIN_SLOW` -> `described.tuning.prism_spin_slow`
  - 602-607: add `hold=described.timing.prism_step_ms,` as the last argument of `_prism_choreography(...)`
  - 866 `holds=[DYNAMIC_CHASE_HOLD, DYNAMIC_PINGPONG_HOLD],` -> `holds=[described.timing.dynamic_chase_ms, described.timing.dynamic_pingpong_ms],`
  - 894 `AMBIENT_HOLD,` -> `described.timing.ambient_ms,`; 914 `PARTY_HOLD,` -> `described.timing.party_ms,`; 929 `PEAK_HOLD,` -> `described.timing.peak_ms,`; 947 `DYNAMIC_HOLD,` -> `described.timing.dynamic_ms,`
  - 984 `CHARLA_WHITE,` -> `described.tuning.talk_white,`
  - 1099 `bpm=0 if beats else DEFAULT_BPM,` -> `bpm=0 if beats else described.timing.bpm,`
  - 1101 `_tempo_functions(workspace, master, matrices)` -> `_tempo_functions(workspace, master, matrices, described.timing.beat_ms)`
  - 1102 `_movement_tempo_functions(workspace)` -> `_movement_tempo_functions(workspace, described.timing.beat_ms)`
  - 1114 `BEAT_TIMINGS.items()` -> `described.timing.beat_timings.items()`
  - 1118 `MATRIX_BEATS` -> `described.timing.matrix_beats`
  - 1135 `keys=KEYS,` -> `keys=dict(described.console.keys),`
  - 1136 `flash_functions=FLASH_FUNCTIONS,` -> `flash_functions=described.console.flash_functions,` and add two arguments after `colour_flash_ids=color_flashes.ids,`:
    `canvas=described.console.canvas,` and `tempo_beat_ms=described.timing.beat_ms,`
  - `_prism_choreography` (1182): add parameter `hold: int` after `extra_step_ids`; 1214 `hold=PRISM_STEP_HOLD_MS,` -> `hold=hold,`
  - `_movement_tempo_functions` (1264): signature `(workspace, beat_ms: int)`; 1297, 1298, 1310: `TAP_BEAT_MS` -> `beat_ms`
  - `_tempo_functions` (1315): signature `(workspace, master, matrices, beat_ms: int)`; 1354: `TAP_BEAT_MS` -> `beat_ms`

`qlctool/generate/live_console.py`:
- `generate_live_console` signature: after `colour_flash_ids: dict[str, int] | None = None,` add
  `canvas: tuple[int, int] = (CANVAS_WIDTH, CANVAS_HEIGHT),` and `tempo_beat_ms: int = TEMPO_BEAT_MS,`.
- 454-464 `_page_show(...)`: append argument `tempo_beat_ms`; its definition (534-544) gains a last parameter `tempo_beat_ms`; 726 `time_ms=TEMPO_BEAT_MS,` -> `time_ms=tempo_beat_ms,`.
- 481-494 `_page_control(...)`: append argument `tempo_beat_ms`; its definition (746-759) gains a last parameter `tempo_beat_ms`; 981 `time_ms=TEMPO_BEAT_MS,` -> `time_ms=tempo_beat_ms,`.
- 530 `_set_canvas(workspace.root)` -> `_set_canvas(workspace.root, canvas)`; `_set_canvas` (1405) becomes `def _set_canvas(root: etree._Element, canvas: tuple[int, int]) -> None:` and its last two lines `size.set("Width", str(canvas[0]))`, `size.set("Height", str(canvas[1]))`.

Tests that imported moved constants:
- `tests/test_play_generators.py:12` -> `from qlctool.generate.canonical_show import build_canonical_show` plus `from qlctool.vibra.tuning import VIBRA_TUNING`; line 306 `FLASH_STROBE_FAST` -> `VIBRA_TUNING.strobe_fast`.
- `tests/test_night_2026_08_30.py:30` -> `from qlctool.generate.canonical_show import build_canonical_show` plus `from qlctool.vibra.tuning import VIBRA_TUNING`; line 154 `BEAM_FOCUS` -> `VIBRA_TUNING.beam_focus`.
- `tests/test_old_show_recovery.py:15`, `tests/test_live_console.py:16`, `tests/test_canonical_show.py:17` -> `from qlctool.generate.canonical_show import build_canonical_show` plus `from qlctool.vibra.keys import KEYS`; `tests/test_live_console.py:744` -> `from qlctool.vibra.keys import KEYS`.

`codeality-py.toml`, `[roles] data`: add `"qlctool/vibra/timing.py"`, `"qlctool/vibra/tuning.py"`,
`"qlctool/vibra/keys.py"`, `"qlctool/vibra/flash_functions.py"`, `"qlctool/vibra/console.py"`.

- [ ] **Step 5: Run the new test**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_show_description.py -q -n 0
```
Expected: `2 passed`.

- [ ] **Step 6: Gates** - Global Constraint 2 commands, plus `ruff check` and
  `ruff format --check` on every `.py` created or modified in this task.
  Expected: suite `481 passed, 10 skipped`; `vibra_compare.py --validate` three
  `identical` lines; three checks exit 0.

- [ ] **Step 7: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/description tools/qlctool/qlctool/vibra \
  tools/qlctool/qlctool/generate/canonical_show.py tools/qlctool/qlctool/generate/live_console.py \
  tools/qlctool/tests/test_show_description.py tools/qlctool/tests/test_play_generators.py \
  tools/qlctool/tests/test_old_show_recovery.py tools/qlctool/tests/test_night_2026_08_30.py \
  tools/qlctool/tests/test_live_console.py tools/qlctool/tests/test_canonical_show.py \
  tools/qlctool/codeality-py.toml
git commit -m "refactor(qlctool): hold the show's timing, tuning and console in a ShowDescription" \
  -m "The constants canonical_show.py hard-coded for Vibra - the energy levels, beat timings, BPM, beam focus, prism spin, flash strobe speeds, talk white, keys, held functions, canvas and curated matrices - move verbatim into qlctool/vibra/ and reach the generator through a ShowDescription whose default is vibra_description(). The three Vibra workspaces regenerate byte for byte." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 3: The description's colours reach every generator that read the palette

Spec step 2, second half: palette, primaries, simple colours, white, the three
pair tables and the matrix colours become `ShowDescription.colours`, and every
generator `newshow` runs that imported `PALETTE`, `WHEEL_PALETTE`,
`KEY_SPLIT_PAIRS` or `CONTRAST_PAIRS` receives them as arguments (module
constants stay as the defaults, so `qlctool palette`/`matrix`/`layout` are
untouched). Line numbers are before this task's edits, after Task 2's.
Re-locate by the quoted text, not by number.

**Files:**
- Create: `qlctool/description/colour_settings.py`, `qlctool/description/wheel_palette_of.py`,
  `qlctool/description/pastel_palette_of.py`, `qlctool/description/split_pairs_of.py`,
  `qlctool/description/contrast_pairs_of.py`, `qlctool/vibra/matrix_colors.py`, `qlctool/vibra/colours.py`
- Modify: `qlctool/description/show_description.py`, `qlctool/vibra/description.py`,
  `qlctool/generate/canonical_show.py`, `qlctool/generate/color_banks.py`,
  `qlctool/generate/matrix_effects.py`, `qlctool/generate/quad_color_scenes.py`,
  `qlctool/generate/live_console.py`, `qlctool/generate/play_page.py`,
  `tests/test_show_description.py`, `codeality-py.toml`

**Interfaces:**
- Produces:
  - `ColourSettings(palette: Mapping[str, RGB], primary: tuple[str, ...], simple: tuple[str, ...], white: str, analogous_pairs: tuple[ColorPair, ...], key_split_pairs: tuple[tuple[str, str], ...], complementary_pairs: tuple[ColorPair, ...], matrix_colors: tuple[str, ...])`.
  - `ShowDescription.colours: ColourSettings` (first field).
  - `wheel_palette_of(colours) -> dict[str, RGB]`, `pastel_palette_of(colours) -> dict[str, RGB]`, `split_pairs_of(colours) -> tuple[tuple[str, str], ...]`, `contrast_pairs_of(colours) -> tuple[tuple[str, str], ...]` - each equal to today's `WHEEL_PALETTE`, `PASTEL_PALETTE`, `SPLIT_PAIRS`, `CONTRAST_PAIRS` for Vibra.
  - `VIBRA_COLOURS`, `MATRIX_COLORS` (moved to `qlctool/vibra/matrix_colors.py`).
  - New keyword parameters (all defaulting to today's module constants):
    `generate_color_banks(..., palette: Mapping[str, RGB] | None = None, wheel_palette: Mapping[str, RGB] | None = None, key_split_pairs: Sequence[tuple[str, str]] = KEY_SPLIT_PAIRS)`;
    `generate_matrix_effects(..., curated_palette: Mapping[str, RGB] | None = None)`;
    `generate_quad_color_scenes(..., palette: Mapping[str, RGB] | None = None)`;
    `generate_live_console(..., palette: Mapping[str, RGB] | None = None)`;
    `build_play_page(..., palette: Mapping[str, RGB] | None = None)`.
  - `build_canonical_show(..., matrix_colors: Sequence[str] | None = None, ...)` (default was `MATRIX_COLORS`).
- Consumes: `PALETTE`, `PRIMARY_COLORS` (`palette.py`), `SIMPLE_COLORS`, `WHITE`
  (`wheel_palette.py`), `ANALOGOUS_PAIRS`, `KEY_SPLIT_PAIRS`, `COMPLEMENTARY_PAIRS`,
  `ColorPair`, `pastel`, `RGB` (`argb.py`).

- [ ] **Step 1: Write the failing tests** - append to `tests/test_show_description.py`
  (add the imports at the top of the file):

```python
from qlctool.argb import argb_from_rgb
from qlctool.description.contrast_pairs_of import contrast_pairs_of
from qlctool.description.pastel_palette_of import pastel_palette_of
from qlctool.description.split_pairs_of import split_pairs_of
from qlctool.description.wheel_palette_of import wheel_palette_of
from qlctool.generate.unison_colors import CONTRAST_PAIRS
from qlctool.pastel_palette import PASTEL_PALETTE
from qlctool.split_pairs import SPLIT_PAIRS
from qlctool.wheel_palette import WHEEL_PALETTE


def test_the_derived_colour_tables_are_todays():
    colours = vibra_description().colours
    assert list(wheel_palette_of(colours).items()) == list(WHEEL_PALETTE.items())
    assert list(pastel_palette_of(colours).items()) == list(PASTEL_PALETTE.items())
    assert split_pairs_of(colours) == SPLIT_PAIRS
    assert contrast_pairs_of(colours) == CONTRAST_PAIRS


def test_the_description_palette_colours_the_matrices():
    vibra = vibra_description()
    colours = replace(
        vibra.colours,
        palette={**vibra.colours.palette, "Rojo": (250, 0, 0)},
        matrix_colors=("Rojo",),
    )
    root = _generated(replace(vibra, colours=colours))
    bars = [
        f for f in root.iter()
        if f.tag.endswith("}Function") and f.get("Path") == "Matrices BarrasLed"
    ]
    names = [f.get("Name") for f in bars]
    assert "BarrasLed - Fill Rojo" in names
    assert "BarrasLed - Fill Verde" not in names
    red = str(argb_from_rgb((250, 0, 0)))
    assert any(e.text == red for f in bars for e in f.iter())
```

- [ ] **Step 2: Run them and watch them fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_show_description.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.description.contrast_pairs_of'`.

- [ ] **Step 3: Create the colour settings and the derived tables**

`qlctool/description/colour_settings.py`:

```python
"""A show's colours: the palette and every subset and pairing drawn from it."""

from collections.abc import Mapping
from dataclasses import dataclass

from ..argb import RGB
from ..color_pair import ColorPair


@dataclass(frozen=True)
class ColourSettings:
    """The palette, which of its colours each mode uses, and which pairs go together.

    `white` is the palette entry no automatic rotation steps (`wheel_palette`);
    `analogous_pairs` and `key_split_pairs` build the per-group splits,
    `complementary_pairs` the heads-against-the-rest contrasts.
    """

    palette: Mapping[str, RGB]
    primary: tuple[str, ...]
    simple: tuple[str, ...]
    white: str
    analogous_pairs: tuple[ColorPair, ...]
    key_split_pairs: tuple[tuple[str, str], ...]
    complementary_pairs: tuple[ColorPair, ...]
    matrix_colors: tuple[str, ...]
```

`qlctool/description/wheel_palette_of.py`:

```python
"""The palette a rotation may step by itself: all of it but white (`wheel_palette`)."""

from ..argb import RGB
from .colour_settings import ColourSettings


def wheel_palette_of(colours: ColourSettings) -> dict[str, RGB]:
    """Every palette colour except the show's white, in palette order."""
    return {name: rgb for name, rgb in colours.palette.items() if name != colours.white}
```

`qlctool/description/pastel_palette_of.py`:

```python
"""The wheel palette taken towards white, for the pastel mode (`pastel_palette`)."""

from ..argb import RGB
from ..pastel import pastel
from .colour_settings import ColourSettings
from .wheel_palette_of import wheel_palette_of


def pastel_palette_of(colours: ColourSettings) -> dict[str, RGB]:
    """Same names and hues as the wheel palette, each blended towards white."""
    return {name: pastel(rgb) for name, rgb in wheel_palette_of(colours).items()}
```

`qlctool/description/split_pairs_of.py`:

```python
"""What a per-group mix wheel steps: neighbours both ways round, plus the keys (`split_pairs`)."""

from .colour_settings import ColourSettings


def split_pairs_of(colours: ColourSettings) -> tuple[tuple[str, str], ...]:
    """Analogous pairs lead-first, then bed-first, then the key splits, without repeats."""
    return tuple(
        dict.fromkeys(
            [
                *((pair.lead, pair.bed) for pair in colours.analogous_pairs),
                *((pair.bed, pair.lead) for pair in colours.analogous_pairs),
                *colours.key_split_pairs,
            ]
        )
    )
```

`qlctool/description/contrast_pairs_of.py`:

```python
"""The heads-against-the-rest contrasts a rotation steps (`unison_colors.CONTRAST_PAIRS`)."""

from .colour_settings import ColourSettings


def contrast_pairs_of(colours: ColourSettings) -> tuple[tuple[str, str], ...]:
    """(heads, rest) for every complementary pair, the warm lead on the heads."""
    return tuple((pair.lead, pair.bed) for pair in colours.complementary_pairs)
```

`qlctool/vibra/matrix_colors.py`: move `canonical_show.py`'s comment and
`MATRIX_COLORS = ("Rojo", "Verde", "Azul", "Ambar", "Magenta", "Cyan")`
(lines 104-106) here, under the docstring
`"""The colours every Vibra fixture group's base matrices are drawn in."""`.

`qlctool/vibra/colours.py`:

```python
"""The Vibra show's colours, from the tables its owner's choices are recorded in."""

from ..analogous_pairs import ANALOGOUS_PAIRS
from ..complementary_pairs import COMPLEMENTARY_PAIRS
from ..description.colour_settings import ColourSettings
from ..key_split_pairs import KEY_SPLIT_PAIRS
from ..palette import PALETTE, PRIMARY_COLORS
from ..simple_colors import SIMPLE_COLORS
from ..wheel_palette import WHITE
from .matrix_colors import MATRIX_COLORS

VIBRA_COLOURS = ColourSettings(
    palette=PALETTE,
    primary=PRIMARY_COLORS,
    simple=SIMPLE_COLORS,
    white=WHITE,
    analogous_pairs=ANALOGOUS_PAIRS,
    key_split_pairs=KEY_SPLIT_PAIRS,
    complementary_pairs=COMPLEMENTARY_PAIRS,
    matrix_colors=MATRIX_COLORS,
)
```

`qlctool/description/show_description.py`: import `from .colour_settings import ColourSettings`
and add `colours: ColourSettings` as the **first** field. `qlctool/vibra/description.py`:
import `from .colours import VIBRA_COLOURS` and pass `colours=VIBRA_COLOURS` first.
`codeality-py.toml` `[roles] data`: add `"qlctool/vibra/matrix_colors.py"`, `"qlctool/vibra/colours.py"`.

- [ ] **Step 4: Thread the colours through the generators**

`qlctool/generate/color_banks.py`:
- Add `from collections.abc import Mapping` and `from ..argb import RGB`.
- `generate_color_banks` gains, after `exclude_effect_mode_fixture_ids`:
  `palette: Mapping[str, RGB] | None = None, wheel_palette: Mapping[str, RGB] | None = None, key_split_pairs: Sequence[tuple[str, str]] = KEY_SPLIT_PAIRS,`.
  Before the loop: `values_of = PALETTE if palette is None else palette` and
  `wheel_of = WHEEL_PALETTE if wheel_palette is None else wheel_palette`; pass
  `values_of, wheel_of, key_split_pairs` as three new last positional arguments
  of `_bank_for_group`, whose signature gains `values_of: Mapping[str, RGB], wheel_of: Mapping[str, RGB], key_split_pairs: Sequence[tuple[str, str]]`.
- In `_bank_for_group`: `PALETTE[name]` -> `values_of[name]`; `PALETTE[first]` -> `values_of[first]`;
  `PALETTE[second]` -> `values_of[second]`; `if name in WHEEL_PALETTE:` -> `if name in wheel_of:`;
  both `KEY_SPLIT_PAIRS` in the key-splits block -> `key_split_pairs`.

`qlctool/generate/matrix_effects.py`: add `from collections.abc import Mapping` if
absent; `generate_matrix_effects` gains a last parameter
`curated_palette: Mapping[str, RGB] | None = None`; above `for entry in curated:` add
`curated_colors = PALETTE if curated_palette is None else curated_palette` and use it
for `PALETTE[entry.colors[0]]` and `PALETTE[entry.colors[1]]`.

`qlctool/generate/quad_color_scenes.py`: add `from collections.abc import Mapping`
and `from ..argb import RGB`; `generate_quad_color_scenes` gains a last parameter
`palette: Mapping[str, RGB] | None = None`; first body line
`values_of = PALETTE if palette is None else palette`; `PALETTE[name]` -> `values_of[name]`.

`qlctool/generate/play_page.py`: `build_play_page` gains a last parameter
`palette: Mapping[str, tuple[int, int, int]] | None = None`; its call of
`_build_colour_hits(...)` (line 88) appends the argument
`PALETTE if palette is None else palette`; `_build_colour_hits` gains a last
parameter `palette: Mapping[str, tuple[int, int, int]]` and `PALETTE[colour_name]` -> `palette[colour_name]`.

`qlctool/generate/live_console.py`:
- `generate_live_console` gains `palette: Mapping[str, tuple[int, int, int]] | None = None,`
  (after `tempo_beat_ms`); first body line `colours = PALETTE if palette is None else palette`.
- `build_play_page(...)` call (466-480): append `palette=colours`.
- `_page_control(...)` and `_page_library(...)` calls: append argument `colours`; both
  definitions gain a last parameter `palette`.
- `_swatch` (1360): `def _swatch(name: str, palette: Mapping[str, tuple[int, int, int]], second: bool = False) -> str:`
  and both `PALETTE` inside it -> `palette`. Call sites 819-820 and 1069-1070:
  `_swatch(name)` -> `_swatch(name, palette)`, `_swatch(name, second=True)` -> `_swatch(name, palette, second=True)`.
- Add `from collections.abc import Mapping, Sequence` (replacing the `Sequence`-only import).

`qlctool/generate/canonical_show.py`:
- Imports: delete `PALETTE, PRIMARY_COLORS` (palette), `PASTEL_PALETTE`,
  `SIMPLE_COLORS`, `WHEEL_PALETTE`, and `CONTRAST_PAIRS` from the
  `.unison_colors` import; delete the `MATRIX_COLORS` constant and its comment
  (moved); add `from collections.abc import Mapping` and imports of
  `contrast_pairs_of`, `pastel_palette_of`, `wheel_palette_of`, `split_pairs_of`.
- Signature: `matrix_colors: Sequence[str] | None = None,`.
- After `described = ...` add:
  ```python
      colours = described.colours
      wheel = wheel_palette_of(colours)
      pastels = pastel_palette_of(colours)
      contrasts = contrast_pairs_of(colours)
  ```
- `{name: PALETTE[name] for name in PRIMARY_COLORS},` -> `{name: colours.palette[name] for name in colours.primary},`
- `generate_color_banks(workspace, library, exclude_effect_mode_fixture_ids=builtins.fixture_ids,)` gains
  `colors=colours.primary, split_pairs=split_pairs_of(colours), palette=colours.palette, wheel_palette=wheel, key_split_pairs=colours.key_split_pairs,`.
- `subset = {name: PALETTE[name] for name in matrix_colors}` ->
  `subset = {name: colours.palette[name] for name in (colours.matrix_colors if matrix_colors is None else matrix_colors)}`.
- `generate_matrix_effects(...)` gains `curated_palette=colours.palette,`.
- Every `_wheel_colors()` (three calls) -> `_wheel_colors(wheel, contrasts)`;
  `{name: PASTEL_PALETTE[name] for name in _wheel_colors(...)}` -> `{name: pastels[name] for name in _wheel_colors(wheel, contrasts)}`.
- `generate_quad_color_scenes(...)` gains `palette=colours.palette,`.
- First `generate_unison_colors` (the rig wheel): `colors=tuple(WHEEL_PALETTE),` -> `colors=tuple(wheel),` and add `contrasts=contrasts, palette=dict(colours.palette),`.
- Second (`wheel_name="Rueda Simples"`): `colors=SIMPLE_COLORS,` -> `colors=colours.simple,` and add `palette=dict(colours.palette),`.
- Third (`wheel_name="Rueda Pastel"`): `colors=tuple(PASTEL_PALETTE),` -> `colors=tuple(pastels),`; `palette=PASTEL_PALETTE,` -> `palette=pastels,`.
- `generate_live_console(...)` gains `palette=colours.palette,`.
- `_wheel_colors` definition:
  ```python
  def _wheel_colors(
      wheel: Mapping[str, tuple[int, int, int]], contrasts: Sequence[tuple[str, str]]
  ) -> dict[str, tuple[int, int, int]]:
  ```
  body: keep the docstring and comments; `names = list(wheel)`;
  `names += [rest for _, rest in contrasts if rest not in names]`;
  `return {name: wheel[name] for name in names}`.

- [ ] **Step 5: Run the tests**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_show_description.py -q -n 0
```
Expected: `4 passed`.

- [ ] **Step 6: Gates** - Global Constraint 2 plus ruff on touched files.
  Expected: `483 passed, 10 skipped`; three `identical`; checks exit 0.

- [ ] **Step 7: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/description tools/qlctool/qlctool/vibra \
  tools/qlctool/qlctool/generate/canonical_show.py tools/qlctool/qlctool/generate/color_banks.py \
  tools/qlctool/qlctool/generate/matrix_effects.py tools/qlctool/qlctool/generate/quad_color_scenes.py \
  tools/qlctool/qlctool/generate/live_console.py tools/qlctool/qlctool/generate/play_page.py \
  tools/qlctool/tests/test_show_description.py tools/qlctool/codeality-py.toml
git commit -m "refactor(qlctool): pass the description's colours to every generator that read the palette" \
  -m "Palette, primaries, simple colours, white, the analogous, key-split and complementary pairs and the matrix colours become ShowDescription.colours. The colour banks, curated matrices, four-colour deal, unison wheels, console swatches and colour hits take them as arguments instead of importing the Vibra tables, which stay as the defaults for the standalone commands." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 4: English and Spanish catalogues, and the `Names` resolver

Spec step 3, first half. Pure addition: nothing in the generator uses it yet.

**Files:**
- Create: `qlctool/locales/es.toml`, `qlctool/locales/en.toml`
- Create: `qlctool/names/__init__.py`, `qlctool/names/sections.py`,
  `qlctool/names/identifier_pattern.py`, `qlctool/names/catalogue_dir.py`,
  `qlctool/names/load_catalogue.py`, `qlctool/names/shipped_languages.py`,
  `qlctool/names/name_resolution_error.py`, `qlctool/names/names.py`,
  `qlctool/names/shipped_names.py`, `qlctool/names/default_names.py`
- Create: `tests/test_names.py`, `tests/test_catalogue_vocabulary.py`
- Modify: `pyproject.toml` (`[tool.setuptools.package-data]`)

**Interfaces:**
- Produces:
  - Catalogue files: TOML with sections `[colors]`, `[functions]`, `[frames]`, `[captions]`; keys are identifiers (`^[a-z][a-z0-9_]*$`, unique across all sections), values display names. Every shipped catalogue has the same identifiers in the same order.
  - `SECTIONS: tuple[str, ...] = ("colors", "functions", "frames", "captions")`.
  - `load_catalogue(language: str) -> dict[str, dict[str, str]]` (cached; callers must not mutate).
  - `shipped_languages() -> tuple[str, ...]` (sorted stems of `qlctool/locales/*.toml`).
  - `class NameResolutionError(ValueError)`.
  - `Names(language: str, catalogues: Mapping[str, Mapping[str, Mapping[str, str]]], overrides: Mapping[str, Mapping[str, str]] = {})` with
    `identifiers(section) -> tuple[str, ...]`, `display(identifier) -> str`,
    `spellings(identifier) -> tuple[str, ...]`, `lookup(name, sections) -> tuple[str, ...]`,
    `identify(name, sections) -> str` (raises `NameResolutionError` listing close matches, or every match when ambiguous).
  - `shipped_names(language: str = "es", overrides: Mapping[str, Mapping[str, str]] | None = None) -> Names`; `default_names() -> Names` (cached `shipped_names()`).
- Consumes: the generator constants the drift test pins: `ROOM_FRAME`, `HITS_FRAME`,
  `SMOKE_FRAME`, `CHASES_FRAME`, `SMOKE_LIGHT_CAPTION`, `HITS` (`generate/live_console.py`),
  `COLOR_HITS_FRAME`, `FAMILY_FRAMES`, `PICK_PREFIX` (`generate/play_page.py`),
  `BURST_FRAME`, `split_caption` (`desk_policy.py`), `PALETTE`, `KEYS`, `FLASH_FUNCTIONS`, `VIBRA_TIMING`.

- [ ] **Step 1: Write the failing tests**

`tests/test_names.py`:

```python
"""Names in any shipped language resolve to one stable identifier (2026-09-24, spec step 3)."""

import pytest

from qlctool.names.load_catalogue import load_catalogue
from qlctool.names.name_resolution_error import NameResolutionError
from qlctool.names.names import Names
from qlctool.names.sections import SECTIONS
from qlctool.names.shipped_languages import shipped_languages
from qlctool.names.shipped_names import shipped_names


def test_english_and_spanish_ship():
    assert {"en", "es"} <= set(shipped_languages())


@pytest.mark.parametrize("spelling", ["red", "Red", "rojo", "Rojo", "ROJO", " rojo "])
def test_a_colour_is_the_same_colour_in_any_language(spelling):
    assert shipped_names().identify(spelling, ("colors",)) == "red"


def test_the_show_language_picks_the_display_name():
    assert shipped_names("es").display("party_moment") == "Momento Fiesta"
    assert shipped_names("en").display("party_moment") == "Party Moment"


def test_a_description_overrides_one_display_name():
    names = shipped_names("es", {"es": {"party_moment": "Fiestón"}})
    assert names.display("party_moment") == "Fiestón"
    assert names.identify("fiestón", ("functions",)) == "party_moment"
    assert names.display("calm_moment") == "Momento Tranquilo"


def test_an_unknown_name_lists_the_close_matches():
    with pytest.raises(NameResolutionError, match="Rojo"):
        shipped_names().identify("Roja", ("colors",))


def test_an_ambiguous_name_lists_every_match():
    names = Names(language="xx", catalogues={"xx": {"colors": {"dawn": "Alba", "dusk": "alba"}}})
    with pytest.raises(NameResolutionError, match="dawn, dusk"):
        names.identify("ALBA", ("colors",))


def test_an_unknown_language_is_refused():
    with pytest.raises(NameResolutionError, match="shipped"):
        shipped_names("fr")


@pytest.mark.parametrize("language", ["en", "es"])
def test_every_catalogue_carries_the_same_identifiers(language):
    reference = {section: list(entries) for section, entries in load_catalogue("en").items()}
    assert {s: list(e) for s, e in load_catalogue(language).items()} == reference
    assert tuple(reference) == SECTIONS


def test_an_identifier_lives_in_one_section_only():
    seen = [identifier for entries in load_catalogue("en").values() for identifier in entries]
    assert len(seen) == len(set(seen))


def test_no_shipped_spelling_names_two_identifiers():
    names = shipped_names()
    for section in SECTIONS:
        for identifier in names.identifiers(section):
            for spelling in names.spellings(identifier):
                assert names.lookup(spelling, (section,)) == (identifier,), spelling
```

`tests/test_catalogue_vocabulary.py`:

```python
"""The Spanish catalogue is exactly the vocabulary the generator writes (2026-09-24).

Until the generators take their names from the catalogue (the next plan), the
Spanish strings exist twice - here and in the generator. This pins them together
so neither can drift without the suite failing.
"""

from qlctool.desk_policy import BURST_FRAME, split_caption
from qlctool.generate.live_console import (
    CHASES_FRAME,
    HITS,
    HITS_FRAME,
    ROOM_FRAME,
    SMOKE_FRAME,
    SMOKE_LIGHT_CAPTION,
)
from qlctool.generate.play_page import COLOR_HITS_FRAME, FAMILY_FRAMES, PICK_PREFIX
from qlctool.names.load_catalogue import load_catalogue
from qlctool.palette import PALETTE
from qlctool.vibra.flash_functions import FLASH_FUNCTIONS
from qlctool.vibra.keys import KEYS
from qlctool.vibra.timing import VIBRA_TIMING

SPANISH = load_catalogue("es")
HIT_IDS = (
    "hit_flash", "hit_flash_slow", "hit_flash_colour", "hit_smoke_now",
    "hit_vertical_smoke_now", "hit_strobe", "hit_strobe_soft",
)


def test_the_spanish_colours_are_the_palette_in_order():
    assert list(SPANISH["colors"].values()) == list(PALETTE)


def test_every_function_the_vibra_tables_name_is_catalogued():
    named = set(KEYS) | set(FLASH_FUNCTIONS) | set(VIBRA_TIMING.beat_timings)
    assert named <= set(SPANISH["functions"].values())


def test_the_spanish_frames_are_the_captions_the_console_writes():
    frames = SPANISH["frames"]
    assert frames["room_states"] == ROOM_FRAME
    assert frames["hits"] == HITS_FRAME
    assert frames["haze"] == SMOKE_FRAME
    assert frames["intensity_chases"] == CHASES_FRAME
    assert frames["colour_hits"] == COLOR_HITS_FRAME
    assert frames["desk_bursts"] == BURST_FRAME
    families = ("colour", "pixels", "heads", "gobos", "prism")
    assert [frames[f"family_{family}"] for family in families] == list(FAMILY_FRAMES)


def test_the_spanish_captions_are_the_console_hits():
    captions = SPANISH["captions"]
    assert [split_caption(caption)[0] for _, caption in HITS] == [captions[i] for i in HIT_IDS]
    assert captions["vertical_smoke_light"] == SMOKE_LIGHT_CAPTION
    assert captions["pick_prefix"] == PICK_PREFIX
```

- [ ] **Step 2: Run them and watch them fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_names.py tests/test_catalogue_vocabulary.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.names'`.

- [ ] **Step 3: Write the catalogues**

`qlctool/locales/es.toml`:

```toml
# Spanish display names: the vocabulary the Vibra show's operator reads.
# Keys are stable English snake-case identifiers; every catalogue carries the
# same ones in the same order. A new language is a new file beside this one.

[colors]
red = "Rojo"
fire_red = "Rojo Fuego"
orange = "Naranja"
amber = "Ambar"
yellow = "Amarillo"
green = "Verde"
mint_green = "Verde Menta"
cyan = "Cyan"
light_blue = "Celeste"
sky_blue = "Azul Cielo"
blue = "Azul"
deep_blue = "Azul Profundo"
purple = "Morado"
ultraviolet = "UltraVioleta"
magenta = "Magenta"
fuchsia = "Fucsia"
pink = "Rosa"
white = "Blanco"

[functions]
auto = "AUTO"
talk_moment = "Momento Charla"
calm_moment = "Momento Tranquilo"
party_moment = "Momento Fiesta"
frenzy_moment = "Momento Locura"
full_white = "Blanco Total"
all_black = "Todo Negro"
flash_full = "Flash 100%"
flash_half = "Flash 50%"
flash_colour = "Flash Color"
smoke_on = "Humo ON"
vertical_smoke_now = "Humo Vertical YA"
strobe_fast = "Strobo Rapido"
strobe_medium = "Strobo Medio"
colour_wheel = "Rueda Colores"
simple_wheel = "Rueda Simples"
pastel_wheel = "Rueda Pastel"
multicolour_wheel = "Rueda Multicolor"
mix_wheel = "Rueda Mezcla"
head_movements = "Movimientos Cabezas"
gobo_animation = "Gobo Animacion"
prism_animation = "Prisma Animacion"
rainbow_together = "Arcoiris Simultaneo"
rainbow_steps = "Arcoiris Pasos"
smoke_auto = "Humo Auto"
vertical_smoke = "Humo Vertical"
dimmer_chase = "Dimmer Chase"
dimmer_chase_2 = "Dimmer Chase 2"
dimmer_sequence = "Dimmer Secuencia"
dimmer_pingpong = "Dimmer PingPong"
strobe_on = "Strobo ON"
strobe_off = "Strobo OFF"
bass_hit = "Golpe Graves"
stage_aim = "Escenario"
soft_movements = "Movimientos Suaves"
wash_movements = "Movimientos Washes"
beam_movements = "Movimientos Beams"
fast_washes = "Rapidos Washes"
fast_beams = "Rapidos Beams"

[frames]
room_states = "LA SALA ESTÁ ASÍ — solo una a la vez"
hits = "GOLPES — se suman a lo que ya está sonando"
haze = "HUMO AMBIENTE — cada cuánto dispara solo"
intensity_chases = "Intensidad y strobo de fixture"
colour_hits = "GOLPES DE COLOR — mantén pulsado"
family_colour = "COLOR"
family_pixels = "PIXELES"
family_heads = "CABEZAS"
family_gobos = "GOBOS"
family_prism = "PRISMA"
desk_bursts = "Ráfagas del desk"

[captions]
vertical_smoke_light = "HUMO VERTICAL — su luz · N"
pick_prefix = "Jugar · "
hit_flash = "FLASH"
hit_flash_slow = "FLASH LENTO"
hit_flash_colour = "FLASH COLOR"
hit_smoke_now = "HUMO YA"
hit_vertical_smoke_now = "HUMO VERT"
hit_strobe = "STROBO"
hit_strobe_soft = "STROBO SUAVE"
```

`qlctool/locales/en.toml` - same identifiers, same order:

```toml
# English display names. Same identifiers, same order, as every other catalogue.

[colors]
red = "Red"
fire_red = "Fire Red"
orange = "Orange"
amber = "Amber"
yellow = "Yellow"
green = "Green"
mint_green = "Mint Green"
cyan = "Cyan"
light_blue = "Light Blue"
sky_blue = "Sky Blue"
blue = "Blue"
deep_blue = "Deep Blue"
purple = "Purple"
ultraviolet = "Ultraviolet"
magenta = "Magenta"
fuchsia = "Fuchsia"
pink = "Pink"
white = "White"

[functions]
auto = "AUTO"
talk_moment = "Talk Moment"
calm_moment = "Calm Moment"
party_moment = "Party Moment"
frenzy_moment = "Frenzy Moment"
full_white = "Full White"
all_black = "All Black"
flash_full = "Flash 100%"
flash_half = "Flash 50%"
flash_colour = "Flash Colour"
smoke_on = "Smoke On"
vertical_smoke_now = "Vertical Smoke Now"
strobe_fast = "Strobe Fast"
strobe_medium = "Strobe Medium"
colour_wheel = "Colour Wheel"
simple_wheel = "Simple Wheel"
pastel_wheel = "Pastel Wheel"
multicolour_wheel = "Multicolour Wheel"
mix_wheel = "Mix Wheel"
head_movements = "Head Movements"
gobo_animation = "Gobo Animation"
prism_animation = "Prism Animation"
rainbow_together = "Rainbow Together"
rainbow_steps = "Rainbow Steps"
smoke_auto = "Smoke Auto"
vertical_smoke = "Vertical Smoke"
dimmer_chase = "Dimmer Chase"
dimmer_chase_2 = "Dimmer Chase 2"
dimmer_sequence = "Dimmer Sequence"
dimmer_pingpong = "Dimmer Ping-Pong"
strobe_on = "Strobe On"
strobe_off = "Strobe Off"
bass_hit = "Bass Hit"
stage_aim = "Stage"
soft_movements = "Soft Movements"
wash_movements = "Wash Movements"
beam_movements = "Beam Movements"
fast_washes = "Fast Washes"
fast_beams = "Fast Beams"

[frames]
room_states = "THE ROOM IS — one at a time"
hits = "HITS — they add to whatever is playing"
haze = "AMBIENT HAZE — how often it fires"
intensity_chases = "Fixture intensity and strobe"
colour_hits = "COLOUR HITS — hold down"
family_colour = "COLOUR"
family_pixels = "PIXELS"
family_heads = "HEADS"
family_gobos = "GOBOS"
family_prism = "PRISM"
desk_bursts = "Desk bursts"

[captions]
vertical_smoke_light = "VERTICAL HAZE — its light · N"
pick_prefix = "Play · "
hit_flash = "FLASH"
hit_flash_slow = "SLOW FLASH"
hit_flash_colour = "COLOUR FLASH"
hit_smoke_now = "HAZE NOW"
hit_vertical_smoke_now = "VERTICAL HAZE"
hit_strobe = "STROBE"
hit_strobe_soft = "SOFT STROBE"
```

`pyproject.toml`, `[tool.setuptools.package-data]`:
`qlctool = ["library/*.xsd", "library/system/*.qxf", "locales/*.toml"]`.

- [ ] **Step 4: Write the resolver**

`qlctool/names/__init__.py`:

```python
"""Stable identifiers for everything the generator names, and their words per language."""
```

`qlctool/names/sections.py`:

```python
"""The kinds of thing a catalogue names, in catalogue order."""

SECTIONS: tuple[str, ...] = ("colors", "functions", "frames", "captions")
```

`qlctool/names/identifier_pattern.py`:

```python
"""What an identifier looks like: English snake case, starting with a letter."""

import re

IDENTIFIER_PATTERN = re.compile(r"[a-z][a-z0-9_]*")
```

`qlctool/names/catalogue_dir.py`:

```python
"""Where the shipped catalogues live: one `<language>.toml` per language."""

from pathlib import Path

CATALOGUE_DIR = Path(__file__).resolve().parent.parent / "locales"
```

`qlctool/names/load_catalogue.py`:

```python
"""Read one language's catalogue and refuse a malformed one."""

import tomllib
from functools import cache

from .catalogue_dir import CATALOGUE_DIR
from .identifier_pattern import IDENTIFIER_PATTERN
from .sections import SECTIONS


@cache
def load_catalogue(language: str) -> dict[str, dict[str, str]]:
    """Section -> identifier -> display name. Cached: callers must not mutate it."""
    path = CATALOGUE_DIR / f"{language}.toml"
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    for section, entries in document.items():
        if section not in SECTIONS or not isinstance(entries, dict):
            raise ValueError(f"{path}: [{section}] is not a catalogue section; sections: {SECTIONS}")
        for identifier, text in entries.items():
            if not IDENTIFIER_PATTERN.fullmatch(identifier) or not isinstance(text, str) or not text:
                raise ValueError(
                    f"{path}: [{section}] {identifier!r} must be snake_case = a non-empty string"
                )
    return document
```

`qlctool/names/shipped_languages.py`:

```python
"""The languages a catalogue ships for."""

from .catalogue_dir import CATALOGUE_DIR


def shipped_languages() -> tuple[str, ...]:
    """Every `<language>.toml` in the catalogue folder, sorted."""
    return tuple(sorted(path.stem for path in CATALOGUE_DIR.glob("*.toml")))
```

`qlctool/names/name_resolution_error.py`:

```python
"""A name that resolves to no identifier, or to more than one."""


class NameResolutionError(ValueError):
    """Raised with the matches, or the close matches, in the message."""
```

`qlctool/names/names.py`:

```python
"""Identifiers <-> display names, across every shipped language and a show's overrides."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from difflib import get_close_matches

from .name_resolution_error import NameResolutionError


@dataclass(frozen=True)
class Names:
    """One show's vocabulary: its language, every catalogue, and its own overrides.

    `display` answers in the show's language; `lookup` and `identify` accept an
    identifier or any spelling in any catalogue or override, case-insensitively,
    because "rojo", "Rojo" and "red" are the same colour.
    """

    language: str
    catalogues: Mapping[str, Mapping[str, Mapping[str, str]]]
    overrides: Mapping[str, Mapping[str, str]] = field(default_factory=dict)

    def identifiers(self, section: str) -> tuple[str, ...]:
        """The identifiers one section defines, in catalogue order."""
        return tuple(self.catalogues[self.language].get(section, {}))

    def display(self, identifier: str) -> str:
        """The word the show writes for an identifier."""
        override = self.overrides.get(self.language, {}).get(identifier)
        if override is not None:
            return override
        for entries in self.catalogues[self.language].values():
            if identifier in entries:
                return entries[identifier]
        raise NameResolutionError(f"no {self.language!r} name for identifier {identifier!r}")

    def spellings(self, identifier: str) -> tuple[str, ...]:
        """Every word any catalogue or override gives an identifier, without repeats."""
        found = [
            entries[identifier]
            for catalogue in self.catalogues.values()
            for entries in catalogue.values()
            if identifier in entries
        ]
        found += [words[identifier] for words in self.overrides.values() if identifier in words]
        return tuple(dict.fromkeys(found))

    def lookup(self, name: str, sections: Sequence[str]) -> tuple[str, ...]:
        """Every identifier in these sections that `name` spells, case-insensitively."""
        wanted = name.strip().casefold()
        return tuple(
            identifier
            for section in sections
            for identifier in self.identifiers(section)
            if wanted == identifier
            or any(wanted == spelling.strip().casefold() for spelling in self.spellings(identifier))
        )

    def identify(self, name: str, sections: Sequence[str]) -> str:
        """The one identifier `name` spells; an error naming the candidates otherwise."""
        matches = self.lookup(name, sections)
        if len(matches) == 1:
            return matches[0]
        if matches:
            raise NameResolutionError(f"{name!r} is ambiguous: it names {', '.join(matches)}")
        known = [
            word
            for section in sections
            for identifier in self.identifiers(section)
            for word in (identifier, *self.spellings(identifier))
        ]
        close = get_close_matches(name, known, n=5)
        hint = f"; did you mean {', '.join(repr(word) for word in close)}?" if close else ""
        raise NameResolutionError(f"unknown name {name!r} among {', '.join(sections)}{hint}")
```

`qlctool/names/shipped_names.py`:

```python
"""A `Names` over every shipped catalogue, in one show language."""

from collections.abc import Mapping

from .load_catalogue import load_catalogue
from .name_resolution_error import NameResolutionError
from .names import Names
from .shipped_languages import shipped_languages


def shipped_names(
    language: str = "es", overrides: Mapping[str, Mapping[str, str]] | None = None
) -> Names:
    """The shipped catalogues, answering in `language`, with a show's overrides on top."""
    languages = shipped_languages()
    if language not in languages:
        raise NameResolutionError(
            f"no catalogue for language {language!r}; shipped: {', '.join(languages)}"
        )
    return Names(
        language=language,
        catalogues={code: load_catalogue(code) for code in languages},
        overrides=dict(overrides or {}),
    )
```

`qlctool/names/default_names.py`:

```python
"""The vocabulary a check or the desk reads a saved workspace with."""

from functools import cache

from .names import Names
from .shipped_names import shipped_names


@cache
def default_names() -> Names:
    """Every shipped catalogue, in Spanish, with no overrides - built once."""
    return shipped_names()
```

- [ ] **Step 5: Run the tests**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_names.py tests/test_catalogue_vocabulary.py -q -n 0
```
Expected: `20 passed` (16 in `test_names.py` with its parametrisations, 4 in the vocabulary file), no failures.

- [ ] **Step 6: Gates** - Global Constraint 2 plus ruff on the new `.py` files.
  Expected: suite green, three `identical`, checks exit 0.

- [ ] **Step 7: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/locales tools/qlctool/qlctool/names tools/qlctool/pyproject.toml \
  tools/qlctool/tests/test_names.py tools/qlctool/tests/test_catalogue_vocabulary.py
git commit -m "feat(qlctool): English and Spanish name catalogues, resolved by identifier or any spelling" \
  -m "qlctool/locales/{en,es}.toml give every colour, function, console frame and desk caption the generator names a stable snake-case identifier. Names resolves an identifier or any shipped spelling, case-insensitively, answers in the show's language, applies a show's overrides, and refuses unknown or ambiguous names with the candidates. A test pins the Spanish catalogue to the strings the generator writes today." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 5: Vibra described by identifier, localised at the build

Spec step 3, second half. `vibra_description()` now names colours and
functions by identifier; `build_canonical_show` localises the description
through `Names` before any generator runs, and refuses a vocabulary the
generator cannot write yet (ruling R1).

**Files:**
- Create: `qlctool/description/rename_description.py`, `qlctool/description/identify_description.py`,
  `qlctool/description/localize_description.py`, `qlctool/description/description_names.py`,
  `qlctool/names/generator_language.py`, `qlctool/names/check_generator_vocabulary.py`
- Create: `tests/test_description_identifiers.py`
- Modify: `qlctool/description/show_description.py` (fields `language`, `names`),
  `qlctool/vibra/description.py`, `qlctool/generate/canonical_show.py` (entry),
  `tests/test_show_description.py` (identifier keys)

**Interfaces:**
- Produces:
  - `ShowDescription.language: str = "es"`, `ShowDescription.names: Mapping[str, Mapping[str, str]] = field(default_factory=dict)` (language -> identifier -> display override).
  - `rename_description(description: ShowDescription, colour: Callable[[str], str], function: Callable[[str], str]) -> ShowDescription` - maps every colour name (palette keys, primary, simple, white, the three pair tables, matrix colours, curated-matrix colours) and every function name (console keys' keys, flash functions, beat-timing keys); fixture-group names are never renamed.
  - `identify_description(description, names: Names) -> ShowDescription` (names -> identifiers).
  - `localize_description(description, names: Names) -> ShowDescription` (identifier or any spelling -> display name in `names.language`).
  - `description_names(description) -> Names` (`shipped_names(description.language, description.names)`).
  - `GENERATOR_LANGUAGE = "es"`; `check_generator_vocabulary(names: Names) -> None` (raises `ValueError` mentioning "Spanish vocabulary").
  - `vibra_description()` now identifier-keyed (`palette["red"]`, `keys["auto"]`, `beat_timings["colour_wheel"]`).
- Consumes: Task 4's `Names`, `shipped_names`, `default_names`, `load_catalogue`.

- [ ] **Step 1: Write the failing tests** - `tests/test_description_identifiers.py`

```python
"""The description names things by identifier; the build writes them in the show's words.

2026-09-24, spec step 3: localised to Spanish, the Vibra description is today's
show to the byte (tests/test_vibra_byte_identity.py); localised to English only
the names change. Until the generators' own literals come from the catalogue,
the build refuses any vocabulary but the Spanish one (plan ruling R1).
"""

from dataclasses import replace
from pathlib import Path

import pytest

from qlctool.description.localize_description import localize_description
from qlctool.description.matrices_by_group import matrices_by_group
from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.matrix_algorithms import CURATED_MATRICES
from qlctool.names.check_generator_vocabulary import check_generator_vocabulary
from qlctool.names.shipped_names import shipped_names
from qlctool.palette import PALETTE, PRIMARY_COLORS
from qlctool.vibra.description import vibra_description
from qlctool.vibra.flash_functions import FLASH_FUNCTIONS
from qlctool.vibra.keys import KEYS
from qlctool.vibra.timing import VIBRA_TIMING
from qlctool.workspace import Workspace

SHOW = Path(__file__).resolve().parents[3] / "QLC+ Setups" / "Vibra.qxw"


def test_the_vibra_description_names_things_by_identifier():
    show = vibra_description()
    assert list(show.colours.palette)[:3] == ["red", "fire_red", "orange"]
    assert show.colours.white == "white"
    assert show.console.keys["auto"] == "Q" and show.console.keys["talk_moment"] == "F1"
    assert "stage_aim" in show.console.flash_functions
    assert show.timing.beat_timings["colour_wheel"].hold == 8
    assert show.matrices["BarrasLed"][0].colors == ("red", "blue")
    assert show.language == "es" and show.names == {}


def test_localised_to_spanish_it_is_todays_show():
    show = localize_description(vibra_description(), shipped_names("es"))
    assert list(show.colours.palette.items()) == list(PALETTE.items())
    assert show.colours.primary == PRIMARY_COLORS
    assert list(show.console.keys.items()) == list(KEYS.items())
    assert show.console.flash_functions == FLASH_FUNCTIONS
    assert list(show.timing.beat_timings.items()) == list(VIBRA_TIMING.beat_timings.items())
    assert show.matrices == matrices_by_group(CURATED_MATRICES)


def test_localised_to_english_only_the_names_change():
    show = localize_description(vibra_description(), shipped_names("en"))
    assert show.colours.palette["Red"] == (255, 0, 0)
    assert show.console.keys["Party Moment"] == "F3"


def test_the_generator_refuses_a_vocabulary_it_cannot_write_yet():
    check_generator_vocabulary(shipped_names("es"))
    with pytest.raises(ValueError, match="'en'"):
        check_generator_vocabulary(shipped_names("en"))
    with pytest.raises(ValueError, match="party_moment"):
        check_generator_vocabulary(shipped_names("es", {"es": {"party_moment": "Fiestón"}}))


def test_build_refuses_an_english_description():
    workspace = Workspace.load(SHOW)
    with pytest.raises(ValueError, match="Spanish vocabulary"):
        build_canonical_show(
            workspace, FixtureLibrary.load(), description=replace(vibra_description(), language="en")
        )
```

- [ ] **Step 2: Run them and watch them fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_description_identifiers.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.description.localize_description'`.

- [ ] **Step 3: Implement**

`qlctool/description/show_description.py`: add `from dataclasses import dataclass, field`
and, after `console`, the fields:

```python
    language: str = "es"
    # language -> identifier -> the show's own word for it ([names.<lang>]).
    names: Mapping[str, Mapping[str, str]] = field(default_factory=dict)
```

`qlctool/description/rename_description.py`:

```python
"""Rename every colour and function a description names, leaving its values alone."""

from collections.abc import Callable
from dataclasses import replace

from ..color_pair import ColorPair
from .show_description import ShowDescription


def rename_description(
    description: ShowDescription,
    colour: Callable[[str], str],
    function: Callable[[str], str],
) -> ShowDescription:
    """The same description with `colour` applied to colour names and `function` to function names.

    Fixture-group names come from the patch and are never renamed.
    """
    colours = description.colours
    renamed_colours = replace(
        colours,
        palette={colour(name): rgb for name, rgb in colours.palette.items()},
        primary=tuple(colour(name) for name in colours.primary),
        simple=tuple(colour(name) for name in colours.simple),
        white=colour(colours.white),
        analogous_pairs=tuple(ColorPair(colour(p.lead), colour(p.bed)) for p in colours.analogous_pairs),
        key_split_pairs=tuple((colour(a), colour(b)) for a, b in colours.key_split_pairs),
        complementary_pairs=tuple(
            ColorPair(colour(p.lead), colour(p.bed)) for p in colours.complementary_pairs
        ),
        matrix_colors=tuple(colour(name) for name in colours.matrix_colors),
    )
    matrices = {
        group: tuple(replace(s, colors=tuple(colour(name) for name in s.colors)) for s in scripts)
        for group, scripts in description.matrices.items()
    }
    timing = replace(
        description.timing,
        beat_timings={function(name): t for name, t in description.timing.beat_timings.items()},
    )
    console = replace(
        description.console,
        keys={function(name): key for name, key in description.console.keys.items()},
        flash_functions=tuple(function(name) for name in description.console.flash_functions),
    )
    return replace(description, colours=renamed_colours, matrices=matrices, timing=timing, console=console)
```

`qlctool/description/identify_description.py`:

```python
"""A description whose names are identifiers, whatever language it was written in."""

from ..names.names import Names
from .rename_description import rename_description
from .show_description import ShowDescription


def identify_description(description: ShowDescription, names: Names) -> ShowDescription:
    """Every colour and function name resolved to its catalogue identifier."""
    return rename_description(
        description,
        colour=lambda name: names.identify(name, ("colors",)),
        function=lambda name: names.identify(name, ("functions",)),
    )
```

`qlctool/description/localize_description.py`:

```python
"""A description in the words the generator writes: the show language's display names."""

from ..names.names import Names
from .rename_description import rename_description
from .show_description import ShowDescription


def localize_description(description: ShowDescription, names: Names) -> ShowDescription:
    """Every name - an identifier or any spelling - replaced by its display name.

    Accepting any spelling makes this safe on a description built in code with
    display names (the tests do) as well as on an identified one.
    """
    return rename_description(
        description,
        colour=lambda name: names.display(names.identify(name, ("colors",))),
        function=lambda name: names.display(names.identify(name, ("functions",))),
    )
```

`qlctool/description/description_names.py`:

```python
"""The vocabulary a description is written in and generated with."""

from ..names.names import Names
from ..names.shipped_names import shipped_names
from .show_description import ShowDescription


def description_names(description: ShowDescription) -> Names:
    """The shipped catalogues in the description's language, with its overrides."""
    return shipped_names(description.language, description.names)
```

`qlctool/names/generator_language.py`:

```python
"""The one vocabulary the generators still write literally (plan A ruling R1)."""

GENERATOR_LANGUAGE = "es"
```

`qlctool/names/check_generator_vocabulary.py`:

```python
"""Refuse a vocabulary the generator cannot write yet, instead of writing a broken show."""

from .generator_language import GENERATOR_LANGUAGE
from .load_catalogue import load_catalogue
from .names import Names


def check_generator_vocabulary(names: Names) -> None:
    """Raise unless every display name `names` gives is the Spanish catalogue's.

    The generators still spell their own function, frame and caption names in
    Spanish, and look the description's names up against those spellings: a
    key bound to "Party Moment" would never reach the "Momento Fiesta" button.
    Until those literals come from the catalogue (TODO.md), only the Spanish
    vocabulary produces a correct show.
    """
    problems = []
    if names.language != GENERATOR_LANGUAGE:
        problems.append(f"language {names.language!r}")
    spanish = load_catalogue(GENERATOR_LANGUAGE)
    for identifier, text in names.overrides.get(names.language, {}).items():
        expected = next((e[identifier] for e in spanish.values() if identifier in e), None)
        if text != expected:
            problems.append(f"{identifier} = {text!r}")
    if problems:
        raise ValueError(
            "the generator still writes its Spanish vocabulary literally and cannot produce "
            + "; ".join(problems)
            + " yet (TODO.md: generator names through the catalogue)"
        )
```

`qlctool/vibra/description.py`: import `identify_description` and `default_names`;
build the display-named description exactly as before into a local `spoken`,
then `return identify_description(spoken, default_names())`. Docstring:
`"""Today's Vibra values, named by catalogue identifier."""`.

`qlctool/generate/canonical_show.py`: import `localize_description`,
`description_names`, `check_generator_vocabulary`; replace the Task 2 line
`described = description if description is not None else vibra_description()` with:

```python
    source = description if description is not None else vibra_description()
    vocabulary = description_names(source)
    check_generator_vocabulary(vocabulary)
    described = localize_description(source, vocabulary)
```

`tests/test_show_description.py`: in `test_vibra_is_the_default_description`,
`beat_timings["Rueda Colores"]` -> `beat_timings["colour_wheel"]`,
`keys["AUTO"]` -> `keys["auto"]`, `"Escenario" in` -> `"stage_aim" in`; in
`test_the_description_palette_colours_the_matrices`, `"Rojo": (250, 0, 0)` ->
`"red": (250, 0, 0)` and `matrix_colors=("Rojo",)` -> `matrix_colors=("red",)`
(the asserted function names stay Spanish: they are what the build writes).

- [ ] **Step 4: Run the tests**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_description_identifiers.py tests/test_show_description.py -q -n 0
```
Expected: all pass.

- [ ] **Step 5: Gates** - Global Constraint 2 plus ruff on touched files. The
  byte comparison is the proof that localising the identified description gives
  back today's names and order.

- [ ] **Step 6: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/description tools/qlctool/qlctool/names tools/qlctool/qlctool/vibra/description.py \
  tools/qlctool/qlctool/generate/canonical_show.py tools/qlctool/tests/test_description_identifiers.py \
  tools/qlctool/tests/test_show_description.py
git commit -m "refactor(qlctool): describe Vibra by identifier and localise it at the build" \
  -m "vibra_description() names its colours and functions by catalogue identifier; build_canonical_show localises the description into the show language's display names before any generator runs. The generators still spell their own names in Spanish, so any other vocabulary is refused with an explicit error until that migration lands." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 6: The desk finds frames and bursts by identifier

The tablet desk (`desk_policy.place`, `desk_burst_sources`, `desk_burst_buttons`)
finds the console's frames today by comparing caption heads with the Spanish
constants of `live_console.py`/`play_page.py`, and keys burst durations and
notes by slugs of Spanish captions (`"flash-lento"`, `"humo-ya"`, `"rojo"`).
After this task each frame and each accent is resolved to a catalogue
identifier; `BURST_MS` and `desk_burst_note` are keyed by identifier. The
deskmap's output keys stay slugs (ruling R4), so `Vibra.desk.json` stays
byte-identical (`tests/test_shipped_deskmap.py`).

**Files:**
- Create: `qlctool/desk_frame_identifier.py`, `qlctool/desk_burst_identifier.py`,
  `qlctool/desk_burst_duration.py`, `tests/test_desk_identifiers.py`
- Modify: `qlctool/desk_policy.py` (imports 16-24, `BURST_MS` 31-49, `FAMILY_PAGES` 60,
  `place` 104-145, delete `_head` 164-165), `qlctool/desk_burst_sources.py`,
  `qlctool/desk_burst_buttons.py`, `qlctool/desk_burst_note.py`, `qlctool/deskmap.py`,
  `qlctool/generate/desk_bursts.py`, `qlctool/checks/rule_desk_bursts.py`,
  `qlctool/checks/valid_desk_bursts.py`, `tests/test_deskmap.py` (61-69),
  `tests/test_desk_bursts.py` (39)

**Interfaces:**
- Produces:
  - `desk_frame_identifier(caption: str, names: Names) -> str | None` - the `frames` identifier whose head (text before ` — `) matches the caption's head in any spelling, case-insensitively.
  - `desk_burst_identifier(caption: str, names: Names) -> str | None` - glyph and key hint stripped (`leading_glyph(split_caption(caption)[0])`), then a unique `lookup` in `("captions", "colors")`.
  - `desk_burst_duration(source: DeskWidget, names: Names) -> int | None` - `BURST_MS.get(desk_burst_identifier(...))`.
  - `BURST_MS: dict[str, int]` keyed by identifier: `hit_flash`, `hit_flash_slow`, `hit_flash_colour` 8000; `hit_strobe`, `hit_strobe_soft` 4000; `hit_smoke_now`, `hit_vertical_smoke_now` 3000; `red`, `green`, `blue`, `ultraviolet`, `yellow`, `cyan`, `magenta`, `white`, `orange`, `pink` 8000 (same values, same order as today's slug keys).
  - `desk_burst_note(identifier: str) -> str | None` (same texts).
  - New optional last parameter `names: Names | None = None` (default `default_names()`) on `place`, `desk_burst_sources`, `desk_burst_buttons`, `build_deskmap`, `check_desk_bursts`, `valid_desk_bursts`.
- Consumes: Task 4's `Names`, `default_names`; `DeskWidget`, `desk_widgets`, `leading_glyph`, `split_caption`.

- [ ] **Step 1: Write the failing test** - `tests/test_desk_identifiers.py`

```python
"""The desk places controls by frame identifier, not by Spanish words (2026-09-24).

Spec: "Checks and the desk map resolve widgets through the identifiers, never
through the Spanish strings they search for today." Renaming every console frame
to its English catalogue spelling must leave the desk's pages exactly as they were.
"""

from copy import deepcopy
from pathlib import Path

import pytest

from qlctool.deskmap import build_deskmap
from qlctool.desk_burst_duration import desk_burst_duration
from qlctool.desk_widgets import DeskWidget
from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.names.default_names import default_names
from qlctool.names.load_catalogue import load_catalogue
from qlctool.workspace import Workspace

SHOW = Path(__file__).resolve().parents[3] / "QLC+ Setups" / "Vibra.qxw"


@pytest.fixture(scope="module")
def generated():
    workspace = Workspace.load(SHOW)
    build_canonical_show(workspace, FixtureLibrary.load())
    return workspace


def _frames_in_english(workspace):
    translated = deepcopy(workspace)
    spanish, english = load_catalogue("es")["frames"], load_catalogue("en")["frames"]
    for element in translated.root.iter():
        for identifier, text in spanish.items():
            if element.get("Caption") == text:
                element.set("Caption", english[identifier])
    return translated


def _sections(deskmap):
    return [(p["key"], s["key"], s["controls"]) for p in deskmap["pages"] for s in p["sections"]]


def test_the_desk_places_frames_named_in_any_shipped_language(generated, tmp_path):
    library = FixtureLibrary.load()
    spanish = build_deskmap(generated, library, tmp_path / "show.qxw")
    english = build_deskmap(_frames_in_english(generated), library, tmp_path / "show.qxw")
    assert _sections(english) == _sections(spanish)


@pytest.mark.parametrize(
    ("caption", "duration"),
    [
        ("⚡ FLASH LENTO · -", 8000),
        ("ROJO", 8000),
        ("RED", 8000),
        ("☁ HUMO YA", 3000),
        ("✳ STROBE", 4000),
        ("Rig Rojo / Azul", None),
    ],
)
def test_a_burst_lasts_what_its_identifier_says(caption, duration):
    widget = DeskWidget(
        id=1, kind="Button", caption=caption, page=0, function=1, action="Flash",
        key=None, frames=(), solo=None, fade_out_ms=0, slider_mode="",
    )
    assert desk_burst_duration(widget, default_names()) == duration
```

- [ ] **Step 2: Run it and watch it fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_desk_identifiers.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.desk_burst_duration'`.

- [ ] **Step 3: Implement**

`qlctool/desk_frame_identifier.py`:

```python
"""Which console frame a caption heads, by catalogue identifier, in any shipped language."""

from .names.names import Names


def desk_frame_identifier(caption: str, names: Names) -> str | None:
    """The `frames` identifier whose head matches this caption's head, or None.

    A frame caption is "<name> — <explanation>"; only the name identifies it,
    so a reworded explanation does not drop a page.
    """
    head = caption.split(" — ", maxsplit=1)[0].strip().casefold()
    for identifier in names.identifiers("frames"):
        for spelling in names.spellings(identifier):
            if spelling.split(" — ", maxsplit=1)[0].strip().casefold() == head:
                return identifier
    return None
```

`qlctool/desk_burst_identifier.py`:

```python
"""What a held desk accent is, by identifier: a hit caption or a palette colour."""

from .desk_policy import split_caption
from .leading_glyph import leading_glyph
from .names.names import Names


def desk_burst_identifier(caption: str, names: Names) -> str | None:
    """The identifier the accent's name spells, without its glyph and key hint; None if none or many."""
    _, text = leading_glyph(split_caption(caption)[0])
    matches = names.lookup(text, ("captions", "colors"))
    return matches[0] if len(matches) == 1 else None
```

`qlctool/desk_burst_duration.py`:

```python
"""How long a desk burst runs, from its source accent's identifier."""

from .desk_burst_identifier import desk_burst_identifier
from .desk_policy import BURST_MS
from .desk_widgets import DeskWidget
from .names.names import Names


def desk_burst_duration(source: DeskWidget, names: Names) -> int | None:
    """Milliseconds for this accent's burst, or None when the desk has no duration for it."""
    identifier = desk_burst_identifier(source.caption, names)
    return None if identifier is None else BURST_MS.get(identifier)
```

`qlctool/desk_policy.py`:
- Imports: delete the `.generate.live_console` import (16-23 region) and the
  `.generate.play_page` import (24); add `from .desk_frame_identifier import desk_frame_identifier`,
  `from .names.default_names import default_names`, `from .names.names import Names`.
  Update the module docstring's second paragraph: frames are found by catalogue
  identifier (`qlctool/locales`), so a frame caption in any shipped language places the same.
- `BURST_MS` (31-49) becomes, same values and order:
  ```python
  BURST_MS = {
      "hit_flash": 8000,
      "hit_flash_slow": 8000,
      "hit_flash_colour": 8000,
      "hit_strobe": 4000,
      "hit_strobe_soft": 4000,
      "hit_smoke_now": 3000,
      "hit_vertical_smoke_now": 3000,
      "red": 8000,
      "green": 8000,
      "blue": 8000,
      "ultraviolet": 8000,
      "yellow": 8000,
      "cyan": 8000,
      "magenta": 8000,
      "white": 8000,
      "orange": 8000,
      "pink": 8000,
  }
  ```
- `FAMILY_PAGES` (60) becomes
  `FAMILY_PAGES = {"family_colour": "color", "family_pixels": "pixels", "family_heads": "heads", "family_gobos": "gobos", "family_prism": "prism"}`.
- `place` (104-145):
  ```python
  def place(
      widget: DeskWidget,
      frames: dict[int, DeskWidget],
      function_name: str | None,
      function_kind: str = "",
      names: Names | None = None,
  ) -> Placement | None:
      """Where a widget goes on the desk, or None when the desk does not show it."""
      vocabulary = default_names() if names is None else names
      if widget.kind != "Button" or widget.function is None:
          return None
      held = widget.action == "Flash"
      if widget.action not in ("Toggle", "Flash"):
          return None
      within = {
          desk_frame_identifier(frames[fid].caption, vocabulary)
          for fid in widget.frames
          if fid in frames
      }
      if "room_states" in within:
          return Placement("live", "state", "state", True, "")
      if "hits" in within:
          if held:
              return Placement("live", "accents", "accent", False, HELD_REASON)
          return Placement("live", "accents", "toggle", True, "")
      if "haze" in within:
          return Placement("live", "haze", "haze", True, "")
      if "colour_hits" in within:
          return Placement("color", "accents", "accent", False, HELD_REASON)
      for family, page in FAMILY_PAGES.items():
          if family in within:
              if held:
                  return None
              prefixes = vocabulary.spellings("pick_prefix")
              pick = any((function_name or "").startswith(prefix) for prefix in prefixes)
              return Placement(
                  page, "picks" if pick else "hooks", "pick" if pick else "hook", True, ""
              )
      if "intensity_chases" in within:
          # (keep the two comment lines from the old CHASES_FRAME branch)
          if held or function_kind not in ("Chaser", "Collection", "Sequence"):
              return None
          return Placement("control", "chases", "chase", True, "")
      # (keep the two comment lines about the glyph prefix)
      if vocabulary.lookup(leading_glyph(widget.caption)[1], ("captions",)) == ("vertical_smoke_light",):
          return Placement("control", "haze-light", "toggle", True, "")
      return None
  ```
- Delete `_head` (164-165), now unused.

`qlctool/desk_burst_sources.py`: signature
`def desk_burst_sources(root: etree._Element, names: Names | None = None) -> dict[str, DeskWidget]:`;
first line `vocabulary = default_names() if names is None else names`;
`place(widget, frames, None)` -> `place(widget, frames, None, names=vocabulary)`. Keys stay
`slugify(split_caption(widget.caption)[0])`.

`qlctool/desk_burst_buttons.py`: same signature change; the frame set becomes
```python
    frames = {
        w.id
        for w in widgets
        if w.kind in ("Frame", "SoloFrame")
        and desk_frame_identifier(w.caption, vocabulary) == "desk_bursts"
    }
```
and the `BURST_FRAME` import is removed (the generator still writes `BURST_FRAME`).

`qlctool/desk_burst_note.py`:
```python
"""Explain the priority loss of an API-started burst beside the held Mac cue."""


def desk_burst_note(identifier: str) -> str | None:
    """The desk's warning for a burst, by its source accent's identifier."""
    if identifier in ("hit_smoke_now", "hit_vertical_smoke_now"):
        return None
    if identifier in ("hit_strobe", "hit_strobe_soft"):
        return "Sin prioridad Override: otro barrido de shutter puede pisar el estrobo."
    if identifier in ("hit_flash", "hit_flash_slow", "white"):
        return "Luz a máxima intensidad; rueda de color y estrobo pueden ser pisados por el show."
    if identifier == "hit_flash_colour":
        return "Conserva el color del show; otro barrido de shutter puede pisar el estrobo."
    return "Sin ForceLTP ni Override: el color se suma al show; rueda y estrobo pueden ser pisados."
```

`qlctool/checks/rule_desk_bursts.py`:
```python
"""2026-09-13: a lost tablet release must never leave a held accent running."""

from lxml import etree

from ..desk_burst_buttons import desk_burst_buttons
from ..desk_burst_duration import desk_burst_duration
from ..desk_burst_sources import desk_burst_sources
from ..names.default_names import default_names
from ..names.names import Names
from .desk_burst_errors import desk_burst_errors
from .finding import ERROR, Finding
from .show_graph import ShowGraph

RULE = "rafaga del desk"


def check_desk_bursts(
    graph: ShowGraph, root: etree._Element, names: Names | None = None
) -> list[Finding]:
    vocabulary = default_names() if names is None else names
    sources = desk_burst_sources(root, vocabulary)
    buttons = desk_burst_buttons(root, vocabulary)
    findings = []
    for key in sources.keys() | buttons.keys():
        candidates = buttons.get(key, [])
        duration = desk_burst_duration(sources[key], vocabulary) if key in sources else None
        if duration is None or len(candidates) != 1:
            findings.append(
                Finding(
                    RULE, ERROR, key, "requiere un origen, una duracion y un unico Toggle de rafaga"
                )
            )
            continue
        for error in desk_burst_errors(graph, root, sources[key], candidates[0], duration):
            findings.append(Finding(RULE, ERROR, key, error))
    return findings
```

`qlctool/checks/valid_desk_bursts.py`: same shape - `names: Names | None = None`,
`vocabulary`, `sources = desk_burst_sources(root, vocabulary)`, iterate
`desk_burst_buttons(root, vocabulary).items()`, `duration = desk_burst_duration(sources[key], vocabulary) if key in sources else None`,
skip when `duration is None or len(buttons) != 1`, and pass `duration` to
`desk_burst_errors` in place of `BURST_MS[key]`; drop the `BURST_MS` import.

`qlctool/generate/desk_bursts.py`: import `desk_burst_duration` and `default_names`, drop
`BURST_MS` from the `desk_policy` import; in the loop replace
`duration = BURST_MS[key]` / `if duration <= 0:` with
```python
        duration = desk_burst_duration(source, default_names())
        if duration is None or duration <= 0:
            raise ValueError(f"burst duration must be positive: {key}")
```

`qlctool/deskmap.py`: signature
`def build_deskmap(workspace: Workspace, library: FixtureLibrary, path: str | Path, names: Names | None = None) -> dict:`;
`vocabulary = default_names() if names is None else names` first; pass it to
`check_desk_bursts(graph, root, vocabulary)`, `desk_burst_buttons(root, vocabulary)` and
`place(widget, frames, function_name, graph.kind(widget.function), names=vocabulary)`;
in the accent branch compute `identifier = desk_burst_identifier(widget.caption, vocabulary)` and use
`"burstMs": BURST_MS[identifier]` and `note = desk_burst_note(identifier)` (the control key,
`"source": key` and everything else unchanged). Imports: add `desk_burst_identifier`,
`default_names`, `Names`.

`tests/test_deskmap.py` 61-69 (`test_2026_09_13_held_accents_are_replaced_by_bounded_bursts`):
replace the two `BURST_MS` assertions with
```python
    assert len(bursts) == len(BURST_MS)
    assert sorted(c["burstMs"] for c in bursts.values()) == sorted(BURST_MS.values())
```
and delete `assert control["burstMs"] == BURST_MS[key]` inside the loop.

`tests/test_desk_bursts.py:39`: replace with
```python
    assert sources.keys() == buttons.keys()
    names = default_names()
    assert {desk_burst_identifier(s.caption, names) for s in sources.values()} == BURST_MS.keys()
```
adding imports `from qlctool.desk_burst_identifier import desk_burst_identifier` and
`from qlctool.names.default_names import default_names`.

- [ ] **Step 4: Run the desk tests**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_desk_identifiers.py tests/test_deskmap.py tests/test_desk_bursts.py tests/test_shipped_deskmap.py tests/test_check.py -q
```
Expected: all pass - `test_shipped_deskmap.py` proves `Vibra.desk.json` is
rebuilt byte for byte, and `test_2026_09_13_desk_link_loss_requires_bounded_hits`
still counts 17 findings keyed `humo-ya`, `humo-vert`, `flash`, `rojo`.

- [ ] **Step 5: Gates** - Global Constraint 2 plus ruff on touched files.

- [ ] **Step 6: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/desk_frame_identifier.py tools/qlctool/qlctool/desk_burst_identifier.py \
  tools/qlctool/qlctool/desk_burst_duration.py tools/qlctool/qlctool/desk_policy.py \
  tools/qlctool/qlctool/desk_burst_sources.py tools/qlctool/qlctool/desk_burst_buttons.py \
  tools/qlctool/qlctool/desk_burst_note.py tools/qlctool/qlctool/deskmap.py \
  tools/qlctool/qlctool/generate/desk_bursts.py tools/qlctool/qlctool/checks/rule_desk_bursts.py \
  tools/qlctool/qlctool/checks/valid_desk_bursts.py tools/qlctool/tests/test_desk_identifiers.py \
  tools/qlctool/tests/test_deskmap.py tools/qlctool/tests/test_desk_bursts.py
git commit -m "refactor(qlctool): the desk finds frames and bursts by identifier" \
  -m "desk_policy placed widgets by comparing frame captions with the console's Spanish constants, and keyed burst durations and notes by slugs of Spanish captions. Frames now resolve to catalogue identifiers in any shipped language, and BURST_MS and the burst notes are keyed by identifier. The tablet's control keys stay slugs, so Vibra.desk.json is rebuilt byte for byte." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 7: Controller profiles and the rule-provider registry

Spec step 4. `[controllers]` becomes `ControllerSettings`; the SMC-PAD is a
`MidiPadProfile` (bindings, button colours, input patch) the generator applies
only when asked; the tablet desk's bursts are generated only when asked; and
`checks/run.py` stops calling `check_desk_bursts`/`check_pad_input` directly -
they come back as `RuleProvider`s registered under the `qlctool.rules`
entry-point group and run only where they apply (ruling R3: modules stay where
they are). Vibra's default keeps both, so nothing it generates changes.

**Files:**
- Create: `qlctool/description/controller_settings.py`, `qlctool/vibra/controllers.py`
- Create: `qlctool/controllers/__init__.py`, `qlctool/controllers/midi_pad_profile.py`,
  `qlctool/controllers/smc_pad_profile.py`, `qlctool/controllers/midi_pads.py`,
  `qlctool/controllers/midi_pad_named.py`, `qlctool/controllers/smc_pad_applies.py`,
  `qlctool/controllers/smc_pad_check.py`, `qlctool/controllers/smc_pad_rules.py`,
  `qlctool/controllers/tablet_desk_applies.py`, `qlctool/controllers/tablet_desk_check.py`,
  `qlctool/controllers/tablet_desk_rules.py`
- Create: `qlctool/checks/rule_context.py`, `qlctool/checks/rule_provider.py`,
  `qlctool/checks/rule_group.py`, `qlctool/checks/own_rule_providers.py`,
  `qlctool/checks/rule_providers.py`, `qlctool/checks/bound_widgets.py`,
  `qlctool/checks/pad_bindings.py`, `qlctool/generate/bind_pad.py`,
  `qlctool/desk_function_path.py`
- Create: `tests/test_controllers.py`
- Modify: `qlctool/description/show_description.py`, `qlctool/vibra/description.py`,
  `qlctool/checks/run.py` (imports 27, 46; lines 98, 155; signature 84-88),
  `qlctool/checks/rule_pad_input.py` (36, 89-100), `qlctool/generate/live_console.py`
  (imports 52, 62-63; signature; 413-416, 433-434, 451-452, 454-464, 481-494, 640, 653, 730, 882, 984),
  `qlctool/generate/canonical_show.py` (import 25, line 301, lines 1124-1146),
  `qlctool/generate/desk_bursts.py` (two `"Desk"` literals), `pyproject.toml`, `codeality-py.toml`

**Interfaces:**
- Produces:
  - `ControllerSettings(midi_pad: str | None = None, tablet_desk: bool = False)`; `ShowDescription.controllers: ControllerSettings = ControllerSettings()`; `VIBRA_CONTROLLERS = ControllerSettings(midi_pad="smc-pad", tablet_desk=True)`.
  - `MidiPadProfile(name: str, bindings: Mapping[str, int], colors: Mapping[str, RGB], pin_input: Callable[[etree._Element], None])`; `SMC_PAD`; `MIDI_PADS: Mapping[str, MidiPadProfile]`; `midi_pad_named(name: str | None) -> MidiPadProfile | None` (ValueError listing known pads).
  - `RuleContext(root, graph: ShowGraph, groups: Mapping[int, tuple[int, ...]], entries: Mapping[int, str], states: set[int])`.
  - `RuleProvider(name: str, applies: Callable[[etree._Element], bool], check: Callable[[RuleContext], list[Finding]])`.
  - `RULE_GROUP = "qlctool.rules"`; `OWN_RULE_PROVIDERS = ("smc-pad", "tablet_desk")`; `rule_providers() -> tuple[RuleProvider, ...]` (cached; `TypeError` for a non-provider entry point; `RuntimeError` naming the reinstall command when an own provider is missing - ruling R10).
  - `SMC_PAD_RULES`, `TABLET_DESK_RULES` (entry-point targets).
  - `check_workspace(workspace, library, canvas=None, providers: Sequence[RuleProvider] | None = None)`.
  - `pad_bindings(root) -> dict[int, list[str]]` (extracted from `rule_pad_input._bindings`); `BOUND_WIDGETS`.
  - `bind_pad(widget: etree._Element, bindings: Mapping[str, int], name: str, source_id: int = 0) -> None`.
  - `DESK_FUNCTION_PATH = "Desk"`.
  - `generate_live_console(..., pad_bindings: Mapping[str, int] | None = None, pad_colors: Mapping[str, tuple[int, int, int]] | None = None)` - no pad unless passed.
- Consumes: `SMC_PAD_BINDINGS`, `FUNCTION_COLORS`, `pin_midi_input`, `check_pad_input`,
  `check_desk_bursts`, `desk_widgets`, `desk_frame_identifier`, `default_names`.

- [ ] **Step 1: Write the failing tests** - `tests/test_controllers.py`

```python
"""Controllers are optional profiles; their checks run only where they apply (2026-09-24).

Spec step 4: "A show without a controller block gets neither, and its checks do
not run", and `qlctool check` still runs every check that applies, found
through the `qlctool.rules` entry points.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from qlctool.checks.finding import ERROR, Finding
from qlctool.checks.pad_bindings import pad_bindings
from qlctool.checks.rule_provider import RuleProvider
from qlctool.checks.rule_providers import rule_providers
from qlctool.checks.run import check_workspace
from qlctool.description.controller_settings import ControllerSettings
from qlctool.desk_function_path import DESK_FUNCTION_PATH
from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.vibra.description import vibra_description
from qlctool.workspace import Workspace

SHOW = Path(__file__).resolve().parents[3] / "QLC+ Setups" / "Vibra.qxw"


@pytest.fixture(scope="module")
def library():
    return FixtureLibrary.load()


@pytest.fixture(scope="module")
def bare(library):
    workspace = Workspace.load(SHOW)
    description = replace(vibra_description(), controllers=ControllerSettings())
    build_canonical_show(workspace, library, description=description)
    return workspace


def test_the_toolkits_own_providers_are_registered():
    assert {p.name for p in rule_providers()} >= {"smc-pad", "tablet_desk"}


def test_the_vibra_show_uses_both_controllers():
    root = Workspace.load(SHOW).root
    providers = {p.name: p for p in rule_providers()}
    assert providers["smc-pad"].applies(root)
    assert providers["tablet_desk"].applies(root)


def test_a_provider_runs_only_where_it_applies(library):
    workspace = Workspace.load(SHOW)
    seen = []

    def check(context):
        seen.append(context.root)
        return [Finding("regla de prueba", ERROR, "x", "y")]

    quiet = RuleProvider("quiet", applies=lambda root: False, check=check)
    loud = RuleProvider("loud", applies=lambda root: True, check=check)
    assert check_workspace(workspace, library, providers=[quiet]) == []
    assert [f.rule for f in check_workspace(workspace, library, providers=[loud])] == ["regla de prueba"]
    assert len(seen) == 1


def test_a_show_without_controllers_has_no_pad_binding_and_no_desk(bare):
    assert not pad_bindings(bare.root)
    assert not any(f.get("Path") == DESK_FUNCTION_PATH for f in bare.engine)
    own = [p for p in rule_providers() if p.name in ("smc-pad", "tablet_desk")]
    assert not any(p.applies(bare.root) for p in own)


def test_a_show_without_controllers_passes_every_check(bare, library):
    assert check_workspace(bare, library) == []


def test_an_unknown_pad_is_refused(library):
    description = replace(vibra_description(), controllers=ControllerSettings(midi_pad="launchpad"))
    with pytest.raises(ValueError, match="smc-pad"):
        build_canonical_show(Workspace.load(SHOW), library, description=description)
```

- [ ] **Step 2: Run them and watch them fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_controllers.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.checks.pad_bindings'`.

- [ ] **Step 3: Settings and profiles**

`qlctool/description/controller_settings.py`:

```python
"""Which control surfaces a show is bound to."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ControllerSettings:
    """A MIDI pad profile name and whether the tablet desk exists. Neither, unless a show says so."""

    midi_pad: str | None = None
    tablet_desk: bool = False
```

`qlctool/description/show_description.py`: import it and add, after `names`,
`controllers: ControllerSettings = ControllerSettings()`.

`qlctool/vibra/controllers.py`:

```python
"""The surfaces the Vibra show is played from: the SMC-PAD and the tablet desk."""

from ..description.controller_settings import ControllerSettings

VIBRA_CONTROLLERS = ControllerSettings(midi_pad="smc-pad", tablet_desk=True)
```

`qlctool/vibra/description.py`: pass `controllers=VIBRA_CONTROLLERS` in `spoken`.
`codeality-py.toml` `[roles] data`: add `"qlctool/vibra/controllers.py"`.

`qlctool/controllers/__init__.py`:

```python
"""Optional control surfaces - a MIDI pad, the tablet desk - and the checks that belong to them."""
```

`qlctool/controllers/midi_pad_profile.py`:

```python
"""A MIDI pad the console can be bound to."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from lxml import etree

from ..argb import RGB


@dataclass(frozen=True)
class MidiPadProfile:
    """Its map (widget name -> input channel), its button colours, and how to patch its input."""

    name: str
    bindings: Mapping[str, int]
    colors: Mapping[str, RGB]
    pin_input: Callable[[etree._Element], None]
```

`qlctool/controllers/smc_pad_profile.py`:

```python
"""The M-VAVE SMC-PAD as a profile: `smc_pad_bindings`, `smc_pad_colors`, `input_binding`."""

from ..generate.smc_pad_bindings import SMC_PAD_BINDINGS
from ..generate.smc_pad_colors import FUNCTION_COLORS
from ..input_binding import pin_midi_input
from .midi_pad_profile import MidiPadProfile

SMC_PAD = MidiPadProfile(
    name="smc-pad",
    bindings=SMC_PAD_BINDINGS,
    colors=FUNCTION_COLORS,
    pin_input=pin_midi_input,
)
```

`qlctool/controllers/midi_pads.py`:

```python
"""Every MIDI pad profile the toolkit ships, by the name a description uses."""

from collections.abc import Mapping

from .midi_pad_profile import MidiPadProfile
from .smc_pad_profile import SMC_PAD

MIDI_PADS: Mapping[str, MidiPadProfile] = {SMC_PAD.name: SMC_PAD}
```

`qlctool/controllers/midi_pad_named.py`:

```python
"""The pad profile a description names, or none."""

from .midi_pad_profile import MidiPadProfile
from .midi_pads import MIDI_PADS


def midi_pad_named(name: str | None) -> MidiPadProfile | None:
    """None for no pad; the profile for a known name; an error listing the known ones otherwise."""
    if name is None:
        return None
    if name not in MIDI_PADS:
        raise ValueError(f"unknown MIDI pad {name!r}; known: {', '.join(sorted(MIDI_PADS))}")
    return MIDI_PADS[name]
```

`qlctool/desk_function_path.py`:

```python
"""The function folder the tablet desk's burst cues are generated into."""

DESK_FUNCTION_PATH = "Desk"
```

`qlctool/generate/desk_bursts.py`: import it; both `"Desk"` literals (the
`scene.set("Path", "Desk")` and `path="Desk"` arguments) -> `DESK_FUNCTION_PATH`.

- [ ] **Step 4: The generator applies controllers only when described**

`qlctool/generate/bind_pad.py`:

```python
"""Bind one console widget to the pad, when the pad has a control for it."""

from collections.abc import Mapping

from lxml import etree

from ..vc.input_source import build_input_source


def bind_pad(
    widget: etree._Element, bindings: Mapping[str, int], name: str, source_id: int = 0
) -> None:
    """Append the `<Input>` for `name`'s pad control; nothing when there is no pad or no control."""
    channel = bindings.get(name)
    if channel is not None:
        build_input_source(widget, channel, source_id=source_id)
```

`qlctool/generate/live_console.py`:
- Imports: delete `from .smc_pad_bindings import SMC_PAD_BINDINGS`; change
  `from .smc_pad_colors import FUNCTION_COLORS, readable_foreground` to
  `from .smc_pad_colors import readable_foreground`; delete
  `from ..vc.input_source import build_input_source` if no use remains (grep after the edits);
  add `from .bind_pad import bind_pad`.
- Signature: add `pad_bindings: Mapping[str, int] | None = None,` and
  `pad_colors: Mapping[str, tuple[int, int, int]] | None = None,` after `palette`;
  first body lines `pad_bindings = dict(pad_bindings or {})` and `pad_colors = dict(pad_colors or {})`.
- 413 `colour = FUNCTION_COLORS.get(name)` -> `colour = pad_colors.get(name)`.
- 433-434 `if name in SMC_PAD_BINDINGS:` / `build_input_source(element, SMC_PAD_BINDINGS[name])` -> `bind_pad(element, pad_bindings, name)`.
- 451 -> `bind_pad(outer, pad_bindings, "Pagina Siguiente")`; 452 -> `bind_pad(outer, pad_bindings, "Pagina Anterior", source_id=1)`.
- `_page_show(...)` call and definition: append `pad_bindings`; 640 -> `bind_pad(stop_all, pad_bindings, "PARAR TODO")`; 653 -> `bind_pad(blackout, pad_bindings, "APAGON")`; 730 -> `bind_pad(dial, pad_bindings, "Tempo Show")`.
- `_page_control(...)` call and definition: append `pad_bindings`; 882 -> `bind_pad(grand_master, pad_bindings, "Master General")`; 984 -> `bind_pad(dial, pad_bindings, "Vel. Movimiento")`.

`qlctool/generate/canonical_show.py`:
- Delete the import `from ..input_binding import pin_midi_input`; add
  `from ..controllers.midi_pad_named import midi_pad_named`.
- Replace line 301 `pin_midi_input(workspace.root)` (keep the comment above it) with:
  ```python
      pad = midi_pad_named(described.controllers.midi_pad)
      if pad is not None:
          pad.pin_input(workspace.root)
  ```
- `generate_live_console(...)` call: add `pad_bindings=pad.bindings if pad is not None else None,`
  and `pad_colors=pad.colors if pad is not None else None,`.
- `button_ids.extend(generate_desk_bursts(workspace))` becomes
  ```python
          if described.controllers.tablet_desk:
              button_ids.extend(generate_desk_bursts(workspace))
  ```

- [ ] **Step 5: The registry**

`qlctool/checks/rule_context.py`:

```python
"""What one pass over a workspace has already worked out, handed to a provider's rules."""

from collections.abc import Mapping
from dataclasses import dataclass

from lxml import etree

from .show_graph import ShowGraph


@dataclass(frozen=True)
class RuleContext:
    """The workspace root, its function graph, groups, console entry points and room states."""

    root: etree._Element
    graph: ShowGraph
    groups: Mapping[int, tuple[int, ...]]
    entries: Mapping[int, str]
    states: set[int]
```

`qlctool/checks/rule_provider.py`:

```python
"""A set of checks that belongs to one part of a show: a controller, or a show's own."""

from collections.abc import Callable
from dataclasses import dataclass

from lxml import etree

from .finding import Finding
from .rule_context import RuleContext


@dataclass(frozen=True)
class RuleProvider:
    """`applies` says whether the workspace uses this part at all; `check` runs its rules."""

    name: str
    applies: Callable[[etree._Element], bool]
    check: Callable[[RuleContext], list[Finding]]
```

`qlctool/checks/rule_group.py`:

```python
"""The entry-point group a package registers its `RuleProvider`s under."""

RULE_GROUP = "qlctool.rules"
```

`qlctool/checks/own_rule_providers.py`:

```python
"""The providers qlctool itself registers, whose absence means a stale install."""

OWN_RULE_PROVIDERS: tuple[str, ...] = ("smc-pad", "tablet_desk")
```

`qlctool/checks/rule_providers.py`:

```python
"""Every rule provider installed under `qlctool.rules`, the toolkit's own and a show's.

The group is read from installed package metadata, so a checkout whose
`pyproject.toml` gained a provider has to be reinstalled (`pip install -e`)
before the provider exists. That is exactly the failure that would pass in
silence - a desk check that stops running looks like a desk with no problems -
so a missing own provider is an error, not an empty list.
"""

from functools import cache
from importlib.metadata import entry_points as installed_entry_points

from .own_rule_providers import OWN_RULE_PROVIDERS
from .rule_group import RULE_GROUP
from .rule_provider import RuleProvider


@cache
def rule_providers() -> tuple[RuleProvider, ...]:
    """The installed providers, by name."""
    providers = []
    for point in sorted(installed_entry_points(group=RULE_GROUP), key=lambda p: p.name):
        provider = point.load()
        if not isinstance(provider, RuleProvider):
            raise TypeError(f"{RULE_GROUP} entry point {point.name!r} is not a RuleProvider: {point.value}")
        providers.append(provider)
    missing = sorted(set(OWN_RULE_PROVIDERS) - {p.name for p in providers})
    if missing:
        raise RuntimeError(
            f"qlctool's own rule providers are not installed ({', '.join(missing)}): "
            "run `.venv/bin/pip install -e '.[dev]'` in tools/qlctool so its entry points are written"
        )
    return tuple(providers)
```

`qlctool/checks/bound_widgets.py`: move `BOUND_WIDGETS = ("Button", "Slider", "SpeedDial", "Frame", "XYPad", "CueList")`
out of `rule_pad_input.py:36`, under the docstring
`"""The console widgets that can carry an external input binding."""`.

`qlctool/checks/pad_bindings.py`: move `_bindings` out of `rule_pad_input.py:89-100`
as the public function:

```python
"""Every input channel a console widget listens on, and the widgets listening on it."""

from lxml import etree

from ..xmlutil import findall_local, localname
from .bound_widgets import BOUND_WIDGETS


def pad_bindings(root: etree._Element) -> dict[int, list[str]]:
    """Channel -> captions of the widgets bound to it. Key-only `<Input>`s bind a keyboard, not a pad."""
    bindings: dict[int, list[str]] = {}
    for element in root.iter():
        if localname(element) not in BOUND_WIDGETS:
            continue
        caption = element.attrib.get("Caption") or localname(element)
        for source in findall_local(element, "Input"):
            if "Channel" not in source.attrib:
                continue
            bindings.setdefault(int(source.attrib["Channel"]), []).append(caption)
    return bindings
```

`qlctool/checks/rule_pad_input.py`: delete `BOUND_WIDGETS` and `_bindings`; import
`pad_bindings`; `bindings = _bindings(root)` -> `bindings = pad_bindings(root)`; drop
imports that become unused.

`qlctool/controllers/smc_pad_applies.py`:

```python
"""Whether a workspace is bound to a MIDI pad at all."""

from lxml import etree

from ..checks.pad_bindings import pad_bindings


def smc_pad_applies(root: etree._Element) -> bool:
    """True when any widget listens on an input channel - what `rule_pad_input` checks."""
    return bool(pad_bindings(root))
```

`qlctool/controllers/smc_pad_check.py`:

```python
"""The SMC-PAD's rules over one workspace."""

from ..checks.finding import Finding
from ..checks.rule_context import RuleContext
from ..checks.rule_pad_input import check_pad_input


def smc_pad_check(context: RuleContext) -> list[Finding]:
    """Bindings the pad cannot send, doubled channels, and a missing MIDI input patch."""
    return check_pad_input(context.root)
```

`qlctool/controllers/smc_pad_rules.py`:

```python
"""The SMC-PAD's rule provider, registered under `qlctool.rules` as `smc-pad`."""

from ..checks.rule_provider import RuleProvider
from .smc_pad_applies import smc_pad_applies
from .smc_pad_check import smc_pad_check

SMC_PAD_RULES = RuleProvider(name="smc-pad", applies=smc_pad_applies, check=smc_pad_check)
```

`qlctool/controllers/tablet_desk_applies.py`:

```python
"""Whether a workspace was generated with the tablet desk."""

from lxml import etree

from ..desk_frame_identifier import desk_frame_identifier
from ..desk_function_path import DESK_FUNCTION_PATH
from ..desk_widgets import desk_widgets
from ..names.default_names import default_names
from ..xmlutil import find_local, iter_local


def tablet_desk_applies(root: etree._Element) -> bool:
    """True when the desk's burst frame or any of its burst cues is in the workspace.

    Either is enough: a burst frame deleted by hand leaves its cues behind, and
    that half-removed desk is exactly what `rule_desk_bursts` must still see.
    """
    names = default_names()
    for widget in desk_widgets(root):
        if widget.kind in ("Frame", "SoloFrame") and desk_frame_identifier(widget.caption, names) == "desk_bursts":
            return True
    engine = find_local(root, "Engine")
    return engine is not None and any(
        function.get("Path") == DESK_FUNCTION_PATH for function in iter_local(engine, "Function")
    )
```

`qlctool/controllers/tablet_desk_check.py`:

```python
"""The tablet desk's rules over one workspace."""

from ..checks.finding import Finding
from ..checks.rule_context import RuleContext
from ..checks.rule_desk_bursts import check_desk_bursts


def tablet_desk_check(context: RuleContext) -> list[Finding]:
    """Every held accent has one verified, bounded burst (2026-09-13)."""
    return check_desk_bursts(context.graph, context.root)
```

`qlctool/controllers/tablet_desk_rules.py`:

```python
"""The tablet desk's rule provider, registered under `qlctool.rules` as `tablet_desk`."""

from ..checks.rule_provider import RuleProvider
from .tablet_desk_applies import tablet_desk_applies
from .tablet_desk_check import tablet_desk_check

TABLET_DESK_RULES = RuleProvider(name="tablet_desk", applies=tablet_desk_applies, check=tablet_desk_check)
```

`qlctool/checks/run.py`:
- Delete imports `from .rule_desk_bursts import check_desk_bursts` and
  `from .rule_pad_input import check_pad_input`; delete line 98
  `findings += check_desk_bursts(graph, root)` and line 155
  `findings += check_pad_input(root)`.
- Add `from collections.abc import Sequence`, `from .rule_context import RuleContext`,
  `from .rule_provider import RuleProvider`, `from .rule_providers import rule_providers`.
- Signature gains `providers: Sequence[RuleProvider] | None = None`.
- Before the final `return sorted(...)`:
  ```python
      context = RuleContext(root=root, graph=graph, groups=groups, entries=entries, states=states)
      for provider in rule_providers() if providers is None else providers:
          if provider.applies(root):
              findings += provider.check(context)
  ```
- Add one sentence to the module docstring: controller rules come from the
  `qlctool.rules` entry points (`checks/rule_providers.py`) and run only where they apply.

`pyproject.toml`, after `[project.scripts]`:

```toml
[project.entry-points."qlctool.rules"]
smc-pad = "qlctool.controllers.smc_pad_rules:SMC_PAD_RULES"
tablet_desk = "qlctool.controllers.tablet_desk_rules:TABLET_DESK_RULES"
```

- [ ] **Step 6: Reinstall so the entry points exist, and prove it**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -c "from importlib.metadata import entry_points; print(sorted(e.name for e in entry_points(group='qlctool.rules')))"
```
Expected: `['smc-pad', 'tablet_desk']`. (The venv has no setuptools, so pip
fetches it into its isolated build environment: this step needs the network.)

- [ ] **Step 7: Run the tests**

```bash
.venv/bin/python -m pytest tests/test_controllers.py tests/test_check.py tests/test_input_profile.py tests/test_live_console.py -q
```
Expected: all pass. If `test_a_show_without_controllers_passes_every_check`
fails, a core rule depends on a controller: stop and report the finding - do not
weaken a rule to make it pass.

- [ ] **Step 8: Gates** - Global Constraint 2 plus ruff on touched files. The
  three `qlctool check` runs now reach the desk and pad rules through the
  registry and must still print `522 botones revisados, ningun problema`.

- [ ] **Step 9: Commit**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add tools/qlctool/qlctool/description tools/qlctool/qlctool/vibra tools/qlctool/qlctool/controllers \
  tools/qlctool/qlctool/checks/rule_context.py tools/qlctool/qlctool/checks/rule_provider.py \
  tools/qlctool/qlctool/checks/rule_group.py tools/qlctool/qlctool/checks/own_rule_providers.py \
  tools/qlctool/qlctool/checks/rule_providers.py tools/qlctool/qlctool/checks/bound_widgets.py \
  tools/qlctool/qlctool/checks/pad_bindings.py tools/qlctool/qlctool/checks/rule_pad_input.py \
  tools/qlctool/qlctool/checks/run.py tools/qlctool/qlctool/generate/bind_pad.py \
  tools/qlctool/qlctool/generate/live_console.py tools/qlctool/qlctool/generate/canonical_show.py \
  tools/qlctool/qlctool/generate/desk_bursts.py tools/qlctool/qlctool/desk_function_path.py \
  tools/qlctool/pyproject.toml tools/qlctool/codeality-py.toml tools/qlctool/tests/test_controllers.py
git commit -m "feat(qlctool): controllers are optional profiles, their checks a rule-provider registry" \
  -m "The SMC-PAD becomes a MidiPadProfile and the tablet desk a switch, both applied only when a description asks for them. Their checks leave checks/run.py and return as RuleProviders under the qlctool.rules entry points, run only where they apply; a missing own provider is an error, because a desk check that silently stops running looks like a clean desk. Vibra keeps both, byte for byte." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
```

---

### Task 8: The TOML loader, `newshow --description`, and Vibra written out

Spec step 5. `load_show_description(path, root)` reads a description with
`tomllib`, resolves every name through `Names`, validates fixture groups against
the patch (as `load_stage_plot` validates fixture ids), and returns a
`ShowDescription`. `newshow --description FILE` regenerates from it. Vibra's
three descriptions are written with today's exact values (rulings R5, R6).

**Files:**
- Create: `qlctool/description/rig_files.py`, `qlctool/description/load_show_description.py`,
  `qlctool/description/description_workspace.py`
- Create: `qlctool/description/reading/__init__.py`, `.../description_sections.py`,
  `.../read_toml_file.py`, `.../reject_unknown_keys.py`, `.../table_at.py`,
  `.../rgb_value.py`, `.../milliseconds.py`, `.../beat_timing_value.py`, `.../named.py`,
  `.../read_show.py`, `.../read_names.py`, `.../read_palette.py`, `.../read_matrices.py`,
  `.../read_timing.py`, `.../read_tuning.py`, `.../read_console.py`,
  `.../read_controllers.py`, `.../read_rig.py`
- Create: `QLC+ Setups/vibra.toml`, `QLC+ Setups/vibra-beats.toml`, `QLC+ Setups/vibra-split.toml`
- Create: `tests/test_load_show_description.py`
- Modify: `qlctool/description/show_description.py` (`name`, `rig`), `qlctool/vibra/description.py`
  (`name="Vibra"`), `qlctool/cli.py` (`cmd_newshow` 326-363, parser 705-735),
  `tests/vibra_baseline.json` (`description` per entry), `tests/test_vibra_byte_identity.py`,
  `AGENTS.md`, `tools/qlctool/README.md`, `TODO.md`

**Interfaces:**
- Produces:
  - `RigFiles(workspace: Path | None = None, output: Path | None = None, stage_plot: Path | None = None)`; `ShowDescription.name: str = ""`, `ShowDescription.rig: RigFiles = RigFiles()`.
  - `load_show_description(path: str | Path, root: etree._Element) -> ShowDescription` (identifier-keyed; `ValueError` naming the file and the section for every problem).
  - `description_workspace(path: str | Path) -> Path` (the `[rig] workspace`, resolved against the description's folder).
  - TOML schema: `[show] name, language`; `[rig] workspace (required), output, stage_plot`; `[palette] primary, simple, white, matrix_colors, analogous_pairs, key_split_pairs, complementary_pairs` + `[palette.colors]`; `[[groups.<group>.matrices]] script, colors, properties`; `[timing] bpm, beats, levels{ambient_s,party_s,peak_s,dynamic_s}, dynamic{chase_s,pingpong_s}, panels{effects_s,manual_s}, prism_step_s, matrix_beats{hold,fade}` + `[timing.beat_timings] <function> = {hold, fade}`; `[fixture_tuning] beam_focus, prism_spin_slow, strobe{fast,slow}, talk_white`; `[console] canvas{width,height}, flash_functions` + `[console.keys] <function> = "<key>"`; `[controllers] midi_pad, tablet_desk`; `[names.<lang>] <identifier> = "<word>"`.
  - CLI: `qlctool newshow [workspace] --description FILE [--out] [--plot] [--beats] ...`.
- Consumes: everything above; `fixture_groups(root)` for the patch check; `MIDI_PADS`; `shipped_languages`; `GENERATOR_LANGUAGE`.

- [ ] **Step 1: Write the three Vibra descriptions**

`QLC+ Setups/vibra.toml` (generated on 2026-09-24 from today's constants by
reading them back; every value below is today's):

```toml
# The Vibra show, described: every value the generator used to hard-code for it.
# Regenerate:  cd tools/qlctool && .venv/bin/qlctool newshow --description "../../QLC+ Setups/vibra.toml" --validate
# Format: docs/superpowers/specs/2026-09-24-show-description-design.md

[show]
name = "Vibra"
language = "es"

[rig]
workspace = "Vibra.qxw"
stage_plot = "vibra-stage-plot.json"

[controllers]
midi_pad = "smc-pad"
tablet_desk = true

[palette]
primary = ["red", "green", "blue", "ultraviolet", "yellow", "cyan", "magenta", "white", "orange", "pink"]
simple = ["red", "yellow", "green", "cyan", "blue", "magenta"]
white = "white"
matrix_colors = ["red", "green", "blue", "amber", "magenta", "cyan"]
analogous_pairs = [["red", "yellow"], ["amber", "red"], ["red", "magenta"], ["magenta", "blue"], ["cyan", "blue"], ["green", "cyan"], ["yellow", "green"]]
key_split_pairs = [["blue", "red"], ["red", "blue"]]
complementary_pairs = [["amber", "blue"], ["yellow", "blue"], ["red", "cyan"], ["magenta", "green"], ["red", "blue"]]

[palette.colors]
red = [255, 0, 0]
fire_red = [255, 20, 0]
orange = [255, 127, 0]
amber = [255, 183, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
mint_green = [0, 255, 128]
cyan = [0, 255, 255]
light_blue = [0, 200, 255]
sky_blue = [0, 127, 255]
blue = [0, 0, 255]
deep_blue = [0, 35, 255]
purple = [85, 0, 255]
ultraviolet = [160, 0, 255]
magenta = [255, 0, 255]
fuchsia = [255, 0, 176]
pink = [255, 0, 100]
white = [255, 255, 255]

[[groups.BarrasLed.matrices]]
script = "Sine Wave"
colors = ["red", "blue"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Lines"
colors = ["green"]
properties = { linesType = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Marquee"
colors = ["yellow", "blue"]
properties = { marquee = "Forward", marqueeCount = "3" }

[[groups.BarrasLed.matrices]]
script = "Plasma"
colors = ["cyan"]
properties = { presetIndex = "Rainbow" }

[[groups.BarrasLed.matrices]]
script = "Alternate"
colors = ["blue", "red"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Alternate"
colors = ["cyan", "pink"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Alternate"
colors = ["green", "yellow"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Opposite"
colors = ["green"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Fill From Center"
colors = ["orange"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Stripes From Center"
colors = ["purple"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "Random Column"
colors = ["yellow"]

[[groups.BarrasLed.matrices]]
script = "Fill Unfill"
colors = ["pink"]
properties = { orientation = "Horizontal" }

[[groups.BarrasLed.matrices]]
script = "One By One"
colors = ["cyan"]

[[groups.Cabezas.matrices]]
script = "One By One"
colors = ["cyan"]

[[groups.Cabezas.matrices]]
script = "Fill Unfill"
colors = ["orange"]
properties = { orientation = "Horizontal" }

[[groups.Cabezas.matrices]]
script = "Noise"
colors = ["pink"]
properties = { noisePercentage = "Medium" }

[[groups.Cabezas.matrices]]
script = "Alternate"
colors = ["mint_green", "deep_blue"]
properties = { orientation = "Horizontal" }

[[groups.Cabezas.matrices]]
script = "Opposite"
colors = ["light_blue"]
properties = { orientation = "Horizontal" }

[[groups.Cabezas.matrices]]
script = "Random Column"
colors = ["fuchsia"]

[[groups.PAR.matrices]]
script = "Circular"
colors = ["red"]
properties = { circularMode = "Radar" }

[[groups.PAR.matrices]]
script = "3D Starfield"
colors = ["light_blue"]

[[groups.PAR.matrices]]
script = "Gradient"
colors = ["amber"]
properties = { presetIndex = "Rainbow", presetSize = "5", orientation = "Horizontal" }

[[groups.PAR.matrices]]
script = "Fill From Center"
colors = ["fire_red"]
properties = { orientation = "Horizontal" }

[[groups.PAR.matrices]]
script = "Stripes From Center"
colors = ["sky_blue"]
properties = { orientation = "Horizontal" }

[[groups.PAR.matrices]]
script = "Alternate"
colors = ["pink", "cyan"]
properties = { orientation = "Horizontal" }

[timing]
bpm = 120
levels = { ambient_s = 240, party_s = 480, peak_s = 40, dynamic_s = 240 }
dynamic = { chase_s = 30, pingpong_s = 8 }
panels = { effects_s = 480, manual_s = 240 }
prism_step_s = 8
matrix_beats = { hold = 4, fade = 0 }

[timing.beat_timings]
colour_wheel = { hold = 8, fade = 1 }
soft_movements = { hold = 64, fade = 10 }
wash_movements = { hold = 32, fade = 10 }
beam_movements = { hold = 32, fade = 10 }
fast_washes = { hold = 16, fade = 0 }
fast_beams = { hold = 16, fade = 0 }
gobo_animation = { hold = 16, fade = 0 }
prism_animation = { hold = 32, fade = 0 }
dimmer_chase = { hold = 4, fade = 0 }
dimmer_pingpong = { hold = 2, fade = 0 }

[fixture_tuning]
beam_focus = 127
prism_spin_slow = 25
strobe = { fast = 0.97, slow = 0.785 }
talk_white = [255, 214, 170]

[console]
canvas = { width = 1440, height = 900 }
flash_functions = ["flash_full", "flash_half", "flash_colour", "smoke_on", "vertical_smoke_now", "bass_hit", "strobe_fast", "strobe_medium", "stage_aim"]

[console.keys]
auto = "Q"
talk_moment = "F1"
calm_moment = "F2"
party_moment = "F3"
frenzy_moment = "F4"
full_white = "X"
all_black = "º"
flash_full = "Space"
flash_half = "-"
flash_colour = "."
smoke_on = "H"
vertical_smoke_now = "U"
strobe_fast = "F"
strobe_medium = "T"
colour_wheel = "W"
simple_wheel = "C"
pastel_wheel = "L"
multicolour_wheel = "R"
mix_wheel = "E"
head_movements = "A"
gobo_animation = "G"
prism_animation = "P"
rainbow_together = "'"
rainbow_steps = "¡"
smoke_auto = "J"
vertical_smoke = "N"
dimmer_chase = "V"
dimmer_chase_2 = "B"
dimmer_sequence = "K"
dimmer_pingpong = "Z"
strobe_on = "S"
strobe_off = "D"
```

`QLC+ Setups/vibra-beats.toml`: `cp "QLC+ Setups/vibra.toml" "QLC+ Setups/vibra-beats.toml"`, then
make exactly these edits:
- line 2 `vibra.toml` -> `vibra-beats.toml`, and add a line 3:
  `# The same show with the chases on the music's beat: pick an audio input in QLC+'s Configuration, or nothing advances.`
- `[rig]` becomes:
  ```toml
  [rig]
  workspace = "Vibra.qxw"
  output = "Vibra-beats.qxw"
  stage_plot = "vibra-stage-plot.json"
  ```
- under `[timing]`, a new first line `beats = true`.

`QLC+ Setups/vibra-split.toml`: `cp "QLC+ Setups/vibra.toml" "QLC+ Setups/vibra-split.toml"`, then:
- line 2 `vibra.toml` -> `vibra-split.toml`;
- `[rig]` becomes `workspace = "Vibra-split.qxw"` and `stage_plot = "vibra-stage-plot-split.json"`.

- [ ] **Step 2: Write the failing tests**

`tests/test_load_show_description.py`:

```python
"""A show description is read from TOML and checked against its patch (2026-09-24, spec step 5)."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from qlctool.cli import main
from qlctool.description.controller_settings import ControllerSettings
from qlctool.description.load_show_description import load_show_description
from qlctool.description.rig_files import RigFiles
from qlctool.vibra.description import vibra_description
from qlctool.workspace import Workspace

TESTS = Path(__file__).resolve().parent
SETUPS = TESTS.parents[2] / "QLC+ Setups"
BASELINE = json.loads((TESTS / "vibra_baseline.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def patch_root():
    return Workspace.load(SETUPS / "Vibra.qxw").root


def _write(tmp_path, text):
    path = tmp_path / "show.toml"
    path.write_text('[rig]\nworkspace = "Vibra.qxw"\n' + text, encoding="utf-8")
    return path


def test_vibra_toml_is_the_vibra_description(patch_root):
    loaded = load_show_description(SETUPS / "vibra.toml", patch_root)
    vibra = vibra_description()
    assert replace(loaded, rig=RigFiles()) == vibra
    assert list(loaded.colours.palette) == list(vibra.colours.palette)
    assert list(loaded.console.keys) == list(vibra.console.keys)
    assert loaded.rig == RigFiles(
        workspace=SETUPS / "Vibra.qxw", stage_plot=SETUPS / "vibra-stage-plot.json"
    )


@pytest.mark.parametrize(
    ("name", "workspace", "beats"),
    [("vibra-beats.toml", "Vibra.qxw", True), ("vibra-split.toml", "Vibra-split.qxw", False)],
)
def test_the_variants_differ_only_in_their_rig_and_clock(name, workspace, beats):
    loaded = load_show_description(SETUPS / name, Workspace.load(SETUPS / workspace).root)
    assert loaded.timing.beats is beats
    unrigged = replace(loaded, rig=RigFiles(), timing=replace(loaded.timing, beats=False))
    assert unrigged == vibra_description()


def test_the_smallest_description_is_a_rig(tmp_path, patch_root):
    loaded = load_show_description(_write(tmp_path, ""), patch_root)
    assert loaded.controllers == ControllerSettings()
    assert loaded.colours == vibra_description().colours
    assert loaded.rig.workspace == tmp_path / "Vibra.qxw"


def test_names_in_any_language_are_the_same_colour(tmp_path, patch_root):
    loaded = load_show_description(
        _write(tmp_path, '[palette]\nprimary = ["Rojo", "red", "AZUL"]\n'), patch_root
    )
    assert loaded.colours.primary == ("red", "red", "blue")


@pytest.mark.parametrize(
    ("text", "complaint"),
    [
        ('[palette]\nprimary = ["Roja"]\n', "Rojo"),
        ('[[groups.Laser.matrices]]\nscript = "Fill"\ncolors = ["red"]\n', "Laser.*the patch has: BarrasLed"),
        ("[pallete]\n", "pallete"),
        ('[names.es]\nparty_momment = "Fiesta"\n', "party_momment.*party_moment"),
        ('[controllers]\nmidi_pad = "launchpad"\n', "smc-pad"),
        ('[show]\nlanguage = "fr"\n', "shipped"),
        ('[palette.colors]\nred = [256, 0, 0]\n', "0-255"),
        ("[timing]\nbpm = 0\n", "bpm"),
    ],
)
def test_a_bad_description_is_refused_with_what_is_wrong(tmp_path, patch_root, text, complaint):
    with pytest.raises(ValueError, match=complaint):
        load_show_description(_write(tmp_path, text), patch_root)


def test_newshow_writes_vibra_from_its_description(tmp_path):
    out = tmp_path / "Vibra.qxw"
    assert main(["newshow", "--description", str(SETUPS / "vibra.toml"), "--out", str(out)]) == 0
    assert hashlib.sha256(out.read_bytes()).hexdigest() == BASELINE["Vibra.qxw"]["sha256"]
```

Append to `tests/test_vibra_byte_identity.py`:

```python
def test_the_three_vibra_descriptions_regenerate_byte_for_byte(tmp_path):
    hashes = regenerate_vibra(tmp_path, use_descriptions=True)
    assert hashes == {name: entry["sha256"] for name, entry in BASELINE.items()}
```

`tests/vibra_baseline.json`: add `"description": "vibra.toml"`, `"description": "vibra-beats.toml"`,
`"description": "vibra-split.toml"` to the three entries respectively.

- [ ] **Step 3: Run them and watch them fail**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_load_show_description.py tests/test_vibra_byte_identity.py -q -n 0
```
Expected: `ModuleNotFoundError: No module named 'qlctool.description.load_show_description'`.

- [ ] **Step 4: Implement the readers**

`qlctool/description/rig_files.py`:

```python
"""Where a description's patch, stage plot and output live."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RigFiles:
    """Paths resolved against the description's folder; None where it does not say.

    `output` None means the workspace itself, regenerated in place.
    """

    workspace: Path | None = None
    output: Path | None = None
    stage_plot: Path | None = None
```

`qlctool/description/show_description.py`: import `RigFiles`; add last fields
`name: str = ""` and `rig: RigFiles = RigFiles()`. `qlctool/vibra/description.py`:
`spoken` gains `name="Vibra"`.

`qlctool/description/reading/__init__.py`:

```python
"""One reader per section of a show description's TOML."""
```

`qlctool/description/reading/description_sections.py`:

```python
"""The top-level sections a show description may have."""

DESCRIPTION_SECTIONS: frozenset[str] = frozenset(
    {"show", "rig", "palette", "groups", "timing", "fixture_tuning", "console", "controllers", "names"}
)
```

`qlctool/description/reading/read_toml_file.py`:

```python
"""Parse a description file, naming the file when it is not TOML."""

import tomllib
from pathlib import Path
from typing import Any


def read_toml_file(path: Path) -> dict[str, Any]:
    """The parsed document; a ValueError naming the file on a syntax error."""
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"{path}: not valid TOML: {error}") from error
```

`qlctool/description/reading/reject_unknown_keys.py`:

```python
"""Refuse a key a section does not define - a typo must not become a silent default."""

from collections.abc import Iterable, Mapping
from typing import Any


def reject_unknown_keys(table: Mapping[str, Any], allowed: Iterable[str], where: str) -> None:
    """Raise listing the unknown keys and the allowed ones."""
    known = set(allowed)
    unknown = sorted(set(table) - known)
    if unknown:
        raise ValueError(
            f"{where}: unknown key(s) {', '.join(unknown)}; allowed: {', '.join(sorted(known))}"
        )
```

`qlctool/description/reading/table_at.py`:

```python
"""A sub-table of a description, empty when absent, refused when not a table."""

from collections.abc import Mapping
from typing import Any


def table_at(parent: Mapping[str, Any], key: str, where: str) -> Mapping[str, Any]:
    """`parent[key]` as a table, or an empty one when the key is not there."""
    value = parent.get(key, {})
    if not isinstance(value, dict):
        raise ValueError(f"{where}: {key} must be a table")
    return value
```

`qlctool/description/reading/rgb_value.py`:

```python
"""A colour as the description writes it: three whole numbers 0-255."""

from typing import Any

from ...argb import RGB


def rgb_value(value: Any, where: str) -> RGB:
    """The (r, g, b) tuple, or a ValueError saying what a colour is."""
    if not (
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(c, int) and not isinstance(c, bool) and 0 <= c <= 255 for c in value)
    ):
        raise ValueError(f"{where}: a colour is three whole numbers 0-255, got {value!r}")
    return (value[0], value[1], value[2])
```

`qlctool/description/reading/milliseconds.py`:

```python
"""A duration the description gives in seconds, as the milliseconds QLC+ counts."""

from typing import Any


def milliseconds(seconds: Any, where: str) -> int:
    """Seconds -> whole milliseconds; a ValueError for anything but a positive number."""
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds <= 0:
        raise ValueError(f"{where}: a duration is a positive number of seconds, got {seconds!r}")
    return round(seconds * 1000)
```

`qlctool/description/reading/beat_timing_value.py`:

```python
"""A step timing in beats: `{ hold = 8, fade = 1 }`."""

from typing import Any

from ...generate.beat_tempo import BeatTiming
from .reject_unknown_keys import reject_unknown_keys


def beat_timing_value(value: Any, where: str) -> BeatTiming:
    """The BeatTiming, with a positive hold and a fade of zero or more."""
    if not isinstance(value, dict):
        raise ValueError(f"{where}: a beat timing is {{ hold = <beats>, fade = <beats> }}")
    reject_unknown_keys(value, ("hold", "fade"), where)
    hold, fade = value.get("hold"), value.get("fade", 0)
    numbers = all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in (hold, fade))
    if not numbers or hold <= 0 or fade < 0:
        raise ValueError(f"{where}: hold is a positive number of beats and fade zero or more")
    return BeatTiming(hold=hold, fade=fade)
```

`qlctool/description/reading/named.py`:

```python
"""One name from a description, resolved to its identifier, with the file in the error."""

from typing import Any

from ...names.name_resolution_error import NameResolutionError
from ...names.names import Names


def named(names: Names, name: Any, section: str, where: str) -> str:
    """The identifier `name` spells in `section`; a ValueError that says where otherwise."""
    if not isinstance(name, str):
        raise ValueError(f"{where}: expected a name, got {name!r}")
    try:
        return names.identify(name, (section,))
    except NameResolutionError as error:
        raise ValueError(f"{where}: {error}") from error
```

`qlctool/description/reading/read_show.py`:

```python
"""[show]: the show's name and the language its names are written in."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ...names.generator_language import GENERATOR_LANGUAGE
from ...names.shipped_languages import shipped_languages
from .reject_unknown_keys import reject_unknown_keys


def read_show(table: Mapping[str, Any], path: Path) -> tuple[str, str]:
    """(name, language). The name defaults to the file's stem, the language to Spanish (R6)."""
    where = f"{path}: [show]"
    reject_unknown_keys(table, ("name", "language"), where)
    name = table.get("name", path.stem)
    language = table.get("language", GENERATOR_LANGUAGE)
    if not isinstance(name, str) or not name:
        raise ValueError(f"{where} name must be a non-empty string")
    if language not in shipped_languages():
        raise ValueError(
            f"{where} no catalogue for language {language!r}; shipped: {', '.join(shipped_languages())}"
        )
    return name, language
```

`qlctool/description/reading/read_names.py`:

```python
"""[names.<lang>]: the show's own words for catalogue identifiers."""

from collections.abc import Mapping
from difflib import get_close_matches
from typing import Any

from ...names.default_names import default_names
from ...names.sections import SECTIONS
from ...names.shipped_languages import shipped_languages


def read_names(table: Mapping[str, Any], where: str) -> dict[str, dict[str, str]]:
    """Language -> identifier -> word, every identifier one the catalogues know."""
    known = sorted({i for section in SECTIONS for i in default_names().identifiers(section)})
    overrides: dict[str, dict[str, str]] = {}
    for language, entries in table.items():
        here = f"{where}: [names.{language}]"
        if language not in shipped_languages():
            raise ValueError(f"{here} is not a shipped language: {', '.join(shipped_languages())}")
        if not isinstance(entries, dict):
            raise ValueError(f"{here} must be a table of identifier = \"word\"")
        for identifier, text in entries.items():
            if identifier not in known:
                close = get_close_matches(identifier, known, n=3)
                hint = f"; did you mean {', '.join(close)}?" if close else ""
                raise ValueError(f"{here} {identifier!r} is not a catalogue identifier{hint}")
            if not isinstance(text, str) or not text:
                raise ValueError(f"{here} {identifier} must be a non-empty string")
        overrides[language] = dict(entries)
    return overrides
```

`qlctool/description/reading/read_palette.py`:

```python
"""[palette]: the colours, and every subset and pairing drawn from them."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from ...color_pair import ColorPair
from ...names.names import Names
from ..colour_settings import ColourSettings
from .named import named
from .reject_unknown_keys import reject_unknown_keys
from .rgb_value import rgb_value

LISTS = ("primary", "simple", "matrix_colors")
PAIRS = ("analogous_pairs", "key_split_pairs", "complementary_pairs")


def read_palette(
    table: Mapping[str, Any], base: ColourSettings, names: Names, where: str
) -> ColourSettings:
    """The base colours with what the description states replacing whole tables (R6)."""
    here = f"{where}: [palette]"
    reject_unknown_keys(table, ("colors", "white", *LISTS, *PAIRS), here)
    changes: dict[str, Any] = {}
    if "colors" in table:
        changes["palette"] = {
            named(names, name, "colors", f"{here} colors"): rgb_value(rgb, f"{here} colors.{name}")
            for name, rgb in table["colors"].items()
        }
    for key in LISTS:
        if key in table:
            changes[key] = tuple(named(names, n, "colors", f"{here} {key}") for n in table[key])
    if "white" in table:
        changes["white"] = named(names, table["white"], "colors", f"{here} white")
    for key in PAIRS:
        if key in table:
            pairs = []
            for pair in table[key]:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise ValueError(f"{here} {key} holds [lead, bed] pairs, got {pair!r}")
                lead, bed = (named(names, n, "colors", f"{here} {key}") for n in pair)
                pairs.append((lead, bed) if key == "key_split_pairs" else ColorPair(lead, bed))
            changes[key] = tuple(pairs)
    colours = replace(base, **changes)
    used = [*colours.primary, *colours.simple, *colours.matrix_colors, colours.white]
    used += [n for pair in colours.key_split_pairs for n in pair]
    used += [n for p in (*colours.analogous_pairs, *colours.complementary_pairs) for n in (p.lead, p.bed)]
    missing = sorted(set(used) - set(colours.palette))
    if missing:
        raise ValueError(f"{here} uses colours the palette does not have: {', '.join(missing)}")
    return colours
```

`qlctool/description/reading/read_matrices.py`:

```python
"""[[groups.<group>.matrices]]: hand-tuned RGB scripts, per fixture group of the patch."""

from collections.abc import Mapping
from typing import Any

from lxml import etree

from ...argb import RGB
from ...fixture_group import fixture_groups
from ...matrix_algorithms import CuratedScript
from ...names.names import Names
from .named import named
from .reject_unknown_keys import reject_unknown_keys


def read_matrices(
    table: Mapping[str, Any] | None,
    base: Mapping[str, tuple[CuratedScript, ...]],
    palette: Mapping[str, RGB],
    names: Names,
    root: etree._Element,
    where: str,
) -> dict[str, tuple[CuratedScript, ...]]:
    """Group -> scripts. A stated group must be one the patch has, like a stage plot's ids."""
    matrices = dict(base)
    if table is not None:
        matrices = {}
        patched = [group.name for group in fixture_groups(root)]
        for group, settings in table.items():
            here = f"{where}: [groups.{group}]"
            if group not in patched:
                raise ValueError(
                    f"{here} names a fixture group the patch does not have; "
                    f"the patch has: {', '.join(patched)}"
                )
            reject_unknown_keys(settings, ("matrices",), here)
            scripts = []
            for index, entry in enumerate(settings.get("matrices", [])):
                at = f"{here} matrices[{index}]"
                reject_unknown_keys(entry, ("script", "colors", "properties"), at)
                script, colors = entry.get("script"), entry.get("colors", [])
                properties = entry.get("properties", {})
                if not isinstance(script, str) or not script:
                    raise ValueError(f"{at}: script is the RGB script's name as QLC+ has it")
                if not isinstance(colors, list) or not 1 <= len(colors) <= 2:
                    raise ValueError(f"{at}: colors names one or two palette colours")
                if not isinstance(properties, dict) or not all(isinstance(v, str) for v in properties.values()):
                    raise ValueError(f"{at}: properties are the script's own names with string values")
                identified = tuple(named(names, c, "colors", at) for c in colors)
                scripts.append(CuratedScript(group, script, dict(properties), identified))
            matrices[group] = tuple(scripts)
    missing = sorted({c for s in matrices.values() for m in s for c in m.colors} - set(palette))
    if missing:
        raise ValueError(f"{where}: [groups] matrices use colours the palette lacks: {', '.join(missing)}")
    return matrices
```

`qlctool/description/reading/read_timing.py`:

```python
"""[timing]: BPM, the Beats clock, level lengths in seconds, and step timings in beats."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from ...names.names import Names
from ..show_timing import ShowTiming
from .beat_timing_value import beat_timing_value
from .milliseconds import milliseconds
from .named import named
from .reject_unknown_keys import reject_unknown_keys
from .table_at import table_at


def read_timing(table: Mapping[str, Any], base: ShowTiming, names: Names, where: str) -> ShowTiming:
    """The base timing with every stated value replacing its default."""
    here = f"{where}: [timing]"
    groups = {
        "levels": {"ambient_s": "ambient_ms", "party_s": "party_ms", "peak_s": "peak_ms", "dynamic_s": "dynamic_ms"},
        "dynamic": {"chase_s": "dynamic_chase_ms", "pingpong_s": "dynamic_pingpong_ms"},
        "panels": {"effects_s": "panel_effects_ms", "manual_s": "panel_manual_ms"},
    }
    reject_unknown_keys(table, ("bpm", "beats", "prism_step_s", "matrix_beats", "beat_timings", *groups), here)
    changes: dict[str, Any] = {}
    if "bpm" in table:
        bpm = table["bpm"]
        if isinstance(bpm, bool) or not isinstance(bpm, int) or bpm <= 0:
            raise ValueError(f"{here} bpm is a positive whole number, got {bpm!r}")
        changes["bpm"] = bpm
    if "beats" in table:
        if not isinstance(table["beats"], bool):
            raise ValueError(f"{here} beats is true or false")
        changes["beats"] = table["beats"]
    for key, fields in groups.items():
        section = table_at(table, key, here)
        reject_unknown_keys(section, fields, f"{here} {key}")
        for seconds_key, field_name in fields.items():
            if seconds_key in section:
                changes[field_name] = milliseconds(section[seconds_key], f"{here} {key}.{seconds_key}")
    if "prism_step_s" in table:
        changes["prism_step_ms"] = milliseconds(table["prism_step_s"], f"{here} prism_step_s")
    if "matrix_beats" in table:
        changes["matrix_beats"] = beat_timing_value(table["matrix_beats"], f"{here} matrix_beats")
    if "beat_timings" in table:
        changes["beat_timings"] = {
            named(names, name, "functions", f"{here} beat_timings"): beat_timing_value(
                value, f"{here} beat_timings.{name}"
            )
            for name, value in table_at(table, "beat_timings", here).items()
        }
    return replace(base, **changes)
```

`qlctool/description/reading/read_tuning.py`:

```python
"""[fixture_tuning]: beam focus, prism spin, flash strobe speeds, the talk light's white."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from ..fixture_tuning import FixtureTuning
from .reject_unknown_keys import reject_unknown_keys
from .rgb_value import rgb_value
from .table_at import table_at


def read_tuning(table: Mapping[str, Any], base: FixtureTuning, where: str) -> FixtureTuning:
    """The base tuning with every stated value replacing its default."""
    here = f"{where}: [fixture_tuning]"
    reject_unknown_keys(table, ("beam_focus", "prism_spin_slow", "strobe", "talk_white"), here)
    changes: dict[str, Any] = {}
    for key in ("beam_focus", "prism_spin_slow"):
        if key in table:
            value = table[key]
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError(f"{here} {key} is a DMX value 0-255, got {value!r}")
            changes[key] = value
    strobe = table_at(table, "strobe", here)
    reject_unknown_keys(strobe, ("fast", "slow"), f"{here} strobe")
    for key in ("fast", "slow"):
        if key in strobe:
            value = strobe[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 < value <= 1:
                raise ValueError(f"{here} strobe.{key} is a share of the strobe run, above 0 and up to 1")
            changes[f"strobe_{key}"] = float(value)
    if "talk_white" in table:
        changes["talk_white"] = rgb_value(table["talk_white"], f"{here} talk_white")
    return replace(base, **changes)
```

`qlctool/description/reading/read_console.py`:

```python
"""[console]: the canvas, the held functions, and [console.keys]."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from ...names.names import Names
from ..console_settings import ConsoleSettings
from .named import named
from .reject_unknown_keys import reject_unknown_keys
from .table_at import table_at


def read_console(
    table: Mapping[str, Any], base: ConsoleSettings, names: Names, where: str
) -> ConsoleSettings:
    """The base console with every stated table replacing its default (R6)."""
    here = f"{where}: [console]"
    reject_unknown_keys(table, ("canvas", "keys", "flash_functions"), here)
    changes: dict[str, Any] = {}
    if "canvas" in table:
        canvas = table_at(table, "canvas", here)
        reject_unknown_keys(canvas, ("width", "height"), f"{here} canvas")
        size = (canvas.get("width"), canvas.get("height"))
        if not all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in size):
            raise ValueError(f"{here} canvas needs a positive width and height in pixels")
        changes["canvas"] = size
    if "keys" in table:
        keys: dict[str, str] = {}
        for name, key in table_at(table, "keys", here).items():
            if not isinstance(key, str) or not key:
                raise ValueError(f"{here} keys.{name} must be a key name such as \"Q\" or \"F1\"")
            keys[named(names, name, "functions", f"{here} keys")] = key
        changes["keys"] = keys
    if "flash_functions" in table:
        changes["flash_functions"] = tuple(
            named(names, n, "functions", f"{here} flash_functions") for n in table["flash_functions"]
        )
    return replace(base, **changes)
```

`qlctool/description/reading/read_controllers.py`:

```python
"""[controllers]: the MIDI pad profile and the tablet desk. Omitted means neither."""

from collections.abc import Mapping
from typing import Any

from ...controllers.midi_pads import MIDI_PADS
from ..controller_settings import ControllerSettings
from .reject_unknown_keys import reject_unknown_keys


def read_controllers(table: Mapping[str, Any], where: str) -> ControllerSettings:
    """The stated controllers; none for an absent table, as the spec says."""
    here = f"{where}: [controllers]"
    reject_unknown_keys(table, ("midi_pad", "tablet_desk"), here)
    midi_pad = table.get("midi_pad")
    if midi_pad is not None and midi_pad not in MIDI_PADS:
        raise ValueError(f"{here} midi_pad {midi_pad!r} is not a known pad; known: {', '.join(sorted(MIDI_PADS))}")
    tablet_desk = table.get("tablet_desk", False)
    if not isinstance(tablet_desk, bool):
        raise ValueError(f"{here} tablet_desk is true or false")
    return ControllerSettings(midi_pad=midi_pad, tablet_desk=tablet_desk)
```

`qlctool/description/reading/read_rig.py`:

```python
"""[rig]: the workspace that holds the patch, the stage plot, and where the show is written."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ..rig_files import RigFiles
from .reject_unknown_keys import reject_unknown_keys


def read_rig(table: Mapping[str, Any], path: Path) -> RigFiles:
    """Paths resolved against the description's own folder. `workspace` is required."""
    here = f"{path}: [rig]"
    reject_unknown_keys(table, ("workspace", "output", "stage_plot"), here)
    for key in ("workspace", "output", "stage_plot"):
        if key in table and (not isinstance(table[key], str) or not table[key]):
            raise ValueError(f"{here} {key} must be a file name")
    if "workspace" not in table:
        raise ValueError(f"{here} workspace is required: the QLC+ workspace that holds the patch")
    folder = path.parent
    return RigFiles(
        workspace=folder / table["workspace"],
        output=folder / table["output"] if "output" in table else None,
        stage_plot=folder / table["stage_plot"] if "stage_plot" in table else None,
    )
```

`qlctool/description/load_show_description.py`:

```python
"""Read a show description and check it against the patch it claims to describe.

The patch stays in QLC+; the description says what to do with it. Like a stage
plot (`stage_plot.load_stage_plot`), it is bound to a patch: a matrix tuned for
a fixture group the workspace does not have is refused, loudly, rather than
silently generating nothing. Every section is optional and falls back to the
Vibra show's values, except [controllers], which falls back to none.
"""

from pathlib import Path

from lxml import etree

from ..names.shipped_names import shipped_names
from ..vibra.description import vibra_description
from .reading.description_sections import DESCRIPTION_SECTIONS
from .reading.read_console import read_console
from .reading.read_controllers import read_controllers
from .reading.read_matrices import read_matrices
from .reading.read_names import read_names
from .reading.read_palette import read_palette
from .reading.read_rig import read_rig
from .reading.read_show import read_show
from .reading.read_timing import read_timing
from .reading.read_toml_file import read_toml_file
from .reading.read_tuning import read_tuning
from .reading.reject_unknown_keys import reject_unknown_keys
from .reading.table_at import table_at
from .show_description import ShowDescription


def load_show_description(path: str | Path, root: etree._Element) -> ShowDescription:
    """The description at `path`, named by identifier, validated against `root`'s patch."""
    source = Path(path)
    where = str(source)
    document = read_toml_file(source)
    reject_unknown_keys(document, DESCRIPTION_SECTIONS, where)
    base = vibra_description()
    name, language = read_show(table_at(document, "show", where), source)
    overrides = read_names(table_at(document, "names", where), where)
    names = shipped_names(language, overrides)
    colours = read_palette(table_at(document, "palette", where), base.colours, names, where)
    groups = table_at(document, "groups", where) if "groups" in document else None
    return ShowDescription(
        colours=colours,
        matrices=read_matrices(groups, base.matrices, colours.palette, names, root, where),
        timing=read_timing(table_at(document, "timing", where), base.timing, names, where),
        tuning=read_tuning(table_at(document, "fixture_tuning", where), base.tuning, where),
        console=read_console(table_at(document, "console", where), base.console, names, where),
        language=language,
        names=overrides,
        controllers=read_controllers(table_at(document, "controllers", where), where),
        name=name,
        rig=read_rig(table_at(document, "rig", where), source),
    )
```

`qlctool/description/description_workspace.py`:

```python
"""The workspace a description's [rig] names, needed before the rest can be validated."""

from pathlib import Path

from .reading.read_rig import read_rig
from .reading.read_toml_file import read_toml_file
from .reading.table_at import table_at


def description_workspace(path: str | Path) -> Path:
    """`[rig] workspace`, resolved against the description's folder."""
    source = Path(path)
    rig = read_rig(table_at(read_toml_file(source), "rig", str(source)), source)
    if rig.workspace is None:
        raise ValueError(f"{source}: [rig] workspace is required")
    return rig.workspace
```

- [ ] **Step 5: `newshow --description`**

`qlctool/cli.py`:
- Imports: add `from .description.description_workspace import description_workspace`,
  `from .description.load_show_description import load_show_description`,
  `from .vibra.description import vibra_description`.
- Parser (705-735): `p_new.add_argument("workspace", help=...)` becomes
  `p_new.add_argument("workspace", nargs="?", help="the show to take the patch from (default: the description's [rig] workspace)")`;
  add
  ```python
      p_new.add_argument(
          "--description",
          metavar="FILE",
          help="a show description (.toml): palette, matrices, timing, console, controllers",
      )
  ```
- `cmd_newshow` (326-363): replace its first eleven lines (through `ws.save(out)`) with:
  ```python
  def cmd_newshow(args: argparse.Namespace) -> int:
      if args.workspace is None and args.description is None:
          raise SystemExit("newshow needs a workspace or --description")
      src = Path(args.workspace) if args.workspace else description_workspace(args.description)
      ws = Workspace.load(src)
      description = load_show_description(args.description, ws.root) if args.description else None
      if args.out:
          out = Path(args.out)
      elif description is not None:
          out = description.rig.output or src
      else:
          out = src.with_name("Vibra.qxw")
      plot = args.plot
      if plot is None and description is not None and description.rig.stage_plot is not None:
          plot = str(description.rig.stage_plot)
      shown = description or vibra_description()
      beats = args.beats or shown.timing.beats

      show = build_canonical_show(
          ws,
          FixtureLibrary.load(),
          with_layout=not args.no_buttons,
          plot_path=plot,
          beats=args.beats,
          bpm_tap=args.bpm_tap,
          description=description,
      )
      ws.save(out)
  ```
  In the summary print, `one 1440x900 screen` -> `one {shown.console.canvas[0]}x{shown.console.canvas[1]} screen`;
  `if args.beats:` -> `if beats:`.

- [ ] **Step 6: Run the tests**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool
.venv/bin/python -m pytest tests/test_load_show_description.py tests/test_vibra_byte_identity.py -q -n 0
```
Expected: all pass.

- [ ] **Step 7: The recipe, through the descriptions, into a scratch dir**

```bash
.venv/bin/python tests/vibra_compare.py --descriptions --validate
.venv/bin/python tests/vibra_compare.py --validate
```
Expected: both print three `identical, 0 finding(s), QLC+ loaded it` lines, exit 0.

- [ ] **Step 8: Documentation and backlog**

`AGENTS.md`, section "Regenerating the show (verified recipe)": after the
existing three-command block, add:

````markdown
Since the show-description refactor (2026-09-24) the same three regenerate from
their descriptions, which carry the patch, the plot and every show choice:

```bash
.venv/bin/qlctool newshow --description "../../QLC+ Setups/vibra.toml" --validate
.venv/bin/qlctool newshow --description "../../QLC+ Setups/vibra-beats.toml" --validate
.venv/bin/qlctool newshow --description "../../QLC+ Setups/vibra-split.toml" --validate
```

`.venv/bin/python tests/vibra_compare.py --descriptions --validate` does all
three into a temp dir and fails on any changed byte, check finding or QLC+
complaint. After a pull that touched `pyproject.toml`, run
`.venv/bin/pip install -e '.[dev]'`: the desk and pad checks are found through
its `qlctool.rules` entry points, and `qlctool check` refuses to run without them.
````

`tools/qlctool/README.md`, section "Use", after the `--beats` example, add:

````markdown
# ...or from a show description: the patch stays in QLC+, the .toml says the
# rest (palette, matrices, timing, console, controllers). Names may be written
# in any shipped language: red, Red and rojo are the same colour.
.venv/bin/qlctool newshow --description "../../QLC+ Setups/vibra.toml" --validate
````

and under "Layout" add the line
`- description/, names/, locales/, vibra/, controllers/ - the show description, its name catalogues, Vibra's values, and the optional controller profiles with their rule providers`.

`TODO.md`: under the item that starts `**Objetivo del dueño (2026-09-24)`, add
the indented sub-item:

```markdown
  - [~] Plan A (`docs/superpowers/plans/2026-09-24-show-description-plan-a.md`,
    spec steps 1-5) landed: `ShowDescription`, `qlctool/locales/{en,es}.toml`,
    controller profiles with `qlctool.rules` providers, `newshow --description`
    and `QLC+ Setups/vibra*.toml`, all three workspaces byte-identical. Next,
    before step 7's second rig: **generator names through the catalogue** - the
    generators still write Spanish literals (`live_console`, `play_page`,
    `control_glyph.GLYPHS`, `smc_pad_bindings`, `smc_pad_colors`,
    `color_wheel_match.WHEEL_NAMES`, `canonical_show` master names), so
    `check_generator_vocabulary` refuses `language != "es"` and overrides that
    change a name. Smallest next step: route `canonical_show`'s `master` keys
    through `Names.display`, then the console tables that key by them.
```

- [ ] **Step 9: Gates** - Global Constraint 2 plus ruff on every touched `.py`.

- [ ] **Step 10: Commit and push**

```bash
cd /Users/cristiandeluxe/p/DMX-Fixtures
git add "QLC+ Setups/vibra.toml" "QLC+ Setups/vibra-beats.toml" "QLC+ Setups/vibra-split.toml" \
  tools/qlctool/qlctool/description tools/qlctool/qlctool/vibra/description.py tools/qlctool/qlctool/cli.py \
  tools/qlctool/tests/test_load_show_description.py tools/qlctool/tests/test_vibra_byte_identity.py \
  tools/qlctool/tests/vibra_baseline.json AGENTS.md tools/qlctool/README.md TODO.md
git commit -m "feat(qlctool): newshow --description, and Vibra written as three descriptions" \
  -m "load_show_description reads a show description with tomllib, resolves every name through the catalogues in any shipped language, and refuses a matrix group the patch does not have, the way a stage plot refuses a fixture it cannot place. vibra.toml, vibra-beats.toml and vibra-split.toml hold today's values exactly and regenerate the three workspaces byte for byte." \
  -m "Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw"
git pull --rebase origin main
git push origin main
```

---

## Self-review against the spec

**Coverage of spec steps 1-5.**
- Step 1 (baseline + script): Task 1 - hashes recorded, `regenerate_vibra`,
  `vibra_compare.py`, and a suite test that runs on every task.
- Step 2 (data tables into `ShowDescription`, Vibra default, no behaviour
  change): Tasks 2-3 - palette, primaries, simple, white, pairs, matrix colours,
  curated matrices, timings (levels, dynamic, panels, prism step, BPM, beat
  timings, matrix beats), tuning (beam focus, prism spin, strobe fast/slow, talk
  white), console geometry (canvas) and keys (plus held functions). Byte
  identity checked each time.
- Step 3 (identifiers + `en`/`es` catalogues, names by identifier or any
  spelling, `[show] language`, `[names.<lang>]` overrides): Task 4 (catalogues,
  `Names`, errors that list matches) and Task 5 (identifier-keyed description,
  localisation at the build). **Deviation, ruling R1:** the generators' own
  Spanish literals are not yet catalogue-driven, so the build refuses a non-`es`
  vocabulary; the resolution layer is complete and tested, and the migration is
  logged in `TODO.md` as the first step of the next plan.
- "Checks and the desk map resolve widgets through the identifiers": Task 6
  (desk frames, burst durations, notes). The pad check never matched names; the
  desk burst checks now go through identifiers.
- Step 4 (controller profiles; registry via `qlctool.rules` entry points;
  `qlctool check` runs every applicable check): Task 7, with R3 (no package
  move) and R10 (missing own providers are an error).
- Step 5 (TOML loader via `tomllib`, validated against the patch like
  `stage_plot.py`, `newshow --description`, Vibra's descriptions incl. the beats
  variant): Task 8, with R5 (`[rig] output`, `vibra-beats.toml`) and R6
  (defaults).

**Placeholder scan.** Every new function and class is written out. Moves of
existing tables name source lines and destination (`canonical_show.py`
108-263 -> `qlctool/vibra/*`; `rule_pad_input.py` 36 and 89-100 ->
`checks/bound_widgets.py`, `checks/pad_bindings.py`). Two copies are specified
as exact edits on a copied file (`vibra-beats.toml`, `vibra-split.toml`), not
"similar to". Line numbers are marked as pre-edit and every edit also quotes
the text to find.

**Type consistency.** `ShowDescription` fields in final order: `colours`,
`matrices`, `timing`, `tuning`, `console`, `language="es"`, `names={}`,
`controllers=ControllerSettings()`, `name=""`, `rig=RigFiles()` - Task 2 creates
the four required ones, Task 3 prepends `colours`, Tasks 5, 7 and 8 append
defaulted fields, and `load_show_description` passes them by keyword.
`BeatTiming(hold, fade)` is shared by `ShowTiming`, `beat_timing_value` and
`apply_beat_tempo` (whose `_units` rounds to `int`, so `4` and `4.0` write the
same bytes). `RGB` comes from `qlctool/argb.py` everywhere. `Names` methods
(`identifiers`, `display`, `spellings`, `lookup`, `identify`) are the only API
the desk, the loader and the transforms call. `desk_burst_sources` and
`desk_burst_buttons` keep returning slug-keyed dicts, which is what
`deskmap.py`, `test_check.py` and `Vibra.desk.json` expect. `check_workspace`'s
new `providers` parameter is keyword-with-default, so every existing caller is
unchanged; `rule_providers` is imported as `entry_points as installed_entry_points`
because `checks/entry_points.py` already exports an unrelated `entry_points`.

**Risks the executor should watch.** Task 7 Step 6 needs the network (pip's
isolated build fetches setuptools). Task 7's
`test_a_show_without_controllers_passes_every_check` may expose a core rule that
silently depends on a controller; that is a finding to report, not a test to
loosen. Tasks 2-3 shift line numbers in `canonical_show.py` and
`live_console.py` - locate by quoted text.
