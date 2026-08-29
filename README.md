# DMX-Fixtures - the Vibra lighting show

Everything the Vibra venue's lighting runs on: the fixture definitions
verified against their manuals, the QLC+ workspaces the show plays from, the
MIDI controller that drives it, and `qlctool` - the generator that builds the
whole show and the console it is operated from.

This repository is **public**. Machine access - addresses, accounts,
credentials - is deliberately not in it.

## What lives where

| Path | What it is |
| --- | --- |
| `QLC+ Setups/` | The workspaces. `Vibra-split.qxw` carries the current patch; `Vibra.qxw` and `Vibra-beats.qxw` are the same show in other flavours. `DeluxeEventos2.qxw` is the hand-built original, kept as the reference the generators are tested against. |
| `QLC+ Fixtures/` | Fixture definitions (`.qxf`), each verified against the manual in `Manual/`. |
| `QLC+ InputProfiles/` | `M-VAVE-SMC-PAD.qxi` - the MIDI controller's input profile, captured from the real device. |
| `Manual/` | The rig's manuals, including the scanned leaflets nobody else has. |
| `docs/` | The findings: file format, rig, operation, checks, toolkit. Start at [docs/README.md](docs/README.md). |
| `tools/qlctool/` | The generator and checker. |
| `tools/smc-pad/` | The MIDI/BLE tools that mapped the controller and reverse-engineered its LED protocol. |
| `TODO.md` | The backlog, including what is blocked on somebody standing at the rig. |

## The show, briefly

The show is generated, not hand-built: `qlctool newshow` derives colour
scenes, matrices, movement, gobo/prism animation, smoke and a three-page
virtual console from the patch itself. One button (**AUTO**, key `Q`) runs
the night; moments (`F1`-`F4`), hits (flash, smoke, strobe) and manual
layers ride on top. [docs/show-operation.md](docs/show-operation.md) explains
the operating model.

## The controller

An M-VAVE SMC-PAD drives the console over USB-MIDI (port
`SINCO SMC-PAD-Master`, omni channel mode "1-16"). The mapping is generated
into every workspace - see
`tools/qlctool/qlctool/generate/smc_pad_bindings.py` for the map and its
capture notes:

- **Pads 13-16**: flash, slow flash, colour flash, colour beam
- **Pads 9-12**: vertical smoke, smoke, strobe, soft strobe
- **Pads 5-8**: AUTO, fiesta, locura, tranquilo
- **Pads 1-3**: full white, blackout scene, charla (pad 4 free on purpose)
- **SHIFT + top rows**: the eight manual layers
- **Encoders 1-3**: grand master, colour wheel speed, movement speed
- **`<` / `>`**: console pages; **pause** = stop all; **record** = blackout

QLC+ setup on a new machine: copy the `.qxi` into QLC+'s InputProfiles
folder, then Inputs/Outputs -> universe 1 -> Input on `SMC-PAD-Master`,
profile "M-VAVE SMC-PAD", MIDI channel **1-16**.

## Working on it

```bash
cd tools/qlctool
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest tests/ -q        # ~5 min
.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"
```

Regenerating the show means regenerating **all three** workspaces and
validating each in headless QLC+ (`--validate`); the exact commands are in
[AGENTS.md](AGENTS.md), along with the traps. The engineering rules - above
all *"a malfunction is not fixed until a check can see it"* - are in
[CLAUDE.md](CLAUDE.md).
