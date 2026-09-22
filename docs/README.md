# Documentation

What was learned about this show, its rig and the QLC+ file format while
building `tools/qlctool`. Written down so none of it has to be re-derived.

| Document | What is in it |
| --- | --- |
| [qxw-format.md](qxw-format.md) | The `.qxw` workspace format, reverse-engineered and confirmed against the real shows: every function type's XML, the traps, and what changed between QLC+ versions |
| [rig.md](rig.md) | The 29 patched fixtures, the groups, which ones move, and how far each fixture definition has been verified |
| [show-operation.md](show-operation.md) | How these shows are actually run - unattended - and the console and keyboard that follows from that |
| [qlcplus-environment.md](qlcplus-environment.md) | Where QLC+ keeps fixture definitions, how to validate a workspace headless, and which QLC+ versions are in play |
| [toolkit.md](toolkit.md) | What `qlctool` does, command by command, and the two safety nets it rests on |
| [checks.md](checks.md) | The `qlctool check` rules: what each one catches and the night it came from |
| [panel-effects.md](panel-effects.md) | The WX panels' 42 built-in programmes, catalogued from the owner's videos of each one |
| [qlc5-verification.md](qlc5-verification.md) | Which QLC+ 5 features the installed binary really supports, verified against the source clone |
| [old-vs-new-audit-2026-08-28.md](old-vs-new-audit-2026-08-28.md) | The hand-built show audited against the generated one: what the old one still did better |
| [smc-pad-led.md](smc-pad-led.md) | Lighting the SMC-PAD's pads from the show: why MIDI cannot, the BLE GATT protocol the app uses, and what a bridge would do |
| [usb-dmx-interface.md](usb-dmx-interface.md) | Why the FT232R dongle randomly flashes the rig, the gig-day mitigations, and the researched DIY replacement (Pico or Raspberry Pi) |

This repository is **public**. Machine access - addresses, accounts,
credentials, SSH - is deliberately not written here; it lives in the owner's
private notes.
