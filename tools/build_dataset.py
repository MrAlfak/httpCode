#!/usr/bin/env python3
"""Build codes.json from the pinned IANA snapshot and vendor extensions."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IANA_PATH = ROOT / "data" / "iana.json"
VENDOR_PATH = ROOT / "data" / "vendors.json"
OUTPUT_PATH = ROOT / "codes.json"

CLASS_NAMES = {1: "Informational", 2: "Success", 3: "Redirection", 4: "Client Error", 5: "Server Error"}


def code_class(code: int) -> str:
    family = code // 100
    return f"{family}xx {CLASS_NAMES.get(family, 'Extension')}"


def build_dataset() -> list[dict]:
    iana = json.loads(IANA_PATH.read_text(encoding="utf-8"))
    vendors = json.loads(VENDOR_PATH.read_text(encoding="utf-8"))
    result: list[dict] = []
    for entry in iana["entries"]:
        result.append({
            "id": f"iana-{entry['code']}", "code": entry["code"], "type": "standard", "provider": "iana",
            "phrase": entry["phrase"], "description": entry["description"], "class": code_class(entry["code"]),
            "status": entry["status"], "reference": entry["reference"],
            "source": {"name": iana["registry"], "url": iana["source"], "quality": "official"},
            "verified_at": iana["snapshot_date"],
            "mdn_link": f"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{entry['code']}" if entry["status"] == "active" else None,
        })
    for vendor in vendors:
        item = dict(vendor)
        item["class"] = code_class(item["code"])
        result.append(item)
    result.sort(key=lambda item: (item["code"], 0 if item["type"] == "standard" else 1, item.get("provider", "")))
    return result


def main() -> int:
    dataset = build_dataset()
    OUTPUT_PATH.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(dataset)} entries to {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
