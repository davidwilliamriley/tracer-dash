# pages/nodes.py

# Import Libraries
import dash
from dash import html, dcc, callback, Input, Output, no_update, State
import dash_bootstrap_components as dbc
from datetime import datetime
import json
import pandas as pd
from typing import Any, Dict, List
import uuid

# Import Model and View
from models.model import Model
from utils.pdf_utils import generate_table_pdf
from views.node_view import NodeView

dash.register_page(__name__, path='/nodes')

# Initialize Model and View
model = Model()
view = NodeView()

# ==================== HELPER FUNCTIONS ====================

def get_nodes_data() -> List[Dict[str, Any]]:
    """Get nodes from database for display"""
    try:
        return model.get_nodes_for_editor() or []
    except Exception as e:
        print(f"Error getting nodes: {e}")
        return []

# ==================== LAYOUT ====================

def layout():
    """Main layout - delegates to view"""
    current_nodes = get_nodes_data()
    return view.create_layout(current_nodes)

# ==================== CALLBACKS ====================

# Handle changes to Table Data (Cell Edits)
@callback(
    [
        Output('nodes-table', 'data', allow_duplicate=True),
        Output('toast-message', 'is_open', allow_duplicate=True),
        Output('toast-message', 'children', allow_duplicate=True),
        Output('toast-message', 'icon', allow_duplicate=True)
    ],
    Input('nodes-table', 'dataChanged'),
    State('nodes-table', 'data'),
    prevent_initial_call=True
)
def handle_cell_edit(changed_data, current_data):
    """Handle inline cell editing"""
    if not changed_data:
        return no_update, no_update, no_update, no_update
    
    try:
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                node_id = row['ID']
                updates = {
                    'identifier': row.get('Identifier', ''),
                    'name': row.get('Name', ''),
                    'description': row.get('Description', '')
                }
                
                result = model.update_node(node_id, **updates)
                if result.get('success'):
                    updated_count += 1
                else:
                    errors.append(result.get('message', 'Unknown error'))
        
        updated_data = get_nodes_data()
        
        if errors:
            message = f"Updated {updated_count} nodes. Errors: {'; '.join(errors[:2])}"
            return updated_data, True, message, "warning"
        else:
            return updated_data, True, f"Successfully saved {updated_count} node(s)", "success"
            
    except Exception as e:
        return no_update, True, f"Error saving changes: {str(e)}", "danger"

# Enable/disable delete button based on selection
@callback(
    Output('delete-node-btn', 'disabled'),
    Input('nodes-table', 'multiRowsClicked')
)
def toggle_delete_button(selected_rows):
    """Enable delete button when rows are selected"""
    return not selected_rows or len(selected_rows) == 0

# Toggle create modal
@callback(
    Output('create-node-modal', 'is_open'),
    [Input('create-node-btn', 'n_clicks'),
     Input('confirm-create-node', 'n_clicks'),
     Input('cancel-create-node', 'n_clicks')],
    State('create-node-modal', 'is_open')
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Show/hide create modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open

# Toggle delete modal - FIXED: Added allow_duplicate=True
@callback(
    Output('delete-node-modal', 'is_open'),
    Output('delete-modal-body', 'children', allow_duplicate=True),
    [Input('delete-node-btn', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks'),
     Input('cancel-delete-node', 'n_clicks')],
    [State('delete-node-modal', 'is_open'),
     State('nodes-table', 'multiRowsClicked')],
    prevent_initial_call=True
)
def toggle_delete_modal(delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows):
    """Show/hide delete confirmation modal"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return False, ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'delete-node-btn' and selected_rows:
        selected_names = [row['Name'] for row in selected_rows]
        body = view.create_delete_confirmation(selected_names)
        return True, body
    elif button_id in ['confirm-delete-node', 'cancel-delete-node']:
        return False, ""
    
    return is_open, ""

# Handle CRUD operations
@callback(
    [Output('nodes-table', 'data'),
     Output('toast-message', 'is_open', allow_duplicate=True),
     Output('toast-message', 'children', allow_duplicate=True),
     Output('toast-message', 'icon', allow_duplicate=True),
     Output('new-node-identifier', 'value'),
     Output('new-node-name', 'value'),
     Output('new-node-description', 'value')],
    [Input('confirm-create-node', 'n_clicks'),
     Input('confirm-delete-node', 'n_clicks')],
    [State('new-node-identifier', 'value'),
     State('new-node-name', 'value'),
     State('new-node-description', 'value'),
     State('nodes-table', 'data'),
     State('nodes-table', 'multiRowsClicked')],
    prevent_initial_call=True
)
def handle_crud_operations(create_clicks, delete_clicks, identifier, name, 
                           description, data, selected_rows):
    """Handle create and delete operations"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Create new node
    if button_id == 'confirm-create-node' and name:
        new_node_id = str(uuid.uuid4())
        result = model.create_node(
            node_id=new_node_id,
            identifier=identifier or '',
            name=name,
            description=description or ''
        )
        
        if result.get('success'):
            updated_data = get_nodes_data()
            return updated_data, True, f"Successfully created: {name}", "success", '', '', ''
        else:
            return data, True, f"Failed: {result.get('message')}", "danger", no_update, no_update, no_update
    
    # Delete selected nodes
    elif button_id == 'confirm-delete-node' and selected_rows:
        deleted_count = 0
        errors = []
        
        for row in selected_rows:
            success, message = model.delete_node(row['ID'])
            if success:
                deleted_count += 1
            else:
                errors.append(f"{row['Name']}: {message}")
        
        updated_data = get_nodes_data()
        
        if errors:
            msg = f"Deleted {deleted_count}. Errors: {'; '.join(errors[:2])}"
            return updated_data, True, msg, "warning", no_update, no_update, no_update
        else:
            return updated_data, True, f"Deleted {deleted_count} node(s)", "success", no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update

# Download CSV
@callback(
    Output('download-nodes-csv', 'data'),
    Input('download-nodes-btn', 'n_clicks'),
    State('nodes-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Export nodes to CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        return dict(
            content=df.to_csv(index=False),
            filename=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_nodes.csv"
        )

# Print PDF
@callback(
    Output("print-nodes-pdf", "data"),
    Input("print-nodes-btn", "n_clicks"),
    State("nodes-table", "data"),
    prevent_initial_call=True
)
def download_pdf(n_clicks, table_data):
    return generate_table_pdf(
        data=table_data,
        title="Nodes Table",
        columns_to_exclude=["ID"],
        filename="nodes"
    )

# Refresh Table
@callback(
    [Output('nodes-table', 'data', allow_duplicate=True),
     Output('toast-message', 'is_open', allow_duplicate=True),
     Output('toast-message', 'children', allow_duplicate=True),
     Output('toast-message', 'icon', allow_duplicate=True)],
    Input('refresh-nodes-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_table(n_clicks):
    """Reload data from database"""
    if n_clicks:
        try:
            refreshed_data = get_nodes_data()
            return refreshed_data, True, f"Loaded {len(refreshed_data)} nodes", "info"
        except Exception as e:
            return no_update, True, f"Error: {str(e)}", "danger"
    return no_update, no_update, no_update, no_update