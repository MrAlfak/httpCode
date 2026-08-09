#!/usr/bin/env python3
"""Validate the HTTP status dataset and translation files without third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CODES_PATH = ROOT / "codes.json"
IANA_PATH = ROOT / "data" / "iana.json"
VENDORS_PATH = ROOT / "data" / "vendors.json"
I18N_DIR = ROOT / "i18n"
VALID_TYPES = {"standard", "vendor"}
VALID_STATUS = {"active", "temporary", "unused", "obsoleted"}
VALID_SOURCE_QUALITY = {"official", "vendor", "community", "historical"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def expected_class(code: int) -> str:
    names = {1: "Informational", 2: "Success", 3: "Redirection", 4: "Client Error", 5: "Server Error"}
    family = code // 100
    return f"{family}xx {names.get(family, 'Extension')}"


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        codes = load_json(CODES_PATH); iana = load_json(IANA_PATH); vendors = load_json(VENDORS_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load core data: {exc}"], warnings
    if not isinstance(codes, list) or not codes:
        return ["codes.json must be a non-empty array"], warnings
    seen_ids: set[str] = set(); standard_codes: set[int] = set(); vendor_keys: set[tuple[str, int]] = set()
    for index, item in enumerate(codes):
        where = f"codes.json[{index}]"
        if not isinstance(item, dict): errors.append(f"{where}: entry must be an object"); continue
        for key in ("id","code","type","provider","phrase","description","class","status","source"):
            if key not in item: errors.append(f"{where}: missing {key}")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_RE.match(item_id): errors.append(f"{where}: invalid id {item_id!r}")
        elif item_id in seen_ids: errors.append(f"{where}: duplicate id {item_id}")
        else: seen_ids.add(item_id)
        code = item.get("code")
        if not isinstance(code, int) or not (100 <= code <= 999): errors.append(f"{where}: code must be an integer from 100 to 999"); continue
        item_type = item.get("type")
        if item_type not in VALID_TYPES: errors.append(f"{where}: invalid type {item_type!r}")
        if item.get("status") not in VALID_STATUS: errors.append(f"{where}: invalid status {item.get('status')!r}")
        if item.get("class") != expected_class(code): errors.append(f"{where}: class does not match code family")
        source = item.get("source")
        if not isinstance(source, dict): errors.append(f"{where}: source must be an object")
        else:
            if not source.get("name"): errors.append(f"{where}: source.name is required")
            if not isinstance(source.get("url"), str) or not is_https_url(source["url"]): errors.append(f"{where}: source.url must be HTTPS")
            if source.get("quality") not in VALID_SOURCE_QUALITY: errors.append(f"{where}: invalid source.quality")
        verified_at = item.get("verified_at")
        if verified_at is not None:
            try: date.fromisoformat(verified_at)
            except (TypeError, ValueError): errors.append(f"{where}: verified_at must be YYYY-MM-DD or null")
        elif source and source.get("quality") in {"official", "vendor"}: warnings.append(f"{where}: authoritative source is not date-verified")
        if item_type == "standard":
            if item.get("provider") != "iana": errors.append(f"{where}: standard entries must use provider 'iana'")
            if code in standard_codes: errors.append(f"{where}: duplicate standard code {code}")
            standard_codes.add(code)
            if item_id != f"iana-{code}": errors.append(f"{where}: standard id must be iana-{code}")
        elif item_type == "vendor":
            provider = item.get("provider")
            if not isinstance(provider, str) or not provider: errors.append(f"{where}: vendor provider is required")
            key = (str(provider), code)
            if key in vendor_keys: errors.append(f"{where}: duplicate vendor/provider combination {key}")
            vendor_keys.add(key)
    snapshot = {entry["code"]: entry for entry in iana.get("entries", [])}
    dataset_standard = {item["code"]: item for item in codes if item.get("type") == "standard"}
    if set(snapshot) != set(dataset_standard):
        errors.append(f"IANA snapshot mismatch: missing={sorted(set(snapshot)-set(dataset_standard))}, extra={sorted(set(dataset_standard)-set(snapshot))}")
    else:
        for code, expected in snapshot.items():
            actual = dataset_standard[code]
            for field in ("phrase","status","reference","description"):
                if actual.get(field) != expected.get(field): errors.append(f"IANA {code}: {field} differs from pinned snapshot")
    vendor_ids = {item["id"] for item in vendors}
    dataset_vendor_ids = {item["id"] for item in codes if item.get("type") == "vendor"}
    if vendor_ids != dataset_vendor_ids: errors.append("Vendor source file and generated dataset are out of sync")
    standard_ids = {f"iana-{code}" for code in standard_codes}; legacy_numeric_keys = {str(code) for code in standard_codes}
    for path in sorted(I18N_DIR.glob("*.json")):
        if path.name == "manifest.json": continue
        try: translations = load_json(path)
        except (OSError, json.JSONDecodeError) as exc: errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}"); continue
        if not isinstance(translations, dict): errors.append(f"{path.relative_to(ROOT)}: root must be an object"); continue
        for key, value in translations.items():
            if key not in standard_ids and key not in legacy_numeric_keys and key not in seen_ids: warnings.append(f"{path.relative_to(ROOT)}: translation key {key!r} has no dataset entry")
            if not isinstance(value, dict): errors.append(f"{path.relative_to(ROOT)}:{key}: translation must be an object"); continue
            if not isinstance(value.get("phrase"), str) or not isinstance(value.get("description"), str): errors.append(f"{path.relative_to(ROOT)}:{key}: phrase and description are required strings")
    return errors, warnings


def main() -> int:
    errors, warnings = validate()
    for warning in warnings: print(f"WARNING: {warning}")
    for error in errors: print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s).", file=sys.stderr); return 1
    print(f"Validation passed with {len(warnings)} warning(s)."); return 0


if __name__ == "__main__": raise SystemExit(main())
