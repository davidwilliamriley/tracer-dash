# views/dashboards_view.

# Imports
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from typing import Dict, Any


class DashboardView:
    def __init__(self):
        pass

    def create_layout(self):
        return dbc.Container(
            [
                html.H1("Dashboards", className="my-4"),
                html.P("This is a Placeholder for the Dashboards.", className="mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 1"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 2"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 3"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4)
                ], className="mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 4"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 5"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Panel 6"),
                            dbc.CardBody([
                                html.P("This is a blank panel for a Metric.", className="card-text")
                            ])
                        ], className="pt-2")
                    ], width=4)
                ], className="mb-4")
            ],
            fluid=True,
        )
