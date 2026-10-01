#!/usr/bin/env python3
"""Check a DOA verification report against the Verification Kit plan and, optionally, a conformance claim.

Usage: python scripts/check_verification_report.py report.yaml [--claim claim.yaml]

The script checks structure, references to verification/conformance-test-plan.yaml and verification/fault-scenarios.yaml,
the isolation rules of the plan and, with --claim, contradictions between the report and a claim. It does not run tests and
does not inspect the evidence artifacts; that remains the assessor's responsibility. Exit code 1 means errors; warnings do not change it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative: str) -> dict:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def check_report(report: dict, claim: dict | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    schema = json.loads((ROOT / "specifications/verification-report.schema.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(report):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema: {location}: {error.message}")
    if errors:
        return errors, warnings

    plan = load_yaml("verification/conformance-test-plan.yaml")
    cases = {case["id"]: case for case in plan["cases"]}
    scenarios = {item["id"]: item for item in load_yaml("verification/fault-scenarios.yaml")["scenarios"]}
    if report["plan_version"] != plan["plan_version"]:
        warnings.append(f"report plan_version {report['plan_version']} differs from the plan version {plan['plan_version']}")

    default_environment = report["environment"]["type"]
    results: dict[str, dict] = {}
    for entry in report["results"]:
        case_id = entry["case"]
        if case_id not in cases:
            errors.append(f"unknown test case id: {case_id}")
        elif case_id in results:
            errors.append(f"duplicate test case id: {case_id}")
        elif cases[case_id].get("isolated_environment") and entry.get("environment_type", default_environment) != "isolated":
            errors.append(f"{case_id} requires an isolated environment")
        results[case_id] = entry

    scenario_results: dict[str, dict] = {}
    for entry in report.get("scenario_results", []):
        scenario_id = entry["scenario"]
        if scenario_id not in scenarios:
            errors.append(f"unknown scenario id: {scenario_id}")
        elif scenario_id in scenario_results:
            errors.append(f"duplicate scenario id: {scenario_id}")
        elif scenarios[scenario_id]["minimum_environment"] == "isolated" and entry.get("environment_type", default_environment) != "isolated":
            errors.append(f"{scenario_id} requires an isolated environment")
        scenario_results[scenario_id] = entry

    for case_id, entry in results.items():
        if entry["status"] != "PASS" or case_id not in cases:
            continue
        for scenario_id in cases[case_id].get("scenarios", []):
            if scenario_results.get(scenario_id, {}).get("status") != "PASS":
                errors.append(f"{case_id} is PASS but scenario {scenario_id} has no PASS result")

    if claim is not None:
        for requirement in claim.get("requirements", []):
            if requirement["status"] != "PASS":
                continue
            required = [case_id for case_id, case in cases.items() if case["requirement"] == requirement["id"]]
            for case_id in required:
                status = results.get(case_id, {}).get("status")
                if status == "FAIL":
                    errors.append(f"claim reports {requirement['id']} as PASS but {case_id} is FAIL")
                elif status != "PASS":
                    warnings.append(f"claim reports {requirement['id']} as PASS but {case_id} is not PASS in this report ({status or 'absent'})")
    return errors, warnings


def main(argv: list[str]) -> int:
    args = argv[1:]
    claim_path = None
    if "--claim" in args:
        position = args.index("--claim")
        if position + 1 >= len(args):
            print(__doc__)
            return 2
        claim_path = args[position + 1]
        del args[position:position + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    report = yaml.safe_load(Path(args[0]).read_text(encoding="utf-8"))
    claim = yaml.safe_load(Path(claim_path).read_text(encoding="utf-8")) if claim_path else None
    errors, warnings = check_report(report, claim)
    if errors:
        print("DOA verification report: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    passed = sum(1 for entry in report["results"] if entry["status"] == "PASS")
    print(f"DOA verification report: PASS ({passed} of {len(report['results'])} cases PASS)")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
