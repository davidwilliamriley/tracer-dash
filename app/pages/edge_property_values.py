# pages/edge_property_values.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/edge-property-values", name="Edge Property Values")


def layout():
    return dbc.Container(
        [
            html.H2("Edge Property Values", className="mb-3"),
            html.P(
                "Edge Property Values page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
