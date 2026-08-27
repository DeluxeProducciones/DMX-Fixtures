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

## The backlog

`TODO.md` in this repo, not `~/p/TODO.md` — it moved here on 2026-08-26. Read
it at the start and end of related work; closed items go to `~/p/TODO_LOG.md`
with the date and the evidence, then out of the backlog.

## QLC+'s own source is at `~/p/qlcplus`

A clone of upstream QLC+ (`master`, the QLC+ 5 line the show runs). When a
question is about what QLC+ actually does - which XML tags an engine loads,
how a chaser times its steps, what the 3D view can and cannot render, what an
RGBMatrix blend mode really is - **read that clone**, not the web and not
`strings` over the installed binary. `engine/src/` is the engine,
`qmlui/` is the QLC+ 5 UI and 3D preview, `resources/rgbscripts/` the matrix
algorithms.

## What lives where

- `QLC+ Setups/` - the workspaces. `Vibra-split.qxw` carries the current patch.
- `QLC+ Fixtures/` - fixture definitions, verified against the manuals.
- `docs/` - the public findings: the file format, the rig, how the show is
  operated, the checks, the toolkit.
- `tools/qlctool/` - the generator. One exported unit per file.
- `TODO.md` - what is still open, and what is blocked on somebody watching the
  rig.

The private context - the show machine, its access, and the decisions behind
the work - is in `~/p/brain/projects/vibra-dmx.md`.
