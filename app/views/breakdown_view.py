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

    def create_layout(self, breakdown_options: List[DropdownOption]) -> "dbc.Container":
        return dbc.Container(
            [
                # Toast Notification
                self._create_toast_notification(),

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
                                self._create_action_buttons(),
                            ]
                        ),
                        # Main Content
                        html.Div(
                            [
                                self._create_table_container(),
                            ]

                        ),
                        # html.Iframe(
                        #     id="breakdown-iframe",
                        #     src="https://copilot.microsoft.com/",
                        #     style={"width": "100%", "height": "600px", "border": "none"},
                        # )
                    ]
                ),
                # Hidden data store for Clientside Callbacks
                html.Div(id="table-data-store", style={"display": "none"}),
            ],
            fluid=True,
        )

    def _create_toast_notification(self):
        return dbc.Toast(
            id="toast-message",
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

    def _create_content_header(self):
        """Create page header"""
        return html.Div(
            [
                html.H1("Breakdowns", className="my-3"),
                html.P("Manage System and Subsystem Breakdowns", className="mb-4"),
            ],
            className="px-3",
        )

    def _create_action_buttons(self):
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
                                            id="create-node-btn",
                                            color="primary",
                                            title="Create a new Node",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className="bi bi-arrow-clockwise me-2"
                                                ),
                                                "Refresh",
                                            ],
                                            id="refresh-nodes-btn",
                                            color="primary",
                                            title="Refresh the Nodes Table",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-trash me-2"),
                                                "Delete",
                                            ],
                                            id="delete-node-btn",
                                            color="warning",
                                            title="Delete a selected Node",
                                            disabled=True,
                                        ),
                                    ]
                                )
                            ],
                            md=6,
                            className="d-flex justify-content-start",
                        ),
                        # Right Side Button Group
                        dbc.Col(
                            [
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-printer me-2"),
                                                "Print",
                                            ],
                                            id="print-nodes-btn",
                                            color="primary",
                                            title="Print the Table to PDF",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-download me-2"),
                                                "Download",
                                            ],
                                            id="download-nodes-btn",
                                            color="primary",
                                            title="Download the Table as CSV",
                                        ),
                                    ]
                                )
                            ],
                            md=6,
                            className="d-flex justify-content-end",
                        ),
                    ],
                    className="mb-3 px-3",
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
                                            id="breakdown-dropdown",
                                            options=breakdown_options,  # type: ignore[arg-type]
                                            value="",  # No Default
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
                                            id="reset-filter-btn",
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
            className="mb-4 px-3",
        )

    def _create_table_container(self):
        """Create the table container for Tabulator"""
        return dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id="row-info", className="mb-2 text-muted"
                        ),  # Add this
                        html.Div(
                            id="tabulator-table",
                        ),
                    ]
                )
            ],
            className="px-3",
        )
