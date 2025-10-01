# views/dashboards_view.

# Imports
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from typing import Dict, Any


class DashboardView:
    """View layer for Dashboards page - handles UI Layout and Components"""

    def __init__(self):
        pass

    def _create_toast(self) -> dbc.Toast:
        return dbc.Toast(
            id="networks-toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            style={
                "position": "fixed",
                "bottom": 20,
                "left": 20,
                "width": 350,
                "z-index": 9999,
            },
        )

    def create_layout(self):
        return dbc.Container(
            [
                self._create_toast(),
                
                html.H1([html.I(className="bi bi-speedometer me-2"), "Dashboard"], className="my-4"),
                html.P("Metrics for the current Network.", className="mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Descriptive Metrics"),
                            dbc.CardBody([dcc.Graph(id="descriptive-metrics")]),
                        ], className="mb-4",
                    )], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("System Health"),
                            dbc.CardBody([dcc.Graph(id="system-health-graph")]),
                        ], className="mb-4",
                    )], md=6),
                ]),
                dbc.Accordion([
                    dbc.AccordionItem([dcc.Graph(id="completeness-metrics")], title="Network Completeness"),
                    dbc.AccordionItem([dcc.Graph(id="robustness-metrics")], title="Network Robustness"),
                    dbc.AccordionItem([dcc.Graph(id="resilience-metrics")], title="Network Resilience"),
                ],
                    start_collapsed=True,
                    always_open=False,
                ),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "100px",
                "display": "flex",
                "flexDirection": "column",
            },
        )
