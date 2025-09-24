#!/usr/bin/env python3

# controllers/controller.py

import datetime
import io
import matplotlib.pyplot as plt
import pandas as pd
import random
import streamlit as st
import uuid
from typing import List, Dict, Any


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self._initialize_session_state()

    def _initialize_session_state(self):
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.data_modified = False
            st.session_state.selected_table = 'nodes'
            st.session_state.current_page = 'Networks'
            st.session_state.app_data = {}

    def initialize_app(self):
        # To-Do : move the initialization to Config
        st.session_state.app_data['app_name'] = 'Tracer'
        st.session_state.app_data['version'] = '1.0.0'
        st.session_state.app_data['initialized_at'] = datetime.datetime.now()

    def run(self):
        try:
            if not st.session_state.get('app_initialized', False):
                self.initialize_app()
                st.session_state.app_initialized = True

            self.view.render_content()
                
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            st.write("Please refresh the Page or if the problem persists contact Support.")
             
    def get_edges(self):
        """Get all edges from the database"""
        try:
            return self.model.get_edges()
        except Exception as e:
            self.view.show_message(f"Failed to get Edges: {str(e)}", "error")
            return []

    def get_nodes(self):
        try:
            return self.model.get_nodes()
        except Exception as e:
            self.view.show_message(f"Failed to get Nodes: {str(e)}", "error")
            return []
        
    def get_edge_types(self):
        """Get all edge types from the database"""
        try:
            return self.model.get_edge_types()
        except Exception as e:
            self.view.show_message(f"Failed to get Edge Types: {str(e)}", "error")
            return []

    def get_data_by_table(self, table_name):
        """Get data based on selected table"""
        if table_name == 'nodes':
            return self.get_nodes()
        elif table_name == 'edges':
            return self.get_edges()
        elif table_name == 'edge_types':
            return self.get_edge_types()
        else:
            return []

    def handle_page_change(self, page):
        if page != st.session_state.get('current_page'):
            st.session_state.current_page = page
            st.rerun()

    def handle_table_selection(self, table_name):
            """Handle table selection change"""
            if table_name != st.session_state.get('selected_table'):
                st.session_state.selected_table = table_name
                st.rerun()

    def export_data(self, table_name, format='csv'):
        """Export data in specified format"""
        try:
            data = self.get_data_by_table(table_name)
            
            if not data:
                self.view.show_message("No data to export", "warning")
                return None
            
            # Convert SQLAlchemy objects to dictionaries
            data_dicts = []
            for item in data:
                if hasattr(item, '__dict__'):
                    # Convert SQLAlchemy object to dict, excluding private attributes
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    data_dicts.append(item_dict)
                else:
                    data_dicts.append(item)
            
            if format == 'csv':
                # Convert to CSV
                df = pd.DataFrame(data_dicts)
                csv_data = df.to_csv(index=False)
                return csv_data
            
            elif format == 'json':
                import json
                return json.dumps(data_dicts, indent=2, default=str)
                
        except Exception as e:
            self.view.show_message(f"Export failed: {str(e)}", "error")
            return None

    def get_app_stats(self):
        """Get application statistics"""
        try:
            stats = {
                'total_nodes': len(self.get_nodes()),
                'total_edges': len(self.get_edges()),
                # 'edge_types_count': len(self.get_edge_types()),
                'app_version': st.session_state.app_data.get('version', '1.0.0'),
                'initialized_at': st.session_state.app_data.get('initialized_at', 'Unknown')
            }
            return stats
        except Exception as e:
            st.error(f"Failed to get stats: {str(e)}")
            return {}

    # ==================== EXISTING METHODS (UNCHANGED) ====================

    def get_dashboard_metrics(self):
        """Get all dashboard metrics in one call"""
        try:
            stats = self.get_app_stats()
            return {
                'total_nodes': stats.get('total_nodes', 0),
                'total_edges': stats.get('total_edges', 0),
                'node_types_count': stats.get('node_types_count', 0),
                'edge_types_count': stats.get('edge_types_count', 0),
                'app_version': stats.get('app_version', '1.0.0'),
                'initialized_at': stats.get('initialized_at', 'Unknown')
            }
        except Exception as e:
            return {'error': str(e)}

    def prepare_edges_for_editor(self):
        """Prepare edges data with lookups for the data editor"""
        try:
            edges = self.get_edges()
            edge_types = self.get_edge_types()
            nodes = self.get_nodes()
            
            if not edges:
                return None, "No Edges found in the Database."
            
            edge_type_lookup = {et.id: et.name for et in edge_types}
            node_lookup = {n.id: n.name for n in nodes}

            edges_data = []
            for edge in edges:
                edges_data.append({
                    'ID': edge.id,
                    'Source ID': edge.source_node_id,
                    'Source': node_lookup.get(edge.source_node_id, 'Unknown'),
                    'Edge Type': edge_type_lookup.get(edge.edge_type_id, 'Unknown'),
                    'Target ID': edge.target_node_id,
                    'Target': node_lookup.get(edge.target_node_id, 'Unknown'),
                    'Description': edge.description
                })
            
            return {
                'data': edges_data,
                'node_options': list(node_lookup.values()),
                'edge_type_options': list(edge_type_lookup.values()),
                'node_id_lookup': {v: k for k, v in node_lookup.items()},
                'edge_type_id_lookup': {v: k for k, v in edge_type_lookup.items()}
            }, None
            
        except Exception as e:
            return None, f"Error loading edges data: {str(e)}"

    def prepare_nodes_for_editor(self):
        """Prepare nodes data for the data editor"""
        try:
            nodes = self.get_nodes()

            if not nodes:
                return None, "No Nodes found in the Database."
            
            nodes_data = []
            for node in nodes:
                nodes_data.append({
                    'ID': node.id,
                    'Name': node.name,
                    'Description': node.description
                })
            
            return {'data': nodes_data}, None
            
        except Exception as e:
            return None, f"Error loading nodes data: {str(e)}"

    def prepare_edge_types_for_editor(self):
        """Prepare edge types data for the data editor"""
        try:
            edge_types = self.get_edge_types()
            
            if not edge_types:
                return None, "No edge types found in the database."
            
            edge_types_data = []
            for et in edge_types:
                edge_types_data.append({
                    'ID': et.id,
                    'Name': et.name,
                    'Description': et.description
                })
            
            return {'data': edge_types_data}, None
            
        except Exception as e:
            return None, f"Error loading edge types data: {str(e)}"

    # ==================== CRUD OPERATIONS ====================

    # -------------------- NODE CRUD --------------------

    def create_node(self, name: str, description: str = 'None') -> Dict[str, Any]:
        """Create a new node"""
        try:
            node_id = str(uuid.uuid4())
            success, message = self.model.create_node(node_id, name, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create node: {str(e)}"}

    def update_node(self, node_id: str, name: str = None, description: str = None) -> Dict[str, Any]:
        """Update an existing node"""
        try:
            success, message = self.model.update_node(node_id, name, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update node: {str(e)}"}

    def delete_node(self, node_id: str) -> Dict[str, Any]:
        """Delete a node"""
        try:
            success, message = self.model.delete_node(node_id)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete node: {str(e)}"}

    def batch_update_nodes(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch update multiple nodes"""
        try:
            success, message = self.model.batch_update_nodes(updates)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Batch update failed: {str(e)}"}

    # -------------------- EDGE CRUD --------------------

    def create_edge(self, source_node_name: str, target_node_name: str, edge_type_name: str, description: str = 'None') -> Dict[str, Any]:
        """Create a new edge"""
        try:
            # Get lookups
            nodes = self.get_nodes()
            edge_types = self.get_edge_types()
            
            node_name_to_id = {n.name: n.id for n in nodes}
            edge_type_name_to_id = {et.name: et.id for et in edge_types}
            
            source_node_id = node_name_to_id.get(source_node_name)
            target_node_id = node_name_to_id.get(target_node_name)
            edge_type_id = edge_type_name_to_id.get(edge_type_name)
            
            if not source_node_id:
                return {"status": "error", "message": f"Source node '{source_node_name}' not found"}
            if not target_node_id:
                return {"status": "error", "message": f"Target node '{target_node_name}' not found"}
            if not edge_type_id:
                return {"status": "error", "message": f"Edge type '{edge_type_name}' not found"}
            
            edge_id = str(uuid.uuid4())
            success, message = self.model.create_edge(edge_id, source_node_id, target_node_id, edge_type_id, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create edge: {str(e)}"}

    def update_edge(self, edge_id: str, source_node_name: str = None, target_node_name: str = None, 
                   edge_type_name: str = None, description: str = None) -> Dict[str, Any]:
        """Update an existing edge"""
        try:
            # Convert names to IDs if provided
            source_node_id = None
            target_node_id = None
            edge_type_id = None
            
            if source_node_name or target_node_name or edge_type_name:
                nodes = self.get_nodes()
                edge_types = self.get_edge_types()
                
                node_name_to_id = {n.name: n.id for n in nodes}
                edge_type_name_to_id = {et.name: et.id for et in edge_types}
                
                if source_node_name:
                    source_node_id = node_name_to_id.get(source_node_name)
                    if not source_node_id:
                        return {"status": "error", "message": f"Source node '{source_node_name}' not found"}
                
                if target_node_name:
                    target_node_id = node_name_to_id.get(target_node_name)
                    if not target_node_id:
                        return {"status": "error", "message": f"Target node '{target_node_name}' not found"}
                
                if edge_type_name:
                    edge_type_id = edge_type_name_to_id.get(edge_type_name)
                    if not edge_type_id:
                        return {"status": "error", "message": f"Edge type '{edge_type_name}' not found"}
            
            success, message = self.model.update_edge(edge_id, source_node_id, target_node_id, edge_type_id, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update edge: {str(e)}"}

    def delete_edge(self, edge_id: str) -> Dict[str, Any]:
        """Delete an edge"""
        try:
            success, message = self.model.delete_edge(edge_id)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete edge: {str(e)}"}

    def batch_update_edges(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch update multiple edges with name-to-ID conversion"""
        try:
            # Get lookups for name-to-ID conversion
            nodes = self.get_nodes()
            edge_types = self.get_edge_types()
            
            node_name_to_id = {n.name: n.id for n in nodes}
            edge_type_name_to_id = {et.name: et.id for et in edge_types}
            
            # Convert updates with names to IDs
            converted_updates = []
            for update in updates:
                converted_update = {'id': update.get('id')}
                
                if 'source' in update:
                    source_id = node_name_to_id.get(update['source'])
                    if source_id:
                        converted_update['source_node_id'] = source_id
                
                if 'target' in update:
                    target_id = node_name_to_id.get(update['target'])
                    if target_id:
                        converted_update['target_node_id'] = target_id
                
                if 'edge_type' in update:
                    edge_type_id = edge_type_name_to_id.get(update['edge_type'])
                    if edge_type_id:
                        converted_update['edge_type_id'] = edge_type_id
                
                if 'description' in update:
                    converted_update['description'] = update['description']
                
                converted_updates.append(converted_update)
            
            success, message = self.model.batch_update_edges(converted_updates)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Batch update failed: {str(e)}"}

    # -------------------- EDGE TYPE CRUD --------------------

    def create_edge_type(self, name: str, description: str = 'None') -> Dict[str, Any]:
        """Create a new edge type"""
        try:
            edge_type_id = str(uuid.uuid4())
            success, message = self.model.create_edge_type(edge_type_id, name, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to create edge type: {str(e)}"}

    def update_edge_type(self, edge_type_id: str, name: str = None, description: str = None) -> Dict[str, Any]:
        """Update an existing edge type"""
        try:
            success, message = self.model.update_edge_type(edge_type_id, name, description)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to update edge type: {str(e)}"}

    def delete_edge_type(self, edge_type_id: str) -> Dict[str, Any]:
        """Delete an edge type"""
        try:
            success, message = self.model.delete_edge_type(edge_type_id)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete edge type: {str(e)}"}

    def batch_update_edge_types(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch update multiple edge types"""
        try:
            success, message = self.model.batch_update_edge_types(updates)
            
            if success:
                st.session_state.data_modified = True
                return {"status": "success", "message": message}
            else:
                return {"status": "error", "message": message}
        except Exception as e:
            return {"status": "error", "message": f"Batch update failed: {str(e)}"}

    # -------------------- DATA EDITOR HANDLERS --------------------

    def handle_nodes_data_changes(self, edited_df: pd.DataFrame, original_data: List[Dict]) -> Dict[str, Any]:
        """Handle changes from the nodes data editor"""
        try:
            # Convert DataFrame to list of dicts
            new_data = edited_df.to_dict('records')
            
            # Find changes by comparing with original data
            updates = []
            for i, new_row in enumerate(new_data):
                if i < len(original_data):
                    original_row = original_data[i]
                    changes = {}
                    
                    if new_row.get('Name') != original_row.get('Name'):
                        changes['name'] = new_row.get('Name')
                    if new_row.get('Description') != original_row.get('Description'):
                        changes['description'] = new_row.get('Description')
                    
                    if changes:
                        changes['id'] = new_row.get('ID')
                        updates.append(changes)
            
            # Handle new rows (added by user)
            new_rows = new_data[len(original_data):]
            for new_row in new_rows:
                if new_row.get('Name'):  # Only create if name is provided
                    result = self.create_node(new_row.get('Name', ''), new_row.get('Description', 'None'))
                    if result['status'] != 'success':
                        return result
            
            # Batch update existing rows
            if updates:
                return self.batch_update_nodes(updates)
            else:
                return {"status": "info", "message": "No changes detected"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to process node changes: {str(e)}"}

    def handle_edges_data_changes(self, edited_df: pd.DataFrame, original_data: List[Dict]) -> Dict[str, Any]:
        """Handle changes from the edges data editor"""
        try:
            # Convert DataFrame to list of dicts
            new_data = edited_df.to_dict('records')
            
            # Find changes by comparing with original data
            updates = []
            for i, new_row in enumerate(new_data):
                if i < len(original_data):
                    original_row = original_data[i]
                    changes = {}
                    
                    if new_row.get('Source') != original_row.get('Source'):
                        changes['source'] = new_row.get('Source')
                    if new_row.get('Target') != original_row.get('Target'):
                        changes['target'] = new_row.get('Target')
                    if new_row.get('Edge Type') != original_row.get('Edge Type'):
                        changes['edge_type'] = new_row.get('Edge Type')
                    if new_row.get('Description') != original_row.get('Description'):
                        changes['description'] = new_row.get('Description')
                    
                    if changes:
                        changes['id'] = new_row.get('ID')
                        updates.append(changes)
            
            # Handle new rows (added by user)
            new_rows = new_data[len(original_data):]
            for new_row in new_rows:
                if new_row.get('Source') and new_row.get('Target') and new_row.get('Edge Type'):
                    result = self.create_edge(
                        new_row.get('Source'),
                        new_row.get('Target'),
                        new_row.get('Edge Type'),
                        new_row.get('Description', 'None')
                    )
                    if result['status'] != 'success':
                        return result
            
            # Batch update existing rows
            if updates:
                return self.batch_update_edges(updates)
            else:
                return {"status": "info", "message": "No changes detected"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to process edge changes: {str(e)}"}

    def handle_edge_types_data_changes(self, edited_df: pd.DataFrame, original_data: List[Dict]) -> Dict[str, Any]:
        """Handle changes from the edge types data editor"""
        try:
            # Convert DataFrame to list of dicts
            new_data = edited_df.to_dict('records')
            
            # Find changes by comparing with original data
            updates = []
            for i, new_row in enumerate(new_data):
                if i < len(original_data):
                    original_row = original_data[i]
                    changes = {}
                    
                    if new_row.get('Name') != original_row.get('Name'):
                        changes['name'] = new_row.get('Name')
                    if new_row.get('Description') != original_row.get('Description'):
                        changes['description'] = new_row.get('Description')
                    
                    if changes:
                        changes['id'] = new_row.get('ID')
                        updates.append(changes)
            
            # Handle new rows (added by user)
            new_rows = new_data[len(original_data):]
            for new_row in new_rows:
                if new_row.get('Name'):  # Only create if name is provided
                    result = self.create_edge_type(new_row.get('Name', ''), new_row.get('Description', 'None'))
                    if result['status'] != 'success':
                        return result
            
            # Batch update existing rows
            if updates:
                return self.batch_update_edge_types(updates)
            else:
                return {"status": "info", "message": "No changes detected"}
                
        except Exception as e:
            return {"status": "error", "message": f"Failed to process edge type changes: {str(e)}"}

    # -------------------- UTILITY METHODS --------------------

    def validate_database_integrity(self) -> Dict[str, Any]:
        """Validate database integrity and return results"""
        try:
            is_valid, issues = self.model.validate_database_integrity()
            
            if is_valid:
                return {"status": "success", "message": "Database integrity check passed"}
            else:
                issue_list = "\n".join(issues[:10])  # Show first 10 issues
                if len(issues) > 10:
                    issue_list += f"\n... and {len(issues) - 10} more issues"
                return {"status": "warning", "message": f"Database integrity issues found:\n{issue_list}"}
                
        except Exception as e:
            return {"status": "error", "message": f"Integrity check failed: {str(e)}"}

    def get_data_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics about the data"""
        try:
            stats = self.get_app_stats()
            
            # Add more detailed stats
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
            
            stats.update({
                'avg_node_degree': round(avg_degree, 2),
                'max_node_degree': max_degree,
                'isolated_nodes': len([n for n in nodes if n.id not in node_degrees]),
                'edge_type_distribution': {et.name: len([e for e in edges if e.edge_type_id == et.id]) for et in edge_types}
            })
            
            return {"status": "success", "data": stats}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get statistics: {str(e)}"}

    # ==================== EXISTING METHODS (UNCHANGED) ====================

    def get_network_graph_data(self, graph_type="simple"):
        """Get formatted data for network graph visualization"""
        try:
            if graph_type == "simple":
                return self._get_simple_network_data()
            elif graph_type == "detailed":
                return self._get_detailed_network_data()
            else:
                return self._get_simple_network_data()
        except Exception as e:
            return {
                'error': str(e),
                'fallback_message': 'Network visualization temporarily unavailable'
            }

    def _get_simple_network_data(self):
        """Generate simple network graph data"""
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
        
        config = {
            "width": 700, "height": 400, "directed": True,
            "physics": True, "hierarchical": False,
            "nodeHighlightBehavior": True, "highlightColor": "#F7A7A6",
            "collapsible": False
        }
        
        return {"nodes": nodes, "edges": edges, "config": config}

    def _get_detailed_network_data(self):
        """Generate detailed network graph data"""
        nodes = [
            {"id": "Core1", "label": "Core Router 1", "size": 35, "color": "#FF6B6B"},
            {"id": "Core2", "label": "Core Router 2", "size": 35, "color": "#FF6B6B"},
            {"id": "Dist1", "label": "Distribution 1", "size": 25, "color": "#4ECDC4"},
            {"id": "Dist2", "label": "Distribution 2", "size": 25, "color": "#4ECDC4"},
            {"id": "Dist3", "label": "Distribution 3", "size": 25, "color": "#4ECDC4"},
            {"id": "Access1", "label": "Access Switch 1", "size": 20, "color": "#45B7D1"},
            {"id": "Access2", "label": "Access Switch 2", "size": 20, "color": "#45B7D1"},
            {"id": "Access3", "label": "Access Switch 3", "size": 20, "color": "#45B7D1"},
            {"id": "Access4", "label": "Access Switch 4", "size": 20, "color": "#45B7D1"},
            {"id": "Server1", "label": "Web Server", "size": 15, "color": "#96CEB4"},
            {"id": "Server2", "label": "App Server", "size": 15, "color": "#96CEB4"},
            {"id": "DB1", "label": "Database", "size": 30, "color": "#FFEAA7"},
            {"id": "FW1", "label": "Firewall", "size": 25, "color": "#DDA0DD"},
        ]
        
        edges = [
            {"source": "Core1", "target": "Core2", "color": "#FF0000", "width": 3},
            {"source": "Core1", "target": "Dist1", "color": "#888"},
            {"source": "Core1", "target": "Dist2", "color": "#888"},
            {"source": "Core2", "target": "Dist2", "color": "#888"},
            {"source": "Core2", "target": "Dist3", "color": "#888"},
            {"source": "Dist1", "target": "Access1", "color": "#888"},
            {"source": "Dist1", "target": "Access2", "color": "#888"},
            {"source": "Dist2", "target": "Access2", "color": "#888"},
            {"source": "Dist2", "target": "Access3", "color": "#888"},
            {"source": "Dist3", "target": "Access3", "color": "#888"},
            {"source": "Dist3", "target": "Access4", "color": "#888"},
            {"source": "Access1", "target": "Server1", "color": "#888"},
            {"source": "Access2", "target": "Server2", "color": "#888"},
            {"source": "Access3", "target": "DB1", "color": "#888"},
            {"source": "FW1", "target": "Core1", "color": "Purple", "width": 2},
            {"source": "Dist1", "target": "Dist2", "color": "#888", "style": "dashed"},
            {"source": "Access1", "target": "Access3", "color": "#888", "style": "dashed"},
        ]
        
        config = {
            "width": 800, "height": 500, "directed": False,
            "physics": True, "hierarchical": True,
            "nodeHighlightBehavior": True, "highlightColor": "#F7A7A6",
            "collapsible": False
        }
        
        return {
            "nodes": nodes, "edges": edges, "config": config,
            "stats": {"total_nodes": len(nodes), "total_connections": len(edges), "network_layers": 3}
        }

    def get_network_metrics(self):
        """Get network health and connection metrics"""
        return {
            "total_networks": 5,
            "active_connections": 127,
            "network_health": "98%"
        }

    def get_available_reports(self):
        """Get list of available report types"""
        return ["Select a Report...", "Progressive Assurance Case Report", "Safety Case"]

    def generate_report(self, report_type):
        """Generate reports based on type"""
        try:
            if report_type == "Select a Report...":
                return {"status": "none", "message": ""}
            elif report_type == "Progressive Assurance Case Report":
                return {"status": "info", "message": "Generating Progressive Assurance Case Report..."}
            elif report_type == "Safety Case":
                return {"status": "info", "message": "Generating Safety Case..."}
            else:
                return {"status": "error", "message": "Unknown report type"}
        except Exception as e:
            return {"status": "error", "message": f"Report generation failed: {str(e)}"}

    def get_app_settings(self):
        """Get current application settings"""
        return st.session_state.get('app_settings', {
            'theme': 'Light',
            'notifications': True,
            'auto_save': True
        })

    def save_app_settings(self, theme, notifications, auto_save):
        """Save application settings"""
        try:
            st.session_state.app_settings = {
                'theme': theme,
                'notifications': notifications,
                'auto_save': auto_save
            }
            return {"status": "success", "message": "Settings saved Successfully!"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to save settings: {str(e)}"}

    def reset_app_settings(self):
        """Reset settings to defaults"""
        try:
            default_settings = {
                'theme': 'Light',
                'notifications': True,
                'auto_save': True
            }
            st.session_state.app_settings = default_settings
            return {"status": "warning", "message": "Settings have been reset to Defaults!"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to reset settings: {str(e)}"}

    def handle_network_action(self, action_type):
        """Handle network management actions"""
        try:
            if action_type == "create":
                return {"status": "success", "message": "New network creation started!"}
            elif action_type == "analyze":
                return {"status": "info", "message": "Network analysis in progress..."}
            elif action_type == "export":
                return {"status": "success", "message": "Network data exported!"}
            else:
                return {"status": "error", "message": "Unknown action type"}
        except Exception as e:
            return {"status": "error", "message": f"Action failed: {str(e)}"}

    def get_graph_data_for_visualization(self):
        try:
            nodes = self.get_nodes()
            edges = self.get_edges()
            edge_types = self.get_edge_types()
            
            # Create lookup dictionaries
            # node_type_lookup = {nt.id: nt.name for nt in node_types}
            edge_type_lookup = {et.id: et.name for et in edge_types}
            
            # Format nodes for visualization
            formatted_nodes = []
            for node in nodes:
                formatted_nodes.append({
                    'id': node.id,
                    'name': node.name,
                    'description': node.description
                })
            
            # Format edges for visualization
            formatted_edges = []
            for edge in edges:
                formatted_edges.append({
                    'id': edge.id,
                    'source': edge.source,
                    'target': edge.target,
                    'type': edge_type_lookup.get(edge.edge_type_id, 'Unknown'),
                    'description': edge.description
                })
            
            return {
                'nodes': formatted_nodes,
                'edges': formatted_edges,
                'edge_types': [{'id': et.id, 'name': et.name} for et in edge_types]
            }
            
        except Exception as e:
            self.view.show_message(f"Failed to get graph data: {str(e)}", "error")
            return {'nodes': [], 'edges': [], 'edge_types': []}

    def reset_app_state(self):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Reinitialize
        self._initialize_session_state()
        self.initialize_app()
        
        self.view.show_message("Successfully reset Application State", "success")