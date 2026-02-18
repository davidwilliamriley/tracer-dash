#!/usr/bin/env python3

import argparse
import json
import uuid
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any, Dict, List, Tuple


def _node_level(identifier: str) -> int:
    if not identifier:
        return 0
    return identifier.count('.')


def _node_label(node: Dict[str, Any]) -> str:
    identifier = str(node.get('identifier') or '')
    name = str(node.get('name') or '')
    if identifier and name:
        return f"{identifier} - {name}"
    return identifier or name or str(node.get('id') or '')


def _build_layout(nodes: List[Dict[str, Any]]) -> Dict[str, Tuple[int, int]]:
    level_groups: Dict[int, List[Dict[str, Any]]] = {}
    for node in nodes:
        level = _node_level(str(node.get('identifier') or ''))
        level_groups.setdefault(level, []).append(node)

    for level in level_groups:
        level_groups[level].sort(key=lambda n: str(n.get('identifier') or n.get('name') or ''))

    coordinates: Dict[str, Tuple[int, int]] = {}
    horizontal_gap = 260
    vertical_gap = 120
    base_x = 80
    base_y = 80

    for level in sorted(level_groups.keys()):
        level_nodes = level_groups[level]
        for row, node in enumerate(level_nodes):
            node_id = str(node.get('id'))
            x = base_x + (level * horizontal_gap)
            y = base_y + (row * vertical_gap)
            coordinates[node_id] = (x, y)

    return coordinates


def build_drawio_xml(network: Dict[str, Any], diagram_name: str = 'Network') -> str:
    nodes: List[Dict[str, Any]] = network.get('nodes', [])
    edges: List[Dict[str, Any]] = network.get('edges', [])

    mxfile = ET.Element('mxfile', host='app.diagrams.net', modified='2026-02-18T00:00:00.000Z', agent='GitHub Copilot GPT-5.3-Codex', version='24.7.17', type='device')
    diagram = ET.SubElement(mxfile, 'diagram', id=f'diagram-{uuid.uuid4().hex[:8]}', name=diagram_name)
    model = ET.SubElement(
        diagram,
        'mxGraphModel',
        dx='1320',
        dy='760',
        grid='1',
        gridSize='10',
        guides='1',
        tooltips='1',
        connect='1',
        arrows='1',
        fold='1',
        page='1',
        pageScale='1',
        pageWidth='1920',
        pageHeight='1080',
        math='0',
        shadow='0',
    )
    root = ET.SubElement(model, 'root')

    ET.SubElement(root, 'mxCell', id='0')
    ET.SubElement(root, 'mxCell', id='1', parent='0')

    coords = _build_layout(nodes)
    drawio_node_ref: Dict[str, str] = {}

    node_style = 'rounded=1;whiteSpace=wrap;html=1;strokeColor=#3E7CB1;fillColor=#EAF2FA;fontSize=12;'
    edge_style = 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#5B5B5B;fontSize=11;'

    for idx, node in enumerate(nodes, start=2):
        node_id = str(node.get('id'))
        drawio_id = f'n{idx}'
        drawio_node_ref[node_id] = drawio_id

        x, y = coords.get(node_id, (80, 80))
        cell = ET.SubElement(
            root,
            'mxCell',
            id=drawio_id,
            value=_node_label(node),
            style=node_style,
            vertex='1',
            parent='1',
        )
        ET.SubElement(cell, 'mxGeometry', {'x': str(x), 'y': str(y), 'width': '220', 'height': '70', 'as': 'geometry'})

    edge_counter = 1
    for edge in edges:
        source_node_id = str(edge.get('source_node_id') or '')
        target_node_id = str(edge.get('target_node_id') or '')
        source = drawio_node_ref.get(source_node_id)
        target = drawio_node_ref.get(target_node_id)
        if not source or not target:
            continue

        edge_type_name = str(edge.get('edge_type_name') or '')
        edge_id = f'e{edge_counter}'
        edge_counter += 1

        edge_cell = ET.SubElement(
            root,
            'mxCell',
            id=edge_id,
            value=edge_type_name,
            style=edge_style,
            edge='1',
            parent='1',
            source=source,
            target=target,
        )
        ET.SubElement(edge_cell, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    xml_bytes = ET.tostring(mxfile, encoding='utf-8')
    pretty = minidom.parseString(xml_bytes).toprettyxml(indent='  ', encoding='utf-8')
    return pretty.decode('utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Convert network JSON to draw.io file')
    parser.add_argument('--input', dest='input_path', default='dev/network_output.json', help='Input network JSON file path')
    parser.add_argument('--output', dest='output_path', default='dev/network_diagram.drawio', help='Output draw.io file path')
    parser.add_argument('--name', dest='diagram_name', default='Network', help='Draw.io diagram name')
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_path).resolve()

    if not input_path.exists():
        print(f'Error: Input file not found: {input_path}')
        return 1

    try:
        network = json.loads(input_path.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        print(f'Error: Failed to parse JSON: {type(exc).__name__}: {exc}')
        return 1

    drawio_xml = build_drawio_xml(network, diagram_name=args.diagram_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(drawio_xml, encoding='utf-8')

    print(f'Wrote draw.io diagram to: {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
