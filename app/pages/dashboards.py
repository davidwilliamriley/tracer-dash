# pages/dashboards.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc

# MVC Imports
from controllers.dashboards_controller import DashboardController
from views.dashboards_view import DashboardView

register_page(
    __name__, 
    path="/dashboards",
    name="Dashboards",
    title="Tracer - Dashboards"
)

dashboard_controller = DashboardController(model=None)
dashboard_view = DashboardView()

layout = dashboard_view.create_layout()

