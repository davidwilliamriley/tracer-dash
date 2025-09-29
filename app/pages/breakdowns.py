# pages / breakdowns.py

from typing import Dict, Any, List
import json
import dash
from dash import callback, Input, Output, html, register_page, clientside_callback
from views.breakdown_view import BreakdownView, DropdownOption

register_page(__name__, path="/breakdowns", name="Breakdowns", title="Tracer - Breakdowns")

breakdown_view = BreakdownView()

SAMPLE_DATA = [
    {
        "id": 1,
        "Element": "1.0",
        "Relation": "",
        "Weight": "",
        "Identifier": "",
        "Name": "Acceptance Verification Procedures (AVP)",
        "Description": "Root Node for AVR Register",
        "_children": [
            {
                "id": 2,
                "Element": "1.01",
                "Relation": "includes_procedure",
                "Weight": "1",
                "Identifier": "SRL-WPF-XPA-NAP-PRC-XSE-PWD-N001",
                "Name": "Acceptance Verification Procedure [001]",
                "Description": "Initial procedure verification",
                "_children": [
                    {
                        "id": 3,
                        "Element": "1.01.01",
                        "Relation": "sub_procedure",
                        "Weight": "0.5",
                        "Identifier": "SRL-WPF-XPA-NAP-PRC-XSE-PWD-N001-A",
                        "Name": "Sub-procedure A",
                        "Description": "Sub-component of procedure 001",
                    }
                ],
            },
            {
                "id": 4,
                "Element": "1.02",
                "Relation": "includes_procedure",
                "Weight": "1",
                "Identifier": "SRL-WPF-XPA-NAP-PRC-XSE-PWD-N002",
                "Name": "Acceptance Verification Procedure [002]",
                "Description": "Secondary procedure verification",
            },
        ],
    },
    {
        "id": 5,
        "Element": "2.0",
        "Relation": "",
        "Weight": "",
        "Identifier": "",
        "Name": "Safety Management Procedures (SMP)",
        "Description": "Root Node for Safety Management",
        "_children": [
            {
                "id": 6,
                "Element": "2.01",
                "Relation": "includes_safety",
                "Weight": "2",
                "Identifier": "SRL-WPF-XPA-NAP-SMP-XSE-PWD-S001",
                "Name": "Safety Management Procedure [001]",
                "Description": "Primary safety management procedure",
            }
        ],
    },
]


class MockModel:
    """Mock model for testing - replace with your actual model"""

    def get_data(self) -> List[Dict[str, Any]]:
        return SAMPLE_DATA

    def get_breakdown_options(self) -> List[DropdownOption]:
        return [
            {
                "label": "Acceptance Verification Procedures (AVP)",
                "value": "avp",
                "disabled": False,
            },
            {
                "label": "Safety Management Procedures (SMP)",
                "value": "smp",
                "disabled": False,
            },
            {"label": "All Procedures", "value": "all", "disabled": False},
        ]

    def filter_by_graph(self, graph_type: str) -> List[Dict[str, Any]]:
        if graph_type == "avp":
            return [item for item in SAMPLE_DATA if "AVP" in item.get("Name", "")]
        elif graph_type == "smp":
            return [item for item in SAMPLE_DATA if "SMP" in item.get("Name", "")]
        return SAMPLE_DATA

    def create_new_item(self) -> Dict[str, str]:
        return {"status": "success", "message": "Item created successfully"}

    def delete_items(self, items: List[Dict]) -> Dict[str, str]:
        return {"status": "success", "message": f"Deleted {len(items)} items"}

    def export_data(self, format_type: str = "json") -> Dict[str, Any]:
        if format_type == "json":
            return {"status": "success", "data": SAMPLE_DATA, "format": "json"}
        elif format_type == "csv":
            return {"status": "success", "data": "csv_data_here", "format": "csv"}
        return {"status": "error", "message": "Unknown format"}


class BreakdownController:
    def __init__(self, model=None):
        self.model = model or MockModel()
        self.view = BreakdownView()

    def get_layout(self):
        breakdown_options = self.model.get_breakdown_options()
        return self.view.create_layout(breakdown_options)

    def get_breakdown_data(self) -> List[Dict[str, Any]]:
        """Get breakdown data from the model"""
        return self.model.get_data()

    def get_graph_options(self) -> List[DropdownOption]:
        """Get available graph options from the model"""
        return self.model.get_breakdown_options()

# Create the controller instance
breakdown_controller = BreakdownController()

# Create the layout variable that Dash expects for auto-discovery
layout = breakdown_controller.get_layout()

# Callbacks
@callback(
    Output("table-data-store", "children"),
    [Input("breakdown-dropdown", "value"), Input("refresh-nodes-btn", "n_clicks")],
)
def update_table_data(selected_graph, refresh_clicks):
    """Update the data that will be used by Tabulator"""
    if selected_graph:
        filtered_data = breakdown_controller.model.filter_by_graph(selected_graph)
    else:
        filtered_data = breakdown_controller.get_breakdown_data()

    return json.dumps(filtered_data)


# Clientside callback to initialize Tabulator
clientside_callback(
    """
    function(dataJson) {
        if (!dataJson) {
            return window.dash_clientside.no_update;
        }
        
        let data;
        try {
            data = JSON.parse(dataJson);
        } catch (e) {
            console.error('Failed to parse data:', e);
            return window.dash_clientside.no_update;
        }
        
        if (typeof Tabulator === 'undefined') {
            console.error('Tabulator library not loaded');
            return window.dash_clientside.no_update;
        }
        
        const container = document.getElementById('tabulator-table');
        if (!container) {
            console.error('Container not found');
            return window.dash_clientside.no_update;
        }
        
        container.innerHTML = '';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div class="text-center py-4 text-muted">No data available for selected graph</div>';
            return "table-empty";
        }
        
        try {
            const table = new Tabulator("#tabulator-table", {
                data: data,
                layout: "fitColumns",
                dataTree: true,
                dataTreeStartExpanded: false,
                dataTreeChildField: "_children",
                height: "500px",
                pagination: "local",
                paginationSize: 10,  // Fixed value
                selectable: true,
                columns: [
                    {
                        title: "", 
                        field: "select", 
                        formatter: "rowSelection", 
                        titleFormatter: "rowSelection", 
                        hozAlign: "center", 
                        headerSort: false, 
                        width: 60
                    },
                    {title: "Element", field: "Element", width: 100, headerFilter: "input"},
                    {title: "Relation", field: "Relation", width: 150, headerFilter: "input"},
                    {title: "Weight", field: "Weight", width: 100, headerFilter: "input"},
                    {title: "Identifier", field: "Identifier", width: 250, headerFilter: "input"},
                    {title: "Name", field: "Name", width: 300, headerFilter: "input"},
                    {title: "Description", field: "Description", headerFilter: "input", minWidth: 200}
                ],
                rowClick: function(e, row) {
                    console.log("Row clicked:", row.getData());
                }
            });
            
            window.tabulatorTable = table;
            
            // Update row count
            const totalRows = table.getDataCount();
            const rowInfo = document.getElementById('row-info');
            if (rowInfo) {
                rowInfo.textContent = `Showing ${totalRows} rows`;
            }
            
            return "table-loaded";
            
        } catch (error) {
            console.error('Error initializing Tabulator:', error);
            container.innerHTML = '<div class="text-center py-4 text-danger">Error loading table</div>';
            return "table-error";
        }
    }
    """,
    Output("tabulator-table", "data-status"),
    Input("table-data-store", "children"),  # Removed page-size-dropdown input
)


@callback(Output("breakdown-dropdown", "options"), Input("breakdown-dropdown", "id"))
def populate_graph_options(_):
    """Populate graph dropdown options"""
    return breakdown_controller.get_graph_options()


@callback(
    Output("row-info", "children"),
    [Input("breakdown-dropdown", "value"), Input("refresh-nodes-btn", "n_clicks")],
)
def update_row_info(selected_graph, refresh_clicks):
    """Update the row information display"""
    if selected_graph:
        filtered_data = breakdown_controller.model.filter_by_graph(selected_graph)
    else:
        filtered_data = breakdown_controller.get_breakdown_data()

    total_rows = len(filtered_data)
    return (
        "No rows to display" if total_rows == 0 else f"Loaded {total_rows} root items"
    )


@callback(
    [
        Output("toast-message", "is_open"),
        Output("toast-message", "children"),
        Output("toast-message", "header"),
    ],
    Input("create-node-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_create_click(n_clicks):
    """Handle create button clicks"""
    if n_clicks and n_clicks > 0:
        result = breakdown_controller.model.create_new_item()
        if result.get("status") == "success":
            return True, result.get("message"), "Success"
        return True, result.get("message", "An error occurred"), "Error"
    return False, "", ""


@callback(
    [
        Output("toast-message", "is_open", allow_duplicate=True),
        Output("toast-message", "children", allow_duplicate=True),
        Output("toast-message", "header", allow_duplicate=True),
    ],
    Input("delete-node-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_delete_click(n_clicks):
    """Handle delete button clicks"""
    if n_clicks and n_clicks > 0:
        # TODO: Get selected rows from clientside
        selected_items = []
        result = breakdown_controller.model.delete_items(selected_items)
        if result.get("status") == "success":
            return True, result.get("message"), "Success"
        return True, result.get("message", "An error occurred"), "Error"
    return False, "", ""


@callback(
    [
        Output("toast-message", "is_open", allow_duplicate=True),
        Output("toast-message", "children", allow_duplicate=True),
        Output("toast-message", "header", allow_duplicate=True),
    ],
    Input("download-nodes-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_download_click(n_clicks):
    """Handle download button clicks"""
    if n_clicks and n_clicks > 0:
        result = breakdown_controller.model.export_data()
        if result.get("status") == "success":
            return True, "Data exported successfully", "Success"
        return True, "Failed to export data", "Error"
    return False, "", ""
