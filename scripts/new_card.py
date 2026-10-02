#!/usr/bin/env python3
"""Create a mechanism-card skeleton in mechanisms/cards/ from PubMed metadata.

Usage:
  python scripts/new_card.py --slug respiratory-gas-exchange --title "дыхание и газообмен" \
      --mechanisms M-06,H-01 --sources pubmed.json

`pubmed.json` is the unchanged result of the PubMed `get_article_metadata` call (an object with an `articles` list) or a list of
such article objects. The script formats the "Источники" section from that data, so author lists, years, volumes, pages and DOI are
copied rather than retyped. It does not read abstracts and does not write any biological claim: every content section is a TODO
that a human has to fill in after checking each statement against the abstract. `scripts/validate_repository.py` already rejects any
card that still contains a TODO marker, so an unfinished skeleton cannot be merged.

The script creates one new file, registers the card in mechanisms/README.md and prints a checklist for the remaining manual work
(principles, graph edges with PMID basis, CHANGELOG). It never overwrites an existing card.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "mechanisms/cards"
README = ROOT / "mechanisms/README.md"
GRAPH = ROOT / "mechanisms/interaction-graph.yaml"
PRINCIPLES = ROOT / "mechanisms/principles.yaml"
MAX_AUTHORS = 12
TODO = "TODO"

SKELETON = """# Карточка: {title}

**Статус:** informative, пилот. Проверка биологом не проводилась. Факты взяты из рефератов статей PubMed (полные тексты не читались); выводы автора помечены отдельно. {todo}: сколько источников, какого типа и какого года.

## Что это и зачем

{todo}: одна-две фразы, что делает механизм в организме и зачем он стандарту. Связанные механизмы DOA: {related}.

## Как устроена

- {todo}: только то, что сказано в реферате; рядом номер источника, например [1].

## Как работает (по шагам)

1. {todo}: шаги; каждый шаг со ссылкой на источник.

## Регуляция

- {todo}: что регулирует механизм; если в рефератах не сказано, так и написать.

## Как ломается и цена

- {todo}: что сказано в источниках о нарушениях.
- Вывод автора: {todo}.

## Инженерный принцип (вывод автора)

- **P-{next_principle} «{todo}».** {todo}: принцип и идея проверки добавляются также в `mechanisms/principles.yaml`.

## Где аналогия кончается

- {todo}: тип и размер каждого источника; что перенос на цифровые системы — гипотеза автора.

## Связь с DOA

| Механизм | Связь |
|---|---|
{table}

Принципы и идеи проверок — в [`../principles.yaml`](../principles.yaml).

## Источники

Based on articles retrieved from PubMed:

{sources}

## Ограничения карточки

Только рефераты. {todo}: что не нашлось, какие источники слабые. Карточка не заменяет проверку биологом.
"""


def load_articles(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    articles = data["articles"] if isinstance(data, dict) else data
    if not articles:
        raise SystemExit(f"{path}: no articles found")
    return articles


def authors_text(authors: list[dict]) -> str:
    names = [f"{a.get('last_name', '').strip()} {a.get('initials', '').strip()}".strip() for a in authors]
    names = [name for name in names if name]
    if len(names) > MAX_AUTHORS:
        return ", ".join(names[:MAX_AUTHORS]) + ", et al"
    return ", ".join(names)


def expand_pages(pages: str) -> str:
    """PubMed abbreviates the end page ("603-21"); write it in full ("603–621") like the existing cards."""
    match = re.fullmatch(r"(\d+)-(\d+)", pages)
    if not match:
        return pages.replace("-", "–")
    start, end = match.groups()
    if len(end) < len(start):
        end = start[: len(start) - len(end)] + end
    return f"{start}–{end}"


def format_source(number: int, article: dict) -> str:
    ids = article.get("identifiers", {})
    pmid = ids.get("pmid")
    if not pmid:
        raise SystemExit(f"article {number} has no PMID")
    title = article.get("title", "").strip()
    if title and not title.endswith((".", "?", "!")):
        title += "."
    journal = article.get("journal", {}).get("iso_abbreviation") or article.get("journal", {}).get("title", "")
    year = article.get("publication_date", {}).get("year", "")
    citation = article.get("citation", {})
    volume, issue, pages = citation.get("volume", ""), citation.get("issue", ""), citation.get("pages", "")
    where = f"{journal}. {year}" if journal else str(year)
    if volume:
        where += f";{volume}"
        if issue:
            where += f"({issue})"
    if pages:
        where += f":{expand_pages(pages)}"
    links = []
    if ids.get("doi"):
        links.append(f"[DOI](https://doi.org/{ids['doi']})")
    links.append(f"[PMID {pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")
    authors = authors_text(article.get("authors", []))
    head = f"{authors}. " if authors else ""
    return f"{number}. {head}{title} {where}. {', '.join(links)}."


def next_principle_number() -> str:
    ids = [int(item["id"][2:]) for item in yaml.safe_load(PRINCIPLES.read_text(encoding="utf-8"))["principles"]]
    return f"{max(ids) + 1:02d}"


def register_in_readme(slug: str, title: str) -> bool:
    text = README.read_text(encoding="utf-8")
    marker = ").\n\n## Что в карточку попадает"
    if marker not in text or f"cards/{slug}.md" in text:
        return False
    README.write_text(text.replace(marker, f"), [{title}](cards/{slug}.md).\n\n## Что в карточку попадает", 1), encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a mechanism-card skeleton from PubMed metadata.")
    parser.add_argument("--slug", required=True, help="file name without extension, latin letters, digits and hyphens")
    parser.add_argument("--title", required=True, help="card title in Russian, shown in the README list")
    parser.add_argument("--mechanisms", required=True, help="comma-separated mechanism ids from the registry, for example M-06,H-01")
    parser.add_argument("--sources", required=True, type=Path, help="JSON file with the PubMed get_article_metadata result")
    args = parser.parse_args(argv)

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise SystemExit("slug must consist of latin letters, digits and hyphens")
    target = CARDS / f"{args.slug}.md"
    if target.exists():
        raise SystemExit(f"{target.relative_to(ROOT)} already exists; refusing to overwrite")
    graph = yaml.safe_load(GRAPH.read_text(encoding="utf-8"))
    names = {node["id"]: node["name"] for node in graph["nodes"]}
    ids = [item.strip() for item in args.mechanisms.split(",") if item.strip()]
    unknown = [item for item in ids if item not in names]
    if unknown:
        raise SystemExit(f"unknown mechanism ids: {', '.join(unknown)}")
    articles = load_articles(args.sources)
    pmids = [a.get("identifiers", {}).get("pmid") for a in articles]
    if len(pmids) != len(set(pmids)):
        raise SystemExit("duplicate PMIDs in the sources file")

    table = "\n".join(f"| `{item}` {names[item]} | {TODO}: связь с карточкой |" for item in ids)
    sources = "\n".join(format_source(number, article) for number, article in enumerate(articles, start=1))
    related = ", ".join(f"`{item}`" for item in ids)
    target.write_text(
        SKELETON.format(title=args.title, todo=TODO, related=related, table=table, sources=sources, next_principle=next_principle_number()),
        encoding="utf-8",
    )
    registered = register_in_readme(args.slug, args.title)

    cards = len(list(CARDS.glob("*.md")))
    edges = len(graph["edges"])
    principles = len(yaml.safe_load(PRINCIPLES.read_text(encoding="utf-8"))["principles"])
    print(f"Created {target.relative_to(ROOT)} with {len(articles)} sources.")
    print("Listed in mechanisms/README.md." if registered else "README.md was not changed: add the card to the list by hand.")
    print("\nStill to do by hand (the validator fails until every TODO is gone):")
    print(f"  1. Read each abstract; fill every {TODO} with statements that the abstract supports; mark author conclusions as such.")
    print("  2. Add principles to mechanisms/principles.yaml (cards: [" + args.slug + "], status: candidate).")
    print("  3. Add graph edges to mechanisms/interaction-graph.yaml; every PMID basis must be cited in a card.")
    print(f"  4. Update CHANGELOG.md counts (now {cards} cards, {principles} principles, {edges} edges).")
    print("  5. Run: python scripts/validate_repository.py && git diff --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
