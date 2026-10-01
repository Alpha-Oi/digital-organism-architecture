#!/usr/bin/env python3
"""Validate the canonical DOA repository without modifying it.

Checks structure, JSON Schemas, examples (valid and invalid), state machines vs schemas/diagrams/docs,
the Biology-to-IT matrix, the conformance requirement registry, cross-references, versions and Markdown hygiene.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_NAMES = {
    "capability-grant", "cell", "conformance-claim", "control-loop", "event", "genome", "health-evidence",
    "hormone", "lifecycle-transition", "lineage-manifest", "memory-record", "organ", "organism", "policy-overlay",
}

REQUIRED_FILES = {
    ".gitattributes", ".gitignore", ".github/CODEOWNERS", ".github/dependabot.yml", ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/standard-gap.yml", ".github/workflows/validate.yml",
    "CHANGELOG.md", "CHANGES_AND_NEW_FINDINGS.md", "CONTRIBUTING.md", "GOVERNANCE.md", "LICENSE", "README.md",
    "ROADMAP.md", "SECURITY.md", "VERSION",
    "docs/ARCHITECTURE.md", "docs/BIOLOGY_TO_IT_MAPPING.md", "docs/BOUNDARY_AND_IDENTITY.md", "docs/CONFORMANCE.md",
    "docs/DOA_STANDARD_v1.0.md", "docs/FAILURE_AND_RECOVERY.md", "docs/GENOME_AND_EVOLUTION.md", "docs/HOMEOSTASIS.md",
    "docs/IMPLEMENTATION_GUIDE.md",
    "docs/LIFECYCLE.md", "docs/MEMORY_AND_NERVOUS_SYSTEM.md", "docs/METABOLISM.md", "docs/PRINCIPLES.md",
    "docs/RELEASE_READINESS_v1.0.md", "docs/ROBOTICS_EXTENSION.md", "docs/SECURITY_AND_IMMUNITY.md", "docs/SOURCES.md",
    "docs/TERMINOLOGY.md",
    "reference/EXAMPLE_GENOME.yaml", "reference/REFERENCE_ARCHITECTURE.md", "reference/REFERENCE_STACK.md",
    "requirements-validation.txt", "scripts/check_conformance_claim.py", "scripts/validate_repository.py",
    "specifications/failure-classes.yaml", "specifications/requirements.yaml", "specifications/state-machines.yaml",
    "templates/DOA_CONFORMANCE_CLAIM.md",
} | {f"specifications/{name}.schema.json" for name in SCHEMA_NAMES}

DIAGRAM_MACHINES = {
    "organism-lifecycle": "organism",
    "cell-lifecycle": "cell",
    "immune-response": "incident",
    "change-protocol": "change",
    "embodied-safety": "embodied_safety",
}
OTHER_DIAGRAMS = {"apoptosis-flow", "homeostasis-loop", "organism-layers", "system-context"}

REQUIRED_MAPPING_TERMS = {
    "Nucleus", "Nucleolus", "Cytoskeleton", "Peroxisomes", "Golgi", "DNA repair", "Epigenetics", "Morphogenesis",
    "Differentiation", "Neuroplasticity", "Regeneration", "Inflammation", "Senescence", "Oncogenesis", "Microbiome",
    "Immune tolerance", "Circadian rhythm", "Emergency circulation", "Proteostasis", "Extracellular matrix",
    "Coagulation", "Respiratory exchange", "Nociception", "Quorum sensing", "Ecosystem treaty", "Endocrine",
    "Immune memory", "Innate immunity", "Adaptive immunity", "Self / non-self", "Necrosis", "Apoptosis", "Autophagy",
    "Lysosomes", "Mitochondria", "Nutrient and oxygen sensing", "Cellular stress response", "Reproduction",
    "Checkpoints", "Stem-cell", "Compartmentalization", "Positive feedback", "Homeostasis (negative feedback)",
    "Redundant organs", "Genetic drift", "Natural selection", "Horizontal transfer", "Competition", "Forgetting",
    "attention/salience", "Spinal reflex", "Peripheral ganglia", "Sensory hierarchy", "Motor hierarchy",
    "Synchronization", "Identity continuity", "State continuity", "Provenance", "Heredity", "Organism termination",
    "Organism-scale regeneration", "Sensor fusion and calibration", "Withdrawal reflex",
}

MAPPING_COLUMNS = 12
PROFILES = {"Core", "Distributed", "Adaptive", "Embodied", "Conditional", "Pattern", "Anti-pattern"}
REQ_PREFIX = {"Core": "CORE", "Distributed": "DIST", "Adaptive": "ADPT", "Embodied": "EMB", "Conditional": "COND"}

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
MERMAID_START = re.compile(
    r"^\s*(flowchart|graph|stateDiagram(?:-v2)?|sequenceDiagram|classDiagram|erDiagram|gantt|pie|mindmap|timeline|gitGraph)\b"
)
EDGE = re.compile(r"^\s*([A-Z_]+)\s*-->\s*([A-Z_]+)\s*$")
MECHANISM_ID = re.compile(r"(?<![A-Za-z0-9`-])([CTNMHIER]-\d{2})(?![\d-])")
REQ_ID = re.compile(r"\bREQ-(?:CORE|DIST|ADPT|EMB|COND)-\d{2}\b")
STALE = re.compile(r"(?i)\b(draft|beta|provisional|release candidate)\b|УСЛОВНО ГОТОВО|NOT_CONFIGURED|\bPENDING\b")
STALE_CHECKED = [
    "README.md", "docs/DOA_STANDARD_v1.0.md", "GOVERNANCE.md", "SECURITY.md", "ROADMAP.md", "CONTRIBUTING.md",
    "docs/RELEASE_READINESS_v1.0.md", "docs/CONFORMANCE.md", "docs/TERMINOLOGY.md",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def text_of(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def validate_required_files(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_FILES):
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"missing required file: {relative}")
        elif path.stat().st_size == 0:
            fail(errors, f"empty required file: {relative}")
    for junk in ("__pycache__", ".DS_Store", ".env"):
        for path in ROOT.rglob(junk):
            if ".git" not in path.parts:
                fail(errors, f"junk artifact in tree: {path.relative_to(ROOT)}")


def load_schemas(errors: list[str]) -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for path in sorted((ROOT / "specifications").glob("*.schema.json")):
        name = path.name.removesuffix(".schema.json")
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # aggregate all failures
            fail(errors, f"invalid JSON Schema {path.relative_to(ROOT)}: {exc}")
            continue
        expected_id = f"https://doa-standard.org/schemas/{path.name}"
        if schema.get("$id") != expected_id:
            fail(errors, f"schema {path.name} has $id {schema.get('$id')!r}, expected {expected_id!r}")
        schemas[name] = schema
    if set(schemas) != SCHEMA_NAMES:
        fail(errors, f"schema set mismatch: missing {sorted(SCHEMA_NAMES - set(schemas))}, extra {sorted(set(schemas) - SCHEMA_NAMES)}")
    return schemas


def make_registry(schemas: dict[str, dict]) -> Registry:
    return Registry().with_resources([(s["$id"], Resource.from_contents(s)) for s in schemas.values()])


def validate_examples(errors: list[str], schemas: dict[str, dict]) -> None:
    registry = make_registry(schemas)
    covered: dict[str, set[str]] = {name: set() for name in schemas}
    cases = [("valid", p) for p in sorted((ROOT / "reference/examples/valid").glob("*.yaml"))]
    cases += [("invalid", p) for p in sorted((ROOT / "reference/examples/invalid").glob("*.yaml"))]
    cases.append(("valid", ROOT / "reference/EXAMPLE_GENOME.yaml"))
    for kind, path in cases:
        name = "genome" if path.name == "EXAMPLE_GENOME.yaml" else path.name.split("--")[0]
        if name not in schemas:
            fail(errors, f"example {path.relative_to(ROOT)} does not name a known schema")
            continue
        try:
            instance = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"invalid YAML {path.relative_to(ROOT)}: {exc}")
            continue
        problems = list(Draft202012Validator(schemas[name], registry=registry).iter_errors(instance))
        if kind == "valid" and problems:
            fail(errors, f"valid example fails {name} schema: {path.relative_to(ROOT)}: {problems[0].message[:120]}")
        if kind == "invalid" and not problems:
            fail(errors, f"invalid example unexpectedly passes {name} schema: {path.relative_to(ROOT)}")
        covered[name].add(kind)
    for name, kinds in covered.items():
        if kinds != {"valid", "invalid"}:
            fail(errors, f"schema {name} needs both valid and invalid examples, has {sorted(kinds)}")


def load_machines(errors: list[str]) -> dict[str, dict]:
    machines = yaml.safe_load(text_of("specifications/state-machines.yaml"))["machines"]
    for name, machine in machines.items():
        states = machine["states"]
        if len(states) != len(set(states)):
            fail(errors, f"machine {name}: duplicate states")
        if machine["initial"] not in states:
            fail(errors, f"machine {name}: unknown initial state")
        edges = set()
        for transition in machine["transitions"]:
            for key in ("from", "to", "guard", "authority", "timeout"):
                if not transition.get(key):
                    fail(errors, f"machine {name}: transition {transition} lacks {key}")
            if transition["from"] not in states or transition["to"] not in states:
                fail(errors, f"machine {name}: transition uses undeclared state: {transition['from']}->{transition['to']}")
            edge = (transition["from"], transition["to"])
            if edge in edges:
                fail(errors, f"machine {name}: duplicate transition {edge}")
            edges.add(edge)
            if transition["from"] in machine["terminal"]:
                fail(errors, f"machine {name}: terminal state {transition['from']} has outgoing transition")
        reachable, frontier = {machine["initial"]}, [machine["initial"]]
        while frontier:
            current = frontier.pop()
            for src, dst in edges:
                if src == current and dst not in reachable:
                    reachable.add(dst)
                    frontier.append(dst)
        for state in set(states) - reachable:
            fail(errors, f"machine {name}: state {state} unreachable from {machine['initial']}")
        if machine["terminal"]:
            for state in states:
                if state in machine["terminal"]:
                    continue
                seen, stack = {state}, [state]
                while stack:
                    current = stack.pop()
                    for src, dst in edges:
                        if src == current and dst not in seen:
                            seen.add(dst)
                            stack.append(dst)
                if not seen & set(machine["terminal"]):
                    fail(errors, f"machine {name}: state {state} cannot reach a terminal state")
    return machines


def validate_state_machines(errors: list[str], schemas: dict[str, dict], machines: dict[str, dict]) -> None:
    if not machines:
        return
    organism_states = schemas["organism"]["properties"]["state"]["enum"]
    cell_states = schemas["cell"]["properties"]["lifecycle"]["properties"]["state"]["enum"]
    if organism_states != machines["organism"]["states"]:
        fail(errors, "organism.schema.json state enum differs from state-machines.yaml")
    if cell_states != machines["cell"]["states"]:
        fail(errors, "cell.schema.json lifecycle.state enum differs from state-machines.yaml")
    if set(schemas["lifecycle-transition"]["properties"]["entity_type"]["enum"]) != set(machines):
        fail(errors, "lifecycle-transition entity_type enum differs from machine names")

    for diagram, machine_name in DIAGRAM_MACHINES.items():
        path = ROOT / "diagrams" / f"{diagram}.md"
        if not path.is_file():
            continue
        block = MERMAID_BLOCK.findall(path.read_text(encoding="utf-8"))
        if len(block) != 1:
            continue
        edges = {m.groups() for line in block[0].splitlines() if (m := EDGE.match(line))}
        expected = {(t["from"], t["to"]) for t in machines[machine_name]["transitions"]}
        if edges != expected:
            fail(errors, f"diagram {diagram}.md edges differ from machine {machine_name}: "
                         f"missing {sorted(expected - edges)}, extra {sorted(edges - expected)}")

    doc = text_of("docs/LIFECYCLE.md")
    for machine_name in machines:
        for transition in machines[machine_name]["transitions"]:
            row = f"| `{transition['from']}` | `{transition['to']}` | {transition['guard']} | {transition['authority']} | {transition['timeout']} |"
            if row not in doc:
                fail(errors, f"LIFECYCLE.md lacks transition row for {machine_name}: {transition['from']}->{transition['to']}")

    for path in sorted((ROOT / "reference/examples/valid").glob("lifecycle-transition--*.yaml")):
        example = yaml.safe_load(path.read_text(encoding="utf-8"))
        edges = {(t["from"], t["to"]) for t in machines[example["entity_type"]]["transitions"]}
        if (example["from"], example["to"]) not in edges:
            fail(errors, f"{path.name}: transition {example['from']}->{example['to']} not allowed by machine")


def parse_mapping(errors: list[str]) -> dict[str, list[str]]:
    text = text_of("docs/BIOLOGY_TO_IT_MAPPING.md")
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = re.match(r"^\| ([A-Z]-\d{2}) \|", line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split(" | ")]
        row_id = match.group(1)
        if row_id in rows and len(cells) == MAPPING_COLUMNS:
            fail(errors, f"duplicate mapping id: {row_id}")
        rows.setdefault(row_id, cells)
    main_rows = {k: v for k, v in rows.items() if len(v) == MAPPING_COLUMNS}
    for row_id, cells in main_rows.items():
        for index, cell in enumerate(cells):
            if not cell:
                fail(errors, f"mapping {row_id}: empty column {index + 1}")
        if cells[11] not in PROFILES:
            fail(errors, f"mapping {row_id}: unknown Profile {cells[11]!r}")
    if len(main_rows) < 100:
        fail(errors, f"expected at least 100 mechanism rows, found {len(main_rows)}")
    appendix = re.findall(r"^\| ([A-Z]-\d{2}) \| [^|]+ \| [^|]+ \|$", text, re.M)
    if set(appendix) != set(main_rows):
        fail(errors, f"Appendix A ids differ from matrix: missing {sorted(set(main_rows) - set(appendix))}")
    for term in sorted(REQUIRED_MAPPING_TERMS):
        if term not in text:
            fail(errors, f"required mapping term missing: {term}")
    coverage = text.split("## Приложение B.", 1)[1].split("## Приложение C.", 1)[0]
    for ref in MECHANISM_ID.findall(coverage):
        if ref not in main_rows:
            fail(errors, f"coverage appendix references unknown id {ref}")
    if len(MECHANISM_ID.findall(coverage)) < 50:
        fail(errors, "coverage appendix is too small")
    return main_rows


def validate_requirements(errors: list[str], mapping: dict[str, list[str]]) -> None:
    registry = yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]
    ids = [item["id"] for item in registry]
    if len(ids) != len(set(ids)):
        fail(errors, "duplicate requirement ids")
    referenced: set[str] = set()
    for item in registry:
        match = re.fullmatch(r"REQ-(CORE|DIST|ADPT|EMB|COND)-(\d{2})", item["id"])
        if not match or REQ_PREFIX.get(item["profile"]) != match.group(1):
            fail(errors, f"requirement {item['id']} does not match profile {item['profile']}")
        if item["verification"] not in {"schema", "test", "inspection"}:
            fail(errors, f"requirement {item['id']}: bad verification {item['verification']}")
        for key in ("title", "statement", "evidence", "mappings"):
            if not item.get(key):
                fail(errors, f"requirement {item['id']}: missing {key}")
        for ref in item["mappings"]:
            referenced.add(ref)
            if ref not in mapping:
                fail(errors, f"requirement {item['id']} references unknown mechanism {ref}")
    for row_id, cells in sorted(mapping.items()):
        if cells[11] != "Pattern" and row_id not in referenced:
            fail(errors, f"normative mapping row {row_id} ({cells[11]}) is not covered by any requirement")

    doc = text_of("docs/CONFORMANCE.md")
    doc_rows = dict(re.findall(r"^\| (REQ-[A-Z]+-\d{2}) \| (\w+) \|", doc, re.M))
    if doc_rows != {item["id"]: item["profile"] for item in registry}:
        fail(errors, "docs/CONFORMANCE.md requirement table differs from specifications/requirements.yaml")
    template = text_of("templates/DOA_CONFORMANCE_CLAIM.md")
    for rid in ids:
        if rid not in template:
            fail(errors, f"claim template lacks {rid}")


def validate_failure_classes(errors: list[str], mapping: dict[str, list[str]]) -> None:
    """specifications/failure-classes.yaml is the machine-readable twin of the table in FAILURE_AND_RECOVERY.md."""
    registry = yaml.safe_load(text_of("specifications/failure-classes.yaml"))["failure_classes"]
    ids = [item["id"] for item in registry]
    expected = [f"F-{number:02d}" for number in range(1, len(ids) + 1)]
    if ids != expected:
        fail(errors, f"failure-classes.yaml ids must be {expected[0]}..{expected[-1]} without gaps or duplicates")
    keys = ("id", "title", "detection", "containment", "recovery", "verification", "mechanisms")
    for item in registry:
        for key in keys:
            if not item.get(key):
                fail(errors, f"failure class {item.get('id')}: missing {key}")
        for ref in item.get("mechanisms", []):
            if ref not in mapping:
                fail(errors, f"failure class {item['id']} references unknown mechanism {ref}")
    doc = text_of("docs/FAILURE_AND_RECOVERY.md").split("## 2. Реестр классов отказа")[1].split("\n## 3.")[0]
    table = {}
    for line in doc.splitlines():
        if re.match(r"\| F-\d{2} \|", line):
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            table[cells[0]] = cells
    from_registry = {
        item["id"]: [item["id"], item["title"], item["detection"], item["containment"], item["recovery"],
                     item["verification"], ", ".join(item["mechanisms"])]
        for item in registry
    }
    if table != from_registry:
        differing = sorted(set(table) ^ set(from_registry) | {k for k in table.keys() & from_registry.keys() if table[k] != from_registry[k]})
        fail(errors, f"FAILURE_AND_RECOVERY.md table differs from failure-classes.yaml: {differing}")
    statuses = set(json.loads(text_of("specifications/conformance-claim.schema.json"))["properties"]["requirements"]["items"]["properties"]["status"]["enum"])
    conformance = text_of("docs/CONFORMANCE.md")
    for status in sorted(statuses):
        if f"| `{status}` |" not in conformance:
            fail(errors, f"docs/CONFORMANCE.md does not define requirement status {status}")


def validate_claim_checker(errors: list[str]) -> None:
    spec = importlib.util.spec_from_file_location("check_conformance_claim", ROOT / "scripts/check_conformance_claim.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for kind, path in (("valid", "conformance-claim--reference.yaml"), ("invalid", "conformance-claim--verified-with-gaps.yaml")):
        claim = yaml.safe_load((ROOT / "reference/examples" / kind / path).read_text(encoding="utf-8"))
        problems = module.check_claim(claim)
        if kind == "valid" and problems:
            fail(errors, f"claim checker rejects the reference claim: {problems[0]}")
        if kind == "invalid" and not problems:
            fail(errors, "claim checker accepts an invalid claim")
    complete = {
        "standard": "DOA-FS-1.0", "implementation": "x", "owner": "x", "version": "1", "assessment_date": "2026-10-01",
        "status": "VERIFIED", "assurance": "self-assessed", "profiles": ["Core"],
        "scope": {"boundary": "x", "environments": ["x"]}, "assessor": "x", "blocking_gaps": [],
        "requirements": [],
    }
    registry = yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]
    for item in registry:
        if item["profile"] in {"Core", "Conditional"}:
            complete["requirements"].append({"id": item["id"], "status": "PASS", "evidence_ref": "evidence://x"})
    if module.check_claim(complete):
        fail(errors, "claim checker rejects a fully covered Core claim")
    complete["requirements"].pop()
    if not module.check_claim(complete):
        fail(errors, "claim checker accepts a VERIFIED claim with an uncovered requirement")
    designed = copy.deepcopy(complete)
    designed["status"] = "PARTIAL"
    designed["requirements"][0].update({"status": "DESIGNED", "component": "design", "gap_owner": "owner"})
    if module.check_claim(designed):
        fail(errors, "claim checker rejects a PARTIAL claim with a DESIGNED requirement")
    designed["status"] = "VERIFIED"
    if not module.check_claim(designed):
        fail(errors, "claim checker accepts a VERIFIED claim with a DESIGNED requirement")
    classes = copy.deepcopy(complete)
    classes["status"] = "PARTIAL"
    classes["failure_classes"] = [{"id": "F-99", "status": "NOT_ASSESSED"}]
    if not any("unknown failure class" in problem for problem in module.check_claim(classes)):
        fail(errors, "claim checker accepts an unknown failure class id")
    classes["failure_classes"] = [{"id": "F-01", "status": "PASS", "evidence_ref": "evidence://x"}]
    if not any("not covered" in problem for problem in module.check_claim(classes)):
        fail(errors, "claim checker accepts REQ-CORE-23 PASS with uncovered failure classes")
    mutable = copy.deepcopy(complete)
    mutable["requirements"][0]["evidence_ref"] = "https://example.org/o/r/blob/main/README.md"
    if not module.evidence_warnings(mutable):
        fail(errors, "claim checker does not warn about a mutable evidence_ref")
    if module.evidence_warnings(complete):
        fail(errors, "claim checker warns about a valid evidence_ref")


def validate_markdown(errors: list[str], mapping_ids: set[str]) -> None:
    requirement_ids = {item["id"] for item in yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]}
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        in_fence, table_width = False, None
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.endswith((" ", "\t")):
                fail(errors, f"trailing whitespace: {relative}:{line_number}")
            if re.search(r"\b(TODO|TBD|FIXME)\b", line):
                fail(errors, f"unfinished marker: {relative}:{line_number}")
            if line.startswith("```"):
                in_fence = not in_fence
                table_width = None
                continue
            if in_fence:
                continue
            if line.startswith("|"):
                width = len(re.split(r"(?<!\\)\|", line.strip())) - 2
                if table_width is None:
                    table_width = width
                elif width != table_width:
                    fail(errors, f"table column mismatch ({width} vs {table_width}): {relative}:{line_number}")
            else:
                table_width = None
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            local_target = target.split("#", 1)[0]
            if local_target and not (path.parent / local_target).resolve().exists():
                fail(errors, f"broken local link in {relative}: {target}")
        if str(relative) != "docs/BIOLOGY_TO_IT_MAPPING.md":
            for ref in MECHANISM_ID.findall(text):
                if ref not in mapping_ids:
                    fail(errors, f"{relative} references unknown mechanism id {ref}")
        for ref in REQ_ID.findall(text):
            if ref not in requirement_ids:
                fail(errors, f"{relative} references unknown requirement {ref}")


def validate_diagrams(errors: list[str]) -> None:
    found = {p.stem for p in (ROOT / "diagrams").glob("*.md")}
    expected = set(DIAGRAM_MACHINES) | OTHER_DIAGRAMS
    if found != expected:
        fail(errors, f"diagram set mismatch: missing {sorted(expected - found)}, extra {sorted(found - expected)}")
    for path in sorted((ROOT / "diagrams").glob("*.md")):
        blocks = MERMAID_BLOCK.findall(path.read_text(encoding="utf-8"))
        if len(blocks) != 1:
            fail(errors, f"expected one Mermaid block: {path.relative_to(ROOT)}")
        elif not MERMAID_START.search(blocks[0]):
            fail(errors, f"unknown Mermaid diagram start: {path.relative_to(ROOT)}")


def validate_yaml_documents(errors: list[str]) -> None:
    for pattern in ("*.yml", "*.yaml"):
        for path in sorted(ROOT.rglob(pattern)):
            if ".git" in path.parts:
                continue
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                fail(errors, f"invalid YAML {path.relative_to(ROOT)}: {exc}")


def validate_versions(errors: list[str]) -> None:
    version = text_of("VERSION").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(errors, f"VERSION is not semver: {version!r}")
        return
    short = ".".join(version.split(".")[:2])
    readme = text_of("README.md")
    if f"**Version:** {version}" not in readme:
        fail(errors, f"README.md must state **Version:** {version}")
    standard = text_of("docs/DOA_STANDARD_v1.0.md")
    if f"**Версия релиза:** v{version}" not in standard or "`DOA-FS-1.0`" not in standard:
        fail(errors, "canonical standard must state release v%s and DOA-FS-1.0" % version)
    changelog = text_of("CHANGELOG.md")
    first = re.search(r"^## \[([^\]]+)\]", changelog, re.M)
    if not first or first.group(1) != version:
        fail(errors, f"CHANGELOG.md top release must be [{version}], found {first.group(1) if first else None}")
    if f"DOA v{short}" not in readme and f"v{short}" not in readme:
        fail(errors, f"README.md must reference DOA v{short}")
    readiness = text_of("docs/RELEASE_READINESS_v1.0.md")
    if f"v{version}" not in readiness or "ГОТОВО" not in readiness:
        fail(errors, "RELEASE_READINESS must reference the release version and a final ГОТОВО status")
    for relative in STALE_CHECKED:
        for number, line in enumerate(text_of(relative).splitlines(), start=1):
            if STALE.search(line):
                fail(errors, f"stale pre-release wording in {relative}:{number}: {line.strip()[:80]}")
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".json", ".yaml", ".yml"}:
            if "DOA-FS-1.1" in path.read_text(encoding="utf-8") or "DOA-FS-0" in path.read_text(encoding="utf-8"):
                fail(errors, f"conflicting standard identifier in {path.relative_to(ROOT)}")
    holders = [p.name for p in (ROOT / "docs").glob("*.md") if "HomeostaticSignal" in p.read_text(encoding="utf-8")]
    if set(holders) - {"DOA_STANDARD_v1.0.md", "TERMINOLOGY.md"}:
        fail(errors, f"HomeostaticSignal used outside terminology/standard: {holders}")


def validate_workflow(errors: list[str]) -> None:
    workflow = yaml.safe_load(text_of(".github/workflows/validate.yml"))
    if workflow.get("permissions") != {"contents": "read"}:
        fail(errors, "workflow permissions must be exactly contents: read")
    for step in workflow["jobs"]["validate"]["steps"]:
        action = step.get("uses")
        if action and not re.fullmatch(r"[\w.-]+/[\w./-]+@[0-9a-f]{40}", action):
            fail(errors, f"workflow action must be pinned to a full commit SHA: {action}")
    steps = " ".join(str(s.get("run", "")) for s in workflow["jobs"]["validate"]["steps"])
    if "scripts/validate_repository.py" not in steps:
        fail(errors, "workflow must run scripts/validate_repository.py")


def validate_canonical_terms(errors: list[str]) -> None:
    if "метаархитектурный стандарт" not in text_of("README.md"):
        fail(errors, "README must define DOA as a meta-architecture standard")
    if "DOA — метаархитектурный стандарт" not in text_of("docs/DOA_STANDARD_v1.0.md"):
        fail(errors, "canonical terminology missing from DOA standard")
    if "Apache License" not in text_of("LICENSE"):
        fail(errors, "LICENSE is not recognizable as Apache License")


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    schemas = load_schemas(errors)
    machines: dict[str, dict] = {}
    mapping: dict[str, list[str]] = {}
    try:
        machines = load_machines(errors)
        mapping = parse_mapping(errors)
    except (OSError, KeyError, yaml.YAMLError) as exc:
        fail(errors, f"cannot load core registries: {exc}")
    if schemas:
        validate_examples(errors, schemas)
        validate_state_machines(errors, schemas, machines)
    if mapping:
        validate_requirements(errors, mapping)
        validate_failure_classes(errors, mapping)
    try:
        validate_claim_checker(errors)
    except Exception as exc:  # aggregate
        fail(errors, f"claim checker validation failed: {exc}")
    validate_yaml_documents(errors)
    validate_markdown(errors, set(mapping))
    validate_diagrams(errors)
    validate_versions(errors)
    validate_workflow(errors)
    validate_canonical_terms(errors)

    if errors:
        print("DOA repository validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    requirements = yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]
    print("DOA repository validation: PASS")
    print(f"- required files: {len(REQUIRED_FILES)}")
    print(f"- schemas: {len(schemas)} (each with valid and invalid examples)")
    print(f"- state machines: {len(machines)} (schemas, diagrams and LIFECYCLE.md consistent)")
    print(f"- Biology-to-IT mechanisms: {len(mapping)} (12 columns, all normative rows traced to requirements)")
    print(f"- conformance requirements: {len(requirements)}")
    print("- Markdown links, tables, whitespace and cross-references: valid")
    print(f"- Mermaid documents: {len(DIAGRAM_MACHINES) + len(OTHER_DIAGRAMS)}")
    print(f"- version: {text_of('VERSION').strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
