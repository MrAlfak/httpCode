#!/usr/bin/env python3
"""Compare the pinned IANA snapshot with the live IANA CSV registry."""
from __future__ import annotations
import csv, io, json, sys, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SNAPSHOT_PATH=ROOT/"data"/"iana.json"; CSV_URL="https://www.iana.org/assignments/http-status-codes/http-status-codes-1.csv"

def normalize_description(value: str) -> tuple[str,str]:
    value=value.strip()
    if "(TEMPORARY" in value: return value.split(" (TEMPORARY",1)[0],"temporary"
    if value.endswith("(OBSOLETED)"): return value[:-len(" (OBSOLETED)")].strip(),"obsoleted"
    if value=="(Unused)": return value,"unused"
    return value,"active"

def fetch_live() -> dict[int,dict]:
    request=urllib.request.Request(CSV_URL,headers={"User-Agent":"httpCode-registry-check/2"})
    with urllib.request.urlopen(request,timeout=20) as response: text=response.read().decode("utf-8-sig")
    result={}
    for row in csv.DictReader(io.StringIO(text)):
        raw=(row.get("Value") or "").strip()
        if not raw.isdigit(): continue
        phrase,status=normalize_description(row.get("Description") or "")
        result[int(raw)]={"phrase":phrase,"status":status}
    return result

def main() -> int:
    snapshot=json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8")); pinned={entry["code"]:entry for entry in snapshot["entries"]}
    try: live=fetch_live()
    except Exception as exc: print(f"Could not fetch IANA registry: {exc}",file=sys.stderr); return 2
    problems=[]
    if set(pinned)!=set(live): problems.append(f"assigned-code set changed: added={sorted(set(live)-set(pinned))}, removed={sorted(set(pinned)-set(live))}")
    for code in sorted(set(pinned)&set(live)):
        for field in ("phrase","status"):
            if pinned[code][field]!=live[code][field]: problems.append(f"{code} {field}: pinned={pinned[code][field]!r}, live={live[code][field]!r}")
    if problems:
        print("IANA registry differs from the pinned snapshot:",file=sys.stderr)
        for problem in problems: print(f"- {problem}",file=sys.stderr)
        return 1
    print("Pinned IANA snapshot matches the live registry."); return 0
if __name__ == "__main__": raise SystemExit(main())
