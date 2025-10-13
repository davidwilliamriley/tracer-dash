# views/networks_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any, Optional
import json

from utils.toast_utils import ToastFactory


class NetworkView:
    """View layer for networks page - handles UI layout and components"""

    def __init__(self):
        pass

    @staticmethod
    def create_layout(networks_data: Dict[str, Any]) -> dbc.Container:
        return dbc.Container(
            [
                ToastFactory.create_toast(toast_id="networks-toast-message"),
                dcc.Store(id="toast-store"),
                html.Div(
                    id="cytoscape-data-div",
                    children=json.dumps(networks_data),
                    style={"display": "none"},
                ),
                NetworkView._create_filters(),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "20px",
                "display": "flex",
                "flexDirection": "column",
            },
        )

    @staticmethod
    def _create_filters() -> html.Div:
        return html.Div(
            [
                # Search Section - Clean and Simple
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="filter-value-input",
                                placeholder="Search Nodes and Edges by Identifier, Name, Description...",
                                disabled=False,
                                size="md",
                                className="mt-3",
                            ),
                            width=12,
                            md=10,
                        ),
                        dbc.Col(
                            dbc.Button(
                                [
                                    html.I(className="bi bi-x-circle me-1"),
                                    "Reset",
                                ],
                                id="reset-element-btn",
                                outline=True,
                                color="primary",
                                size="md",
                                className="w-100 mt-3",
                                disabled=False,
                            ),
                            width=12,
                            md=2,
                        ),
                    ],
                    className="align-items-center g-3 mb-3",
                ),
                # Filters & Controls Accordion
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                # First Row - Graph Root Select
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Select(
                                                id="filter-graph-select",
                                                options=[
                                                    {
                                                        "label": "All Roots",
                                                        "value": "all",
                                                    }
                                                ],
                                                value="all",
                                                placeholder="Select a Graph Root Node...",
                                                disabled=False,
                                            ),
                                            width=12,
                                            className="mb-3",
                                        ),
                                        # dbc.Col(
                                        #     dbc.Button(
                                        #         [
                                        #             html.I(
                                        #                 className="bi bi-x-circle me-1"
                                        #             ),
                                        #             "Reset",
                                        #         ],
                                        #         id="reset-graph-filter-btn",
                                        #         outline=True,
                                        #         color="primary",
                                        #         size="md",
                                        #         className="w-100",
                                        #         disabled=False,
                                        #     ),
                                        #     width=1,
                                        #     lg=1,
                                        # ),
                                    ]
                                ),
                                # Filter Row - Elements, Edge Type, and Labels
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Select(
                                                    id="filter-element-select",
                                                    options=[
                                                        {
                                                            "label": "Show All Elements",
                                                            "value": "all",
                                                        },
                                                        {
                                                            "label": "Edges Only",
                                                            "value": "edges",
                                                        },
                                                        {
                                                            "label": "Nodes Only",
                                                            "value": "nodes",
                                                        },
                                                    ],
                                                    value="all",
                                                    disabled=False,
                                                    size="md",
                                                ),
                                            ],
                                            width=12,
                                            lg=4,
                                            className="mb-3 mb-lg-0",
                                        ),
                                        dbc.Col(
                                            [
                                                # dbc.Label(
                                                #     "Edge Type Filter:",
                                                #     className="form-label fw-bold small",
                                                # ),
                                                dbc.Select(
                                                    id="filter-edgetype-select",
                                                    options=[
                                                        {
                                                            "label": "All Edge Types",
                                                            "value": "all",
                                                        },
                                                        # Dynamic options will be populated via callback
                                                    ],
                                                    value="all",
                                                    disabled=False,
                                                    size="md",
                                                ),
                                            ],
                                            width=12,
                                            lg=4,
                                            className="mb-3 mb-lg-0",
                                        ),
                                        dbc.Col(
                                            [
                                                # dbc.Label(
                                                #     "Show Labels:",
                                                #     className="form-label fw-bold small",
                                                # ),
                                                dbc.Select(
                                                    id="filter-labels-select",
                                                    options=[
                                                        {
                                                            "label": "Show All Labels",
                                                            "value": "all",
                                                        },
                                                        {
                                                            "label": "Node Labels Only",
                                                            "value": "nodes",
                                                        },
                                                        {
                                                            "label": "Edge Labels Only",
                                                            "value": "edges",
                                                        },
                                                        {
                                                            "label": "Hide Labels",
                                                            "value": "none",
                                                        },
                                                    ],
                                                    value="all",
                                                    disabled=False,
                                                    size="md",
                                                ),
                                            ],
                                            width=12,
                                            lg=4,
                                            className="mb-3 mb-lg-0",
                                        ),
                                    ],
                                    className="align-items-end g-3",
                                ),
                                # Network Statistics Row
                                # dbc.Row(
                                #     [
                                #         dbc.Col(
                                #             html.Div(
                                #                 id="network-stats-display",
                                #                 className="text-muted small mt-2",
                                #                 children="Loading network statistics...",
                                #             ),
                                #             width=12,
                                #         ),
                                #     ]
                                # ),
                                # Layout Algorithm Row with Reset Button
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Select(
                                                id="layout-algorithm-select",
                                                options=[
                                                    {
                                                        "label": "Breadthfirst",
                                                        "value": "breadthfirst",
                                                    },
                                                    {
                                                        "label": "Circle",
                                                        "value": "circle",
                                                    },
                                                    {
                                                        "label": "COLA (Constraint-based)",
                                                        "value": "cola",
                                                    },
                                                    {
                                                        "label": "Concentric",
                                                        "value": "concentric",
                                                    },
                                                    {
                                                        "label": "Cose (Force-directed)",
                                                        "value": "cose",
                                                    },
                                                    {
                                                        "label": "Dagre (Hierarchical)",
                                                        "value": "dagre",
                                                    },
                                                    {
                                                        "label": "fCoSE (Force-directed)",
                                                        "value": "fcose",
                                                    },
                                                    {"label": "Grid", "value": "grid"},
                                                    {
                                                        "label": "Klay (Layered) - Experimental",
                                                        "value": "klay",
                                                    },
                                                    {
                                                        "label": "Random",
                                                        "value": "random",
                                                    },
                                                ],
                                                placeholder="Select a Layout Algorithm...",
                                                value="fcose",
                                                disabled=False,
                                            ),
                                            width=12,
                                            lg=10,
                                            className="mt-3",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-arrow-clockwise me-1"
                                                    ),
                                                    "Reset All Filters",
                                                ],
                                                id="reset-all-filters-btn",
                                                outline=True,
                                                color="primary",
                                                size="md",
                                                className="w-100 mt-3",
                                                title="Reset all filters to default values",
                                            ),
                                            width=12,
                                            lg=2,
                                            className="mt-3",
                                        ),
                                    ],
                                    className="align-items-end g-3",
                                ),
                            ],
                            title=[
                                html.I(className="bi bi-funnel me-2"),
                                "Filters & Controls",
                            ],
                            item_id="filters-accordion",
                        ),
                        # Export Options Accordion
                        dbc.AccordionItem(
                            [
                                # # Export Row
                                # dbc.Row(
                                #     [
                                #         dbc.Col(
                                #             html.Label(
                                #                 "Export Network:",
                                #                 className="form-label fw-bold text-muted",
                                #             ),
                                #             width=12,
                                #             className="mb-3",
                                #         ),
                                #     ]
                                # ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-image me-1"
                                                    ),
                                                    "Export PNG",
                                                ],
                                                id="export-png-btn",
                                                outline=True,
                                                color="primary",
                                                size="md",
                                                className="w-100",
                                            ),
                                            width=6,
                                            lg=2,
                                            className="mb-2 pe-1",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-filetype-svg me-1"
                                                    ),
                                                    "Export SVG",
                                                ],
                                                id="export-svg-btn",
                                                outline=True,
                                                color="primary",
                                                size="md",
                                                className="w-100",
                                            ),
                                            width=6,
                                            lg=2,
                                            className="mb-2 ps-1",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-filetype-json me-1"
                                                    ),
                                                    "Export JSON",
                                                ],
                                                id="export-json-btn",
                                                outline=True,
                                                color="primary",
                                                size="md",
                                                className="w-100",
                                            ),
                                            width=6,
                                            lg=2,
                                            className="mb-2 px-1",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="bi bi-camera me-1"
                                                    ),
                                                    "High-Res PNG",
                                                ],
                                                id="export-highres-png-btn",
                                                outline=True,
                                                color="primary",
                                                size="md",
                                                className="w-100",
                                            ),
                                            width=6,
                                            lg=2,
                                            className="mb-2 px-1",
                                        ),
                                    ],
                                    className="align-items-center g-2",
                                ),
                            ],
                            title=[
                                html.I(className="bi bi-download me-2"),
                                "Graph Export",
                            ],
                            item_id="export-accordion",
                        ),
                    ],
                    start_collapsed=True,
                    className="mb-3 mt-3",
                ),
                # Network Graph Container
                NetworkView._create_cytoscape_container(),
            ]
        )

    @staticmethod
    def _create_cytoscape_container() -> dbc.Card:
        return dbc.Card(
            [
                # dbc.CardHeader(html.H5("Network Graph", className="mb-0")),
                dbc.CardBody(
                    [
                        dbc.Spinner(
                            html.Div(
                                id="cytoscape-container",
                                style={
                                    "width": "100%",
                                    "height": "calc(100vh - 395px)",
                                    "minHeight": "400px",
                                    "borderRadius": "0.375rem",
                                    "backgroundColor": "white",
                                    "position": "relative",
                                },
                            ),
                            id="cytoscape-spinner",
                            color="primary",
                        ),
                        html.Div(id="cytoscape-trigger", style={"display": "none"}),
                    ]
                ),
            ],
        )

    @staticmethod
    def get_cytoscape_client_callback() -> str:
        """Return a simple JavaScript function that delegates to the external callback"""
        return """
        function(networkDataJson, filteredValue, layoutAlgorithm) {
            // Delegate to the external callback function loaded from cytoscape_callback.js
            if (typeof window.cytoscapeCallback === 'function') {
                return window.cytoscapeCallback(networkDataJson, filteredValue, layoutAlgorithm);
            } else {
                console.error('cytoscapeCallback function not found. Make sure cytoscape_callback.js is loaded.');
                return window.dash_clientside.no_update;
            }
        }
        """
