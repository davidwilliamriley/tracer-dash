# app/utils/metric_utils.py

# Import Libraries
import logging
from memory_profiler import memory_usage
import networkx as nx
from networkx.algorithms import average_clustering, degree_assortativity_coefficient
import time

from models.model import Model, Node, Edge

logger = logging.getLogger('TracerApp')

# Completeness Metrics

def calculate_completeness_metrics(G, session=None):
    """Calculate completeness metrics for the graph"""
    if session is None:
        model = Model()
        session = model._get_session()
        close_session = True
    else:
        close_session = False
    
    try:
        db_node_count = session.query(Node).count()
        db_edge_count = session.query(Edge).count()
        
        metrics = {
            'node_coverage': round(G.number_of_nodes() / db_node_count * 100, 2) if db_node_count > 0 else 0,
            'edge_coverage': round(G.number_of_edges() / db_edge_count * 100, 2) if db_edge_count > 0 else 0,
            'orphaned_nodes': sum(1 for n in G.nodes() if G.degree(n) == 0),
            'nodes_with_names': sum(1 for _, data in G.nodes(data=True) if data.get('name')),
            'nodes_with_descriptions': sum(1 for _, data in G.nodes(data=True) if data.get('description')),
            'attribute_completeness': round(
                sum(1 for _, data in G.nodes(data=True) if data.get('name') and data.get('description')) 
                / G.number_of_nodes() * 100, 2
            ) if G.number_of_nodes() > 0 else 0
        }

        logger.info(f"Completeness Metrics: {metrics}")
        return metrics
    finally:
        if close_session:
            session.close()

# Efficiency Metrics

def calculate_efficiency_metrics(G, build_time=None, memory_used=None):
    """Calculate efficiency metrics for the graph build process"""
    
    metrics = {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'graph_density': round(nx.density(G), 4),
    }
    
    if build_time is not None:
        metrics['build_time_seconds'] = round(build_time, 3)
        metrics['nodes_per_second'] = round(G.number_of_nodes() / build_time, 2) if build_time > 0 else 0
        metrics['edges_per_second'] = round(G.number_of_edges() / build_time, 2) if build_time > 0 else 0
    
    if memory_used is not None:
        metrics['memory_mb'] = round(memory_used, 2)
    
    logger.info(f"Efficiency Metrics: {metrics}")
    return metrics

# Robustness Metrics

def calculate_robustness_metrics(G):
    """Calculate robustness metrics for the graph"""
    metrics = {
        'self_loops': nx.number_of_selfloops(G),
        'isolated_nodes': len(list(nx.isolates(G))),
        'is_connected': nx.is_connected(G),
        'number_of_components': nx.number_connected_components(G),
        'invalid_edges': count_invalid_edges(G),
    }
    
    # Only calculate clustering for graphs with nodes
    if G.number_of_nodes() > 0:
        metrics['average_clustering'] = round(average_clustering(G), 4)
    
    # Only calculate assortativity for graphs with edges
    if G.number_of_edges() > 0:
        try:
            metrics['degree_assortativity'] = round(degree_assortativity_coefficient(G), 4)
        except:
            metrics['degree_assortativity'] = None
    
    logger.info(f"Robustness Metrics: {metrics}")
    return metrics

def count_invalid_edges(G):
    """Count edges where source or target doesn't exist"""
    invalid = 0
    for u, v in G.edges():
        if not G.has_node(u) or not G.has_node(v):
            invalid += 1
    return invalid

# Resilience Metrics

def calculate_resilience_metrics(G):
    """Calculate resilience metrics for the graph"""
    metrics = {
        'is_connected': nx.is_connected(G),
        'number_of_components': nx.number_connected_components(G),
        'average_degree': round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2) if G.number_of_nodes() > 0 else 0,
        'density': round(nx.density(G), 4),
        'articulation_points': len(list(nx.articulation_points(G))),
    }
    
    # Only calculate for connected graphs
    if nx.is_connected(G) and G.number_of_nodes() > 1:
        try:
            metrics['node_connectivity'] = nx.node_connectivity(G)
            metrics['edge_connectivity'] = nx.edge_connectivity(G)
            metrics['average_shortest_path'] = round(nx.average_shortest_path_length(G), 2)
            metrics['diameter'] = nx.diameter(G)
        except:
            logger.warning("Could not calculate some resilience metrics")
    
    logger.info(f"Resilience Metrics: {metrics}")
    return metrics

def comprehensive_metrics_report(G, session=None, build_time=None, memory_used=None):
    """Generate a comprehensive metrics report"""
    
    if session is None:
        model = Model()
        session = model._get_session()
        close_session = True
    else:
        close_session = False
    
    try:
        report = {
            'completeness': calculate_completeness_metrics(G, session),
            'efficiency': calculate_efficiency_metrics(G, build_time, memory_used),
            'robustness': calculate_robustness_metrics(G),
            'resilience': calculate_resilience_metrics(G)
        }
        
        return report
    finally:
        if close_session:
            session.close()