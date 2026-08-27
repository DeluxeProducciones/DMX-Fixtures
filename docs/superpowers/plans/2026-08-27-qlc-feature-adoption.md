# QLC+ Feature Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt the QLC+ capabilities the 2026-08-27 audit found unused or
misused: console safety controls, a live audio band, a wider matrix and EFX
repertoire, visible Peak intensity, and an operations runbook — every claim
already verified against source by the Codex cross-check.

**Architecture:** Everything flows through `tools/qlctool` (the generator);
the three workspaces are build artifacts and are never edited by hand. Each
behavioural change lands as: builder/generator change → dated regression test
→ `qlctool check` rule when a malfunction class is involved → regenerate all
three workspaces → headless-QLC+ validation. QLC+5-only features are gated on
Task 1's verification against the installed 5.2.2 binary.

**Tech Stack:** Python 3 (`tools/qlctool`, pytest), QLC+ 4.13-format XML
loaded by QLC+ 5.2.2, headless QLC+ validation via `qlctool --validate`.

**Spec:** `TODO.md` section "QLC+ feature audit (2026-08-27)" +
`docs/superpowers/plans/2026-08-27-qlc-audit-verification.md` (Codex
verification report with file:line evidence for every claim).

## Global Constraints

- One exported unit and one responsibility per file (`~/.claude/CLAUDE.md`).
- A malfunction is not fixed until a check rule sees the cause and a dated
  regression test puts the bug back and asserts the checker bites
  (repo `CLAUDE.md`).
- Check rules reason about capabilities and the function graph — never about
  a function's name.
- Strobe safety: nothing may flash above 4 Hz; audio triggers must never
  start a strobe (rules `estrobo demasiado rapido`, `estrobo enganchado`).
- Colour clocks: matrices started inside `Rueda Colores` steps must carry the
  step's wheel colour (rule `relojes de color`). New multi-colour matrices go
  to the librería page only, never into wheel steps.
- All code, comments, commits in English. Commit messages in the repo's
  existing lowercase-prefix narrative style (`console: …`, `rig: …`).
- Finish gate for every task that touches generation:
  `cd tools/qlctool && .venv/bin/python -m pytest tests/ -q` and
  `.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"`.
- Full regeneration (Task 9) rebuilds `Vibra.qxw`, `Vibra-beats.qxw`,
  `Vibra-split.qxw` and validates each with `--validate` (headless QLC+).

---

### Task 1: Verify the installed QLC+ 5.2.2 against the feature claims

The source clone is master/5.3.0-git; the show runs 5.2.2. Every QLC+5-only
feature this plan builds on must first be proven on the installed binary
(Codex report, section B14, lists the at-risk claims).

**Files:**
- Create: `docs/qlc5-verification.md` (findings table)
- Create: `tools/qlctool/tests/probes/` (tiny probe workspaces, one per claim)
- Read first: `tools/qlctool/qlctool/validate.py` (how the headless binary is
  launched and where it lives), `~/p/qlcplus/qmlui/virtualconsole/vcslider.cpp`
  (`loadXML` — the exact tags a v5 slider accepts from a v4-format file)

**Interfaces:**
- Produces: `docs/qlc5-verification.md` with one row per claim:
  claim | probe | result on 5.2.2. Tasks 3, 5, 8 consume its verdicts.

- [ ] **Step 1: List the claims to probe** (from the Codex report): palettes
  load in a 4.13-format file (B6); VC Slider accepts `SliderMode`
  GrandMaster/Submaster from v4 XML (B4); RGBMatrix `<Property>` script
  parameters and indexed `<Color Index="…">` load (A5/B1); `BlendMode`
  attribute on `<Function>` loads (B8); `ControlMode` Dimmer loads (B8);
  web interface flags `-w`/`-wp` and kiosk `-k` exist (B11/B12); `-p` operate
  flag exists at all (documented only for v4).
- [ ] **Step 2: Write one minimal probe workspace per XML claim** in
  `tools/qlctool/tests/probes/` — smallest valid 4.13-format `.qxw` (copy the
  header of `Vibra-split.qxw`, one fixture, one function/widget under test).
- [ ] **Step 3: Run each probe through the existing loader**:
  `.venv/bin/qlctool validate tests/probes/<probe>.qxw` (or the
  `validate_workspace` helper — read `validate.py` for the exact entry
  point). A clean load is the acceptance signal; a dropped widget or load
  warning is a fail.
- [ ] **Step 4: Probe the CLI flags**: run the installed binary with
  `--help`; record which of `-w -wp -wa -k -f -p -c` it advertises. Do not
  leave a `-w` instance running.
- [ ] **Step 5: Write `docs/qlc5-verification.md`** with the results table
  and the binary version string. Mark every claim CONFIRMED-ON-5.2.2 or
  NOT-ON-5.2.2; downstream tasks drop anything not confirmed.
- [ ] **Step 6: Commit** — `docs: what the installed QLC+ 5.2.2 really loads`

### Task 2: Blackout button in "SI ALGO VA MAL"

StopAll stops functions; Blackout forces outputs to zero. The console has
only StopAll (Codex A4). The `Blackout` action constant already exists unused
at `tools/qlctool/qlctool/vc/button.py:23`.

**Files:**
- Modify: `tools/qlctool/qlctool/generate/live_console.py` (the panic frame)
- Test: `tools/qlctool/tests/` (find the existing console-layout test module
  by grepping for "SI ALGO VA MAL"; add there)

**Interfaces:**
- Consumes: `build_button(...)` from `qlctool/vc/button.py` — read its
  signature first; it already accepts the action constant.
- Produces: a second button in the panic frame, caption `APAGON`, action
  `Blackout`, key binding `Escape` if free (check `rule_console` key-collision
  rule), no function ID.

- [ ] **Step 1: Write the failing test**: generate the console, assert the
  panic frame contains exactly one button whose `<Action>` text is
  `Blackout`, and that the StopAll button is still there.
- [ ] **Step 2: Run it, confirm it fails** (`pytest tests/<module> -q`).
- [ ] **Step 3: Add the button in `live_console.py`** beside StopAll, reusing
  the existing frame-building call shape.
- [ ] **Step 4: Test passes; `qlctool check` still clean** (key collisions,
  canvas extent).
- [ ] **Step 5: Commit** — `console: a second panic — blackout, not stop`

### Task 3: GrandMaster slider

The workspace declares a GrandMaster nobody can reach (Codex A3). Gated on
Task 1 confirming a v4-format slider with GrandMaster mode loads in 5.2.2.

**Files:**
- Create: `tools/qlctool/qlctool/vc/grand_master_slider.py` (one exported
  unit: `build_grand_master_slider`)
- Modify: `tools/qlctool/qlctool/generate/live_console.py` (page 1, beside
  the "Intensidad y strobo" frame), `qlctool/vc/widget_ids.py` if the widget
  tag needs registering
- Test: same console test module as Task 2

**Interfaces:**
- Consumes: the exact `<Slider>` XML shape from Task 1's probe (SliderMode,
  ValueDisplayStyle, geometry attributes) and the appearance helper
  `qlctool/vc/appearance.py`.
- Produces: `build_grand_master_slider(x, y, w, h, widget_id) -> Element`.

- [ ] **Step 1: Write the failing test**: generated console contains exactly
  one `<Slider>` with GrandMaster mode; console extent still ≤ 1440x900.
- [ ] **Step 2: Confirm it fails.**
- [ ] **Step 3: Implement the builder** mirroring the probe XML from Task 1;
  wire it into page 1 of `live_console.py`.
- [ ] **Step 4: Tests pass; `qlctool check` clean; validate the regenerated
  split workspace loads headless.**
- [ ] **Step 5: Commit** — `console: the grand master gets a handle`

### Task 4: Bind the bass band and add the empty-audio-widget rule

The AudioTriggers widget ships with all five bands unbound — dead UI by
configuration (Codex A1). Bind the bass band to the `Todo Blanco` Scene
(flash-safe: a Scene, no strobe, already the pre-2026-08-27 pairing);
leave the other four unbound. Thresholds stay an on-site item.

**Files:**
- Modify: `tools/qlctool/qlctool/generate/live_console.py:195-201`
  (`AUDIO_BANDS`)
- Create: `tools/qlctool/qlctool/checks/rule_audio_triggers.py` (rule:
  `disparador de audio vacio` — an AudioTriggers widget none of whose bars
  is bound to a channel, function, or widget does nothing; and no bound bar
  may start a function that reaches a shutter/strobe capability — reuse the
  capability walk from `rule_latched_strobe.py`)
- Test: `tools/qlctool/tests/test_check.py` (dated 2026-08-27, cites this
  audit), plus the generator test asserting the bass `<SpectrumBar>` exists
- Read first: `qlctool/vc/audio_triggers.py:44-54` (target shapes the
  builder accepts), `qlctool/checks/rule_latched_strobe.py` (capability
  walk to reuse), an existing rule file for the rule-registration pattern

**Interfaces:**
- Produces: check rule id `disparador de audio vacio` registered like the
  existing six rules in `qlctool/checks/`.

- [ ] **Step 1: Write the dated regression test** in `test_check.py`: take a
  generated show, strip all `<SpectrumBar>` children from the widget, assert
  the checker bites; second case: bind a bar to `Strobo Rapido`, assert the
  checker bites on the strobe path too.
- [ ] **Step 2: Confirm both fail** (rule doesn't exist yet).
- [ ] **Step 3: Implement `rule_audio_triggers.py`.**
- [ ] **Step 4: The rule now bites the *shipped* workspaces** (they are all
  inert) — that is the point. Fix the generator: set the bass entry of
  `AUDIO_BANDS` to the `Todo Blanco` scene.
- [ ] **Step 5: Full check over all three regenerated workspaces is clean;
  the dated tests pass.**
- [ ] **Step 6: Commit** — `show: the bass gets a hand back, and an empty ear
  is now a finding`
- [ ] **Step 7: Update `TODO.md`**: audit item → `[x]` (move evidence to
  `~/p/TODO_LOG.md`); the on-site thresholds item loses its "stale" note.

### Task 5: Widen the matrix repertoire — scripts, parameters, colours

4 of 39 RGB scripts used, zero script parameters, mono-colour only (Codex
A5/B1). The builder already supports `properties` and indexed colours
(`functions/rgbmatrix.py:29-30, 64-75, 80-83`).

**Files:**
- Modify: `tools/qlctool/qlctool/matrix_algorithms.py` (curated additions),
  `tools/qlctool/qlctool/generate/matrix_effects.py` (parameter + colour
  emission), `tools/qlctool/qlctool/matrix_step_count.py` (step counts for
  the new scripts), `tools/qlctool/qlctool/generate/live_console.py`
  (librería page grows)
- Test: the existing matrix generation test module + `test_check.py`
- Read first: each candidate `.js` in `~/p/qlcplus/resources/rgbscripts/`
  — its `rgbMapStepCount` and declared properties are the ground truth for
  step counts and parameter names; `matrix_step_count.py` for how pass
  length feeds duration.

**Interfaces:**
- Consumes: `build_rgb_matrix(...)` in `functions/rgbmatrix.py` — the
  `properties` dict and `color_format` indexed mode it already accepts.
- Produces: an extended algorithm table; each entry carries script name,
  step-count formula (or fixed duration for non-terminating scripts like
  plasma/noise), chosen property values, and colour count.

- [ ] **Step 1: Curate per grid** (read the scripts first): BarrasLed 8x2 —
  `sinewave`, `lines` (Horizontal), `marquee`, `plasma` (Rainbow preset);
  Cabezas 12x1 — `onebyone`, `fillunfill`, `noise`; PAR 15x1 — `circular`
  (Radar), `starfield`, `gradient`. Drop any whose 1-row rendering reads
  poorly in the 3D preview at Step 6.
- [ ] **Step 2: Write the failing tests**: generated split workspace contains
  matrices for each new script with the curated `<Property>` values; the
  two-colour entries carry `<Color Index="0">` and `<Color Index="1">`;
  every new matrix's duration matches its declared step count formula;
  wheel-step Collections still reference only single-wheel-colour matrices
  (rule `relojes de color` untouched).
- [ ] **Step 3: Confirm they fail.**
- [ ] **Step 4: Extend `matrix_algorithms.py` + `matrix_step_count.py` +
  `matrix_effects.py`; wire the new matrices into the librería page and the
  per-group `Ciclo Matrices` chasers only — not into `Rueda Colores` steps.**
- [ ] **Step 5: Tests pass; `qlctool check` clean; regenerate split and eyeball
  the new patterns in the QLC+ 3D preview** (matrices paint RGB — they render
  off-site).
- [ ] **Step 6: Cut anything that reads badly; re-run tests.**
- [ ] **Step 7: Commit** — `rig: the matrix library learns nine new tricks`

### Task 6: EFX variety — rotation and serial cascades

23 EFX, all Rotation=0, all Parallel, identical axes (Codex A6). Serial
propagation delays each fixture by `loopDuration/(n+1)*serial` — a cascade
down the 12-head row for free (Codex B2).

**Files:**
- Modify: `tools/qlctool/qlctool/generate/movement_efx.py`,
  `tools/qlctool/qlctool/functions/efx.py` (only if `build_efx` lacks
  rotation/propagation parameters — read it first),
  `tools/qlctool/qlctool/efx_algorithms.py`
- Test: the movement test module + `test_check.py`

**Interfaces:**
- Consumes: `build_efx`, `EFXFixture`, `EFXAxis` from `functions/efx.py`.
- Produces: one new figure per family — washes: `Ola Suave` (Line, Serial
  propagation, slow); beams: `Cascada Beams` (Circle, Serial, Rotation 45) —
  plus Rotation on two existing beam figures (90 on `Diamond`, 45 on `Leaf`)
  so the shapes stop being axis-aligned clones.

- [ ] **Step 1: Write the failing tests**: the new EFX exist with
  `PropagationMode` Serial; rotations are set; the mirrored house-right
  direction logic still holds (existing test must keep passing); rule
  `familias de movimiento mezcladas` still passes (one family per EFX).
- [ ] **Step 2: Confirm they fail.**
- [ ] **Step 3: Implement; keep 16-bit/8-bit split logic intact**
  (`movement_efx.py:84-86`, `efx_16bit.py`).
- [ ] **Step 4: Tests pass; check clean; watch the cascade in the 3D
  preview.**
- [ ] **Step 5: Commit** — `rig: movement stops marching in lockstep`

### Task 7: Peak's intensity becomes visible — the Dimmer Chase owns it

`Dimmer Chase` (the only Mode=1 EFX) is HTP-shadowed by `Intensidad Total`
at 255 in Peak — cosmetic today, pointless forever (deferred item in
`TODO.md`). Fix: in Peak, the chase is the sole intensity owner.

**Files:**
- Modify: `tools/qlctool/qlctool/generate/canonical_show.py` (the Peak
  level's Collection)
- Test: `test_check.py` (dated) + the level-composition test module
- Read first: how `rule_shadowed_intensity` and `rule` "acento sin dueño"
  walk the graph — the fix must satisfy both, not dodge them.

**Interfaces:**
- Consumes: the Peak Collection builder in `canonical_show.py` and the
  existing `Dimmer Chase` EFX (23 fixtures, Mode Dimmer, offsets 0-344).
- Produces: Peak Collection = colour bed + movement + `Dimmer Chase`, with
  `Intensidad Total` removed from Peak only (Fiesta/moments keep theirs);
  fixtures the chase cannot dim (MiN Wash — no dimmer channel) keep a
  static intensity owner so no fixture goes dark.

- [ ] **Step 1: Write the dated regression test**: put `Intensidad Total`
  back beside the chase in a generated Peak and assert `intensidad tapada`
  (or a sharpened variant) bites; assert the new Peak passes.
- [ ] **Step 2: Confirm the desired-state assertion fails today.**
- [ ] **Step 3: Rework Peak's Collection; special-case the no-dimmer
  fixtures via the capability walk, not by name.**
- [ ] **Step 4: Tests + check + validate pass.**
- [ ] **Step 5: Commit** — `show: peak breathes — the chase owns the light`

### Task 8: Operations runbook — kiosk start and the phone console

Gated on Task 1's flag verification. No generator change.

**Files:**
- Modify: the operations doc in `docs/` (grep `docs/` for the operate-mode
  page; extend it)

- [ ] **Step 1: Write the show-Mac launch line** (exact flags Task 1
  confirmed, e.g. `qlcplus -k -f -o "QLC+ Setups/Vibra-split.qxw"`), the
  no-on-screen-exit caveat (Cmd+Q still works), and the web-console recipe:
  `-w`, phone browser → `http://<mac-ip>:9999`, what works from the phone
  (buttons, frames, speed dials) for the on-site verification items.
- [ ] **Step 2: Commit** — `docs: how the show starts itself and fits in a
  pocket`

### Task 9: Regenerate, validate, close the loop

- [ ] **Step 1: Regenerate all three workspaces** with `qlctool newshow`
  (read its CLI in `tools/qlctool` for the exact invocations the repo uses).
- [ ] **Step 2: Validate each**: `--validate` (headless QLC+ load) on
  `Vibra.qxw`, `Vibra-beats.qxw`, `Vibra-split.qxw`.
- [ ] **Step 3: Full gate**: `.venv/bin/python -m pytest tests/ -q` and
  `.venv/bin/qlctool check "../../QLC+ Setups/Vibra-split.qxw"`.
- [ ] **Step 4: Update `TODO.md`**: audit items done → `[x]` with evidence →
  entries moved to `~/p/TODO_LOG.md`; on-site-gated items stay, each naming
  its smallest unblocking action.
- [ ] **Step 5: Commit** — `show: the audit lands — regenerated, checked,
  validated`

---

## Gated — deliberately NOT in this plan

Each is blocked on something outside the repo; the TODO carries them:

- **MIDI controller bindings** — blocked on the owner choosing/buying the
  controller (APC mini class). Then: input profile + `<Input>` emission +
  LED feedback.
- **Position palettes with fanning for `Beams Abanico`** — Task 1 must
  confirm palettes on 5.2.2 first, and aiming needs the rig.
- **XY Pad presets / floor control** — needs calibrated positions from the
  rig session.
- **Beat-locked matrices** — `Vibra-beats.qxw` already carries the beat
  experiment; needs the venue PA to judge BPM tracking.
- **VC Clock scheduler (auto-start AUTO)** — needs the venue's opening time
  from the owner; trivial once known.
- **Adjust-mode sliders (live EFX size / matrix parameter tweaking)** —
  which parameters deserve console space is an operator call; decide after
  the Task 5/6 repertoire has been seen on the rig.
- **Audio-trigger thresholds** — on-site by definition (Task 4 only ships
  the safe binding).
