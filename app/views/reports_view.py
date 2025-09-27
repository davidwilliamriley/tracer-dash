# views/reports_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any, Optional, Union


class ReportView:
    """View layer for Reports page - handles UI Layout and Components"""

    def __init__(self, controller=None):
        self.controller = controller

    def create_layout(self) -> dbc.Container:
        """Creates the layout for the Reports page"""
        return dbc.Container(
            [
                ReportView._create_toast(),
                self._create_header(),
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
            fluid=True,
            className="py-4",
        )

    @staticmethod
    def _create_toast() -> dbc.Toast:
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

    def _create_header(self) -> html.Div:
        """Create the header row for the Reports page"""
        return html.Div(
            [
                dbc.Row(dbc.Col(html.H1("Reports", className="mb-4"), width=12)),
                # dbc.Row(
                #     dbc.Col(
                #         html.P("Placeholder for the Report Server.", className="mb-4"),
                #         width=12,
                #     )
                # ),
                # Report Selection Row
                dbc.Card(
                    [
                        # dbc.CardHeader(html.H5("Select Report", className="mb-0")),
                        dbc.CardBody(
                            dcc.Dropdown(
                                id="report-select",
                                options=self._get_report_options(),  # type: ignore
                                value="",  # No Default
                                placeholder="Select a Report...",
                                className="mb-3",
                                style={"width": "100%"},
                            )
                        ),
                    ],
                    style={"border": "none"}
                ),
            ],
            className="mb-4",
        )

    def _get_report_options(self) -> List[Union[str, Dict[str, Any]]]:
        """
        Get the list of available report options for the dropdown
        Uses controller data if available, otherwise provides fallback

        Returns:
            List of report options with labels and values
        """
        if self.controller:
            return self.controller.get_available_reports()
        else:
            # Fallback if no controller provided
            return [
                {"label": "Select a Report Option...", "value": "", "disabled": True},
                {"label": "No reports available", "value": "", "disabled": True},
            ]
