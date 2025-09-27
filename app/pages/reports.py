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

# Initialize MVC components
report_controller = ReportController(model=None)
report_view = ReportView(controller=report_controller)

# Create the Layout
layout = report_view.create_layout()

# Callback to reset the Dropdown
@callback(
    Output("report-select", "value"),
    Input("report-reset-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_dropdown(n_clicks):
    if n_clicks:
        return ""
    return dash.no_update

# Callback to update the PDF Viewer
@callback(
    Output("pdf-iframe", "src"),
    [Input("report-select", "value")]
)
def update_pdf_viewer(selected_report):
    return report_controller.get_pdf_viewer_url(selected_report)