# pages/networks.py
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import networkx as nx
import json
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload

# Import View and Model
from views.network_view import NetworkView
from models.model import Node, Edge

# Register the Page
dash.register_page(__name__, path='/network')

# ==================== HELPER FUNCTIONS ====================

def build_network_from_database() -> nx.Graph:
    """Build NetworkX graph from database Nodes and Edges"""
    model = get_model()

    try:
        session = model._get_session()
        
        try:
            nodes = session.query(Node).all()
            edges = (
                session.query(Edge)
                .options(
                    joinedload(Edge.edge_type),
                    joinedload(Edge.source_node),
                    joinedload(Edge.target_node),
                )
                .all()
            )
            
            G = nx.Graph()
            
            # Add the Nodes
            for node in nodes:
                G.add_node(
                    node.id,
                    identifier=node.identifier or "",
                    name=node.name or "",
                    description=node.description or "",
                )
            
            # Add the Edges
            for edge in edges:
                if G.has_node(edge.source_node_id) and G.has_node(edge.target_node_id):
                    G.add_edge(
                        edge.source_node_id,
                        edge.target_node_id,
                        edge_id=edge.id,
                        identifier=edge.identifier or "",
                        relationship_type=(
                            edge.edge_type.name if edge.edge_type else "connects to"
                        ),
                        description=edge.description or "",
                    )
            
            return G
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error building the NetworkX Graph: {e}")
        return nx.Graph()


def networkx_to_cytoscape(G: nx.Graph) -> dict:
    """Convert NetworkX graph to Cytoscape format"""
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
    return NetworkView.create_layout({"elements": []})

# ==================== CALLBACKS ====================

@callback(
    Output('cytoscape-data-div', 'children'),
    Input('cytoscape-data-div', 'id'),
    prevent_initial_call=False
)
def load_cytoscape_data(_):
    """Load and convert network data when the page loads"""
    import app
    G = app.get_network()
    
    if G and G.number_of_nodes() > 0:
        cytoscape_data = networkx_to_cytoscape(G)
    else:
        cytoscape_data = {"elements": []}
    
    return json.dumps(cytoscape_data)

clientside_callback(
    NetworkView.get_cytoscape_client_callback(),
    Output('cytoscape-trigger', 'children'),
    [Input('cytoscape-data-div', 'children'),
     Input('filter-value-input', 'value')]
)