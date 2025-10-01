# views/index_view.py

import dash
from dash import html, dcc, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc


class IndexView:
    def __init__(self):
        return
   
    def get_layout(self):
        """Create the main layout for the home page"""

        return dbc.Container([
            dbc.Row([
                html.Nav([
                    html.Ol([
                        html.Li(html.A("Home", href="#"), className="breadcrumb-item active")
                    ], className="breadcrumb mb-2")
                ]), 
                html.H2("Home", className="mb-1"),
                html.P("Welcome to the Tracer Network Analysis Application.", className="text-muted mb-4")
            ]),

            # First Row of Cards
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-speedometer display-3 text-primary mb-3"),
                                html.H5("Dashboards", className="card-title"),
                                html.P("Get an overview of the System.", className="card-text mb-2"),
                                dbc.Button("Go to Dashboards", href="/dashboards", color="primary", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
        
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-file-earmark-richtext display-3 text-success mb-3"),
                                html.H5("Reports", className="card-title"),
                                html.P("Generate detailed Reports.", className="card-text mb-2"),
                                dbc.Button("View Reports", href="/reports", color="success", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-bezier2 display-3 text-info mb-3"),
                                html.H5("Networks", className="card-title"),
                                html.P("Visualize with interactive Networks.", className="card-text mb-2"),
                                dbc.Button("Explore Networks", href="/networks", color="info", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-diagram-2 display-3 text-warning mb-3"),
                                html.H5("Breakdowns", className="card-title"),
                                html.P("Navigate network Breakdowns.", className="card-text mb-2"),
                                dbc.Button("View Breakdowns", href="/breakdowns", color="warning", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4")
            ], className="g-3"),

            # Second Row of Cards
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-arrow-repeat display-3 text-danger mb-3"),
                                html.H5("Edges", className="card-title"),
                                html.P("Create and manage Edges.", className="card-text mb-2"),
                                dbc.Button("Manage Edges", href="/edges", color="danger", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-plus-circle display-3 text-secondary mb-3"),
                                html.H5("Nodes", className="card-title"),
                                html.P("Create and manage Nodes.", className="card-text mb-2"),
                                dbc.Button("Manage Nodes", href="/nodes", color="secondary", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-link-45deg display-3 text-dark mb-3"),
                                html.H5("Edge Types", className="card-title"),
                                html.P("Define Edge Types in your System.", className="card-text mb-2"),
                                dbc.Button("Manage Edge Types", href="/edge-types", color="dark", className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="bi bi-life-preserver display-3 text-muted mb-3"),
                                html.H5("Help", className="card-title"),
                                html.P("Get assistance with the App.", className="card-text mb-2"),
                                dbc.Button("Get Help", href="/help", color="light", outline=True, className="btn-fixed-width")
                            ], className="text-center")
                        ])
                    ], className="bg-light h-100 shadow-sm")
                ], lg=3, md=6, className="mb-4")
            ], className="g-3")
        ], className="container px-4 py-5")