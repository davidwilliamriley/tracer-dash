# views/reports_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import List, Dict, Any, Union, TypedDict


class DropdownOption(TypedDict):
    """Type definition for dropdown options"""

    label: str
    value: str
    disabled: bool


class ReportView:
    """View layer for Reports page - handles UI Layout and Components"""

    def _create_toast(self) -> dbc.Toast:
        return dbc.Toast(
            id="networks-toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            style={
                "position": "fixed",
                "bottom": 20,
                "left": 20,
                "width": 350,
                "z-index": 9999,
            },
        )

    def _create_report_selector(self, report_options: List[DropdownOption]) -> html.Div:
        return html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id="report-select",
                            options=report_options,  # type: ignore[arg-type]
                            value="",  # No Default
                            placeholder="Select a Report to View...",
                            className="mb-0",
                            style={"width": "100%"},
                        )
                    ], width=11),
                    dbc.Col([
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-1"), "Reset"],
                                    id="report-reset-btn",
                                    outline=True,
                                    color="primary",
                                    size="md",
                                    className="mb-0",
                                    style={"width": "100%"},
                                )
                    ], width=1),
                ], className="g-2", style={"padding": "0"}),
            ], className="mb-4", style={"border": "none"},
        )

    def create_layout(self, report_options: List[DropdownOption]) -> "dbc.Container":
        return dbc.Container(
            [
                self._create_toast(),

                html.H1([html.I(className="bi bi-file-earmark-richtext me-2"), "Reports"], className="my-4"),
                html.P("Report for the Network", className="mb-4 text-muted"),

                self._create_report_selector(report_options),
                
                # PDF Viewer
                
                dbc.Row([
                    dbc.Col([
                        html.Div(id="pdf-viewer-container",
                                children=[html.Iframe(
                                    id="pdf-iframe", src="/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/dummy.pdf",
                                            style={
                                                "width": "100%",
                                                "height": "80vh",
                                                "border": "solid 1px gainsboro",
                                            },
                                        )
                                    ], style={"height": "80vh"})
                    ], width=12),
                ], className="mb-0" ),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "100px",
                "display": "flex",
                "flexDirection": "column",
            },
        )
