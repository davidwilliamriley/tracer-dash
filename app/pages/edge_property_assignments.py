# pages/edge_property_assignments.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__, path="/edge-property-assignments", name="Edge Property Assignments"
)


def layout():
    return dbc.Container(
        [
            html.H2("Edge Property Assignments", className="mb-3"),
            html.P(
                "Edge Property Assignments page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
