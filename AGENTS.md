# AGENTS.md

Instructions for AI coding agents working in this repository. Humans: start
with [README.md](README.md). The engineering rules (the check-rule workflow,
what "fixed" means here) are in [CLAUDE.md](CLAUDE.md) and are not repeated
in this file.

## What this is

A lighting-show repository, not an app: XML data (QLC+ `.qxw` workspaces,
`.qxf` fixture definitions, one `.qxi` MIDI input profile) and the show's own
tests in `tests/`. The Python toolkit that generates and checks the show,
`qlctool` (Python >= 3.11, venv currently 3.14.7; lxml, pygdtf, pymvr), lives in
https://github.com/spectalive/qlctool since 2026-09-25 and is installed from a
pinned tag (`requirements.txt`, `v0.1.0`) into the repo-root `.venv`. There is
no CI and no server; the "deploy" is the show Mac pulling this repo by hand.

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

Work happens on `main` since 2026-09-22, when `qlctool` was merged into it
(`40f06f8`, `4fa1a74`); the branch still exists, fully merged. Push finished,
verified work to `origin/main`. A push is not a deploy - the show Mac pulls by
hand.

## Build and run

From the repository root:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                 # the show's tests against the pinned toolkit
.venv/bin/python -m pytest -q -n 0            # serial, for a debugger
.venv/bin/qlctool check "QLC+ Setups/Vibra-split.qxw"
```

The toolkit's own suite, its quality gate and its docs (`toolkit.md`,
`checks.md`, `qxw-format.md`, `qlcplus-environment.md`,
`qlc5-verification.md`) are in https://github.com/spectalive/qlctool.

qlctool finds the rig's definitions through the repo-root `qlctool.toml`; a
rig elsewhere names them with `[rig] fixtures`, `QLCTOOL_FIXTURES` or
`qlctool --fixtures DIR`.

`qlctool check` (semantic rules) and `qlctool validate` (does QLC+ load it)
are different questions; run both sides via the recipe below before calling
show work done.

## Reinstalling after the extraction (2026-09-25)

```text
Every checkout that had the in-repo toolkit and its venv:
  git status --short && git stash    # FIRST: the show Mac saves workspaces in place; a reset erases them
  git fetch origin && git reset --hard origin/main   # not git pull: the history was rewritten on 2026-09-25
  (cd tools && rm -rf qlctool)    # only the ignored venv and caches are left there
  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  .venv/bin/qlctool install --check
Machines: the MacBook, the show Mac (vibra-oficina), the Mac mini. The Mac
mini's launcher opens the workspace in the DMX-Fixtures-qlctool worktree
(branch qlctool) and does not use the toolkit; that worktree is left to the
owner.
Changing the toolkit: work in spectalive/qlctool, tag a release, bump the tag
in requirements.txt, reinstall, and run the show's tests here.
```

After the reset, `git stash pop` (or copy the saved workspace back) and diff it.

## Regenerating the show (verified recipe)

All three workspaces regenerate together or not at all, each from its own
patch and plot, from the repository root. Run against macOS with `/Applications/QLC+.app` installed,
2026-08-29, every command ended in `Validated: QLC+ loaded it with no
complaints`:

```bash
.venv/bin/qlctool newshow "QLC+ Setups/Vibra.qxw" \
  --plot "QLC+ Setups/vibra-stage-plot.json" \
  --out "QLC+ Setups/Vibra.qxw" --validate
.venv/bin/qlctool newshow "QLC+ Setups/Vibra.qxw" \
  --plot "QLC+ Setups/vibra-stage-plot.json" --beats \
  --out "QLC+ Setups/Vibra-beats.qxw" --validate
.venv/bin/qlctool newshow "QLC+ Setups/Vibra-split.qxw" \
  --plot "QLC+ Setups/vibra-stage-plot-split.json" \
  --out "QLC+ Setups/Vibra-split.qxw" --validate
```

Since the show-description refactor (2026-09-24) the same three regenerate from
their descriptions, which carry the patch, the plot and every show choice:

```bash
.venv/bin/qlctool newshow --description "QLC+ Setups/vibra.toml" --validate
.venv/bin/qlctool newshow --description "QLC+ Setups/vibra-beats.toml" --validate
.venv/bin/qlctool newshow --description "QLC+ Setups/vibra-split.toml" --validate
```

`.venv/bin/python tests/vibra_compare.py --descriptions --validate` does all
three into a temp dir and fails on any changed byte, check finding or QLC+
complaint. After a pull that touched `requirements.txt`, run
`.venv/bin/pip install -r requirements.txt`: the desk and pad checks are found
through the installed package's `qlctool.rules` entry points, and
`qlctool check` refuses to run without them.

If the SMC-PAD's map changed, regenerate its input profile in the same pass -
the shows carry the profile's *name*, the profile carries the numbers:

```bash
.venv/bin/qlctool input-profile "QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi"
```

QLC+ runs on *copies* of the repo's definitions, profile and gobos, and a
copy it was never handed is the silent failure here: the show loads, validates
and runs on last week's channel map. Before validating, and on the show Mac
after every pull:

```bash
.venv/bin/qlctool install --check   # exit 1 and a list when QLC+ is behind
.venv/bin/qlctool install           # copy what it lacks; restart QLC+ after
```

Smoke test, 2026-09-25, Mac mini, against `v0.1.0`:

```bash
.venv/bin/python -m pytest -q
# -> 30 passed
.venv/bin/python tests/vibra_compare.py --validate
# -> Vibra-split.qxw: identical, 0 finding(s), QLC+ loaded it (and the other two)
.venv/bin/qlctool check "QLC+ Setups/Vibra-split.qxw"
# -> QLC+ Setups/Vibra-split.qxw: 522 botones revisados, ningun problema
```

## Traps

- **Never hand-edit a generated `.qxw`** (`Vibra*.qxw`): the next `newshow`
  erases the edit. A wanted change goes into the generator plus a test, or it
  does not survive the week.
- **`newshow` regenerates FROM the file it reads**: `Vibra.qxw` and
  `Vibra-split.qxw` are each their own patch source. Regenerating Vibra from
  `DeluxeEventos2.qxw` fails - that reference patch is two fixtures behind
  the rig (see docs/rig.md).
- `--validate` needs a QLC+ binary. `qlctool` finds `/Applications/QLC+
  <version>.app` by itself, newest first, widgets build before QML, skipping a
  binary this CPU cannot run (the x86_64 `QLC+ 4.13.1.app` on an arm64 Mac
  without Rosetta). `QLCTOOL_QLCPLUS` still overrides it. Without any QLC+
  installed, validation silently cannot run - do not claim it passed.
- `*.autosave.qxw` files are QLC+'s transient editor state, gitignored;
  never read one as the show.
- **Installed copies drift.** On 2026-09-01 four of the eleven definitions
  in `~/Library/Application Support/QLC+/Fixtures` were a week behind the
  repo - among them the fog machine's pump group, which is what stops a
  released Flash from fogging on. `qlctool install --check` is the question;
  nothing else asks it, QLC+ least of all.
- **The MIDI input profile is generated, not written.** It comes from
  `qlctool/generate/smc_pad_device.py` in https://github.com/spectalive/qlctool via
  `qlctool input-profile "QLC+ InputProfiles/M-VAVE-SMC-PAD.qxi"`, and
  `tests/test_input_profile.py` fails if the shipped copy drifts. It must also
  be copied to the OS-level QLC+ folder to take effect locally (macOS:
  `~/Library/Application Support/QLC+/InputProfiles/`); the repo copy is the
  source of truth. Re-measuring the pad means editing `smc_pad_device.py` and
  regenerating - never hand-editing the `.qxi`, which is how it came to declare
  the pad's factory notes for a day while the show used different ones.
  Its header comment still names the toolkit's old in-repo path: it is
  byte-tested against the pinned release and changes with the next toolkit
  release.
- Every generated name comes from the catalogue in `[show] language` (`en` or
  `es`, Spanish by default); a generator module may not spell a catalogue word
  itself, apart from ruling B6's listed exclusions. In the toolkit repository,
  `tests/test_generator_literals.py` holds every `generate/` module to that,
  and `tests/test_english_vibra.py` builds Vibra in English and requires
  every check to pass. Vibra itself is Spanish on purpose (the operator reads
  it), and so is `check` output for now (ruling B10); code, comments, commits
  and docs are English.

## Conventions

One exported unit per file (see repo CLAUDE.md chain); the toolkit keeps the
same rule in its own repository. Commits
are narrative English one-liners plus a body that names the cause, dated
regressions in tests ("date it and say which night it came from"). Finished,
verified work is committed and pushed without asking.
