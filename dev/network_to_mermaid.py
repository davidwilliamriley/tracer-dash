#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _safe_label(value: str) -> str:
    clean = value.replace('"', "'").replace("\n", " ").strip()
    return clean


def build_mermaid(network: Dict[str, Any], direction: str = "LR") -> str:
    nodes: List[Dict[str, Any]] = network.get("nodes", [])
    edges: List[Dict[str, Any]] = network.get("edges", [])

    node_ref_map: Dict[str, str] = {}
    lines: List[str] = [f"flowchart {direction}"]

    for index, node in enumerate(nodes, start=1):
        node_id = str(node.get("id", ""))
        identifier = str(node.get("identifier") or "")
        name = str(node.get("name") or "")
        label = f"{identifier} - {name}" if identifier else name or node_id
        label = _safe_label(label)

        mermaid_ref = f"N{index}"
        node_ref_map[node_id] = mermaid_ref
        lines.append(f'    {mermaid_ref}["{label}"]')

    for edge in edges:
        source_id = str(edge.get("source_node_id", ""))
        target_id = str(edge.get("target_node_id", ""))
        edge_label = str(edge.get("edge_type_name") or "")
        edge_label = _safe_label(edge_label)

        source_ref = node_ref_map.get(source_id)
        target_ref = node_ref_map.get(target_id)

        if not source_ref or not target_ref:
            continue

        if edge_label:
            lines.append(f"    {source_ref} -->|{edge_label}| {target_ref}")
        else:
            lines.append(f"    {source_ref} --> {target_ref}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert network JSON into a Mermaid diagram")
    parser.add_argument(
        "--input",
        dest="input_path",
        default="dev/network_output.json",
        help="Input network JSON file path",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        default="dev/network_diagram.mmd",
        help="Output Mermaid file path",
    )
    parser.add_argument(
        "--direction",
        dest="direction",
        default="LR",
        choices=["TB", "TD", "BT", "RL", "LR"],
        help="Mermaid flow direction",
    )
    parser.add_argument(
        "--print",
        dest="print_stdout",
        action="store_true",
        help="Print Mermaid content to terminal",
    )

    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_path).resolve()

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    try:
        network = json.loads(input_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(f"Error: Failed to parse JSON: {type(exc).__name__}: {exc}")
        return 1

    mermaid = build_mermaid(network, direction=args.direction)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(mermaid, encoding="utf-8")

    print(f"Wrote Mermaid diagram to: {output_path}")
    if args.print_stdout:
        print("\n" + mermaid)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
