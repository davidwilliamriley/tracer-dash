# pages/node_property_assignments.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(
    __name__, path="/node-property-assignments", name="Node Property Assignments"
)


def layout():
    return dbc.Container(
        [
            html.H2("Node Property Assignments", className="mb-3"),
            html.P(
                "Node Property Assignments page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
