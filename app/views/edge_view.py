# views/edges_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
import json
from typing import List, Dict, Any

class EdgeView:
    """View class for Edges page - handles all UI layout"""
    
    def create_layout(
        self,
        edges_data: List[Dict[str, Any]],
        node_label_map: Dict[str, str],
        edge_type_label_map: Dict[str, str]
    ) -> html.Div:
        """Create the main layout for the Edges page"""
        return html.Div([
            # Toast notification
            self._create_toast(),
            
            # Page header
            self._create_header(),
            
            # Main content with toolbar and table
            self._create_main_content(edges_data, node_label_map, edge_type_label_map),
            
            # Modals
            self._create_create_modal(),
            self._create_delete_modal(),
            
            # Hidden download component
            dcc.Download(id="download-edges-csv")
        ])
    
    def _create_toast(self) -> dbc.Toast:
        """Create toast notification component"""
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
                "z-index": 9999
            }
        )
    
    def _create_header(self) -> dbc.Container:
        """Create page header"""
        return dbc.Container([
            html.H1("Edges", className="my-4"),
            html.P(
                "Manage Edges in the system. Edges represent relationships between Nodes.",
                className="mb-4"
            )
        ], fluid=True, className="px-4")
    
    def _create_main_content(
        self,
        edges_data: List[Dict[str, Any]],
        node_label_map: Dict[str, str],
        edge_type_label_map: Dict[str, str]
    ) -> html.Div:
        """Create main content area with toolbar and table"""
        return html.Div([
            # Toolbar
            self._create_toolbar(),
            
            # Table
            self._create_table(edges_data, node_label_map, edge_type_label_map)
        ], className="container-fluid px-4 py-5")
    
    def _create_toolbar(self) -> html.Div:
        """Create toolbar with action buttons"""
        return html.Div([
            html.Div([
                # Left side buttons
                html.Div([
                    html.Div([
                        dbc.Button(
                            [html.I(className="bi bi-plus-lg me-2"), "Create"],
                            id="create-edge-btn",
                            color="primary",
                            className="me-2",
                            title="Create a new Edge"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"],
                            id="refresh-edges-btn",
                            color="primary",
                            className="me-2",
                            title="Refresh the Edges Table"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-trash me-2"), "Delete"],
                            id="delete-edge-btn",
                            color="warning",
                            title="Delete selected Edge(s)",
                            disabled=True
                        ),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                
                # Right side buttons
                html.Div([
                    html.Div([
                        dbc.Button(
                            [html.I(className="bi bi-printer me-2"), "Print"],
                            id="print-edges-btn",
                            color="primary",
                            className="me-2",
                            title="Print the Table to PDF"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-download me-2"), "Download"],
                            id="download-edges-btn",
                            color="primary",
                            title="Download the Table as CSV"
                        ),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 edges-toolbar"),
        ])
    
    def _create_table(
        self,
        edges_data: List[Dict[str, Any]],
        node_label_map: Dict[str, str],
        edge_type_label_map: Dict[str, str]
    ) -> html.Div:
        """Create Tabulator table"""
        return html.Div([
            dash_tabulator.DashTabulator(
                id='edges-table',
                theme='tabulator',
                data=edges_data,
                columns=[
                    {
                        "title": "ID",
                        "field": "ID",
                        "headerFilter": False,
                        "visible": False
                    },
                    {
                        "title": "Identifier",
                        "field": "Identifier",
                        "headerFilter": True,
                        "editor": "input"
                    },
                    {
                        "title": "Source_UUID",
                        "field": "Source_UUID",
                        "headerFilter": False,
                        "visible": False
                    },
                    {
                        "title": "Source",
                        "field": "Source",
                        "headerFilter": True,
                        "editor": "select",
                        "editorParams": {"values": node_label_map}
                    },
                    {
                        "title": "Edge_Type_UUID",
                        "field": "Edge_Type_UUID",
                        "headerFilter": False,
                        "visible": False
                    },
                    {
                        "title": "Edge Type",
                        "field": "Edge Type",
                        "headerFilter": True,
                        "editor": "select",
                        "editorParams": {"values": edge_type_label_map}
                    },
                    {
                        "title": "Target_UUID",
                        "field": "Target_UUID",
                        "headerFilter": False,
                        "visible": False
                    },
                    {
                        "title": "Target",
                        "field": "Target",
                        "headerFilter": True,
                        "editor": "select",
                        "editorParams": {"values": node_label_map}
                    },
                    {
                        "title": "Description",
                        "field": "Description",
                        "headerFilter": True,
                        "editor": "input"
                    }
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
                            placeholder="Enter unique identifier (optional)"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Source Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-source",
                            placeholder="Select source node*",
                            clearable=False
                        )
                    ], width=6, className="mb-3"),
                    dbc.Col([
                        dbc.Label("Target Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-target",
                            placeholder="Select target node*",
                            clearable=False
                        )
                    ], width=6, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Edge Type:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-type",
                            placeholder="Select edge type*",
                            clearable=False
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-edge-description",
                            placeholder="Enter description (optional)",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Create Edge",
                    id="confirm-create-edge",
                    color="primary",
                    className="me-2"
                ),
                dbc.Button(
                    "Cancel",
                    id="cancel-create-edge",
                    color="secondary"
                )
            ])
        ], id="create-edge-modal", is_open=False, backdrop="static", size="lg")
    
    def _create_delete_modal(self) -> dbc.Modal:
        """Create modal for delete confirmation"""
        return dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button(
                    "Delete",
                    id="confirm-delete-edge",
                    color="danger",
                    className="me-2"
                ),
                dbc.Button(
                    "Cancel",
                    id="cancel-delete-edge",
                    color="secondary"
                )
            ])
        ], id="delete-edge-modal", is_open=False, backdrop="static")
    
    def create_delete_confirmation(
        self,
        selected_edges: List[str],
        raw_selected_rows: List[Dict[str, Any]]
    ) -> html.Div:
        """Create delete confirmation message body"""
        return html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_edges)} edge(s)?"),
            html.Ul([html.Li(edge) for edge in selected_edges]),
            html.P("This action cannot be undone.", className="text-danger fw-bold"),
            # Store the raw selected rows data in a hidden div
            html.Div(
                id="raw-selected-data",
                children=json.dumps(raw_selected_rows),
                style={"display": "none"}
            )
        ])