# views/dashboards_view.

# Imports
from dash import html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import logging
from typing import Dict, Any

logger = logging.getLogger('TracerApp')


class DashboardView:
    """View layer for Dashboards page - handles UI Layout and Components"""

    def __init__(self):
        pass

    def _make_toast(self) -> dbc.Toast:
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

    def get_layout(self):
        logger.info("Generating layout for DashboardView")
        return dbc.Container(
            [
                self._make_toast(),
                
                html.H1([html.I(className="bi bi-speedometer me-2"), "Dashboard"], className="my-4 text-primary"),
                html.P("Metrics for the Network", className="mb-4 text-muted"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Descriptive Metrics"),
                                dbc.CardBody([

                                    dash_table.DataTable(
                                        id="descriptive-metrics-table",
                                        style_table={'overflowX': 'auto'},
                                        style_cell={
                                            'textAlign': 'left',
                                            'padding': '10px'
                                        },
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ])
                        ], className="mb-4",
                    )], md=12),
                ]),

                dbc.Accordion([
                    dbc.AccordionItem([dcc.Graph(id="completeness-metrics")], title="Completeness Metrics"),
                    dbc.AccordionItem([dcc.Graph(id="efficiency-metrics")], title="Efficiency Metrics"),
                    dbc.AccordionItem([dcc.Graph(id="robustness-metrics")], title="Robustness Metrics"),
                    dbc.AccordionItem([dcc.Graph(id="resilience-metrics")], title="Resilience Metrics"),
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
    
