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
    """Get Edges from the Database"""

    # To-Do : Sort Edges by Source, then Target Identifier and Name
    
    try:
        return model.get_edges_for_table()
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
    logging.info(f"Nodes for dropdown: {nodes_for_dropdown}")

    nodes_data = model.get_nodes_for_table()  # Get dictionaries
    node_values = {}
    for node in nodes_for_dropdown:
        # Find matching node data using dictionary access
        node_data = next((n for n in nodes_data if str(n['ID']) == node['value']), None)
        if node_data:
            displayed_name = str(node_data['Name'])  # Dictionary access
            dropdown_label = node['label']  
            node_values[displayed_name] = dropdown_label

    logging.info(f"Node Values for dropdown: {node_values}")

    edge_types_for_dropdown = get_edge_types_for_dropdown()
    logging.info(f"Edge Types for dropdown: {edge_types_for_dropdown}")

    # Same fix for edge types
    edge_types_data = model.get_edge_types_for_table()  # Get dictionaries
    edge_type_values = {}
    for et in edge_types_for_dropdown:
        # Find matching edge type data using dictionary access
        et_data = next((e for e in edge_types_data if str(e['ID']) == et['value']), None)
        if et_data:
            displayed_name = str(et_data['Name'])  # Dictionary access
            dropdown_label = et['label']       
            edge_type_values[displayed_name] = dropdown_label

    logging.info(f"Edge Type values for dropdown: {edge_type_values}")
    
    node_editor_values = {str(node['value']): str(node['label']) for node in nodes_for_dropdown}
    edge_type_editor_values = {str(et['value']): str(et['label']) for et in edge_types_for_dropdown}

    print("DEBUG - Node editor values (display -> UUID):")
    for k, v in list(node_editor_values.items())[:3]:
        print(f"  '{k}': '{v}'")

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
                        {
                            "title": "Source", 
                            "field": "Source", 
                            "headerFilter": True,
                            "editor": "select",
                            "editorParams": {"values": node_editor_values},
                            "formatterParams": {"labels": node_editor_values}
                        },
                        {
                            "title": "Edge Type", 
                            "field": "Edge Type", 
                            "headerFilter": True,
                            "editor": "select",
                            "editorParams": {"values": edge_type_editor_values},
                        },
                        {
                            "title": "Target", 
                            "field": "Target", 
                            "headerFilter": True,
                            "editor": "select",
                            "editorParams": {"values": node_editor_values},
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

# Handle table data changes (including cell edits)
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
    """Handle table data changes - now much simpler with UUIDs"""
    if not changed_data:
        return no_update, no_update, no_update, no_update
    
    try:
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                edge_id = row['ID']
                updates = {}
                
                if 'Identifier' in row:
                    updates['identifier'] = row['Identifier'] or ''
                if 'Source' in row:
                    updates['source_node_id'] = row['Source']      # Already a UUID
                if 'Target' in row:
                    updates['target_node_id'] = row['Target']      # Already a UUID
                if 'Edge Type' in row:
                    updates['edge_type_id'] = row['Edge Type']     # Already a UUID
                if 'Description' in row:
                    updates['description'] = row['Description'] or ''
                
                if updates:
                    success, message = model.update_edge(edge_id, **updates)
                    if success:
                        updated_count += 1
                    else:
                        errors.append(f"Failed to update edge {edge_id}: {message}")
        
        # Get fresh data from database
        updated_data = get_edges_from_db()
        
        if errors:
            message = f"Updated {updated_count} edges. Errors: {'; '.join(errors[:2])}"
            return updated_data, True, message, "warning"
        else:
            message = f"Successfully saved changes to {updated_count} edge(s)"
            return updated_data, True, message, "success"
            
    except Exception as e:
        message = f"Error saving changes: {str(e)}"
        return no_update, True, message, "danger"

# def handle_data_change(changed_data, current_data):
#     """Handle table data changes including cell edits with dropdown selections"""
#     if not changed_data:
#         return no_update, no_update, no_update, no_update
    
#     print(f"DEBUG: Data changed event fired with: {changed_data}")
    
#     try:
#         # Get lookup dictionaries for mapping display names to IDs
#         nodes = model.get_nodes()
#         edge_types = model.get_edge_types()
        
#         # Create mapping dictionaries
#         node_name_to_id = {}
#         for node in nodes:
#             # Handle new format: "Identifier - Name" or just "Name"
#             if node.identifier is not None and str(node.identifier).strip() != '':
#                 display_name = f"{str(node.identifier)} - {str(node.name)}"
#             else:
#                 display_name = str(node.name)
#             node_name_to_id[display_name] = str(node.id)
        
#         edge_type_name_to_id = {}
#         for et in edge_types:
#             if et.identifier is not None and str(et.identifier).strip() != '':
#                 display_name = f"{str(et.identifier)} - {str(et.name)}"
#             else:
#                 display_name = str(et.name)
#             edge_type_name_to_id[display_name] = str(et.id)
        
#         errors = []
#         updated_count = 0
        
#         for row in changed_data:
#             if 'ID' in row:
#                 edge_id = row['ID']
                
#                 # Build update dictionary
#                 updates = {}
                
#                 if 'Identifier' in row:
#                     updates['identifier'] = row['Identifier'] or ''
                
#                 if 'Source' in row:
#                     source_display = row['Source']
#                     source_node_id = node_name_to_id.get(source_display)
#                     if source_node_id:
#                         updates['source_node_id'] = source_node_id
#                     else:
#                         errors.append(f"Could not find source node: {source_display}")
#                         continue
                
#                 if 'Target' in row:
#                     target_display = row['Target']
#                     target_node_id = node_name_to_id.get(target_display)
#                     if target_node_id:
#                         updates['target_node_id'] = target_node_id
#                     else:
#                         errors.append(f"Could not find target node: {target_display}")
#                         continue
                
#                 if 'Edge Type' in row:
#                     edge_type_display = row['Edge Type']
#                     edge_type_id = edge_type_name_to_id.get(edge_type_display)
#                     if edge_type_id:
#                         updates['edge_type_id'] = edge_type_id
#                     else:
#                         errors.append(f"Could not find edge type: {edge_type_display}")
#                         continue
                
#                 if 'Description' in row:
#                     updates['description'] = row['Description'] or ''
                
#                 # Update the edge with all changed fields
#                 if updates:
#                     success, message = model.update_edge(edge_id, **updates)
#                     if success:
#                         updated_count += 1
#                     else:
#                         errors.append(f"Failed to update edge {edge_id}: {message}")
        
#         # Get fresh data from database
#         updated_data = get_edges_from_db()
        
#         if errors:
#             message = f"Updated {updated_count} edges. Errors: {'; '.join(errors[:2])}" + (f" and {len(errors)-2} more..." if len(errors) > 2 else "")
#             return updated_data, True, message, "warning"
#         else:
#             message = f"Successfully saved changes to {updated_count} edge(s)"
#             return updated_data, True, message, "success"
            
#     except Exception as e:
#         print(f"Error handling data change: {e}")
#         message = f"Error saving changes: {str(e)}"
#         return no_update, True, message, "danger"

# Test callback to debug tabulator events and update columns
# @callback(
#     [
#         Output('edges-table', 'columns'),
#         Output('toast-message', 'is_open', allow_duplicate=True),
#         Output('toast-message', 'children', allow_duplicate=True),
#         Output('toast-message', 'icon', allow_duplicate=True)
#     ],
#     [
#         Input('edges-table', 'data'),
#         Input('edges-table', 'columns'),
#         Input('refresh-edges-btn', 'n_clicks'),
#         Input('edges-table', 'cellEdited'),
#         Input('edges-table', 'rowClicked'),
#         Input('edges-table', 'dataChanged'),
#         Input('edges-table', 'dataEdited')
#     ],
#     prevent_initial_call=True
# )

# # def debug_tabulator_events(data, columns, refresh_clicks, cell_edited, row_clicked, data_changed, data_edited):
# #     """Debug callback to see which events are firing"""
# #     ctx = dash.callback_context
# #     if not ctx.triggered:
# #         return no_update, no_update, no_update
    
# #     trigger = ctx.triggered[0]
# #     prop_id = trigger['prop_id']
# #     value = trigger['value']
    
# #     print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
    
# #     # Don't show toasts for dataChanged since we handle that elsewhere
# #     if 'dataChanged' in prop_id:
# #         return no_update, no_update, no_update
    
# #     if 'cellEdited' in prop_id:
# #         print(f"DEBUG: Cell edited data: {cell_edited}")
# #         return True, f"Cell edited event detected: {cell_edited}", "info"
    
# #     elif 'dataEdited' in prop_id:
# #         print(f"DEBUG: Data edited: {data_edited}")
# #         return True, f"Data edited event detected: {data_edited}", "success"
    
# #     elif 'rowClicked' in prop_id:
# #         return True, f"Row clicked: {row_clicked}", "info"
    
# #     elif 'refresh-edges-btn' in prop_id:
# #         return True, "Refresh button clicked", "info"
    
# #     elif 'edges-table.data' in prop_id:
# #         return True, f"Table data updated - {len(data) if data else 0} rows", "info"
        
# #     elif 'edges-table.columns' in prop_id:
# #         return True, f"Table columns updated - {len(columns) if columns else 0} columns", "info"
    
# #     return no_update, no_update, no_update

# def update_table_columns(data, columns, refresh_clicks, cell_edited, row_clicked, data_changed, data_edited):
#     """Update table columns with fresh dropdown options and debug tabulator events"""
    
#     # Get fresh dropdown data
#     nodes = get_nodes_for_dropdown()
#     edge_types = get_edge_types_for_dropdown()
    
#     node_values = {node['value']: node['label'] for node in nodes}
#     edge_type_values = {et['value']: et['label'] for et in edge_types}
    
#     columns = [
#         {"title": "ID", "field": "ID", "headerFilter": False, "visible": False},
#         {"title": "Identifier", "field": "Identifier", "headerFilter": True, "editor": "input"},
#         {
#             "title": "Source", 
#             "field": "Source", 
#             "headerFilter": True,
#             "editor": "list",
#             "editorParams": {"values": node_values}
#         },
#         {
#             "title": "Edge Type", 
#             "field": "Edge Type", 
#             "headerFilter": True,
#             "editor": "list",
#             "editorParams": {"values": edge_type_values}
#         },
#         {
#             "title": "Target", 
#             "field": "Target", 
#             "headerFilter": True,
#             "editor": "list",
#             "editorParams": {"values": node_values}
#         },
#         {"title": "Description", "field": "Description", "headerFilter": True, "editor": "input"}
#     ]
    
#     # Debug logic
#     ctx = dash.callback_context
#     if ctx.triggered:
#         trigger = ctx.triggered[0]
#         prop_id = trigger['prop_id']
#         value = trigger['value']
        
#         print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
        
#         # Don't show toasts for dataChanged since it's handled elsewhere
#         if 'dataChanged' in prop_id:
#             return columns, no_update, no_update, no_update
        
#         if 'cellEdited' in prop_id:
#             print(f"DEBUG: Cell edited data: {cell_edited}")
#             return columns, True, f"Cell edited event detected: {cell_edited}", "info"
        
#         elif 'dataEdited' in prop_id:
#             print(f"DEBUG: Data edited: {data_edited}")
#             return columns, True, f"Data edited event detected: {data_edited}", "success"
        
#         elif 'rowClicked' in prop_id:
#             return columns, True, f"Row clicked: {row_clicked}", "info"
        
#         elif 'refresh-edges-btn' in prop_id:
#             return columns, True, f"Table columns refreshed with {len(nodes)} nodes", "info"

# def debug_tabulator_events(cell_edited, row_clicked, data_changed, data_edited):
#     """Debug callback to see which events are firing"""
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return no_update, no_update, no_update
    
#     trigger = ctx.triggered[0]
#     prop_id = trigger['prop_id']
#     value = trigger['value']
    
#     print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
    
#     # Don't show toasts for dataChanged since we handle that elsewhere
#     if 'dataChanged' in prop_id:
#         return no_update, no_update, no_update
    
#     if 'cellEdited' in prop_id:
#         print(f"DEBUG: Cell edited data: {cell_edited}")
#         return True, f"Cell edited event detected: {cell_edited}", "info"
    
#     elif 'dataEdited' in prop_id:
#         print(f"DEBUG: Data edited: {data_edited}")
#         return True, f"Data edited event detected: {data_edited}", "success"
    
#     elif 'rowClicked' in prop_id:
#         return True, f"Row clicked: {row_clicked}", "info"
    
#     return no_update, no_update, no_update

# def debug_tabulator_events(data, columns, refresh_clicks, cell_edited, row_clicked, data_changed, data_edited):
#     """Debug callback to see which events are firing"""
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return no_update, no_update, no_update
    
#     trigger = ctx.triggered[0]
#     prop_id = trigger['prop_id']
#     value = trigger['value']
    
#     print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
    
#     # Don't show toasts for dataChanged since we handle that elsewhere
#     if 'dataChanged' in prop_id:
#         return no_update, no_update, no_update
    
#     if 'cellEdited' in prop_id:
#         print(f"DEBUG: Cell edited data: {cell_edited}")
#         return True, f"Cell edited event detected: {cell_edited}", "info"
    
#     elif 'dataEdited' in prop_id:
#         print(f"DEBUG: Data edited: {data_edited}")
#         return True, f"Data edited event detected: {data_edited}", "success"
    
#     elif 'rowClicked' in prop_id:
#         return True, f"Row clicked: {row_clicked}", "info"
    
#     elif 'refresh-edges-btn' in prop_id:
#         return True, "Refresh button clicked", "info"
    
#     elif 'edges-table.data' in prop_id:
#         return True, f"Table data updated - {len(data) if data else 0} rows", "info"
        
#     elif 'edges-table.columns' in prop_id:
#         return True, f"Table columns updated - {len(columns) if columns else 0} columns", "info"
    
#     return no_update, no_update, no_update

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

# Toggle create modal
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

# Toggle delete modal
@callback(
    Output('delete-edge-modal', 'is_open'),
    Output('delete-modal-body', 'children', allow_duplicate=True),
    [Input('delete-edge-btn', 'n_clicks'),
     Input('confirm-delete-edge', 'n_clicks'),
     Input('cancel-delete-edge', 'n_clicks')],
    [State('delete-edge-modal', 'is_open'),
     State('edges-table', 'multiRowsClicked'),
     State('edges-table', 'data')],
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, data):
    """Toggle delete confirmation modal"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-edge-btn' and selected_rows:
        selected_edges = [f"{row['Source']} → {row['Target']} ({row['Edge Type']})" for row in selected_rows]
        body = html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_rows)} edge(s)?"),
            html.Ul([html.Li(name) for name in selected_edges]),
            html.P("This action cannot be undone.", className="text-danger fw-bold")
        ])
        return True, body
    elif button_id in ['confirm-delete-edge', 'cancel-delete-edge']:
        return False, ""
    
    return is_open, ""

# Handle CRUD operations
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
     State('edges-table', 'multiRowsClicked')],
    prevent_initial_call=True
)
def manage_edges(create_clicks, delete_clicks, identifier, source_id, target_id, edge_type_id, 
                description, data, selected_rows):
    """Handle create and delete operations"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new edge
    if button_id == 'confirm-create-edge' and source_id and target_id and edge_type_id:
        # Use database to create edge
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
            # Get updated data from database
            updated_data = get_edges_from_db()
            return updated_data, True, message, "success", '', None, None, None, ''
        else:
            return data, True, f"Failed to create edge: {message}", "danger", no_update, no_update, no_update, no_update, no_update
    
    # Delete selected edges
    elif button_id == 'confirm-delete-edge' and selected_rows:
        deleted_count = 0
        errors = []
        
        for row in selected_rows:
            edge_id = row['ID']
            success, message = model.delete_edge(edge_id)
            if success:
                deleted_count += 1
            else:
                errors.append(f"Failed to delete edge: {message}")
        
        # Get updated data from database
        updated_data = get_edges_from_db()
        
        if errors:
            message = f"Deleted {deleted_count} edges. Errors: {'; '.join(errors[:3])}" + (f" and {len(errors)-3} more..." if len(errors) > 3 else "")
            return updated_data, True, message, "warning", no_update, no_update, no_update, no_update, no_update
        else:
            message = f"Successfully deleted {deleted_count} edge(s)"
            return updated_data, True, message, "success", no_update, no_update, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

# Download CSV
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

# Print functionality
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

# Refresh functionality - now reloads from database
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