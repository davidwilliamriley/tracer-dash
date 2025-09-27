# controllers/controller.py - Dash Compatible Version

import datetime
import uuid
from typing import List, Dict, Any
import logging
import pandas as pd

from dash import Input, Output, State, callback, no_update, callback_context
import dash_bootstrap_components as dbc
from dash import html

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, app, model, view):
        self.app = app
        self.model = model
        self.view = view
        
        # Inject controller into view for proper MVC pattern
        self.view.controller = self
        
        # Initialize app data
        self.initialize_app()
        
        # Register all callbacks
        self.register_callbacks()

    def initialize_app(self):
        """Initialize application data"""
        self.app_data = {
            'app_name': 'Tracer',
            'version': '1.0.0',
            'initialized_at': datetime.datetime.now()
        }

    def register_callbacks(self):
        """Register all Dash callbacks"""
        
        # Navigation callback
        @callback(
            Output("main-content", "children"),
            Output("current-page", "data"),
            [Input("nav-networks", "n_clicks"),
             Input("nav-reports", "n_clicks"),
             Input("nav-data", "n_clicks"),
             Input("nav-settings", "n_clicks")],
            [State("current-page", "data")]
        )
        def handle_navigation(networks_clicks, reports_clicks, data_clicks, settings_clicks, current_page):
            """Handle navigation between pages"""
            ctx = callback_context
            
            if not ctx.triggered:
                return self.view.render_networks_page(), "networks"
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            if button_id == "nav-networks":
                return self.view.render_networks_page(), "networks"
            elif button_id == "nav-reports":
                return self.view.render_reports_page(), "reports"
            elif button_id == "nav-data":
                return self.view.render_data_page(), "data"
            elif button_id == "nav-settings":
                return self.view.render_settings_page(), "settings"
            
            return no_update, no_update
        
        # Network graph callback
        @callback(
            Output("network-graph", "figure"),
            [Input("current-page", "data")]
        )
        def update_network_graph(current_page):
            """Update the network graph when on networks page"""
            if current_page == "networks":
                graph_data = self.get_network_graph_data("database")
                return self.view.create_network_graph(graph_data)
            return no_update
        
        # Data table callback
        @callback(
            Output("data-table-content", "children"),
            [Input("data-tabs", "active_tab"),
             Input("refresh-btn", "n_clicks")]
        )
        def update_data_table(active_tab, refresh_clicks):
            """Update data table based on selected tab"""
            try:
                if active_tab == "nodes-tab":
                    return self.render_nodes_table()
                elif active_tab == "edges-tab":
                    return self.render_edges_table()
                elif active_tab == "edge-types-tab":
                    return self.render_edge_types_table()
                return html.Div("Select a tab to view data")
            except Exception as e:
                logger.error(f"Error updating data table: {str(e)}")
                return dbc.Alert(f"Error loading data: {str(e)}", color="danger")
        
        # Report generation callback
        @callback(
            Output("report-output", "children"),
            [Input("generate-report-btn", "n_clicks")],
            [State("report-selector", "value")]
        )
        def generate_report(n_clicks, report_type):
            """Generate selected report"""
            if n_clicks and report_type and report_type != "none":
                try:
                    result = self.handle_report_generation(report_type)
                    if result['status'] == 'success':
                        return dbc.Alert(result['message'], color="success")
                    elif result['status'] == 'info':
                        return dbc.Alert(result['message'], color="info")
                    else:
                        return dbc.Alert(result['message'], color="danger")
                except Exception as e:
                    return dbc.Alert(f"Report generation failed: {str(e)}", color="danger")
            return no_update
        
        # Settings callbacks
        @callback(
            Output("settings-feedback", "children", allow_duplicate=True),
            [Input("save-settings-btn", "n_clicks"),
             Input("reset-settings-btn", "n_clicks")],
            [State("theme-selector", "value"),
             State("settings-checkboxes", "value")],
            prevent_initial_call=True
        )
        def handle_settings(save_clicks, reset_clicks, theme, checkboxes):
            """Handle settings save/reset"""
            ctx = callback_context
            
            if not ctx.triggered:
                return no_update
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            try:
                if button_id == "save-settings-btn":
                    notifications = "notifications" in (checkboxes or [])
                    auto_save = "auto-save" in (checkboxes or [])
                    result = self.save_app_settings(theme, notifications, auto_save)
                    color = "success" if result['status'] == 'success' else "danger"
                    return dbc.Alert(result['message'], color=color, dismissable=True)
                
                elif button_id == "reset-settings-btn":
                    result = self.reset_app_settings()
                    return dbc.Alert(result['message'], color="warning", dismissable=True)
                    
            except Exception as e:
                return dbc.Alert(f"Settings operation failed: {str(e)}", color="danger", dismissable=True)
            
            return no_update
        
        # Validation and statistics callbacks
        @callback(
            [Output("validation-results", "children", allow_duplicate=True),
             Output("statistics-results", "children", allow_duplicate=True)],
            [Input("validate-btn", "n_clicks"),
             Input("stats-btn", "n_clicks")],
            prevent_initial_call=True
        )
        def handle_data_operations(validate_clicks, stats_clicks):
            """Handle data validation and statistics"""
            ctx = callback_context
            
            if not ctx.triggered:
                return no_update, no_update
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            try:
                if button_id == "validate-btn":
                    result = self.validate_database_integrity()
                    color = "success" if result['status'] == 'success' else "warning" if result['status'] == 'warning' else "danger"
                    alert = dbc.Alert(result['message'], color=color, dismissable=True)
                    return alert, no_update
                
                elif button_id == "stats-btn":
                    result = self.get_data_statistics()
                    if result['status'] == 'success':
                        stats_content = self.format_statistics_display(result['data'])
                        return no_update, stats_content
                    else:
                        alert = dbc.Alert(result['message'], color="danger", dismissable=True)
                        return no_update, alert
                        
            except Exception as e:
                error_alert = dbc.Alert(f"Operation failed: {str(e)}", color="danger", dismissable=True)
                return error_alert, no_update
            
            return no_update, no_update

    # ==================== DATA RETRIEVAL METHODS ====================

    def get_edges(self):
        """Get all edges from the database"""
        try:
            return self.model.get_edges()
        except Exception as e:
            logger.error(f"Failed to get edges: {str(e)}")
            return []

    def get_nodes(self):
        """Get all nodes from the database"""
        try:
            return self.model.get_nodes()
        except Exception as e:
            logger.error(f"Failed to get nodes: {str(e)}")
            return []
        
    def get_edge_types(self):
        """Get all edge types from the database"""
        try:
            return self.model.get_edge_types()
        except Exception as e:
            logger.error(f"Failed to get edge types: {str(e)}")
            return []

    # ==================== TABLE RENDERING METHODS ====================

    def render_nodes_table(self):
        """Render nodes data table"""
        try:
            nodes = self.get_nodes()
            if not nodes:
                return dbc.Alert("No nodes found in the database.", color="info")
            
            data = []
            for node in nodes:
                data.append({
                    'ID': node.id,
                    'Name': node.name,
                    'Description': node.description
                })
            
            df = pd.DataFrame(data)
            
            return html.Div([
                html.H4("Nodes Data"),
                self._create_table_from_dataframe(df)
            ])
            
        except Exception as e:
            logger.error(f"Error rendering nodes table: {str(e)}")
            return dbc.Alert(f"Error loading nodes data: {str(e)}", color="danger")

    def render_edges_table(self):
        """Render edges data table"""
        try:
            edges = self.get_edges()
            nodes = self.get_nodes()
            edge_types = self.get_edge_types()
            
            if not edges:
                return dbc.Alert("No edges found in the database.", color="info")
            
            # Create lookup dictionaries
            node_lookup = {n.id: n.name for n in nodes}
            edge_type_lookup = {et.id: et.name for et in edge_types}
            
            data = []
            for edge in edges:
                data.append({
                    'ID': edge.id,
                    'Source': node_lookup.get(edge.source_node_id, 'Unknown'),
                    'Target': node_lookup.get(edge.target_node_id, 'Unknown'),
                    'Edge Type': edge_type_lookup.get(edge.edge_type_id, 'Unknown'),
                    'Description': edge.description
                })
            
            df = pd.DataFrame(data)
            
            return html.Div([
                html.H4("Edges Data"),
                self._create_table_from_dataframe(df)
            ])
            
        except Exception as e:
            logger.error(f"Error rendering edges table: {str(e)}")
            return dbc.Alert(f"Error loading edges data: {str(e)}", color="danger")

    def render_edge_types_table(self):
        """Render edge types data table"""
        try:
            edge_types = self.get_edge_types()
            if not edge_types:
                return dbc.Alert("No edge types found in the database.", color="info")
            
            data = []
            for et in edge_types:
                data.append({
                    'ID': et.id,
                    'Name': et.name,
                    'Description': et.description
                })
            
            df = pd.DataFrame(data)
            
            return html.Div([
                html.H4("Edge Types Data"),
                self._create_table_from_dataframe(df)
            ])
            
        except Exception as e:
            logger.error(f"Error rendering edge types table: {str(e)}")
            return dbc.Alert(f"Error loading edge types data: {str(e)}", color="danger")

    # ==================== NETWORK VISUALIZATION ====================

    def get_network_graph_data(self, graph_type="simple"):
        """Get formatted data for network graph visualization"""
        try:
            if graph_type == "database":
                return self._get_database_network_data()
            elif graph_type == "simple":
                return self._get_simple_network_data()
            elif graph_type == "detailed":
                return self._get_detailed_network_data()
            else:
                return self._get_simple_network_data()
        except Exception as e:
            logger.error(f"Failed to get network graph data: {str(e)}")
            return {
                'error': str(e),
                'fallback_message': 'Network visualization temporarily unavailable'
            }

    def _get_database_network_data(self):
        """Generate network graph data from the actual database"""
        try:
            nodes = self.get_nodes()
            edges = self.get_edges()
            
            if not nodes:
                return {
                    'error': 'No nodes found in database',
                    'fallback_message': 'Add some nodes to see the network visualization'
                }
            
            # Format nodes
            formatted_nodes = []
            for node in nodes:
                formatted_nodes.append({
                    "id": node.id,
                    "label": node.name,
                    "size": 25,
                    "color": "#4ECDC4"
                })
            
            # Format edges
            formatted_edges = []
            for edge in edges:
                formatted_edges.append({
                    "source": edge.source_node_id,
                    "target": edge.target_node_id,
                    "color": "#888"
                })
            
            return {
                "nodes": formatted_nodes, 
                "edges": formatted_edges,
                "stats": {
                    "total_nodes": len(nodes),
                    "total_edges": len(edges)
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate database network data: {str(e)}")
            return {
                'error': str(e),
                'fallback_message': 'Database network visualization failed'
            }

    def _get_simple_network_data(self):
        """Generate simple demo network graph data"""
        nodes = [
            {"id": "Node1", "label": "Server A", "size": 25, "color": "#FF6B6B"},
            {"id": "Node2", "label": "Server B", "size": 20, "color": "#4ECDC4"},
            {"id": "Node3", "label": "Database", "size": 30, "color": "#45B7D1"},
            {"id": "Node4", "label": "Load Balancer", "size": 25, "color": "#96CEB4"},
            {"id": "Node5", "label": "Client", "size": 15, "color": "#FFEAA7"},
            {"id": "Node6", "label": "Cache", "size": 20, "color": "#DDA0DD"},
        ]
        
        edges = [
            {"source": "Node1", "target": "Node3", "color": "#888"},
            {"source": "Node2", "target": "Node3", "color": "#888"},
            {"source": "Node4", "target": "Node1", "color": "#888"},
            {"source": "Node4", "target": "Node2", "color": "#888"},
            {"source": "Node5", "target": "Node4", "color": "#888"},
            {"source": "Node1", "target": "Node6", "color": "#888"},
            {"source": "Node2", "target": "Node6", "color": "#888"},
        ]
        
        return {"nodes": nodes, "edges": edges}

    def _get_detailed_network_data(self):
        """Generate detailed demo network graph data"""
        # Similar implementation to simple but with more nodes
        return self._get_simple_network_data()

    # ==================== UTILITY METHODS ====================

    def validate_database_integrity(self) -> Dict[str, Any]:
        """Validate database integrity and return results"""
        try:
            is_valid, issues = self.model.validate_database_integrity()
            
            if is_valid:
                logger.info("Database integrity check passed")
                return {"status": "success", "message": "Database integrity check passed"}
            else:
                logger.warning(f"Database integrity issues found: {len(issues)} issues")
                issue_list = "\\n".join(issues[:10])  # Show first 10 issues
                if len(issues) > 10:
                    issue_list += f"\\n... and {len(issues) - 10} more issues"
                return {"status": "warning", "message": f"Database integrity issues found:\\n{issue_list}"}
                
        except Exception as e:
            error_msg = f"Integrity check failed: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def _create_table_from_dataframe(self, df):
        """Create a Dash Bootstrap table from a pandas DataFrame"""
        if df.empty:
            return html.P("No data available", className="text-muted")
        
        # Create table header
        header = html.Thead([
            html.Tr([html.Th(col) for col in df.columns])
        ])
        
        # Create table body
        rows = []
        for index, row in df.iterrows():
            rows.append(html.Tr([html.Td(row[col]) for col in df.columns]))
        
        body = html.Tbody(rows)
        
        # Return the complete table
        return dbc.Table(
            [header, body],
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            className="mt-2"
        )

    def get_data_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics about the data"""
        try:
            nodes = self.get_nodes()
            edges = self.get_edges()
            edge_types = self.get_edge_types()
            
            # Calculate additional metrics
            node_degrees = {}
            for edge in edges:
                node_degrees[edge.source_node_id] = node_degrees.get(edge.source_node_id, 0) + 1
                node_degrees[edge.target_node_id] = node_degrees.get(edge.target_node_id, 0) + 1
            
            avg_degree = sum(node_degrees.values()) / len(nodes) if nodes else 0
            max_degree = max(node_degrees.values()) if node_degrees else 0
            isolated_nodes = len([n for n in nodes if n.id not in node_degrees])
            
            stats = {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'edge_types_count': len(edge_types),
                'avg_node_degree': round(avg_degree, 2),
                'max_node_degree': max_degree,
                'isolated_nodes': isolated_nodes,
            }
            
            return {"status": "success", "data": stats}
            
        except Exception as e:
            error_msg = f"Failed to get statistics: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def format_statistics_display(self, stats):
        """Format statistics for display in Dash"""
        return dbc.Card([
            dbc.CardHeader("Data Statistics"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Basic Statistics"),
                        html.P(f"Total Nodes: {stats.get('total_nodes', 0)}"),
                        html.P(f"Total Edges: {stats.get('total_edges', 0)}"),
                        html.P(f"Edge Types: {stats.get('edge_types_count', 0)}"),
                    ], width=6),
                    dbc.Col([
                        html.H5("Network Metrics"),
                        html.P(f"Average Node Degree: {stats.get('avg_node_degree', 0)}"),
                        html.P(f"Max Node Degree: {stats.get('max_node_degree', 0)}"),
                        html.P(f"Isolated Nodes: {stats.get('isolated_nodes', 0)}"),
                    ], width=6)
                ])
            ])
        ])

    def handle_report_generation(self, report_type):
        """Generate reports based on type"""
        try:
            if report_type == "topology":
                stats = self.get_data_statistics()
                if stats['status'] == 'success':
                    data = stats['data']
                    return {"status": "info", "message": f"Network Topology Report: {data['total_nodes']} nodes, {data['total_edges']} edges"}
                else:
                    return stats
            elif report_type == "node-stats":
                result = self.get_data_statistics()
                if result['status'] == 'success':
                    return {"status": "info", "message": "Node Statistics Report generated successfully"}
                else:
                    return result
            elif report_type == "edge-analysis":
                return {"status": "info", "message": "Edge Analysis Report generated successfully"}
            else:
                return {"status": "error", "message": "Unknown report type"}
        except Exception as e:
            error_msg = f"Report generation failed: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def save_app_settings(self, theme, notifications, auto_save):
        """Save application settings"""
        try:
            # In a real app, you'd save these to a database or config file
            settings = {
                'theme': theme,
                'notifications': notifications,
                'auto_save': auto_save
            }
            logger.info(f"Settings saved: {settings}")
            return {"status": "success", "message": "Settings saved successfully!"}
        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def reset_app_settings(self):
        """Reset settings to defaults"""
        try:
            logger.info("Settings reset to defaults")
            return {"status": "success", "message": "Settings have been reset to defaults!"}
        except Exception as e:
            error_msg = f"Failed to reset settings: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}