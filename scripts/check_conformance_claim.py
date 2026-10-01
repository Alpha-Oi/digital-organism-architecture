#!/usr/bin/env python3
"""Check a DOA conformance claim against the schema and the requirement registry.

Usage: python scripts/check_conformance_claim.py claim.yaml

The script checks structure and coverage rules from docs/CONFORMANCE.md. It does not
inspect the evidence artifacts themselves; that is the assessor's responsibility. It prints
warnings (exit code unchanged) for evidence references that cannot be immutable.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MUTABLE_REFS = {"main", "master", "develop", "development", "head", "latest"}
BRANCH_URL = re.compile(r"https?://[^\s;]+?/(?:blob|tree|raw)/([^/\s;]+)/", re.I)
HEX_ID = re.compile(r"(?i)\b[0-9a-f]{7,64}\b")


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

    errors += check_failure_classes(claim, seen)

    for rid, entry in seen.items():
        if rid in by_id and by_id[rid]["profile"] not in profiles | {"Conditional"}:
            errors.append(f"requirement {rid} belongs to profile {by_id[rid]['profile']} that is not claimed")
    return errors


def failure_class_ids() -> set[str]:
    registry = yaml.safe_load((ROOT / "specifications/failure-classes.yaml").read_text(encoding="utf-8"))
    return {item["id"] for item in registry["failure_classes"]}


def check_failure_classes(claim: dict, seen: dict[str, dict]) -> list[str]:
    """Consistency of the optional `failure_classes` field with the registry and with REQ-CORE-23."""
    entries = claim.get("failure_classes")
    if entries is None:
        return []
    errors: list[str] = []
    known = failure_class_ids()
    by_class: dict[str, dict] = {}
    for entry in entries:
        if entry["id"] not in known:
            errors.append(f"unknown failure class id: {entry['id']}")
        elif entry["id"] in by_class:
            errors.append(f"duplicate failure class id: {entry['id']}")
        by_class[entry["id"]] = entry
    complete_claim = claim["status"] == "VERIFIED" or seen.get("REQ-CORE-23", {}).get("status") == "PASS"
    if complete_claim:
        for class_id in sorted(known):
            entry = by_class.get(class_id)
            if entry is None:
                errors.append(f"failure class {class_id} is not covered although REQ-CORE-23 is PASS or the claim is VERIFIED")
            elif entry["status"] not in {"PASS", "EXCLUDED"}:
                errors.append(f"failure class {class_id} has status {entry['status']} although REQ-CORE-23 is PASS or the claim is VERIFIED")
    return errors


def evidence_warnings(claim: dict) -> list[str]:
    """Warnings for evidence_ref values that cannot satisfy rule 2 of docs/CONFORMANCE.md (immutable reference)."""
    warnings: list[str] = []
    entries = list(claim.get("requirements", [])) + list(claim.get("failure_classes", []))
    for entry in entries:
        ref = entry.get("evidence_ref")
        if not ref:
            continue
        for part in (piece.strip() for piece in ref.split(";") if piece.strip()):
            match = BRANCH_URL.search(part)
            if match and match.group(1).lower() in MUTABLE_REFS:
                warnings.append(f"{entry['id']}: evidence_ref points to a mutable ref '{match.group(1)}': {part}")
            elif "/" not in part and ":" not in part and not HEX_ID.search(part):
                warnings.append(f"{entry['id']}: evidence_ref has no path or identifier: {part!r}")
    return warnings


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
    for warning in evidence_warnings(claim):
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
