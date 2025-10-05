# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
import networkx as nx
import plotly.graph_objects as go

# MVC Imports
from views.dashboard_view import DashboardView
from utils.cache_utils import get_network  
from utils.metric_utils import (
    calculate_completeness_metrics, 
    calculate_efficiency_metrics, 
    calculate_robustness_metrics, 
    calculate_resilience_metrics
)
from models.model import Model

register_page(
    __name__, 
    path="/dashboard",
    name="Dashboard",
    title="Tracer - Dashboard"
)

dashboard_view = DashboardView()

layout = dashboard_view.get_layout()

@callback(
    Output("descriptive-metrics-table", "data"),
    Output("descriptive-metrics-table", "columns"),
    Input("descriptive-metrics-table", "id") 
)
def update_system_health_table(_):
    """Update the descriptive metrics table with network statistics"""
    
    G = get_network()
    
    if G is not None and G.number_of_nodes() > 0:
        # Calculate network metrics
        num_edges = G.number_of_edges()
        num_nodes = G.number_of_nodes()
        density = nx.density(G) if num_nodes > 1 else 0
        
        # Calculate average degree
        degrees = [G.degree(n) for n in G.nodes()]
        avg_degree = sum(degrees) / len(degrees) if degrees else 0

        data = [
            {"Metric": "No. of Nodes", "Value": str(num_nodes)},
            {"Metric": "No. of Edges", "Value": str(num_edges)},
            {"Metric": "Density", "Value": f"{density:.4f}"},
            {"Metric": "Average Degree", "Value": f"{avg_degree:.2f}"}
        ]
    else:
        data = [
            {"Metric": "No. of Nodes", "Value": "0"},
            {"Metric": "No. of Edges", "Value": "0"},
            {"Metric": "Density", "Value": "0.0000"},
            {"Metric": "Average Degree", "Value": "0.00"}
        ]

    columns = [
        {"name": "Metric", "id": "Metric"},
        {"name": "Value", "id": "Value"}
    ]
    
    return data, columns


@callback(
    Output("completeness-metrics", "figure"),
    Input("completeness-metrics", "id")
)
def update_completeness_metrics(_):
    """Update completeness metrics visualization"""
    G = get_network()
    
    if G is None or G.number_of_nodes() == 0:
        return create_empty_figure("No data available")
    
    model = Model()
    session = model._get_session()
    
    try:
        metrics = calculate_completeness_metrics(G, session)
        
        fig = go.Figure()
        
        # Bar chart for coverage metrics
        fig.add_trace(go.Bar(
            x=['Node Coverage', 'Edge Coverage', 'Attribute Completeness'],
            y=[metrics['node_coverage'], metrics['edge_coverage'], metrics['attribute_completeness']],
            text=[f"{metrics['node_coverage']}%", f"{metrics['edge_coverage']}%", f"{metrics['attribute_completeness']}%"],
            textposition='auto',
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
        ))
        
        fig.update_layout(
            title="Completeness Metrics (%)",
            yaxis_title="Percentage",
            yaxis_range=[0, 100],
            template="plotly_white"
        )
        
        return fig
    finally:
        session.close()


@callback(
    Output("efficiency-metrics", "figure"),
    Input("efficiency-metrics", "id")
)
def update_efficiency_metrics(_):
    """Update efficiency metrics visualization"""
    G = get_network()
    
    if G is None or G.number_of_nodes() == 0:
        return create_empty_figure("No data available")
    
    metrics = calculate_efficiency_metrics(G)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Total Nodes', 'Total Edges'],
        y=[metrics['total_nodes'], metrics['total_edges']],
        text=[str(metrics['total_nodes']), str(metrics['total_edges'])],
        textposition='auto',
        marker_color=['#1f77b4', '#ff7f0e']
    ))
    
    fig.update_layout(
        title="Graph Size Metrics",
        yaxis_title="Count",
        template="plotly_white"
    )
    
    return fig


@callback(
    Output("robustness-metrics", "figure"),
    Input("robustness-metrics", "id")
)
def update_robustness_metrics(_):
    """Update robustness metrics visualization"""
    G = get_network()
    
    if G is None or G.number_of_nodes() == 0:
        return create_empty_figure("No data available")
    
    metrics = calculate_robustness_metrics(G)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Self Loops', 'Isolated Nodes', 'Components', 'Invalid Edges'],
        y=[metrics['self_loops'], metrics['isolated_nodes'], 
           metrics['number_of_components'], metrics['invalid_edges']],
        text=[str(metrics['self_loops']), str(metrics['isolated_nodes']),
              str(metrics['number_of_components']), str(metrics['invalid_edges'])],
        textposition='auto',
        marker_color=['#d62728', '#9467bd', '#8c564b', '#e377c2']
    ))
    
    fig.update_layout(
        title="Robustness Metrics",
        yaxis_title="Count",
        template="plotly_white"
    )
    
    return fig


@callback(
    Output("resilience-metrics", "figure"),
    Input("resilience-metrics", "id")
)
def update_resilience_metrics(_):
    """Update resilience metrics visualization"""
    G = get_network()
    
    if G is None or G.number_of_nodes() == 0:
        return create_empty_figure("No data available")
    
    metrics = calculate_resilience_metrics(G)
    
    fig = go.Figure()
    
    # Create metrics for visualization
    metric_names = ['Components', 'Articulation Points']
    metric_values = [metrics['number_of_components'], metrics['articulation_points']]
    
    fig.add_trace(go.Bar(
        x=metric_names,
        y=metric_values,
        text=[str(v) for v in metric_values],
        textposition='auto',
        marker_color=['#1f77b4', '#ff7f0e']
    ))
    
    fig.update_layout(
        title=f"Resilience Metrics (Connected: {metrics['is_connected']})",
        yaxis_title="Count",
        template="plotly_white"
    )
    
    return fig


def create_empty_figure(message="No data available"):
    """Create an empty figure with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20, color="gray")
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly_white"
    )
    return fig