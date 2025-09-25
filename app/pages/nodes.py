# pages/nodes.py - Database integrated version
import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import dash_tabulator
import pandas as pd
import uuid
from datetime import datetime
from typing import Any, Dict, List

# Import model to access database
from models.model import Model

dash.register_page(__name__, path='/nodes')

# Initialize model for database access
model = Model()

def get_nodes_from_db() -> List[Dict[str, Any]]:
    """Get nodes from database"""
    try:
        return model.get_nodes_for_dash_table()
    except Exception as e:
        print(f"Error getting nodes from database: {e}")
        return []

def ensure_sample_data():
    """Ensure there's some sample data in the database"""
    try:
        nodes = model.get_nodes_for_dash_table()
        if len(nodes) == 0:
            # Add some sample nodes
            sample_nodes = [
                {
                    'id': '00000cf8-8a34-42a8-b856-b9615ee93927',
                    'identifier': 'ERG350',
                    'name': 'Burwood Station Pedestrian Overpass',
                    'description': 'Location Breakdown Structure (LBS) Element'
                },
                {
                    'id': '00000de-7564-4edc-a2a8-d934d316d41',
                    'identifier': '',
                    'name': 'Operate, Maintain, & Sustain (OM)',
                    'description': 'Work Phase'
                },
                {
                    'id': '0106f8d-bd32-48d6-a831-c40608d7a31d',
                    'identifier': '',
                    'name': 'Package Interface Register (PIR)',
                    'description': 'Root Node for the Interface Register'
                }
            ]
            
            for node_data in sample_nodes:
                model.create_node(
                    node_id=node_data['id'],
                    identifier=node_data['identifier'],
                    name=node_data['name'],
                    description=node_data['description']
                )
            print(f"Added {len(sample_nodes)} sample nodes to database")
    except Exception as e:
        print(f"Error ensuring sample data: {e}")

# Initialize sample data on module load
ensure_sample_data()

def layout():
    # Get current nodes from database
    current_nodes = get_nodes_from_db()
    
    return html.Div([
        # Fixed alert container - positioned outside main flow
        html.Div(id="alert-container", className="alert-container"),
        
        # Main container
        html.Div([
            # Toolbar
            html.Div([
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-plus-lg me-2"), "Create"], 
                                 id="create-node-btn", color="primary", className="me-2", 
                                 title="Create a new Node"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"], 
                                 id="refresh-nodes-btn", color="primary", className="me-2", 
                                 title="Refresh the Nodes Table"),
                        dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                                 id="delete-node-btn", color="warning", 
                                 title="Delete a selected Node", disabled=True),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                                 id="print-nodes-btn", color="primary", className="me-2", 
                                 title="Print the Table to PDF"),
                        dbc.Button([html.I(className="bi bi-download me-2"), "Download"], 
                                 id="download-nodes-btn", color="primary", 
                                 title="Download the Table as CSV"),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 nodes-toolbar"),
            
            # Table - dash-tabulator with simplified configuration
            html.Div([
                dash_tabulator.DashTabulator(
                    id='nodes-table',
                    theme='tabulator_bootstrap5', 
                    data=current_nodes,
                    columns=[
                        {"title": "ID", "field": "ID", "width": 300, "headerFilter": True},
                        {"title": "Identifier", "field": "Identifier", "width": 200, "headerFilter": True, "editor": "input"},
                        {"title": "Name", "field": "Name", "width": 300, "headerFilter": True, "editor": "input"},
                        {"title": "Description", "field": "Description", "headerFilter": True, "editor": "input"}
                    ],
                    options={
                        "selectable": "highlight",  # Enable row selection with highlighting
                        "selectableRangeMode": "click",  # Allow multi-selection with click
                        "pagination": "local",
                        "paginationSize": 10,
                        "paginationSizeSelector": [5, 10, 20, 50],
                        "paginationButtonCount": 5,
                        "paginationCounter": "rows",
                        "movableColumns": True,
                        "resizableColumns": True,
                        "layout": "fitColumns",
                        "responsiveLayout": "hide",
                        "tooltips": True,
                        "clipboard": True,
                        "printAsHtml": True,
                        "printHeader": "Nodes Table",
                    }
                )
            ]),
            
        ], className="container-fluid px-4 py-5"),
        
        # Create Node Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create New Node")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Identifier:", className="fw-bold"),
                        dbc.Input(
                            id="new-node-identifier", 
                            type="text", 
                            placeholder="Enter unique identifier (optional)"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Name:", className="fw-bold"),
                        dbc.Input(
                            id="new-node-name", 
                            type="text", 
                            placeholder="Enter node name*",
                            required=True
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-node-description", 
                            placeholder="Enter description (optional)",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Create Node", id="confirm-create-node", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-create-node", color="secondary")
            ])
        ], id="create-node-modal", is_open=False, backdrop="static"),
        
        # Delete Confirmation Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button("Delete", id="confirm-delete-node", color="danger", className="me-2"),
                dbc.Button("Cancel", id="cancel-delete-node", color="secondary")
            ])
        ], id="delete-node-modal", is_open=False, backdrop="static"),
        
        # Hidden download component
        dcc.Download(id="download-nodes-csv")
    ])

# Handle table data changes (including cell edits)
@callback(
    [Output('nodes-table', 'data', allow_duplicate=True),
     Output('alert-container', 'children', allow_duplicate=True)],
    Input('nodes-table', 'dataChanged'),
    State('nodes-table', 'data'),
    prevent_initial_call=True
)
def handle_data_change(changed_data, current_data):
    """Handle table data changes including cell edits"""
    if not changed_data:
        return no_update, no_update
    
    print(f"DEBUG: Data changed event fired with: {changed_data}")
    
    try:
        # Try to identify what changed by comparing with current data
        # For now, let's just save all the data and show a success message
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                node_id = row['ID']
                
                # Update each field that might have changed
                updates = {}
                if 'Identifier' in row:
                    updates['identifier'] = row['Identifier'] or ''
                if 'Name' in row:
                    updates['name'] = row['Name']
                if 'Description' in row:
                    updates['description'] = row['Description'] or ''
                
                # Update the node with all fields
                result = model.update_node(node_id, **updates)
                if result['success']:
                    updated_count += 1
                else:
                    errors.append(f"Failed to update node {node_id}: {result['message']}")
        
        # Get fresh data from database
        updated_data = get_nodes_from_db()
        
        if errors:
            alert = dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                f"Updated {updated_count} nodes. Errors: {'; '.join(errors[:2])}" + 
                (f" and {len(errors)-2} more..." if len(errors) > 2 else "")
            ], color="warning", dismissable=True, duration=5000)
        else:
            alert = dbc.Alert([
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Successfully saved changes to {updated_count} node(s)"
            ], color="success", dismissable=True, duration=3000)
        
        return updated_data, alert
            
    except Exception as e:
        print(f"Error handling data change: {e}")
        alert = dbc.Alert([
            html.I(className="bi bi-x-circle-fill me-2"),
            f"Error saving changes: {str(e)}"
        ], color="danger", dismissable=True, duration=4000)
        return no_update, alert

# Test callback to debug tabulator events
@callback(
    Output('alert-container', 'children', allow_duplicate=True),
    [Input('nodes-table', 'cellEdited'),
     Input('nodes-table', 'rowClicked'),
     Input('nodes-table', 'dataChanged'),
     Input('nodes-table', 'dataEdited')],
    prevent_initial_call=True
)
def debug_tabulator_events(cell_edited, row_clicked, data_changed, data_edited):
    """Debug callback to see which events are firing"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    
    trigger = ctx.triggered[0]
    prop_id = trigger['prop_id']
    value = trigger['value']
    
    print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
    
    # Don't show alerts for dataChanged since we handle that elsewhere
    if 'dataChanged' in prop_id:
        return no_update
    
    if 'cellEdited' in prop_id:
        print(f"DEBUG: Cell edited data: {cell_edited}")
        return dbc.Alert([
            html.I(className="bi bi-info-circle-fill me-2"),
            f"Cell edited event detected: {cell_edited}"
        ], color="info", dismissable=True, duration=3000)
    
    elif 'dataEdited' in prop_id:
        print(f"DEBUG: Data edited: {data_edited}")
        return dbc.Alert([
            html.I(className="bi bi-info-circle-fill me-2"),
            f"Data edited event detected: {data_edited}"
        ], color="success", dismissable=True, duration=3000)
    
    elif 'rowClicked' in prop_id:
        return dbc.Alert([
            html.I(className="bi bi-info-circle-fill me-2"),
            f"Row clicked: {row_clicked}"
        ], color="info", dismissable=True, duration=2000)
    
    return no_update

# Enable/disable delete button based on selection
@callback(
    Output('delete-node-btn', 'disabled'),
    Input('nodes-table', 'multiRowsClicked')
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    print(f"DEBUG: toggle_delete_button called with selected_rows: {selected_rows}")
    if selected_rows is None:
        return True
    return len(selected_rows) == 0

# Toggle create modal
@callback(
    Output('create-node-modal', 'is_open'),
    [Input('create-node-btn', 'n_clicks'),
     Input('confirm-create-node', 'n_clicks'),
     Input('cancel-create-node', 'n_clicks')],
    State('create-node-modal', 'is_open')
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Toggle create node modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open

# Toggle delete modal
@callback(
    Output('delete-node-modal', 'is_open'),
    Output('delete-modal-body', 'children'),
    [Input('delete-node-btn', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks'),
     Input('cancel-delete-node', 'n_clicks')],
    [State('delete-node-modal', 'is_open'),
     State('nodes-table', 'multiRowsClicked'),
     State('nodes-table', 'data')]
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, data):
    """Toggle delete confirmation modal"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-node-btn' and selected_rows:
        selected_nodes = [row['Name'] for row in selected_rows]
        body = html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_rows)} node(s)?"),
            html.Ul([html.Li(name) for name in selected_nodes]),
            html.P("This action cannot be undone.", className="text-danger fw-bold")
        ])
        return True, body
    elif button_id in ['confirm-delete-node', 'cancel-delete-node']:
        return False, ""
    
    return is_open, ""

# Handle CRUD operations
@callback(
    [Output('nodes-table', 'data'),
     Output('alert-container', 'children'),
     Output('new-node-identifier', 'value'),
     Output('new-node-name', 'value'),
     Output('new-node-description', 'value')],
    [Input('confirm-create-node', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks')],
    [State('new-node-identifier', 'value'),
     State('new-node-name', 'value'),
     State('new-node-description', 'value'),
     State('nodes-table', 'data'),
     State('nodes-table', 'multiRowsClicked')]
)
def manage_nodes(create_clicks, delete_clicks, identifier, name, description, data, selected_rows):
    """Handle create and delete operations"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new node
    if button_id == 'confirm-create-node' and name:
        # Use database to create node
        new_node_id = str(uuid.uuid4())
        result = model.create_node(
            node_id=new_node_id,
            identifier=identifier or '',
            name=name,
            description=description or ''
        )
        
        if result['success']:
            # Get updated data from database
            updated_data = get_nodes_from_db()
            alert = dbc.Alert([
                html.I(className="bi bi-check-circle-fill me-2"),
                f"Successfully created node: {name}"
            ], color="success", dismissable=True, duration=4000)
            return updated_data, alert, '', '', ''
        else:
            alert = dbc.Alert([
                html.I(className="bi bi-x-circle-fill me-2"),
                f"Failed to create node: {result['message']}"
            ], color="danger", dismissable=True, duration=4000)
            return data, alert, no_update, no_update, no_update
    
    # Delete selected nodes
    elif button_id == 'confirm-delete-node' and selected_rows:
        deleted_count = 0
        errors = []
        
        for row in selected_rows:
            node_id = row['ID']
            success, message = model.delete_node(node_id)
            if success:
                deleted_count += 1
            else:
                errors.append(f"Failed to delete {row['Name']}: {message}")
        
        # Get updated data from database
        updated_data = get_nodes_from_db()
        
        if errors:
            alert = dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                f"Deleted {deleted_count} nodes. Errors: {'; '.join(errors[:3])}" + 
                (f" and {len(errors)-3} more..." if len(errors) > 3 else "")
            ], color="warning", dismissable=True, duration=6000)
        else:
            alert = dbc.Alert([
                html.I(className="bi bi-trash-fill me-2"),
                f"Successfully deleted {deleted_count} node(s)"
            ], color="success", dismissable=True, duration=4000)
        
        return updated_data, alert, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update

# Download CSV
@callback(
    Output('download-nodes-csv', 'data'),
    Input('download-nodes-btn', 'n_clicks'),
    State('nodes-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Download nodes data as CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)
        return dict(
            content=csv_string,
            filename=f"nodes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

# Print functionality
@callback(
    Output('alert-container', 'children', allow_duplicate=True),
    Input('print-nodes-btn', 'n_clicks'),
    prevent_initial_call=True
)
def print_table(n_clicks):
    """Handle print functionality"""
    if n_clicks:
        alert = dbc.Alert([
            html.I(className="bi bi-info-circle-fill me-2"),
            "Print functionality would open a print dialog or generate a PDF report."
        ], color="info", dismissable=True, duration=4000)
        return alert
    return no_update

# Refresh functionality - now reloads from database
@callback(
    [Output('nodes-table', 'data', allow_duplicate=True),
     Output('alert-container', 'children', allow_duplicate=True)],
    Input('refresh-nodes-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table(n_clicks):
    """Handle refresh functionality - reload from database"""
    if n_clicks:
        try:
            refreshed_data = get_nodes_from_db()
            alert = dbc.Alert([
                html.I(className="bi bi-arrow-clockwise me-2"),
                f"Table refreshed successfully - loaded {len(refreshed_data)} nodes"
            ], color="info", dismissable=True, duration=2000)
            return refreshed_data, alert
        except Exception as e:
            alert = dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                f"Error refreshing data: {str(e)}"
            ], color="danger", dismissable=True, duration=4000)
            return no_update, alert
    return no_update, no_update