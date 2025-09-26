# pages/breakdowns.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc

# MVC Imports
from controllers.breakdowns_controller import BreakdownController
from views.breakdowns_view import BreakdownView

register_page(
    __name__, 
    path="/breakdowns",
    name="Breakdowns",
    title="Tracer - Breakdowns"
)

breakdown_controller = BreakdownController(model=None)
breakdown_view = BreakdownView()

layout = breakdown_view.create_layout()

