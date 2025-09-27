# views/reports_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any


class ReportView:
    """View layer for Reports page - handles UI Layout and Components"""

    def __init__(self):
        pass

    def create_layout(self) -> dbc.Container:
        """Creates the layout for the Reports page"""
        return dbc.Container(
            [
                html.H1("Reports", className="my-4"),
                html.P("This is a Placeholder for the Reports.", className="mb-4"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select the Report:", className="form-label"
                                ),
                                dcc.Dropdown(
                                    id="report-dropdown",
                                    options=[
                                        {
                                            "label": "Monthly Sales Report",
                                            "value": "monthly_sales",
                                        },
                                        {
                                            "label": "Inventory Status Report",
                                            "value": "inventory_status",
                                        },
                                        {
                                            "label": "Customer Feedback Report",
                                            "value": "customer_feedback",
                                        },
                                    ],
                                    value="monthly_sales",
                                    className="mb-3",
                                ),
                            ]
                        )
                    ]
                ),
                # Report Display
                dbc.Row([dbc.Col([html.Div(id="report-output")])]),
            ],
            fluid=True,
        )
