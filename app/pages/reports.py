# pages/reports.py

import dash
from dash import html, Input, Output, callback, register_page, no_update
import dash_bootstrap_components as dbc
from typing import List, Dict, Any

# MVC Imports
from views.report_view import ReportView, DropdownOption

register_page(__name__, path="/reports", name="Reports", title="Tracer - Reports")

# Initialize view
report_view = ReportView()

# ==================== HELPER FUNCTIONS ====================


def get_available_reports() -> List[DropdownOption]:
    """Get list of available reports"""
    return [
        {
            "label": "System Requirements Specification",
            "value": "Report_00.pdf",
            "disabled": False,
        },
        {"label": "System Definition", "value": "Report_01.pdf", "disabled": True},
        {
            "label": "System Breakdown Structure",
            "value": "Report_02.pdf",
            "disabled": True,
        },
        {"label": "Interface Register", "value": "Report_03.pdf", "disabled": True},
        {
            "label": "Project Scope Allocation Matrix",
            "value": "Report_04.pdf",
            "disabled": False,
        },
        {"label": "Assurance Case", "value": "Report_05.pdf", "disabled": True},
        {"label": "Safety Case", "value": "Report_06.pdf", "disabled": True},
        {"label": "Completions Checklist", "value": "Report_07.pdf", "disabled": True},
    ]


def get_pdf_viewer_url(selected_report: str) -> str:
    """Generate PDF viewer URL based on selected report"""
    if not selected_report:
        return (
            "/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/dummy.pdf"
        )

    return f"/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/{selected_report}"


# ==================== LAYOUT ====================


def layout():
    """Create the Layout"""
    report_options = get_available_reports()
    return report_view.create_layout(report_options)


# ==================== CALLBACKS ====================


# Callback to reset the Dropdown
@callback(
    Output("report-select", "value"),
    Input("report-reset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_dropdown(n_clicks):
    """Reset the report dropdown to empty"""
    if n_clicks:
        return ""
    return no_update


# Callback to update the PDF Viewer
@callback(Output("pdf-iframe", "src"), Input("report-select", "value"))
def update_pdf_viewer(selected_report):
    """Update PDF viewer when report is selected"""
    return get_pdf_viewer_url(selected_report)
