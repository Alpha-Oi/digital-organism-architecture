"""Automated tests for scripts/validate_repository.py and scripts/new_card.py.

Run from the repository root: python -m unittest discover -s tests -v

Each validator test copies the working tree to a temporary directory, breaks one thing there and checks that the validator fails with
the expected message, so a later edit that silently weakens a check turns into a failing test. The original tree is never modified.
Run the tests on a clean checkout: a local `.env` file or `__pycache__` folder is copied too and fails the baseline test.
Only the standard library is used besides PyYAML, which the validator already needs.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the validator rejects __pycache__ in the tree

import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CARD = "mechanisms/cards/atp-synthase.md"
SENESCENCE_CARD = "mechanisms/cards/senescence-and-fibrosis-brake.md"


def run_script(tree: Path, script: str, *args: str) -> tuple[int, str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    done = subprocess.run(
        [sys.executable, "-B", str(tree / script), *args], capture_output=True, text=True, env=env, cwd=tree, timeout=180
    )
    return done.returncode, done.stdout + done.stderr


class TreeCase(unittest.TestCase):
    """A private copy of the repository for one test."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tree = Path(tmp.name) / "repo"
        shutil.copytree(ROOT, self.tree, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))

    def edit(self, relative: str, old: str, new: str, count: int = 1) -> None:
        path = self.tree / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"{relative}: the text to break was not found, the test needs an update")
        path.write_text(text.replace(old, new, count), encoding="utf-8")

    def edit_graph(self, change) -> None:
        path = self.tree / "mechanisms/interaction-graph.yaml"
        graph = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(graph)
        path.write_text(yaml.safe_dump(graph, allow_unicode=True, sort_keys=False), encoding="utf-8")

    def validate(self) -> tuple[int, str]:
        return run_script(self.tree, "scripts/validate_repository.py")

    def assert_validator_fails(self, expected: str) -> None:
        code, output = self.validate()
        self.assertEqual(code, 1, f"the validator should fail but passed:\n{output}")
        self.assertIn(expected, output)


class ValidatorTests(TreeCase):
    def test_clean_tree_passes(self) -> None:
        code, output = self.validate()
        self.assertEqual(code, 0, output)
        self.assertIn("DOA repository validation: PASS", output)

    def test_version_must_match_everywhere(self) -> None:
        (self.tree / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        self.assert_validator_fails("README.md must state **Version:** 9.9.9")

    def test_card_needs_every_section(self) -> None:
        self.edit(CARD, "## Регуляция\n", "")
        self.assert_validator_fails("mechanism card atp-synthase lacks section ## Регуляция")

    def test_card_with_unfinished_marker_is_rejected(self) -> None:
        marker = "TO" + "DO"  # spelled in two parts so the repository check does not flag this file
        with (self.tree / CARD).open("a", encoding="utf-8") as card:
            card.write(f"\n{marker}: fill in\n")
        self.assert_validator_fails("unfinished marker: mechanisms/cards/atp-synthase.md")

    def test_card_must_attribute_pubmed(self) -> None:
        self.edit(CARD, "Based on articles retrieved from PubMed", "Sources")
        self.assert_validator_fails("mechanism card atp-synthase must cite PubMed articles with links")

    def test_card_must_state_review_status(self) -> None:
        self.edit(CARD, "Проверка биологом не проводилась", "Проверено", count=10)
        self.assert_validator_fails("mechanism card atp-synthase must state the review status")

    def test_edge_basis_pmid_must_be_cited_in_a_card(self) -> None:
        self.edit(SENESCENCE_CARD, "PMID 42809069", "PMID 1", count=10)
        self.assert_validator_fails("PMID:42809069 is not cited in any mechanism card")

    def test_positive_feedback_loop_needs_the_h02_guard(self) -> None:
        guarded = {"I-09", "I-10", "I-12"}
        self.edit_graph(lambda g: g.update(edges=[e for e in g["edges"] if not (e["from"] == "H-02" and e["to"] in guarded)]))
        self.assert_validator_fails("positive-feedback loop without H-02 guard")

    def test_edge_to_unknown_mechanism_is_rejected(self) -> None:
        extra = {"from": "X-99", "to": "I-04", "type": "supplies", "basis": ["REQ-CORE-14"]}
        self.edit_graph(lambda g: g["edges"].append(extra))
        self.assert_validator_fails("unknown mechanism")

    def test_graph_nodes_must_equal_the_registry(self) -> None:
        self.edit_graph(lambda g: g.update(nodes=[n for n in g["nodes"] if n["id"] != "C-01"]))
        self.assert_validator_fails("interaction graph nodes must equal the")

    def test_principles_stay_candidates(self) -> None:
        self.edit("mechanisms/principles.yaml", "status: candidate", "status: accepted")
        self.assert_validator_fails("bad id or status")

    def test_readme_must_list_every_card(self) -> None:
        self.edit("mechanisms/README.md", "(cards/atp-synthase.md)", "(cards/elsewhere.md)")
        self.assert_validator_fails("mechanisms/README.md must list the card atp-synthase")

    def test_workflow_actions_must_be_pinned(self) -> None:
        pinned = yaml.safe_load((self.tree / ".github/workflows/validate.yml").read_text(encoding="utf-8"))
        action = next(s["uses"] for s in pinned["jobs"]["validate"]["steps"] if s.get("uses"))
        self.edit(".github/workflows/validate.yml", action.split("@")[1], "v4", count=1)
        self.assert_validator_fails("workflow action must be pinned to a full commit SHA")

    def test_workflow_permissions_stay_read_only(self) -> None:
        self.edit(".github/workflows/validate.yml", "contents: read", "contents: write")
        self.assert_validator_fails("workflow permissions must be exactly contents: read")


def load_new_card():
    spec = importlib.util.spec_from_file_location("new_card", ROOT / "scripts/new_card.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FormattingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.nc = load_new_card()

    def test_end_page_is_written_in_full(self) -> None:
        cases = {"603-21": "603–621", "1210-5": "1210–1215", "889-901": "889–901", "S243-7": "S243–S247", "12-3": "12–13", "e0142963": "e0142963", "": ""}
        for pages, expected in cases.items():
            self.assertEqual(self.nc.expand_pages(pages), expected, pages)

    def test_every_author_is_listed_by_default(self) -> None:
        authors = [{"last_name": f"L{i}", "initials": "X"} for i in range(15)]
        self.assertNotIn("et al", self.nc.authors_text(authors))
        self.assertTrue(self.nc.authors_text(authors, 12).endswith(", et al"))

    def test_source_line_matches_the_hand_written_style(self) -> None:
        article = {
            "identifiers": {"pmid": "27065163", "doi": "10.1002/cphy.c150015"},
            "title": "Regulation of the Hypothalamic-Pituitary-Adrenocortical Stress Response.",
            "journal": {"iso_abbreviation": "Compr Physiol"},
            "authors": [{"last_name": "Herman", "initials": "JP"}, {"last_name": "Myers", "initials": "B"}],
            "publication_date": {"year": "2016"},
            "citation": {"volume": "6", "issue": "2", "pages": "603-21"},
        }
        self.assertEqual(
            self.nc.format_source(1, article),
            "1. Herman JP, Myers B. Regulation of the Hypothalamic-Pituitary-Adrenocortical Stress Response. Compr Physiol. "
            "2016;6(2):603–621. [DOI](https://doi.org/10.1002/cphy.c150015), [PMID 27065163](https://pubmed.ncbi.nlm.nih.gov/27065163/).",
        )

    def test_missing_fields_leave_no_stray_punctuation(self) -> None:
        line = self.nc.format_source(3, {"identifiers": {"pmid": "3"}, "title": "X"})
        self.assertEqual(line, "3. X. [PMID 3](https://pubmed.ncbi.nlm.nih.gov/3/).")


class NewCardCommandTests(TreeCase):
    def sources(self) -> Path:
        article = {"identifiers": {"pmid": "27065163"}, "title": "T.", "journal": {"iso_abbreviation": "J"}, "authors": [], "publication_date": {"year": "2016"}}
        path = self.tree / "pubmed.json"
        path.write_text(json.dumps({"articles": [article]}), encoding="utf-8")
        return path

    def new_card(self, *extra: str) -> tuple[int, str]:
        args = ["--slug", "gas-exchange", "--title", "газообмен", "--mechanisms", "M-06,H-01", "--sources", str(self.sources()), *extra]
        return run_script(self.tree, "scripts/new_card.py", *args)

    def test_creates_a_skeleton_that_the_validator_rejects_until_it_is_filled_in(self) -> None:
        code, output = self.new_card()
        self.assertEqual(code, 0, output)
        self.assertTrue((self.tree / "mechanisms/cards/gas-exchange.md").is_file())
        self.assertIn("(cards/gas-exchange.md)", (self.tree / "mechanisms/README.md").read_text(encoding="utf-8"))
        self.assert_validator_fails("unfinished marker: mechanisms/cards/gas-exchange.md")

    def test_never_overwrites_an_existing_card(self) -> None:
        self.assertEqual(self.new_card()[0], 0)
        code, output = self.new_card()
        self.assertNotEqual(code, 0)
        self.assertIn("already exists", output)

    def test_rejects_an_unknown_mechanism(self) -> None:
        code, output = run_script(
            self.tree, "scripts/new_card.py", "--slug", "x", "--title", "x", "--mechanisms", "Z-99", "--sources", str(self.sources())
        )
        self.assertNotEqual(code, 0)
        self.assertIn("unknown mechanism ids: Z-99", output)


if __name__ == "__main__":
    unittest.main()
