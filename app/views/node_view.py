# views/node_view.py

# Import Libaries
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import Any, Dict, List

# Import Model, View and Utils
from utils.toast_utils import ToastFactory


class NodeView:
    def __init__(self):
        pass

    def _make_toast(self) -> dbc.Toast:
        return ToastFactory.create_toast()

    def _create_content_header(self) -> html.Div:
        return html.Div(
            [
                html.H1(
                    [html.I(className="bi bi-plus-circle me-2"), "Nodes"],
                    className="my-4 text-primary",
                ),
                html.P("Manage the Network Nodes", className="mb-4 text-muted"),
            ],
        )

    def _create_toolbar(self) -> html.Div:
        return html.Div(
            [
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
                                                "Create Node",
                                            ],
                                            id="nodes-create-btn",
                                            outline=True,
                                            color="primary",
                                            title="Create a new Node",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(
                                                    className="bi bi-arrow-clockwise me-2"
                                                ),
                                                "Refresh Nodes",
                                            ],
                                            id="nodes-refresh-btn",
                                            outline=True,
                                            color="primary",
                                            title="Refresh the Nodes Table",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-trash me-2"),
                                                "Delete Node(s)",
                                            ],
                                            id="nodes-delete-btn",
                                            outline=True,
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
                                                "Print PDF",
                                            ],
                                            id="nodes-print-btn",
                                            outline=True,
                                            color="primary",
                                            title="Print the Table to PDF",
                                        ),
                                        dbc.Button(
                                            [
                                                html.I(className="bi bi-download me-2"),
                                                "Download CSV",
                                            ],
                                            id="nodes-download-btn",
                                            outline=True,
                                            color="primary",
                                            title="Download the Table as CSV",
                                        ),
                                    ],
                                ),
                            ],
                            className="col-md-6 d-flex justify-content-end",
                        ),
                    ],
                    className="row justify-content-between mb-3",
                )
            ]
        )

    def create_layout(self, nodes_data: List[Dict[str, Any]]) -> "dbc.Container":
        return dbc.Container(
            [
                # Toast notification
                ToastFactory.create_toast(),
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
                        html.Div(
                            id="nodes-table-data-store", style={"display": "none"}
                        ),
                        # Modals
                        self._create_create_modal(),
                        self._create_delete_modal(),
                        # Hidden Download Component
                        dcc.Download(id="nodes-download-csv"),
                        dcc.Download(id="nodes-print-pdf"),
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

    def _create_table(self, nodes_data: List[Dict[str, Any]]) -> html.Div:
        """Create Tabulator Table"""
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
                                            id="nodes-new-identifier",
                                            type="text",
                                            placeholder="Enter an (optional) Identifier",
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
                                            id="nodes-new-name",
                                            type="text",
                                            placeholder="Enter a Node Name (Required)",
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
                                            id="nodes-new-description",
                                            placeholder="Enter an (optional) Description",
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
                            id="nodes-confirm-create",
                            outline=True,
                            color="primary",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel",
                            id="nodes-cancel-create",
                            outline=True,
                            color="secondary",
                        ),
                    ]
                ),
            ],
            id="nodes-create-modal",
            is_open=False,
            backdrop="static",
        )

    def _create_delete_modal(self) -> dbc.Modal:
        """Create modal for delete confirmation"""
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
                dbc.ModalBody(html.Div(id="nodes-delete-modal-body")),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Delete",
                            id="nodes-confirm-delete",
                            outline=True,
                            color="danger",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel",
                            id="nodes-cancel-delete",
                            outline=True,
                            color="secondary",
                        ),
                    ]
                ),
            ],
            id="nodes-delete-modal",
            is_open=False,
            backdrop="static",
        )

    def create_delete_confirmation(self, selected_names: List[str]) -> html.Div:
        return html.Div(
            [
                html.P(f"Confirm Deletion of {len(selected_names)} Node(s)?"),
                html.Ul([html.Li(name) for name in selected_names]),
                html.P("You cannot undo this Action!", className="text-danger fw-bold"),
            ]
        )
