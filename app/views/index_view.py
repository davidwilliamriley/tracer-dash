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
            # First Row of Cards
            dbc.Row([
                # Card 1 - Dashboard
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-speedometer display-3 text-primary mb-3"),
                            html.H5("Dashboard", className="card-title"),
                            html.P("Get an overview of the System.", className="card-text mb-2"),
                            html.A("Go to Dashboard", href="/dashboard", className="btn btn-primary btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
                
                # Card 2 - Reports
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-file-earmark-richtext display-3 text-success mb-3"),
                            html.H5("Reports", className="card-title"),
                            html.P("Generate detailed Reports.", className="card-text mb-2"),
                            html.A("View Reports", href="/reports", className="btn btn-success btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
                
                # Card 3 - Networks
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-bezier2 display-3 text-info mb-3"),
                            html.H5("Networks", className="card-title"),
                            html.P("Visualize with interactive Networks.", className="card-text mb-2"),
                            html.A("Explore Networks", href="/network", className="btn btn-info btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
                
                # Card 4 - Breakdowns
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-diagram-2 display-3 text-warning mb-3"),
                            html.H5("Breakdowns", className="card-title"),
                            html.P("Navigate network Breakdowns.", className="card-text mb-2"),
                            html.A("View Breakdowns", href="/breakdowns", className="btn btn-warning btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
            ], className="g-3 mb-3"),
            
            # Second Row of Cards
            dbc.Row([
                # Card 5 - Edges
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-arrow-repeat display-3 text-danger mb-3"),
                            html.H5("Edges", className="card-title"),
                            html.P("Create and manage Edges.", className="card-text mb-2"),
                            html.A("Manage Edges", href="/edges", className="btn btn-danger btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
                
                # Card 6 - Nodes
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-plus-circle display-3 text-secondary mb-3"),
                            html.H5("Nodes", className="card-title"),
                            html.P("Create and manage Nodes.", className="card-text mb-2"),
                            html.A("Manage Nodes", href="/nodes", className="btn btn-secondary btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),

                # Card 7 - Edge Types
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-link-45deg display-3 text-dark mb-3"),
                            html.H5("Edge Types", className="card-title"),
                            html.P("Define Edge Types in your System.", className="card-text mb-2"),
                            html.A("Manage Edge Types", href="/edge-types", className="btn btn-dark btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
                
                # Card 8 - Help
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.I(className="bi bi-life-preserver display-3 text-muted mb-3"),
                            html.H5("Help", className="card-title"),
                            html.P("Get assistance with the App.", className="card-text mb-2"),
                            html.A("Get Help", href="/help", className="btn btn-outline-dark btn-fixed-width")
                        ], className="text-center")
                    ], className="h-100 shadow-sm")
                ], className="col-lg-3 col-md-6"),
            ], className="g-3")
        ], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '100px', 'display': 'flex', 'flexDirection': 'column'}, className="py-3")