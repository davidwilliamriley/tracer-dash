# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
import networkx as nx

# MVC Imports
from views.dashboard_view import DashboardView

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
def update_system_health_table(n):
    
    # G = get_network()

    if G is not None:
        # Example metrics - replace with actual calculations
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        density = nx.density(G) if num_nodes > 1 else 0

        data = [
            {"Metric": "No. of Edges", "Value": str(num_edges)},
            {"Metric": "No. of Nodes", "Value": str(num_nodes)},
            {"Metric": "Density", "Value": f"{density:.4f}"}
        ]
    else:
        data = [
            {"Metric": "No. of Nodes", "Value": "Loading..."},
            {"Metric": "No. of Edges", "Value": "Loading..."}
        ]

    columns = [
        {"name": "Metric", "id": "Metric"},
        {"name": "Value", "id": "Value"}
    ]
    
    return data, columns