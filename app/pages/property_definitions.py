# pages/property_definitions.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/property-definitions", name="Property Definitions")


def layout():
    return dbc.Container(
        [
            html.H2("Property Definitions", className="mb-3"),
            html.P(
                "Property Definitions management page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
