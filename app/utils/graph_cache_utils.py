#!/usr/bin/env python3

# utils/graph_cache_utils.py - Utilities for managing graph data with dcc.Store

import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import networkx as nx
import logging

logger = logging.getLogger(__name__)

class GraphCacheUtils:
    """
    Utilities for managing NetworkX graph data with Dash dcc.Store components.
    This class provides methods to serialize/deserialize graphs and manage cache state.
    """
    
    @staticmethod
    def serialize_networkx_graph(graph: nx.Graph) -> Dict[str, Any]:
        """
        Convert a NetworkX graph to a JSON-serializable format for dcc.Store.
        
        Args:
            graph: NetworkX graph to serialize
            
        Returns:
            Dictionary containing serialized graph data
        """
        try:
            # Convert to node-link format (JSON serializable)
            graph_data = nx.node_link_data(graph)
            
            # Add metadata
            serialized_data = {
                'graph_data': graph_data,
                'metadata': {
                    'nodes_count': graph.number_of_nodes(),
                    'edges_count': graph.number_of_edges(),
                    'created_at': datetime.now().isoformat(),
                    'graph_type': type(graph).__name__
                },
                'cache_version': '1.0'
            }
            
            logger.debug(f"Serialized NetworkX graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
            return serialized_data
            
        except Exception as e:
            logger.error(f"Error serializing NetworkX graph: {e}")
            return {}
    
    @staticmethod
    def deserialize_networkx_graph(serialized_data: Dict[str, Any]) -> Optional[nx.Graph]:
        """
        Convert serialized graph data back to a NetworkX graph.
        
        Args:
            serialized_data: Dictionary containing serialized graph data
            
        Returns:
            NetworkX graph or None if deserialization fails
        """
        try:
            if not serialized_data or 'graph_data' not in serialized_data:
                return None
                
            # Reconstruct graph from node-link format
            graph = nx.node_link_graph(serialized_data['graph_data'])
            
            metadata = serialized_data.get('metadata', {})
            logger.debug(f"Deserialized NetworkX graph with {metadata.get('nodes_count', 0)} nodes and {metadata.get('edges_count', 0)} edges")
            
            return graph
            
        except Exception as e:
            logger.error(f"Error deserializing NetworkX graph: {e}")
            return None
    
    @staticmethod
    def create_cache_metadata(nodes_count: int, edges_count: int, additional_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create metadata for graph cache.
        
        Args:
            nodes_count: Number of nodes in the graph
            edges_count: Number of edges in the graph
            additional_info: Optional additional metadata
            
        Returns:
            Dictionary containing cache metadata
        """
        metadata = {
            'nodes_count': nodes_count,
            'edges_count': edges_count,
            'timestamp': datetime.now().isoformat(),
            'cache_key': f"graph_{nodes_count}_{edges_count}_{int(time.time())}"
        }
        
        if additional_info:
            metadata.update(additional_info)
            
        return metadata
    
    @staticmethod
    def is_cache_valid(cache_data: Optional[Dict[str, Any]], max_age_seconds: int = 300) -> bool:
        """
        Check if cached data is still valid based on timestamp.
        
        Args:
            cache_data: Cached data dictionary
            max_age_seconds: Maximum age in seconds (default: 5 minutes)
            
        Returns:
            True if cache is valid, False otherwise
        """
        if not cache_data or 'metadata' not in cache_data:
            return False
            
        try:
            timestamp_str = cache_data['metadata'].get('timestamp')
            if not timestamp_str:
                return False
                
            cache_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            current_time = datetime.now()
            
            age_seconds = (current_time - cache_time).total_seconds()
            return age_seconds <= max_age_seconds
            
        except Exception as e:
            logger.error(f"Error checking cache validity: {e}")
            return False
    
    @staticmethod
    def convert_cytoscape_to_networkx(cytoscape_data: Dict[str, Any]) -> nx.Graph:
        """
        Convert Cytoscape format data to NetworkX graph.
        
        Args:
            cytoscape_data: Dictionary containing Cytoscape elements
            
        Returns:
            NetworkX graph
        """
        G = nx.Graph()
        
        if 'elements' not in cytoscape_data:
            return G
            
        # Add nodes
        for element in cytoscape_data['elements']:
            if element.get('group') == 'nodes':
                node_data = element.get('data', {})
                node_id = node_data.get('id')
                if node_id:
                    G.add_node(node_id, **{k: v for k, v in node_data.items() if k != 'id'})
        
        # Add edges
        for element in cytoscape_data['elements']:
            if element.get('group') == 'edges':
                edge_data = element.get('data', {})
                source = edge_data.get('source')
                target = edge_data.get('target')
                if source and target:
                    G.add_edge(source, target, **{k: v for k, v in edge_data.items() if k not in ['source', 'target', 'id']})
        
        return G
    
    @staticmethod
    def get_cache_stats(cache_stores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about cached graph data.
        
        Args:
            cache_stores: Dictionary of cache store data
            
        Returns:
            Dictionary containing cache statistics
        """
        stats = {
            'total_stores': len(cache_stores),
            'valid_caches': 0,
            'total_nodes': 0,
            'total_edges': 0,
            'stores_info': {}
        }
        
        for store_name, store_data in cache_stores.items():
            if store_data and isinstance(store_data, dict):
                metadata = store_data.get('metadata', {})
                is_valid = GraphCacheUtils.is_cache_valid(store_data)
                
                if is_valid:
                    stats['valid_caches'] += 1
                    stats['total_nodes'] += metadata.get('nodes_count', 0)
                    stats['total_edges'] += metadata.get('edges_count', 0)
                
                stats['stores_info'][store_name] = {
                    'valid': is_valid,
                    'nodes': metadata.get('nodes_count', 0),
                    'edges': metadata.get('edges_count', 0),
                    'timestamp': metadata.get('timestamp', 'Unknown')
                }
        
        return stats