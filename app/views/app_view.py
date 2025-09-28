# views/view.py

import dash
from dash import html, dcc, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class View:
    def __init__(self):
        self.controller = None
    
    def get_layout(self):
        return html.Div([
            html.Div([

                # Navigation Cards
                html.Div([

                    # First Row of Cards
                    html.Div([
                        
                        # Card 1 - Dashboards
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-speedometer display-3 text-primary mb-3"),
                                html.H5("Dashboards", className="card-title"),
                                html.P("Get an overview of the System.", className="card-text mb-2"),
                                html.A("Go to Dashboards", href="/dashboards", className="btn btn-primary btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Card 2 - Reports
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-file-earmark-richtext display-3 text-success mb-3"),
                                html.H5("Reports", className="card-title"),
                                html.P("Generate detailed Reports.", className="card-text mb-2"),
                                html.A("View Reports", href="/reports", className="btn btn-success btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Card 3 - Networks
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-bezier2 display-3 text-info mb-3"),
                                html.H5("Networks", className="card-title"),
                                html.P("Visualize with interactive Networks.", className="card-text mb-2"),
                                html.A("Explore Networks", href="/networks", className="btn btn-info btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Card 4 - Graphs
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-diagram-2 display-3 text-warning mb-3"),
                                html.H5("Graphs", className="card-title"),
                                html.P("Navigate network Graphs.", className="card-text mb-2"),
                                html.A("View Graphs", href="/graphs", className="btn btn-warning btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Second Row of Cards
                    # Card 5 - Edges
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-arrow-repeat display-3 text-danger mb-3"),
                                html.H5("Edges", className="card-title"),
                                html.P("Create and manage Edges.", className="card-text mb-2"),
                                html.A("Manage Edges", href="/edges", className="btn btn-danger btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Card 6 - Nodes
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-plus-circle display-3 text-secondary mb-3"),
                                html.H5("Nodes", className="card-title"),
                                html.P("Create and manage Nodes.", className="card-text mb-2"),
                                html.A("Manage Nodes", href="/nodes", className="btn btn-secondary btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),

                    # Card 7 - Edge Types
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-link-45deg display-3 text-secondary mb-3"),
                                html.H5("Edge Types", className="card-title"),
                                html.P("Define Edge Types in your System.", className="card-text mb-2"),
                                html.A("Manage Edge Types", href="/edge-types", className="btn btn-dark btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                    # Card 8 - Help
                    html.Div([
                        html.Div([
                            html.Div([
                                html.I(className="bi bi-life-preserver display-3 text-muted mb-3"),
                                html.H5("Help", className="card-title"),
                                html.P("Get assistance with the App.", className="card-text mb-2"),
                                html.A("Get Help", href="/help", className="btn btn-outline-dark btn-fixed-width")
                            ], className="card-body text-center")
                        ], className="card bg-light h-100 shadow-sm")
                    ], className="col-lg-3 col-md-6"),
                    
                ], className="row g-3")
            ], className="container px-4 py-5")
        ])