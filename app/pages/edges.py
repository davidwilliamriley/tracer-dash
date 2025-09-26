# pages/edges.py

# imports
import dash
from dash import html, dcc, callback, Input, Output, no_update, State
import dash_bootstrap_components as dbc
import dash_tabulator
import json
import logging
import pandas as pd
import uuid
from datetime import datetime
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)

# Import the model to access the Database
from models.model import Model

dash.register_page(__name__, path='/edges')

# Initialize the model to access the Database
model = Model()

def get_edges_from_db() -> List[Dict[str, Any]]:
    """Get Edges from the Database with display names for the table"""
    try:
        # Get raw data with UUIDs
        raw_edges = model.get_edges_for_editor()
        
        # Get lookup data
        nodes_for_dropdown = get_nodes_for_dropdown()
        edge_types_for_dropdown = get_edge_types_for_dropdown()
        
        # Create lookup dictionaries
        node_uuid_to_label = {str(node['value']): str(node['label']) for node in nodes_for_dropdown}
        edge_type_uuid_to_label = {str(et['value']): str(et['label']) for et in edge_types_for_dropdown}
        
        # Transform the data for display
        display_edges = []
        for edge in raw_edges:
            source_uuid = edge['Source']
            target_uuid = edge['Target']
            edge_type_uuid = edge['Edge Type']
            
            display_edge = {
                'ID': edge['ID'],
                'Identifier': edge['Identifier'],
                'Source': node_uuid_to_label.get(source_uuid, source_uuid),        # Display name
                'Target': node_uuid_to_label.get(target_uuid, target_uuid),        # Display name
                'Edge Type': edge_type_uuid_to_label.get(edge_type_uuid, edge_type_uuid),  # Display name
                'Description': edge['Description'],
                # Store UUIDs in hidden fields for database operations
                'Source_UUID': source_uuid,
                'Target_UUID': target_uuid,
                'Edge_Type_UUID': edge_type_uuid
            }
            
            display_edges.append(display_edge)
        
        print(f"DEBUG: Transformed edge sample: {display_edges[0] if display_edges else 'None'}")
        return display_edges
        
    except Exception as e:
        print(f"Error getting edges from database: {e}")
        return []

def get_nodes_for_dropdown() -> List[Dict[str, str]]:
    """Get Nodes for the Dropdowns"""
    try:
        nodes = model.get_nodes()
        result = []
        for node in nodes:
            if node.identifier is not None and str(node.identifier).strip() != '':
                label = f"{str(node.identifier)} - {str(node.name)}"
            else:
                label = f"{str(node.name)}"      
            result.append({'label': label, 'value': str(node.id)})
        result.sort(key=lambda item: item['label'].lower())
        return result
    except Exception as e:
        print(f"Unable to get Nodes for dropdown: {e}")
        return []

def get_edge_types_for_dropdown() -> List[Dict[str, str]]:
    """Get Edge Types for Dropdowns"""
    try:
        edge_types = model.get_edge_types()
        result = []
        for edge_type in edge_types:
            if edge_type.identifier is not None and str(edge_type.identifier).strip() != '':
                label = f"{str(edge_type.identifier)} - {str(edge_type.name)}"
            else:
                label = f"{str(edge_type.name)}"
            result.append({'label': label, 'value': str(edge_type.id)})

        result.sort(key=lambda item: item['label'].lower())
        return result
    except Exception as e:
        print(f"Unable to get Edge Types for Dropdowns: {e}")
        return []

def layout():
    current_edges = get_edges_from_db()
    nodes_for_dropdown = get_nodes_for_dropdown()
    edge_types_for_dropdown = get_edge_types_for_dropdown()

    node_label_to_uuid = {str(node['label']): str(node['value']) for node in nodes_for_dropdown}
    edge_type_label_to_uuid = {str(et['label']): str(et['value']) for et in edge_types_for_dropdown}
    
    # For dropdown display: Label -> Label (what user sees in dropdown)
    node_label_to_label = {str(node['label']): str(node['label']) for node in nodes_for_dropdown}
    edge_type_label_to_label = {str(et['label']): str(et['label']) for et in edge_types_for_dropdown}

    print(f"DEBUG: Node label to UUID mapping sample: {list(node_label_to_uuid.items())[:3]}")

    return html.Div([
        # Toast Notifications
        dbc.Toast(
            id="toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000, 
            style={"position": "fixed", "bottom": 20, "left": 20, "width": 350, "z-index": 9999}
        ),
        
        # Main container
        html.Div([
            # Toolbar
            html.Div([
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-plus-lg me-2"), "Create"], 
                                 id="create-edge-btn", color="primary", className="me-2", 
                                 title="Create a new Edge"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"], 
                                 id="refresh-edges-btn", color="primary", className="me-2", 
                                 title="Refresh the Edges Table"),
                        dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                                 id="delete-edge-btn", color="warning", 
                                 title="Delete a selected Edge", disabled=True),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                                 id="print-edges-btn", color="primary", className="me-2", 
                                 title="Print the Table to PDF"),
                        dbc.Button([html.I(className="bi bi-download me-2"), "Download"], 
                                 id="download-edges-btn", color="primary", 
                                 title="Download the Table as CSV"),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 edges-toolbar"),
            
            html.Div([
                dash_tabulator.DashTabulator(
                    id='edges-table',
                    theme='tabulator', 
                    data=current_edges,
                    columns=[
                        {"title": "ID", "field": "ID", "headerFilter": False, "visible": False},
                        {"title": "Identifier", "field": "Identifier", "headerFilter": True, "editor": "input"},
                        {"title": "Source_UUID", "field": "Source_UUID", "headerFilter": False, "visible": False},
                        {
                            "title": "Source", 
                            "field": "Source",  # Contains display names now
                            "headerFilter": True,
                            "editor": "select",
                            "editorParams": {"values": node_label_to_label}  # Label -> Label for dropdown display
                        },
                        {"title": "Edge_Type_UUID", "field": "Edge_Type_UUID", "headerFilter": False, "visible": False},
                        {
                            "title": "Edge Type", 
                            "field": "Edge Type",  # Contains display names now
                            "headerFilter": True,
                            "editor": "select", 
                            "editorParams": {"values": edge_type_label_to_label}  # Label -> Label for dropdown display
                        },
                        {"title": "Target_UUID", "field": "Target_UUID", "headerFilter": False, "visible": False}, 
                        {
                            "title": "Target", 
                            "field": "Target",  # Contains display names now
                            "headerFilter": True,
                            "editor": "select",
                            "editorParams": {"values": node_label_to_label}  # Label -> Label for dropdown display
                        },
                        {"title": "Description", "field": "Description", "headerFilter": True, "editor": "input"}
                    ],
                        options={
                            "selectable": True,
                            "selectableRangeMode": "click",
                            "editTriggerEvent": "click", 
                            "pagination": "local",
                            "paginationSize": 10,
                            "paginationSizeSelector": [5, 10, 20, 50],
                            "paginationButtonCount": 5,
                            "paginationCounter": "rows",
                            "movableColumns": True,
                            "resizableColumns": True,
                            "layout": "fitDataStretch",
                            "responsiveLayout": "hide",
                            "tooltips": True,
                            "clipboard": True,
                            "printAsHtml": True,
                            "printHeader": "Edges Table",
                        }
                    )
                ]),
            
        ], className="container-fluid px-4 py-5"),
        
        # Create Edge Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create New Edge")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Identifier:", className="fw-bold"),
                        dbc.Input(
                            id="new-edge-identifier", 
                            type="text", 
                            placeholder="Enter unique identifier (optional)"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Source Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-source",
                            placeholder="Select source node*",
                            clearable=False
                        )
                    ], width=6, className="mb-3"),
                    dbc.Col([
                        dbc.Label("Target Node:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-target",
                            placeholder="Select target node*",
                            clearable=False
                        )
                    ], width=6, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Edge Type:", className="fw-bold"),
                        dcc.Dropdown(
                            id="new-edge-type",
                            placeholder="Select edge type*",
                            clearable=False
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-edge-description", 
                            placeholder="Enter description (optional)",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Create Edge", id="confirm-create-edge", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-create-edge", color="secondary")
            ])
        ], id="create-edge-modal", is_open=False, backdrop="static", size="lg"),
        
        # Delete Confirmation Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button("Delete", id="confirm-delete-edge", color="danger", className="me-2"),
                dbc.Button("Cancel", id="cancel-delete-edge", color="secondary")
            ])
        ], id="delete-edge-modal", is_open=False, backdrop="static"),
        
        # Hidden download component
        dcc.Download(id="download-edges-csv")
    ])

# Populate dropdown options when modal opens
@callback(
    [Output('new-edge-source', 'options'),
     Output('new-edge-target', 'options'),
     Output('new-edge-type', 'options')],
    Input('create-edge-modal', 'is_open')
)
def populate_dropdown_options(is_open):
    """Populate dropdown options when create modal opens"""
    if is_open:
        nodes = get_nodes_for_dropdown()
        edge_types = get_edge_types_for_dropdown()
        return nodes, nodes, edge_types
    return [], [], []

# Enable/disable delete button based on selection
@callback(
    Output('delete-edge-btn', 'disabled'),
    Input('edges-table', 'multiRowsClicked')
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    print(f"DEBUG: toggle_delete_button called with selected_rows: {selected_rows}")
    if selected_rows is None:
        return True
    return len(selected_rows) == 0

# The problem is that multiRowsClicked returns formatted data, but we need raw data.
# We need to get the raw data from the table's current data state instead.

# Update your delete modal callback:
@callback(
    Output('delete-edge-modal', 'is_open'),
    Output('delete-modal-body', 'children', allow_duplicate=True),
    [Input('delete-edge-btn', 'n_clicks'),
     Input('confirm-delete-edge', 'n_clicks'),
     Input('cancel-delete-edge', 'n_clicks')],
    [State('delete-edge-modal', 'is_open'),
     State('edges-table', 'multiRowsClicked'),
     State('edges-table', 'data')],  # Get the raw data from table state
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, raw_table_data):
    """Toggle delete confirmation modal using raw data"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-edge-btn' and selected_rows:
        print(f"DEBUG: Selected rows (formatted): {selected_rows[:2]}...")  # Show first 2 for debugging
        print(f"DEBUG: Raw table data sample: {raw_table_data[:2] if raw_table_data else 'None'}...")
        
        # Get the IDs from selected rows (these should still be correct)
        selected_ids = [row.get('ID') for row in selected_rows if 'ID' in row]
        print(f"DEBUG: Selected IDs: {selected_ids}")
        
        # Find the corresponding raw data rows using the IDs
        raw_selected_rows = []
        for selected_id in selected_ids:
            raw_row = next((row for row in raw_table_data if row.get('ID') == selected_id), None)
            if raw_row:
                raw_selected_rows.append(raw_row)
        
        print(f"DEBUG: Raw selected rows: {raw_selected_rows[:2]}...")
        
        # Create display names for the confirmation using the formatted data (for user readability)
        # but store the raw data for deletion
        selected_edges = []
        for formatted_row in selected_rows:
            display_name = f"{formatted_row.get('Source', 'Unknown')} → {formatted_row.get('Target', 'Unknown')} ({formatted_row.get('Edge Type', 'Unknown')})"
            selected_edges.append(display_name)
        
        body = html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_rows)} edge(s)?"),
            html.Ul([html.Li(name) for name in selected_edges]),
            html.P("This action cannot be undone.", className="text-danger fw-bold"),
            # Store the raw selected rows data in a hidden div
            html.Div(id="raw-selected-data", children=json.dumps(raw_selected_rows), style={"display": "none"})
        ])
        return True, body
    elif button_id in ['confirm-delete-edge', 'cancel-delete-edge']:
        return False, ""
    
    return is_open, ""

# Update your manage_edges callback to use the raw data:
@callback(
    [Output('edges-table', 'data'),
     Output('toast-message', 'is_open', allow_duplicate=True),
     Output('toast-message', 'children', allow_duplicate=True),
     Output('toast-message', 'icon', allow_duplicate=True),
     Output('new-edge-identifier', 'value'),
     Output('new-edge-source', 'value'),
     Output('new-edge-target', 'value'),
     Output('new-edge-type', 'value'),
     Output('new-edge-description', 'value')],
    [Input('confirm-create-edge', 'n_clicks'),
     Input('confirm-delete-edge', 'n_clicks')],
    [State('new-edge-identifier', 'value'),
     State('new-edge-source', 'value'),
     State('new-edge-target', 'value'),
     State('new-edge-type', 'value'),
     State('new-edge-description', 'value'),
     State('edges-table', 'data'),
     State('delete-modal-body', 'children')],  # Get the modal body which contains raw data
    prevent_initial_call=True
)
def manage_edges(create_clicks, delete_clicks, identifier, source_id, target_id, edge_type_id, 
                description, data, modal_body_children):
    """Handle create and delete operations using raw data"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new edge (unchanged)
    if button_id == 'confirm-create-edge' and source_id and target_id and edge_type_id:
        new_edge_id = str(uuid.uuid4())
        success, message = model.create_edge(
            edge_id=new_edge_id,
            identifier=identifier or '',
            source_node_id=source_id,
            target_node_id=target_id,
            edge_type_id=edge_type_id,
            description=description or ''
        )
        
        if success:
            updated_data = get_edges_from_db()
            return updated_data, True, message, "success", '', None, None, None, ''
        else:
            return data, True, f"Failed to create edge: {message}", "danger", no_update, no_update, no_update, no_update, no_update
    
    # Delete selected edges using raw data
    elif button_id == 'confirm-delete-edge' and modal_body_children:
        try:
            # Extract the raw selected data from the hidden div in modal body
            raw_selected_rows = []
            
            # modal_body_children is a list/dict structure, find the hidden div
            def find_raw_data(children):
                if isinstance(children, dict) and children.get('props', {}).get('id') == 'raw-selected-data':
                    return json.loads(children['props']['children'])
                elif isinstance(children, dict) and 'children' in children.get('props', {}):
                    child_list = children['props']['children']
                    if isinstance(child_list, list):
                        for child in child_list:
                            result = find_raw_data(child)
                            if result:
                                return result
                elif isinstance(children, list):
                    for child in children:
                        result = find_raw_data(child)
                        if result:
                            return result
                return None
            
            raw_selected_rows = find_raw_data(modal_body_children)
            print(f"DEBUG: Extracted raw data for deletion: {raw_selected_rows}")
            
            if not raw_selected_rows:
                return data, True, "Error: Could not find raw data for deletion", "danger", no_update, no_update, no_update, no_update, no_update
            
            deleted_count = 0
            errors = []
            
            for raw_row in raw_selected_rows:
                edge_id = raw_row.get('ID')
                if edge_id:
                    print(f"DEBUG: Deleting edge with ID: {edge_id}")
                    success, message = model.delete_edge(edge_id)
                    if success:
                        deleted_count += 1
                    else:
                        errors.append(f"Failed to delete edge: {message}")
                else:
                    errors.append("Edge missing ID")
            
            updated_data = get_edges_from_db()
            
            if errors:
                message = f"Deleted {deleted_count} edges. Errors: {'; '.join(errors[:3])}" + (f" and {len(errors)-3} more..." if len(errors) > 3 else "")
                return updated_data, True, message, "warning", no_update, no_update, no_update, no_update, no_update
            else:
                message = f"Successfully deleted {deleted_count} edge(s)"
                return updated_data, True, message, "success", no_update, no_update, no_update, no_update, no_update
                
        except Exception as e:
            print(f"ERROR: Exception in delete operation: {e}")
            return data, True, f"Error during deletion: {str(e)}", "danger", no_update, no_update, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

@callback(
    [
        Output('edges-table', 'data', allow_duplicate=True),
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('edges-table', 'dataChanged'),
    State('edges-table', 'data'),
    prevent_initial_call=True
)
def handle_data_change(changed_data, current_data):
    """Handle table data changes using hidden UUID fields and display name conversion"""
    if not changed_data:
        return no_update, no_update, no_update, no_update
    
    print(f"DEBUG: Data changed with display names: {changed_data[0] if changed_data else 'None'}")
    
    try:
        # Get fresh lookup data for converting display names back to UUIDs
        nodes_for_dropdown = get_nodes_for_dropdown()
        edge_types_for_dropdown = get_edge_types_for_dropdown()
        
        node_label_to_uuid = {str(node['label']): str(node['value']) for node in nodes_for_dropdown}
        edge_type_label_to_uuid = {str(et['label']): str(et['value']) for et in edge_types_for_dropdown}
        
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                edge_id = row['ID']
                updates = {}
                
                if 'Identifier' in row:
                    updates['identifier'] = row['Identifier'] or ''
                
                # For Source, Target, Edge Type: convert display names to UUIDs
                if 'Source' in row:
                    source_display = row['Source']
                    source_uuid = node_label_to_uuid.get(source_display)
                    if source_uuid:
                        updates['source_node_id'] = source_uuid
                        print(f"DEBUG: Converted Source '{source_display}' -> UUID '{source_uuid}'")
                    else:
                        # Fallback: check if there's a hidden UUID field
                        if 'Source_UUID' in row and row['Source_UUID']:
                            updates['source_node_id'] = row['Source_UUID']
                            print(f"DEBUG: Using Source UUID from hidden field: '{row['Source_UUID']}'")
                        else:
                            errors.append(f"Could not find UUID for Source: {source_display}")
                            continue
                
                if 'Target' in row:
                    target_display = row['Target']
                    target_uuid = node_label_to_uuid.get(target_display)
                    if target_uuid:
                        updates['target_node_id'] = target_uuid
                        print(f"DEBUG: Converted Target '{target_display}' -> UUID '{target_uuid}'")
                    else:
                        if 'Target_UUID' in row and row['Target_UUID']:
                            updates['target_node_id'] = row['Target_UUID']
                            print(f"DEBUG: Using Target UUID from hidden field: '{row['Target_UUID']}'")
                        else:
                            errors.append(f"Could not find UUID for Target: {target_display}")
                            continue
                
                if 'Edge Type' in row:
                    edge_type_display = row['Edge Type']
                    edge_type_uuid = edge_type_label_to_uuid.get(edge_type_display)
                    if edge_type_uuid:
                        updates['edge_type_id'] = edge_type_uuid
                        print(f"DEBUG: Converted Edge Type '{edge_type_display}' -> UUID '{edge_type_uuid}'")
                    else:
                        if 'Edge_Type_UUID' in row and row['Edge_Type_UUID']:
                            updates['edge_type_id'] = row['Edge_Type_UUID']
                            print(f"DEBUG: Using Edge Type UUID from hidden field: '{row['Edge_Type_UUID']}'")
                        else:
                            errors.append(f"Could not find UUID for Edge Type: {edge_type_display}")
                            continue
                
                if 'Description' in row:
                    updates['description'] = row['Description'] or ''
                
                if updates:
                    print(f"DEBUG: Updating edge {edge_id} with: {updates}")
                    success, message = model.update_edge(edge_id, **updates)
                    if success:
                        updated_count += 1
                    else:
                        errors.append(f"Failed to update edge {edge_id}: {message}")
        
        # Get fresh data from database (this will have new display names)
        updated_data = get_edges_from_db()
        
        if errors:
            message = f"Updated {updated_count} edges. Errors: {'; '.join(errors[:2])}"
            return updated_data, True, message, "warning"
        else:
            message = f"Successfully saved changes to {updated_count} edge(s)"
            return updated_data, True, message, "success"
            
    except Exception as e:
        print(f"ERROR: Exception in handle_data_change: {e}")
        message = f"Error saving changes: {str(e)}"
        return no_update, True, message, "danger"
    
# # Toggle create modal
@callback(
    Output('create-edge-modal', 'is_open'),
    [Input('create-edge-btn', 'n_clicks'),
     Input('confirm-create-edge', 'n_clicks'),
     Input('cancel-create-edge', 'n_clicks')],
    State('create-edge-modal', 'is_open')
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Toggle create edge modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open

# # Toggle delete modal
# @callback(
#     Output('delete-edge-modal', 'is_open'),
#     Output('delete-modal-body', 'children', allow_duplicate=True),
#     [Input('delete-edge-btn', 'n_clicks'),
#      Input('confirm-delete-edge', 'n_clicks'),
#      Input('cancel-delete-edge', 'n_clicks')],
#     [State('delete-edge-modal', 'is_open'),
#      State('edges-table', 'multiRowsClicked'),
#      State('edges-table', 'data')],
#     prevent_initial_call=True
# )
# def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, data):
#     """Toggle delete confirmation modal"""
#     ctx = dash.callback_context
    
#     if not ctx.triggered:
#         return False, ""
    
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
#     if button_id == 'delete-edge-btn' and selected_rows:
#         selected_edges = [f"{row['Source']} → {row['Target']} ({row['Edge Type']})" for row in selected_rows]
#         body = html.Div([
#             html.P(f"Are you sure you want to delete the following {len(selected_rows)} edge(s)?"),
#             html.Ul([html.Li(name) for name in selected_edges]),
#             html.P("This action cannot be undone.", className="text-danger fw-bold")
#         ])
#         return True, body
#     elif button_id in ['confirm-delete-edge', 'cancel-delete-edge']:
#         return False, ""
    
#     return is_open, ""

# # Handle CRUD operations
# @callback(
#     [Output('edges-table', 'data'),
#      Output('toast-message', 'is_open', allow_duplicate=True),
#      Output('toast-message', 'children', allow_duplicate=True),
#      Output('toast-message', 'icon', allow_duplicate=True),
#      Output('new-edge-identifier', 'value'),
#      Output('new-edge-source', 'value'),
#      Output('new-edge-target', 'value'),
#      Output('new-edge-type', 'value'),
#      Output('new-edge-description', 'value')],
#     [Input('confirm-create-edge', 'n_clicks'),
#      Input('confirm-delete-edge', 'n_clicks')],
#     [State('new-edge-identifier', 'value'),
#      State('new-edge-source', 'value'),
#      State('new-edge-target', 'value'),
#      State('new-edge-type', 'value'),
#      State('new-edge-description', 'value'),
#      State('edges-table', 'data'),
#      State('edges-table', 'multiRowsClicked')],
#     prevent_initial_call=True
# )
# def manage_edges(create_clicks, delete_clicks, identifier, source_id, target_id, edge_type_id, 
#                 description, data, selected_rows):
#     """Handle create and delete operations"""
#     ctx = dash.callback_context
    
#     if not ctx.triggered:
#         return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
#     # Create new edge
#     if button_id == 'confirm-create-edge' and source_id and target_id and edge_type_id:
#         # Use database to create edge
#         new_edge_id = str(uuid.uuid4())
#         success, message = model.create_edge(
#             edge_id=new_edge_id,
#             identifier=identifier or '',
#             source_node_id=source_id,
#             target_node_id=target_id,
#             edge_type_id=edge_type_id,
#             description=description or ''
#         )
        
#         if success:
#             # Get updated data from database
#             updated_data = get_edges_from_db()
#             return updated_data, True, message, "success", '', None, None, None, ''
#         else:
#             return data, True, f"Failed to create edge: {message}", "danger", no_update, no_update, no_update, no_update, no_update
    
#     # Delete selected edges
#     elif button_id == 'confirm-delete-edge' and selected_rows:
#         deleted_count = 0
#         errors = []
        
#         for row in selected_rows:
#             edge_id = row['ID']
#             success, message = model.delete_edge(edge_id)
#             if success:
#                 deleted_count += 1
#             else:
#                 errors.append(f"Failed to delete edge: {message}")
        
#         # Get updated data from database
#         updated_data = get_edges_from_db()
        
#         if errors:
#             message = f"Deleted {deleted_count} edges. Errors: {'; '.join(errors[:3])}" + (f" and {len(errors)-3} more..." if len(errors) > 3 else "")
#             return updated_data, True, message, "warning", no_update, no_update, no_update, no_update, no_update
#         else:
#             message = f"Successfully deleted {deleted_count} edge(s)"
#             return updated_data, True, message, "success", no_update, no_update, no_update, no_update, no_update
    
#     return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

# Download the Table as CSV
@callback(
    Output('download-edges-csv', 'data'),
    Input('download-edges-btn', 'n_clicks'),
    State('edges-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Download edges data as CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)
        return dict(
            content=csv_string,
            filename=f"edges_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

# Add the Print Functionality
@callback(
    [
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('print-edges-btn', 'n_clicks'),
    prevent_initial_call=True
)
def print_table(n_clicks):
    """Handle print functionality"""
    if n_clicks:
        message = "Print functionality would open a print dialog or generate a PDF report."
        return True, message, "info"
    return no_update, no_update, no_update

# Add the Refresh Functionality
@callback(
    [
        Output('edges-table', 'data', allow_duplicate=True),
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('refresh-edges-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table(n_clicks):
    """Handle refresh functionality - reload from database"""
    if n_clicks:
        try:
            refreshed_data = get_edges_from_db()
            message = f"Table refreshed successfully - loaded {len(refreshed_data)} edges"
            return refreshed_data, True, message, "info"
        except Exception as e:
            message = f"Error refreshing data: {str(e)}"
            return no_update, True, message, "danger"
    return no_update, no_update, no_update, no_update