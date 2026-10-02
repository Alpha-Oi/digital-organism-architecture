#!/usr/bin/env python3
"""Analyze mechanisms/interaction-graph.yaml: hubs, nodes without inputs or outputs, isolated nodes, positive-feedback loops.

Usage: python scripts/analyze_interaction_graph.py

Read-only. A positive-feedback loop (a cycle of `amplifies` edges) is reported as guarded when some node of the loop is
constrained or inhibited by H-02 (REQ-CORE-07: positive feedback needs a ceiling and TTL).
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GUARD = "H-02"


def analyze(graph: dict) -> dict:
    names = {node["id"]: node["name"] for node in graph["nodes"]}
    incoming: dict[str, list[dict]] = defaultdict(list)
    outgoing: dict[str, list[dict]] = defaultdict(list)
    for edge in graph["edges"]:
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)
    degree = {node: len(incoming[node]) + len(outgoing[node]) for node in names}
    isolated = sorted(node for node in names if degree[node] == 0)
    no_input = sorted(node for node in names if degree[node] and not incoming[node])
    no_output = sorted(node for node in names if degree[node] and not outgoing[node])
    hubs = sorted(names, key=lambda node: (-degree[node], node))[:10]

    amplify = defaultdict(set)
    for edge in graph["edges"]:
        if edge["type"] == "amplifies":
            amplify[edge["from"]].add(edge["to"])
    guarded_nodes = {edge["to"] for edge in graph["edges"] if edge["from"] == GUARD and edge["type"] in {"constrains", "inhibits"}}
    loops = []
    for start in sorted(amplify):
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            for nxt in sorted(amplify.get(node, ())):
                if nxt == start:
                    cycle = tuple(sorted(path))
                    if cycle not in [tuple(sorted(loop["nodes"])) for loop in loops]:
                        loops.append({"nodes": path, "guarded": bool(set(path) & guarded_nodes)})
                elif nxt not in path:
                    stack.append((nxt, path + [nxt]))
    return {"names": names, "degree": degree, "isolated": isolated, "no_input": no_input, "no_output": no_output, "hubs": hubs, "loops": loops}


def main() -> int:
    graph = yaml.safe_load((ROOT / "mechanisms/interaction-graph.yaml").read_text(encoding="utf-8"))
    result = analyze(graph)
    names, degree = result["names"], result["degree"]
    print(f"Mechanisms: {len(names)}, edges: {len(graph['edges'])}")
    print("Hubs (most connected):")
    for node in result["hubs"]:
        print(f"  {node} {names[node]}: {degree[node]}")
    for key, title in (("no_input", "No incoming edges (only give)"), ("no_output", "No outgoing edges (only receive)"), ("isolated", "Isolated (no edges)")):
        print(f"{title}: {len(result[key])}")
        print("  " + ", ".join(f"{node}" for node in result[key]))
    print("Positive-feedback loops:")
    for loop in result["loops"]:
        print(f"  {' -> '.join(loop['nodes'])}: {'guarded by ' + GUARD if loop['guarded'] else 'NOT guarded'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
