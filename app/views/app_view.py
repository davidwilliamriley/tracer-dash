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
            # Header
            html.Header([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H2("Tracer", className="d-flex align-items-center my-lg-0 me-lg-auto text-white text-decoration-none fw-light"),
                            html.Ul([
                                html.Li(html.A([html.I(className="bi bi-house-door-fill"), " Home"], href="/", className="nav-link text-secondary")),
                                html.Li(html.A([html.I(className="bi bi-speedometer"), " Dashboards"], href="/dashboards", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-file-earmark-richtext"), " Reports"], href="/reports", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-bezier2"), " Networks"], href="/networks", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-diagram-2"), " Graphs"], href="/graphs", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-arrow-repeat"), " Edges"], href="/edges", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-link-45deg"), " Relations"], href="/relations", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-plus-circle"), " Nodes"], href="/nodes", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-gear"), " Settings"], href="/settings", className="nav-link text-white")),
                                html.Li(html.A([html.I(className="bi bi-question-circle"), " Help"], href="/help", className="nav-link text-white")),
                            ], className="nav col-12 col-lg-auto justify-content-center my-md-0 text-small", role="navigation")
                        ], className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start")
                    ], className="container-fluid")
                ], className="text-bg-dark px-4 py-3")
            ], className="header"),
            
            # Main Content
            html.Main([
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
                                    dbc.Button("Go to Dashboards", id="dashboards-card", color="primary", className="btn-fixed-width")
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
                                    dbc.Button("View Reports", id="reports-card", color="success", className="btn-fixed-width")
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
                                    dbc.Button("Explore Networks", id="networks-card", color="info", className="btn-fixed-width")
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
                                    dbc.Button("View Graphs", id="graphs-card", color="warning", className="btn-fixed-width")
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
                                    dbc.Button("Manage Edges", id="edges-card", color="danger", className="btn-fixed-width")
                                ], className="card-body text-center")
                            ], className="card bg-light h-100 shadow-sm")
                        ], className="col-lg-3 col-md-6"),
                        
                        # Card 6 - Relations
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.I(className="bi bi-link-45deg display-3 text-secondary mb-3"),
                                    html.H5("Relations", className="card-title"),
                                    html.P("Define relations in your System.", className="card-text mb-2"),
                                    dbc.Button("Manage Relations", id="relations-card", color="dark", className="btn-fixed-width")
                                ], className="card-body text-center")
                            ], className="card bg-light h-100 shadow-sm")
                        ], className="col-lg-3 col-md-6"),
                        
                        # Card 7 - Nodes
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.I(className="bi bi-plus-circle display-3 text-secondary mb-3"),
                                    html.H5("Nodes", className="card-title"),
                                    html.P("Create and manage Nodes.", className="card-text mb-2"),
                                    dbc.Button("Manage Nodes", id="nodes-card", color="secondary", className="btn-fixed-width")
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
                                    dbc.Button("Get Help", id="help-card", color="light", outline=True, className="btn-fixed-width")
                                ], className="card-body text-center")
                            ], className="card bg-light h-100 shadow-sm")
                        ], className="col-lg-3 col-md-6"),
                        
                    ], className="row g-3")
                ], className="container px-4 py-5"),
                
                # Content area for other pages
                html.Div(id="main-content")
                
            ], className="content"),
            
            # Footer
            html.Footer([
                html.Div([
                    html.P("Created by Rail Engineering & Integration (REI) @ John Holland Group Pty. Ltd.", className="text-muted")
                ], className="container-fluid d-flex justify-content-end p-3")
            ], className="footer"),
            
            dcc.Store(id="current-page", data="dashboard"),
            dcc.Store(id="app-data"),
            
        ])
        
    def show_message(self, message, message_type="info"):
        pass