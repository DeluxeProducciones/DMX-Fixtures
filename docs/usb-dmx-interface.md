# The USB-DMX interface: why it flashes, and what replaces it

2026-08-29. The owner: the interface sometimes fires a "flash", as if it sent
255 to every channel at once.

## The cause

The show's output is a generic FT232R USB-DMX dongle (an "Open DMX" clone —
serials `A50285BI` and `AB0PEY7F` have both been seen; the workspaces carry
`UID="None"` so either one works). That design has **no microcontroller and no
frame buffer**: the PC generates every DMX frame in software and pushes it out
over USB in real time. When USB hiccups for an instant — another device on the
bus, a CPU spike, a hub — the frame's break/mark-after-break timing comes out
wrong and the receivers latch shifted or garbage data. Garbage read as high
values is a full-on white flash. It is an architectural defect of every
FT232R clone, not of the workspace or of qlctool: no file change can fix it.

Contrast: an Enttec DMX USB Pro (and anything built like it) keeps the
universe in its own RAM and emits frames from its own microcontroller. A USB
hiccup delays *new values* by a frame; it can never corrupt the frame on the
wire.

## Mitigations with the current dongle (checklist for a gig)

None of these eliminate the flashes; together they make them rare.

1. Dongle in a USB port **directly on the machine** — no hub, and nothing
   noisy (audio interfaces, phones charging) sharing the bus.
2. Nothing heavy running beside QLC+ on the show Mac; flashes that coincide
   with CPU spikes confirm this diagnosis.
3. **120 Ω terminator** on the last fixture of the line (male XLR with a
   120 Ω resistor across pins 2-3). Missing termination causes reflections
   with similar symptoms — still unconfirmed on this rig.
4. Real DMX cable (110 Ω), not microphone XLR, at least for the long runs.
5. Check the plugin mode and frequency (30 seconds, see below): mode
   **Open TX**, output frequency **30**.

## The plugin mode: Open TX is the right one

QLC+'s DMX USB plugin drives nine device modes (read from the plugin source,
`plugins/dmxusb/src/`): Pro RX/TX, Open TX, Open RX, Pro Mk2, Ultra Pro,
DMX4ALL, Vince TX, Eurolite, usbdmx.com legacy. Unless a mode was forced, it
picks by the USB product name — "DMX USB PRO", "PRO MK2" and friends go to
the Pro modes, and a generic FTDI with no recognised name falls through to
`EnttecDMXUSBOpen` = **Open TX**. That is where this clone lands, and it is
the only mode that can work: every other mode wraps the universe in a
protocol that expects firmware on the other end, which this dongle does not
have (Pro mode's `0x7E … 0xE7` frames would go out raw on the DMX line —
constant garbage, not an occasional flash). "Works fine, flashes now and
then" is precisely Open TX behaving as designed. A forced mode is stored per
serial number in QSettings (`qlcftdi/typemap`), not in the workspace, so the
`.qxw` files cannot carry or fix it.

To verify on the show Mac: Input/Output panel → gear icon on the output
plugin → a dialog with Name / Serial / Mode / Output frequency per widget.
Expect mode Open TX and frequency 30 — the Open mode's default (the source
comments it with a literal `// crap`); raising it widens the corruption
window, so if someone turned it up for smoothness, turn it back down.

One nuance: some cheap clones *do* carry a microcontroller and enumerate as
"USB DMX512 Pro" — on those, the Eurolite mode is the fix for flashing. This
one enumerates as a bare FT232R (that is why QLC+ treats it as Open), so the
nuance does not apply; it is only worth remembering if a different dongle
ever lands in the booth.

## The replacement: build one (researched 2026-08-29)

Three viable paths, all verified against their upstream repos. The parts are
the same for A and B: Raspberry Pi Pico (~5 €), MAX485 module (~1-2 €; a
MAX3485 is 3.3 V-native), chassis-mount female 3-pin XLR (~2 €), a box, a USB
cable. Optional upgrade: an isolated transceiver module (ADM2582E, ~10 €) —
the cheap dongle has no isolation either, so plain MAX485 is already parity.

### A. Pico + rp2040-dmxsun (no code)

[OpenLightingProject/rp2040-dmxsun](https://github.com/OpenLightingProject/rp2040-dmxsun)
— Apache-2.0, active, prebuilt UF2 (drag-and-drop flash). The Pico enumerates
as a **USB network card** (CDC NCM, DHCP built in); the host sends **Art-Net
or sACN** to it. QLC+ compatibility is stated in its README. Scales to 16
universes with its stack of boards; one universe needs only the Pico plus an
RS-485 driver wired per the schematics in the repo.

### B. Pico + our own firmware: Enttec Pro emulation (preferred)

Two libraries compose:

- [jostlowe/Pico-DMX](https://github.com/jostlowe/Pico-DMX) — DMX output on
  the RP2040's PIO + DMA; break timing is done in hardware, immune to USB and
  CPU load. In the Arduino library manager.
- [DaAwesomeP/dmxusb](https://github.com/DaAwesomeP/dmxusb) — implements the
  **ENTTEC DMX USB Pro Widget API 1.44** over any serial port (Apache-2.0).

The glue is ~100 lines on the earlephilhower Arduino-Pico core: dmxusb parses
the `0x7E … 0xE7` frames arriving over USB CDC, its callback copies the
universe into the Pico-DMX PIO output loop. QLC+ then detects the dongle as a
DMX USB Pro — plug and play, no network configuration in the booth.

Wiring (one universe):

| From | To |
|---|---|
| Pico GP0 | MAX485 DI |
| 3.3 V | MAX485 DE and R̄Ē (tied high — always transmit) |
| Pico VBUS (pin 40, 5 V) | MAX485 VCC |
| Pico GND | MAX485 GND, XLR pin 1 |
| MAX485 A | XLR pin 3 (Data+) |
| MAX485 B | XLR pin 2 (Data−) |

The MAX485 runs at 5 V; its TTL input threshold (2.0 V) accepts the Pico's
3.3 V logic directly.

### C. The Raspberry Pi 3/4 already in the house: Art-Net node (cheapest test)

QLC+ on the show Mac sends Art-Net over Ethernet; the Pi runs **OLA** with the
`uartdmx` plugin and outputs DMX on its hardware UART through the same MAX485
(GPIO14 / header pin 8 → DI; 5 V pin 2 → VCC; GND pin 6). Known recipe:
[QLC+ forum](https://www.qlcplus.org/forum/viewtopic.php?t=11616),
[Raspberry Pi forum](https://forums.raspberrypi.com/viewtopic.php?t=233159).
Pi 3/4 traps: disable the serial console, and disable Bluetooth
(`dtoverlay=disable-bt`) so the UART is the full PL011 — the mini-UART's
baud rate wanders and cannot hold DMX. Downside for gigs: a second machine
and an Ethernet cable in the booth. Upside: only the ~2 € MAX485 is missing,
so it doubles as the cheap way to *prove* the flashes are the dongle's fault
before building B.

Also looked at: [vanvught/rpidmx512](https://github.com/vanvught/rpidmx512)
(bare-metal Art-Net node with Enttec Pro emulation) — targets Orange Pi and
GD32 boards, not the Pi 3/4 in hand; discarded.

### The plan

1. Gig-day mitigations above, tonight.
2. Path C with the existing Pi as soon as a MAX485 arrives — if the flashes
   vanish behind the Pi, the diagnosis is proven.
3. Build B as the permanent booth interface; A is the fallback if the custom
   firmware fights back.
