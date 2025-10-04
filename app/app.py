# app.py

# Imports
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask
from flask_caching import Cache
import logging
from logging.handlers import RotatingFileHandler
import sys
import uuid
import os

# External Scripts
external_scripts = [
    {"src": "https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"},
    {"src": "https://unpkg.com/cytoscape-fcose@2.2.0/cytoscape-fcose.js"},
    {"src": "/assets/js/cytoscape_config.js"},
    {"src": "/assets/js/cytoscape_utils.js"},
    {"src": "/assets/js/cytoscape_styles.js"},
    {"src": "/assets/js/cytoscape_events.js"},
    {"src": "/assets/js/cytoscape_callback.js"},
    {"src": "https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"}
]

# External Stylesheets  
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_bootstrap5.min.css",
    "/assets/css/tabulator.css"
]

def setup_logging(app_name='TracerApp', log_level=logging.INFO):
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
       return logger
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    os.makedirs('logs', exist_ok=True)

    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024, 
        backupCount=5
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging()
logger.info("Dash Application is starting...")

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

cache = Cache(app.server, config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 3600
})

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
                # dbc.NavItem(dbc.NavLink([html.I(className="bi bi-file-earmark-richtext me-2"), "Reports"], href="/reports", id="nav-reports")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-bezier2 me-2"), "Network"], href="/network", id="nav-network")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-diagram-2 me-2"), "Breakdowns"],href="/breakdowns", id="nav-breakdowns")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-arrow-repeat me-2"), "Edges"], href="/edges", id="nav-edges")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-plus-circle me-2"), "Nodes"], href="/nodes", id="nav-nodes")),
                dbc.NavItem(dbc.NavLink([html.I(className="bi bi-link-45deg me-2"), "Edge Types"], href="/edge-types", id="nav-edge-types")),
                # dbc.NavItem(dbc.NavLink([html.I(className="bi bi-question-circle me-2"), "Help"], href="/help", id="nav-help")),
            ], navbar=True, className="ms-auto", id="nav-items"),
        ]),
        color="dark",
        dark=True,
        className="px-3 py-3",
        sticky="top"
    )

# @callback(
#     [Output(f"nav-{page}", "className") for page in 
#      ["home", "dashboard", "reports", "network", "breakdowns", "edges", "nodes", "edge-types", "help"]],
#     Input("_pages_location", "pathname")
# )

@callback(
    [Output(f"nav-{page}", "className") for page in 
     ["home", "dashboard", "network", "breakdowns", "edges", "nodes", "edge-types"]],
    Input("_pages_location", "pathname")
)
def update_nav_style(pathname):
    nav_map = {
        "/": "home",
        "/dashboard": "dashboard",
        # "/reports": "reports",
        "/network": "network",
        "/breakdowns": "breakdowns",
        "/edges": "edges",
        "/nodes": "nodes",
        "/edge-types": "edge-types",
        # "/help": "help"
    }
    
    active_page = nav_map.get(pathname, None)
    
    # return [
    #     "text-white" if page == active_page else "text-white-50"
    #     for page in ["home", "dashboard", "reports", "network", "breakdowns", "edges", "nodes", "edge-types", "help"]
    # ]

    return [
        "text-white" if page == active_page else "text-white-50"
        for page in ["home", "dashboard", "network", "breakdowns", "edges", "nodes", "edge-types"]
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
    dcc.Store(id='session-id', storage_type='session'),
    get_header(),
    html.Main([
        dash.page_container
    ], className="content"),
    get_footer()
# ], className="page-wrapper", style={'backgroundColor': '#f8f9fa'})
], style={'backgroundColor': '#f8f9fa'})

# Initialize the Session
@callback(
    Output('session-id', 'data'),
    Input('session-id', 'data')
)
def init_session(session_id):
    if session_id:
        logger.info(f"Found an existing session with ID {session_id}")
        return session_id
    new_session = str(uuid.uuid4())
    logger.info(f"Created a new session with ID {new_session}")
    return new_session

if __name__ == '__main__':
    logger.info("Starting the Dash Server...")
    app.run(debug=True)