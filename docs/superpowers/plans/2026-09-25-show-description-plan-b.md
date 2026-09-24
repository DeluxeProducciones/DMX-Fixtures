# Show Description, Plan B: QLC+ discovery, controller decoupling, library paths, generator names

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the toolkit-side half of the show description: `qlctool`
finds any installed QLC+ it can run, no core check knows a controller exists,
fixture definitions are found by configuration instead of this repository's
layout, and every name the generator writes comes from the catalogue, so a
description with `language = "en"` produces an English show that passes every
check.

**Architecture:** Four independent strands in dependency order. (1) A
`/Applications/QLC+ *.app` scan plus a Mach-O architecture test feed
`validate.qlcplus_binary`. (2) `RuleProvider` gains a `bounded_latches` hook,
so `rule_held_column` takes the tablet's verified bursts as an argument, and
the list of the toolkit's own providers is read from `pyproject.toml` instead
of being spelled in core. (3) A `ToolkitConfig` read from a `qlctool.toml`
(found by walking up), overridable by an environment variable, the
description's `[rig] fixtures` and a `--fixtures` flag, replaces
`library.REPO_ROOT`. (4) The catalogue grows six sections (`generated`,
`paths`, `console`, `help`, `abbreviations`, `mix_codes`), `Names` gains
`render` for templates, and every generator literal becomes
`names.display(identifier)` or `names.render(identifier, **fields)`, module by
module under a ratchet test, until `check_generator_vocabulary` can be lifted.

**Tech Stack:** Python >= 3.11 (venv 3.14.7), stdlib `tomllib`, `struct`,
`platform`, `string.Formatter`, `ast`; lxml; pytest + pytest-xdist; headless
QLC+ 5.2.2 (`qlcplus-qml`, arm64) for `--validate`.

**Spec:** `docs/superpowers/specs/2026-09-24-show-description-design.md`
(binding). Plan A (`docs/superpowers/plans/2026-09-24-show-description-plan-a.md`)
covered its "Order" steps 1-5; its rulings R1-R10 are recorded in
`~/p/wiki/brain/projects/vibra-dmx.md`, section "The show description: Plan A
decisions (2026-09-24)", and are not re-derived here. This plan covers the
spec's step 6 (library paths), the part of step 3 Plan A deferred under R1
(generated names come from the catalogue through `language`), the R3 coupling
Plan A left in core, and the QLC+ discovery the suite needs. Steps 7 and 8 are
Plan C (`docs/superpowers/plans/2026-09-25-show-description-plan-c.md`), which
depends on this plan.

---

## Global Constraints

Read these before every task. A task that breaks one is not done.

1. **Byte identity.** `Vibra.qxw`, `Vibra-beats.qxw` and `Vibra-split.qxw`
   regenerate byte-identical to `tests/vibra_baseline.json` after every task:
   `10c12af2...b706f8`, `10fff86f...dea882`, `c7f73cd6...d862e`. A changed
   byte is a failed task: stop, find the cause, do not commit until the owner
   accepts the difference. `tests/test_shipped_deskmap.py` holds
   `QLC+ Setups/Vibra.desk.json` byte-identical the same way.
2. **Gates, every task, from `/Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool`:**
   ```bash
   .venv/bin/python -m pytest tests/ -q
   QLCTOOL_QLCPLUS="/Applications/QLC+ 5.2.2.app/Contents/MacOS/qlcplus-qml" .venv/bin/python tests/vibra_compare.py --validate
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-beats.qxw"
   .venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
   ```
   Baseline on 2026-09-25 at `9266c18`: the suite prints `571 passed, 10
   skipped` without `QLCTOOL_QLCPLUS` and `581 passed` (about 68 s) with it;
   after Task 1 it prints `581 passed` or more with no skip and no variable.
   Each `check` prints `522 botones revisados, ningun problema` and exits 0.
   `vibra_compare.py --validate` prints three `identical, 0 finding(s), QLC+
   loaded it` lines and exits 0. Run the suite in the foreground and **never
   pipe it through `tail` or `head`**: the exit code is lost, and a stopped
   suite leaves a headless QLC+ behind that makes later validation pass. The
   QML build opens a window in the background while it validates; that is
   expected. Before the first `--validate`, run `.venv/bin/qlctool install
   --check`; if it exits 1, run `.venv/bin/qlctool install`. Without QLC+ the
   validation cannot run: never claim it passed.
3. **One exported unit and one responsibility per file.** Helpers, constants,
   types and compound operations go in their own files with explicit imports.
   New source files stay under 150 lines, test files under 300
   (`codeality-py.toml`). New pure-data modules go into `[roles] data` in
   `codeality-py.toml`. Style: `ruff.toml` (line length 100, google
   docstrings). Run `ruff check <touched .py>` and `ruff format --check
   <touched .py>` in every task; the tree's pre-existing findings are not
   yours to fix. `mypy` and `codeality-py` are not installed: do not claim
   they passed.
4. **No new runtime dependency.** Everything used here is stdlib or already
   in `pyproject.toml`.
5. **Checks reason about capabilities and the function graph, never a
   function's display name.** Widgets are found by catalogue identifier across
   every shipped spelling (`Names.lookup`), never by comparing with a Spanish
   string.
6. **A malfunction needs a check before its fix** (`CLAUDE.md`): a rule in
   `qlctool/checks/`, a dated regression test in `tests/test_check.py`, the
   gate over every shipped workspace, and only then the generator fix.
7. **Commits.** One commit per task on `main`, English, conventional style as
   in `git log --oneline -20` (`feat(qlctool): ...`, `refactor(qlctool): ...`,
   `test(qlctool): ...`, `docs(...): ...`), stage only the task's paths, no AI
   attribution in subject or body, every message ending with the line
   `Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw`.
   After Task 12, push `main` to `origin` (finished, verified work is pushed).
8. **Never hand-edit a `Vibra*.qxw`**, and never write regenerated output over
   the shipped files: every regeneration goes to a temp dir
   (`vibra_compare.py`, `tmp_path`).
9. **Every checkout reinstalls after a task that changes entry points or
   package data** (R10): `.venv/bin/pip install -e '.[dev]'` in
   `tools/qlctool`. Tasks 2 and 4 change them.

**Rulings this plan makes where the spec is silent or ambiguous** (each is
repeated where it bites):

- B1. *Discovery prefers what runs.* `/Applications/QLC+ <version>.app` bundles
  are scanned, newest version first; within that order every 4.x-style
  `qlcplus` comes before any `qlcplus-qml` (the module docstring's
  preference: only the widgets build loads with no GUI). A binary whose
  Mach-O slices this CPU cannot execute is skipped: on this Mac,
  `QLC+ 4.13.1.app` is x86_64-only and Rosetta is not installed
  (`/Library/Apple/usr/libexec/oah/libRosettaRuntime` is absent, `arch
  -x86_64` says "Bad CPU type"), so discovery picks
  `QLC+ 5.2.2.app/Contents/MacOS/qlcplus-qml`. `QLCTOOL_QLCPLUS` still wins
  over everything.
- B2. *Controller modules stay where they are* (Plan A R3). Only the call
  edges change: no module a core rule imports may import a desk or pad
  module, and `checks/` no longer spells a provider name. The list of the
  toolkit's own providers, which R10 needs, is read from the
  `[project.entry-points."qlctool.rules"]` table of the `pyproject.toml` that
  sits beside the package; a wheel install has none and skips the stale-install
  test (an installed wheel cannot be stale).
- B3. *Fixture directories resolve in this order, first source that names any
  wins:* `qlctool --fixtures DIR` (repeatable) > the description's
  `[rig] fixtures` (relative to the description) > `QLCTOOL_FIXTURES`
  (`os.pathsep`-separated) > the nearest `qlctool.toml` found by walking up
  from the workspace, the description, or the current directory. Within one
  source the first directory wins a model clash, and every one of them beats
  the bundled system definitions. This repository gets a root `qlctool.toml`
  naming `QLC+ Fixtures`, `QLC+ InputProfiles` and `QLC+ Setups/Gobos`.
  `FixtureLibrary.load()` with no argument resolves from the current
  directory. A patched fixture with no definition is a warning on stderr that
  lists the fixtures and the directories searched (it used to be silent).
- B4. *The generator keeps keying functions by display name.* `master` stays
  `dict[str, int]` keyed by the show-language name, so tests that read
  `show.master_ids["Blanco Total"]` keep working for the Spanish show. Every
  identifier-keyed table (`GLYPHS`, `SMC_PAD_BINDINGS`, `FUNCTION_COLORS`,
  `WHEEL_NAMES`, `QUAD_COLORS`, the EFX shape labels, the room states, hits,
  reset strip, smoke rhythms) is localised to display names at the point of
  use with `names.display`.
- B5. *Generators take `names: Names | None = None`,* defaulting to
  `default_names()` (Spanish, every catalogue). `build_canonical_show` passes
  the description's vocabulary down. The standalone commands (`palette`,
  `matrix`, `movement`, `probe`, `layout`) therefore keep writing Spanish, as
  today; giving them `--language` is not in this plan.
- B6. *What stays literal, and why* (the ratchet test's exclusions): QLC+
  engine tokens and XML tags; fixture-definition data (wheel slot names such
  as "Rainbow effect fast to slow", capability presets, EFX algorithm names,
  model names); the words that are the same in both catalogues ("AUTO",
  "Dimmer Chase", "Flash 100%", "Color Beam", "MultiColor", "Gobo", "EFX",
  "LIVE", "CONTROL"), which the scanner does not flag because their `es` and
  `en` values are equal; the `vibra/` package (the Vibra show's own data,
  held equal to `vibra.toml` by R2); the SMC-PAD input profile
  (`generate/input_profile.py`, a device file byte-tested against
  `QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi`); `generate/channel_probe.py` and the
  `"(generado)"` folder of the standalone commands (B5); exception messages;
  `DESK_FUNCTION_PATH = "Desk"` (a marker the desk finds its cues by, not a
  word); the `"· · ·"` separators in help text.
- B7. *Key hints stay inside captions.* "FLASH · Espacio" is one catalogue
  value per language ("FLASH · Space" in English); a test holds the head
  before " · " equal to the matching `captions.hit_*` value, so the desk still
  recognises it.
- B8. *Parsed markers come from templates.* Wherever the console strips a
  prefix or suffix from a function name ("Ciclo ", "Movimiento ",
  "Paneles - ", " + Pixeles"), the marker is the text before or after the
  template's field (`template_affixes`). English templates keep the Spanish
  word order wherever a marker is parsed ("Cycle {what}", "Movement {shape}",
  "{name} + Pixels"). Group wheel captions are rendered from the bank, not
  parsed from the wheel's name.
- B9. *Spellings stay unique per section across languages* (the existing
  `test_names` invariant). Consequences: one `rest_caption` identifier for
  "Reposo"; the reset strip reuses `haze_word` and the `hit_*` captions where
  its word equals theirs; English mix codes avoid every Spanish code
  (Spanish: Ro Ve Az Am Ab Cy Ma Bl Na Rs UV; English: Rd Gn Bu Yw Ar Cy Ma Wh
  Or Pk UV); abbreviation and code identifiers carry a suffix (`yellow_short`,
  `yellow_code`) because identifiers are unique across sections.
- B10. *Check messages and `Finding.rule` names stay Spanish in this plan.*
  The spec lists check messages among the things that get identifiers; that
  is a separate catalogue section and CLI output change, deferred and logged in
  `TODO.md` by Task 12. The desk map's own texts (page titles, section titles,
  burst notes) do move, because the desk is part of the generated show.
- B11. *`[show] language` still defaults to `"es"`.* Plan C decides whether the
  public toolkit's default becomes `"en"`.
- B12. *The workspace's language is read from the workspace.* The desk map
  and the desk checks work out which catalogue a saved workspace was written
  in from the caption of its `room_states` frame
  (`names/workspace_language.py`), falling back to `es`. `deskmap
  --description` passes the description's overrides; `check` does not take a
  description (the desk provider looks names up across every shipped
  spelling, which is language-independent).

---

## File map

New (paths relative to `tools/qlctool` unless they start with the repo root):

```
qlctool/qlcplus_bundles.py                 Task 1  versioned bundles in /Applications
qlctool/mach_o_architectures.py            Task 1  CPU types in a Mach-O header
qlctool/runs_here.py                       Task 1  can this CPU execute it
qlctool/qlcplus_candidates.py              Task 1  ordered, runnable QLC+ binaries
tests/test_qlcplus_discovery.py            Task 1
qlctool/checks/no_bounded_latches.py       Task 2  RuleProvider default
qlctool/checks/declared_rule_providers.py  Task 2  replaces own_rule_providers.py
qlctool/controllers/tablet_desk_bounded_latches.py  Task 2
tests/test_core_rules_know_no_controller.py         Task 2
qlctool/toolkit_config.py                  Task 3  ToolkitConfig dataclass
qlctool/find_toolkit_config.py             Task 3  walk up for qlctool.toml
qlctool/read_toolkit_config.py             Task 3  parse one qlctool.toml
qlctool/toolkit_config_from.py             Task 3  found-or-empty config
qlctool/fixture_dirs.py                    Task 3  B3 resolution order
qlctool/unresolved_fixtures.py             Task 3  patched fixtures with no definition
qlctool/warn_unresolved.py                 Task 3  the stderr warning
qlctool/library_for.py                     Task 3  the CLI's library
qlctool.toml (repo root)                   Task 3
tests/test_fixture_dirs.py                 Task 3
tests/test_no_repo_layout.py               Task 3
qlctool/names/template_fields.py           Task 4
qlctool/names/template_affixes.py          Task 4
qlctool/names/check_override_fields.py     Task 4
tests/generator_literals.py                Task 4  the scanner (test helper)
tests/test_generator_literals.py           Task 4  the ratchet
tests/test_catalogue_templates.py          Task 4
qlctool/efx_shape_identifiers.py           Task 6  replaces SPANISH_LABELS
qlctool/names/workspace_language.py        Task 10
tests/test_english_vibra.py                Task 12
tests/test_pseudo_locale.py                Task 12
```

Modified: `qlctool/validate.py`, `qlctool/checks/{rule_provider,rule_providers,
rule_held_column,run}.py`, `qlctool/controllers/tablet_desk_rules.py`,
`qlctool/library.py`, `qlctool/install_plan.py`, `qlctool/cli.py`,
`qlctool/description/{rig_files.py,reading/read_rig.py}`, `qlctool/names/
{names,sections}.py`, `qlctool/locales/{en,es}.toml`, every
`qlctool/generate/*.py` named in Tasks 5-10, `qlctool/control_glyph.py`,
`qlctool/color_wheel_match.py`, `qlctool/checks/detent_white.py`,
`qlctool/efx_algorithms.py`, `qlctool/desk_policy.py`, `qlctool/deskmap.py`,
`qlctool/desk_burst_note.py`, the tests those touch, `AGENTS.md`,
`tools/qlctool/README.md`, `docs/toolkit.md`, `TODO.md`, `TODO_LOG.md`.

Deleted: `qlctool/checks/own_rule_providers.py` (Task 2),
`qlctool/names/check_generator_vocabulary.py` (Task 12).
Renamed: `qlctool/names/generator_language.py` -> `qlctool/names/default_language.py`
(Task 12).

All paths below are relative to `/Users/cristiandeluxe/p/DMX-Fixtures/tools/qlctool`
unless they start with the repository root (`/Users/cristiandeluxe/p/DMX-Fixtures`).
Sites in existing files are described by content, not line number: line numbers
drift between tasks.

---

### Task 1: Find every installed QLC+ that this Mac can run

**Files:**
- Create: `qlctool/qlcplus_bundles.py`, `qlctool/mach_o_architectures.py`,
  `qlctool/runs_here.py`, `qlctool/qlcplus_candidates.py`
- Modify: `qlctool/validate.py` (`qlcplus_binary`)
- Test: `tests/test_qlcplus_discovery.py`
- Docs: `/Users/cristiandeluxe/p/DMX-Fixtures/AGENTS.md` (the "QLC+ is not
  installed" trap), `/Users/cristiandeluxe/p/DMX-Fixtures/TODO.md` (the
  dev-environment item about the 10 skipped tests and the gobo note),
  `/Users/cristiandeluxe/p/DMX-Fixtures/TODO_LOG.md`

**Interfaces:**
- Consumes: nothing new.
- Produces:
  - `qlcplus_bundles(applications: Path = Path("/Applications")) -> list[tuple[tuple[int, ...], str]]`
  - `mach_o_architectures(header: bytes) -> frozenset[str] | None`
  - `runs_here(executable: str, machine: str | None = None, rosetta: bool | None = None) -> bool`
  - `qlcplus_candidates(fixed: Sequence[str], applications: Path = Path("/Applications"), runnable: Callable[[str], bool] = runs_here) -> list[str]`
  - `validate.qlcplus_binary()` unchanged in signature; now returns the first
    candidate.

- [ ] **Step 1: Write the failing tests**

`tests/test_qlcplus_discovery.py`:

```python
"""2026-09-25: the suite skipped ten QLC+ tests on a Mac with QLC+ 5.2.2 installed.

`DEFAULT_BINARIES` knew `QLC+ 4.app` and `QLC+.app`; the installers name their
bundles `QLC+ 4.13.1.app` and `QLC+ 5.2.2.app`, and the 4.13.1 binary is
x86_64-only on an arm64 Mac with no Rosetta. Discovery scans the versioned
bundles and keeps only what this CPU can execute.
"""

import struct
from pathlib import Path

from qlctool import validate
from qlctool.mach_o_architectures import mach_o_architectures
from qlctool.qlcplus_bundles import qlcplus_bundles
from qlctool.qlcplus_candidates import qlcplus_candidates
from qlctool.runs_here import runs_here

X86_64 = b"\xcf\xfa\xed\xfe" + struct.pack("<i", 0x01000007) + bytes(24)
ARM64 = b"\xcf\xfa\xed\xfe" + struct.pack("<i", 0x0100000C) + bytes(24)
FAT = (
    b"\xca\xfe\xba\xbe"
    + struct.pack(">I", 2)
    + struct.pack(">iiIII", 0x01000007, 3, 0, 0, 0)
    + struct.pack(">iiIII", 0x0100000C, 0, 0, 0, 0)
)


def _binary(applications: Path, bundle: str, name: str, header: bytes) -> str:
    path = applications / bundle / "Contents" / "MacOS" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header)
    return str(path)


def test_the_header_names_its_architectures():
    assert mach_o_architectures(X86_64) == frozenset({"x86_64"})
    assert mach_o_architectures(ARM64) == frozenset({"arm64"})
    assert mach_o_architectures(FAT) == frozenset({"x86_64", "arm64"})
    assert mach_o_architectures(b"#!/bin/sh\n") is None


def test_an_intel_binary_runs_on_arm_only_through_rosetta(tmp_path):
    intel = _binary(tmp_path, "QLC+ 4.13.1.app", "qlcplus", X86_64)
    assert not runs_here(intel, machine="arm64", rosetta=False)
    assert runs_here(intel, machine="arm64", rosetta=True)
    assert runs_here(intel, machine="x86_64", rosetta=False)
    assert not runs_here(str(tmp_path / "missing"), machine="arm64", rosetta=True)


def test_bundles_are_listed_newest_first(tmp_path):
    old = _binary(tmp_path, "QLC+ 4.13.1.app", "qlcplus", X86_64)
    new = _binary(tmp_path, "QLC+ 5.2.2.app", "qlcplus-qml", ARM64)
    _binary(tmp_path, "Not QLC+.app", "qlcplus", ARM64)
    assert qlcplus_bundles(tmp_path) == [((5, 2, 2), new), ((4, 13, 1), old)]
    assert qlcplus_bundles(tmp_path / "absent") == []


def test_the_widgets_build_wins_when_it_can_run(tmp_path):
    old = _binary(tmp_path, "QLC+ 4.13.1.app", "qlcplus", X86_64)
    new = _binary(tmp_path, "QLC+ 5.2.2.app", "qlcplus-qml", ARM64)
    with_rosetta = qlcplus_candidates((), tmp_path, lambda p: runs_here(p, "arm64", True))
    without = qlcplus_candidates((), tmp_path, lambda p: runs_here(p, "arm64", False))
    assert with_rosetta == [old, new]
    assert without == [new]


def test_fixed_paths_follow_the_versioned_bundles_without_repeats(tmp_path):
    new = _binary(tmp_path, "QLC+ 5.2.2.app", "qlcplus-qml", ARM64)
    fixed = _binary(tmp_path / "usr", "bin", "qlcplus-qml", ARM64)
    found = qlcplus_candidates((new, fixed, str(tmp_path / "nowhere")), tmp_path, lambda p: True)
    assert found == [new, fixed]


def test_the_override_still_wins(monkeypatch, tmp_path):
    chosen = _binary(tmp_path, "custom", "qlcplus", ARM64)
    monkeypatch.setenv("QLCTOOL_QLCPLUS", chosen)
    monkeypatch.setattr(validate, "qlcplus_candidates", lambda fixed: ["/elsewhere"])
    assert validate.qlcplus_binary() == chosen


def test_discovery_feeds_the_validator(monkeypatch):
    monkeypatch.delenv("QLCTOOL_QLCPLUS", raising=False)
    monkeypatch.setattr(validate, "qlcplus_candidates", lambda fixed: ["/first", "/second"])
    assert validate.qlcplus_binary() == "/first"
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `.venv/bin/python -m pytest tests/test_qlcplus_discovery.py -q -n 0`
Expected: FAIL with `ModuleNotFoundError: No module named 'qlctool.mach_o_architectures'`.

- [ ] **Step 3: Write the four units**

`qlctool/qlcplus_bundles.py`:

```python
"""Every versioned QLC+ application bundle in a folder, newest version first.

The installers name their bundles `QLC+ 4.13.1.app` and `QLC+ 5.2.2.app`, so a
fixed list of paths finds none of them (2026-09-25: ten validation tests
skipped with QLC+ 5.2.2 installed).
"""

import re
from pathlib import Path


def qlcplus_bundles(applications: Path = Path("/Applications")) -> list[tuple[tuple[int, ...], str]]:
    """(version, executable) for each `qlcplus` / `qlcplus-qml` in a versioned bundle."""
    if not applications.is_dir():
        return []
    found: list[tuple[tuple[int, ...], str]] = []
    for bundle in sorted(applications.glob("QLC+ *.app")):
        match = re.fullmatch(r"QLC\+ (\d+(?:\.\d+)*)\.app", bundle.name)
        if match is None:
            continue
        version = tuple(int(part) for part in match.group(1).split("."))
        for name in ("qlcplus", "qlcplus-qml"):
            executable = bundle / "Contents" / "MacOS" / name
            if executable.is_file():
                found.append((version, str(executable)))
    return sorted(found, key=lambda entry: entry[0], reverse=True)
```

`qlctool/mach_o_architectures.py`:

```python
"""The CPU architectures a Mach-O header says its binary carries."""

import struct


def mach_o_architectures(header: bytes) -> frozenset[str] | None:
    """Architecture names from a thin or universal header; None when it is not Mach-O.

    Only the types QLC+ ships for are named; anything else is its hex cputype.
    """
    names = {0x01000007: "x86_64", 0x0100000C: "arm64", 7: "i386", 12: "arm"}
    magic = header[:4]
    if magic in (b"\xcf\xfa\xed\xfe", b"\xce\xfa\xed\xfe") and len(header) >= 8:
        (cputype,) = struct.unpack_from("<i", header, 4)
        return frozenset({names.get(cputype, hex(cputype))})
    if magic in (b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf") and len(header) >= 8:
        (count,) = struct.unpack_from(">I", header, 4)
        size = 20 if magic == b"\xca\xfe\xba\xbe" else 32
        # A Java class file shares this magic; its "count" is a version in the 40s.
        if count == 0 or count > 16 or len(header) < 8 + count * size:
            return None
        types = [struct.unpack_from(">i", header, 8 + i * size)[0] for i in range(count)]
        return frozenset(names.get(t, hex(t)) for t in types)
    return None
```

`qlctool/runs_here.py`:

```python
"""Whether this Mac can execute a binary, before QLC+ is launched to find out.

An x86_64-only QLC+ on an arm64 Mac without Rosetta fails with "Bad CPU type"
from inside `open -g`, which the validator would read as a QLC+ that never
finished loading.
"""

import platform
from pathlib import Path

from .mach_o_architectures import mach_o_architectures


def runs_here(executable: str, machine: str | None = None, rosetta: bool | None = None) -> bool:
    """True when the file exists and its Mach-O slices include one this CPU runs.

    A file that is not Mach-O (a script, a Linux ELF) is left to the system: True.
    """
    try:
        with open(executable, "rb") as handle:
            header = handle.read(4096)
    except OSError:
        return False
    architectures = mach_o_architectures(header)
    if architectures is None:
        return True
    cpu = machine or platform.machine()
    if cpu in architectures:
        return True
    translated = (
        Path("/Library/Apple/usr/libexec/oah/libRosettaRuntime").exists()
        if rosetta is None
        else rosetta
    )
    return cpu == "arm64" and "x86_64" in architectures and translated
```

`qlctool/qlcplus_candidates.py`:

```python
"""Every QLC+ executable worth trying, best first."""

from collections.abc import Callable, Sequence
from pathlib import Path

from .qlcplus_bundles import qlcplus_bundles
from .runs_here import runs_here


def qlcplus_candidates(
    fixed: Sequence[str],
    applications: Path = Path("/Applications"),
    runnable: Callable[[str], bool] = runs_here,
) -> list[str]:
    """Versioned bundles newest first, then the fixed paths; only what can run.

    The widgets build (`qlcplus`) sorts before the QML build (`qlcplus-qml`)
    whatever its version: it is the only one that loads with no GUI at all.
    """
    ordered = [path for _, path in qlcplus_bundles(applications)]
    ordered += [path for path in fixed if Path(path).is_file()]
    usable = [path for path in dict.fromkeys(ordered) if runnable(path)]
    return sorted(usable, key=lambda path: Path(path).name == "qlcplus-qml")
```

- [ ] **Step 4: Route `qlcplus_binary` through the candidates**

In `qlctool/validate.py` add `from .qlcplus_candidates import qlcplus_candidates`
to the imports and replace the body of `qlcplus_binary` after the override
block (the `for candidate in DEFAULT_BINARIES:` loop) with:

```python
    candidates = qlcplus_candidates(DEFAULT_BINARIES)
    if candidates:
        return candidates[0]
    return shutil.which("qlcplus") or shutil.which("qlcplus-qml")
```

Add one sentence to the module docstring's last paragraph: "Versioned bundles
in /Applications are found too, newest first, and a binary this CPU cannot run
is skipped (`qlcplus_candidates`)."

- [ ] **Step 5: Run the new tests, then the ten that used to skip**

Run: `.venv/bin/python -m pytest tests/test_qlcplus_discovery.py -q -n 0`
Expected: `7 passed`.

Run (no `QLCTOOL_QLCPLUS` in the environment):
`env -u QLCTOOL_QLCPLUS .venv/bin/python -c "from qlctool.validate import qlcplus_binary; print(qlcplus_binary())"`
Expected: `/Applications/QLC+ 5.2.2.app/Contents/MacOS/qlcplus-qml`.

Run: `env -u QLCTOOL_QLCPLUS .venv/bin/python -m pytest tests/ -q`
Expected: `588 passed` (581 + 7), no `skipped`. If any test still skips, the
reason is printed with `-rs`; do not continue until it is zero.

- [ ] **Step 6: Install check against the discovered bundle**

`qlc_gobo_dir()` now answers with the 5.2.2 bundle's `Resources/Gobos`.
Run: `env -u QLCTOOL_QLCPLUS .venv/bin/qlctool install --check`.
Expected: exit 0 with `QLC+ has every one of the repo's 12 file(s)`. If it
exits 1, run `.venv/bin/qlctool install` once and re-run the check.

- [ ] **Step 7: Update the docs and the backlog**

- `AGENTS.md`: the trap that says the validation tests skip unless
  `QLCTOOL_QLCPLUS` is set becomes: "`qlctool` finds `/Applications/QLC+
  <version>.app` by itself, newest first, widgets build before QML, skipping a
  binary this CPU cannot run (the x86_64 `QLC+ 4.13.1.app` on an arm64 Mac
  without Rosetta). `QLCTOOL_QLCPLUS` still overrides it."
- `TODO.md`: close the dev-environment item about the ten skipped tests
  (`[x]`), move it to `TODO_LOG.md` under 2026 / September with the date
  2026-09-25 and the evidence (`588 passed`, no skip, no variable); correct
  the gobo note to say the gobo folder is the discovered bundle's.

- [ ] **Step 8: Gates, then commit**

Run the five gate commands (Global Constraint 2). Then:

```bash
ruff check qlctool/qlcplus_bundles.py qlctool/mach_o_architectures.py qlctool/runs_here.py qlctool/qlcplus_candidates.py qlctool/validate.py tests/test_qlcplus_discovery.py
ruff format --check qlctool/qlcplus_bundles.py qlctool/mach_o_architectures.py qlctool/runs_here.py qlctool/qlcplus_candidates.py tests/test_qlcplus_discovery.py
git add qlctool/qlcplus_bundles.py qlctool/mach_o_architectures.py qlctool/runs_here.py qlctool/qlcplus_candidates.py qlctool/validate.py tests/test_qlcplus_discovery.py ../../AGENTS.md ../../TODO.md ../../TODO_LOG.md
git commit -m "$(cat <<'EOF'
feat(qlctool): find versioned QLC+ bundles this Mac can run

The fixed binary list missed "QLC+ 5.2.2.app", so ten validation tests
skipped on a machine that had QLC+ installed. The x86_64-only 4.13.1 bundle
is skipped on arm64 without Rosetta.

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
EOF
)"
```

---

### Task 2: Core checks stop knowing the controllers exist

**Files:**
- Create: `qlctool/checks/no_bounded_latches.py`,
  `qlctool/checks/declared_rule_providers.py`,
  `qlctool/controllers/tablet_desk_bounded_latches.py`
- Modify: `qlctool/checks/rule_provider.py`, `qlctool/checks/rule_providers.py`,
  `qlctool/checks/rule_held_column.py`, `qlctool/checks/run.py`,
  `qlctool/controllers/tablet_desk_rules.py`
- Delete: `qlctool/checks/own_rule_providers.py`
- Test: `tests/test_core_rules_know_no_controller.py`; modify
  `tests/test_desk_bursts.py`, `tests/test_controllers.py`

**Interfaces:**
- Consumes: `valid_desk_bursts(graph, root, names=None) -> set[int]`
  (unchanged), `RuleContext` (unchanged).
- Produces:
  - `RuleProvider(name, applies, check, bounded_latches=no_bounded_latches)`,
    `bounded_latches: Callable[[RuleContext], frozenset[int]]`
  - `no_bounded_latches(context: RuleContext) -> frozenset[int]`
  - `tablet_desk_bounded_latches(context: RuleContext) -> frozenset[int]`
  - `check_held_column(graph, groups, root, bounded: frozenset[int] = frozenset()) -> list[Finding]`
  - `declared_rule_providers(project: Path | None = None) -> tuple[str, ...]`

- [ ] **Step 1: Write the failing tests**

`tests/test_core_rules_know_no_controller.py`:

```python
"""2026-09-25: Plan A left two controller edges in core (ruling R3's residue).

`rule_held_column` imported `valid_desk_bursts`, and `own_rule_providers`
spelled "smc-pad" and "tablet_desk" inside `checks/`. A show with neither
controller still ran desk code on every check.
"""

import ast
from pathlib import Path

from qlctool.checks.declared_rule_providers import declared_rule_providers
from qlctool.checks.rule_providers import rule_providers
from qlctool.controllers.tablet_desk_rules import TABLET_DESK_RULES

CHECKS = Path(__file__).resolve().parents[1] / "qlctool" / "checks"
CONTROLLER_MODULES = {
    "valid_desk_bursts",
    "rule_desk_bursts",
    "desk_burst_errors",
    "pad_bindings",
    "rule_pad_input",
}


def _checks_imports(module: str) -> set[str]:
    tree = ast.parse((CHECKS / f"{module}.py").read_text(encoding="utf-8"))
    return {
        node.module.split(".")[-1]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module
    }


def test_no_core_rule_reaches_a_controller_module():
    seen: set[str] = set()
    pending = ["run"]
    while pending:
        module = pending.pop()
        if module in seen or not (CHECKS / f"{module}.py").exists():
            continue
        seen.add(module)
        pending += _checks_imports(module) - {"rule_providers"}
    assert not seen & CONTROLLER_MODULES


def test_checks_spell_no_provider_name():
    for source in CHECKS.glob("*.py"):
        text = source.read_text(encoding="utf-8")
        assert '"smc-pad"' not in text and '"tablet_desk"' not in text, source.name


def test_the_declared_providers_are_the_installed_ones():
    assert set(declared_rule_providers()) == {"smc-pad", "tablet_desk"}
    assert set(declared_rule_providers()) <= {p.name for p in rule_providers()}


def test_a_wheel_install_declares_nothing(tmp_path):
    assert declared_rule_providers(tmp_path) == ()


def test_the_desk_vouches_for_its_bursts_through_its_provider():
    assert TABLET_DESK_RULES.bounded_latches.__name__ == "tablet_desk_bounded_latches"
```

In `tests/test_desk_bursts.py`, import
`from qlctool.controllers.tablet_desk_bounded_latches import tablet_desk_bounded_latches`
and `from qlctool.checks.rule_context import RuleContext`, and replace the two
`check_held_column(graph, group_fixtures(workspace.root), workspace.root)` calls
(in `test_bursts_preserve_sources_and_validate_without_function_names` and in
the `fault == "loop"` branch) with:

```python
    groups = group_fixtures(workspace.root)
    context = RuleContext(root=workspace.root, graph=graph, groups=groups, entries={}, states=set())
    bounded = tablet_desk_bounded_latches(context)
    assert not check_held_column(graph, groups, workspace.root, bounded)
```

(and `assert check_held_column(graph, groups, workspace.root, bounded)` in the
loop branch, indented under its `if`).

- [ ] **Step 2: Run them to see them fail**

Run: `.venv/bin/python -m pytest tests/test_core_rules_know_no_controller.py tests/test_desk_bursts.py -q -n 0`
Expected: FAIL with `ModuleNotFoundError: No module named 'qlctool.checks.declared_rule_providers'`.

- [ ] **Step 3: Write the units**

`qlctool/checks/no_bounded_latches.py`:

```python
"""A rule provider that vouches for no latched button: the default."""

from .rule_context import RuleContext


def no_bounded_latches(context: RuleContext) -> frozenset[int]:
    """No function is exempt from the held-column rule."""
    return frozenset()
```

`qlctool/controllers/tablet_desk_bounded_latches.py`:

```python
"""The tablet's verified bursts: latched, but ended by the master on their own.

Since 2026-09-13 the tablet may fire an isolated, self-ending burst of the
vertical fog column (`valid_desk_bursts`); that is the one latch the
held-column rule allows, and only a show with the desk has one.
"""

from ..checks.rule_context import RuleContext
from ..checks.valid_desk_bursts import valid_desk_bursts


def tablet_desk_bounded_latches(context: RuleContext) -> frozenset[int]:
    """The burst chasers `rule_held_column` must not report."""
    return frozenset(valid_desk_bursts(context.graph, context.root))
```

`qlctool/checks/declared_rule_providers.py`:

```python
"""The rule providers this checkout's `pyproject.toml` declares.

A checkout pulled without `pip install -e` has a stale entry-point list, and a
desk check that stops running looks like a desk with no problems (R10). The
names are read from the project file rather than spelled here, so core never
names a controller. An installed wheel has no project file beside it and
declares nothing - it cannot be stale.
"""

import tomllib
from pathlib import Path

from .rule_group import RULE_GROUP


def declared_rule_providers(project: Path | None = None) -> tuple[str, ...]:
    """Entry-point names under `qlctool.rules` in the qlctool project file, sorted."""
    folder = Path(__file__).resolve().parents[2] if project is None else project
    path = folder / "pyproject.toml"
    if not path.is_file():
        return ()
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    table = document.get("project", {})
    if table.get("name") != "qlctool":
        return ()
    return tuple(sorted(table.get("entry-points", {}).get(RULE_GROUP, {})))
```

- [ ] **Step 4: Wire them in**

`qlctool/checks/rule_provider.py`: import `no_bounded_latches` and add the field
after `check`:

```python
    bounded_latches: Callable[[RuleContext], frozenset[int]] = no_bounded_latches
```

and extend the class docstring: "`bounded_latches` names the latched functions
this part guarantees to end on their own (the tablet's bursts), which
`rule_held_column` then allows."

`qlctool/controllers/tablet_desk_rules.py`:

```python
TABLET_DESK_RULES = RuleProvider(
    name="tablet_desk",
    applies=tablet_desk_applies,
    check=tablet_desk_check,
    bounded_latches=tablet_desk_bounded_latches,
)
```

(with the import).

`qlctool/checks/rule_providers.py`: replace
`from .own_rule_providers import OWN_RULE_PROVIDERS` with
`from .declared_rule_providers import declared_rule_providers`, and
`set(OWN_RULE_PROVIDERS)` with `set(declared_rule_providers())`. Change the
docstring's "a missing own provider" sentence to "a provider this checkout's
`pyproject.toml` declares and the install lacks is an error". Delete
`qlctool/checks/own_rule_providers.py`.

`qlctool/checks/rule_held_column.py`: remove the `valid_desk_bursts` import,
change the signature to

```python
def check_held_column(
    graph: ShowGraph, groups, root: etree._Element, bounded: frozenset[int] = frozenset()
) -> list[Finding]:
```

delete the two comment lines and the `bounded = valid_desk_bursts(graph, root)`
line, and rewrite the docstring's last paragraph as: "Since 2026-09-13 a
controller may vouch for a latch that ends on its own - the tablet's verified
burst (`RuleProvider.bounded_latches`). Those arrive as `bounded`; every other
latch is still forbidden."

`qlctool/checks/run.py`: build the context before the rules, decide the
applying providers once, and pass their union to the held-column rule. Replace
the tail of `check_workspace` from `findings += check_held_column(...)` onward
with the same sequence of `findings +=` lines, changing only:

```python
    context = RuleContext(root=root, graph=graph, groups=groups, entries=entries, states=states)
    applying = [p for p in (rule_providers() if providers is None else providers) if p.applies(root)]
    bounded = frozenset().union(*(p.bounded_latches(context) for p in applying))
```

placed directly after `states = room_states(root, graph, groups)`;
`findings += check_held_column(graph, groups, root, bounded)`; and the final
loop becoming `for provider in applying: findings += provider.check(context)`
(delete the old `context = ...` line near the end).

- [ ] **Step 5: Reinstall, run the tests**

```bash
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest tests/test_core_rules_know_no_controller.py tests/test_desk_bursts.py tests/test_controllers.py tests/test_check.py -q
```

Expected: all pass (`test_a_stale_install_fails_loudly` still raises: the
declared set is read from `pyproject.toml`).

- [ ] **Step 6: Gates, then commit**

Run the five gate commands. Every `check` still prints `522 botones revisados,
ningun problema`: Vibra's bursts are now vouched for by the provider, not by
core.

```bash
git add qlctool/checks/no_bounded_latches.py qlctool/checks/declared_rule_providers.py qlctool/controllers/tablet_desk_bounded_latches.py qlctool/checks/rule_provider.py qlctool/checks/rule_providers.py qlctool/checks/rule_held_column.py qlctool/checks/run.py qlctool/controllers/tablet_desk_rules.py tests/test_core_rules_know_no_controller.py tests/test_desk_bursts.py
git rm qlctool/checks/own_rule_providers.py
git commit -m "$(cat <<'EOF'
refactor(qlctool): core checks reach desk bursts only through the provider

rule_held_column takes the bounded latches as an argument, the tablet desk
provider supplies them, and the toolkit's own provider names are read from
pyproject.toml instead of being spelled inside checks/.

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
EOF
)"
```

---

### Task 3: Fixture definitions are found by configuration, not by this repository's layout

**Files:**
- Create: `qlctool/toolkit_config.py`, `qlctool/find_toolkit_config.py`,
  `qlctool/read_toolkit_config.py`, `qlctool/toolkit_config_from.py`,
  `qlctool/fixture_dirs.py`, `qlctool/unresolved_fixtures.py`,
  `qlctool/warn_unresolved.py`, `qlctool/library_for.py`,
  `/Users/cristiandeluxe/p/DMX-Fixtures/qlctool.toml`
- Modify: `qlctool/library.py`, `qlctool/install_plan.py`, `qlctool/cli.py`,
  `qlctool/cmd_deskmap.py`, `qlctool/description/rig_files.py`,
  `qlctool/description/reading/read_rig.py`
- Test: `tests/test_fixture_dirs.py`, `tests/test_no_repo_layout.py`; modify
  `tests/test_install.py`, `tests/test_definition_schema.py`

**Interfaces:**
- Consumes: `qlctool.description.reading.read_rig` (extended below).
- Produces:
  - `ToolkitConfig(fixtures: tuple[Path, ...] = (), input_profiles: tuple[Path, ...] = (), gobos: tuple[Path, ...] = ())`
  - `find_toolkit_config(start: Path) -> Path | None`
  - `read_toolkit_config(path: Path) -> ToolkitConfig`
  - `toolkit_config_from(start: Path) -> ToolkitConfig`
  - `fixture_dirs(cli: Sequence[str] = (), described: Sequence[Path] = (), environ: Mapping[str, str] | None = None, start: Path | None = None) -> tuple[Path, ...]`
  - `FixtureLibrary.load(fixture_dirs: Sequence[Path] | None = None, system_dir: Path | None = None)`,
    `FixtureLibrary.sources: tuple[Path, ...]`
  - `unresolved_fixtures(root: etree._Element, library: FixtureLibrary) -> list[str]`
  - `warn_unresolved(root: etree._Element, library: FixtureLibrary) -> None`
  - `library_for(cli: Sequence[str], start: Path, described: Sequence[Path] = ()) -> FixtureLibrary`
  - `install_plan(config: ToolkitConfig, user_dir: Path | None = None, gobo_dir: Path | None = None)`
  - `RigFiles.fixtures: tuple[Path, ...] = ()`; `[rig] fixtures = ["dir", ...]`
  - `qlctool --fixtures DIR` (top-level, repeatable) → `args.fixtures: list[str] | None`
  - `SYSTEM_FIXTURES` stays in `library.py`; `REPO_ROOT` and `REPO_FIXTURES` are gone.

- [ ] **Step 1: Write the failing tests**

`tests/test_fixture_dirs.py`:

```python
"""Spec step 6 (2026-09-25): the toolkit finds a rig's fixtures without this repo.

`library.REPO_ROOT` was `parents[3]` of the package; a copy of the package
anywhere else found no definition, and `capabilities_of` skipped every fixture
in silence ("no fixture has both pan and tilt" in a scratch copy, 2026-09-24).
"""

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from qlctool.cli import main
from qlctool.fixture_dirs import fixture_dirs
from qlctool.library import FixtureLibrary
from qlctool.read_toolkit_config import read_toolkit_config
from qlctool.toolkit_config import ToolkitConfig

REPO = Path(__file__).resolve().parents[3]
BASELINE = json.loads((Path(__file__).with_name("vibra_baseline.json")).read_text("utf-8"))


def _config(folder: Path, fixtures: str) -> Path:
    (folder / fixtures).mkdir(parents=True, exist_ok=True)
    (folder / "qlctool.toml").write_text(f'fixtures = ["{fixtures}"]\n', encoding="utf-8")
    return folder / fixtures


def test_the_repo_config_names_its_three_folders():
    config = read_toolkit_config(REPO / "qlctool.toml")
    assert config == ToolkitConfig(
        fixtures=(REPO / "QLC+ Fixtures",),
        input_profiles=(REPO / "QLC+ InputProfiles",),
        gobos=(REPO / "QLC+ Setups" / "Gobos",),
    )


def test_an_unknown_key_is_refused(tmp_path):
    (tmp_path / "qlctool.toml").write_text('fixture = ["x"]\n', encoding="utf-8")
    with pytest.raises(ValueError, match="fixture"):
        read_toolkit_config(tmp_path / "qlctool.toml")


def test_the_nearest_config_walking_up_is_the_last_resort(tmp_path):
    found = _config(tmp_path, "defs")
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    assert fixture_dirs(environ={}, start=nested / "show.qxw") == (found,)
    assert fixture_dirs(environ={}, start=tmp_path.parent / "elsewhere") == ()


def test_each_source_beats_the_ones_after_it(tmp_path):
    _config(tmp_path, "from-config")
    env = {"QLCTOOL_FIXTURES": f"{tmp_path / 'env1'}:{tmp_path / 'env2'}"}
    described = [tmp_path / "described"]
    assert fixture_dirs(["cli"], described, env, tmp_path) == (Path("cli"),)
    assert fixture_dirs([], described, env, tmp_path) == tuple(described)
    assert fixture_dirs([], [], env, tmp_path) == (tmp_path / "env1", tmp_path / "env2")


def test_the_first_directory_wins_a_model_clash(tmp_path):
    source = REPO / "QLC+ Fixtures"
    first, second = tmp_path / "first", tmp_path / "second"
    one = sorted(source.glob("*.qxf"))[0]
    for folder in (first, second):
        folder.mkdir()
        shutil.copy(one, folder / one.name)
    library = FixtureLibrary.load([first, second])
    assert library.sources == (first, second)
    assert len(library) >= 1


def test_a_rig_outside_the_repo_regenerates_vibra(tmp_path, monkeypatch):
    rig = tmp_path / "rig"
    rig.mkdir()
    for name in ("Vibra.qxw", "vibra-stage-plot.json", "vibra.toml"):
        shutil.copy(REPO / "QLC+ Setups" / name, rig / name)
    shutil.copytree(REPO / "QLC+ Fixtures", rig / "fixtures")
    toml = rig / "vibra.toml"
    text = toml.read_text(encoding="utf-8")
    toml.write_text(
        text.replace('stage_plot = "vibra-stage-plot.json"', 'stage_plot = "vibra-stage-plot.json"\nfixtures = ["fixtures"]'),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("QLCTOOL_FIXTURES", raising=False)
    out = tmp_path / "out.qxw"
    assert main(["newshow", "--description", str(toml), "--out", str(out)]) == 0
    assert hashlib.sha256(out.read_bytes()).hexdigest() == BASELINE["Vibra.qxw"]["sha256"]


def test_a_patch_with_no_definition_says_so(tmp_path, monkeypatch, capsys):
    # Copied out of the repo: walking up from the original would find qlctool.toml.
    shutil.copy(REPO / "QLC+ Setups" / "Vibra.qxw", tmp_path / "Vibra.qxw")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("QLCTOOL_FIXTURES", raising=False)
    assert main(["info", str(tmp_path / "Vibra.qxw")]) == 0
    assert "no fixture definition" in capsys.readouterr().err
```

`tests/test_no_repo_layout.py`:

```python
"""Spec step 6: nothing in the package may assume where this repository keeps its files."""

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "qlctool"
REPO_FOLDERS = ("QLC+ Fixtures", "QLC+ Setups", "QLC+ InputProfiles")


def _docstrings(tree: ast.AST) -> set[int]:
    return {
        id(node.body[0].value)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef))
        and node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
    }


def test_no_source_names_a_repo_folder_or_climbs_to_the_repo():
    offenders = []
    for source in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        skip = _docstrings(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
                if any(folder in node.value for folder in REPO_FOLDERS):
                    offenders.append(f"{source.name}:{node.lineno} {node.value!r}")
            if (
                isinstance(node, ast.Subscript)
                and isinstance(node.value, ast.Attribute)
                and node.value.attr == "parents"
                and isinstance(node.slice, ast.Constant)
                and node.slice.value >= 3
            ):
                offenders.append(f"{source.name}:{node.lineno} parents[{node.slice.value}]")
    assert offenders == []
```

In `tests/test_install.py`, add `from qlctool.toolkit_config import ToolkitConfig`
and a helper, then replace every `install_plan(repo, ...)` call's first
argument with `_config(repo)`:

```python
def _config(repo: Path) -> ToolkitConfig:
    return ToolkitConfig(
        fixtures=(repo / "QLC+ Fixtures",),
        input_profiles=(repo / "QLC+ InputProfiles",),
        gobos=(repo / "QLC+ Setups" / "Gobos",),
    )
```

In `tests/test_definition_schema.py`, replace the `REPO_FIXTURES` import and the
`DEFINITIONS` line with:

```python
from qlctool.fixture_dirs import fixture_dirs
from qlctool.library import SYSTEM_FIXTURES

DEFINITIONS = sorted(q for d in fixture_dirs() for q in d.glob("*.qxf")) + sorted(
    SYSTEM_FIXTURES.glob("*.qxf")
)
```

- [ ] **Step 2: Run them to see them fail**

Run: `.venv/bin/python -m pytest tests/test_fixture_dirs.py tests/test_no_repo_layout.py -q -n 0`
Expected: FAIL with `ModuleNotFoundError: No module named 'qlctool.fixture_dirs'`
(and `test_no_repo_layout` failing on `library.py` and `install_plan.py`).

- [ ] **Step 3: Write the configuration units and the repo's config file**

`/Users/cristiandeluxe/p/DMX-Fixtures/qlctool.toml`:

```toml
# Where qlctool finds this repository's own files (spec step 6). Paths are
# relative to this file. Overridden by `qlctool --fixtures`, a description's
# [rig] fixtures, or QLCTOOL_FIXTURES, in that order.
fixtures = ["QLC+ Fixtures"]
input_profiles = ["QLC+ InputProfiles"]
gobos = ["QLC+ Setups/Gobos"]
```

`qlctool/toolkit_config.py`:

```python
"""Where a show's own files live: fixture definitions, input profiles, gobo images."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolkitConfig:
    """Folders, absolute, in priority order; empty where the config says nothing."""

    fixtures: tuple[Path, ...] = ()
    input_profiles: tuple[Path, ...] = ()
    gobos: tuple[Path, ...] = ()
```

`qlctool/find_toolkit_config.py`:

```python
"""The `qlctool.toml` that governs a path: the nearest one at or above it."""

from pathlib import Path


def find_toolkit_config(start: Path) -> Path | None:
    """Walk up from `start` (a file or a folder) to the filesystem root."""
    here = start.resolve()
    for folder in (here, *here.parents):
        candidate = folder / "qlctool.toml"
        if candidate.is_file():
            return candidate
    return None
```

`qlctool/read_toolkit_config.py`:

```python
"""Read one `qlctool.toml`, refusing keys it does not know."""

import tomllib
from pathlib import Path

from .toolkit_config import ToolkitConfig


def read_toolkit_config(path: Path) -> ToolkitConfig:
    """Every listed folder resolved against the file's own folder."""
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    keys = ("fixtures", "input_profiles", "gobos")
    # Checked here rather than with description/reading/reject_unknown_keys:
    # library.py imports this module, and the description package imports the library.
    unknown = sorted(set(document) - set(keys))
    if unknown:
        raise ValueError(f"{path}: unknown key(s) {', '.join(unknown)}; allowed: {', '.join(keys)}")
    folders: dict[str, tuple[Path, ...]] = {}
    for key in keys:
        entries = document.get(key, [])
        if not isinstance(entries, list) or not all(isinstance(e, str) and e for e in entries):
            raise ValueError(f"{path}: {key} must be a list of folder names")
        folders[key] = tuple(path.parent / entry for entry in entries)
    return ToolkitConfig(**folders)
```

The message names the unknown key, which is what `match="fixture"` asserts.

`qlctool/toolkit_config_from.py`:

```python
"""The config governing a path, or an empty one when there is none."""

from pathlib import Path

from .find_toolkit_config import find_toolkit_config
from .read_toolkit_config import read_toolkit_config
from .toolkit_config import ToolkitConfig


def toolkit_config_from(start: Path) -> ToolkitConfig:
    """Nearest `qlctool.toml` at or above `start`, read; `ToolkitConfig()` otherwise."""
    found = find_toolkit_config(start)
    return read_toolkit_config(found) if found is not None else ToolkitConfig()
```

`qlctool/fixture_dirs.py`:

```python
"""Which folders hold a rig's fixture definitions (ruling B3).

The first source that names any folder wins: the command line, then the
description's [rig] fixtures, then QLCTOOL_FIXTURES, then the nearest
qlctool.toml above the workspace, description or current directory.
"""

import os
from collections.abc import Mapping, Sequence
from pathlib import Path

from .toolkit_config_from import toolkit_config_from


def fixture_dirs(
    cli: Sequence[str] = (),
    described: Sequence[Path] = (),
    environ: Mapping[str, str] | None = None,
    start: Path | None = None,
) -> tuple[Path, ...]:
    """Folders in priority order: the first one wins a model clash."""
    if cli:
        return tuple(Path(entry) for entry in cli)
    if described:
        return tuple(described)
    variable = (os.environ if environ is None else environ).get("QLCTOOL_FIXTURES", "")
    listed = [entry for entry in variable.split(os.pathsep) if entry]
    if listed:
        return tuple(Path(entry) for entry in listed)
    return toolkit_config_from(Path.cwd() if start is None else start).fixtures
```

- [ ] **Step 4: The library loads from folders**

`qlctool/library.py`: delete `REPO_ROOT` and `REPO_FIXTURES`; rewrite the module
docstring's first paragraph to "Two sources feed the library: the folders a rig
names for its own .qxf (`fixture_dirs`), and the handful of QLC+ system
definitions bundled under `qlctool/library/system`. A rig's definitions win on
a name clash - that is what QLC+ does with a user library too - and among the
rig's folders the first wins."; then:

```python
class FixtureLibrary:
    def __init__(
        self,
        definitions: dict[tuple[str, str], FixtureDefinition],
        sources: tuple[Path, ...] = (),
    ):
        self._by_key = definitions
        self.sources = sources

    @classmethod
    def load(
        cls,
        fixture_dirs: Sequence[Path] | None = None,
        system_dir: Path | None = None,
    ) -> "FixtureLibrary":
        folders = tuple(resolve_fixture_dirs() if fixture_dirs is None else fixture_dirs)
        definitions: dict[tuple[str, str], FixtureDefinition] = {}
        # System first and the rig's first folder last, so it overrides the rest.
        for source in (system_dir or SYSTEM_FIXTURES, *reversed(folders)):
            if not source.is_dir():
                continue
            for qxf in sorted(source.glob("*.qxf")):
                definition = load_definition(qxf)
                definitions[(definition.manufacturer, definition.model)] = definition
        return cls(definitions, folders)
```

with `from collections.abc import Sequence` and
`from .fixture_dirs import fixture_dirs as resolve_fixture_dirs` (the alias
avoids shadowing by the parameter).

`qlctool/unresolved_fixtures.py`:

```python
"""Patched fixtures the library has no definition for."""

from lxml import etree

from .fixture import patched_fixtures
from .library import FixtureLibrary


def unresolved_fixtures(root: etree._Element, library: FixtureLibrary) -> list[str]:
    """ "Manufacturer Model" of every patched fixture with no definition, without repeats."""
    missing: dict[str, None] = {}
    for fixture in patched_fixtures(root):
        if library.get(fixture.manufacturer, fixture.model) is None:
            missing[f"{fixture.manufacturer} {fixture.model}"] = None
    return list(missing)
```

`qlctool/warn_unresolved.py`:

```python
"""Say which fixtures will be skipped, instead of skipping them in silence."""

import sys

from lxml import etree

from .library import FixtureLibrary
from .unresolved_fixtures import unresolved_fixtures


def warn_unresolved(root: etree._Element, library: FixtureLibrary) -> None:
    """One stderr line per missing model, and where the definitions were looked for."""
    missing = unresolved_fixtures(root, library)
    if not missing:
        return
    searched = ", ".join(str(folder) for folder in library.sources) or "no folder"
    print(
        f"qlctool: no fixture definition for {', '.join(missing)} (searched {searched}); "
        "pass --fixtures, set QLCTOOL_FIXTURES, or add a qlctool.toml",
        file=sys.stderr,
    )
```

`qlctool/library_for.py`:

```python
"""The fixture library a command works with, found from where its files are."""

from collections.abc import Sequence
from pathlib import Path

from .fixture_dirs import fixture_dirs
from .library import FixtureLibrary


def library_for(cli: Sequence[str], start: Path, described: Sequence[Path] = ()) -> FixtureLibrary:
    """`--fixtures`, then the description, then QLCTOOL_FIXTURES, then qlctool.toml from `start`."""
    return FixtureLibrary.load(fixture_dirs(cli or (), described, None, start))
```

- [ ] **Step 5: The description can name its fixtures**

`qlctool/description/rig_files.py`: add `fixtures: tuple[Path, ...] = ()` with
the docstring line "`fixtures` are the rig's definition folders; empty means
found by configuration (`fixture_dirs`)."

`qlctool/description/reading/read_rig.py`: allow the key and resolve it:

```python
    reject_unknown_keys(table, ("workspace", "output", "stage_plot", "fixtures"), here)
    ...
    fixtures = table.get("fixtures", [])
    if not isinstance(fixtures, list) or not all(isinstance(f, str) and f for f in fixtures):
        raise ValueError(f"{here} fixtures must be a list of folder names")
    ...
    return RigFiles(
        workspace=folder / table["workspace"],
        output=folder / table["output"] if "output" in table else None,
        stage_plot=folder / table["stage_plot"] if "stage_plot" in table else None,
        fixtures=tuple(folder / entry for entry in fixtures),
    )
```

- [ ] **Step 6: The CLI and the install plan**

`qlctool/cli.py`:

- In `build_parser`, before `sub = parser.add_subparsers(...)`:

  ```python
  parser.add_argument(
      "--fixtures",
      action="append",
      metavar="DIR",
      help="a folder of .qxf definitions; repeat for more (default: qlctool.toml)",
  )
  ```

- Replace every `FixtureLibrary.load()` with
  `library_for(args.fixtures, Path(args.workspace))` (in `cmd_info`,
  `cmd_palette`, `cmd_matrix`, `cmd_movement`, `cmd_patch`, `cmd_probe`,
  `cmd_stage` (both), `cmd_mvr`, `cmd_check`), and in `cmd_newshow` with
  `library_for(args.fixtures, src, description.rig.fixtures if description else ())`,
  and in `qlctool/cmd_deskmap.py` with
  `library_for(args.fixtures, Path(args.workspace))`.
  Where the command has a loaded workspace, call
  `warn_unresolved(ws.root, library)` right after building the library
  (`cmd_info`, `cmd_newshow`, `cmd_check`, `cmd_stage`, `cmd_mvr`).
- `cmd_install`:

  ```python
  config = toolkit_config_from(Path.cwd())
  if args.fixtures:
      config = replace(config, fixtures=tuple(Path(entry) for entry in args.fixtures))
  items = install_plan(config, user_dir=qlc_user_dir(), gobo_dir=qlc_gobo_dir())
  ```

  and its `--check` message says "QLC+ has every one of the configured
  {len(items)} file(s)" instead of "the repo's" (no test asserts that text;
  `grep -rn "of the repo's" tests` prints nothing on 2026-09-25).

`qlctool/install_plan.py`:

```python
def install_plan(
    config: ToolkitConfig,
    user_dir: Path | None = None,
    gobo_dir: Path | None = None,
) -> list[InstallItem]:
    """Every configured file to install, in configuration order, each with its state."""
    items: list[InstallItem] = []
    if user_dir is not None:
        for folder in config.fixtures:
            for source in sorted(folder.glob("*.qxf")):
                items.append(install_state(source, user_dir / "Fixtures" / source.name))
        for folder in config.input_profiles:
            for source in sorted(folder.glob("*.qxi")):
                items.append(install_state(source, user_dir / "InputProfiles" / source.name))
    if gobo_dir is not None:
        for folder in config.gobos:
            for source in sorted(folder.glob("*/*.png")):
                target = next(
                    (f for d in config.fixtures if (f := gobo_folder(d, source.name)) is not None),
                    None,
                )
                if target is not None:
                    items.append(install_state(source, gobo_dir / target / source.name))
    return items
```

and its docstring's first line becomes "Everything QLC+ has to be handed from a
rig's configured folders, and whether it has it."

- [ ] **Step 7: Run the tests**

Run: `.venv/bin/python -m pytest tests/test_fixture_dirs.py tests/test_no_repo_layout.py tests/test_install.py tests/test_definition_schema.py -q`
Expected: all pass. `test_a_rig_outside_the_repo_regenerates_vibra` must
produce the baseline hash: if it does not, the copied rig lacks a file the
build reads (the output names it); fix the test's copy list, never the hash.

- [ ] **Step 8: Docs, gates, commit**

- `AGENTS.md` "Environment": add "qlctool finds the rig's definitions through
  the repo-root `qlctool.toml`; a rig elsewhere names them with `[rig]
  fixtures`, `QLCTOOL_FIXTURES` or `qlctool --fixtures DIR`."
- `docs/toolkit.md`: a short "Where the toolkit finds your files" section with
  the B3 order and the `qlctool.toml` example above.
- `TODO.md`: close spec step 6 if it is listed; log it in `TODO_LOG.md`.

Run the five gate commands, then:

```bash
git add qlctool/toolkit_config.py qlctool/find_toolkit_config.py qlctool/read_toolkit_config.py qlctool/toolkit_config_from.py qlctool/fixture_dirs.py qlctool/unresolved_fixtures.py qlctool/warn_unresolved.py qlctool/library_for.py qlctool/library.py qlctool/install_plan.py qlctool/cli.py qlctool/cmd_deskmap.py qlctool/description/rig_files.py qlctool/description/reading/read_rig.py tests/test_fixture_dirs.py tests/test_no_repo_layout.py tests/test_install.py tests/test_definition_schema.py ../../qlctool.toml ../../AGENTS.md ../../docs/toolkit.md ../../TODO.md ../../TODO_LOG.md
git commit -m "$(cat <<'EOF'
feat(qlctool): find fixture definitions by configuration

A qlctool.toml found by walking up, QLCTOOL_FIXTURES, a description's
[rig] fixtures and --fixtures replace library.REPO_ROOT, and a patched
fixture with no definition is now a warning instead of a silent skip.

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
EOF
)"
```


---

### Task 4: Templates in the catalogue, six new sections, and the literal ratchet

**Files:**
- Modify: `qlctool/names/names.py` (add `render`), `qlctool/names/sections.py`,
  `qlctool/locales/en.toml`, `qlctool/locales/es.toml`,
  `qlctool/description/reading/read_names.py`
- Create: `qlctool/names/template_fields.py`, `qlctool/names/template_affixes.py`,
  `qlctool/names/check_override_fields.py`, `tests/generator_literals.py`
- Test: `tests/test_catalogue_templates.py`, `tests/test_generator_literals.py`

**Interfaces:**
- Consumes: `Names`, `load_catalogue(language)`, `shipped_languages()`.
- Produces (every later task relies on these names):
  - `Names.render(identifier: str, **fields: object) -> str`
  - `template_fields(text: str) -> tuple[str, ...]`
  - `template_affixes(names: Names, identifier: str) -> tuple[str, str]`
  - `check_override_fields(overrides: Mapping[str, Mapping[str, str]], where: str) -> None`
  - `SECTIONS == ("colors", "functions", "frames", "captions", "generated", "paths", "console", "help", "abbreviations", "mix_codes")`
  - `tests/generator_literals.py`: `catalogue_chunks() -> frozenset[str]`,
    `spanish_literals(path: Path, chunks: frozenset[str]) -> list[str]`
  - `tests/test_generator_literals.py`: `CONVERTED: tuple[str, ...]`, paths
    relative to `qlctool/` (for example `"generate/color_banks.py"`). Every
    later task appends the modules it converts.

**Catalogue conventions every later task follows:**

- A new entry goes into both `es.toml` and `en.toml`, same section, same
  position (the existing test holds identifiers and order equal).
- The `es` value is exactly the literal it replaces, character for character,
  including accents, capitals and spaces: that is what keeps the Vibra
  hashes. Never "fix" a Spanish value.
- A value with a variable part is a template: `"Golpe {colour}"`. Field names
  are English snake case and identical in every language
  (`tests/test_catalogue_templates.py`).
- Sections: `functions` for functions a table or a person refers to by
  identity (keys, glyphs, pad bindings, AUTO members, desk lookups);
  `generated` for every other generated function name and its templates;
  `paths` for function folder paths; `console` for virtual-console captions,
  frame titles and the desk map's titles; `help` for help labels and notes;
  `abbreviations` and `mix_codes` for the console's short colour words.
  `frames` and `captions` are read by the desk: add to them only what the desk
  looks up.
- If the existing no-duplicate-spelling test in `tests/test_names.py` fails
  after an addition, change the English value, never the Spanish one, and say
  so in the commit message.

- [ ] **Step 1: Write the failing tests**

`tests/test_catalogue_templates.py`:

```python
"""Catalogue templates: a name with a hole in it, the hole the same in every language."""

import pytest

from qlctool.description.reading.read_names import read_names
from qlctool.names.load_catalogue import load_catalogue
from qlctool.names.sections import SECTIONS
from qlctool.names.shipped_languages import shipped_languages
from qlctool.names.shipped_names import shipped_names
from qlctool.names.template_affixes import template_affixes
from qlctool.names.template_fields import template_fields


def test_fields_are_read_in_order():
    assert template_fields("Desk · {caption} ráfaga {seconds} s") == ("caption", "seconds")
    assert template_fields("Rueda Colores") == ()


def test_every_language_has_the_same_fields_for_an_identifier():
    reference = load_catalogue("es")
    for language in shipped_languages():
        catalogue = load_catalogue(language)
        for section in SECTIONS:
            for identifier, text in reference.get(section, {}).items():
                other = catalogue[section][identifier]
                assert sorted(template_fields(other)) == sorted(template_fields(text)), (
                    f"{language} {section}.{identifier}: {other!r} vs {text!r}"
                )


def test_render_fills_the_fields():
    names = shipped_names("es", {"es": {"auto": "AUTO {x}"}})
    assert names.render("auto", x="YA") == "AUTO YA"


def test_affixes_are_the_text_around_the_field():
    names = shipped_names("es", {"es": {"auto": "Ciclo {what}!"}})
    assert template_affixes(names, "auto") == ("Ciclo ", "!")
    with pytest.raises(ValueError, match="not a template"):
        template_affixes(shipped_names("es"), "party_moment")


def test_an_override_must_keep_the_fields():
    assert read_names({"es": {"party_moment": "Fiesta"}}, "show.toml")
    with pytest.raises(ValueError, match="fields"):
        read_names({"es": {"party_moment": "Fiesta {now}"}}, "show.toml")
```

`tests/generator_literals.py` (a helper module, imported the way
`tests/test_vibra_byte_identity.py` imports `vibra_regen`):

```python
"""Find the words a generator still spells itself instead of asking the catalogue.

A literal is flagged when, stripped of spaces and joining punctuation, it
equals a piece of a Spanish catalogue value whose English value differs: that
piece would stay Spanish in an English show. Words both languages share
("AUTO", "Dimmer Chase") are not flagged - they are the same either way.
"""

import ast
import re
from pathlib import Path
from string import Formatter

from qlctool.names.load_catalogue import load_catalogue

STRIP = " \t\n·—-/+():,."


def catalogue_chunks() -> frozenset[str]:
    """Every word-bearing piece of every Spanish value that English spells differently."""
    spanish, english = load_catalogue("es"), load_catalogue("en")
    chunks: set[str] = set()
    for section, entries in spanish.items():
        for identifier, text in entries.items():
            if english.get(section, {}).get(identifier) == text:
                continue
            for literal, _, _, _ in Formatter().parse(text):
                piece = literal.strip(STRIP)
                if re.search(r"[^\W\d_]{2,}", piece):
                    chunks.add(piece)
    return frozenset(chunks)


def spanish_literals(path: Path, chunks: frozenset[str]) -> list[str]:
    """`file:line 'literal'` for each non-docstring string that is a catalogue chunk."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = {
        id(node.body[0].value)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef))
        and node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
    }
    return [
        f"{path.name}:{node.lineno} {node.value!r}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstrings
        and node.value.strip(STRIP) in chunks
    ]
```

`tests/test_generator_literals.py`:

```python
"""The generators' Spanish literals, retired module by module (Plan B, 2026-09-25).

Each task that routes a module's names through the catalogue appends it to
CONVERTED; from then on the module may not spell a catalogue word itself.
Task 12 asserts CONVERTED covers every generator module except ruling B6's.
"""

from pathlib import Path

from generator_literals import catalogue_chunks, spanish_literals

PACKAGE = Path(__file__).resolve().parents[1] / "qlctool"

CONVERTED: tuple[str, ...] = ()


def test_converted_modules_spell_no_catalogue_word():
    chunks = catalogue_chunks()
    found = [hit for module in CONVERTED for hit in spanish_literals(PACKAGE / module, chunks)]
    assert found == []


def test_the_scanner_sees_a_spanish_name(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        '"""Momento Fiesta in a docstring is fine."""\nNAME = "Momento Fiesta"\nAUTO = "AUTO"\n',
        encoding="utf-8",
    )
    assert spanish_literals(source, catalogue_chunks()) == ["sample.py:2 'Momento Fiesta'"]
```

- [ ] **Step 2: Run them to see them fail**

Run: `.venv/bin/python -m pytest tests/test_catalogue_templates.py tests/test_generator_literals.py -q -n 0`
Expected: FAIL with `ModuleNotFoundError: No module named 'qlctool.names.template_affixes'`.

- [ ] **Step 3: Write the units**

`qlctool/names/template_fields.py`:

```python
"""The `{field}` names a catalogue value leaves to be filled, in order."""

from string import Formatter


def template_fields(text: str) -> tuple[str, ...]:
    """ "Golpe {colour}" -> ("colour",); a plain name -> ()."""
    return tuple(field for _, field, _, _ in Formatter().parse(text) if field is not None)
```

`qlctool/names/template_affixes.py`:

```python
"""The fixed text around a template's fields: what the console strips when it parses a name.

"Ciclo Matrices BarrasLed" is shown as "Matrices BarrasLed" on a button: the
console removes the cycle template's prefix. Reading the prefix from the
catalogue is what lets the English show strip "Cycle " instead (ruling B8).
"""

from .names import Names


def template_affixes(names: Names, identifier: str) -> tuple[str, str]:
    """(text before the first field, text after the last) in the show's language."""
    text = names.display(identifier)
    head, brace, rest = text.partition("{")
    _, close, tail = rest.rpartition("}")
    if not brace or not close:
        raise ValueError(f"{identifier} is not a template: {text!r}")
    return head, tail
```

`qlctool/names/check_override_fields.py`:

```python
"""Refuse an override that drops or invents a template's fields."""

from collections.abc import Mapping

from .load_catalogue import load_catalogue
from .template_fields import template_fields


def check_override_fields(overrides: Mapping[str, Mapping[str, str]], where: str) -> None:
    """Raise naming the identifier whose override's fields differ from the catalogue's."""
    reference = load_catalogue("en")
    for language, entries in overrides.items():
        for identifier, text in entries.items():
            shipped = next((e[identifier] for e in reference.values() if identifier in e), "")
            expected, given = sorted(template_fields(shipped)), sorted(template_fields(text))
            if expected != given:
                raise ValueError(
                    f"{where}: [names.{language}] {identifier} must keep the catalogue's fields "
                    f"{expected}, not {given}"
                )
```

In `qlctool/description/reading/read_names.py`, import it and call
`check_override_fields(overrides, where)` right after
`reject_ambiguous_names(overrides, where)`.

In `qlctool/names/names.py`, add after `display`:

```python
    def render(self, identifier: str, **fields: object) -> str:
        """The display name with its fields filled: "Golpe {colour}" -> "Golpe Rojo"."""
        return self.display(identifier).format(**fields)
```

In `qlctool/names/sections.py`:

```python
SECTIONS: tuple[str, ...] = (
    "colors",
    "functions",
    "frames",
    "captions",
    "generated",
    "paths",
    "console",
    "help",
    "abbreviations",
    "mix_codes",
)
```

Append to the end of both `qlctool/locales/es.toml` and
`qlctool/locales/en.toml`, in this order, six empty tables for Tasks 5-11 to
fill:

```toml

[generated]

[paths]

[console]

[help]

[abbreviations]

[mix_codes]
```

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/python -m pytest tests/test_catalogue_templates.py tests/test_generator_literals.py tests/test_names.py tests/test_catalogue_vocabulary.py tests/test_load_show_description.py -q -n 0`
Expected: all pass (`test_names.py`'s section-order test now compares the ten
sections).

- [ ] **Step 5: Reinstall, gates, commit**

`locales/*.toml` is package data: run `.venv/bin/pip install -e '.[dev]'`.
Run the five gate commands and `ruff` on the touched `.py`, then stage exactly
the files under **Files** and commit:

```text
feat(qlctool): catalogue templates and the generator-literal ratchet

Names.render fills a catalogue value's fields, template_affixes gives the
text around them, overrides must keep the fields, and six empty sections
are ready for the generator's own vocabulary.

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
```

(From here on, commit messages are given as a `text` block: pass it with
`git commit -F` from a file in the scratchpad or with a quoted heredoc, and
keep the `Claude-Session` line last.)

---

### How Tasks 5-11 convert a module (read once, applies to each)

1. Add the task's catalogue entries to both files (tables below give
   `identifier | es | en`; the `es` value is the current literal).
2. Give each generator function that writes a name a keyword parameter
   `names: Names | None = None` and, first thing in the body,
   `vocabulary = default_names() if names is None else names` (ruling B5).
   Imports: `from ..names.names import Names`,
   `from ..names.default_names import default_names`.
3. Replace each literal with `vocabulary.display("<identifier>")` or
   `vocabulary.render("<identifier>", field=value)`. A default argument that
   is a Spanish word (`path: str = "Colores Rig"`) becomes
   `path: str | None = None`, resolved in the body with
   `vocabulary.display("path_rig_colours") if path is None else path`.
   A module-level Spanish constant is deleted and resolved where it was read.
4. Thread `names=vocabulary` from every caller on the newshow path
   (`build_canonical_show` already has `vocabulary = description_names(source)`
   at its top).
5. Append the module to `CONVERTED` in `tests/test_generator_literals.py`.
6. Run `.venv/bin/python tests/vibra_compare.py` after each module, not only at
   the end: a hash that moves points at the last module touched. The usual
   cause is an `es` value that differs from the literal by a space or an
   accent.

Byte identity proves these edits for Spanish only; the English build (Task 12)
proves the rest, so do not skip a literal because it "looks English already":
run the scanner.

---

### Task 5: Colour, pixel and panel generators name through the catalogue

**Files:**
- Modify: `qlctool/generate/{builtin_effects,color_banks,color_flashes,flash_color,multicolor_scene,pixel_base,pixel_wheel_matrices,quad_color_scenes,rainbow_efx,unison_colors,panel_manual,panel_speed_auto,vertical_smoke_light,matrix_effects,beam_rainbow_spin}.py`,
  `qlctool/color_wheel_match.py`, `qlctool/checks/detent_white.py`,
  `qlctool/generate/canonical_show.py` (only the call sites of these
  generators, to pass `names=vocabulary`), both catalogues
- Test: `tests/test_generator_literals.py` (extend `CONVERTED`),
  `tests/test_catalogue_templates.py` (one test added)

**Interfaces:**
- Consumes: Task 4's `Names.render`, `CONVERTED`.
- Produces:
  - Each generator above takes `names: Names | None = None`.
  - `WHEEL_NAMES: dict[str, tuple[str, ...]]` keyed by colour identifier.
  - `color_wheel_pairs(capabilities, color_name)` unchanged in signature; it
    maps `color_name` to an identifier with
    `default_names().lookup(color_name, ("colors",))` (first match; an
    identifier passes through) before reading `WHEEL_NAMES`.
  - `QUAD_COLORS: tuple[str, ...] = ("blue", "red", "green", "yellow")`,
    identifiers; `generate_quad_color_scenes` maps them with
    `vocabulary.display` before reading the display-keyed palette.
    `description/reading/read_palette.py` keeps
    `names.identify(n, ("colors",)) for n in QUAD_COLORS` unchanged:
    `identify` accepts identifiers.
  - Function identifiers Tasks 6, 7, 9 and 10 use (added here so the
    `functions` section changes once).

**Catalogue entries** (`identifier | es | en`):

`[functions]`, appended after `fast_beams`:

| identifier | es | en |
|---|---|---|
| panel_effects | Efectos Paneles | Panel Effects |
| panel_cycle | Ciclo Paneles Mixto | Mixed Panel Cycle |
| panel_speed_auto | Vel. Paneles Auto | Panel Speed Auto |
| pixels_on | Pixeles ON | Pixels On |
| smoke_auto_2_min | Humo Auto 2 min | Smoke Auto 2 min |
| smoke_auto_4_min | Humo Auto 4 min | Smoke Auto 4 min |
| smoke_auto_8_min | Humo Auto 8 min | Smoke Auto 8 min |
| ambient_intensity | Intensidad Ambiente | Ambient Intensity |
| full_intensity | Intensidad Total | Full Intensity |
| peak_intensity | Intensidad Peak | Peak Intensity |
| dimmer_programmes | Dimmer Programas | Dimmer Programmes |
| level_ambient | Nivel Ambiente | Ambient Level |
| level_party | Nivel Fiesta | Party Level |
| level_peak | Nivel Peak | Peak Level |
| level_dynamic | Nivel Fiesta Dinamico | Dynamic Party Level |
| energy_cycle | Ciclo Energia | Energy Cycle |
| talk_light | Luz Charla | Talk Light |
| fast_movements | Movimientos Rapidos | Fast Movements |
| heads_centre | Cabezas Centro | Heads Centre |

`[generated]`:

| identifier | es | en |
|---|---|---|
| colour_hit | Golpe {colour} | {colour} Hit |
| panel_effect | Efecto {number} | Effect {number} |
| cycle | Ciclo {what} | Cycle {what} |
| panels_label | Paneles | Panels |
| panel_speed_step | Vel. Paneles {value} | Panel Speed {value} |
| panel_manual | Paneles Manual | Manual Panels |
| talk_pixel_intensity | Intensidad Charla Pixeles | Talk Pixel Intensity |
| talk_panels | Paneles Charla | Talk Panels |
| group_colour_wheel | Rueda Colores {group} | Colour Wheel {group} |
| group_mix_wheel | Rueda Mezcla {group} | Mix Wheel {group} |
| rig_prefix_simple | Rig Simple | Simple Rig |
| rig_prefix_pastel | Rig Pastel | Pastel Rig |
| contrast | Cabezas {heads} / Resto {rest} | Heads {heads} / Rest {rest} |
| with_pixels | {name} + Pixeles | {name} + Pixels |
| rig_multicolour | Rig Multicolor {number} | Rig Multicolour {number} |
| rig_four_colours | Rig 4 Colores {number} | Rig 4 Colours {number} |
| wheel_tag | Rueda | Wheel |
| matrices_of | Matrices {group} | Matrices {group} |
| rainbow_layer | Arcoiris (capa) | Rainbow (layer) |
| all_fixtures_group | Todos | All fixtures |

`[paths]`:

| identifier | es | en |
|---|---|---|
| path_builtin_effects | Efectos Propios | Built-in Effects |
| path_rig_colours | Colores Rig | Rig Colours |
| path_group_colours | Colores {group} | Colours {group} |
| path_matrices_generated | Matrices (generado) | Matrices (generated) |
| path_hits | Golpes | Hits |

**Module sites** (content -> replacement):

- `builtin_effects.py`: `"Efectos Propios"` -> `display("path_builtin_effects")`;
  `f"Efecto {index + 1}"` -> `render("panel_effect", number=index + 1)`;
  `f"Ciclo {label}"` -> `render("cycle", what=label)`. Where `canonical_show`
  passes the label `"Paneles"`, it passes `vocabulary.display("panels_label")`
  (Task 7 converts that call site; in this task pass `names=vocabulary` only).
- `color_banks.py`: `f"Colores {group.name}"` ->
  `render("path_group_colours", group=group.name)`; `f"Rueda Colores {group.name}"`
  and `f"Rueda Mezcla {group.name}"` -> `render("group_colour_wheel", group=...)`
  and `render("group_mix_wheel", group=...)`.
- `color_flashes.py`: `f"Golpe {color_name}"` -> `render("colour_hit", colour=color_name)`;
  the path `"Golpes"` -> `display("path_hits")`.
- `flash_color.py`: `"Flash Color"` -> `display("flash_colour")`.
- `multicolor_scene.py`: default path -> `path_rig_colours`;
  `f"Rig Multicolor {number}"` -> `render("rig_multicolour", number=number)`.
- `quad_color_scenes.py`: `QUAD_COLORS` becomes identifiers (Interfaces);
  default path -> `path_rig_colours`; `f"Rig 4 Colores {offset + 1}"` ->
  `render("rig_four_colours", number=offset + 1)`.
- `pixel_base.py`: `"Pixeles ON"` -> `display("pixels_on")`.
- `pixel_wheel_matrices.py`: default path -> `path_rig_colours`; default
  `tag: str = "Rueda"` -> `tag: str | None = None`, resolved to
  `display("wheel_tag")`.
- `rainbow_efx.py`: `"Arcoiris Simultaneo"` and `"Arcoiris Pasos"` ->
  `display("rainbow_together")` and `display("rainbow_steps")`; default path ->
  `path_rig_colours`.
- `unison_colors.py`: delete the module constant `PATH = "Colores Rig"` and
  resolve `display("path_rig_colours")` where it was read (pass the resolved
  path into `_step`); default `wheel_name="Rueda Colores"` -> `None`, resolved
  to `display("colour_wheel")`; `scene_prefix="Rig"` stays (the same word in
  both languages); `f"Cabezas {heads_color} / Resto {rest_color}"` ->
  `render("contrast", heads=heads_color, rest=rest_color)`;
  `f"{name} + Pixeles"` -> `render("with_pixels", name=name)`.
- `panel_manual.py`: `"Paneles Manual"` -> `display("panel_manual")`;
  `"Efectos Propios"` -> `display("path_builtin_effects")`.
- `panel_speed_auto.py`: `"Efectos Propios"` -> `path_builtin_effects`;
  `f"Vel. Paneles {value}"` -> `render("panel_speed_step", value=value)`;
  `"Vel. Paneles Auto"` -> `display("panel_speed_auto")`.
- `vertical_smoke_light.py`: `"Humo Vertical"` -> `display("vertical_smoke")`;
  `"Efectos Propios"` -> `path_builtin_effects`.
- `matrix_effects.py`: default `"Matrices (generado)"` ->
  `display("path_matrices_generated")`; `f"Ciclo Matrices {group_name}"` ->
  `render("cycle", what=vocabulary.render("matrices_of", group=group_name))`;
  `_group_name`'s `"Todos"` -> `display("all_fixtures_group")` (pass the
  vocabulary in).
- `beam_rainbow_spin.py`: `"Color Beam - Arcoiris (capa)"` ->
  `f"Color Beam - {vocabulary.display('rainbow_layer')}"` ("Color Beam" is the
  wheel label, B6).
- `color_wheel_match.py`: rekey `WHEEL_NAMES` by identifier, same tuples, same
  order: `red`, `fire_red`, `orange`, `amber`, `yellow`, `green`, `mint_green`,
  `cyan`, `light_blue`, `sky_blue`, `blue`, `deep_blue`, `purple`,
  `ultraviolet`, `magenta`, `fuchsia`, `pink`, `white` (the Spanish keys map to
  these through `es.toml` `[colors]`). In `color_wheel_pairs`, before the loop:

  ```python
  matches = default_names().lookup(color_name, ("colors",))
  identifier = matches[0] if matches else color_name
  for wanted in WHEEL_NAMES.get(identifier, ()):
  ```

- `checks/detent_white.py`: `WHEEL_NAMES["Blanco"]` -> `WHEEL_NAMES["white"]`.

- [ ] **Step 1: Write the failing tests**

Set `CONVERTED` in `tests/test_generator_literals.py` to:

```python
CONVERTED: tuple[str, ...] = (
    "generate/builtin_effects.py",
    "generate/color_banks.py",
    "generate/color_flashes.py",
    "generate/flash_color.py",
    "generate/multicolor_scene.py",
    "generate/pixel_base.py",
    "generate/pixel_wheel_matrices.py",
    "generate/quad_color_scenes.py",
    "generate/rainbow_efx.py",
    "generate/unison_colors.py",
    "generate/panel_manual.py",
    "generate/panel_speed_auto.py",
    "generate/vertical_smoke_light.py",
    "generate/matrix_effects.py",
    "generate/beam_rainbow_spin.py",
    "color_wheel_match.py",
    "checks/detent_white.py",
)
```

Append to `tests/test_catalogue_templates.py`:

```python
@pytest.mark.parametrize("language", ["es", "en"])
def test_the_matrix_cycle_starts_with_the_cycle_prefix(language):
    """The console strips the cycle prefix from "Ciclo Matrices <group>" (B8)."""
    names = shipped_names(language)
    prefix, _ = template_affixes(names, "cycle")
    cycle = names.render("cycle", what=names.render("matrices_of", group="X"))
    assert cycle.startswith(prefix)
    assert cycle.removeprefix(prefix) == names.render("matrices_of", group="X")
```

Add the catalogue entries above to both files.

- [ ] **Step 2: Run to see the ratchet fail**

Run: `.venv/bin/python -m pytest tests/test_generator_literals.py -q -n 0`
Expected: FAIL listing the literals of these modules (for example
`builtin_effects.py:30 'Efectos Propios'`).

- [ ] **Step 3: Convert the modules** as listed, one at a time, running
  `.venv/bin/python tests/vibra_compare.py` after each (three `identical`).

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_catalogue_templates.py tests/test_names.py tests/test_color_banks.py tests/test_check.py -q`
Expected: all pass.

- [ ] **Step 5: Reinstall, gates, commit**

`.venv/bin/pip install -e '.[dev]'`, the five gate commands, `ruff` on the
touched files; stage exactly the files under **Files**; commit:

```text
refactor(qlctool): colour, pixel and panel generators name through the catalogue

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
```

---

### Task 6: Movement, wheel, intensity, smoke and strobe generators name through the catalogue

**Files:**
- Create: `qlctool/efx_shape_identifiers.py`
- Modify: `qlctool/efx_algorithms.py` (delete `SPANISH_LABELS`),
  `qlctool/generate/{movement_efx,movement_families,home_position,cross_position,fan_position,stage_aim,wheel_scenes,dealt_gobo_scenes,prism_spins,beam_subsets,dimmer_chases,dimmer_sequence,dimmerless_intensity,energy_intensity,energy_levels,smoke_auto,strobe_effects,vertical_smoke_burst,play_wrappers}.py`,
  `qlctool/generate/canonical_show.py` (call sites only, `names=vocabulary`),
  both catalogues
- Test: `tests/test_generator_literals.py`, `tests/test_catalogue_templates.py`

**Interfaces:**
- Consumes: Task 5's `functions` identifiers (`heads_centre`, `smoke_auto_*`,
  `ambient_intensity`, ...), `Names.render`.
- Produces:
  - `EFX_SHAPE_IDENTIFIERS: dict[str, str]` in `qlctool/efx_shape_identifiers.py`:
    QLC+ algorithm name -> `generated` identifier.
  - Each generator above takes `names: Names | None = None`.
  - `generated.animation` renders `functions.gobo_animation` and
    `functions.prism_animation` exactly, in both languages (tested).

`qlctool/efx_shape_identifiers.py`:

```python
"""QLC+'s EFX algorithm names -> the catalogue identifier of the shape's label."""

EFX_SHAPE_IDENTIFIERS: dict[str, str] = {
    "Circle": "shape_circle",
    "Eight": "shape_eight",
    "Line": "shape_line",
    "Diamond": "shape_diamond",
    "Square": "shape_square",
    "Leaf": "shape_leaf",
    "Lissajous": "shape_lissajous",
}
```

Every former `SPANISH_LABELS.get(shape, shape)` becomes
`vocabulary.display(EFX_SHAPE_IDENTIFIERS[shape]) if shape in EFX_SHAPE_IDENTIFIERS else shape`
(write it once per module as a local lambda or inline; do not add a shared
helper module for one expression).

**Catalogue entries** (`identifier | es | en`):

`[generated]`:

| identifier | es | en |
|---|---|---|
| shape_circle | Circulo | Circle |
| shape_eight | Ocho | Eight |
| shape_line | Linea | Line |
| shape_diamond | Diamante | Diamond |
| shape_square | Cuadrado | Square |
| shape_leaf | Hoja | Leaf |
| shape_lissajous | Lissajous | Lissajous |
| prefix_soft | Suave | Soft |
| prefix_soft_beam | Beam Suave | Soft Beam |
| prefix_wave | Ola | Wave |
| prefix_sweep | Barrido | Sweep |
| prefix_fast_wash | Wash Rapido | Fast Wash |
| prefix_fast_beam | Beam Rapido | Fast Beam |
| prefix_movement | Movimiento | Movement |
| soft_wave | Ola Suave | Soft Wave |
| unison_sweep_beams | Barrido Unison Beams | Unison Sweep Beams |
| unison_sweep_washes | Barrido Unison Washes | Unison Sweep Washes |
| soft_beams | Suaves Beams | Soft Beams |
| soft_washes | Suaves Washes | Soft Washes |
| cascade_beams | Cascada Beams | Cascade Beams |
| vertical_wave_washes | Ola Vertical Washes | Vertical Wave Washes |
| vertical_wave_beams | Ola Vertical Beams | Vertical Wave Beams |
| vertical_wave | Ola Vertical | Vertical Wave |
| unison_sweep | Barrido Unison | Unison Sweep |
| movement_shape | Movimiento {shape} | Movement {shape} |
| mode_together | Simultaneo | Together |
| mode_alternating | Alternado | Alternating |
| beams_fan | Beams Abanico | Beams Fan |
| beams_cross | Beams Cruce | Beams Cross |
| animation | {label} Animacion | {label} Animation |
| prism_label | Prisma | Prism |
| gobo_dealt | Gobo Repartido {number} | Dealt Gobo {number} |
| subset_odd | 1 y 3 | 1 and 3 |
| subset_even | 2 y 4 | 2 and 4 |
| subset_all | Todas | All |
| prism_subset | Prisma - {subset} | Prism - {subset} |
| prism_spin_fast | Prisma Giro Rapido | Prism Fast Spin |
| prism_spin_reverse | Prisma Giro Inverso | Prism Reverse Spin |
| gobo_rest | Gobo Reposo | Gobo Rest |
| prism_rest | Prisma Reposo | Prism Rest |
| dimmer_odd | Dimmer Impares | Dimmer Odd |
| dimmer_even | Dimmer Pares | Dimmer Even |
| smoke_off | Humo OFF | Smoke Off |
| talk_light_base | Luz Charla Base | Talk Light Base |

(`gobo_rest`, `prism_rest` and `talk_light_base` are used by Task 7.)

`[paths]`:

| identifier | es | en |
|---|---|---|
| path_movement | Movimiento | Movement |
| path_soft_movement | Movimiento Suave | Soft Movement |
| path_fast_movement | Movimiento Rapido | Fast Movement |
| path_movement_generated | Movimiento (generado) | Movement (generated) |
| path_parts | {path}/Partes | {path}/Parts |
| path_wheel_generated | {label} (generado) | {label} (generated) |
| path_prism | Prisma | Prism |
| path_prisms | Prismas | Prisms |
| path_play | Jugar/{family} | Play/{family} |
| path_family_colour | Color | Colour |
| path_family_pixels | Pixeles | Pixels |
| path_family_heads | Cabezas | Heads |
| path_levels | Niveles | Levels |
| path_haze | Humo | Haze |
| path_strobes | Strobos | Strobes |

**Module sites** (content -> replacement; `V` is `vocabulary`):

- `efx_algorithms.py`: delete `SPANISH_LABELS` (its two importers are below).
- `movement_efx.py`: default `path="Movimiento (generado)"` -> `None` ->
  `V.display("path_movement_generated")`; default `label_prefix="Movimiento"`
  -> `None` -> `V.display("prefix_movement")`; `f"{path}/Partes"` ->
  `V.render("path_parts", path=path)`; `SPANISH_LABELS.get(algorithm, algorithm)`
  -> the `EFX_SHAPE_IDENTIFIERS` expression. `" (16 bit)"`/`" (8 bit)"` stay.
- `movement_families.py`: the `_family(...)` calls pass
  `V.display("prefix_soft")`, `V.display("prefix_soft_beam")`,
  `V.display("prefix_wave")`, `"Wash"`, `"Beam"`, `V.display("prefix_sweep")`,
  `V.display("prefix_fast_wash")`, `V.display("prefix_fast_beam")` for the
  label prefixes, `V.display("path_soft_movement")`,
  `V.display("path_movement")`, `V.display("path_fast_movement")` for the
  paths, `V.display("soft_beams")`, `V.display("fast_washes")`,
  `V.display("fast_beams")` for the chaser names, and
  `names={"Line": V.display("soft_wave")}` /
  `names={"Line": V.display("unison_sweep_beams")}` for the two overrides.
  `"Suaves Washes"` -> `V.display("soft_washes")`; `"Movimientos Suaves"` ->
  `V.display("soft_movements")`; `"Movimientos Washes"` / `"Movimientos Beams"`
  -> `wash_movements` / `beam_movements`; `"Cascada Beams"`,
  `"Ola Vertical Washes"`, `"Ola Vertical Beams"`, `"Barrido Unison Washes"`,
  `"Barrido Unison Beams"` -> their identifiers above;
  `f"Wash {label} Simultaneo"` -> `f"Wash {label} {V.display('mode_together')}"`
  (and the `Beam` and `Alternado` variants with `mode_alternating`);
  `f"Movimiento {label}"` -> `V.render("movement_shape", shape=label)`;
  `f"Movimiento {label} {suffix}"` ->
  `V.render("movement_shape", shape=f"{label} {V.display(mode)}")` with the
  loop over `("mode_together", ...), ("mode_alternating", ...)` identifiers
  instead of the Spanish suffixes; `_figure("Ola Vertical", ...)` and
  `_figure("Barrido Unison", ...)` -> `vertical_wave` and `unison_sweep`;
  `_both("Movimientos Cabezas", ..., "Movimiento")` ->
  `head_movements`, `path_movement`; `"Movimientos Rapidos"` /
  `"Movimiento Rapido"` -> `fast_movements` / `path_fast_movement`.
- `home_position.py`: `"Cabezas Centro"` -> `V.display("heads_centre")`; path
  `"Movimiento"` -> `path_movement`.
- `cross_position.py` / `fan_position.py`: `"Beams Cruce"` / `"Beams Abanico"`
  -> `beams_cross` / `beams_fan`; path `"Movimiento"` -> `path_movement`.
- `stage_aim.py`: `"Escenario"` -> `V.display("stage_aim")`; path
  `"Movimiento"` -> `path_movement`.
- `wheel_scenes.py`: `f"{label} (generado)"` ->
  `V.render("path_wheel_generated", label=label)`; `f"{label} Animacion"` ->
  `V.render("animation", label=label)`. Default `label="Gobo"` stays.
- `dealt_gobo_scenes.py`: `f"Gobo Repartido {deal + 1}"` ->
  `V.render("gobo_dealt", number=deal + 1)`. Wheel slot words (`"open"`,
  `"no gobo"`, `"white light"`) are definition data (B6).
- `prism_spins.py`: `"Prisma Giro Rapido"` / `"Prisma Giro Inverso"` ->
  `prism_spin_fast` / `prism_spin_reverse`; default `path="Prisma"` ->
  `None` -> `V.display("path_prism")`.
- `beam_subsets.py`: `"1 y 3"`, `"2 y 4"`, `"Todas"` -> `subset_odd`,
  `subset_even`, `subset_all`; `"Prismas"` -> `path_prisms`;
  `f"Prisma - {name}"` -> `V.render("prism_subset", subset=name)`.
  `"MultiColor - ..."` and `"Off"` stay.
- `dimmer_chases.py`: `f"{path}/Partes"` -> `path_parts`; `"Dimmer PingPong"`
  -> `dimmer_pingpong`; `"Dimmer Impares"` / `"Dimmer Pares"` -> `dimmer_odd` /
  `dimmer_even`; `"Dimmer Chase"`, `"Dimmer Chase 2"` -> `dimmer_chase`,
  `dimmer_chase_2` (same words, but they are function identities).
- `dimmer_sequence.py`: `"Dimmer Secuencia"` -> `dimmer_sequence`.
- `dimmerless_intensity.py`: `"Intensidad Peak"` -> `peak_intensity`; path
  `"Niveles"` -> `path_levels` (the same in the next two modules).
- `energy_intensity.py`: `"Intensidad Ambiente"` / `"Intensidad Total"` ->
  `ambient_intensity` / `full_intensity`.
- `energy_levels.py`: `"Ciclo Energia"` -> `energy_cycle`.
- `smoke_auto.py`: `"Humo ON"` -> `smoke_on`; `"Humo OFF"` -> `smoke_off`;
  `"Humo Auto"` (both) -> `smoke_auto`; `f"Humo Auto {minutes} min"` ->
  `V.display(f"smoke_auto_{minutes}_min")` (`SMOKE_INTERVALS_MIN` is
  `(1, 2, 4, 8)`, and the catalogue has 2, 4 and 8); path `"Humo"` ->
  `path_haze`.
- `strobe_effects.py`: `"Strobo ON"`, `"Strobo OFF"`, `"Strobo Rapido"`,
  `"Strobo Medio"` -> `strobe_on`, `strobe_off`, `strobe_fast`, `strobe_medium`;
  path `"Strobos"` -> `path_strobes`.
- `vertical_smoke_burst.py`: `"Humo Vertical YA"` -> `vertical_smoke_now`; path
  `"Humo"` -> `path_haze`.
- `play_wrappers.py`: `f"Jugar · {original.attrib['Name']}"` ->
  `V.display("pick_prefix") + original.attrib["Name"]`; `f"Jugar/{family}"` ->
  `V.render("path_play", family=family)`; the family arguments `"Color"`,
  `"Pixeles"`, `"Cabezas"`, `"Prisma"` -> `path_family_colour`,
  `path_family_pixels`, `path_family_heads`, `path_prism`; `"Gobos"` stays.

- [ ] **Step 1: Write the failing tests**

Append the nineteen `generate/...` modules above, `"generate/gobo_shake.py"`
(nothing to change: its words are the same in both languages) and
`"efx_algorithms.py"` to `CONVERTED`. Append to `tests/test_catalogue_templates.py`:

```python
@pytest.mark.parametrize("language", ["es", "en"])
def test_wheel_animations_are_the_functions_keys_bind(language):
    names = shipped_names(language)
    assert names.render("animation", label="Gobo") == names.display("gobo_animation")
    prism = names.render("animation", label=names.display("prism_label"))
    assert prism == names.display("prism_animation")


@pytest.mark.parametrize("language", ["es", "en"])
def test_a_movement_pick_starts_with_the_movement_prefix(language):
    """play_page strips this prefix from pick captions (B8)."""
    names = shipped_names(language)
    prefix, _ = template_affixes(names, "movement_shape")
    assert names.render("movement_shape", shape="X").startswith(prefix)
```

Add the catalogue entries.

- [ ] **Step 2: Run to see the ratchet fail**

Run: `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_catalogue_templates.py -q -n 0`
Expected: the ratchet FAILS listing the modules' literals; if the catalogue
test fails, an English value breaks a composition: fix the English value.

- [ ] **Step 3: Convert the modules**, one at a time, `vibra_compare.py` after each.

- [ ] **Step 4: Run the tests**

Run: `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_catalogue_templates.py tests/test_movement_families.py tests/test_movement_mirror.py tests/test_wheel_scenes.py tests/test_play_generators.py tests/test_check.py -q`
Expected: all pass.

- [ ] **Step 5: Reinstall, gates, commit**

Pip reinstall, the five gate commands, `ruff`; stage the files under **Files**;
commit:

```text
refactor(qlctool): movement, wheel, intensity and smoke generators name through the catalogue

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
```

---

### Task 7: `build_canonical_show` names through the catalogue

**Files:**
- Modify: `qlctool/generate/canonical_show.py`, `qlctool/generate/moments.py`,
  both catalogues (one new entry, `paths.path_moments` = `Momentos` /
  `Moments`; add any other the scanner finds that Tasks 5-6 missed)
- Test: `tests/test_generator_literals.py`

**Interfaces:**
- Consumes: every identifier from Tasks 5-6; `vocabulary` (already bound at
  the top of `build_canonical_show`).
- Produces: `master` keyed by `vocabulary.display(...)` everywhere (B4);
  `_blackout(workspace, caps, name: str)` with the name required;
  `_steps_are_scenes`, `_tempo_functions` and `_movement_tempo_functions` take
  `vocabulary`.

**Sites** (content -> replacement, `V` = `vocabulary`):

| content | replacement |
|---|---|
| `"Blanco Total"` (scene name and `master[...]` key) | `V.display("full_white")` |
| `wheel_color="Blanco"` (four places) | `wheel_color=V.display("white")` |
| `"Todo Negro"`, `_blackout(..., name="Todo Negro")` default | `V.display("all_black")`; make `name` a required argument |
| `"Flash Color"` | `V.display("flash_colour")` |
| `"Flash 100%"`, `"Flash 50%"` | `V.display("flash_full")`, `V.display("flash_half")` |
| `f"Golpe {name}"` | `V.render("colour_hit", colour=name)` |
| `"Golpe Graves"` | `V.display("bass_hit")` |
| `"Efectos Paneles"` | `V.display("panel_effects")` |
| `"Ciclo Paneles Mixto"` | `V.display("panel_cycle")` |
| `"Efectos Propios"` | `V.display("path_builtin_effects")` |
| label `"Paneles"` passed to `generate_builtin_effects` | `V.display("panels_label")` |
| `"Humo Vertical"` | `V.display("vertical_smoke")` |
| `"Vel. Paneles Auto"` | `V.display("panel_speed_auto")` |
| `f"Matrices {group.name}"` | `V.render("matrices_of", group=group.name)` |
| `"Pixeles ON"` | `V.display("pixels_on")` |
| `"Intensidad Charla Pixeles"` | `V.display("talk_pixel_intensity")` |
| `"Paneles Charla"` | `V.display("talk_panels")` |
| `"Rueda Colores"`, `"Rueda Simples"`, `"Rueda Pastel"`, `"Rueda Multicolor"`, `"Rueda Mezcla"` | `colour_wheel`, `simple_wheel`, `pastel_wheel`, `multicolour_wheel`, `mix_wheel` |
| `scene_prefix="Rig Simple"` / `"Rig Pastel"` | `V.display("rig_prefix_simple")` / `V.display("rig_prefix_pastel")` |
| `f"Rig Multicolor {n}"`, `f"Rig 4 Colores {n}"` | `V.render("rig_multicolour", number=n)`, `V.render("rig_four_colours", number=n)` |
| `f"{step_name} + Pixeles"` | `V.render("with_pixels", name=step_name)` |
| `"Arcoiris Simultaneo"`, `"Arcoiris Pasos"` | `rainbow_together`, `rainbow_steps` |
| `"Movimientos Cabezas"`, `"Movimientos Rapidos"`, `"Cabezas Centro"` | `head_movements`, `fast_movements`, `heads_centre` |
| `"Gobo Animacion"`, `"Prisma Animacion"` | `gobo_animation`, `prism_animation` |
| `label="Prisma"`, `path="Prisma"` | `V.display("prism_label")`, `V.display("path_prism")` |
| `"Gobo Reposo"`, `"Prisma Reposo"` (rest scenes) | `V.display("gobo_rest")`, `V.display("prism_rest")` |
| `"Humo ON"`, `"Humo Vertical YA"`, `"Humo Auto"` | `smoke_on`, `vertical_smoke_now`, `smoke_auto` |
| `"Dimmer Chase"`, `"Dimmer Chase 2"`, `"Dimmer PingPong"`, `"Dimmer Secuencia"`, `"Dimmer Programas"` | `dimmer_chase`, `dimmer_chase_2`, `dimmer_pingpong`, `dimmer_sequence`, `dimmer_programmes` |
| `"Strobo Rapido"`, `"Strobo Medio"`, `"Strobo ON"`, `"Strobo OFF"` | `strobe_fast`, `strobe_medium`, `strobe_on`, `strobe_off` |
| `"Intensidad Ambiente"`, `"Intensidad Total"`, `"Intensidad Peak"` | `ambient_intensity`, `full_intensity`, `peak_intensity` |
| `"Nivel Ambiente"`, `"Nivel Fiesta"`, `"Nivel Peak"`, `"Nivel Fiesta Dinamico"` | `level_ambient`, `level_party`, `level_peak`, `level_dynamic` |
| `"Ciclo Energia"` | `energy_cycle` |
| `"AUTO"` | `V.display("auto")` |
| `"Momentos"` (paths), and `moments.py`'s `PATH = "Momentos"` | `V.display("path_moments")`; `generate_moments` takes `names` and the constant is deleted |
| `"Escenario"` | `V.display("stage_aim")` |
| `"Luz Charla Base"`, `"Luz Charla"` | `talk_light_base`, `talk_light` |
| `"Momento Charla"`, `"Momento Tranquilo"`, `"Momento Fiesta"`, `"Momento Locura"` | `talk_moment`, `calm_moment`, `party_moment`, `frenzy_moment` |
| `"Movimientos Washes"`, `"Movimientos Beams"`, `"Rapidos Washes"`, `"Rapidos Beams"` in `_movement_tempo_functions` | `wash_movements`, `beam_movements`, `fast_washes`, `fast_beams` |
| the wanted-name tuple in `_tempo_functions` | a tuple of identifiers mapped with `V.display` |

The beats branch: replace the `name.startswith("Ciclo Matrices")` filter with
the matrix chasers' own names, taken from the structure instead of parsed:

```python
        matrix_cycles = {
            names_by_id[m.chaser_id] for m in matrices if m.chaser_id is not None
        }
        timings.update({name: described.timing.matrix_beats for name in present if name in matrix_cycles})
```

where `names_by_id` is the id -> name map the branch already builds for
`present` (read the branch; if it builds names only, build
`{int(f.get("ID")): f.get("Name") for f in workspace.engine if f.tag.endswith("}Function")}`
the way the function's last lines count functions). `"Show"`, `"Even/Odd"`,
`"EFX"`, `"Color Beam"`, `"Gobo"`, `"Gobos"` stay (B6).

- [ ] **Step 1: Failing test.** Append `"generate/canonical_show.py"` and
  `"generate/moments.py"` to `CONVERTED`; run `.venv/bin/python -m pytest tests/test_generator_literals.py -q -n 0`;
  expected: FAIL listing `canonical_show.py` literals.
- [ ] **Step 2: Convert** in the order of the table, `vibra_compare.py` after
  each group of rows. Run the beats variant compare especially after the
  `Ciclo Matrices` change: `Vibra-beats.qxw` is the only file it touches.
- [ ] **Step 3: Tests.** `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_canonical_show.py tests/test_description_identifiers.py -q`; all pass.
- [ ] **Step 4: Gates, commit.** Five gates, `ruff`; commit
  `refactor(qlctool): the canonical show names every function through the catalogue`
  with the `Claude-Session` line.

---

### Task 8: Glyphs, pad bindings and pad colours keyed by identifier

**Files:**
- Create: `qlctool/names/localised_keys.py`
- Modify: `qlctool/control_glyph.py`, `qlctool/generate/smc_pad_bindings.py`,
  `qlctool/generate/smc_pad_colors.py`, `qlctool/generate/canonical_show.py`
  (localise the pad tables), `qlctool/generate/live_console.py` (only the
  `glyph(...)` call in `master_button`), both catalogues
- Test: `tests/test_canonical_show.py`, `tests/test_live_console.py`,
  `tests/test_input_profile.py`, `tests/test_pad_palette.py` (index updates),
  `tests/test_generator_literals.py`

**Interfaces:**
- Consumes: function identifiers from Tasks 5-6.
- Produces:
  - `localised_keys(table: Mapping[str, T], names: Names) -> dict[str, T]`
  - `GLYPHS`, `SMC_PAD_BINDINGS`, `FUNCTION_COLORS` keyed by identifier.
  - `glyph(identifier: str) -> str`.
  - `generate_live_console(..., glyphs: Mapping[str, str] | None = None)`:
    display-keyed; `None` means `localised_keys(GLYPHS, default_names())`.
  - Console identifiers for the pad's non-function widgets: `grand_master`,
    `tempo_dial`, `movement_speed`, `page_previous`, `page_next`, `stop_all`,
    `blackout`.

`qlctool/names/localised_keys.py`:

```python
"""An identifier-keyed table, keyed instead by the show's display names (ruling B4)."""

from collections.abc import Mapping
from typing import TypeVar

from .names import Names

T = TypeVar("T")


def localised_keys(table: Mapping[str, T], names: Names) -> dict[str, T]:
    """Same values, each key replaced by `names.display(key)`, order kept."""
    return {names.display(identifier): value for identifier, value in table.items()}
```

**Catalogue entries** `[console]`:

| identifier | es | en |
|---|---|---|
| grand_master | Master General | Grand Master |
| tempo_dial | Tempo Show | Show Tempo |
| movement_speed | Vel. Movimiento | Movement Speed |
| page_previous | Pagina Anterior | Previous Page |
| page_next | Pagina Siguiente | Next Page |
| stop_all | PARAR TODO | STOP ALL |
| blackout | APAGON | BLACKOUT |

**Rekeying** (same values, same order, key -> identifier):

- `GLYPHS`: `"AUTO"`->`auto`, `"Momento Charla"`->`talk_moment`,
  `"Momento Tranquilo"`->`calm_moment`, `"Momento Fiesta"`->`party_moment`,
  `"Momento Locura"`->`frenzy_moment`, `"Blanco Total"`->`full_white`,
  `"Todo Negro"`->`all_black`, `"Flash 100%"`->`flash_full`,
  `"Flash 50%"`->`flash_half`, `"Flash Color"`->`flash_colour`,
  `"Humo ON"`->`smoke_on`, `"Humo Vertical YA"`->`vertical_smoke_now`,
  `"Humo Vertical"`->`vertical_smoke`, `"Strobo Rapido"`->`strobe_fast`,
  `"Strobo Medio"`->`strobe_medium`, `"Humo Auto"`->`smoke_auto`,
  `"Humo Auto 2 min"`->`smoke_auto_2_min`, `"Humo Auto 4 min"`->`smoke_auto_4_min`,
  `"Humo Auto 8 min"`->`smoke_auto_8_min`, `"Rueda Colores"`->`colour_wheel`,
  `"Rueda Simples"`->`simple_wheel`, `"Rueda Pastel"`->`pastel_wheel`,
  `"Rueda Multicolor"`->`multicolour_wheel`, `"Rueda Mezcla"`->`mix_wheel`,
  `"Luz Charla"`->`talk_light`, `"Movimientos Cabezas"`->`head_movements`,
  `"Movimientos Suaves"`->`soft_movements`, `"Movimientos Rapidos"`->`fast_movements`,
  `"Cabezas Centro"`->`heads_centre`, `"Gobo Animacion"`->`gobo_animation`,
  `"Prisma Animacion"`->`prism_animation`, `"Arcoiris Simultaneo"`->`rainbow_together`,
  `"Arcoiris Pasos"`->`rainbow_steps`, `"Dimmer Chase"`->`dimmer_chase`,
  `"Dimmer Chase 2"`->`dimmer_chase_2`, `"Dimmer Secuencia"`->`dimmer_sequence`,
  `"Dimmer PingPong"`->`dimmer_pingpong`, `"Strobo ON"`->`strobe_on`,
  `"Strobo OFF"`->`strobe_off`. `leading_glyph.MARKS` reads `GLYPHS.values()`
  and is unaffected.
- `SMC_PAD_BINDINGS`: the function keys as above; `"Master General"`->
  `grand_master`, `"Tempo Show"`->`tempo_dial`, `"Vel. Movimiento"`->
  `movement_speed`, `"Pagina Anterior"`->`page_previous`, `"Pagina Siguiente"`->
  `page_next`, `"PARAR TODO"`->`stop_all`, `"APAGON"`->`blackout`. Keep every
  comment.
- `FUNCTION_COLORS`: the function keys as above.

In `canonical_show.py` pass
`pad_bindings=localised_keys(pad.bindings, vocabulary) if pad is not None else None`,
the same for `pad_colors`, and `glyphs=localised_keys(GLYPHS, vocabulary)`.
In `live_console.py`, `master_button`'s `mark = glyph(name)` becomes
`mark = glyphs.get(name, "")` with `glyphs` the new parameter (resolved at the
top of `generate_live_console` and passed down the way `pad_colors` is), and
the `"Pagina Siguiente"`, `"Pagina Anterior"`, `"PARAR TODO"`, `"APAGON"`,
`"Master General"`, `"Tempo Show"`, `"Vel. Movimiento"` strings passed to
`bind_pad` become `V.display(...)` of the identifiers above (Task 9 converts
the rest of the module; this task only keeps the pad lookups consistent).

**Test updates** (every index by a Spanish key becomes the identifier; where a
key is compared with a caption or used on `show.master_ids`, wrap it in
`default_names().display(key)`):

- `tests/test_canonical_show.py` (the pad-binding test near its
  `SMC_PAD_BINDINGS` import): `SMC_PAD_BINDINGS["Pagina Siguiente"]` ->
  `SMC_PAD_BINDINGS["page_next"]`, `["Pagina Anterior"]` -> `["page_previous"]`,
  `["PARAR TODO"]` -> `["stop_all"]`, `["APAGON"]` -> `["blackout"]`; the
  `inverse` map and `show.master_ids[name]` use `names.display(name)`.
- `tests/test_live_console.py` (the three tests importing `SMC_PAD_BINDINGS`,
  and the room-state glyph test): `SMC_PAD_BINDINGS["Vel. Movimiento"]` ->
  `["movement_speed"]`, `["Master General"]` -> `["grand_master"]`; the
  `captions -> name` map keys through identifiers; `glyph(name) for name, ...
  in ROOM_STATES` stays valid only after Task 9 rekeys `ROOM_STATES`: in this
  task change it to `glyph(default_names().identify(name, ("functions",)))`.
- `tests/test_input_profile.py` and `tests/test_pad_palette.py` iterate the
  tables without naming keys; they pass unchanged. Run them.

- [ ] **Step 1: Failing test.** Append `"control_glyph.py"`,
  `"generate/smc_pad_bindings.py"`, `"generate/smc_pad_colors.py"` to
  `CONVERTED`; add the console entries; run the ratchet: FAIL.
- [ ] **Step 2: Implement** `localised_keys`, rekey the three tables, wire
  them in `canonical_show.py` and `live_console.py`, update the tests.
- [ ] **Step 3: Tests.** `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_canonical_show.py tests/test_live_console.py tests/test_input_profile.py tests/test_pad_palette.py tests/test_controllers.py -q`; all pass.
- [ ] **Step 4: Gates, commit.** Pip reinstall, five gates, `ruff`; commit
  `refactor(qlctool): glyphs and SMC-PAD tables keyed by catalogue identifier`
  with the `Claude-Session` line.

---

### Task 9: The live console's captions, frames and help come from the catalogue

**Files:**
- Modify: `qlctool/generate/live_console.py`, both catalogues
- Test: `tests/test_generator_literals.py`, `tests/test_live_console.py`,
  `tests/test_catalogue_templates.py`

**Interfaces:**
- Consumes: `localised_keys`, `template_affixes`, Task 8's console entries.
- Produces: `generate_live_console(..., names: Names | None = None)`; the
  module tables become identifier tables:
  - `ROOM_STATES: tuple[tuple[str, str, tuple[int, int, int, int], str], ...]`
    = (function identifier, caption identifier, rect, font)
  - `HITS: tuple[tuple[str, str], ...]` = (function identifier, caption identifier)
  - `HELP_LINES`, `TEMPO_LINES`, `MOVEMENT_DIAL_LINES`, `GRAND_MASTER_LINES`,
    `LIBRARY_LINES`: tuples of `help` identifiers (`LIBRARY_LINES` keeps the
    literal `"· · ·"` separators between identifiers; resolve every entry that
    is not `"· · ·"`)
  - `SMOKE_RHYTHMS`: (function identifier, caption identifier)
  - `AUDIO_BANDS: tuple[tuple[str, str | None], ...]` = (band identifier,
    function identifier or None)
  - `SHORT_COLOURS = ("ultraviolet", "yellow", "magenta", "white", "orange")`
    and `MIX_COLOURS = ("red", "green", "blue", "yellow", "amber", "cyan",
    "magenta", "white", "orange", "pink", "ultraviolet")`: the captions look up
    `f"{colour}_short"` / `f"{colour}_code"`.
  - `LONG_WHEEL_NAME` keeps its fixture-data keys; its values become
    `rainbow_plus` / `rainbow_minus`.
  - `ROOM_FRAME`, `HITS_FRAME`, `SMOKE_FRAME`, `CHASES_FRAME`,
    `SMOKE_LIGHT_CAPTION` are deleted: read `frames.room_states`,
    `frames.hits`, `frames.haze`, `frames.intensity_chases`,
    `captions.vertical_smoke_light`.

**Catalogue entries.** `es` is the current literal verbatim (adjacent string
pieces joined exactly as Python joins them). `[console]`:

| identifier | es | en |
|---|---|---|
| room_auto | AUTO — el show se lleva solo · Q | AUTO — the show runs itself · Q |
| room_talk | CHARLA — alguien habla · F1 | TALK — someone is speaking · F1 |
| room_calm | TRANQUILO — bajón · F2 | CALM — a lull · F2 |
| room_party | FIESTA — marcha normal · F3 | PARTY — the usual pace · F3 |
| room_frenzy | LOCURA — todo a la vez · F4 | FRENZY — everything at once · F4 |
| room_white | BLANCO TOTAL — luz de trabajo · X | FULL WHITE — work light · X |
| room_black | TODO NEGRO — apaga las luces · º | ALL BLACK — lights off · º |
| hit_button_flash | FLASH · Espacio | FLASH · Space |
| hit_button_flash_slow | FLASH LENTO · - | SLOW FLASH · - |
| hit_button_flash_colour | FLASH COLOR · . | COLOUR FLASH · . |
| hit_button_smoke_now | HUMO YA · H | HAZE NOW · H |
| hit_button_vertical_smoke_now | HUMO VERT · U | VERTICAL HAZE · U |
| hit_button_strobe | STROBO · F | STROBE · F |
| hit_button_strobe_soft | STROBO SUAVE · T | SOFT STROBE · T |
| haze_every_1 | HUMO cada 1 min · J | HAZE every 1 min · J |
| haze_every_2 | cada 2 min | every 2 min |
| haze_every_4 | cada 4 min | every 4 min |
| haze_every_8 | cada 8 min | every 8 min |
| haze_word | HUMO | HAZE |
| band_bass | Graves | Bass |
| band_low_mid | Medios-graves | Low mids |
| band_mid | Medios | Mids |
| band_high_mid | Medios-agudos | High mids |
| band_high | Agudos | Highs |
| rainbow_plus | Arcoiris + | Rainbow + |
| rainbow_minus | Arcoiris - | Rainbow - |
| audio_triggers | Audio (hay que elegir entrada en Configuración) | Audio (pick an input in Configuration) |
| page_show | 1 · SHOW — pulsa AUTO y ya está. PgDn para el resto. | 1 · SHOW — press AUTO and that is all. PgDn for the rest. |
| panic_frame | SI ALGO VA MAL | IF SOMETHING GOES WRONG |
| stop_all_button | PARAR TODO · Retroceso | STOP ALL · Backspace |
| blackout_button | APAGON · Esc | BLACKOUT · Esc |
| page_control | 3 · CONTROL — bancos, ruedas de BEAM, cabezas, intensidad y humo. | 3 · CONTROL — banks, BEAM wheels, heads, intensity and haze. |
| bank_frame | Colores {group} — mantén 1-0 | Colours {group} — hold 1-0 |
| chase_sweep | Barrido de intensidad · V | Intensity sweep · V |
| chase_reverse | Barrido inverso · B | Reverse sweep · B |
| chase_odd_even | Pares / impares · Z | Odd / even · Z |
| chase_rotation | Rotación de barridos · K | Sweep rotation · K |
| chase_strobe_on | Strobo del fixture · S | Fixture strobe · S |
| chase_strobe_off | Parar ese strobo · D | Stop that strobe · D |
| bass_button | GOLPE GRAVES — lo pulsa el audio | BASS HIT — the audio presses it |
| beam_wheel_frame | Color de los BEAM — su rueda, no RGB | BEAM colour — its wheel, not RGB |
| aim_frame | Apunta las 12 cabezas a mano — arrastra dentro del cuadro | Aim the 12 heads by hand — drag inside the square |
| page_library | 4 · LIBRERÍA — de aquí sale el show. No hace falta tocar nada de esto durante una fiesta. | 4 · LIBRARY — the show comes from here. Nothing here needs touching during a party. |
| mixes_frame | Mezclas de dos colores — mantén pulsado | Two-colour mixes — hold down |
| group_label | Grupo: {group} | Group: {group} |
| multicolour_frame | MultiColor BEAM — dos colores a la vez en el haz | MultiColor BEAM — two colours at once in the beam |
| matrices_frame | Matrices — dibujos sobre las barras y los paneles | Matrices — patterns on the bars and panels |
| group_wheels_frame | Ruedas y ciclos por grupo — no usar a la vez que la rueda general: se suman los colores | Wheels and cycles per group — not together with the main wheel: the colours add up |
| group_colour_wheel_caption | Colores {group} | {group} colours |
| group_mix_wheel_caption | Mezcla {group} | {group} mix |
| panels_frame | Paneles — sus 42 efectos propios, sin ver todavía | Panels — their 42 built-in effects, not yet reviewed |
| panel_speed | Vel. Paneles | Panel Speed |
| panel_speed_auto_button | VEL. AUTO — sube y baja sola | AUTO SPEED — rises and falls by itself |
| live_matrix | Matriz en vivo | Live Matrix |
| xy_pad | Cabezas | Heads |
| hold_frame | {caption} — mantén pulsado | {caption} — hold down |

`[help]` (one row per label; `help_show_*` are the five `HELP_LINES`,
`tempo_*` the three `TEMPO_LINES`, `movement_dial_*` the three
`MOVEMENT_DIAL_LINES`, `grand_master_*` the five `GRAND_MASTER_LINES`,
`library_*` the nine non-separator `LIBRARY_LINES`, in order; `es` = the
literal, `en` as given):

| identifier | en |
|---|---|
| help_show_1 | Top: the state the room is in. Only ONE at a time — pressing another changes the state, they do not add up. AUTO is the normal one: colours, haze and the night rising and falling by itself. |
| help_show_2 | The MOMENTS are for when something happens: someone gets up to speak (TALK), the room drops (CALM), it goes well (PARTY), the last song (FRENZY). When the moment passes, press AUTO again. |
| help_show_3 | Bottom: the HITS. These DO add to whatever is playing. FLASH, STROBE and HAZE NOW work while you hold them and stop when you let go. |
| help_show_4 | STOP ALL switches every function off at once: the button for when something stayed on and you do not know which. |
| help_show_5 | PgDn / PgUp change page: 2 = PLAY, 3 = CONTROL, 4 = LIBRARY. The keys work from any page. |
| tempo_1 | TEMPO — tap M to the beat: colours, |
| tempo_2 | gobos, prism and dimmer follow your |
| tempo_3 | beat. The heads do too (page 3). |
| movement_dial_1 | Speed of the heads. The same |
| movement_dial_2 | M key as page 1's tempo: |
| movement_dial_3 | one figure is 16 taps. |
| grand_master_1 | GRAND MASTER — cuts the |
| grand_master_2 | intensity of the whole room |
| grand_master_3 | over whatever is already |
| grand_master_4 | on. Up = normal |
| grand_master_5 | (255), down = all off. |
| library_1 | This page is the store: the two-colour mixes, the matrices and |
| library_2 | the panels' 42 built-in effects. They are here to look at and to |
| library_3 | build AUTO with, not to press with the room full. |
| library_4 | The arrows in each frame's header change group: each group |
| library_5 | of lights has its own mixes and its own matrices. |
| library_6 | Nobody has watched the panels' 42 effects yet: the device |
| library_7 | only calls them «Effect N». Press, watch, and note which are worth it. |
| library_8 | The per-group wheels paint the same fixtures as the main wheel. |
| library_9 | Switching both on adds the two colours: it comes out white. |
| panic_help | STOP ALL stops the functions with a 1 second fade — press AUTO to resume. BLACKOUT darkens the room — press BLACKOUT again to bring it back, then AUTO. |
| vertical_smoke_help | The panels go to their colour cycles while the vertical haze fires. It stays on: switch it off when you are done. |
| panel_speed_help | Speed of the panels' effects. It follows the cycle's (200) until you move it; from then on the fader rules, zero included. The red X lets go. |

`[abbreviations]`: `ultraviolet_short` UV / UV, `yellow_short` Amar / Yell,
`magenta_short` Mage / Mage, `white_short` Blan / Whit, `orange_short` Nara / Orng.

`[mix_codes]`: `red_code` Ro / Rd, `green_code` Ve / Gn, `blue_code` Az / Bu,
`yellow_code` Am / Yw, `amber_code` Ab / Ar, `cyan_code` Cy / Cy,
`magenta_code` Ma / Ma, `white_code` Bl / Wh, `orange_code` Na / Or,
`pink_code` Rs / Pk, `ultraviolet_code` UV / UV (ruling B9: no English code
equals a different colour's Spanish code).

**Sites that parse names** (ruling B8):

- `_bank_caption(name)`: keep "the first word of the scene name"; the short
  map is `{V.display(c): V.display(f"{c}_short") for c in SHORT_COLOURS}`,
  built once in `generate_live_console` and passed down.
- `_mix_caption(name)`: the code map is
  `{V.display(c): V.display(f"{c}_code") for c in MIX_COLOURS}`, same way.
- `_wheel_caption` is deleted. The per-group wheel entries are built from the
  banks, not parsed:

  ```python
  entries = [
      (b.wheel_id, V.render("group_colour_wheel_caption", group=b.group_name))
      for b in banks
      if b.wheel_id is not None
  ]
  entries += [
      (b.mix_wheel_id, V.render("group_mix_wheel_caption", group=b.group_name))
      for b in banks
      if b.mix_wheel_id is not None
  ]
  ```

  (the `wheel_ids` list above it stays for whatever else reads it).
- `_after(names.get(...), "Ciclo ")` (two places) -> the marker is
  `template_affixes(V, "cycle")[0]`.
- `"Color Beam - "` and `"MultiColor - "` markers stay (wheel labels, B6).
- `f"Grupo: {bank.group_name}"` / `f"Grupo: {group}"` ->
  `V.render("group_label", group=...)`; `f"Colores {bank.group_name} — mantén 1-0"`
  -> `V.render("bank_frame", group=...)`; `f"{caption} — mantén pulsado"` ->
  `V.render("hold_frame", caption=caption)`.
- Room states, hits, haze rhythms: iterate the identifier tables and write
  `V.display(caption_id)`; call `master_button` with `V.display(function_id)`.

Add to `tests/test_catalogue_templates.py`:

```python
HIT_BUTTONS = {
    "hit_button_flash": "hit_flash",
    "hit_button_flash_slow": "hit_flash_slow",
    "hit_button_flash_colour": "hit_flash_colour",
    "hit_button_smoke_now": "hit_smoke_now",
    "hit_button_vertical_smoke_now": "hit_vertical_smoke_now",
    "hit_button_strobe": "hit_strobe",
    "hit_button_strobe_soft": "hit_strobe_soft",
}


@pytest.mark.parametrize("language", ["es", "en"])
def test_a_hit_button_starts_with_the_caption_the_desk_knows(language):
    """Ruling B7: the key hint rides in the caption; the head is the desk's word."""
    names = shipped_names(language)
    for button, caption in HIT_BUTTONS.items():
        assert names.display(button).split(" · ")[0] == names.display(caption)
```

In `tests/test_live_console.py`, every test that reads `ROOM_STATES`, `HITS`,
`SMOKE_RHYTHMS`, `ROOM_FRAME`-style constants resolves them through
`default_names()` (for example
`[names.display(c) for _, c, _, _ in ROOM_STATES]`); the glyph test becomes
`glyph(identifier) for identifier, _, _, _ in ROOM_STATES`.

- [ ] **Step 1: Failing test.** Append `"generate/live_console.py"` to
  `CONVERTED`, add the entries and the hit-button test; run the ratchet and
  the template tests: the ratchet FAILS.
- [ ] **Step 2: Convert** the module top to bottom: tables first, then
  `_page_show`, `_page_control`, `_page_library`, `_wheel_frame`, the parse
  helpers. `vibra_compare.py` after each page function.
- [ ] **Step 3: Tests.** `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_catalogue_templates.py tests/test_live_console.py tests/test_canonical_show.py tests/test_shipped_deskmap.py -q`; all pass.
- [ ] **Step 4: Gates, commit.** Pip reinstall, five gates, `ruff`; commit
  `refactor(qlctool): the live console's words come from the catalogue`
  with the `Claude-Session` line.

---

### Task 10: The JUGAR page's words come from the catalogue

**Files:**
- Modify: `qlctool/generate/play_page.py`, `qlctool/generate/live_console.py`
  (pass `names` to `build_play_page`), both catalogues
- Test: `tests/test_generator_literals.py`, `tests/test_play_generators.py`,
  `tests/test_catalogue_templates.py`

**Interfaces:**
- Consumes: `template_affixes`, the `frames.family_*`, `frames.colour_hits`,
  `captions.pick_prefix`, `captions.hit_*`, `console.haze_word` entries.
- Produces: `build_play_page(..., vocabulary: Names | None = None)` (the
  existing `names` parameter is the id -> function-name map and keeps its
  name); `FAMILY_FRAMES = ("family_colour", "family_pixels", "family_heads",
  "family_gobos", "family_prism")` (identifiers); `RESET_FRAME`,
  `COLOR_HITS_FRAME`, `PICK_PREFIX` deleted (read `console.reset_frame`,
  `frames.colour_hits`, `captions.pick_prefix`); `_RESET_NAMES` becomes
  function identifiers (`auto`, `talk_moment`, `calm_moment`, `party_moment`,
  `frenzy_moment`, `full_white`, `all_black`, `flash_full`, `flash_colour`,
  `smoke_on`, `strobe_fast`).

**Catalogue entries** `[console]`:

| identifier | es | en |
|---|---|---|
| reset_frame | VOLVER AL SHOW | BACK TO THE SHOW |
| page_play | 2 · JUGAR — toma una familia; AUTO dentro de ella la devuelve. | 2 · PLAY — take a family; AUTO inside it gives it back. |
| hook_colours | Colores completos · W | Full colours · W |
| hook_simple | Colores simples · C | Simple colours · C |
| hook_pastel | Pastel tenue · L | Soft pastel · L |
| hook_multicolour | Multicolor · R | Multicolour · R |
| hook_mix | Mezcla · E | Mix · E |
| hook_rainbow_together | Arcoiris junto · ' | Rainbow together · ' |
| hook_rainbow_steps | Arcoiris fases · ¡ | Rainbow phases · ¡ |
| hook_panels_auto | AUTO paneles | AUTO panels |
| hook_heads_slow | AUTO lento | AUTO slow |
| hook_heads_normal | AUTO normal · A | AUTO normal · A |
| hook_heads_fast | AUTO rapido | AUTO fast |
| hook_gobos | AUTO gobos · G | AUTO gobos · G |
| hook_prism | AUTO prisma · P | AUTO prism · P |
| gobo_pages | Gobos para elegir — 2 paginas | Gobos to pick — 2 pages |
| reset_talk | CHARLA | TALK |
| reset_calm | TRANQUILO | CALM |
| reset_party | FIESTA | PARTY |
| reset_frenzy | LOCURA | FRENZY |
| reset_white | BLANCO | WHITE |
| reset_black | NEGRO | BLACK |
| centre_caption | Centro | Centre |
| rest_caption | Reposo | Rest |

(Check `hook_heads_normal` and `hook_gobos`: their `es` and `en` are equal,
which is allowed. "AUTO normal · A" must not already exist in `[console]`.)

`[help]`:

| identifier | en |
|---|---|
| colour_guidance | Fixed pick; repeating it stops it and leaves the family still. AUTO colours or Q/F1-F4 brings the wheel back; stopping it cuts its 800 ms fade. |
| cycle_guidance | Under AUTO, the energy cycle takes it back on its next step (8 min at most); to play for long, pick a Moment first. |
| reset_guidance | Back all the way: AUTO twice if it is already green, or Backspace and Q. |
| pixels_guidance | Press an effect and it stays. AUTO panels brings its cycle back. |

(`es` = the literals `_COLOR_GUIDANCE`, `_CYCLE_GUIDANCE`, the `"Volver del
todo: ..."` label and the `"Pulsa un efecto y se queda. ..."` label.)

**Sites:**

- Hook tables (`("Rueda Colores", "Colores completos · W")` ...): become
  `(function identifier, console identifier)` pairs:
  `colour_wheel/hook_colours`, `simple_wheel/hook_simple`,
  `pastel_wheel/hook_pastel`, `multicolour_wheel/hook_multicolour`,
  `mix_wheel/hook_mix`, `rainbow_together/hook_rainbow_together`,
  `rainbow_steps/hook_rainbow_steps`, `soft_movements/hook_heads_slow`,
  `head_movements/hook_heads_normal`, `fast_movements/hook_heads_fast`,
  `gobo_animation/hook_gobos`, `prism_animation/hook_prism`; single names
  (`"Luz Charla"`, `"Ciclo Paneles Mixto"`, `"Paneles Charla"`,
  `"Cabezas Centro"`, `"Gobo Reposo"`, `"Prisma Reposo"`) -> `talk_light`,
  `panel_cycle`, `talk_panels`, `heads_centre`, `gobo_rest`, `prism_rest`; the
  captions `"Centro"` (heads centre button) and `"Reposo"` (both rest buttons,
  ruling B9: one identifier) -> `centre_caption` and `rest_caption`.
- `_pick_caption(name)`: the prefixes are
  `template_affixes(V, "movement_shape")[0]`,
  `V.display("panels_label") + " - "`, `"Gobo - "` (label, B6),
  `V.display("prism_label") + " - "`; the suffix is
  `template_affixes(V, "with_pixels")[1]`. `_source_name` strips
  `V.display("pick_prefix")`. Both take `V` as an argument.
- `_reset_caption(name)`: a map from `V.display(function)` to
  `V.display(caption)` built from: `talk_moment/reset_talk`,
  `calm_moment/reset_calm`, `party_moment/reset_party`,
  `frenzy_moment/reset_frenzy`, `full_white/reset_white`,
  `all_black/reset_black`, `flash_full/hit_flash`, `flash_colour/hit_flash_colour`,
  `smoke_on/haze_word`, `strobe_fast/hit_strobe` (B9: reuse, the words are
  equal).

Add to `tests/test_catalogue_templates.py`:

```python
@pytest.mark.parametrize("language", ["es", "en"])
def test_a_pixel_pick_ends_with_the_pixels_suffix(language):
    names = shipped_names(language)
    _, suffix = template_affixes(names, "with_pixels")
    assert names.render("with_pixels", name="X").endswith(suffix)
    assert suffix.strip()
```

- [ ] **Step 1: Failing test.** Append `"generate/play_page.py"` to
  `CONVERTED`; add entries and the test; ratchet FAILS.
- [ ] **Step 2: Convert**, `vibra_compare.py` after each family builder.
- [ ] **Step 3: Tests.** `.venv/bin/python -m pytest tests/test_generator_literals.py tests/test_catalogue_templates.py tests/test_play_generators.py tests/test_live_console.py tests/test_solo_handoff.py -q`; all pass.
- [ ] **Step 4: Gates, commit.** Pip reinstall, five gates, `ruff`; commit
  `refactor(qlctool): the JUGAR page's words come from the catalogue`
  with the `Claude-Session` line.

---

### Task 11: The desk map and the desk bursts speak the workspace's language

**Files:**
- Create: `qlctool/names/workspace_language.py`
- Modify: `qlctool/generate/desk_bursts.py`, `qlctool/desk_policy.py`,
  `qlctool/deskmap.py`, `qlctool/desk_burst_note.py`, `qlctool/cmd_deskmap.py`,
  `qlctool/generate/canonical_show.py` (pass `names=vocabulary` to
  `generate_desk_bursts`), both catalogues
- Test: `tests/test_workspace_language.py`, `tests/test_desk_bursts.py`,
  `tests/test_shipped_deskmap.py` (must pass unchanged),
  `tests/test_generator_literals.py`

**Interfaces:**
- Consumes: `shipped_names`, `shipped_languages`, `load_catalogue`,
  `desk_widgets` (reads `Caption` from frames and buttons).
- Produces:
  - `workspace_language(root: etree._Element) -> str`
  - `generate_desk_bursts(workspace, names: Names | None = None) -> list[int]`
  - `build_deskmap(workspace, library, path, names=None)`: `None` now means
    `shipped_names(workspace_language(workspace.root))`.
  - `desk_burst_note(identifier: str, names: Names) -> str | None`
  - `qlctool deskmap --description show.toml` passes
    `description_names(load_show_description(...))`.
  - `SAFETY_DETAIL_BY_FUNCTION`, `SAFETY_CAPTION_BY_FUNCTION` keyed by function
    identifier (`all_black`, `dimmer_pingpong`, `vertical_smoke`), valued by
    catalogue identifier or `None`; `SECTION_TITLES` and `PAGES` valued by
    catalogue identifier.

`qlctool/names/workspace_language.py`:

```python
"""Which shipped language a saved workspace was generated in (ruling B12).

The room-states frame is on every generated console, and its title differs in
every catalogue, so it identifies the language without reading any function
name. A workspace without it (a hand-built one) is read as Spanish, the
language every such workspace in this repository was built in.
"""

from lxml import etree

from ..xmlutil import iter_local
from .load_catalogue import load_catalogue
from .shipped_languages import shipped_languages


def workspace_language(root: etree._Element) -> str:
    """The first shipped language whose room-states title is a frame caption here."""
    captions = {frame.get("Caption", "") for frame in iter_local(root, "Frame")}
    for language in shipped_languages():
        if load_catalogue(language)["frames"]["room_states"] in captions:
            return language
    return "es"
```

(If `desk_widgets.py` reads frame captions through a helper rather than
`frame.get("Caption")`, use the same helper; a frame's caption in `.qxw` is
its `Caption` attribute, `desk_widgets.py` reads `element.attrib.get("Caption")`.)

**Catalogue entries.** `[generated]`:

| identifier | es | en |
|---|---|---|
| desk_burst_scene | Desk · {caption} (ráfaga) | Desk · {caption} (burst) |
| desk_burst_cue | Desk · {caption} ráfaga {seconds} s | Desk · {caption} burst {seconds} s |

`[console]`:

| identifier | es | en |
|---|---|---|
| desk_page_live | LIVE | LIVE |
| desk_page_control | CONTROL | CONTROL |
| desk_section_state | LA SALA ESTÁ ASÍ | THE ROOM IS |
| desk_section_accents | GOLPES | HITS |
| desk_section_haze | HUMO AMBIENTE | AMBIENT HAZE |
| desk_section_hooks | AUTO | AUTO |
| desk_section_picks | ELEGIR | PICK |
| desk_section_chases | BARRIDOS DE INTENSIDAD | INTENSITY SWEEPS |
| desk_section_haze_light | LUZ DEL HUMO VERTICAL | VERTICAL HAZE LIGHT |
| desk_caption_vertical_smoke_light | Luz del humo vertical | Vertical haze light |
| desk_caption_odd_even | Pares / impares | Odd / even |

`[help]`:

| identifier | es | en |
|---|---|---|
| desk_bursts_help | Tablet: ráfagas con límite; soltar las para antes. Colores pueden mezclarse. | Tablet: bounded bursts; releasing stops them early. Colours may mix. |
| desk_detail_not_stop | no es parar | not a stop |
| desk_detail_fire_now | dispara ya | fires now |
| desk_note_strobe | Sin prioridad Override: otro barrido de shutter puede pisar el estrobo. | No Override priority: another shutter sweep can override the strobe. |
| desk_note_flash | Luz a máxima intensidad; rueda de color y estrobo pueden ser pisados por el show. | Full intensity light; the colour wheel and strobe can be overridden by the show. |
| desk_note_flash_colour | Conserva el color del show; otro barrido de shutter puede pisar el estrobo. | Keeps the show's colour; another shutter sweep can override the strobe. |
| desk_note_colour | Sin ForceLTP ni Override: el color se suma al show; rueda y estrobo pueden ser pisados. | No ForceLTP or Override: the colour adds to the show; wheel and strobe can be overridden. |

(`desk_page_live`, `desk_page_control` and `desk_section_hooks` are equal in
both languages: allowed. The desk's page titles for the families reuse
`frames.family_*`.)

**Sites:**

- `generate/desk_bursts.py`: the help label -> `V.display("desk_bursts_help")`;
  `f"Desk · {caption} (ráfaga)"` -> `V.render("desk_burst_scene", caption=caption)`;
  `f"Desk · {caption} ráfaga {duration / 1000:g} s"` ->
  `V.render("desk_burst_cue", caption=caption, seconds=f"{duration / 1000:g}")`;
  `desk_burst_duration(source, default_names())` -> `(source, V)`.
- `desk_policy.py`: `BURST_FRAME = "Ráfagas del desk"` is deleted, read
  `frames.desk_bursts`; `PAGES` titles -> `desk_page_live`, `family_colour`,
  `family_pixels`, `family_heads`, `family_gobos`, `family_prism`,
  `desk_page_control`; `SECTION_TITLES` values -> the `desk_section_*`
  identifiers; `SAFETY_DETAIL_BY_KEY` -> `SAFETY_DETAIL_BY_FUNCTION =
  {"all_black": "desk_detail_not_stop", "dimmer_pingpong": None,
  "vertical_smoke": None}`; `SAFETY_CAPTION_BY_KEY` ->
  `SAFETY_CAPTION_BY_FUNCTION = {"vertical_smoke":
  "desk_caption_vertical_smoke_light", "dimmer_pingpong":
  "desk_caption_odd_even"}`; `SAFETY_DETAIL_BY_ROLE = {"haze":
  "desk_detail_fire_now"}`. `HELD_REASON` stays (English in both). Where the
  map is built (in `deskmap.py`), a widget's function identifier is
  `names.lookup(function_name, ("functions",))` (first match) - the same
  catalogue lookup Plan A uses for frames - and every title is
  `names.display(...)`.
- `deskmap.py`: `caption.removeprefix("HUMO ")` ->
  `caption.removeprefix(names.display("haze_word") + " ")`; `names` defaults
  as in Interfaces.
- `desk_burst_note.py`: return `names.display("desk_note_...")` for the four
  texts; callers pass their `names`.
- `cmd_deskmap.py`: add `--description` (optional); when given,
  `names = description_names(load_show_description(args.description, workspace.root))`.

Write `tests/test_workspace_language.py`:

```python
"""Ruling B12 (2026-09-25): the desk reads a workspace in the language it was written in."""

from pathlib import Path

from lxml import etree

from qlctool.names.load_catalogue import load_catalogue
from qlctool.names.workspace_language import workspace_language
from qlctool.workspace import Workspace

SHOW = Path(__file__).resolve().parents[3] / "QLC+ Setups" / "Vibra.qxw"


def _console(caption: str) -> etree._Element:
    return etree.fromstring(f'<Workspace><VirtualConsole><Frame Caption="{caption}"/></VirtualConsole></Workspace>')


def test_the_shipped_show_is_spanish():
    assert workspace_language(Workspace.load(SHOW).root) == "es"


def test_an_english_room_frame_means_english():
    title = load_catalogue("en")["frames"]["room_states"]
    assert workspace_language(_console(title)) == "en"


def test_a_hand_built_console_is_read_as_spanish():
    assert workspace_language(_console("Anything")) == "es"
```

- [ ] **Step 1: Failing tests.** Write the test file, append
  `"generate/desk_bursts.py"`, `"desk_policy.py"`, `"deskmap.py"`,
  `"desk_burst_note.py"` to `CONVERTED`, add the entries. Run
  `.venv/bin/python -m pytest tests/test_workspace_language.py tests/test_generator_literals.py -q -n 0`:
  FAIL.
- [ ] **Step 2: Implement** the unit and the sites.
- [ ] **Step 3: Tests.** `.venv/bin/python -m pytest tests/test_workspace_language.py tests/test_generator_literals.py tests/test_desk_bursts.py tests/test_shipped_deskmap.py tests/test_deskmap.py tests/test_desk_identifiers.py tests/test_controllers.py -q`;
  all pass, and
  `test_shipped_deskmap` proves `Vibra.desk.json` is byte-identical.
- [ ] **Step 4: Gates, commit.** Pip reinstall, five gates, `ruff`; commit
  `refactor(qlctool): the desk map reads the workspace in its own language`
  with the `Claude-Session` line.

---

### Task 12: Lift the Spanish-only gate; an English Vibra passes every check

**Files:**
- Delete: `qlctool/names/check_generator_vocabulary.py`
- Rename: `qlctool/names/generator_language.py` -> `qlctool/names/default_language.py`
  (`DEFAULT_LANGUAGE = "es"`, docstring: "The language a description is
  written in when `[show]` does not say (ruling B11).")
- Modify: `qlctool/generate/canonical_show.py`,
  `qlctool/description/load_show_description.py` (remove the call and the
  error-section logic that read `GENERATOR_LANGUAGE`),
  `qlctool/description/reading/read_show.py` (import `DEFAULT_LANGUAGE`),
  `tests/test_description_identifiers.py`, `tests/test_newshow_description.py`,
  `tests/test_load_show_description.py`, `tests/test_generator_literals.py`
- Create: `tests/test_english_vibra.py`, `tests/test_pseudo_locale.py`
- Docs: `AGENTS.md`, `tools/qlctool/README.md`, `docs/toolkit.md`,
  `/Users/cristiandeluxe/p/DMX-Fixtures/TODO.md`, `TODO_LOG.md`

**Interfaces:**
- Consumes: everything above.
- Produces: `build_canonical_show` and `load_show_description` accept any
  shipped language and any override that keeps the fields.

- [ ] **Step 1: Write the failing tests**

`tests/test_english_vibra.py`:

```python
"""Spec step 3, completed 2026-09-25: Vibra described in English is a correct show.

The same patch, the same description, `language = "en"`: every name the
generator writes comes from the English catalogue, and every check that passes
on the Spanish show passes on this one.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from qlctool.checks.run import check_workspace
from qlctool.deskmap import build_deskmap
from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.names.load_catalogue import load_catalogue
from qlctool.validate import qlcplus_binary, validate_workspace
from qlctool.vibra.description import vibra_description
from qlctool.workspace import Workspace
from qlctool.xmlutil import iter_local

SETUPS = Path(__file__).resolve().parents[3] / "QLC+ Setups"


@pytest.fixture(scope="module")
def english():
    workspace = Workspace.load(SETUPS / "Vibra.qxw")
    library = FixtureLibrary.load()
    description = replace(vibra_description(), language="en", names={})
    show = build_canonical_show(
        workspace,
        library,
        plot_path=str(SETUPS / "vibra-stage-plot.json"),
        description=description,
    )
    return workspace, library, show


def test_the_console_speaks_english(english):
    workspace, _, show = english
    en = load_catalogue("en")
    captions = {w.get("Caption", "") for w in iter_local(workspace.root, "Frame")}
    assert en["frames"]["room_states"] in captions
    assert en["frames"]["hits"] in captions
    assert "Party Moment" in show.master_ids
    assert "Momento Fiesta" not in show.master_ids


def test_every_check_passes(english):
    workspace, library, _ = english
    assert check_workspace(workspace, library) == []


def test_the_desk_map_builds(english):
    workspace, library, _ = english
    deskmap = build_deskmap(workspace, library, "english.qxw")
    assert deskmap["controls"]


@pytest.mark.skipif(qlcplus_binary() is None, reason="QLC+ is not installed on this machine")
def test_qlcplus_loads_it(english, tmp_path):
    workspace, _, _ = english
    out = tmp_path / "Vibra-en.qxw"
    workspace.save(out)
    assert validate_workspace(out).errors == []
```

(Check `ShowDescription`'s overrides field is `names` and
`validate_workspace(...).errors` is the error list: both hold on 2026-09-25.
`CanonicalShow.master_ids` is the display-keyed map Plan A exposes.)

`tests/test_pseudo_locale.py`:

```python
"""No Spanish word survives an English build (2026-09-25).

Every catalogue identifier is overridden with a marker that keeps its fields,
so any function name, path or caption that still comes out in Spanish was
written by the generator, not the catalogue.
"""

import re
from dataclasses import replace
from pathlib import Path

from qlctool.generate.canonical_show import build_canonical_show
from qlctool.library import FixtureLibrary
from qlctool.names.load_catalogue import load_catalogue
from qlctool.names.template_fields import template_fields
from qlctool.vibra.description import vibra_description
from qlctool.workspace import Workspace
from qlctool.xmlutil import iter_local

SETUPS = Path(__file__).resolve().parents[3] / "QLC+ Setups"


def _pseudo() -> dict[str, str]:
    english = load_catalogue("en")
    return {
        identifier: f"⟦{identifier}⟧" + "".join(f"{{{f}}}" for f in template_fields(text))
        for entries in english.values()
        for identifier, text in entries.items()
    }


def _spanish_words() -> set[str]:
    spanish, english = load_catalogue("es"), load_catalogue("en")
    words: set[str] = set()
    for section, entries in spanish.items():
        for identifier, text in entries.items():
            if english[section][identifier] != text:
                words |= {w for w in re.findall(r"[^\W\d_]{4,}", text) if w not in english[section][identifier]}
    return words


def test_no_spanish_catalogue_word_is_written():
    workspace = Workspace.load(SETUPS / "Vibra.qxw")
    description = replace(vibra_description(), language="en", names={"en": _pseudo()})
    build_canonical_show(workspace, FixtureLibrary.load(), description=description)
    written = [
        value
        for element in iter_local(workspace.root, "Function")
        for value in (element.get("Name", ""), element.get("Path", ""))
    ] + [element.get("Caption", "") for element in workspace.root.iter() if element.get("Caption")]
    written += [label.text or "" for label in iter_local(workspace.root, "Label")]
    leaks = sorted({w for text in written for w in _spanish_words() if re.search(rf"\b{w}\b", text)})
    assert leaks == []
```

(If the description's colour names collide with the pseudo overrides - a
palette colour must keep resolving - exclude the `colors` section from
`_pseudo()` and from `_spanish_words()`: colours are the description's own
data. Fixture, group and wheel-slot names in the patch are data too; if the
test reports a word that comes from the patch (`grep -c "<word>" "QLC+
Setups/Vibra.qxw"` is non-zero before generation), add it to an explicit,
commented `PATCH_WORDS` exclusion set in the test.)

Append to `tests/test_generator_literals.py`:

```python
# Ruling B6: modules that keep their literals, and why.
EXCLUDED = {
    "generate/input_profile.py",  # the SMC-PAD device file, byte-tested against the .qxi
    "generate/channel_probe.py",  # standalone `probe` command (B5)
    "generate/color_palette.py",  # standalone `palette` command (B5)
    "generate/vc_layout.py",  # standalone `layout` command (B5)
    "generate/__init__.py",
}


def test_every_generator_module_is_converted_or_excluded():
    modules = {
        str(path.relative_to(PACKAGE))
        for path in (PACKAGE / "generate").glob("*.py")
    }
    assert modules - set(CONVERTED) - EXCLUDED == set()
```

Run: `.venv/bin/python -m pytest tests/test_english_vibra.py tests/test_pseudo_locale.py tests/test_generator_literals.py -q -n 0`
Expected: FAIL with "the generator still writes its Spanish vocabulary
literally" from the English fixture, and possibly a list of unconverted
modules from the coverage test. On 2026-09-25 the modules outside
`canonical_show`'s import graph are exactly `channel_probe`, `color_palette`,
`input_profile`, `smc_pad_bindings`, `smc_pad_device` and `vc_layout`; every
other module is on the newshow path. A listed module with no Spanish word in
it (`bind_pad`, `beat_tempo`, `color_scene`, `rest_scene`, `stage_layout`,
`smc_pad_device`, ...) is appended to `CONVERTED` as is - the scanner proves it
clean. A module that still has one is converted exactly as Tasks 5-11 do, or
excluded with a one-line reason that fits ruling B6.

- [ ] **Step 2: Lift the gate**

`git rm qlctool/names/check_generator_vocabulary.py`;
`git mv qlctool/names/generator_language.py qlctool/names/default_language.py`
and rename the constant to `DEFAULT_LANGUAGE`; in `read_show.py` use
`table.get("language", DEFAULT_LANGUAGE)` and update its docstring ("the
language to Spanish (B11)"); remove the import and the
`check_generator_vocabulary(...)` call from `canonical_show.py` and
`load_show_description.py`, together with the `try`/`except` block around the
call in `load_show_description.py` that chose between `[show]` and `[names]`
for the error message (it has nothing left to report). In `tests/test_description_identifiers.py`,
replace `test_the_generator_refuses_a_vocabulary_it_cannot_write_yet` and
`test_build_refuses_an_english_description` with one test that
`build_canonical_show` on `replace(vibra_description(), language="en")`
succeeds and names a function "Party Moment"; rewrite the module docstring's
sentence about refusing to "Since Plan B (2026-09-25) the generators' own
literals come from the catalogue too, so any shipped language builds."
In `tests/test_newshow_description.py`, the `language = "en"` case now builds:
assert exit 0 and an English frame title in the output. In
`tests/test_load_show_description.py`, drop the `('[show]\nlanguage = "en"\n', ...)`
refusal case.

- [ ] **Step 3: Run the new tests until they pass**

Run: `.venv/bin/python -m pytest tests/test_english_vibra.py tests/test_pseudo_locale.py tests/test_generator_literals.py tests/test_description_identifiers.py tests/test_newshow_description.py tests/test_load_show_description.py -q`

Each failure of `test_every_check_passes` on the English show is a place where
a check or the desk still depends on a Spanish spelling, or where an English
name broke a composition. Per `CLAUDE.md`: find the cause, and if a check was
reading a name, make it read the graph or the catalogue identifier. Each
`test_pseudo_locale` leak is a literal the ratchet missed: convert it where it
is written.

- [ ] **Step 4: Docs and backlog**

- `docs/toolkit.md`: a "Languages" section - `[show] language` picks `en` or
  `es`; every generated name comes from `qlctool/locales/<lang>.toml`;
  `[names.<lang>]` overrides any identifier and must keep a template's
  `{fields}`; `check` messages are still Spanish (B10).
- `tools/qlctool/README.md`: one line that `language = "en"` works.
- `AGENTS.md`: replace the R1 note ("the generator refuses anything but
  Spanish") with the new rule and the two tests that guard it.
- `TODO.md`: close "generator names through the catalogue" and the R3
  coupling item; add an open item "Check messages and `Finding.rule` names
  through the catalogue (ruling B10, spec 'Multilingual')" with the smallest
  next step "give `Finding` a `rule_id` and move the messages into a
  `checks` catalogue section"; log the closed items in `TODO_LOG.md`.

- [ ] **Step 5: Gates, commit, push**

Pip reinstall, five gates, `ruff` on touched files, then commit:

```text
feat(qlctool): any shipped language builds a show; English Vibra passes every check

check_generator_vocabulary is gone: every name the generator, the console,
the JUGAR page and the desk map write now comes from the catalogue. An
English Vibra builds, passes check_workspace with no finding and loads in
QLC+, and a pseudo-locale build leaks no Spanish catalogue word.

Claude-Session: https://claude.ai/code/session_012XuQbe2HPjWjZHsRx4HjVw
```

Then `git pull --rebase origin main` and `git push origin main`.

---

## Self-review against the spec

- Spec "Multilingual": identifiers and `en`/`es` catalogues (Plan A);
  "generated names come from the catalogue through `language`" - Tasks 4-12;
  "Checks and the desk map resolve widgets through the identifiers" - Task 11
  plus Plan A; "check messages" - deferred by ruling B10, logged in `TODO.md`.
- Spec "Controllers": "`tablet_desk` owns ... `valid_desk_bursts`" and "a show
  without a controller block ... its checks do not run" - Task 2 removes the
  last core call into desk code; the registry stays (R10), now without names in
  core.
- Spec "Order" step 6 - Task 3.
- The QLC+ discovery item is outside the spec's steps; it exists so that the
  gates' `--validate` and the ten QLC+ tests run on this Mac without a
  variable - Task 1.
- Byte identity - Global Constraint 1, re-run in every task; the harness is
  `tests/vibra_compare.py`.
- Placeholder scan: every new unit has its code; the module conversions give
  every literal's identifier and both values. The tables for help text list
  the English value and point at the Spanish literal verbatim, because the
  Spanish value must be copied from the source byte for byte, not retyped.
- Names used across tasks: `Names.render`, `template_affixes`,
  `template_fields`, `localised_keys`, `workspace_language`,
  `EFX_SHAPE_IDENTIFIERS`, `ToolkitConfig`, `fixture_dirs`, `library_for`,
  `qlcplus_candidates`, `bounded_latches` - each defined once, in the task
  named in the file map, with the signature every later task uses.
