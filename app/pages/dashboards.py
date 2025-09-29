# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc

# MVC Imports
from views.dashboard_view import DashboardView

register_page(
    __name__, 
    path="/dashboards",
    name="Dashboards",
    title="Tracer - Dashboards"
)

dashboard_view = DashboardView()

layout = dashboard_view.create_layout()

