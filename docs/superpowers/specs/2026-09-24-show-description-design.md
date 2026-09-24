# A show description anyone can write

Date: 2026-09-24. Status: design approved in conversation by the owner; this
file is the written form, pending the owner's read.

## Why

"La idea es que cualquiera pueda usar la herramienta para generar sus shows"
(owner, 2026-09-24). Today `qlctool newshow` generates a complete show from
any patched workspace, and most of it already reasons about capabilities - a
colour wheel, RGB mixing, a gobo - rather than fixture names. What stops
anyone else from using it is that the Vibra show's own choices are written into
the code: its Spanish palette, its matrix effects for groups called
`BarrasLed`, `Cabezas` and `PAR`, its timings, its 1440x900 console, its
keyboard shortcuts, its captions, and an SMC-PAD that is wired into every show.

The toolkit then moves to its own repository, `spectalive/qlctool`, and this
repository becomes one show built with it.

## What the user writes

The patch stays where lighting people already make it: in QLC+. The user
patches fixtures, groups and universes, saves the workspace, and writes one
description next to it:

```toml
[show]
name = "Vibra"
language = "es"            # captions and names in the generated show

[rig]
workspace = "Vibra.qxw"    # the patch and the groups are read from here
stage_plot = "vibra-stage-plot.json"

[palette]                  # names in any supported language: red == rojo
colors = { red = [255, 0, 0], fire_red = [255, 20, 0], pink = [255, 0, 100] }
primary = ["red", "green", "blue", "ultraviolet", "yellow", "cyan", "magenta"]

[[groups.BarrasLed.matrices]]
script = "Sine Wave"
colors = ["red", "blue"]
properties = { orientation = "Horizontal" }

[timing]
bpm = 120
levels = { ambient_s = 240, party_s = 480, peak_s = 40, dynamic_s = 240 }

[fixture_tuning]
beam_focus = 127
strobe = { fast = 0.97, slow = 0.785 }

[console]
canvas = { width = 1440, height = 900 }
keys = { auto = "Q", talk_moment = "F1" }

[controllers]
midi_pad = "smc-pad"       # optional; omitted means no pad binding
tablet_desk = true         # optional; omitted means no desk map
```

`qlctool newshow --description show.toml` writes the whole show. Every
section is optional and falls back to a documented default, so the smallest
description is `[rig] workspace = "..."`.

TOML because Python reads it with the standard library (`tomllib`), so the
toolkit gains no dependency.

## Multilingual

Everything the generator names - colours, functions, frames, pages, captions,
check messages - gets a stable identifier in English snake case (`red`,
`fire_red`, `party_moment`, `colour_wheel`) and a display name per language.

- Catalogues live in `qlctool/locales/<lang>.toml`, one per language, `en` and
  `es` to start; a new language is a new file.
- The description may name a colour or function by its identifier or by its
  display name in any shipped language: `rojo`, `Rojo` and `red` are the same
  colour. An unknown or ambiguous name is an error that lists the matches.
- `[show] language` picks the display names written into the workspace.
- A description may override a display name (`[names.es] party_moment =
  "Momento Fiesta"`), which is how a show keeps its own vocabulary.

Checks and the desk map resolve widgets through the identifiers, never through
the Spanish strings they search for today.

## Controllers

The SMC-PAD binding and the tablet desk map become optional controller
profiles, each self-contained: `smc-pad` owns its device map, input profile,
bindings and the checks that verify them (`rule_pad_input`); `tablet_desk` owns
the desk map, the desk policy and the burst checks (`rule_desk_bursts`,
`valid_desk_bursts`, `desk_burst_errors`). A show without a controller block
gets neither, and its checks do not run.

The checker finds controller checks through a registry of rule providers
(Python entry points, group `qlctool.rules`), so `qlctool check <workspace>`
keeps running every check that applies, including a show's own.

## Vibra becomes the example

`vibra-lighting` keeps its three workspaces, its stage plots and a
`vibra.toml` (plus `vibra-split.toml` and the `--beats` variant) holding
exactly today's values, with `language = "es"` and Spanish name overrides where
the show's vocabulary differs from the catalogue.

## The rule that governs the refactor

**The three Vibra workspaces come out byte-identical at every step.** Before
the first change, regenerate `Vibra.qxw`, `Vibra-beats.qxw` and
`Vibra-split.qxw` and store their hashes; after every task, regenerate and
compare. The suite (`pytest tests/ -q`), `qlctool check` on each workspace and
`--validate` in headless QLC+ must also pass. A task that changes a byte is
wrong until the difference is explained and accepted by the owner.

## Order

1. Record the baseline hashes and a regeneration script that compares them.
2. Move the data tables (palette, primaries, pairs, curated matrices, timings,
   tuning, console geometry, keys) into a `ShowDescription` dataclass, with
   `vibra` values as the default; no behaviour change.
3. Identifiers and the `en`/`es` catalogues; generated names come from the
   catalogue through `language`.
4. Controller profiles and the rule-provider registry; the SMC-PAD and desk
   code and checks move behind them.
5. The TOML loader, validated against the patch like `stage_plot.py`, and
   `newshow --description`; Vibra's descriptions written out.
6. Library paths no longer assume this repository's layout (`library.py`,
   `install_plan.py`).
7. A second example rig with a different patch and no controllers, generated,
   checked and validated, to prove the description is enough.
8. Extract `tools/qlctool` and the toolkit docs to `spectalive/qlctool` with
   `git filter-repo`; this repository depends on a tagged release.

## Out of scope

Declaring the patch itself in the description (QLC+ remains the patch
editor), the MCP server for AI control, and the other splits (`fixtures`,
`smc-pad`, the launcher, `dmxdesk`), which each get their own design.
