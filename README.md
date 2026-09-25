# DMX-Fixtures - the Vibra lighting show

Everything the Vibra venue's lighting runs on: the fixture definitions
verified against their manuals, the QLC+ workspaces the show plays from, the
MIDI controller that drives it, and the tests that hold
[`qlctool`](https://github.com/spectalive/qlctool) - the generator that builds
the whole show and the console it is operated from - to it. The toolkit lives
in its own repository since 2026-09-25; this one installs a pinned release.

This repository is **public**. Machine access - addresses, accounts,
credentials - is deliberately not in it.

## What lives where

| Path | What it is |
| --- | --- |
| `QLC+ Setups/` | The workspaces. `Vibra-split.qxw` carries the current patch; `Vibra.qxw` and `Vibra-beats.qxw` are the same show in other flavours. `DeluxeEventos2.qxw` is the hand-built original, kept as the reference the generators are tested against. |
| `QLC+ Fixtures/` | Fixture definitions (`.qxf`), each verified against the manual in `Manual/`. |
| `QLC+ InputProfiles/` | `M-VAVE-SMC-PAD.qxi` - the MIDI controller's input profile, captured from the real device. |
| `Manual/` | The rig's manuals, including the scanned leaflets nobody else has. |
| `docs/` | The findings: rig, operation, controller, viewer. Start at [docs/README.md](docs/README.md). The file format, checks and toolkit docs moved with the toolkit to [spectalive/qlctool](https://github.com/spectalive/qlctool). |
| `tests/` | The show's tests: the pinned toolkit still generates the three workspaces byte for byte. |
| `requirements.txt` | The toolkit, pinned to a `spectalive/qlctool` release. |
| `tools/qlc-launcher/` | [The QLC+ Vibra Dock app](tools/qlc-launcher/README.md), which starts the show with verified tablet web access. |
| `tools/smc-pad/` | The MIDI/BLE tools that mapped the controller and reverse-engineered its LED protocol. |
| `TODO.md` | The backlog, including what is blocked on somebody standing at the rig. |

## The show, briefly

The show is generated, not hand-built: `qlctool newshow` derives colour
scenes, matrices, movement, gobo/prism animation, smoke and a four-page
virtual console from the patch itself. One button (**AUTO**, key `Q`) runs
the night; moments (`F1`-`F4`), hits (flash, smoke, strobe) and manual
layers ride on top. [docs/show-operation.md](docs/show-operation.md) explains
the operating model.

## The controller

An M-VAVE SMC-PAD drives the console over USB-MIDI (port
`SINCO SMC-PAD-Master`, omni channel mode "1-16"). The mapping is generated
into every workspace - see `qlctool/generate/smc_pad_bindings.py` in
[spectalive/qlctool](https://github.com/spectalive/qlctool) for the map and its
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

From the repository root:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q               # the show's tests, parallel
.venv/bin/qlctool check "QLC+ Setups/Vibra-split.qxw"
```

Regenerating the show means regenerating **all three** workspaces and
validating each in headless QLC+ (`--validate`); the exact commands are in
[AGENTS.md](AGENTS.md), along with the traps. The engineering rules - above
all *"a malfunction is not fixed until a check can see it"* - are in
[CLAUDE.md](CLAUDE.md).

## Licence

Open, so anyone can use it:

- **Code** - the tools under `tools/`, the show's tests in `tests/`, the
  fixture definitions in `QLC+ Fixtures/` and the input profiles in
  `QLC+ InputProfiles/` - is under
  the [Apache License 2.0](LICENSE), the licence QLC+ itself uses.
- **The show and its material** - the workspaces in `QLC+ Setups/`, `docs/`
  and `Colores/` - is under [CC BY 4.0](LICENSE-CC-BY-4.0): use it, change
  it, perform it, and credit Vibra.
- **`Manual/` is not ours.** Those are the manufacturers' manuals, kept for
  reference; they stay under their owners' copyright and neither licence
  covers them.

Two fixture definitions are QLC+'s own, under QLC+'s Apache-2.0 (see
[NOTICE](NOTICE)): `Stairville-CLB2.4-CompactLED.qxf` and the
`Stairville-CLB2.4-PAR-Strobe.qxf` split from it. The toolkit, and the QLC+
files it vendors, carry their licences in their own repository,
[spectalive/qlctool](https://github.com/spectalive/qlctool).
