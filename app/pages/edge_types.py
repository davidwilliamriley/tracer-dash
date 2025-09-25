# pages/edge_types.py
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

dash.register_page(__name__, path='/edge-types')

# Initialize model for database access
model = Model()

def get_edge_types_from_db() -> List[Dict[str, Any]]:
    """Get edge types from database"""
    try:
        return model.get_edge_types_for_table()
    except Exception as e:
        print(f"Error getting edge types from database: {e}")
        return []

def ensure_sample_data():
    """Ensure there's some sample data in the database"""
    try:
        edge_types = model.get_edge_types_for_table()
        if len(edge_types) == 0:
            # Add some sample edge types
            sample_edge_types = [
                {
                    'id': '11111cf8-8a34-42a8-b856-b9615ee93927',
                    'identifier': 'REL001',
                    'name': 'Dependency',
                    'description': 'Represents a dependency relationship between nodes'
                },
                {
                    'id': '22222de-7564-4edc-a2a8-d934d316d41',
                    'identifier': 'REL002',
                    'name': 'Containment',
                    'description': 'Represents a parent-child containment relationship'
                },
                {
                    'id': '3333f8d-bd32-48d6-a831-c40608d7a31d',
                    'identifier': 'REL003',
                    'name': 'Interface',
                    'description': 'Represents an interface connection between components'
                }
            ]
            
            for edge_type_data in sample_edge_types:
                model.create_edge_type(
                    edge_type_id=edge_type_data['id'],
                    identifier=edge_type_data['identifier'],
                    name=edge_type_data['name'],
                    description=edge_type_data['description']
                )
            print(f"Added {len(sample_edge_types)} sample edge types to database")
    except Exception as e:
        print(f"Error ensuring sample data: {e}")

# Initialize sample data on module load
ensure_sample_data()

def layout():
    # Get current edge types from database
    current_edge_types = get_edge_types_from_db()
    
    return html.Div([
        # Toast notification component
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
                                 id="create-edge-type-btn", color="primary", className="me-2", 
                                 title="Create a new Edge Type"),
                        dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Refresh"], 
                                 id="refresh-edge-types-btn", color="primary", className="me-2", 
                                 title="Refresh the Edge Types Table"),
                        dbc.Button([html.I(className="bi bi-trash me-2"), "Delete"], 
                                 id="delete-edge-type-btn", color="warning", 
                                 title="Delete a selected Edge Type", disabled=True),
                    ], className="d-flex justify-content-start"),
                ], className="col-md-6"),
                html.Div([
                    html.Div([
                        dbc.Button([html.I(className="bi bi-printer me-2"), "Print"], 
                                 id="print-edge-types-btn", color="primary", className="me-2", 
                                 title="Print the Table to PDF"),
                        dbc.Button([html.I(className="bi bi-download me-2"), "Download"], 
                                 id="download-edge-types-btn", color="primary", 
                                 title="Download the Table as CSV"),
                    ], className="d-flex justify-content-end"),
                ], className="col-md-6"),
            ], className="row justify-content-between mb-3 edge-types-toolbar"),
            
            # Table - dash-tabulator with simplified configuration
            html.Div([
                dash_tabulator.DashTabulator(
                    id='edge-types-table',
                    theme='tabulator', 
                    data=current_edge_types,
                    columns=[
                        {"title": "ID", "field": "ID", "width": 300, "headerFilter": True, "editor": False, "visible": False},
                        {"title": "Identifier", "field": "Identifier", "width": 200, "headerFilter": True, "editor": "input"},
                        {"title": "Name", "field": "Name", "width": 300, "headerFilter": True, "editor": "input"},
                        {"title": "Description", "field": "Description", "headerFilter": True, "editor": "input"}
                    ],
                    options={
                        "selectable": True,
                        "selectableRangeMode": "click",
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
                        "printHeader": "Edge Types Table",
                    }
                )
            ]),
            
        ], className="container-fluid px-4 py-5"),
        
        # Create Edge Type Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Create New Edge Type")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Identifier:", className="fw-bold"),
                        dbc.Input(
                            id="new-edge-type-identifier", 
                            type="text", 
                            placeholder="Enter unique identifier (optional)"
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Name:", className="fw-bold"),
                        dbc.Input(
                            id="new-edge-type-name", 
                            type="text", 
                            placeholder="Enter edge type name*",
                            required=True
                        )
                    ], width=12, className="mb-3"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Description:", className="fw-bold"),
                        dbc.Textarea(
                            id="new-edge-type-description", 
                            placeholder="Enter description (optional)",
                            rows=3
                        )
                    ], width=12)
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Create Edge Type", id="confirm-create-edge-type", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-create-edge-type", color="secondary")
            ])
        ], id="create-edge-type-modal", is_open=False, backdrop="static"),
        
        # Delete Confirmation Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Confirm Delete")),
            dbc.ModalBody(html.Div(id="delete-modal-body")),
            dbc.ModalFooter([
                dbc.Button("Delete", id="confirm-delete-edge-type", color="danger", className="me-2"),
                dbc.Button("Cancel", id="cancel-delete-edge-type", color="secondary")
            ])
        ], id="delete-edge-type-modal", is_open=False, backdrop="static"),
        
        # Hidden download component
        dcc.Download(id="download-edge-types-csv")
    ])

# Handle table data changes (including cell edits)
@callback(
    [
        Output('edge-types-table', 'data', allow_duplicate=True),
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('edge-types-table', 'dataChanged'),
    State('edge-types-table', 'data'),
    prevent_initial_call=True
)
def handle_data_change(changed_data, current_data):
    """Handle table data changes including cell edits"""
    if not changed_data:
        return no_update, no_update, no_update, no_update
    
    print(f"DEBUG: Data changed event fired with: {changed_data}")
    
    try:
        # Try to identify what changed by comparing with current data
        # For now, let's just save all the data and show a success message
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                edge_type_id = row['ID']
                
                # Update each field that might have changed
                updates = {}
                if 'Identifier' in row:
                    updates['identifier'] = row['Identifier'] or ''
                if 'Name' in row:
                    updates['name'] = row['Name']
                if 'Description' in row:
                    updates['description'] = row['Description'] or ''
                
                # Update the edge type with all fields
                result = model.update_edge_type(edge_type_id, **updates)
                if isinstance(result, dict) and result.get('success'):
                    updated_count += 1
                else:
                    error_msg = result.get('message', 'Unknown error') if isinstance(result, dict) else 'Update failed'
                    errors.append(f"Failed to update edge type {edge_type_id}: {error_msg}")
        
        # Get fresh data from database
        updated_data = get_edge_types_from_db()
        
        if errors:
            message = f"Updated {updated_count} edge types. Errors: {'; '.join(errors[:2])}" + (f" and {len(errors)-2} more..." if len(errors) > 2 else "")
            return updated_data, True, message, "warning"
        else:
            message = f"Successfully saved changes to {updated_count} edge type(s)"
            return updated_data, True, message, "success"
            
    except Exception as e:
        print(f"Error handling data change: {e}")
        message = f"Error saving changes: {str(e)}"
        return no_update, True, message, "danger"

# Test callback to debug tabulator events
@callback(
    [
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    [Input('edge-types-table', 'cellEdited'),
     Input('edge-types-table', 'rowClicked'),
     Input('edge-types-table', 'dataChanged'),
     Input('edge-types-table', 'dataEdited')],
    prevent_initial_call=True
)
def debug_tabulator_events(cell_edited, row_clicked, data_changed, data_edited):
    """Debug callback to see which events are firing"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update
    
    trigger = ctx.triggered[0]
    prop_id = trigger['prop_id']
    value = trigger['value']
    
    print(f"DEBUG: Tabulator event fired - Property: {prop_id}, Value: {value}")
    
    # Don't show toasts for dataChanged since we handle that elsewhere
    if 'dataChanged' in prop_id:
        return no_update, no_update, no_update
    
    if 'cellEdited' in prop_id:
        print(f"DEBUG: Cell edited data: {cell_edited}")
        return True, f"Cell edited event detected: {cell_edited}", "info"
    
    elif 'dataEdited' in prop_id:
        print(f"DEBUG: Data edited: {data_edited}")
        return True, f"Data edited event detected: {data_edited}", "success"
    
    elif 'rowClicked' in prop_id:
        return True, f"Row clicked: {row_clicked}", "info"
    
    return no_update, no_update, no_update

# Enable/disable delete button based on selection
@callback(
    Output('delete-edge-type-btn', 'disabled'),
    Input('edge-types-table', 'multiRowsClicked')
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    print(f"DEBUG: toggle_delete_button called with selected_rows: {selected_rows}")
    if selected_rows is None:
        return True
    return len(selected_rows) == 0

# Toggle create modal
@callback(
    Output('create-edge-type-modal', 'is_open'),
    [Input('create-edge-type-btn', 'n_clicks'),
     Input('confirm-create-edge-type', 'n_clicks'),
     Input('cancel-create-edge-type', 'n_clicks')],
    State('create-edge-type-modal', 'is_open')
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Toggle create edge type modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open

# Toggle delete modal
@callback(
    Output('delete-edge-type-modal', 'is_open'),
    Output('delete-modal-body', 'children'),
    [Input('delete-edge-type-btn', 'n_clicks'),
     Input('confirm-delete-edge-type', 'n_clicks'),
     Input('cancel-delete-edge-type', 'n_clicks')],
    [State('delete-edge-type-modal', 'is_open'),
     State('edge-types-table', 'multiRowsClicked'),
     State('edge-types-table', 'data')]
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, data):
    """Toggle delete confirmation modal"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-edge-type-btn' and selected_rows:
        selected_edge_types = [row['Name'] for row in selected_rows]
        body = html.Div([
            html.P(f"Are you sure you want to delete the following {len(selected_rows)} edge type(s)?"),
            html.Ul([html.Li(name) for name in selected_edge_types]),
            html.P("This action cannot be undone.", className="text-danger fw-bold")
        ])
        return True, body
    elif button_id in ['confirm-delete-edge-type', 'cancel-delete-edge-type']:
        return False, ""
    
    return is_open, ""

# Handle CRUD operations
@callback(
    [Output('edge-types-table', 'data'),
     Output('toast-message', 'is_open', allow_duplicate=True),
     Output('toast-message', 'children', allow_duplicate=True),
     Output('toast-message', 'icon', allow_duplicate=True),
     Output('new-edge-type-identifier', 'value'),
     Output('new-edge-type-name', 'value'),
     Output('new-edge-type-description', 'value')],
    [Input('confirm-create-edge-type', 'n_clicks'),
     Input('confirm-delete-edge-type', 'n_clicks')],
    [State('new-edge-type-identifier', 'value'),
     State('new-edge-type-name', 'value'),
     State('new-edge-type-description', 'value'),
     State('edge-types-table', 'data'),
     State('edge-types-table', 'multiRowsClicked')],
    prevent_initial_call=True
)
def manage_edge_types(create_clicks, delete_clicks, identifier, name, description, data, selected_rows):
    """Handle create and delete operations"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new edge type
    if button_id == 'confirm-create-edge-type' and name:
        # Use database to create edge type
        new_edge_type_id = str(uuid.uuid4())
        result = model.create_edge_type(
            edge_type_id=new_edge_type_id,
            identifier=identifier or '',
            name=name,
            description=description or ''
        )
        
        if isinstance(result, dict) and result.get('success'):
            # Get updated data from database
            updated_data = get_edge_types_from_db()
            message = f"Successfully created edge type: {name}"
            return updated_data, True, message, "success", '', '', ''
        else:
            error_msg = result.get('message', 'Unknown error') if isinstance(result, dict) else 'Create failed'
            message = f"Failed to create edge type: {error_msg}"
            return data, True, message, "danger", no_update, no_update, no_update
    
    # Delete selected edge types
    elif button_id == 'confirm-delete-edge-type' and selected_rows:
        deleted_count = 0
        errors = []
        
        for row in selected_rows:
            edge_type_id = row['ID']
            success, message = model.delete_edge_type(edge_type_id)
            if success:
                deleted_count += 1
            else:
                errors.append(f"Failed to delete {row['Name']}: {message}")
        
        # Get updated data from database
        updated_data = get_edge_types_from_db()
        
        if errors:
            message = f"Deleted {deleted_count} edge types. Errors: {'; '.join(errors[:3])}" + (f" and {len(errors)-3} more..." if len(errors) > 3 else "")
            return updated_data, True, message, "warning", no_update, no_update, no_update
        else:
            message = f"Successfully deleted {deleted_count} edge type(s)"
            return updated_data, True, message, "success", no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update

# Download CSV
@callback(
    Output('download-edge-types-csv', 'data'),
    Input('download-edge-types-btn', 'n_clicks'),
    State('edge-types-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Download edge types data as CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)
        return dict(
            content=csv_string,
            filename=f"edge_types_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

# Print functionality
@callback(
    [
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('print-edge-types-btn', 'n_clicks'),
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
        Output('edge-types-table', 'data', allow_duplicate=True),
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('refresh-edge-types-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table(n_clicks):
    """Handle refresh functionality - reload from database"""
    if n_clicks:
        try:
            refreshed_data = get_edge_types_from_db()
            message = f"Table refreshed successfully - loaded {len(refreshed_data)} edge types"
            return refreshed_data, True, message, "info"
        except Exception as e:
            message = f"Error refreshing data: {str(e)}"
            return no_update, True, message, "danger"
    return no_update, no_update, no_update, no_update