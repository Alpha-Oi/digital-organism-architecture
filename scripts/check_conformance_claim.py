#!/usr/bin/env python3
"""Check a DOA conformance claim against the schema and the requirement registry.

Usage: python scripts/check_conformance_claim.py claim.yaml

The script checks structure and coverage rules from docs/CONFORMANCE.md. It does not
inspect the evidence artifacts themselves; that is the assessor's responsibility.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def check_claim(claim: dict) -> list[str]:
    errors: list[str] = []
    schema = json.loads((ROOT / "specifications/conformance-claim.schema.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(claim):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema: {location}: {error.message}")
    if errors:
        return errors

    registry = yaml.safe_load((ROOT / "specifications/requirements.yaml").read_text(encoding="utf-8"))["requirements"]
    by_id = {item["id"]: item for item in registry}
    profiles = set(claim["profiles"])
    if "Core" not in profiles:
        errors.append("claim must include the Core profile")

    seen: dict[str, dict] = {}
    for entry in claim["requirements"]:
        if entry["id"] not in by_id:
            errors.append(f"unknown requirement id: {entry['id']}")
        if entry["id"] in seen:
            errors.append(f"duplicate requirement id: {entry['id']}")
        seen[entry["id"]] = entry

    applicable = {rid for rid, item in by_id.items() if item["profile"] in profiles | {"Conditional"}}
    status = claim["status"]
    if status == "VERIFIED":
        for rid in sorted(applicable):
            entry = seen.get(rid)
            if entry is None:
                errors.append(f"VERIFIED claim does not cover {rid}")
            elif entry["status"] not in {"PASS", "EXCLUDED"}:
                errors.append(f"VERIFIED claim has {rid} with status {entry['status']}")
            elif entry["status"] == "EXCLUDED" and by_id[rid]["profile"] == "Core" and claim["assurance"] != "independently-reviewed":
                errors.append(f"Core exclusion {rid} requires assurance=independently-reviewed")
    elif status == "PARTIAL":
        if not any(entry["status"] == "PASS" for entry in claim["requirements"]):
            errors.append("PARTIAL claim must contain at least one PASS requirement with evidence")
    elif status == "UNVERIFIED" and any(entry["status"] == "PASS" for entry in claim["requirements"]):
        errors.append("UNVERIFIED claim must not report PASS requirements; use PARTIAL or VERIFIED")

    for rid, entry in seen.items():
        if rid in by_id and by_id[rid]["profile"] not in profiles | {"Conditional"}:
            errors.append(f"requirement {rid} belongs to profile {by_id[rid]['profile']} that is not claimed")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    claim = yaml.safe_load(Path(argv[1]).read_text(encoding="utf-8"))
    errors = check_claim(claim)
    if errors:
        print("DOA conformance claim: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"DOA conformance claim: PASS ({claim['status']}, {len(claim['requirements'])} requirements assessed)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
