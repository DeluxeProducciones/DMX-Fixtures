# QLC+ feature-gap findings — verification report

## A1

**CONFIRMED**

- `DMX-Fixtures/QLC+ Setups/Vibra-split.qxw:12993-13002` declares `BarsNumber="5"` but contains no `<SpectrumBar>`.
- The same is true of `Vibra.qxw:12471-12480` and `Vibra-beats.qxw:12485-12494`.
- The generator supports bindings: `tools/qlctool/qlctool/vc/audio_triggers.py:44-54` emits `<SpectrumBar>` for every non-`None` target.
- The current omission is deliberate: `generate/live_console.py:195-201` defines all five `AUDIO_BANDS` targets as `None`; lines `305-313` pass them to the builder. Thus the shipped widget is inert by configuration.

## A2

**NUANCE**

- `Vibra-split.qxw:368-430` defines groups 0–3, including `PixelesLed` as group 3, size 4×1.
- XPath counts are exactly group 0 = 41, group 1 = 30, group 2 = 30, group 3 = 0 RGBMatrix functions.
- `TODO.md:45-46` says “30 matrices más para el grupo nuevo”; that statement is materially wrong for the shipped workspace.
- The omission is deliberate, not an accidental failure in `matrix_effects.py`: `generate/canonical_show.py:197-217` says self-animating groups ignore matrix RGB and skips them; `_all_self_animating()` at lines `598-604` implements that test.
- `matrix_effects.py:44-49` itself can generate matrices for any valid group. Therefore the counts are true, the TODO claim is false, and the omission reflects a generator policy.

## A3

**CONFIRMED**

- `Vibra-split.qxw:13005-13008` declares `<GrandMaster ChannelMode="Intensity" ValueMode="Reduce" .../>`.
- The Virtual Console contains zero `<Slider>` widgets, hence zero GrandMaster-mode sliders. No other VC widget references or controls the GrandMaster.

## A4

**CONFIRMED**

- The sole StopAll control is `Vibra-split.qxw:7247-7259`, with `<Action FadeOut="1000">StopAll</Action>`.
- Targeted XML counts: StopAll buttons = 1; Blackout-action buttons = 0.
- The adjacent caption saying it leaves the room dark (`:7261`) does not turn it into the distinct QLC+ Blackout action.

## A5

**CONFIRMED**

- The workspace has exactly 101 RGBMatrix functions, spanning `Vibra-split.qxw:2983-3978`.
- XPath counts: `<Property>` = 0, `<MonoColor>` = 101, `<EndColor>` = 0, indexed `<Color>` = 0.
- `functions/rgbmatrix.py:29-30` accepts `properties` and `color_format`.
- `functions/rgbmatrix.py:64-75` supports indexed `<Color Index="…">`, legacy `<MonoColor>`, and optional `<EndColor>`.
- `functions/rgbmatrix.py:80-83` emits supplied script properties.

## A6

**CONFIRMED**

- Exactly 23 EFX functions exist, from `Vibra-split.qxw:3982` through `:5985`.
- All 23 match Rotation 0, Parallel propagation, X=(127,2,90), and Y=(127,3,0).
- A representative instance appears at `Vibra-split.qxw:4039-4057`.

## B1

**CONFIRMED**

- `qlcplus/resources/rgbscripts/` contains exactly 39 `.js` files.
- The named scripts all exist. Examples of tunable declarations include:
  - `plasma.js:31-50`
  - `fireworks.js:61-71`
  - `circular.js:31-48`
  - `lines.js:32-48`
  - `sinewave.js:32-38`
  - `marquee.js:29-40`
  - `noise.js:30-35`
  - `starfield.js:30-36`
  - `gradient.js:31-37`
- The show’s scripted matrices use only Fill, Even/Odd, Strobe, and Waves: 21/21/18/21 occurrences respectively. The remaining 20 of 101 matrices are plain/solid.

## B2

**CONFIRMED**

- `qlcplus/engine/src/efx.h:541-546` defines Parallel, Serial, and Asymmetric.
- `efxfixture.cpp:380-386` calculates the Serial/Asymmetric delay as `loopDuration() / (fixtures().size() + 1) * serialNumber()`.
- `efx.cpp:57-62` registers Rotation as a live attribute ranging 0–359.
- `efx.cpp:531-535` applies the adjusted Rotation value and updates the rotation cache.

## B3

**CONFIRMED**

- Chaser serializes and loads the common Tempo type at `chaser.cpp:343-346` and `:426-428`; `chaserrunner.cpp:789-797` advances Beats-tempo steps on beats.
- RGBMatrix serializes/loads Tempo at `rgbmatrix.cpp:515-517` and `:581-585`.
- Beat resynchronization is exactly described at `rgbmatrix.cpp:756-765`; lines `771-787` defer a step when the next beat is within `stepBeatDuration / 16`.
- `inputoutputmap.h:589-595` defines Disabled, Internal, Plugin, and Audio beat sources.
- Audio constructs a `BeatTracker` at `engine/audio/src/audiocapture.cpp:77`.
- `beattracker.h:83-94` documents autocorrelation over a 50–240 BPM grid; `beattracker.cpp:258-259` constructs that grid.

## B4

**CONFIRMED**

- `qmlui/virtualconsole/vcslider.h:167-171` defines Level, Adjust, Submaster, and GrandMaster modes.
- Adjust mode resolves a function and calls its registered attribute adjustment at `vcslider.cpp:1421-1460`.
- RGBMatrix registers Color 1–5 and Pattern at `rgbmatrix.cpp:88-97`.
- Every script property is dynamically registered as an attribute at `rgbmatrix.cpp:1121-1147`.

## B5

**NUANCE**

- `chaser.h:217-223` confirms `FromFunction`, `Blended`, `Crossfade`, and `BlendedCrossfade`.
- Incoming scenes can start from an outgoing scene’s values: `chaserrunner.cpp:517-536` installs the previous scene as the blend source, and `scene.cpp:749-768` copies matching outgoing values into the incoming fader.
- However, attributing that behavior specifically to `Blended` is imprecise. `chaserrunner.cpp:540-557` shows `Blended` retaining normal step fade times while Crossfade variants set them to zero; the blend-source setup occurs separately from that switch.

## B6

**CONFIRMED**

- Palette fanning types Flat/Linear/Sine/Square/Saw are defined at `qlcpalette.h:171-177`; X/Y/Z layouts are at `:183-193`.
- Palettes serialize as `<Palette>`: `qlcpalette.h:37`; `qlcpalette.cpp:1082-1095`.
- `Doc::loadXML()` recognizes `<Palette>` directly under `<Engine>` at `doc.cpp:1270-1288`, without checking the workspace Creator version.
- Therefore palettes can serialize/load in the show’s QLC+ 4-format workspace (`Vibra-split.qxw:3-7` reports 4.13.1).
- A VC Button exposes only a Function ID (`vcbutton.h:33-38`) and serializes `<Function ID="…">` at `vcbutton.cpp:690-708`; it cannot reference a palette directly.

## B7

**CONFIRMED**

- `vcxypadpreset.h:53-59` defines Position, EFX, Scene, and FixtureGroup preset types.
- `vcxypad.h:127-138` documents floor control: X/Z stage coordinates plus Y target height.
- `vcxypad.cpp:1976-1987` implements floor-mode targeting for the fixtures selected by the pad/preset.

## B8

**CONFIRMED**

- `rgbmatrix.h:348-355` includes Dimmer and Shutter control modes.
- Shutter and Dimmer rendering are implemented at `rgbmatrix.cpp:930-948`.
- Function blend modes Normal/Mask/Additive/Subtractive are defined at `universe.h:507-511`.
- Non-normal blend mode persists as the `<Function BlendMode="…">` attribute at `function.cpp:329-341` and loads at `:908-919`.
- RGBMatrix passes that mode to its fader at `rgbmatrix.cpp:855-863`, which ultimately uses blended universe writes.

## B9

**CONFIRMED**

- `vcclock.h:29-37` defines each schedule entry’s function ID, start time, stop time, and weekday flags.
- Schedule mode is exposed at `vcclock.h:111-119`.
- Optional stop-time serialization is implemented at `vcclock.cpp:724-757`.
- Runtime weekday/start/stop handling appears at `vcclock.cpp:362-428`.

## B10

**CONFIRMED**

- `scriptrunner.h:45-70` marks the following public slots as JavaScript-exported methods.
- The requested API is present:
  - `setFixture`: `:82-90`
  - `startFunction` / `stopFunction`: `:100-114`
  - indexed/named `setFunctionAttribute`: `:133-151`
  - `systemCommand`: `:153-159`
  - `waitTime`, `waitFunctionStart/Stop`, `setBlackout`, `setBPM`, `random`: `:162-225`
- `scriptrunner.cpp:96-104` exposes the runner to JavaScript as the global `Engine` object.

## B11

**CONFIRMED**

- qmlui links WebSockets and `qlcpluswebaccess` at `qmlui/CMakeLists.txt:212-223`.
- `webaccess-qml.h:28-39` declares Button, Slider, XYPad, Frame, CueList, AudioTriggers, Clock, SpeedDial, and Animation support.
- HTTP and WebSocket handlers are declared at `webaccess-qml.h:61-64`.
- Type-specific remote handling is implemented across `webaccess-qml.cpp:795-1005`.
- CLI options `-w`, `-wp`, and `-wa` are defined at `qmlui/main.cpp:110-121`.

## B12

**CONFIRMED**

- `qmlui/main.cpp:85-87` defines `-k`/`--kiosk`; lines `206-208` enable it.
- `app.cpp:678-682` restricts access to VC control.
- `app.cpp:684-688` shows `createKioskCloseButton()` is only `Q_UNUSED(rect)` plus `// TODO`.
- `qml/MainView.qml:145-149` hides the toolbar in kiosk mode, so its Actions/Exit UI is unavailable. Window-manager or operating-system closure remains possible, but there is no kiosk on-screen exit control.

## B13

**CONFIRMED**

- `virtualconsole.h:273-284` provides external-controller source creation and auto-detection.
- Keyboard auto-detection is explicit at `virtualconsole.h:348-358`.
- MIDI-specific feedback-channel support appears at `vcwidget.cpp:754-779`; source feedback values and plugin-specific extra parameters, including OSC-path-style metadata, are handled at `vcwidget.cpp:810-870` and `:906-933`.
- Workspace XPath counts: 374 VC Buttons, zero VC `<Input>` bindings, and 64 Buttons with a non-empty `<Key>`.
- Representative key bindings begin at `Vibra-split.qxw:7000-7003`.

## B14

**NUANCE**

- `qlcplus/variables.cmake:47-59` identifies qmlui as version `5.3.0` and appends `GIT` for development builds.
- The clone is a shallow, single-commit checkout at 2026-08-22, so it contains no local 5.2.2 tag/history with which to establish introduction dates.
- Consequently, B1–B13 are confirmed only against 5.3.0-GIT source, not against the installed 5.2.2 binary.
- The strongest installed-version verification risks are:
  - B3: the current autocorrelation `BeatTracker`.
  - B4: dynamic RGBMatrix live attributes.
  - B6: palettes/fanning.
  - B7: XYPad presets and floor aiming—the checkout’s sole commit is itself an XYPad EFX-control change.
  - B8: RGBMatrix control/blend modes.
  - B10: named function-attribute scripting.
  - B11: the qmlui web-access implementation.
  - B13: enhanced source-specific feedback handling.
- B1 also depends on the resource package installed on the show machine, even though current source contains 39 scripts. Direct 5.2.2 binary/resource verification remains required for every operational deployment claim.

## Material corrections

- A2’s TODO statement that `PixelesLed` received “30 matrices más” is false for the shipped workspace; the generator deliberately excludes that self-animating group.
- B5 overattributes outgoing-value blending to the `Blended` enum. The blend-source mechanism is separate from the fade-control switch.
- Current-source confirmation does not prove 5.2.2 availability. The shallow clone prevents a reliable source-history comparison.

## Verification command

The following read-only verification command was run successfully and returned `verification-pass`:

```sh
set -e
workspace="DMX-Fixtures/QLC+ Setups/Vibra-split.qxw"
xmllint --noout "$workspace" \
  "DMX-Fixtures/QLC+ Setups/Vibra.qxw" \
  "DMX-Fixtures/QLC+ Setups/Vibra-beats.qxw"
test "$(xmllint --xpath 'count(//*[local-name()="Function"][@Type="RGBMatrix"])' "$workspace")" = 101
test "$(xmllint --xpath 'count(//*[local-name()="Function"][@Type="EFX"])' "$workspace")" = 23
test "$(find qlcplus/resources/rgbscripts -maxdepth 1 -type f -name '*.js' | wc -l | tr -d ' ')" = 39
rg -q 'enum SliderMode \{ Level, Adjust, Submaster, GrandMaster \}' qlcplus/qmlui/virtualconsole/vcslider.h
rg -q 'Serial.*Pattern propagates' qlcplus/engine/src/efx.h
rg -q 'QCommandLineOption webAccessOption' qlcplus/qmlui/main.cpp
rg -q 'Q_UNUSED\(rect\)' qlcplus/qmlui/app.cpp
```

| ID | Verdict |
|---|---|
| A1 | CONFIRMED |
| A2 | NUANCE |
| A3 | CONFIRMED |
| A4 | CONFIRMED |
| A5 | CONFIRMED |
| A6 | CONFIRMED |
| B1 | CONFIRMED |
| B2 | CONFIRMED |
| B3 | CONFIRMED |
| B4 | CONFIRMED |
| B5 | NUANCE |
| B6 | CONFIRMED |
| B7 | CONFIRMED |
| B8 | CONFIRMED |
| B9 | CONFIRMED |
| B10 | CONFIRMED |
| B11 | CONFIRMED |
| B12 | CONFIRMED |
| B13 | CONFIRMED |
| B14 | NUANCE |