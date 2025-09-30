import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_tabulator import DashTabulator

app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://unpkg.com/tabulator-tables@5.5.0/dist/css/tabulator_bootstrap4.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"
])

# Custom CSS for selected rows and footer
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .tabulator-row.tabulator-selected {
                background-color: #cfe2ff !important;
                color: #084298 !important;
            }
            .tabulator-row.tabulator-selected:hover {
                background-color: #b6d4fe !important;
                color: #084298 !important;
            }
            .tabulator-footer {
                background-color: #f8f9fa !important;
                border-top: 1px solid #dee2e6 !important;
            }
            .tabulator-paginator {
                color: #495057 !important;
            }
            .tabulator-page-counter {
                display: inline-block !important;
                margin: 0 10px !important;
            }
            /* Style tabulator headers to match Bootstrap */
            .tabulator-header {
                background-color: #f8f9fa !important;
                border-bottom: 2px solid #dee2e6 !important;
            }
            .tabulator-col {
                background-color: #f8f9fa !important;
                color: #495057 !important;
            }
            .tabulator-col:hover,
            .tabulator-col.tabulator-sortable:hover {
                background-color: #cfe2ff !important;
                color: #084298 !important;
                cursor: pointer !important;
            }
            .tabulator-col.tabulator-sorted {
                background-color: #cfe2ff !important;
                color: #084298 !important;
            }
            /* Style pagination buttons to match Bootstrap outline buttons */
            .tabulator-page {
                border: 1px solid #0d6efd !important;
                color: #0d6efd !important;
                background-color: transparent !important;
                padding: 0.375rem 0.75rem !important;
                border-radius: 0.25rem !important;
                margin: 0 2px !important;
            }
            .tabulator-page:hover:not(.disabled) {
                background-color: #0d6efd !important;
                color: white !important;
            }
            .tabulator-page.active {
                background-color: transparent !important;
                color: #0d6efd !important;
                border-color: #0d6efd !important;
                font-weight: 600 !important;
            }
            .tabulator-page.active:hover {
                background-color: #0d6efd !important;
                color: white !important;
            }
            .tabulator-page.disabled {
                border-color: #6c757d !important;
                color: #6c757d !important;
                opacity: 0.65 !important;
                cursor: not-allowed !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Sample data for the table
table_data = [
    {"id": 1, "name": "Item 1", "value": 100, "status": "Active"},
    {"id": 2, "name": "Item 2", "value": 200, "status": "Pending"},
    {"id": 3, "name": "Item 3", "value": 300, "status": "Active"},
    {"id": 4, "name": "Item 4", "value": 150, "status": "Completed"},
    {"id": 5, "name": "Item 5", "value": 250, "status": "Pending"},
    {"id": 6, "name": "Item 6", "value": 100, "status": "Active"},
    {"id": 7, "name": "Item 7", "value": 200, "status": "Pending"},
    {"id": 8, "name": "Item 8", "value": 300, "status": "Active"},
    {"id": 9, "name": "Item 9", "value": 100, "status": "Active"},
    {"id": 10, "name": "Item 10", "value": 200, "status": "Pending"},
    {"id": 11, "name": "Item 11", "value": 300, "status": "Active"},
    {"id": 12, "name": "Item 12", "value": 150, "status": "Completed"},
]

table_columns = [
    {"title": "ID", "field": "id", "width": 80, "hozAlign": "left"},
    {"title": "Name", "field": "name", "headerFilter": "input", "hozAlign": "left"},
    {"title": "Value", "field": "value", "sorter": "number", "headerFilter": "number", "hozAlign": "left"},
    {"title": "Status", "field": "status", "headerFilter": "list", 
     "headerFilterParams": {"values": ["Active", "Pending", "Completed"]}, "hozAlign": "left"},
]

# Navbar with search
navbar = dbc.Navbar(
    [
        dbc.Container([
            dbc.NavbarBrand("My Dashboard", href="#"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="#")),
                dbc.NavItem(dbc.NavLink("About", href="#")),
                dbc.NavItem(dbc.NavLink("Contact", href="#")),
            ], navbar=True),
        ])
    ],
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
            html.H6("Filters", className="mb-0")
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
                    html.Label("\u00A0", className="form-label"),  # Non-breaking space for alignment
                    dbc.Button([html.I(className="bi bi-arrow-clockwise me-1"), "Reset"], 
                              id="reset-button", color="outline-primary", className="w-100")
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
                          color="warning", outline=True),
            ])
        ], width="auto"),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button([html.I(className="bi bi-download me-2"), "Export"], 
                          color="primary", outline=True),
                dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                          color="primary", outline=True),
            ])
        ], width="auto", className="ms-auto")
    ], className="mb-3"),

    # Table card - with full height
    dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H6("Data Table", className="mb-0"),
                html.Small(f"{len(table_data)} Items", className="text-muted")
            ], className="d-flex justify-content-between align-items-center")
        ]),
        dbc.CardBody([
            html.Div([
                DashTabulator(
                    id='table',
                    columns=table_columns,
                    data=table_data,
                    options={
                        "layout": "fitColumns",
                        "pagination": "local",
                        "paginationSize": 10,
                        "paginationSizeSelector": [5, 10, 20, 30, 50],
                        "paginationCounter": "rows",
                        "movableColumns": True,
                        "resizableColumns": True,
                        "selectable": True,
                        "headerFilterLiveFilterDelay": 600,
                    },
                )
            ], style={
                'fontFamily': 'inherit',
                'height': 'calc(100vh - 540px)',  # Full height minus navbar, header, filters, buttons, footer
                'overflow': 'auto'
            })
        ], className="p-0")
    ], className="shadow-sm", style={'flex': '1'})
], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '100px', 'display': 'flex', 'flexDirection': 'column'})

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