# views/edges_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
import json
from typing import List, Dict, Any

class EdgeView:
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
                "top": 100,
                "left": 20,
                "width": 350,
                "z-index": 9999
            }
        )

    def _create_content_header(self):
        return html.Div(
            [
                html.H1([html.I(className="bi bi-arrow-repeat me-2"), "Edges"], className="my-4 text-primary"),
                html.P("Create, Modify and / or Delete the Edges between the Nodes of the Network ", className="mb-4 text-muted"),
            ]
        )

    def _create_toolbar(self) -> html.Div:
        return html.Div([
            html.Div([
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button(
                            [html.I(className="bi bi-plus-lg me-2"), "Create Edge"],
                            id="create-edge-btn",
                            outline=True,
                            color="primary",
                            title="Create a new Edge"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-arrow-clockwise me-2"), "Refresh Edges"],
                            id="refresh-edges-btn",
                            outline=True,
                            color="primary",
                            title="Refresh the Edges Table"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-trash me-2"), "Delete Edge(s)"],
                            id="delete-edge-btn",
                            outline=True,   
                            color="warning",
                            title="Delete selected Edge(s)",
                            disabled=True
                        ),
                    ]),
                ], className="col-md-6"),
                
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button(
                            [html.I(className="bi bi-printer me-2"), "Print PDF"],
                            id="print-edges-btn",
                            outline=True,
                            color="primary",
                            title="Print the Table to PDF"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-download me-2"), "Download CSV"],
                            id="download-edges-btn",
                            outline=True,
                            color="primary",
                            title="Download the Table as CSV"
                        ),
                    ]),
                ], className="col-md-6 d-flex justify-content-end"),
            ], className="row justify-content-between mb-3 edges-toolbar"),
        ])
     
    def create_layout(self, edges_data: List[Dict[str, Any]], node_label_map: Dict[str, str], edge_type_label_map: Dict[str, str]) -> dbc.Container:
        """Create the main layout for the Edges Page"""
        return dbc.Container([
                # Toast Notification
                self._make_toast(),

                dbc.Stack(
                    [
                        # Main Content Header
                        self._create_content_header(),

                        # Controls and Table
                        html.Div(
                            [
                                self._create_toolbar(),
                            ]
                        ),

                        # Main Content
                        html.Div(
                            [
                                self._create_table(edges_data, node_label_map, edge_type_label_map),
                            ],
                        ),
                        html.Div(id="table-data-store", style={"display": "none"}),

                        # Modals
                        self._create_create_modal(),
                        self._create_delete_modal(),
                    
                        # Hidden download component
                        dcc.Download(id="download-edges-csv"),
                        dcc.Download(id="print-edges-pdf"),
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
 
    def _create_table(
        self,
        edges_data: List[Dict[str, Any]],
        node_label_map: Dict[str, str],
        edge_type_label_map: Dict[str, str]
    ) -> html.Div:
        """Create Tabulator Table"""
        return html.Div([
            dash_tabulator.DashTabulator(
                id='edges-table',
                theme='tabulator',
                data=edges_data,
                columns=[
                    {"title": "ID", "field": "ID", "headerFilter": False, "visible": False},
                    {
                        "title": "Identifier", 
                        "field": "Identifier", 
                        "headerFilter": "input", 
                        "headerFilterParams": {"clearable": True},
                        "headerFilterPlaceholder": "Filter by Identifier...", 
                        "editor": "input"
                    },
                    {"title": "Source_UUID", "field": "Source_UUID", "headerFilter": False, "visible": False},
                    {
                        "title": "Source",
                        "field": "Source",
                        "headerFilter": "input",
                        "headerFilterParams": {"clearable": True},
                        "headerFilterPlaceholder": "Filter by Source...",
                        "editor": "select",
                        "editorParams": {"values": node_label_map}
                    },
                    {"title": "Edge_Type_UUID", "field": "Edge_Type_UUID", "headerFilter": False, "visible": False},
                    {
                        "title": "Edge Type", 
                        "field": "Edge Type", 
                        "headerFilter": "input",
                        "headerFilterParams": {"clearable": True},
                        "headerFilterPlaceholder": "Filter by Edge Type...",
                        "editor": "select", 
                        "editorParams": {"values": edge_type_label_map}
                    },
                    {"title": "Target_UUID", "field": "Target_UUID", "headerFilter": False, "visible": False},
                    {
                        "title": "Target",
                        "field": "Target",
                        "headerFilter": "input",
                        "headerFilterParams": {"clearable": True},
                        "headerFilterPlaceholder": "Filter by Target...",
                        "editor": "select",
                        "editorParams": {"values": node_label_map}
                    },
                    {
                        "title": "Description", 
                        "field": "Description", 
                        "headerFilter": "input",
                        "headerFilterPlaceholder": "Filter by Description...", 
                        "editor": "input"}
                ],
                options={
                    "selectable": True,
                    "selectableRangeMode": "click",
                    "editTriggerEvent": "click",
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
                    "printHeader": "Edges Table",
                }
            )
        ])
    
    def _create_create_modal(self) -> dbc.Modal:
        """Create modal for creating new edges"""
        return dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create New Edge")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Identifier:", className="fw-bold"),
                        dbc.Input(
                            id="new-edge-identifier",
                            type="text",
                            placeholder="Enter an (optional) Identifier"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Source Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-source",
                            placeholder="Select the Source Node (Required)",
                            clearable=False
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Edge Type:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-type",
                            placeholder="Select the Edge Type (Required)",
                            clearable=False
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Target Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-target",
                            placeholder="Select the Target Node (Required)",
                            clearable=False
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-edge-description",
                            placeholder="Enter an (optional) Description",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Create Edge",
                    id="confirm-create-edge",
                    outline=True,
                    color="primary",
                    className="me-2"
                ),
                dbc.Button(
                    "Cancel",
                    id="cancel-create-edge",
                    outline=True,
                    color="secondary"
                )
            ])
        ], id="create-edge-modal", is_open=False, backdrop="static", size="md")
    
    def _create_delete_modal(self) -> dbc.Modal:
        return dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button(
                    "Delete",
                    id="confirm-delete-edge",
                    outline=True,
                    color="danger",
                    className="me-2"
                ),
                dbc.Button(
                    "Cancel",
                    id="cancel-delete-edge",
                    outline=True,
                    color="secondary"
                )
            ])
        ], id="delete-edge-modal", is_open=False, backdrop="static")
    
    def create_delete_confirmation(
        self,
        selected_edges: List[str],
        raw_selected_rows: List[Dict[str, Any]]
    ) -> html.Div:
        return html.Div([
            html.P(f"Confirm Deletion of {len(selected_edges)} Edge(s)?"),
            html.Ul([html.Li(edge) for edge in selected_edges]),
            html.P("YYou cannot undo this Action.", className="text-danger fw-bold"),
            # Store the raw selected rows data in a hidden div
            html.Div(
                id="raw-selected-data",
                children=json.dumps(raw_selected_rows),
                style={"display": "none"}
            )
        ])