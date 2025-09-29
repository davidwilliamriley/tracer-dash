# views/breakdowns_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc

class BreakdownView:
    def __init__(self):
        self.controller = None  
            
    def create_layout(self):
        return dbc.Container([
            # Toast notification
            self._create_toast_notification(),
            
            # Main content stack
            dbc.Stack([
                # Page Header
                self._create_header(),
                
                # Controls
                html.Div([
                    self._create_action_buttons(),
                    self._create_graph_selection(),
                ]),
                
                # Main Content - Table
                html.Div([
                    self._create_table_container(),
                ], style={'flex': '1'}),
                
                # Footer with pagination info
                # self._create_footer(),
            ]),
            
            # Hidden data store for clientside callbacks
            html.Div(id="table-data-store", style={"display": "none"})
            
        ], fluid=True, style={"height": "100vh"})
    
    def _create_toast_notification(self):
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
    
    def _create_header(self):
        """Create page header"""
        return html.Div([
            html.H1("Breakdowns", className="mb-3")
        ])
    
    def _create_action_buttons(self):
        """Create action button toolbar"""
        return html.Div([
            dbc.Row([
                # Left side buttons
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button(
                            [html.I(className="bi bi-plus-lg me-2"), "Create"],
                            id="create-node-btn",
                            color="primary",
                            title="Create a new Node"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"],
                            id="refresh-nodes-btn",
                            color="primary",
                            title="Refresh the Nodes Table"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-trash me-2"), "Delete"],
                            id="delete-node-btn",
                            color="warning",
                            title="Delete a selected Node",
                            disabled=True
                        ),
                    ])
                ], md=6, className="d-flex justify-content-start"),
                
                # Right side buttons
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button(
                            [html.I(className="bi bi-printer me-2"), "Print"],
                            id="print-nodes-btn",
                            color="primary",
                            title="Print the Table to PDF"
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-download me-2"), "Download"],
                            id="download-nodes-btn",
                            color="primary",
                            title="Download the Table as CSV"
                        ),
                    ])
                ], md=6, className="d-flex justify-content-end"),
            ], className="mb-3")
        ])
    
    def _create_graph_selection(self):
        """Create the graph selection dropdown"""
        return dbc.Row([
            dbc.Col([
                html.Label("Select the Graph:", className="form-label fw-bold"),
                dcc.Dropdown(
                    id="graph-dropdown",
                    options=[], 
                    value="avp",
                    placeholder="Select a graph...",
                    className="mb-3"
                )
            ])
        ])
    
    def _create_table_container(self):
        """Create the table container for Tabulator"""
        return dbc.Row([
            dbc.Col([
                html.Div(
                    id="tabulator-table",
                    style={
                        "minHeight": "400px",
                        "border": "1px solid #dee2e6",
                        "borderRadius": "0.25rem"
                    }
                )
            ])
        ])