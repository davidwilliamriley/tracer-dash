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

    def create_layout(self, report_options: List[DropdownOption]) -> "dbc.Container":
        """Creates the layout for the Reports page"""
        return dbc.Container(
            [
                self._create_toast(),
                self._create_header(report_options),
                # PDF Viewer Row
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    id="pdf-viewer-container",
                                    children=[
                                        html.Iframe(
                                            id="pdf-iframe",
                                            src="/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/dummy.pdf",
                                            style={
                                                "width": "100%",
                                                "height": "80vh",
                                                "border": "solid 1px gainsboro",
                                            },
                                        )
                                    ],
                                    style={"height": "80vh"},
                                )
                            ],
                            width=12,
                        )
                    ],
                    className="mb-0",
                ),
            ],
            className="py-4",
        )

    def _create_toast(self) -> dbc.Toast:
        """Create toast notification component"""
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

    def _create_header(self, report_options: List[DropdownOption]) -> html.Div:
        """Create the header row for the Reports page"""
        return html.Div(
            [
                dbc.Row(dbc.Col(html.H1("Reports", className="mb-4"), width=12)),
                # Report Selection Row
                dbc.Card(
                    [
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="report-select",
                                            options=report_options,  # type: ignore[arg-type]
                                            value="",  # No Default
                                            placeholder="Select a Report to View...",
                                            className="mb-0",
                                            style={"width": "100%"},
                                        ),
                                        width=11,
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className="bi bi-arrow-clockwise me-1"
                                                ),
                                                "Reset",
                                            ],
                                            id="report-reset-btn",
                                            color="primary",
                                            size="md",
                                            className="mb-0",
                                            style={"width": "100%"},
                                        ),
                                        width=1,
                                    ),
                                ],
                                className="g-2",
                            ),
                            style={"padding": "0"},
                        ),
                    ],
                    style={"border": "none"},
                ),
            ],
            className="mb-4",
        )
