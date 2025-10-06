# utils/network_utils.py
import logging
from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import joinedload
import networkx as nx   

from models.model import Model, Edge, Node
from utils.cache_utils import invalidate_network_cache, get_network, update_network_cache

logger = logging.getLogger('TracerApp')

def build_networkx_from_database():
    """Build a NetworkX directed multigraph from database Nodes and Edges"""
    
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

            # FIXED: Use MultiDiGraph for directed graph with multiple edges between nodes
            G = nx.MultiDiGraph()
            
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
                        key=edge.id,  # MultiDiGraph uses keys for multiple edges
                        edge_id=edge.id,
                        identifier=edge.identifier or "",
                        label=(edge.edge_type.name if edge.edge_type else "connects to"),
                        weight=getattr(edge, 'weight', 1),  # Add weight if it exists
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
        return nx.MultiDiGraph()  # Return empty directed graph

def get_graph_roots(G: nx.MultiDiGraph) -> List[Any]:
    """Find root nodes (nodes with no incoming edges but have outgoing edges)"""
    if G is None or G.number_of_nodes() == 0:
        return []
    
    if not isinstance(G, (nx.DiGraph, nx.MultiDiGraph)):
        logger.warning("Graph is not directed. Cannot identify roots properly.")
        return []
    
    roots = [
        node for node in G.nodes() 
        if G.in_degree(node) == 0 and G.out_degree(node) > 0  # type: ignore
    ]
    logger.info(f"Identified {len(roots)} Root Nodes")
    return roots

def build_breakdown_from_graph(G: nx.MultiDiGraph, root_node: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Build hierarchical breakdown for Tabulator table"""
    if G is None or G.number_of_nodes() == 0:
        return []
    
    if not isinstance(G, (nx.DiGraph, nx.MultiDiGraph)):
        logger.error("Graph must be directed to build hierarchy")
        return []
    
    def build_hierarchy(node: Any, visited: Optional[Set[Any]] = None) -> List[Dict[str, Any]]:
        """Recursively build hierarchy from a node"""
        if visited is None:
            visited = set()
        
        # Prevent cycles
        if node in visited:
            return []
        
        visited.add(node)
        
        # Get node attributes
        node_data = G.nodes.get(node, {})
        
        # Get children (outgoing edges)
        children_data = []
        out_edges = G.out_edges(node, data=True, keys=True)  # type: ignore
        for _, target, key, edge_data in out_edges:
            child_hierarchy = build_hierarchy(target, visited.copy())
            
            child_item = {
                'id': target,
                'identifier': G.nodes[target].get('identifier', ''),
                'name': G.nodes[target].get('name', ''),
                'description': G.nodes[target].get('description', ''),
                'edge_label': edge_data.get('label', ''),
                'edge_type': edge_data.get('relationship_type', ''),
                'weight': edge_data.get('weight', 1),
                '_children': child_hierarchy  # Tabulator uses _children
            }
            children_data.append(child_item)
        
        # Sort children by weight and identifier (natural sort for identifiers like 6.4.1, 6.4.2, 6.4.10)
        def natural_sort_key(item):
            import re
            identifier = item.get('identifier', '')
            if identifier:
                # Split identifier into parts and convert numeric parts to integers for proper sorting
                parts = re.split(r'(\d+)', identifier)
                converted_parts = []
                for part in parts:
                    if part.isdigit():
                        converted_parts.append(int(part))
                    else:
                        converted_parts.append(part)
                return (item['weight'], converted_parts, item.get('name', ''))
            else:
                return (item['weight'], [item.get('name', '')], item.get('name', ''))
        
        children_data.sort(key=natural_sort_key)
        
        return children_data
    
    # If specific root provided, build from there
    if root_node:
        if root_node not in G:
            logger.error(f"Root node {root_node} not found in graph")
            return []
        
        node_data = G.nodes.get(root_node, {})
        return [{
            'id': root_node,
            'identifier': node_data.get('identifier', ''),
            'name': node_data.get('name', ''),
            'description': node_data.get('description', ''),
            '_children': build_hierarchy(root_node)
        }]
    
    # Otherwise, build from all roots
    roots = get_graph_roots(G)
    breakdown = []
    
    for root in roots:
        node_data = G.nodes.get(root, {})
        root_item = {
            'id': root,
            'identifier': node_data.get('identifier', ''),
            'name': node_data.get('name', ''),
            'description': node_data.get('description', ''),
            '_children': build_hierarchy(root)
        }
        breakdown.append(root_item)
    
    return breakdown