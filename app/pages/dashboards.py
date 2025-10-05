# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
import networkx as nx

# MVC Imports
from views.dashboard_view import DashboardView
from utils.cache_utils import get_network  # Import from cache module instead of app

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
            {"Metric": "No. of Edges", "Value": str(num_edges)},
            {"Metric": "No. of Nodes", "Value": str(num_nodes)},
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