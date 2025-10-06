# views/networks_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any
import json


class NetworkView:
    """View layer for networks page - handles UI layout and components"""

    def __init__(self):
        pass

    @staticmethod
    def _create_toast() -> dbc.Toast:
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

    @staticmethod
    def create_layout(networks_data: Dict[str, Any]) -> dbc.Container:
        return dbc.Container(
            [
                NetworkView._create_toast(),

                html.Div(id="cytoscape-data-div",  children=json.dumps(networks_data), style={"display": "none"}),

                html.H1([html.I(className="bi bi-bezier2 me-2"), "Network"], className="my-4 text-primary"),
                html.P("Visualise and Analyse the Network.", className="mb-4 text-muted"),

                NetworkView._create_filters(),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "100px",
                "display": "flex",
                "flexDirection": "column",
            },
        )

    @staticmethod
    def _create_filters() -> html.Div:
        return html.Div([
            dbc.Card([
                dbc.CardBody([

                    # First Row - Graph Root Select
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="filter-graph-select",
                                options=[
                                    {"label": "All Roots", "value": "all"},
                                    {"label": "Root 1", "value": "root1"},
                                    {"label": "Root 2", "value": "root2"},
                                    {"label": "Root 3", "value": "root3"},
                                ],
                                placeholder="Select a Graph Root Node...",
                                disabled=True
                            ),
                            width=12,
                            className="mb-3",
                        ),
                    ]),

                    # Filter Row - Element, "include", Property, Value, Apply, Reset
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="filter-element-select",
                                options=[
                                    {"label": "All Elements", "value": "all"},
                                    {"label": "Edges", "value": "edges"},
                                    {"label": "Nodes", "value": "nodes"},
                                ],
                                value="all",
                                disabled=True,
                            ),
                            width=12,
                            lg=2,
                            className="mb-3 mb-lg-0",
                        ),

                        # label
                        dbc.Col(
                            html.Div("include", className="text-center text-muted", 
                                    style={"lineHeight": "38px"}),
                            lg=1,
                            className="d-none d-lg-block",
                        ),

                        dbc.Col(
                            dbc.Select(
                                id="filter-property-select",
                                options=[{"label": "All Properties", "value": "all"}],
                                value="all",
                                disabled=True,
                            ),
                            width=12,
                            lg=2,
                            className="mb-3 mb-lg-0",
                        ),

                        dbc.Col(
                            dbc.Input(
                                id="filter-value-input",
                                placeholder="Add Search Terms",
                            ),
                            width=12,
                            lg=5,
                            className="mb-3 mb-lg-0",
                        ),

                        dbc.Col(
                            dbc.Button([html.I(className="bi bi-filter me-1"), "Apply"],
                                id="apply-element-btn",
                                outline=True,
                                color="primary",
                                size="md",
                                className="w-100",
                            ),
                            width=6,
                            lg=1,
                            className="mb-3 mb-lg-0 pe-1",
                        ),
                        
                        dbc.Col(
                            dbc.Button([html.I(className="bi bi-arrow-clockwise me-1"), "Reset"],
                                id="reset-element-btn",
                                outline=True,
                                color="secondary",
                                size="md",
                                className="w-100",
                            ),
                            width=6,
                            lg=1,
                            className="ps-1",
                        ),
                    ], className="align-items-center g-3"),
                    
                    # Layout Algorithm Row
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="layout-algorithm-select",
                                options=[
                                    {"label": "fCoSE (Force-directed)", "value": "fcose"},
                                    {"label": "Breadthfirst", "value": "breadthfirst"},
                                    {"label": "Circle", "value": "circle"},
                                    {"label": "Concentric", "value": "concentric"},
                                    {"label": "Cose (Force-directed)", "value": "cose"},
                                    {"label": "Grid", "value": "grid"},
                                ],
                                placeholder="Select a Layout Algorithm...",
                                value="fcose",
                                disabled=True
                            ),
                            width=12,
                            className="mt-3",
                        ),
                    ]),
                ]),
            ], className="mb-4"),
            
            # Network Graph Container
            NetworkView._create_cytoscape_container(),     
        ])

    @staticmethod
    def _create_cytoscape_container() -> dbc.Card:
        return dbc.Card([
            # dbc.CardHeader(html.H5("Network Graph", className="mb-0")),
                dbc.CardBody([
                        dbc.Spinner(
                            html.Div(
                                id="cytoscape-container",
                                style={
                                    "width": "100%",
                                    "height": "70vh",
                                    "border-radius": "0.375rem",
                                    "backgroundColor": "white",
                                    "position": "relative"
                                },
                            ),
                            id="cytoscape-spinner",
                            color="primary"
                        ),
                        html.Div(id="cytoscape-trigger", style={"display": "none"})
                    ], className="p-0",  
                ),
            ], className="mb-4",
        )
    
    @staticmethod
    def get_cytoscape_client_callback() -> str:
        """Return a simple JavaScript function that delegates to the external callback"""
        return """
        function(networkDataJson, filteredValue) {
            // Delegate to the external callback function loaded from cytoscape_callback.js
            if (typeof window.cytoscapeCallback === 'function') {
                return window.cytoscapeCallback(networkDataJson, filteredValue);
            } else {
                console.error('cytoscapeCallback function not found. Make sure cytoscape_callback.js is loaded.');
                return window.dash_clientside.no_update;
            }
        }
        """