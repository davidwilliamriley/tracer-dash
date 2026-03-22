# pages/types.py

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/types", name="Types")


def _render_node_types_tab():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Node Types", className="card-title"),
                html.P(
                    "Manage Node Types from this unified Types area. "
                    "Full CRUD wiring can be added next.",
                    className="text-muted mb-3",
                ),
                dbc.Button(
                    "Open Legacy Node Types Route",
                    href="/node-types",
                    color="secondary",
                    size="sm",
                ),
            ]
        ),
        className="mt-3",
    )


def _render_edge_types_tab():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Edge Types", className="card-title"),
                html.P(
                    "Manage Edge Types from this unified Types area. "
                    "Full CRUD wiring can be added next.",
                    className="text-muted mb-3",
                ),
                dbc.Button(
                    "Open Legacy Edge Types Route",
                    href="/edge-types",
                    color="secondary",
                    size="sm",
                ),
            ]
        ),
        className="mt-3",
    )


def layout():
    return dbc.Container(
        [
            html.H2("Types", className="mb-3"),
            dcc.Tabs(
                id="types-tabs",
                value="node",
                children=[
                    dcc.Tab(label="Node Types", value="node"),
                    dcc.Tab(label="Edge Types", value="edge"),
                ],
            ),
            html.Div(id="types-tab-content"),
        ],
        fluid=True,
        className="py-3",
    )


@callback(Output("types-tab-content", "children"), Input("types-tabs", "value"))
def render_types_tab(active_tab):
    if active_tab == "edge":
        return _render_edge_types_tab()

    return _render_node_types_tab()
