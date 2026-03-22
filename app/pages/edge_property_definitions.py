# pages/edge_property_definitions.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__, path="/edge-property-definitions", name="Edge Property Definitions"
)


def layout():
    return dbc.Container(
        [
            html.H2("Edge Property Definitions", className="mb-3"),
            html.P(
                "Edge Property Definitions page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
