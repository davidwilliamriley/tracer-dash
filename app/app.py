# app.py

# Imports
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask

# External Scripts
external_scripts = [
    {"src": "https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"},
    {"src": "https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"}
]

# External Stylesheets  
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_bootstrap5.min.css",
    "/assets/css/tabulator.css"
]

server = Flask(__name__)
app = dash.Dash(
    __name__, 
    server=server,
    use_pages=True,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="Tracer"
)

server.static_folder = 'assets'

# Import pages AFTER instantiation of the App
import pages

# Page Navigation Bar
def get_header():
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([html.I(className="bi bi-node-plus me-2"), "Tracer"], href="/", className="fw-light fs-2"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-house-door-fill me-2"), "Home"], href="/", id="nav-home")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-speedometer me-2"), "Dashboard"],href="/dashboard", id="nav-dashboard")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-file-earmark-richtext me-2"), "Reports"], href="/reports", id="nav-reports")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-bezier2 me-2"), "Network"], href="/network", id="nav-network")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-diagram-2 me-2"), "Breakdowns"],href="/breakdowns", id="nav-breakdowns")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-arrow-repeat me-2"), "Edges"], href="/edges", id="nav-edges")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-plus-circle me-2"), "Nodes"], href="/nodes", id="nav-nodes")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-link-45deg me-2"), "Edge Types"], href="/edge-types", id="nav-edge-types")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-question-circle me-2"), "Help"], href="/help", id="nav-help")),
            ], navbar=True, className="ms-auto", id="nav-items"),
        ]),
        color="dark",
        dark=True,
        className="px-3 py-3",
        sticky="top"
    )

@callback(
    [Output(f"nav-{page}", "className") for page in 
     ["home", "dashboard", "reports", "network", "breakdowns", "edges", "nodes", "edge-types", "help"]],
    Input("_pages_location", "pathname")
)
def update_nav_style(pathname):
    nav_map = {
        "/": "home",
        "/dashboard": "dashboard",
        "/reports": "reports",
        "/network": "network",
        "/breakdowns": "breakdowns",
        "/edges": "edges",
        "/nodes": "nodes",
        "/edge-types": "edge-types",
        "/help": "help"
    }
    
    active_page = nav_map.get(pathname, None)
    
    return [
        "text-white" if page == active_page else "text-white-50"
        for page in ["home", "dashboard", "reports", "network", "breakdowns", "edges", "nodes", "edge-types", "help"]
    ]

# Footer
def get_footer():
    return html.Footer([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P("© 2025 John Holland Group Pty. Ltd. All Rights Reserved.", 
                           className="text-muted mb-0 small")
                ], md=6),
                dbc.Col([
                    html.P([
                        html.A("Privacy", href="#", className="text-muted me-3 small text-decoration-none"),
                        html.A("Terms", href="#", className="text-muted me-3 small text-decoration-none"),
                        # html.A("Help", href="#", className="text-muted small text-decoration-none"),
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

# To-Do : update the Footer to use the updated Template
app.layout = html.Div([
    get_header(),
    html.Main([
        dash.page_container
    ], className="content"),
    get_footer()
], className="page-wrapper", style={'backgroundColor': '#f8f9fa'})

if __name__ == '__main__':
    app.run(debug=True)