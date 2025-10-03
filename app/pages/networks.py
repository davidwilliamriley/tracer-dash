# pages/networks.py
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import networkx as nx
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload
from typing import cast

# Import View and Model
from views.network_view import NetworkView
from models.model import Model, Node, Edge

# Register the Page
dash.register_page(__name__, path='/network')

# Initialize the Model
model = Model()

# ==================== HELPER FUNCTIONS ====================

def build_network_from_database() -> nx.Graph:
    """Build NetworkX graph from database Nodes and Edges"""
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


def get_network_visualization_data() -> Dict[str, Any]:
    """Get the Network formatted for Cytoscape"""
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
            
            elements = []
            
            # Add Nodes to Elements List
            for node in nodes:
                elements.append(
                    {
                        "group": "nodes",
                        "data": {
                            "id": str(node.id),
                            "label": node.name or node.identifier or "Unnamed",
                            "name": node.name or "",
                            "identifier": node.identifier or "",
                            "description": node.description or "",
                        },
                    }
                )
            
            # Add Edges to Elements List
            for edge in edges:
                edge_type_name = (
                    edge.edge_type.name if edge.edge_type else "connects to"
                )
                
                elements.append(
                    {
                        "group": "edges",
                        "data": {
                            "id": str(edge.id),
                            "identifier": edge.identifier or "",
                            "source": str(edge.source_node_id),
                            "label": edge_type_name,
                            "target": str(edge.target_node_id),
                            "description": edge_type_name,
                        },
                    }
                )
            
            return {"elements": elements}
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error getting the visualization data: {e}")
        return {"elements": []}

# ==================== LAYOUT ====================

def layout():
    networks_data = get_network_visualization_data()
    return NetworkView.create_layout(networks_data)

# ==================== CALLBACKS ====================

clientside_callback(
    NetworkView.get_cytoscape_client_callback(),
    Output('cytoscape-trigger', 'children'),
    [Input('cytoscape-data-div', 'children'),
     Input('filter-value-input', 'value')]
)