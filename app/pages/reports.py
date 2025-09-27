# pages/reports.py

# Imports
import dash
from dash import html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc

# MVC Imports
from controllers.reports_controller import ReportController
from views.reports_view import ReportView

register_page(
    __name__, 
    path="/reports",
    name="Reports",
    title="Tracer - Reports"
)

report_controller = ReportController(model=None)
report_view = ReportView()

layout = report_view.create_layout()