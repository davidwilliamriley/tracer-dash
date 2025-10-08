# pages/edges.py

# Iport Libraries
import dash
from dash import html, dcc, callback, Input, Output, no_update, State
import dash_bootstrap_components as dbc
from datetime import datetime
import json
import pandas as pd
from typing import Any, Dict, List, Tuple, Optional
import uuid

# Import Model and View
from models.model import Model
from utils.pdf_utils import generate_table_pdf
from utils.toast_utils import ToastFactory
from views.edge_view import EdgeView

dash.register_page(__name__, path="/edges")

# Initialize Model and View
model = Model()
view = EdgeView()

# ==================== HELPER FUNCTIONS ====================

def get_edges_from_db() -> List[Dict[str, Any]]:
    """Get Edges from the Database with display names for the table"""
    try:
        raw_edges = model.get_edges_for_editor()
        nodes_for_dropdown = get_nodes_for_dropdown()
        edge_types_for_dropdown = get_edge_types_for_dropdown()

        node_uuid_to_label = {
            str(node["value"]): str(node["label"]) for node in nodes_for_dropdown
        }
        edge_type_uuid_to_label = {
            str(et["value"]): str(et["label"]) for et in edge_types_for_dropdown
        }

        display_edges = []
        for edge in raw_edges:
            source_uuid = edge["Source"]
            edge_type_uuid = edge["Edge Type"]
            target_uuid = edge["Target"]


            display_edge = {
                "ID": edge["ID"],
                "Identifier": edge["Identifier"],
                "Source_UUID": source_uuid,
                "Source": node_uuid_to_label.get(source_uuid, source_uuid),
                "Edge_Type_UUID": edge_type_uuid,
                "Edge Type": edge_type_uuid_to_label.get(edge_type_uuid, edge_type_uuid),
                "Target_UUID": target_uuid,
                "Target": node_uuid_to_label.get(target_uuid, target_uuid),
                "Description": edge["Description"],
            }
            display_edges.append(display_edge)

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
            identifier_str = str(node.identifier) if node.identifier is not None else ""
            if identifier_str.strip():
                label = f"{identifier_str} - {node.name}"
            else:
                label = str(node.name)
            result.append({"label": label, "value": str(node.id)})
        result.sort(key=lambda item: item["label"].lower())
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
            identifier_str = (
                str(edge_type.identifier) if edge_type.identifier is not None else ""
            )
            if identifier_str.strip():
                label = f"{identifier_str} - {edge_type.name}"
            else:
                label = str(edge_type.name)
            result.append({"label": label, "value": str(edge_type.id)})
        result.sort(key=lambda item: item["label"].lower())
        return result
    except Exception as e:
        print(f"Unable to get Edge Types for Dropdowns: {e}")
        return []


# ==================== LAYOUT ====================


def layout():
    """Main layout - delegates to view"""
    current_edges = get_edges_from_db()
    nodes_for_dropdown = get_nodes_for_dropdown()
    edge_types_for_dropdown = get_edge_types_for_dropdown()

    node_label_to_label = {
        str(node["label"]): str(node["label"]) for node in nodes_for_dropdown
    }
    edge_type_label_to_label = {
        str(et["label"]): str(et["label"]) for et in edge_types_for_dropdown
    }

    return view.create_layout(
        current_edges, node_label_to_label, edge_type_label_to_label
    )


# ==================== CALLBACKS ====================


# Populate dropdown options when modal opens
@callback(
    [
        Output("new-edge-source", "options"),
        Output("new-edge-target", "options"),
        Output("new-edge-type", "options"),
    ],
    Input("create-edge-modal", "is_open"),
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
    Output("delete-edge-btn", "disabled"), Input("edges-table", "multiRowsClicked")
)
def toggle_delete_button(selected_rows):
    """Enable/disable delete button based on selection"""
    return not selected_rows or len(selected_rows) == 0


# Toggle create modal
@callback(
    Output("create-edge-modal", "is_open"),
    [
        Input("create-edge-btn", "n_clicks"),
        Input("confirm-create-edge", "n_clicks"),
        Input("cancel-create-edge", "n_clicks"),
    ],
    State("create-edge-modal", "is_open"),
)
def toggle_create_modal(create_clicks, confirm_clicks, cancel_clicks, is_open):
    """Toggle create edge modal"""
    if create_clicks or confirm_clicks or cancel_clicks:
        return not is_open
    return is_open


# Toggle delete modal
@callback(
    Output("delete-edge-modal", "is_open"),
    Output("delete-modal-body", "children", allow_duplicate=True),
    [
        Input("delete-edge-btn", "n_clicks"),
        Input("confirm-delete-edge", "n_clicks"),
        Input("cancel-delete-edge", "n_clicks"),
    ],
    [
        State("delete-edge-modal", "is_open"),
        State("edges-table", "multiRowsClicked"),
        State("edges-table", "data"),
    ],
    prevent_initial_call=True,
)
def toggle_delete_modal(
    delete_clicks, confirm_clicks, cancel_clicks, is_open, selected_rows, raw_table_data
):
    """Toggle delete confirmation modal using raw data"""
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, ""

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "delete-edge-btn" and selected_rows:
        selected_ids = [row.get("ID") for row in selected_rows if "ID" in row]

        raw_selected_rows = []
        for selected_id in selected_ids:
            raw_row = next(
                (row for row in raw_table_data if row.get("ID") == selected_id), None
            )
            if raw_row:
                raw_selected_rows.append(raw_row)

        selected_edges = []
        for formatted_row in selected_rows:
            display_name = f"{formatted_row.get('Source', 'Unknown')} → {formatted_row.get('Target', 'Unknown')} ({formatted_row.get('Edge Type', 'Unknown')})"
            selected_edges.append(display_name)

        body = view.create_delete_confirmation(selected_edges, raw_selected_rows)
        return True, body
    elif button_id in ["confirm-delete-edge", "cancel-delete-edge"]:
        return False, ""

    return is_open, ""


# Handle CRUD operations
@callback(
    [
        Output("edges-table", "data"),
        Output("toast-message", "is_open", allow_duplicate=True),
        Output("toast-message", "children", allow_duplicate=True),
        Output("toast-message", "header", allow_duplicate=True),
        Output("toast-message", "className", allow_duplicate=True),
        Output("new-edge-identifier", "value"),
        Output("new-edge-source", "value"),
        Output("new-edge-target", "value"),
        Output("new-edge-type", "value"),
        Output("new-edge-description", "value"),
    ],
    [
        Input("confirm-create-edge", "n_clicks"),
        Input("confirm-delete-edge", "n_clicks"),
    ],
    [
        State("new-edge-identifier", "value"),
        State("new-edge-source", "value"),
        State("new-edge-target", "value"),
        State("new-edge-type", "value"),
        State("new-edge-description", "value"),
        State("edges-table", "data"),
        State("delete-modal-body", "children"),
    ],
    prevent_initial_call=True,
)
def manage_edges(
    create_clicks,
    delete_clicks,
    identifier,
    source_id,
    target_id,
    edge_type_id,
    description,
    data,
    modal_body_children,
):
    """Handle create and delete operations"""
    ctx = dash.callback_context

    if not ctx.triggered:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Create new edge
    if button_id == "confirm-create-edge" and source_id and target_id and edge_type_id:
        new_edge_id = str(uuid.uuid4())
        result = model.create_edge(
            edge_id=new_edge_id,
            identifier=identifier or "",
            source_node_id=source_id,
            target_node_id=target_id,
            edge_type_id=edge_type_id,
            description=description or "",
        )

        if result.get('success'):
            updated_data = get_edges_from_db()
            header_component = ToastFactory.get_header_by_type("success")
            return updated_data, True, result.get('message'), header_component, "toast-success", "", None, None, None, ""
        else:
            header_component = ToastFactory.get_header_by_type("danger")
            return (
                data,
                True,
                f"Failed to create Edge: {result.get('message')}",
                header_component,
                "toast-danger",
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            )

    # Delete selected edges
    elif button_id == "confirm-delete-edge" and modal_body_children:
        try:

            def find_raw_data(children):
                if (
                    isinstance(children, dict)
                    and children.get("props", {}).get("id") == "raw-selected-data"
                ):
                    return json.loads(children["props"]["children"])
                elif isinstance(children, dict) and "children" in children.get(
                    "props", {}
                ):
                    child_list = children["props"]["children"]
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

            if not raw_selected_rows:
                return (
                    data,
                    True,
                    "Error: Could not find raw data for deletion",
                    "danger",
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

            deleted_count = 0
            errors = []

            for raw_row in raw_selected_rows:
                edge_id = raw_row.get("ID")
                if edge_id:
                    result = model.delete_edge(edge_id)
                    if result['success']:
                        deleted_count += 1
                    else:
                        errors.append(f"Failed to delete edge: {result['message']}")
                else:
                    errors.append("Edge missing ID")

            updated_data = get_edges_from_db()

            if errors:
                message = (
                    f"Deleted {deleted_count} edges. Errors: {'; '.join(errors[:3])}"
                )
                return (
                    updated_data,
                    True,
                    message,
                    "warning",
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )
            else:
                message = f"Successfully deleted {deleted_count} edge(s)"
                return (
                    updated_data,
                    True,
                    message,
                    "success",
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

        except Exception as e:
            return (
                data,
                True,
                f"Error during deletion: {str(e)}",
                "danger",
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            )

    return (
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
    )


# Handle table data changes
@callback(
    [
        Output("edges-table", "data", allow_duplicate=True),
        Output("toast-message", "is_open", allow_duplicate=True),
        Output("toast-message", "children", allow_duplicate=True),
        Output("toast-message", "header", allow_duplicate=True),
        Output("toast-message", "className", allow_duplicate=True),
    ],
    Input("edges-table", "dataChanged"),
    State("edges-table", "data"),
    prevent_initial_call=True,
)
def handle_data_change(changed_data, current_data):
    """Handle table data changes using hidden UUID fields"""
    if not changed_data:
        return no_update, no_update, no_update, no_update, no_update

    try:
        nodes_for_dropdown = get_nodes_for_dropdown()
        edge_types_for_dropdown = get_edge_types_for_dropdown()

        node_label_to_uuid = {
            str(node["label"]): str(node["value"]) for node in nodes_for_dropdown
        }
        edge_type_label_to_uuid = {
            str(et["label"]): str(et["value"]) for et in edge_types_for_dropdown
        }

        errors = []
        updated_count = 0

        for row in changed_data:
            if "ID" in row:
                edge_id = row["ID"]
                updates = {}

                if "Identifier" in row:
                    updates["identifier"] = row["Identifier"] or ""

                if "Source" in row:
                    source_display = row["Source"]
                    source_uuid = node_label_to_uuid.get(source_display)
                    if source_uuid:
                        updates["source_node_id"] = source_uuid
                    elif "Source_UUID" in row and row["Source_UUID"]:
                        updates["source_node_id"] = row["Source_UUID"]
                    else:
                        errors.append(
                            f"Could not find UUID for Source: {source_display}"
                        )
                        continue

                if "Target" in row:
                    target_display = row["Target"]
                    target_uuid = node_label_to_uuid.get(target_display)
                    if target_uuid:
                        updates["target_node_id"] = target_uuid
                    elif "Target_UUID" in row and row["Target_UUID"]:
                        updates["target_node_id"] = row["Target_UUID"]
                    else:
                        errors.append(
                            f"Could not find UUID for Target: {target_display}"
                        )
                        continue

                if "Edge Type" in row:
                    edge_type_display = row["Edge Type"]
                    edge_type_uuid = edge_type_label_to_uuid.get(edge_type_display)
                    if edge_type_uuid:
                        updates["edge_type_id"] = edge_type_uuid
                    elif "Edge_Type_UUID" in row and row["Edge_Type_UUID"]:
                        updates["edge_type_id"] = row["Edge_Type_UUID"]
                    else:
                        errors.append(
                            f"Could not find UUID for Edge Type: {edge_type_display}"
                        )
                        continue

                if "Description" in row:
                    updates["description"] = row["Description"] or ""

                if updates:
                    result = model.update_edge(edge_id, **updates)
                    if result['success']:
                        updated_count += 1
                    else:
                        errors.append(f"Failed to update edge {edge_id}: {result['message']}")

        updated_data = get_edges_from_db()

        if errors:
            message = f"Updated {updated_count} edges. Errors: {'; '.join(errors[:2])}"
            header_component = ToastFactory.get_header_by_type("warning")
            return updated_data, True, message, header_component, "toast-warning"
        else:
            message = f"Successfully saved changes to {updated_count} edge(s)"
            header_component = ToastFactory.get_header_by_type("success")
            return updated_data, True, message, header_component, "toast-success"

    except Exception as e:
        header_component = ToastFactory.get_header_by_type("danger")
        return no_update, True, f"Error saving changes: {str(e)}", header_component, "toast-danger"


# Download CSV
@callback(
    Output("download-edges-csv", "data"),
    Input("download-edges-btn", "n_clicks"),
    State("edges-table", "data"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data):
    """Download edges data as CSV"""
    if n_clicks and data:
        df = pd.DataFrame(data)
        return dict(
            content=df.to_csv(index=False),
            filename=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_edges.csv"
        )

# Print PDF
@callback(
    Output("print-edges-pdf", "data"),
    Input("print-edges-btn", "n_clicks"),
    State("edges-table", "data"),
    prevent_initial_call=True
)
def download_pdf(n_clicks, table_data):
    return generate_table_pdf(
        data=table_data,
        title="Edges Table",
        columns_to_exclude=["ID", "Source_UUID", "Target_UUID", "Edge_Type_UUID"],
        filename="edges"
    )

# Refresh table
@callback(
    [
        Output("edges-table", "data", allow_duplicate=True),
        Output("toast-message", "is_open", allow_duplicate=True),
        Output("toast-message", "children", allow_duplicate=True),
        Output("toast-message", "header", allow_duplicate=True),
        Output("toast-message", "className", allow_duplicate=True),
    ],
    Input("refresh-edges-btn", "n_clicks"),
    prevent_initial_call=True,
)
def refresh_table(n_clicks):
    """Handle refresh functionality"""
    if n_clicks:
        try:
            refreshed_data = get_edges_from_db()
            header_component = ToastFactory.get_header_by_type("info")
            return (
                refreshed_data,
                True,
                f"Table refreshed successfully - loaded {len(refreshed_data)} edges",
                header_component,
                "toast-info",
            )
        except Exception as e:
            header_component = ToastFactory.get_header_by_type("danger")
            return no_update, True, f"Error refreshing data: {str(e)}", header_component, "toast-danger"
    return no_update, no_update, no_update, no_update, no_update
