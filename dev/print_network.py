#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


def _resolve_paths() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root


def build_network_payload(model) -> Dict[str, Any]:
    nodes = model.get_nodes()
    edges = model.get_edges()
    edge_types = model.get_edge_types()

    edge_type_lookup = {str(edge_type.id): edge_type for edge_type in edge_types}

    edges_payload = []
    for edge in edges:
        edge_type = edge_type_lookup.get(str(edge.edge_type_id_fk))
        edges_payload.append(
            {
                "id": str(edge.id),
                "source_node_id": str(edge.source_node_id_fk),
                "target_node_id": str(edge.target_node_id_fk),
                "edge_type_id": str(edge.edge_type_id_fk),
                "edge_type_name": edge_type.name if edge_type is not None else None,
                "description": edge.description,
            }
        )

    payload = {
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "edge_type_count": len(edge_types),
        },
        "nodes": [
            {
                "id": str(node.id),
                "identifier": node.identifier,
                "name": node.name,
                "description": node.description,
                "node_type_id": str(node.node_type_id_fk),
            }
            for node in nodes
        ],
        "edges": edges_payload,
        "edge_types": [
            {
                "id": str(edge_type.id),
                "identifier": edge_type.identifier,
                "name": edge_type.name,
                "description": edge_type.description,
            }
            for edge_type in edge_types
        ],
    }

    return payload


def main() -> int:
    project_root = _resolve_paths()

    parser = argparse.ArgumentParser(description="Print complete network from model.py")
    parser.add_argument(
        "--db",
        dest="db_path",
        default=None,
        help="Optional path to SQLite database file. Defaults to app config path.",
    )
    args = parser.parse_args()

    from app.models.model import Model

    model = None
    try:
        db_path = args.db_path
        if db_path:
            db_path = str((project_root / db_path).resolve()) if not Path(db_path).is_absolute() else db_path
            model = Model(db_path=db_path)
        else:
            model = Model()

        payload = build_network_payload(model)
        print(json.dumps(payload, indent=2))
        return 0
    except Exception as exc:
        print(f"Error: {type(exc).__name__}: {exc}")
        return 1
    finally:
        if model is not None:
            model.close()


if __name__ == "__main__":
    raise SystemExit(main())
