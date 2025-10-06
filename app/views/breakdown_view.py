# views/breakdowns_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import List, Dict, Any, Union, TypedDict


class DropdownOption(TypedDict):
    """Type definition for Dropdown Options"""

    label: str
    value: str
    disabled: bool


class BreakdownView:
    def __init__(self):
        self.controller = None

    def _make_toast(self) -> dbc.Toast:
        return dbc.Toast(
            id="toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            style={
                "position": "fixed",
                "top": 100,
                "left": 20,
                "width": 350,
                "z-index": 9999,
            },
        )

    def _create_content_header(self):
        """Create page header"""
        return html.Div(
            [
                html.H1(
                    [html.I(className="bi bi-diagram-2 me-2"), "Breakdowns"],
                    className="my-4 text-primary",
                ),
                html.P(
                    "Manage System and Subsystem Breakdowns",
                    className="mb-4 text-muted",
                ),
            ],
        )

    def create_layout(self, breakdown_options: List[DropdownOption]) -> "dbc.Container":
        """Create the main layout for the Breakdown View"""
        return dbc.Container(
            [
                # Toast Notification
                self._make_toast(),
                dcc.Download(id="breakdowns-download-pdf"),
                # Main Content Stack
                dbc.Stack(
                    [
                        # Content Header
                        self._create_content_header(),
                        # Controls
                        html.Div(
                            [
                                self._create_breakdown_selection(breakdown_options),
                                html.Hr(),
                                self._create_toolbar(),
                            ]
                        ),
                        # Main Content
                        html.Div(
                            [
                                self._create_table_container(),
                            ],
                        ),
                        html.Div(
                            id="breakdowns-table-data-store", style={"display": "none"}
                        ),
                    ]
                ),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "100px",
                "display": "flex",
                "flexDirection": "column",
            },
        )

    def _create_toolbar(self):
        """Create action button toolbar"""
        return html.Div(
            [
                dbc.Row(
                    [
                        # Left Side Button Group
                        dbc.Col(
                            [
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-plus-lg me-2"),
                                                "Create",
                                            ],
                                            id="breakdowns-create-btn",
                                            outline=True,
                                            color="primary",
                                            title="Create a new Node",
                                            disabled=True,
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className="bi bi-arrow-clockwise me-2"
                                                ),
                                                "Refresh",
                                            ],
                                            id="breakdowns-refresh-btn",
                                            outline=True,
                                            color="primary",
                                            title="Refresh the Nodes Table",
                                            disabled=True,
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-trash me-2"),
                                                "Delete",
                                            ],
                                            id="breakdowns-delete-btn",
                                            outline=True,
                                            color="warning",
                                            title="Delete a selected Node",
                                            disabled=True,
                                        ),
                                    ]
                                )
                            ],
                            className="col-md-6",
                        ),
                        # Right Side Button Group
                        dbc.Col(
                            [
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-printer me-2"),
                                                "Print PDF",
                                            ],
                                            id="breakdowns-print-btn",
                                            outline=True,
                                            color="primary",
                                            title="Print the Table to PDF",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-download me-2"),
                                                "Download CSV",
                                            ],
                                            id="breakdowns-download-btn",
                                            outline=True,
                                            color="primary",
                                            title="Download the Table as CSV",
                                        ),
                                    ]
                                )
                            ],
                            className="col-md-6 d-flex justify-content-end",
                        ),
                    ],
                    className="row justify-content-between mb-3",
                )
            ]
        )

    def _create_breakdown_selection(
        self, breakdown_options: List[DropdownOption]
    ) -> html.Div:
        return html.Div(
            [
                # Breakdown Selection Row
                dbc.Card(
                    [
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="breakdowns-dropdown",
                                            options=breakdown_options,  # type: ignore[arg-type]
                                            value=None,  # No Default selection
                                            placeholder="Select a Breakdown...",
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
                                            id="breakdowns-reset-filter-btn",
                                            outline=True,
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

    def _create_table_container(self):
        """Create the table container for Tabulator"""
        return dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id="breakdowns-row-info", className="mb-2 text-muted"
                        ),  # Add this
                        html.Div(
                            id="breakdowns-tabulator-table",
                        ),
                    ]
                )
            ]
        )
