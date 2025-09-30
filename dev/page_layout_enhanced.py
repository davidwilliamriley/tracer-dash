import dash
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for the table
table_data = [
    {"id": 1, "name": "Item 1", "value": 100, "status": "Active"},
    {"id": 2, "name": "Item 2", "value": 200, "status": "Pending"},
    {"id": 3, "name": "Item 3", "value": 300, "status": "Active"},
    {"id": 4, "name": "Item 4", "value": 150, "status": "Completed"},
]

table_columns = [
    {"name": "ID", "id": "id"},
    {"name": "Name", "id": "name"},
    {"name": "Value", "id": "value"},
    {"name": "Status", "id": "status"},
]

# Navbar with search
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("My Dashboard", href="#", className="ms-2"),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.NavItem(dbc.NavLink("About", href="#")),
            dbc.NavItem(dbc.NavLink("Contact", href="#")),
        ], navbar=True),
    ]),
    color="primary",
    dark=True,
    className="mb-4",
    sticky="top"
)

# Main content with stacked elements
main_content = dbc.Container([
    # Header row with breadcrumb
    dbc.Row([
        dbc.Col([
            html.Nav([
                html.Ol([
                    html.Li(html.A("Home", href="#"), className="breadcrumb-item"),
                    html.Li("Dashboard", className="breadcrumb-item active"),
                ], className="breadcrumb mb-2")
            ]),
            html.H2("Dashboard Overview", className="mb-1"),
            html.P("Monitor and manage your data from this central location", 
                   className="text-muted mb-4")
        ])
    ]),
    
    # Card with filters
    dbc.Card([
        dbc.CardHeader([
            html.H5("Filters", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Category", className="form-label fw-bold"),
                    dbc.Select(
                        id="select-dropdown",
                        options=[
                            {"label": "All Items", "value": "all"},
                            {"label": "Category 1", "value": "1"},
                            {"label": "Category 2", "value": "2"},
                            {"label": "Category 3", "value": "3"},
                        ],
                        value="all",
                    )
                ], md=10),
                dbc.Col([
                    html.Label("Actions", className="form-label fw-bold"),
                    dbc.Button("Reset", id="reset-button", color="outline-secondary", className="w-100")
                ], md=2)
            ])
        ])
    ], className="mb-4 shadow-sm"),
    
    # Action buttons row
    dbc.Row([
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button([html.I(className="bi bi-plus-circle me-2"), "Add New"], 
                          color="primary", outline=True),
                dbc.Button([html.I(className="bi bi-pencil me-2"), "Edit"], 
                          color="primary", outline=True),
                dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                          color="danger", outline=True),
            ])
        ], width="auto"),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button([html.I(className="bi bi-download me-2"), "Export"], 
                          color="success", outline=True),
                dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                          color="success", outline=True),
            ])
        ], width="auto", className="ms-auto")
    ], className="mb-3"),

    # Table card
    dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H5("Data Table", className="d-inline mb-0"),
                dbc.Badge(f"{len(table_data)} items", color="secondary", className="ms-2")
            ])
        ]),
        dbc.CardBody([
            dash_table.DataTable(
                id='table',
                columns=table_columns,  # type: ignore
                data=table_data,  # type: ignore
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left', 
                    'padding': '12px',
                    'fontFamily': 'inherit'
                },
                style_header={
                    'backgroundColor': 'rgb(248, 249, 250)',
                    'fontWeight': '600',
                    'borderBottom': '2px solid #dee2e6',
                    'color': '#495057'
                },
                style_data={
                    'borderBottom': '1px solid #dee2e6',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 249, 250)',
                    }
                ],
                page_size=10,
                sort_action="native",
                filter_action="native",
            )
        ], className="p-0")
    ], className="shadow-sm")
], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '80px'})

# Sticky footer
footer = html.Footer([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P("© 2025 My Dashboard. All rights reserved.", 
                       className="text-muted mb-0 small")
            ], md=6),
            dbc.Col([
                html.P([
                    html.A("Privacy", href="#", className="text-muted me-3 small text-decoration-none"),
                    html.A("Terms", href="#", className="text-muted me-3 small text-decoration-none"),
                    html.A("Help", href="#", className="text-muted small text-decoration-none"),
                ], className="text-end mb-0")
            ], md=6)
        ])
    ])
], style={
    'position': 'fixed',
    'bottom': '0',
    'width': '100%',
    'backgroundColor': 'white',
    'padding': '15px 0',
    'borderTop': '1px solid #dee2e6',
    'boxShadow': '0 -2px 4px rgba(0,0,0,0.05)'
})

# Complete Layout
app.layout = html.Div([
    navbar,
    main_content,
    footer
], style={'backgroundColor': '#f8f9fa'})

if __name__ == '__main__':
    app.run(debug=True)