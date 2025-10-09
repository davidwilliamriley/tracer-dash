# app.py

# Imports
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask
from flask_caching import Cache
import logging
from logging.handlers import RotatingFileHandler
import networkx as nx
import sys
import uuid
import os

from utils import network_utils

# External Scripts
external_scripts = [
    {"src": "https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"},
    {"src": "https://unpkg.com/cytoscape-fcose@2.2.0/cytoscape-fcose.js"},
    {"src": "https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"},
    {"src": "https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"},
    # Try to load Klay but don't fail if it doesn't work
    {"src": "https://unpkg.com/cytoscape-klay@3.1.4/cytoscape-klay.js"},
    {"src": "https://unpkg.com/klayjs@0.4.1/klay.js"},
    # COLA layout extension
    {"src": "https://unpkg.com/cytoscape-cola@2.4.0/cytoscape-cola.js"},
    {"src": "https://unpkg.com/webcola@3.4.0/WebCola/cola.min.js"},
    {"src": "https://cdn.jsdelivr.net/npm/cytoscape-svg@0.4.0/cytoscape-svg.js"},
    {"src": "/assets/js/cytoscape_config.js"},
    {"src": "/assets/js/cytoscape_utils.js"},
    {"src": "/assets/js/cytoscape_styles.js"},
    {"src": "/assets/js/cytoscape_events.js"},
    {"src": "/assets/js/cytoscape_callback.js"},
    {"src": "https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"},
]

# External Stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_bootstrap5.min.css",
    "/assets/css/app.css",
    "/assets/css/tabulator.css"
]


def setup_logging(app_name="TracerApp", log_level=logging.INFO):
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    if logger.hasHandlers():
        return logger

    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    logger.addHandler(console_handler)

    os.makedirs("logs", exist_ok=True)

    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5
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
    pages_folder="pages",
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="Tracer",
)

cache = Cache(
    app.server, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 3600}
)

server.static_folder = "assets"

# Import pages AFTER app creation
import pages

_cached_network = None


def get_network():
    global _cached_network
    if _cached_network is None or _cached_network.number_of_nodes() == 0:
        _cached_network = network_utils.build_networkx_from_database()
        roots = network_utils.get_graph_roots(_cached_network)
        if roots:
            logger.info(f"Identified {len(roots)} root nodes in the NetworkX graph.")
            for root in roots:
                logger.info(f"Root Node ID: {root}")
        else:
            logger.info("No root nodes found in the NetworkX graph.")

        logger.info("Network was re-built from the DB.")

        breakdown = network_utils.build_breakdown_from_graph(_cached_network)
        logger.info(f"Breakdown built with {len(breakdown)} top-level items.")

    return _cached_network


def refresh_network_cache():
    global _cached_network
    _cached_network = None
    logger.info("Network was cleared from Cache.")


logger.info("Initializing theNetwork Graph...")
startup_graph = get_network()
logger.info(
    f"Initial Graph has {startup_graph.number_of_edges()} Edges and {startup_graph.number_of_nodes()} Nodes."
)


# Page Navigation Bar
def get_header():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    [html.I(className="bi bi-node-plus me-2"), html.Span(id="navbar-brand-text", children="Tracer")],
                    href="/",
                    className="fw-light fs-2",
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-house-door-fill me-2"),
                                    "Home",
                                ],
                                href="/",
                                id="nav-home",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-speedometer me-2"),
                                    "Dashboard",
                                ],
                                href="/dashboard",
                                id="nav-dashboard",
                            )
                        ),
                        # dbc.NavItem(dbc.NavLink([html.I(className="bi bi-file-earmark-richtext me-2"), "Reports"], href="/reports", id="nav-reports")),
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="bi bi-bezier2 me-2"), "Network"],
                                href="/network",
                                id="nav-network",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-diagram-2 me-2"),
                                    "Breakdowns",
                                ],
                                href="/breakdowns",
                                id="nav-breakdowns",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="bi bi-arrow-repeat me-2"), "Edges"],
                                href="/edges",
                                id="nav-edges",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="bi bi-plus-circle me-2"), "Nodes"],
                                href="/nodes",
                                id="nav-nodes",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-link-45deg me-2"),
                                    "Edge Types",
                                ],
                                href="/edge-types",
                                id="nav-edge-types",
                            )
                        ),
                        # dbc.NavItem(dbc.NavLink([html.I(className="bi bi-question-circle me-2"), "Help"], href="/help", id="nav-help")),
                    ],
                    navbar=True,
                    className="ms-auto",
                    id="nav-items",
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="px-3 py-3",
        sticky="top",
    )


# Footer
def get_footer():
    return html.Footer(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.P(
                                        "© 2025 John Holland Group Pty. Ltd. All Rights Reserved.",
                                        className="text-muted mb-0 small",
                                    )
                                ],
                                md=6,
                            ),
                            dbc.Col(
                                [
                                    html.P(
                                        [
                                            html.A(
                                                "Privacy",
                                                href="#",
                                                className="text-muted me-3 small text-decoration-none",
                                            ),
                                            html.A(
                                                "Terms",
                                                href="#",
                                                className="text-muted me-3 small text-decoration-none",
                                            ),
                                        ],
                                        className="text-end mb-0",
                                    )
                                ],
                                md=6,
                            ),
                        ]
                    )
                ]
            )
        ],
        style={
            "position": "fixed",
            "bottom": "0",
            "width": "100%",
            "backgroundColor": "white",
            "padding": "15px 0",
            "borderTop": "1px solid #dee2e6",
            "boxShadow": "0 -2px 4px rgba(0,0,0,0.05)",
        },
    )


app.layout = html.Div(
    [get_header(), html.Main([dash.page_container], className="content"), get_footer()],
    style={"backgroundColor": "#f8f9fa"},
)


@callback(
    [
        Output(f"nav-{page}", "className")
        for page in [
            "home",
            "dashboard",
            "network",
            "breakdowns",
            "edges",
            "nodes",
            "edge-types",
        ]
    ] + [Output("navbar-brand-text", "children")],
    Input("_pages_location", "pathname"),
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
    
    # Page name mapping for navbar brand
    page_names = {
        "/": "Tracer",
        "/dashboard": "Tracer - Dashboard",
        "/network": "Tracer - Network",
        "/breakdowns": "Tracer - Breakdowns", 
        "/edges": "Tracer - Edges",
        "/nodes": "Tracer - Nodes",
        "/edge-types": "Tracer - Edge Types",
    }

    active_page = nav_map.get(pathname, None)
    brand_text = page_names.get(pathname, "Tracer")

    nav_classes = [
        "text-white" if page == active_page else "text-white-50"
        for page in [
            "home",
            "dashboard",
            "network",
            "breakdowns",
            "edges",
            "nodes",
            "edge-types",
        ]
    ]
    
    return nav_classes + [brand_text]


if __name__ == "__main__":
    logger.info("Starting the Dash Server...")
    app.run(debug=True)
