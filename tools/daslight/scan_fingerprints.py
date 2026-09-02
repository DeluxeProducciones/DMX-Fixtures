"""Fingerprint the decrypted Daslight library (library.jsonl) for the Vibra rig.

Match by channel order, never by name: the same AliExpress head is sold under a
dozen names. A: the 230 W 7R beam (16 channels, pan, tilt, fine, fine, speed,
strobe, dimmer, ...). B: the Mini Led Moving Head (pan, tilt, dimmer, RGBW,
strobe, then eight more). D: an 8-channel panel (dimmer, RGB, strobe, ...).
E: a 5-channel PAR (RGB, dimmer, strobe). N: names worth a look.

    python3 scan_fingerprints.py library.jsonl
"""
import json, re, sys
from collections import Counter
# Nicolaudie channel type ids seen so far: 1 pan, 2 tilt, 7 dimmer, 14 zoom, 15 shutter/strobe,
# 18 speed, 25 red, 26 green, 27 blue, 31 white, 37 macro/effect, 0 other
def kind(ch):
    t = ch["type"]; n = ch["name"].lower()
    if "µ" in ch["name"] or "micro" in n or "fine" in n:
        return "panf" if "pan" in n else ("tiltf" if "tilt" in n else "fine")
    return {"1": "pan", "2": "tilt", "7": "dim", "14": "zoom", "15": "strobe", "18": "speed",
            "25": "r", "26": "g", "27": "b", "31": "w", "37": "macro"}.get(t, "t" + t)
A = ["pan", "tilt", "panf", "tiltf", "speed", "strobe", "dim"]
B = ["pan", "tilt", "dim", "r", "g", "b", "w", "strobe"]
hits = {"A": [], "B": [], "D": [], "E": [], "N": []}
names = re.compile(r"vortex|hyu|wx-?60|48 ?part|pc-?64|oukaning|junman|mac ?mah|1915", re.I)
n = 0
for line in open(sys.argv[1]):
    d = json.loads(line); n += 1
    label = f'{d["brand"]} | {d["name"]} | {d["file"]}'
    if names.search(d["brand"] + " " + d["name"] + " " + d["file"]):
        hits["N"].append((label, [(m["n"], [c["name"] for c in m["channels"]][:10]) for m in d["modes"]]))
    for m in d["modes"]:
        ks = [kind(c) for c in m["channels"]]
        if m["n"] == 16 and ks[:7] == A:
            hits["A"].append((label, [c["name"] for c in m["channels"]]))
        if m["n"] == 16 and ks[:8] == B:
            hits["B"].append((label, [c["name"] for c in m["channels"]][8:]))
        if m["n"] == 8 and ks[:5] == ["dim", "r", "g", "b", "strobe"]:
            hits["D"].append((label, [c["name"] for c in m["channels"]][5:]))
        if m["n"] == 5 and ks == ["r", "g", "b", "dim", "strobe"]:
            hits["E"].append((label, []))
print("profiles:", n)
for k in ("N", "A", "B", "D", "E"):
    print(f"\n## {k}: {len(hits[k])}")
    for label, rest in hits[k][:30]:
        print(" -", label, "|", rest)
