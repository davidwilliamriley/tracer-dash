# pages/node_types.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/node-types", name="Node Types")


def layout():
    return dbc.Container(
        [
            html.H2("Node Types", className="mb-3"),
            html.P(
                "Node Types page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
