"""Print the channel table of Lightkey fixture profiles.

Lightkey (`brew install --cask lightkey`) ships 7,704 fixture profiles as
NSKeyedArchiver binary plists under
`/Applications/Lightkey.app/Contents/Resources/Fixture Profiles/`. A profile is
somebody's reading of the manufacturer's DMX chart, typed - pan, tilt, colour
component, shutter/strobe, zoom, gobo, prism, command - so a fixture nobody has
a manual for can be found by fingerprinting the channel *order* across the
whole library. That is how the MAC WASH 1915Z's twin (Algam MW19x15Z) and the
Mini Led Moving Head's OEM (Big Dipper LM108) were found on 2026-09-02.

Usage:

    python3 tools/lightkey/decode_profile.py "Algam Lighting - MW19x15Z.lightkeyfxt"

Ranges print as `start..end`; a negative end is 256 + end (Lightkey stores
NSRange-like pairs), and `0..-1` is the whole channel. A zoom with no
`transformation` parameter is Lightkey's default direction, not a
measurement: it read 0 = narrow on 45 of the 54 fixtures QLC+ also describes,
and got the MW19x15Z backwards.
"""
import plistlib, sys, json
from pathlib import Path

P = Path("/Applications/Lightkey.app/Contents/Resources/Fixture Profiles")

def unarchive(path):
    d = plistlib.load(open(path, "rb"))
    objs = d["$objects"]
    def res(o):
        if isinstance(o, plistlib.UID):
            return res(objs[o.data])
        if isinstance(o, dict):
            if "$classname" in o:
                return o["$classname"]
            if "NS.objects" in o and "NS.keys" in o:
                return {res(k): res(v) for k, v in zip(o["NS.keys"], o["NS.objects"])}
            if "NS.objects" in o:
                return [res(v) for v in o["NS.objects"]]
            if "NS.string" in o:
                return o["NS.string"]
            return {k: res(v) for k, v in o.items()}
        if isinstance(o, list):
            return [res(v) for v in o]
        return o
    return res(d["$top"]["fixtureProfile"])

def table(prof):
    """[(personality name, footprint, [(channel, class, params, settings)])]"""
    out = []
    for p in prof.get("personalities") or []:
        rows = []
        for cap in p.get("capabilities") or []:
            if not isinstance(cap, dict):
                continue
            cls = cap.get("$class", "?")
            if isinstance(cls, dict): cls = cls.get("$classname", "?")
            sets = []
            for st in cap.get("settings") or []:
                if isinstance(st, dict):
                    rng = st.get("$0"); params = st.get("params") or {}
                    sets.append((rng.get("$0") if isinstance(rng, dict) else rng, rng.get("$1") if isinstance(rng, dict) else None, {k: v for k, v in params.items() if k != "$class"}))
            rows.append((cap.get("channel"), cls, cap.get("customName"), sets))
        rows.sort(key=lambda r: (r[0] if isinstance(r[0], int) else 999))
        out.append((p.get("name") or p.get("customName"), p.get("footprint"), rows))
    return out

if __name__ == "__main__":
    for name in sys.argv[1:]:
        prof = unarchive(P / name)
        print("==", prof.get("manufacturer"), "|", prof.get("name"), "| pan", prof.get("panRange"), "tilt", prof.get("tiltRange"))
        for pname, fp, rows in table(prof):
            print("  MODE", pname, "footprint", fp)
            for ch, cls, custom, sets in rows:
                s = " ; ".join(f"{a}..{b} {p}" for a, b, p in sets[:10])
                print(f"    ch{ch:>3} {cls:<34} {custom or ''} {s[:160]}")
