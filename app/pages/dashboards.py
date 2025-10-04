# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc

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
    # Example data - replace with your actual system health metrics
    data = [
        {"Metric": "No. of Edges", "Value": "100"},
        {"Metric": "No. of Nodes", "Value": "51"}
    ]
    
    columns = [
        {"name": "Metric", "id": "Metric"},
        {"name": "Value", "id": "Value"}
        # {"name": "Status", "id": "Status"}
    ]
    
    return data, columns