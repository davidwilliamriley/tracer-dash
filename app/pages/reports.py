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

# Callback for PDF viewer updates
@callback(
    Output("pdf-iframe", "src"),
    [Input("report-select", "value")]
)
def update_pdf_viewer(selected_report):
    return report_controller.get_pdf_viewer_url(selected_report)