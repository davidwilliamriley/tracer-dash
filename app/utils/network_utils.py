# utils/network_utils.py
import logging
from sqlalchemy.orm import joinedload
import networkx as nx   

from models.model import Model, Edge, Node
from utils.cache_utils import invalidate_network_cache, get_network, update_network_cache

logger = logging.getLogger('TracerApp')

def build_networkx_from_database():
    """Build a NetworkX graph from database Nodes and Edges"""
    
    cached_graph = get_network()
    if cached_graph:
        logger.info("Clearing cached Graph")
        invalidate_network_cache()
    
    logger.info("Building the NetworkX Graph from the Database")
    
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

            logger.info(f"Loaded {len(edges)} Edges and {len(nodes)} Nodes from the Database")

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

            logger.info(f"Built NetworkX graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
            
            update_network_cache(G)
            
            return G
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error building NetworkX Graph {e}")
        import traceback
        traceback.print_exc()
        return nx.Graph()
    
def build_breakdown_from_graph():
    pass