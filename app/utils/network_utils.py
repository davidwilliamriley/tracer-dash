# utils / network_utils.py
import logging
from sqlalchemy.orm import joinedload
import networkx as nx   

from models.model import Model, Edge, Node

logger = logging.getLogger('TracerApp')

def build_networkx_from_database():
    """
    Build a NetworkX graph from database Nodes and Edges
    Returns a NetworkX Graph Object
    """
    logger.info("Building NetworkX graph from Database")

    model = Model()

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
            
            print(f"[build_network_from_database] Loaded {len(nodes)} nodes and {len(edges)} edges")

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

            print(f"Built a NetworkX graph with {G.number_of_nodes()} Nodes and {G.number_of_edges()} Edges")
            return G
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"[build_network_from_database] Error building the NetworkX Graph: {e}")
        import traceback
        traceback.print_exc()
        return nx.Graph()