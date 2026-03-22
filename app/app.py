# app.py

# Imports
import importlib.util
import pkgutil
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


if not hasattr(pkgutil, "find_loader"):

    def _find_loader(name):
        try:
            spec = importlib.util.find_spec(name)
        except (ModuleNotFoundError, ValueError):
            return None
        return spec.loader if spec else None

    pkgutil.find_loader = _find_loader

from utils import network_utils
from pkg.config import LOG_DIR

# External Scripts
external_scripts = [
    {"src": "https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"},
    {"src": "https://unpkg.com/cytoscape-fcose@2.2.0/cytoscape-fcose.js"},
    {"src": "https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"},
    {"src": "https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"},
    # Klay Layout
    {"src": "https://unpkg.com/cytoscape-klay@3.1.4/cytoscape-klay.js"},
    {"src": "https://unpkg.com/klayjs@0.4.1/klay.js"},
    # COLA Layout
    {"src": "https://unpkg.com/cytoscape-cola@2.4.0/cytoscape-cola.js"},
    {"src": "https://unpkg.com/webcola@3.4.0/WebCola/cola.min.js"},
    {"src": "https://cdn.jsdelivr.net/npm/cytoscape-svg@0.4.0/cytoscape-svg.js"},
    {"src": "/assets/js/cytoscape_config.js"},
    {"src": "/assets/js/cytoscape_utils.js"},
    {"src": "/assets/js/cytoscape_styles.js"},
    {"src": "/assets/js/cytoscape_events.js"},
    {"src": "/assets/js/cytoscape_search.js"},
    {"src": "/assets/js/cytoscape_callback.js"},
    {"src": "https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"},
    {
        "src": "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"
    },
]

# External Stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
    "https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator_bootstrap5.min.css",
    "/assets/css/app.css",
    "/assets/css/tabulator.css",
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

    log_file_path = LOG_DIR / "app.log"
    file_handler = RotatingFileHandler(
        str(log_file_path), maxBytes=10 * 1024 * 1024, backupCount=5
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
logger.info("Tracer Application is starting...")

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

# Import pages AFTER creating the App
import pages

_cached_network = None


def get_network():
    global _cached_network
    if _cached_network is None or _cached_network.number_of_nodes() == 0:
        _cached_network = network_utils.build_networkx_from_database()
        roots = network_utils.get_graph_roots(_cached_network)
        if roots:
            logger.info(f"Identified {len(roots)} Root Nodes in the NetworkX Graph")
            for root in roots:
                logger.info(f"Root Node ID: {root}")
        else:
            logger.info("No Root Nodes found in the NetworkX Graph")

        logger.info("Network was re-built from the DB.")

        breakdown = network_utils.build_breakdown_from_graph(_cached_network)
        logger.info(f"Breakdown built with {len(breakdown)} Top-level Items.")

    return _cached_network


def refresh_network_cache():
    global _cached_network
    _cached_network = None
    logger.info("Network cleared from Cache.")


logger.info("Initializing the Network Graph...")
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
                    [
                        html.I(className="bi bi-node-plus me-2"),
                        html.Span(id="navbar-brand-text", children="Tracer"),
                    ],
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
                        # dbc.NavItem(dbc.NavLink([html.I(className="bi bi-file-earmark-richtext me-2"), "Reports"], href="/reports", id="nav-reports")),
                        dbc.NavItem(
                            dbc.NavLink(
                                # Update to Graphs
                                [html.I(className="bi bi-bezier2 me-2"), "Graphs"],
                                href="/network",
                                id="nav-network",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                # Update to Components
                                [
                                    html.I(className="bi bi-diagram-2 me-2"),
                                    "Components",
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
                        dbc.DropdownMenu(
                            label="Configuration",
                            nav=True,
                            in_navbar=True,
                            id="nav-config",
                            toggle_class_name="text-white-50",
                            children=[
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-diagram-3 me-2"),
                                        "Node Types",
                                    ],
                                    href="/node-types",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-link-45deg me-2"),
                                        "Edge Types",
                                    ],
                                    href="/edge-types",
                                ),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-sliders me-2"),
                                        "Node Property Definitions",
                                    ],
                                    href="/node-property-definitions",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-sliders2 me-2"),
                                        "Edge Property Definitions",
                                    ],
                                    href="/edge-property-definitions",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(
                                            className="bi bi-input-cursor-text me-2"
                                        ),
                                        "Node Property Values",
                                    ],
                                    href="/node-property-values",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-text-paragraph me-2"),
                                        "Edge Property Values",
                                    ],
                                    href="/edge-property-values",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-list-check me-2"),
                                        "Node Property Assignments",
                                    ],
                                    href="/node-property-assignments",
                                ),
                                dbc.DropdownMenuItem(
                                    [
                                        html.I(className="bi bi-card-checklist me-2"),
                                        "Edge Property Assignments",
                                    ],
                                    href="/edge-property-assignments",
                                ),
                            ],
                        ),
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
        for page in ["home", "network", "breakdowns", "edges", "nodes"]
    ]
    + [Output("nav-config", "toggle_class_name")]
    + [Output("navbar-brand-text", "children")],
    Input("_pages_location", "pathname"),
)
def update_nav_style(pathname):
    nav_map = {
        "/": "home",
        # "/reports": "reports",
        "/network": "network",
        "/breakdowns": "breakdowns",
        "/edges": "edges",
        "/edge-types": "config",
        "/node-types": "config",
        "/node-property-definitions": "config",
        "/edge-property-definitions": "config",
        "/node-property-values": "config",
        "/edge-property-values": "config",
        "/node-property-assignments": "config",
        "/edge-property-assignments": "config",
        "/property-definitions": "config",
        "/property-assignments": "config",
        "/nodes": "nodes",
    }

    # Page name mapping for navbar brand
    page_names = {
        "/": "Tracer",
        "/network": "Tracer - Graphs",
        "/breakdowns": "Tracer - Components",
        "/edges": "Tracer - Edges",
        "/nodes": "Tracer - Nodes",
        "/edge-types": "Tracer - Edge Types",
        "/node-types": "Tracer - Node Types",
        "/node-property-definitions": "Tracer - Node Property Definitions",
        "/edge-property-definitions": "Tracer - Edge Property Definitions",
        "/node-property-values": "Tracer - Node Property Values",
        "/edge-property-values": "Tracer - Edge Property Values",
        "/node-property-assignments": "Tracer - Node Property Assignments",
        "/edge-property-assignments": "Tracer - Edge Property Assignments",
        "/property-definitions": "Tracer - Property Definitions",
        "/property-assignments": "Tracer - Property Assignments",
    }

    active_page = nav_map.get(pathname, None)
    brand_text = page_names.get(pathname, "Tracer")

    nav_classes = [
        "text-white" if page == active_page else "text-white-50"
        for page in ["home", "network", "breakdowns", "edges", "nodes"]
    ]

    config_class = "text-white" if active_page == "config" else "text-white-50"

    return nav_classes + [config_class, brand_text]


if __name__ == "__main__":
    logger.info("Starting the Dash Server...")
    app.run(debug=True)
