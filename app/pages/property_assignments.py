# pages/property_assignments.py

import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/property-assignments", name="Property Assignments")


def layout():
    return dbc.Container(
        [
            html.H2("Property Assignments", className="mb-3"),
            html.P(
                "Property Assignments management page scaffolded. CRUD implementation pending.",
                className="text-muted",
            ),
        ],
        fluid=True,
        className="py-3",
    )
