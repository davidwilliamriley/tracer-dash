# views/breakdowns_view.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import List, Dict, Any
import json

class BreakdownView:
    def __init__(self):
        pass

    def create_layout(self):
        # current_graph = get_nodes_from_db()

        return dbc.Container([
                    dbc.Toast(
            id="toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000, 
            style={"position": "fixed", "bottom": 20, "left": 20, "width": 350, "z-index": 9999}
        ),

        dbc.Stack([
            # Page Header
            html.Div([
                html.H1("Header")
            ]),
                
            # Controls
            html.Div([
                    # Action buttons row
                    self._create_action_buttons(),
                    
                    # Graph selection row
                    self._create_graph_selection(),
                ]),
                
                # Main Content
                html.Div([
                    # Tabulator table
                    self._create_table_container(),
                ], style={'flex': '1'}),

                # Footer
                html.Div([
                    # Footer with pagination controls
                    self._create_pagination_footer(),
                ])
            ]),
            
            # Add Tabulator initialization script
            self._create_tabulator_script()
            
        ], fluid=True, style={
            "height": "100vh"
            # "margin": "0",
            # "padding": "0",
        })

    def _create_action_buttons(self):
        return html.Div([
            # Toolbar
            html.Div([
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-plus-lg me-2"), "Create"], 
                                 id="create-node-btn", color="primary", className="me-2", 
                                 title="Create a new Node"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"], 
                                 id="refresh-nodes-btn", color="primary", className="me-2", 
                                 title="Refresh the Nodes Table"),
                        dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                                 id="delete-node-btn", color="warning", 
                                 title="Delete a selected Node", disabled=True),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                                 id="print-nodes-btn", color="primary", className="me-2", 
                                 title="Print the Table to PDF"),
                        dbc.Button([html.I(className="bi bi-download me-2"), "Download"], 
                                 id="download-nodes-btn", color="primary", 
                                 title="Download the Table as CSV"),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 nodes-toolbar"),
        ], className="mb-3")

    def _create_graph_selection(self):
        """Create the graph selection dropdown"""
        return dbc.Row([
            dbc.Col([
                html.Label("Select the Graph:", className="form-label"),
                dcc.Dropdown(
                    id="graph-dropdown",
                    options=[
                        {"label": "Acceptance Verification Procedures (AVP)", "value": "avp"}
                    ],
                    value="avp",
                    className="mb-3"
                )
            ])
        ])

    def _create_table_container(self):
        """Create the table container for Tabulator"""
        return dbc.Row([
            dbc.Col([
                html.Div(id="tabulator-table", style={"minHeight": "400px"})
            ])
        ])

    def _create_pagination_footer(self):
        return
        # """Create the pagination footer"""
        # return dbc.Row([
        #     dbc.Col([
        #         html.Div([
        #             html.Span("", id="row-info", className="text-muted"),
        #             html.Div([
        #                 html.Span("Page Size", className="me-2"),
        #                 dcc.Dropdown(
        #                     id="page-size-dropdown",
        #                     options=[
        #                         {"label": "10", "value": 10},
        #                         {"label": "25", "value": 25},
        #                         {"label": "50", "value": 50},
        #                         {"label": "100", "value": 100}
        #                     ],
        #                     value=10,
        #                     style={"width": "80px", "display": "inline-block"},
        #                     className="me-3"
        #                 )
        #             ], className="d-flex align-items-center justify-content-end")
        #         ], className="d-flex justify-content-between align-items-center mt-3")
        #     ])
        # ])

    def _create_tabulator_script(self):
        """Create the Tabulator initialization script"""
        return html.Script("""
            window.dash_clientside = Object.assign({}, window.dash_clientside, {
                clientside: {
                    initialize_tabulator: function(data, page_size) {
                        if (typeof Tabulator === 'undefined') {
                            console.error('Tabulator library not loaded');
                            return window.dash_clientside.no_update;
                        }
                        
                        // Clear existing table
                        const container = document.getElementById('tabulator-table');
                        if (container && container.children.length > 0) {
                            container.innerHTML = '';
                        }
                        
                        if (!data || data.length === 0) {
                            container.innerHTML = '<div class="text-center py-4">No data available</div>';
                            return window.dash_clientside.no_update;
                        }
                        
                        // Initialize Tabulator
                        const table = new Tabulator("#tabulator-table", {
                            data: data,
                            layout: "fitColumns",
                            dataTree: true,
                            dataTreeStartExpanded: false,
                            dataTreeChildField: "_children",
                            height: "400px",
                            pagination: "local",
                            paginationSize: page_size,
                            selectable: true,
                            selectableCheck: function(row) {
                                return true;
                            },
                            columns: [
                                {
                                    title: "", 
                                    field: "select", 
                                    formatter: "rowSelection", 
                                    titleFormatter: "rowSelection", 
                                    hozAlign: "center", 
                                    headerSort: false, 
                                    width: 40
                                },
                                {title: "Element", field: "Element", width: 100, headerFilter: "input"},
                                {title: "Relation", field: "Relation", width: 150, headerFilter: "input"},
                                {title: "Weight", field: "Weight", width: 100, headerFilter: "input"},
                                {title: "Identifier", field: "Identifier", width: 250, headerFilter: "input"},
                                {title: "Name", field: "Name", width: 300, headerFilter: "input"},
                                {title: "Description", field: "Description", headerFilter: "input"}
                            ],
                            rowClick: function(e, row) {
                                console.log("Row clicked:", row.getData());
                            },
                            dataChanged: function() {
                                // Update row count
                                const totalRows = table.getDataCount();
                                const visibleRows = table.getDataCount("visible");
                                const rowInfo = document.getElementById('row-info');
                                if (rowInfo) {
                                    rowInfo.textContent = `Showing ${visibleRows} of ${totalRows} rows`;
                                }
                            }
                        });
                        
                        // Store table reference globally for other functions
                        window.tabulatorTable = table;
                        
                        return window.dash_clientside.no_update;
                    },
                    
                    update_page_size: function(page_size) {
                        if (window.tabulatorTable) {
                            window.tabulatorTable.setPageSize(page_size);
                        }
                        return window.dash_clientside.no_update;
                    },
                    
                    get_selected_rows: function() {
                        if (window.tabulatorTable) {
                            return window.tabulatorTable.getSelectedData();
                        }
                        return [];
                    }
                }
            });
        """)

    def create_table(self, data: List[Dict[str, Any]], page_size: int = 10):
        """Return data for Tabulator initialization"""
        return data

    def create_loading_spinner(self):
        """Create a loading spinner component"""
        return dbc.Spinner(
            html.Div("Loading..."),
            size="lg",
            color="primary",
            type="border",
            fullscreen=False
        )

    def create_error_message(self, message: str):
        """Create an error message component"""
        return dbc.Alert(
            [html.I(className="bi bi-exclamation-triangle me-2"), message],
            color="danger",
            className="mt-3"
        )

    def create_success_message(self, message: str):
        """Create a success message component"""
        return dbc.Alert(
            [html.I(className="bi bi-check-circle me-2"), message],
            color="success",
            className="mt-3"
        )

    def create_info_message(self, message: str):
        """Create an info message component"""
        return dbc.Alert(
            [html.I(className="bi bi-info-circle me-2"), message],
            color="info",
            className="mt-3"
        )