import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# Sample hierarchical data for Tabulator
sample_data = [
    {
        "id": 1,
        "Element": "1.0",
        "Relation": "",
        "Weight": "",
        "Identifier": "",
        "Name": "Acceptance Verification Procedures (A...",
        "Description": "Root Node for AVR Register",
        "_children": [
            {
                "id": 2,
                "Element": "1.01",
                "Relation": "includes_procedure",
                "Weight": "1",
                "Identifier": "SRL-WPF-XPA-NAP-PRC-XSE-PWD-N...",
                "Name": "Acceptance Verification Procedure [0...",
                "Description": "-"
            }
        ]
    }
]

class BreakdownView:
    def __init__(self):
        pass

    def create_layout(self):
        return dbc.Container([
            # Action buttons row
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button([html.I(className="bi bi-plus-circle"), " Create"], 
                                color="primary", size="sm"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise"), " Refresh"], 
                                color="secondary", outline=True, size="sm"),
                        dbc.Button([html.I(className="bi bi-trash"), " Delete"], 
                                color="warning", outline=True, size="sm")
                    ])
                ], width="auto"),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button([html.I(className="bi bi-printer"), " Print"], 
                                color="primary", outline=True, size="sm"),
                        dbc.Button([html.I(className="bi bi-download"), " Download"], 
                                color="primary", size="sm")
                    ])
                ], width="auto", className="ms-auto")
            ], className="mb-3"),
            
            # Graph selection row
            dbc.Row([
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
            ]),
            
            # Tabulator table
            dbc.Row([
                dbc.Col([
                    html.Div(id="tabulator-table")
                ])
            ]),
            
            # Footer with tabulator info
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span("Showing 1-2 of 2 rows", className="text-muted"),
                        html.Div([
                            html.Span("Page Size", className="me-2"),
                            dcc.Dropdown(
                                id="page-size-dropdown",
                                options=[
                                    {"label": "10", "value": 10},
                                    {"label": "25", "value": 25},
                                    {"label": "50", "value": 50}
                                ],
                                value=10,
                                style={"width": "80px", "display": "inline-block"},
                                className="me-3"
                            ),
                            dbc.ButtonGroup([
                                dbc.Button("First", size="sm", outline=True, disabled=True),
                                dbc.Button("Prev", size="sm", outline=True, disabled=True),
                                dbc.Button("1", size="sm", color="primary"),
                                dbc.Button("Next", size="sm", outline=True, disabled=True),
                                dbc.Button("Last", size="sm", outline=True, disabled=True)
                            ])
                        ], className="d-flex align-items-center justify-content-end")
                    ], className="d-flex justify-content-between align-items-center mt-3")
                ])
            ]),
            
            # Tabulator initialization script
            html.Script("""
                document.addEventListener('DOMContentLoaded', function() {
                    if (typeof Tabulator !== 'undefined') {
                        var table = new Tabulator("#tabulator-table", {
                            data: """ + str(sample_data).replace("'", '"') + """,
                            layout: "fitColumns",
                            dataTree: true,
                            dataTreeStartExpanded: false,
                            columns: [
                                {title: "Element", field: "Element", width: 100},
                                {title: "Relation", field: "Relation", width: 150},
                                {title: "Weight", field: "Weight", width: 100},
                                {title: "Identifier", field: "Identifier", width: 200},
                                {title: "Name", field: "Name", width: 250},
                                {title: "Description", field: "Description", width: 200}
                            ],
                            pagination: "local",
                            paginationSize: 10,
                            paginationSizeSelector: [10, 25, 50, 100]
                        });
                    }
                });
            """)
        ], fluid=True)

    # Callback for page size (if needed for other components)
    @callback(
        Output("page-size-dropdown", "value"),
        Input("page-size-dropdown", "value")
    )
    def update_page_size(page_size):
        return page_size