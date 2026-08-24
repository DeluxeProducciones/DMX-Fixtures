# Documentation

What was learned about this show, its rig and the QLC+ file format while
building `tools/qlctool`. Written down so none of it has to be re-derived.

| Document | What is in it |
| --- | --- |
| [qxw-format.md](qxw-format.md) | The `.qxw` workspace format, reverse-engineered and confirmed against the real shows: every function type's XML, the traps, and what changed between QLC+ versions |
| [rig.md](rig.md) | The 27 patched fixtures, the groups, which ones move, and how far each fixture definition has been verified |
| [show-operation.md](show-operation.md) | How these shows are actually run - unattended - and the console and keyboard that follows from that |
| [qlcplus-environment.md](qlcplus-environment.md) | Where QLC+ keeps fixture definitions, how to validate a workspace headless, and which QLC+ versions are in play |
| [toolkit.md](toolkit.md) | What `qlctool` does, command by command, and the two safety nets it rests on |

This repository is **public**. Machine access - addresses, accounts,
credentials, SSH - is deliberately not written here; it lives in the owner's
private notes.
