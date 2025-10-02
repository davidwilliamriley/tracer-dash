# views/node_view.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import Any, Dict, List


class NodeView:
    def __init__(self):
        pass

    def _make_toast(self) -> dbc.Toast:
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
    
    def _create_content_header(self) -> html.Div:
        """Create page header"""
        return html.Div(
            [
                html.H1([html.I(className="bi bi-plus-circle me-2"), "Nodes"], className="my-4"),
                html.P("Manage the Network Nodes", className="mb-4 text-muted"),
            ],
        )

    def create_layout(self, nodes_data: List[Dict[str, Any]]) -> "dbc.Container":
            """Create the main layout for the Nodes page"""
            return dbc.Container(
                [
                    # Toast notification
                    self._make_toast(),
                    
                    # Main Content Stack
                    dbc.Stack(
                        [
                            # Content Header
                            self._create_content_header(),

                            # Controls
                            html.Div(
                                [
                                    self._create_toolbar(),
                                ]
                            ),

                            # Main Content
                            html.Div(
                                [
                                    self._create_table(nodes_data),
                                ],
                            ),
                            html.Div(id="table-data-store", style={"display": "none"}),
                                                        
                            # Modals
                            self._create_create_modal(),
                            self._create_delete_modal(),

                            # Hidden Download Component
                            dcc.Download(id="download-nodes-csv"),
                        ]
                    )
                ],
                style={
                    "minHeight": "calc(100vh - 120px)",
                    "paddingBottom": "100px",
                    "display": "flex",
                    "flexDirection": "column",
                },
            )

    def _create_toolbar(self) -> html.Div:
            """Create toolbar with action buttons"""
            return html.Div([
                html.Div(
                        [
                            # Left side buttons
                            html.Div(
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
                                                title="Delete selected Node(s)",
                                                disabled=True,
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-md-6",
                            ),
                            # Right side buttons
                            html.Div(
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
                                        ],
                                    ),
                                ],
                                className="col-md-6 d-flex justify-content-end",
                            ),
                        ],
                        className="row justify-content-between mb-3 nodes-toolbar",
                    ),
                ]
            )

    # def _create_table_container(self, nodes_data: List[Dict[str, Any]]) -> html.Div:
    #     """Create main content area with toolbar and table"""
    #     return html.Div(
    #         [
    #             # Toolbar
    #             self._create_toolbar(),
    #             # Table
    #             self._create_table(nodes_data),
    #         ],
    #         className="container-fluid px-4 py-5",
    #     )

    def _create_table(self, nodes_data: List[Dict[str, Any]]) -> html.Div:
        """Create Tabulator table"""
        return html.Div(
            [
                dash_tabulator.DashTabulator(
                    id="nodes-table",
                    theme="tabulator",
                    data=nodes_data,
                    columns=[
                        {
                            "title": "ID",
                            "field": "ID",
                            "width": 300,
                            "headerFilter": False,
                            "editor": False,
                            "visible": False,
                        },
                        {
                            "title": "Identifier",
                            "field": "Identifier",
                            "width": 200,
                            "headerFilter": True,
                            "editor": "input",
                        },
                        {
                            "title": "Name",
                            "field": "Name",
                            "width": 300,
                            "headerFilter": True,
                            "editor": "input",
                        },
                        {
                            "title": "Description",
                            "field": "Description",
                            "headerFilter": True,
                            "editor": "input",
                        },
                    ],
                    options={
                        "selectable": True,
                        "selectableRangeMode": "click",
                        "pagination": "local",
                        "paginationSize": 10,
                        "paginationSizeSelector": [5, 10, 20, 50],
                        "paginationButtonCount": 5,
                        "paginationCounter": "rows",
                        "movableColumns": True,
                        "resizableColumns": True,
                        "layout": "fitDataStretch",
                        "responsiveLayout": "hide",
                        "tooltips": True,
                        "clipboard": True,
                        "printAsHtml": True,
                        "printHeader": "Nodes Table",
                    },
                )
            ]
        )

    def _create_create_modal(self) -> dbc.Modal:
        """Create modal for creating new nodes"""
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Create New Node")),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Identifier:", className="fw-bold"),
                                        dbc.Input(
                                            id="new-node-identifier",
                                            type="text",
                                            placeholder="Enter unique identifier (optional)",
                                        ),
                                    ],
                                    width=12,
                                    className="mb-3",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Name:", className="fw-bold"),
                                        dbc.Input(
                                            id="new-node-name",
                                            type="text",
                                            placeholder="Enter node name*",
                                            required=True,
                                        ),
                                    ],
                                    width=12,
                                    className="mb-3",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Description:", className="fw-bold"),
                                        dbc.Textarea(
                                            id="new-node-description",
                                            placeholder="Enter description (optional)",
                                            rows=3,
                                        ),
                                    ],
                                    width=12,
                                )
                            ]
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Create Node",
                            id="confirm-create-node",
                            color="primary",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel", id="cancel-create-node", color="secondary"
                        ),
                    ]
                ),
            ],
            id="create-node-modal",
            is_open=False,
            backdrop="static",
        )

    def _create_delete_modal(self) -> dbc.Modal:
        """Create modal for delete confirmation"""
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
                dbc.ModalBody(html.Div(id="delete-modal-body")),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Delete",
                            id="confirm-delete-node",
                            color="danger",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel", id="cancel-delete-node", color="secondary"
                        ),
                    ]
                ),
            ],
            id="delete-node-modal",
            is_open=False,
            backdrop="static",
        )

    def create_delete_confirmation(self, selected_names: List[str]) -> html.Div:
        """Create delete confirmation message body"""
        return html.Div(
            [
                html.P(
                    f"Are you sure you want to delete the following {len(selected_names)} node(s)?"
                ),
                html.Ul([html.Li(name) for name in selected_names]),
                html.P(
                    "This action cannot be undone.", className="text-danger fw-bold"
                ),
            ]
        )
