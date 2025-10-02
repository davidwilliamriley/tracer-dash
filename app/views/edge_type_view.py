# views/edge_type_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any


class EdgeTypeView:
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

    def _create_content_header(self):
        """Create page header"""
        return html.Div(
            [
                html.H1([html.I(className="bi bi-link-45deg me-2"), "Edge Types"], className="my-4"),
                html.P("Manage the Edge Types", className="mb-4"),
            ]
        )

    def _create_toolbar(self) -> html.Div:
            return html.Div(
                [
                    html.Div(
                        [
                            dbc.ButtonGroup(
                                [
                                    dbc.Button(
                                        [html.I(className="bi bi-plus-lg me-2"), "Create"],
                                        id="create-edge-type-btn",
                                        color="primary",
                                        title="Create a new Edge Type",
                                    ),
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-arrow-clockwise me-2"),
                                            "Refresh",
                                        ],
                                        id="refresh-edge-types-btn",
                                        color="primary",
                                        title="Refresh the Edge Types Table",
                                    ),
                                    dbc.Button(
                                        [html.I(className="bi bi-trash me-2"), "Delete"],
                                        id="delete-edge-type-btn",
                                        color="warning",
                                        title="Delete a selected Edge Type",
                                        disabled=True,
                                    ),
                                ],
                            ),
                        ],
                        className="col-md-6",
                    ),
                    html.Div(
                        [
                            dbc.ButtonGroup(
                                [
                                    dbc.Button(
                                        [html.I(className="bi bi-printer me-2"), "Print"],
                                        id="print-edge-types-btn",
                                        color="primary",
                                        title="Print the Table to PDF",
                                    ),
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-download me-2"),
                                            "Download",
                                        ],
                                        id="download-edge-types-btn",
                                        color="primary",
                                        title="Download the Table as CSV",
                                    ),
                                ],
                            ),
                        ],
                        className="col-md-6 d-flex justify-content-end",
                    ),
                ],
                className="row justify-content-between mb-3 edge-types-toolbar",
            )

    def create_layout(self, edge_types: List[Dict[str, Any]]) -> "dbc.Container":
        return dbc.Container(
            [
                self._make_toast(),
                
                dbc.Stack(
                    [
                        self._create_content_header(), 

                        html.Div(
                            [
                                self._create_toolbar()
                            ]
                        ),
                        
                        html.Div(
                            [
                                self._render_table(edge_types)
                            ]
                        ),
                        html.Div(id="table-data-store", style={"display": "none"}),

                        self._render_create_modal(),
                        self._render_delete_modal(),

                        dcc.Download(id="download-edge-types-csv"),
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

    def _render_table(self, edge_types: List[Dict[str, Any]]) -> html.Div:
        """
        Render the edge types table

        Args:
            edge_types: List of edge type dictionaries to display

        Returns:
            html.Div containing the table component
        """
        return html.Div(
            [
                dash_tabulator.DashTabulator(
                    id="edge-types-table",
                    theme="tabulator",
                    data=edge_types,
                    columns=[
                        {
                            "title": "ID",
                            "field": "ID",
                            "width": 300,
                            "headerFilter": True,
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
                        "printHeader": "Edge Types Table",
                    },
                )
            ]
        )

    def _render_create_modal(self) -> dbc.Modal:
        """Render the create edge type modal"""
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Create New Edge Type")),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label("Identifier:", className="fw-bold"),
                                        dbc.Input(
                                            id="new-edge-type-identifier",
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
                                            id="new-edge-type-name",
                                            type="text",
                                            placeholder="Enter edge type name*",
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
                                            id="new-edge-type-description",
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
                            "Create Edge Type",
                            id="confirm-create-edge-type",
                            color="primary",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel", id="cancel-create-edge-type", color="secondary"
                        ),
                    ]
                ),
            ],
            id="create-edge-type-modal",
            is_open=False,
            backdrop="static",
        )

    def _render_delete_modal(self) -> dbc.Modal:
        """Render the delete confirmation modal"""
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
                dbc.ModalBody(html.Div(id="delete-modal-body")),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Delete",
                            id="confirm-delete-edge-type",
                            color="danger",
                            className="me-2",
                        ),
                        dbc.Button(
                            "Cancel", id="cancel-delete-edge-type", color="secondary"
                        ),
                    ]
                ),
            ],
            id="delete-edge-type-modal",
            is_open=False,
            backdrop="static",
        )

    @staticmethod
    def create_delete_modal_body(selected_names: List[str]) -> html.Div:
        """
        Create the content for the delete confirmation modal

        Args:
            selected_names: List of edge type names to be deleted

        Returns:
            html.Div containing the modal body content
        """
        return html.Div(
            [
                html.P(
                    f"Are you sure you want to delete the following {len(selected_names)} edge type(s)?"
                ),
                html.Ul([html.Li(name) for name in selected_names]),
                html.P(
                    "This action cannot be undone.", className="text-danger fw-bold"
                ),
            ]
        )
