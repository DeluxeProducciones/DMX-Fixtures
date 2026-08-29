# AGENTS.md

Instructions for AI coding agents working in this repository. Humans: start
with [README.md](README.md). The engineering rules (the check-rule workflow,
what "fixed" means here) are in [CLAUDE.md](CLAUDE.md) and are not repeated
in this file.

## What this is

A lighting-show repository, not an app: XML data (QLC+ `.qxw` workspaces,
`.qxf` fixture definitions, one `.qxi` MIDI input profile) plus one Python
package, `tools/qlctool` (Python >= 3.11, venv currently 3.14.7, lxml only),
that generates and checks the show. There is no CI and no server; the
"deploy" is the show Mac pulling this repo by hand.

## Blast radius

The generated workspaces are what a real venue runs. Two things can do real
damage:

- **The smoke pumps.** A scene that writes a value above zero to a fog
  machine's pump channel outside the smoke scenes is a tank emptying itself
  into a room. The check rules guard this (`rule_smoke`, `rule_smoke_light`);
  never weaken them to make a generator's output pass.
- **This repo is public.** Never commit machine access, addresses, accounts
  or credentials. Private context lives in the owner's notes, outside the
  repo.

Everything else is safe: generation always writes files, never DMX, and
tests never touch the `QLC+ Setups/` files in place (they build from the
reference workspace into a temp dir).

## Branch model

Work happens on `qlctool` (currently ~89 commits ahead); `main` is a year
stale and the merge is an open TODO item. Push finished, verified work to
`origin/qlctool`. A push is not a deploy - the show Mac pulls by hand.

## Build and run

```bash
cd tools/qlctool
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest tests/ -q          # full suite, ~5 min - looks hung, is not
.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
```

`qlctool check` (semantic rules) and `qlctool validate` (does QLC+ load it)
are different questions; run both sides via the recipe below before calling
show work done.

## Regenerating the show (verified recipe)

All three workspaces regenerate together or not at all, each from its own
patch and plot. Run against macOS with `/Applications/QLC+.app` installed,
2026-08-29, every command ended in `Validated: QLC+ loaded it with no
complaints`:

```bash
cd tools/qlctool
.venv/bin/qlctool newshow "../../QLC+ Setups/Vibra.qxw" \
  --plot "../../QLC+ Setups/vibra-stage-plot.json" \
  --out "../../QLC+ Setups/Vibra.qxw" --validate
.venv/bin/qlctool newshow "../../QLC+ Setups/Vibra.qxw" \
  --plot "../../QLC+ Setups/vibra-stage-plot.json" --beats \
  --out "../../QLC+ Setups/Vibra-beats.qxw" --validate
.venv/bin/qlctool newshow "../../QLC+ Setups/Vibra-split.qxw" \
  --plot "../../QLC+ Setups/vibra-stage-plot-split.json" \
  --out "../../QLC+ Setups/Vibra-split.qxw" --validate
```

If the SMC-PAD's map changed, regenerate its input profile in the same pass -
the shows carry the profile's *name*, the profile carries the numbers:

```bash
.venv/bin/qlctool input-profile "../../QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi"
```

Smoke test, same date and machine:

```bash
.venv/bin/python -m pytest tests/ -q
# -> 323 passed in 327.78s (0:05:27)
.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
# -> 427 botones revisados, ningun problema
```

## Traps

- **Never hand-edit a generated `.qxw`** (`Vibra*.qxw`): the next `newshow`
  erases the edit. A wanted change goes into the generator plus a test, or it
  does not survive the week.
- **`newshow` regenerates FROM the file it reads**: `Vibra.qxw` and
  `Vibra-split.qxw` are each their own patch source. Regenerating Vibra from
  `DeluxeEventos2.qxw` fails - that reference patch is two fixtures behind
  the rig (see docs/rig.md).
- `--validate` needs a QLC+ binary; discovery order is in
  `qlctool/validate.py` (`QLCTOOL_QLCPLUS` env var overrides). Without one
  installed, validation silently cannot run - do not claim it passed.
- `*.autosave.qxw` files are QLC+'s transient editor state, gitignored;
  never read one as the show.
- **The MIDI input profile is generated, not written.** It comes from
  `qlctool/generate/smc_pad_device.py` via
  `qlctool input-profile "../../QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi"`, and
  `tests/test_input_profile.py` fails if the shipped copy drifts. It must also
  be copied to the OS-level QLC+ folder to take effect locally (macOS:
  `~/Library/Application Support/QLC+/InputProfiles/`); the repo copy is the
  source of truth. Re-measuring the pad means editing `smc_pad_device.py` and
  regenerating - never hand-editing the `.qxi`, which is how it came to declare
  the pad's factory notes for a day while the show used different ones.
- Widget captions and check output are **Spanish on purpose** (the operator
  reads them); code, comments, commits and docs are English.

## Conventions

One exported unit per file in `qlctool` (see repo CLAUDE.md chain). Commits
are narrative English one-liners plus a body that names the cause, dated
regressions in tests ("date it and say which night it came from"). Finished,
verified work is committed and pushed without asking.
