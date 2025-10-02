# pages/edge_types.py
import dash
from dash import callback, Input, Output, State, no_update
import pandas as pd
import uuid
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional

# Import Model and View
from models.model import Model
from views.edge_type_view import EdgeTypeView

# Register page
dash.register_page(__name__, path='/edge-types')

# Initialize Model and View
model = Model()
view = EdgeTypeView()


# ============================================================================
# BUSINESS LOGIC / CONTROLLER METHODS
# ============================================================================

def get_edge_types_from_db() -> List[Dict[str, Any]]:
    """Get edge types from database"""
    try:
        return model.get_edge_types_for_editor()
    except Exception as e:
        print(f"Error getting edge types from database: {e}")
        return []


def create_edge_type(identifier: str, name: str, description: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Create a new edge type
    
    Args:
        identifier: Edge type identifier (optional)
        name: Edge type name (required)
        description: Edge type description (optional)
        
    Returns:
        Tuple of (success, message, updated_data)
    """
    if not name:
        return False, "Name is required", None
    
    try:
        new_edge_type_id = str(uuid.uuid4())
        result = model.create_edge_type(
            edge_type_id=new_edge_type_id,
            identifier=identifier or '',
            name=name,
            description=description or ''
        )
        
        if isinstance(result, dict) and result.get('success'):
            updated_data = get_edge_types_from_db()
            return True, f"Successfully created edge type: {name}", updated_data
        else:
            error_msg = result.get('message', 'Unknown error') if isinstance(result, dict) else 'Create failed'
            return False, f"Failed to create edge type: {error_msg}", None
    except Exception as e:
        print(f"Error creating edge type: {e}")
        return False, f"Error creating edge type: {str(e)}", None


def update_edge_types(changed_data: List[Dict[str, Any]]) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Update edge types based on changed data
    
    Args:
        changed_data: List of edge type dictionaries with updated values
        
    Returns:
        Tuple of (success, message, updated_data)
    """
    if not changed_data:
        return False, "No data to update", None
    
    try:
        errors = []
        updated_count = 0
        
        for row in changed_data:
            if 'ID' in row:
                edge_type_id = row['ID']
                
                updates = {}
                if 'Identifier' in row:
                    updates['identifier'] = row['Identifier'] or ''
                if 'Name' in row:
                    updates['name'] = row['Name']
                if 'Description' in row:
                    updates['description'] = row['Description'] or ''
                
                result = model.update_edge_type(edge_type_id, **updates)
                if isinstance(result, dict) and result.get('success'):
                    updated_count += 1
                else:
                    error_msg = result.get('message', 'Unknown error') if isinstance(result, dict) else 'Update failed'
                    errors.append(f"Failed to update edge type {edge_type_id}: {error_msg}")
        
        updated_data = get_edge_types_from_db()
        
        if errors:
            message = f"Updated {updated_count} edge types. Errors: {'; '.join(errors[:2])}"
            if len(errors) > 2:
                message += f" and {len(errors)-2} more..."
            return False, message, updated_data
        else:
            return True, f"Successfully saved changes to {updated_count} edge type(s)", updated_data
            
    except Exception as e:
        print(f"Error updating edge types: {e}")
        return False, f"Error saving changes: {str(e)}", None


def delete_edge_types(selected_rows: List[Dict[str, Any]]) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Delete selected edge types
    
    Args:
        selected_rows: List of edge type dictionaries to delete
        
    Returns:
        Tuple of (success, message, updated_data)
    """
    if not selected_rows:
        return False, "No edge types selected for deletion", None
    
    try:
        deleted_count = 0
        errors = []
        
        for row in selected_rows:
            edge_type_id = row['ID']
            success, message = model.delete_edge_type(edge_type_id)
            if success:
                deleted_count += 1
            else:
                errors.append(f"Failed to delete {row['Name']}: {message}")
        
        updated_data = get_edge_types_from_db()
        
        if errors:
            message = f"Deleted {deleted_count} edge types. Errors: {'; '.join(errors[:3])}"
            if len(errors) > 3:
                message += f" and {len(errors)-3} more..."
            return False, message, updated_data
        else:
            return True, f"Successfully deleted {deleted_count} edge type(s)", updated_data
            
    except Exception as e:
        print(f"Error deleting edge types: {e}")
        return False, f"Error deleting edge types: {str(e)}", None


def export_to_csv(data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Export edge types data to CSV
    
    Args:
        data: List of edge type dictionaries
        
    Returns:
        Tuple of (csv_content, filename)
    """
    if not data:
        return "", ""
    
    df = pd.DataFrame(data)
    csv_string = df.to_csv(index=False)
    filename = f"edge_types_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return csv_string, filename


def validate_selection(selected_rows: Optional[List[Dict[str, Any]]]) -> bool:
    """
    Validate if any rows are selected
    
    Args:
        selected_rows: List of selected row dictionaries or None
        
    Returns:
        True if rows are selected, False otherwise
    """
    return selected_rows is not None and len(selected_rows) > 0


# ============================================================================
# LAYOUT
# ============================================================================

def layout():
    """
    Generate the page layout
    
    Returns:
        The complete page layout from the view
    """
    edge_types = get_edge_types_from_db()
    return view.create_layout(edge_types)


# ============================================================================
# CALLBACKS
# ============================================================================

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
    
    success, message, updated_data = update_edge_types(changed_data)
    
    if updated_data is not None:
        icon = "success" if success else "warning"
        return updated_data, True, message, icon
    else:
        return no_update, True, message, "danger"


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


@callback(
    Output('delete-edge-type-btn', 'disabled'),
    Input('edge-types-table', 'multiRowsClicked')
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    print(f"DEBUG: toggle_delete_button called with selected_rows: {selected_rows}")
    return not validate_selection(selected_rows)


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
        selected_names = [row['Name'] for row in selected_rows]
        body = view.create_delete_modal_body(selected_names)
        return True, body
    elif button_id in ['confirm-delete-edge-type', 'cancel-delete-edge-type']:
        return False, ""
    
    return is_open, ""


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
    if button_id == 'confirm-create-edge-type':
        success, message, updated_data = create_edge_type(identifier, name, description)
        
        if success and updated_data is not None:
            return updated_data, True, message, "success", '', '', ''
        else:
            return data, True, message, "danger", no_update, no_update, no_update
    
    # Delete selected edge types
    elif button_id == 'confirm-delete-edge-type':
        success, message, updated_data = delete_edge_types(selected_rows)
        
        if updated_data is not None:
            icon = "success" if success else "warning"
            return updated_data, True, message, icon, no_update, no_update, no_update
        else:
            return data, True, message, "danger", no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update


@callback(
    Output('download-edge-types-csv', 'data'),
    Input('download-edge-types-btn', 'n_clicks'),
    State('edge-types-table', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    """Download edge types data as CSV"""
    if n_clicks and data:
        csv_content, filename = export_to_csv(data)
        if csv_content:
            return dict(content=csv_content, filename=filename)
    return no_update


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