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
    "verification-report",
}

REQUIRED_FILES = {
    ".gitattributes", ".gitignore", ".github/CODEOWNERS", ".github/dependabot.yml", ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/standard-gap.yml", ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/application-report.yml", ".github/ISSUE_TEMPLATE/bug-report.yml",
    ".github/ISSUE_TEMPLATE/config.yml", ".github/ISSUE_TEMPLATE/question.yml",
    "CHANGELOG.md", "CHANGES_AND_NEW_FINDINGS.md", "CITATION.cff", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "GOVERNANCE.md",
    "LICENSE", "README.md", "ROADMAP.md", "SECURITY.md", "SUPPORT.md", "VERSION",
    "docs/ARCHITECTURE.md", "docs/BIOLOGY_TO_IT_MAPPING.md", "docs/BOUNDARY_AND_IDENTITY.md", "docs/CONFORMANCE.md",
    "docs/DOA_STANDARD_v1.0.md", "docs/FAILURE_AND_RECOVERY.md", "docs/GENOME_AND_EVOLUTION.md", "docs/HOMEOSTASIS.md",
    "docs/IMPLEMENTATION_GUIDE.md", "docs/README.md", "docs/VERIFICATION_KIT.md",
    "docs/LIFECYCLE.md", "docs/MEMORY_AND_NERVOUS_SYSTEM.md", "docs/METABOLISM.md", "docs/PRINCIPLES.md",
    "docs/RELEASE_READINESS_v1.0.md", "docs/ROBOTICS_EXTENSION.md", "docs/SECURITY_AND_IMMUNITY.md", "docs/SOURCES.md",
    "docs/TERMINOLOGY.md",
    "reference/EXAMPLE_GENOME.yaml", "reference/REFERENCE_ARCHITECTURE.md", "reference/REFERENCE_STACK.md",
    "requirements-validation.txt", "scripts/check_conformance_claim.py", "scripts/check_verification_report.py",
    "scripts/validate_repository.py",
    "specifications/failure-classes.yaml", "specifications/requirements.yaml", "specifications/state-machines.yaml",
    "templates/DOA_CONFORMANCE_CLAIM.md", "templates/DOA_HAZARD_ANALYSIS.md", "templates/DOA_THREAT_MODEL.md",
    "profiles/README.md", "profiles/modular-monolith.md", "profiles/modular-monolith.yaml",
    "profiles/kubernetes-event-streaming.md", "profiles/kubernetes-event-streaming.yaml",
    "verification/conformance-test-plan.yaml", "verification/fault-scenarios.yaml",
    "verification/otel-semantic-conventions.yaml",
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
MAX_PATH_NODES = 10

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
        text = path.read_text(encoding="utf-8")
        blocks = MERMAID_BLOCK.findall(text)
        full = [b for b in blocks if b.lstrip().startswith("stateDiagram")]
        simple = [b for b in blocks if b.lstrip().startswith("flowchart TD")]
        if len(blocks) != 2 or len(full) != 1 or len(simple) != 1:
            continue
        edges = {m.groups() for line in full[0].splitlines() if (m := EDGE.match(line))}
        expected = {(t["from"], t["to"]) for t in machines[machine_name]["transitions"]}
        if edges != expected:
            fail(errors, f"diagram {diagram}.md edges differ from machine {machine_name}: "
                         f"missing {sorted(expected - edges)}, extra {sorted(edges - expected)}")
        path_edges = {m.groups() for line in simple[0].splitlines() if (m := EDGE.match(line))}
        if not path_edges <= expected:
            fail(errors, f"diagram {diagram}.md main path has transitions absent from machine {machine_name}: "
                         f"{sorted(path_edges - expected)}")
        path_nodes = {state for edge in path_edges for state in edge}
        if len(path_nodes) > MAX_PATH_NODES:
            fail(errors, f"diagram {diagram}.md main path has {len(path_nodes)} nodes, at most {MAX_PATH_NODES} stay readable")
        section = text.split("## Что значит каждое состояние")
        if len(section) != 2:
            fail(errors, f"diagram {diagram}.md lacks the state meaning table")
        else:
            listed = re.findall(r"^\| `([A-Z_]+)` \|", section[1].split("\n## ")[0], re.M)
            if sorted(listed) != sorted(machines[machine_name]["states"]):
                fail(errors, f"diagram {diagram}.md state table differs from machine {machine_name}: "
                             f"{sorted(set(listed) ^ set(machines[machine_name]['states']))}")

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
    claim_schema = json.loads(text_of("specifications/conformance-claim.schema.json"))
    if "observed_accounting" not in claim_schema["properties"]:
        fail(errors, "conformance-claim.schema.json lacks observed_accounting (REQ-CORE-18)")
    for relative in ("docs/CONFORMANCE.md", "docs/METABOLISM.md", "templates/DOA_CONFORMANCE_CLAIM.md"):
        if "observed_accounting" not in text_of(relative):
            fail(errors, f"{relative} must mention the claim field observed_accounting")
    statuses = set(claim_schema["properties"]["requirements"]["items"]["properties"]["status"]["enum"])
    conformance = text_of("docs/CONFORMANCE.md")
    for status in sorted(statuses):
        if f"| `{status}` |" not in conformance:
            fail(errors, f"docs/CONFORMANCE.md does not define requirement status {status}")


CASE_ID = re.compile(r"TC-(CORE|DIST|ADPT|EMB|COND)-(\d{2})-(\d{2})")
SCENARIO_CATEGORIES = {"cell": "CELL", "organ": "ORGAN", "circulation": "CIRC", "organism": "ORG"}
OTEL_NAME = re.compile(r"doa(\.[a-z][a-z0-9_]*)+")
OTEL_EVENT_NAME = re.compile(r"doa(\.(?:[a-z][a-z0-9_]*|\{entity_type\}))+\.v\d+")
OTEL_ATTRIBUTE_TYPES = {"string", "int", "double", "boolean"}
OTEL_INSTRUMENTS = {"counter", "updowncounter", "gauge", "histogram"}
OTEL_REQUIREMENT_LEVELS = {"required", "recommended", "opt_in"}
RECOVERY_MODES = {"RESTART", "RESTORE", "REPAIR", "REPLACE", "REGENERATE", "REBUILD", "RECONFIGURE", "ROLLBACK"}


def validate_verification_kit(errors: list[str], machines: dict[str, dict]) -> None:
    """Verification Kit registries (informative) must stay consistent with the normative registries they reference."""
    requirements = {item["id"]: item for item in yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]}
    failure_ids = {item["id"] for item in yaml.safe_load(text_of("specifications/failure-classes.yaml"))["failure_classes"]}
    plan = yaml.safe_load(text_of("verification/conformance-test-plan.yaml"))
    catalog = yaml.safe_load(text_of("verification/fault-scenarios.yaml"))
    semconv = yaml.safe_load(text_of("verification/otel-semantic-conventions.yaml"))
    version = text_of("VERSION").strip()
    short = ".".join(version.split(".")[:2])
    for name, document, key in (("conformance-test-plan.yaml", plan, "plan_version"), ("fault-scenarios.yaml", catalog, "kit_version")):
        if document.get("standard") != "DOA-FS-1.0":
            fail(errors, f"verification/{name}: standard must be DOA-FS-1.0")
        if ".".join(str(document.get(key, "")).split(".")[:2]) != short:
            fail(errors, f"verification/{name}: {key} must have the same major.minor as VERSION ({short})")
    if plan.get("plan_version") != catalog.get("kit_version"):
        fail(errors, "plan_version and kit_version must be equal")

    scenarios = {}
    for item in catalog["scenarios"]:
        scenario_id = item.get("id", "<missing>")
        if scenario_id in scenarios:
            fail(errors, f"duplicate scenario id {scenario_id}")
        scenarios[scenario_id] = item
        prefix = SCENARIO_CATEGORIES.get(item.get("category"))
        if prefix is None or not re.fullmatch(rf"FS-{prefix}-\d{{2}}", scenario_id):
            fail(errors, f"scenario {scenario_id}: id does not match category {item.get('category')}")
        for key in ("title", "fault", "steady_state", "abort_conditions", "blast_radius"):
            if not item.get(key):
                fail(errors, f"scenario {scenario_id}: missing {key}")
        if item.get("minimum_environment") not in {"isolated", "staging"}:
            fail(errors, f"scenario {scenario_id}: minimum_environment must be isolated or staging")
        expected = item.get("expected") or {}
        for key in ("detection", "containment", "recovery", "verification"):
            if not expected.get(key):
                fail(errors, f"scenario {scenario_id}: expected.{key} is missing")
        if not item.get("failure_classes"):
            fail(errors, f"scenario {scenario_id}: failure_classes is empty")
        for ref in item.get("failure_classes", []):
            if ref not in failure_ids:
                fail(errors, f"scenario {scenario_id} references unknown failure class {ref}")
        for ref in item.get("requirements", []):
            if ref not in requirements:
                fail(errors, f"scenario {scenario_id} references unknown requirement {ref}")
    for category in SCENARIO_CATEGORIES:
        if not any(item.get("category") == category for item in scenarios.values()):
            fail(errors, f"fault-scenarios.yaml has no scenario of category {category}")

    cases = {}
    for item in plan["cases"]:
        case_id = item.get("id", "<missing>")
        if case_id in cases:
            fail(errors, f"duplicate test case id {case_id}")
        cases[case_id] = item
        match = CASE_ID.fullmatch(case_id)
        requirement = requirements.get(item.get("requirement"))
        if requirement is None:
            fail(errors, f"test case {case_id} references unknown requirement {item.get('requirement')}")
            continue
        if not match or item["requirement"] != f"REQ-{match.group(1)}-{match.group(2)}":
            fail(errors, f"test case {case_id} id does not match requirement {item['requirement']}")
        if item.get("method") != requirement["verification"]:
            fail(errors, f"test case {case_id}: method {item.get('method')} differs from verification {requirement['verification']} of {item['requirement']}")
        for key in ("title", "procedure", "pass_criteria", "evidence"):
            if not item.get(key):
                fail(errors, f"test case {case_id}: missing {key}")
        if "isolated_environment" in item and not isinstance(item["isolated_environment"], bool):
            fail(errors, f"test case {case_id}: isolated_environment must be boolean")
        for ref in item.get("scenarios", []):
            if ref not in scenarios:
                fail(errors, f"test case {case_id} references unknown scenario {ref}")
            elif scenarios[ref]["minimum_environment"] == "isolated" and not item.get("isolated_environment"):
                fail(errors, f"test case {case_id} uses isolated scenario {ref} but is not marked isolated_environment")
    for rid in requirements:
        if not any(item.get("requirement") == rid for item in cases.values()):
            fail(errors, f"requirement {rid} has no test case in the plan")

    coverage = catalog.get("coverage") or {}
    if set(coverage) != failure_ids:
        fail(errors, f"fault-scenarios.yaml coverage must list exactly the failure classes: differs by {sorted(set(coverage) ^ failure_ids)}")
    listed: dict[str, set[str]] = {}
    for class_id, entry in coverage.items():
        covering = entry.get("scenarios", [])
        test_cases = entry.get("test_cases", [])
        if not covering and not test_cases:
            fail(errors, f"coverage of {class_id} names neither scenarios nor test cases")
        if test_cases and not entry.get("reason"):
            fail(errors, f"coverage of {class_id} by test cases needs a reason")
        for ref in covering:
            listed.setdefault(ref, set()).add(class_id)
            if ref not in scenarios:
                fail(errors, f"coverage of {class_id} references unknown scenario {ref}")
            elif class_id not in scenarios[ref].get("failure_classes", []):
                fail(errors, f"coverage of {class_id} lists {ref}, whose failure_classes do not include it")
        for ref in test_cases:
            if ref not in cases:
                fail(errors, f"coverage of {class_id} references unknown test case {ref}")
    for scenario_id, item in scenarios.items():
        missing = set(item.get("failure_classes", [])) - listed.get(scenario_id, set())
        if missing:
            fail(errors, f"scenario {scenario_id} is not listed in coverage of {sorted(missing)}")

    validate_semantic_conventions(errors, semconv, machines, requirements, failure_ids, scenarios)
    validate_report_checker(errors)


def schema_path_values(relative: str, path: list[str]) -> list | None:
    node = json.loads(text_of(relative))
    for part in path:
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, list) else None


def validate_semantic_conventions(errors, semconv, machines, requirements, failure_ids, scenarios) -> None:
    attributes = {}
    for item in semconv["attributes"]:
        name = item.get("name", "<missing>")
        if not OTEL_NAME.fullmatch(name):
            fail(errors, f"otel attribute {name}: invalid name")
        if name in attributes:
            fail(errors, f"duplicate otel attribute {name}")
        attributes[name] = item
        if item.get("type") not in OTEL_ATTRIBUTE_TYPES:
            fail(errors, f"otel attribute {name}: bad type {item.get('type')}")
        for key in ("brief", "source"):
            if not item.get(key):
                fail(errors, f"otel attribute {name}: missing {key}")
        if not isinstance(item.get("metric_safe"), bool):
            fail(errors, f"otel attribute {name}: metric_safe must be boolean")
        source_file = item.get("source", "").split("#")[0].split(",")[0].strip()
        if source_file.startswith(("specifications/", "verification/", "docs/")) and not (ROOT / source_file).is_file():
            fail(errors, f"otel attribute {name}: source file does not exist: {source_file}")
        origin = item.get("values_from")
        if origin and "values" in item:
            fail(errors, f"otel attribute {name}: use either values or values_from")
        if origin:
            if origin["kind"] == "schema-enum":
                values = schema_path_values(origin["file"], origin["path"])
                if not values:
                    fail(errors, f"otel attribute {name}: values_from path does not resolve to an enum")
                elif name == "doa.lifecycle.entity_type" and set(values) != set(machines):
                    fail(errors, f"otel attribute {name}: enum {sorted(values)} differs from state machines {sorted(machines)}")
                elif name == "doa.recovery.mode" and set(values) != RECOVERY_MODES:
                    fail(errors, f"otel attribute {name}: enum differs from the recovery taxonomy")
            elif origin["kind"] not in {"failure-classes", "fault-scenarios"}:
                fail(errors, f"otel attribute {name}: unknown values_from kind {origin['kind']}")
        elif name not in {"doa.organism.id", "doa.organ.id", "doa.cell.id", "doa.cell.type", "doa.cell.tissue", "doa.epoch"} and "values" not in item \
                and item.get("type") == "string" and not name.endswith((".id", ".entity_id", ".authority", ".from", ".to")):
            fail(errors, f"otel attribute {name}: enumerated attribute lacks values or values_from")
    if RECOVERY_MODES != set(re.findall(r"^\| `([A-Z]+)` \|", text_of("docs/FAILURE_AND_RECOVERY.md").split("## 2.")[0], re.M)):
        fail(errors, "recovery taxonomy in FAILURE_AND_RECOVERY.md differs from the expected set of modes")

    event_type = json.loads(text_of("specifications/event.schema.json"))["properties"]["type"]["pattern"]
    for item in semconv["events"]:
        name = item.get("name", "<missing>")
        if not OTEL_EVENT_NAME.fullmatch(name):
            fail(errors, f"otel event {name}: invalid name")
        expansions = [name.replace("{entity_type}", entity) for entity in sorted(machines)] if "{entity_type}" in name else [name]
        for expanded in expansions:
            if not re.search(event_type, expanded):
                fail(errors, f"otel event {expanded} does not satisfy the EventEnvelope type pattern")
        if "{entity_type}" in name and name != "doa.lifecycle.{entity_type}.transitioned.v1":
            fail(errors, "templated otel event must be doa.lifecycle.{entity_type}.transitioned.v1")
        for ref in item.get("attributes", []):
            if ref["ref"] not in attributes:
                fail(errors, f"otel event {name} references unknown attribute {ref['ref']}")
            if ref["requirement_level"] not in OTEL_REQUIREMENT_LEVELS:
                fail(errors, f"otel event {name}: bad requirement_level {ref['requirement_level']}")
        for ref in item.get("requirements", []):
            if ref not in requirements:
                fail(errors, f"otel event {name} references unknown requirement {ref}")
    if not any(item["name"] == "doa.lifecycle.{entity_type}.transitioned.v1" for item in semconv["events"]):
        fail(errors, "otel registry must define the lifecycle transition event")

    metrics = {}
    for item in semconv["metrics"]:
        name = item.get("name", "<missing>")
        if not OTEL_NAME.fullmatch(name):
            fail(errors, f"otel metric {name}: invalid name")
        if name in metrics or name in attributes:
            fail(errors, f"otel metric {name}: duplicate or collides with an attribute name")
        metrics[name] = item
        if item.get("instrument") not in OTEL_INSTRUMENTS:
            fail(errors, f"otel metric {name}: bad instrument {item.get('instrument')}")
        if not item.get("unit") or not item.get("brief"):
            fail(errors, f"otel metric {name}: missing unit or brief")
        for ref in item.get("attributes", []):
            if ref not in attributes:
                fail(errors, f"otel metric {name} references unknown attribute {ref}")
            elif not attributes[ref].get("metric_safe"):
                fail(errors, f"otel metric {name} uses unbounded-cardinality attribute {ref}")
        for ref in item.get("requirements", []):
            if ref not in requirements:
                fail(errors, f"otel metric {name} references unknown requirement {ref}")


def validate_report_checker(errors: list[str]) -> None:
    spec = importlib.util.spec_from_file_location("check_verification_report", ROOT / "scripts/check_verification_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = yaml.safe_load(text_of("reference/examples/valid/verification-report--reference.yaml"))
    problems, _ = module.check_report(report)
    if problems:
        fail(errors, f"report checker rejects the reference report: {problems[0]}")
        return
    mutations = {
        "unknown case id": lambda r: r["results"].append({"case": "TC-CORE-99-01", "status": "SKIPPED", "justification": "x"}),
        "duplicate case id": lambda r: r["results"].append(dict(r["results"][0])),
        "PASS without PASS scenario": lambda r: r["scenario_results"].__setitem__(0, dict(r["scenario_results"][0], status="FAIL")),
        "isolated case in staging": lambda r: r["environment"].__setitem__("type", "staging"),
    }
    for label, mutate in mutations.items():
        broken = copy.deepcopy(report)
        mutate(broken)
        if not module.check_report(broken)[0]:
            fail(errors, f"report checker accepts a report with {label}")
    claim = {"requirements": [{"id": "REQ-CORE-16", "status": "PASS"}]}
    if not module.check_report(report, claim)[0]:
        fail(errors, "report checker does not flag a PASS claim requirement whose case FAILED")


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
        text = path.read_text(encoding="utf-8")
        blocks = MERMAID_BLOCK.findall(text)
        expected_blocks = 2 if path.stem in DIAGRAM_MACHINES else 1
        if len(blocks) != expected_blocks:
            fail(errors, f"expected {expected_blocks} Mermaid block(s): {path.relative_to(ROOT)}")
        for block in blocks:
            if not MERMAID_START.search(block):
                fail(errors, f"unknown Mermaid diagram start: {path.relative_to(ROOT)}")
        if "## Простыми словами" not in text:
            fail(errors, f"diagram page lacks the plain-language section: {path.relative_to(ROOT)}")


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
    released = [name for name in re.findall(r"^## \[([^\]]+)\]", changelog, re.M) if name != "Unreleased"]
    if not released or released[0] != version:
        fail(errors, f"CHANGELOG.md top release must be [{version}], found {released[0] if released else None}")
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


COMMUNITY_LINKS = ("CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md", "LICENSE", "docs/README.md")


def validate_community_files(errors: list[str]) -> None:
    """GitHub community-standard files: citation metadata, issue forms and links from the README."""
    citation = yaml.safe_load(text_of("CITATION.cff"))
    for key in ("cff-version", "message", "title", "authors", "version", "date-released", "license", "repository-code"):
        if not citation.get(key):
            fail(errors, f"CITATION.cff: missing {key}")
    if str(citation.get("version")) != text_of("VERSION").strip():
        fail(errors, "CITATION.cff version differs from VERSION")
    readme = text_of("README.md")
    for link in COMMUNITY_LINKS:
        if f"]({link})" not in readme:
            fail(errors, f"README.md must link to {link}")
    forms = sorted(p for p in (ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml") if p.name != "config.yml")
    if len(forms) < 4:
        fail(errors, "expected at least four issue forms")
    for path in forms:
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        relative = path.relative_to(ROOT)
        for key in ("name", "description", "body"):
            if not form.get(key):
                fail(errors, f"issue form {relative}: missing {key}")
        ids = [item["id"] for item in form.get("body", []) if "id" in item]
        if len(ids) != len(set(ids)) or not any(item.get("type") != "markdown" for item in form.get("body", [])):
            fail(errors, f"issue form {relative}: needs unique ids and at least one input")
    config = yaml.safe_load(text_of(".github/ISSUE_TEMPLATE/config.yml"))
    if config.get("blank_issues_enabled") is not False or not config.get("contact_links"):
        fail(errors, "issue template config must disable blank issues and list contact links")
    for link in config.get("contact_links", []):
        if not str(link.get("url", "")).startswith("https://github.com/Alpha-Oi/digital-organism-architecture/"):
            fail(errors, f"issue template contact link must point to this repository: {link.get('url')}")


PROFILE_APPLICABILITY = {"applicable": "да", "applicable-with-limits": "да, с пределом"}
PROFILES_COVERAGE = {
    "modular-monolith": {"Core", "Conditional"},
    "kubernetes-event-streaming": {"Core", "Distributed", "Conditional"},
}
PROFILE_SECTIONS = (
    "## Простыми словами", "## Термины профиля", "## Когда выбирать и когда нет", "## Как DOA выглядит в ",
    "## Главный риск", "## Что можно заявить", "## Состав приложения", "## Требования по пунктам", "## Как проверять",
    "## Порядок внедрения", "## Ограничения профиля",
)


def validate_profiles(errors: list[str]) -> None:
    """Implementation profiles (informative): coverage of requirements, test-plan references and the mirrored tables."""
    requirements = {item["id"]: item for item in yaml.safe_load(text_of("specifications/requirements.yaml"))["requirements"]}
    cases = {case["id"]: case for case in yaml.safe_load(text_of("verification/conformance-test-plan.yaml"))["cases"]}
    index = text_of("profiles/README.md")
    for name, covered_profiles in PROFILES_COVERAGE.items():
        profile = yaml.safe_load(text_of(f"profiles/{name}.yaml"))
        if profile.get("standard") != "DOA-FS-1.0" or profile.get("status") != "informative" or profile.get("profile") != name:
            fail(errors, f"profiles/{name}.yaml: standard must be DOA-FS-1.0, status informative, profile {name}")
        expected = [rid for rid, item in requirements.items() if item["profile"] in covered_profiles]
        listed = [item["id"] for item in profile["requirements"]]
        if sorted(listed) != sorted(expected) or len(listed) != len(set(listed)):
            fail(errors, f"profile {name} must cover {sorted(covered_profiles)} exactly once: differs by {sorted(set(listed) ^ set(expected))}")
        rows = []
        for item in profile["requirements"]:
            rid = item["id"]
            if item.get("applicability") not in PROFILE_APPLICABILITY:
                fail(errors, f"profile {name} {rid}: bad applicability {item.get('applicability')}")
                continue
            if not item.get("approach"):
                fail(errors, f"profile {name} {rid}: missing approach")
            if item["applicability"] == "applicable-with-limits" and not item.get("limit"):
                fail(errors, f"profile {name} {rid}: applicable-with-limits needs a limit")
            if not item.get("evidence_cases"):
                fail(errors, f"profile {name} {rid}: missing evidence_cases")
            for case_id in item.get("evidence_cases", []):
                if case_id not in cases or cases[case_id]["requirement"] != rid:
                    fail(errors, f"profile {name} {rid}: evidence case {case_id} is unknown or belongs to another requirement")
            if rid in requirements:
                rows.append(f"| `{rid}` {requirements[rid]['title']} | {PROFILE_APPLICABILITY[item['applicability']]} | {item['approach']} | "
                            f"{item.get('limit') or '—'} | {', '.join(item.get('evidence_cases', []))} |")
        document = text_of(f"profiles/{name}.md")
        for row in rows:
            if row not in document:
                fail(errors, f"profiles/{name}.md table differs from the registry: {row[:60]}")
        for section in PROFILE_SECTIONS:
            if section not in document:
                fail(errors, f"profiles/{name}.md lacks section {section}")
        if f"{name}.md" not in index:
            fail(errors, f"profiles/README.md must list the profile {name}")


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
        validate_verification_kit(errors, machines)
    try:
        validate_claim_checker(errors)
    except Exception as exc:  # aggregate
        fail(errors, f"claim checker validation failed: {exc}")
    validate_yaml_documents(errors)
    validate_markdown(errors, set(mapping))
    validate_diagrams(errors)
    validate_versions(errors)
    validate_workflow(errors)
    validate_community_files(errors)
    validate_profiles(errors)
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
    print("- Verification Kit: test plan, fault scenarios, doa.* conventions and report checker consistent")
    print("- Markdown links, tables, whitespace and cross-references: valid")
    print(f"- Mermaid documents: {len(DIAGRAM_MACHINES) + len(OTHER_DIAGRAMS)}")
    print("- community files: citation, issue forms and README links valid")
    print("- implementation profiles: requirements covered, test cases and tables consistent")
    print(f"- version: {text_of('VERSION').strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
