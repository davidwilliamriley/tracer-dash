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
    
    def render_networks_page(self):
        return html.Div([
            html.H2("Network Configuration", className="mb-4"),
                     
            dbc.Card([
                dbc.CardHeader("Filter & Sort the Graph"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Filter by Graph:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id="graph-filter",
                                options=[
                                    {"label": "Option 1", "value": "opt1"},
                                    {"label": "Option 2", "value": "opt2"},
                                    {"label": "Option 3", "value": "opt3"},
                                    {"label": "Option 4", "value": "opt4"},
                                ],
                                placeholder="Select a Graph Root...",
                            )
                        ], width=8),
                        dbc.Col([
                            html.Div([  # Wrapper div to push buttons to bottom
                                dbc.Button("Submit", color="primary", className="me-2"),
                                dbc.Button("Reset", color="secondary")
                            ], className="d-flex justify-content-end")
                        ], width=4, className="d-flex align-items-end")
                    ], align="center")
                ])
            ], className="mb-4"),
            
            # About section
            dbc.Card([
                dbc.CardHeader("ℹ️ About the Graph"),
                dbc.CardBody([
                    html.P("💡 To-Do : Add a Description of the Network and the applied Filters"),
                    html.P("💡 To-Do : Add Network Metrics"),
                    html.P("💡 To-Do : Add Option to export Configuration & Filters"),
                ])
            ], className="mb-4"),
            
            # Network visualization
            dbc.Card([
                dbc.CardHeader("Network Topology"),
                dbc.CardBody([
                    dcc.Graph(id="network-graph", style={"height": "600px"})
                ])
            ])
        ])
    
    def render_data_page(self):
        """Render the data management page"""
        return html.Div([
            html.H2("📊 Data Management", className="mb-4"),
            
            # Toolbar
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("🔄 Refresh Data", id="refresh-btn", color="info"),
                        dbc.Button("✅ Validate Integrity", id="validate-btn", color="success"),
                        dbc.Button("📈 Show Statistics", id="stats-btn", color="warning"),
                        dbc.Button("📥 Export All", id="export-btn", color="secondary"),
                    ])
                ], width=12)
            ], className="mb-4"),
            
            # Tabs for different data types
            dbc.Tabs([
                dbc.Tab(label="Nodes", tab_id="nodes-tab"),
                dbc.Tab(label="Edges", tab_id="edges-tab"),
                dbc.Tab(label="Edge Types", tab_id="edge-types-tab"),
            ], id="data-tabs", active_tab="nodes-tab"),
            
            html.Div(id="data-table-content", className="mt-4")
        ])
    
    def render_reports_page(self):
        """Render the reports page"""
        return html.Div([
            html.H2("📄 Reports", className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id="report-selector",
                        options=[
                            {"label": "Select a Report...", "value": "none"},
                            {"label": "Network Topology Report", "value": "topology"},
                            {"label": "Node Statistics Report", "value": "node-stats"},
                            {"label": "Edge Analysis Report", "value": "edge-analysis"},
                        ],
                        value="none"
                    )
                ], width=6),
                dbc.Col([
                    dbc.Button("Generate Report", id="generate-report-btn", color="primary")
                ], width=6)
            ]),
            
            html.Div(id="report-output", className="mt-4")
        ])
    
    def render_settings_page(self):
        """Render the settings page"""
        return html.Div([
            html.H2("⚙️ Settings", className="mb-4"),
            
            dbc.Card([
                dbc.CardHeader("Application Settings"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Theme:", className="fw-bold"),
                            dcc.Dropdown(
                                id="theme-selector",
                                options=[
                                    {"label": "Light", "value": "light"},
                                    {"label": "Dark", "value": "dark"},
                                    {"label": "Auto", "value": "auto"},
                                ],
                                value="light"
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Checklist(
                                id="settings-checkboxes",
                                options=[
                                    {"label": "Enable Notifications", "value": "notifications"},
                                    {"label": "Auto-save Changes", "value": "auto-save"},
                                ],
                                value=["notifications", "auto-save"]
                            )
                        ], width=8)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Save Settings", id="save-settings-btn", color="success", className="me-2"),
                            dbc.Button("Reset to Default", id="reset-settings-btn", color="warning")
                        ])
                    ])
                ])
            ])
        ])
    
    def create_network_graph(self, graph_data):
        """Create a network graph using Plotly"""
        if not graph_data or 'error' in graph_data:
            return go.Figure().add_annotation(
                text="Network data unavailable",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Extract nodes and edges
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        
        # Create edge traces
        edge_x = []
        edge_y = []
        edge_info = []
        
        # Simple layout - you might want to use a proper network layout algorithm
        import math
        node_positions = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = math.cos(angle)
            y = math.sin(angle)
            node_positions[node['id']] = (x, y)
        
        for edge in edges:
            x0, y0 = node_positions.get(edge['source'], (0, 0))
            x1, y1 = node_positions.get(edge['target'], (0, 0))
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        for node in nodes:
            x, y = node_positions.get(node['id'], (0, 0))
            node_x.append(x)
            node_y.append(y)
            node_text.append(node.get('label', node['id']))
            node_colors.append(node.get('color', '#4ECDC4'))
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=[node.get('size', 20) for node in nodes],
                color=node_colors,
                line=dict(width=2, color='white')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Network Topology',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Click on nodes for more information",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="#888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    def show_message(self, message, message_type="info"):
        """Show a message (in Dash, this would typically be handled through callbacks)"""
        pass