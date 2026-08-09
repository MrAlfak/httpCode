#!/usr/bin/env python3
"""Report translation coverage and optionally write a web manifest."""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CODES = json.loads((ROOT / "codes.json").read_text(encoding="utf-8")); I18N_DIR = ROOT / "i18n"
STANDARD = [item for item in CODES if item["type"] == "standard"]
STANDARD_IDS = {item["id"] for item in STANDARD}; STANDARD_CODES = {str(item["code"]) for item in STANDARD}; ALL_IDS = {item["id"] for item in CODES}

def translated_sets(data: dict) -> tuple[set[str], set[str]]:
    standard=set(); overall=set()
    for key in data:
        if key in STANDARD_IDS or key in STANDARD_CODES: standard.add(key)
        if key in ALL_IDS or key in STANDARD_CODES: overall.add(key)
    return standard, overall

def rows() -> list[dict]:
    result=[]
    for path in sorted(I18N_DIR.glob("*.json")):
        if path.name == "manifest.json": continue
        data=json.loads(path.read_text(encoding="utf-8")); standard, overall=translated_sets(data)
        result.append({"lang":path.stem,"translated_standard":len(standard),"standard_total":len(STANDARD),"standard_percent":round(100*len(standard)/len(STANDARD),1),"translated_overall":len(overall),"overall_total":len(CODES),"overall_percent":round(100*len(overall)/len(CODES),1)})
    return result

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--json",action="store_true"); parser.add_argument("--write-manifest",type=Path); args=parser.parse_args(); result=rows()
    if args.write_manifest:
        args.write_manifest.parent.mkdir(parents=True,exist_ok=True); args.write_manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(f"{'LANG':<12} {'STANDARD':>12} {'OVERALL':>12}")
        for row in result: print(f"{row['lang']:<12} {row['standard_percent']:>10.1f}% {row['overall_percent']:>10.1f}%")
    return 0
if __name__ == "__main__": raise SystemExit(main())
