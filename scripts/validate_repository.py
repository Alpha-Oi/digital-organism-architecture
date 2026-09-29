#!/usr/bin/env python3
"""Validate the canonical DOA repository without modifying it."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    ".gitattributes",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/validate.yml",
    "CHANGELOG.md",
    "CHANGES_AND_NEW_FINDINGS.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "docs/ARCHITECTURE.md",
    "docs/BIOLOGY_TO_IT_MAPPING.md",
    "docs/DOA_STANDARD_v1.0.md",
    "docs/GENOME_AND_EVOLUTION.md",
    "docs/HOMEOSTASIS.md",
    "docs/MEMORY_AND_NERVOUS_SYSTEM.md",
    "docs/METABOLISM.md",
    "docs/PRINCIPLES.md",
    "docs/ROBOTICS_EXTENSION.md",
    "docs/RELEASE_READINESS_v1.0.md",
    "docs/SECURITY_AND_IMMUNITY.md",
    "docs/SOURCES.md",
    "reference/EXAMPLE_GENOME.yaml",
    "reference/REFERENCE_ARCHITECTURE.md",
    "reference/REFERENCE_STACK.md",
    "requirements-validation.txt",
    "specifications/cell.schema.json",
    "specifications/event.schema.json",
    "specifications/genome.schema.json",
    "specifications/hormone.schema.json",
    "specifications/organ.schema.json",
    "specifications/organism.schema.json",
    "templates/DOA_CONFORMANCE_CLAIM.md",
}

REQUIRED_MAPPING_TERMS = {
    "Nucleus",
    "Nucleolus",
    "Cytoskeleton",
    "Peroxisomes",
    "Golgi",
    "DNA repair",
    "Epigenetics",
    "Morphogenesis",
    "Differentiation",
    "Neuroplasticity",
    "Regeneration",
    "Inflammation",
    "Senescence",
    "Oncogenesis",
    "Microbiome",
    "Immune tolerance",
    "Circadian rhythm",
    "Emergency circulation",
    "Proteostasis",
    "Extracellular matrix",
    "Coagulation",
    "Respiratory exchange",
    "Nociception",
    "Quorum sensing",
    "Ecosystem treaty",
}

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
MERMAID_START = re.compile(
    r"^\s*(flowchart|graph|stateDiagram(?:-v2)?|sequenceDiagram|classDiagram|erDiagram|gantt|pie|mindmap|timeline|gitGraph)\b"
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_required_files(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_FILES):
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"missing required file: {relative}")
        elif path.stat().st_size == 0:
            fail(errors, f"empty required file: {relative}")


def load_schemas(errors: list[str]) -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for path in sorted((ROOT / "specifications").glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # validation tool must aggregate all failures
            fail(errors, f"invalid JSON Schema {path.relative_to(ROOT)}: {exc}")
            continue
        schema_id = schema.get("$id")
        if not schema_id:
            fail(errors, f"schema has no $id: {path.relative_to(ROOT)}")
            continue
        schemas[schema_id] = schema
    if len(schemas) != 6:
        fail(errors, f"expected 6 schemas, found {len(schemas)}")
    return schemas


def validate_example_genome(errors: list[str], schemas: dict[str, dict]) -> None:
    try:
        instance = yaml.safe_load(
            (ROOT / "reference/EXAMPLE_GENOME.yaml").read_text(encoding="utf-8")
        )
        registry = Registry().with_resources(
            [(schema_id, Resource.from_contents(schema)) for schema_id, schema in schemas.items()]
        )
        genome = next(schema for schema in schemas.values() if schema.get("title") == "DOA Genome")
        Draft202012Validator(genome, registry=registry).validate(instance)
    except Exception as exc:
        fail(errors, f"EXAMPLE_GENOME.yaml does not validate: {exc}")


def validate_yaml_documents(errors: list[str]) -> None:
    for pattern in ("*.yml", "*.yaml"):
        for path in sorted(ROOT.rglob(pattern)):
            if ".git" in path.parts:
                continue
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(errors, f"invalid YAML {path.relative_to(ROOT)}: {exc}")


def validate_markdown(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                fail(errors, f"trailing whitespace: {relative}:{line_number}")
            if re.search(r"\b(TODO|TBD)\b", line):
                fail(errors, f"unfinished marker: {relative}:{line_number}")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            local_target = target.split("#", 1)[0]
            if local_target and not (path.parent / local_target).resolve().exists():
                fail(errors, f"broken local link in {relative}: {target}")


def validate_diagrams(errors: list[str]) -> None:
    diagrams = sorted((ROOT / "diagrams").glob("*.md"))
    if len(diagrams) != 6:
        fail(errors, f"expected 6 diagram documents, found {len(diagrams)}")
    for path in diagrams:
        blocks = MERMAID_BLOCK.findall(path.read_text(encoding="utf-8"))
        if len(blocks) != 1:
            fail(errors, f"expected one Mermaid block: {path.relative_to(ROOT)}")
        elif not MERMAID_START.search(blocks[0]):
            fail(errors, f"unknown Mermaid diagram start: {path.relative_to(ROOT)}")


def validate_mapping(errors: list[str]) -> None:
    path = ROOT / "docs/BIOLOGY_TO_IT_MAPPING.md"
    text = path.read_text(encoding="utf-8")
    for term in sorted(REQUIRED_MAPPING_TERMS):
        if term not in text:
            fail(errors, f"required mapping term missing: {term}")
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("|")
        and not line.startswith("|---")
        and not line.startswith("| Механизм")
    ]
    if len(rows) < 70:
        fail(errors, f"expected at least 70 mechanism rows, found {len(rows)}")
    for index, row in enumerate(rows, start=1):
        if row.count("|") != 9:
            fail(errors, f"mapping row {index} does not have 8 columns")


def validate_canonical_terms(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    standard = (ROOT / "docs/DOA_STANDARD_v1.0.md").read_text(encoding="utf-8")
    if "метаархитектурный стандарт" not in readme:
        fail(errors, "README must define DOA as a meta-architecture standard")
    if "DOA — метаархитектурный стандарт" not in standard:
        fail(errors, "canonical terminology missing from DOA standard")
    if "Apache License" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        fail(errors, "LICENSE is not recognizable as Apache License")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    schemas = load_schemas(errors)
    if schemas:
        validate_example_genome(errors, schemas)
    validate_yaml_documents(errors)
    validate_markdown(errors)
    validate_diagrams(errors)
    validate_mapping(errors)
    validate_canonical_terms(errors)

    if errors:
        print("DOA repository validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("DOA repository validation: PASS")
    print(f"- required files: {len(REQUIRED_FILES)}")
    print(f"- schemas: {len(schemas)}")
    print("- example genome: valid")
    print("- YAML documents: valid")
    print("- Markdown links and whitespace: valid")
    print("- Mermaid documents: 6")
    print("- Biology-to-IT mapping coverage: valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
