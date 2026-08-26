# DMX-Fixtures

The Vibra lighting show: the fixture definitions, the QLC+ workspaces, and
`tools/qlctool`, which generates the whole show and the console it is run from.

## A malfunction is not fixed until a check can see it

This show ran on luck for months. A colour was wrong, somebody nudged it, and
nobody could say whether the next workspace would be right - "a veces
acertamos" (owner, 2026-08-26). Every one of those failures turned out to be a
rule nobody had written down, so writing them down is the work:

1. **Find the cause, not the symptom.** "The beams are dark" is a symptom. "A
   generator that reasons in red, green and blue says nothing at all to a
   fixture whose colour is a wheel" is a cause, and it predicts the next four
   bugs.
2. **Add a rule to `qlctool check`** (`tools/qlctool/qlctool/checks/`) that
   sees the cause. A rule reasons about capabilities and the function graph -
   never about a function's name.
3. **Add a regression test to `tests/test_check.py`** that puts the bug back
   into a generated show and asserts the checker bites. Date it and say which
   night it came from.
4. **Run it over every workspace this repo ships**, which the gate test does.
   A rule that is only true of one file is not a rule.
5. Only then fix the generator, and regenerate.

`qlctool check <workspace>` is the command. It is a different question from
`qlctool validate`, which only asks whether QLC+ can load the file.

## Before finishing

```bash
cd tools/qlctool
.venv/bin/python -m pytest tests/ -q          # the whole suite
.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
```

Regenerating a show means regenerating all three (`Vibra.qxw`,
`Vibra-beats.qxw`, `Vibra-split.qxw`) and validating each with `--validate`,
which loads it in headless QLC+.

## What lives where

- `QLC+ Setups/` - the workspaces. `Vibra-split.qxw` carries the current patch.
- `QLC+ Fixtures/` - fixture definitions, verified against the manuals.
- `docs/` - the public findings: the file format, the rig, how the show is
  operated, the checks, the toolkit.
- `tools/qlctool/` - the generator. One exported unit per file.

The private context - the show machine, its access, and the decisions behind
the work - is in `~/p/brain/projects/vibra-dmx.md`.
