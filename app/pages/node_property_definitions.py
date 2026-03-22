# pages/node_property_definitions.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__, path="/node-property-definitions", name="Node Property Definitions"
)


def layout():
    return dbc.Container(
        [
            html.H2("Node Property Definitions", className="mb-3"),
            html.P(
                "Node Property Definitions page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
