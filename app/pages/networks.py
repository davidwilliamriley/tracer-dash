# pages/networks.py
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import networkx as nx
import json
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload

# Import View and Model
from views.network_view import NetworkView
from models.model import Model, Node, Edge
from utils.network_utils import build_networkx_from_database

# Register the Page
dash.register_page(__name__, path='/network')

def networkx_to_cytoscape(G: nx.Graph) -> dict:
    elements = []
    
    # Add nodes from NetworkX graph
    for node_id, node_data in G.nodes(data=True):
        elements.append({
            "group": "nodes",
            "data": {
                "id": str(node_id),
                "label": node_data.get('name') or node_data.get('identifier') or "Unnamed",
                "name": node_data.get('name', ''),
                "identifier": node_data.get('identifier', ''),
                "description": node_data.get('description', ''),
            },
        })
    
    # Add edges from NetworkX graph
    for source, target, edge_data in G.edges(data=True):
        elements.append({
            "group": "edges",
            "data": {
                "id": str(edge_data.get('edge_id', f"{source}-{target}")),
                "identifier": edge_data.get('identifier', ''),
                "source": str(source),
                "label": edge_data.get('relationship_type', 'connects to'),
                "target": str(target),
                "description": edge_data.get('description', ''),
            },
        })
    
    return {"elements": elements}


# ==================== LAYOUT ====================

def layout():
    print("[layout] Creating network layout with empty initial data")
    return NetworkView.create_layout({"elements": []})

# ==================== CALLBACKS ====================

@callback(
    Output('cytoscape-data-div', 'children'),
    Input('cytoscape-data-div', 'id'),  # This works, just not elegant
    prevent_initial_call=False
)
def load_cytoscape_data(_):
    try:
        G = build_networkx_from_database()
        cytoscape_data = networkx_to_cytoscape(G) if G else {"elements": []}
        return json.dumps(cytoscape_data)
    except Exception as e:
        print(f"Error loading network: {e}")
        return json.dumps({"elements": []})