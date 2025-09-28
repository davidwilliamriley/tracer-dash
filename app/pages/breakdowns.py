# breakdowns.py

from typing import Dict, Any, Optional, List
import pandas as pd
import dash
from dash import callback, Input, Output, State, html, register_page, clientside_callback
import json

# MVC Imports
from views.breakdowns_view import BreakdownView

# Enhanced sample data for testing
sample_data = [
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
                        "Description": "Sub-component of procedure 001"
                    }
                ]
            },
            {
                "id": 4,
                "Element": "1.02",
                "Relation": "includes_procedure",
                "Weight": "1",
                "Identifier": "SRL-WPF-XPA-NAP-PRC-XSE-PWD-N002",
                "Name": "Acceptance Verification Procedure [002]",
                "Description": "Secondary procedure verification"
            }
        ]
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
                "Description": "Primary safety management procedure"
            }
        ]
    }
]

class MockModel:
    """Mock model for testing - replace with your actual model"""
    def get_data(self):
        return sample_data
    
    def get_graph_options(self):
        return [
            {"label": "Acceptance Verification Procedures (AVP)", "value": "avp"},
            {"label": "Safety Management Procedures (SMP)", "value": "smp"},
            {"label": "All Procedures", "value": "all"}
        ]
    
    def filter_by_graph(self, graph_type):
        if graph_type == "avp":
            return [item for item in sample_data if "AVP" in item.get("Name", "")]
        elif graph_type == "smp":
            return [item for item in sample_data if "SMP" in item.get("Name", "")]
        else:
            return sample_data
    
    def create_new_item(self):
        return {"status": "success", "message": "Item created successfully"}
    
    def refresh_data(self):
        return sample_data
    
    def delete_items(self, items):
        return {"status": "success", "message": f"Deleted {len(items)} items"}
    
    def export_data(self, format_type="json"):
        if format_type == "json":
            return {"status": "success", "data": sample_data, "format": "json"}
        elif format_type == "csv":
            return {"status": "success", "data": "csv_data_here", "format": "csv"}

class BreakdownController:   
    def __init__(self, model=None):
        self.model = model or MockModel()
        self.view = BreakdownView()
    
    def get_layout(self):
        """Get the layout from the view"""
        layout = self.view.create_layout()
        # Add a hidden div to store data for clientside callbacks
        if layout and hasattr(layout, 'children') and layout.children is not None:
            layout.children.append(
                html.Div(id="table-data-store", style={"display": "none"})
            )
        return layout
    
    def get_breakdown_data(self) -> List[Dict[str, Any]]:
        """Get breakdown data from the model"""
        return self.model.get_data()
    
    def get_graph_options(self) -> List[Dict[str, str]]:
        """Get available graph options from the model"""
        return self.model.get_graph_options()

# Create the controller instance
breakdown_controller = BreakdownController()

# Register the page with Dash
register_page(
    __name__,
    path="/breakdowns",
    name="Breakdowns", 
    title="Tracer - Breakdowns"
)

# Create the layout variable that Dash expects for auto-discovery
layout = breakdown_controller.get_layout()

# Server-side callback to provide data to clientside callbacks
@callback(
    Output("table-data-store", "children"),
    [Input("graph-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
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
    function(data_json, page_size) {
        if (!data_json) {
            return window.dash_clientside.no_update;
        }
        
        let data;
        try {
            data = JSON.parse(data_json);
        } catch (e) {
            console.error('Failed to parse data:', e);
            return window.dash_clientside.no_update;
        }
        
        if (typeof Tabulator === 'undefined') {
            console.error('Tabulator library not loaded');
            return window.dash_clientside.no_update;
        }
        
        // Clear existing table
        const container = document.getElementById('tabulator-table');
        if (container) {
            container.innerHTML = '';
        }
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div class="text-center py-4 text-muted">No data available for selected graph</div>';
            return window.dash_clientside.no_update;
        }
        
        // Initialize Tabulator
        try {
            const table = new Tabulator("#tabulator-table", {
                data: data,
                layout: "fitColumns",
                dataTree: true,
                dataTreeStartExpanded: false,
                dataTreeChildField: "_children",
                height: "500px",
                pagination: "local",
                paginationSize: page_size || 10,
                selectable: true,
                columns: [
                    {
                        title: "", 
                        field: "select", 
                        formatter: "rowSelection", 
                        titleFormatter: "rowSelection", 
                        hozAlign: "center", 
                        headerSort: false, 
                        width: 40
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
                },
                tableBuilt: function() {
                    // Update row count when table is built
                    setTimeout(function() {
                        const totalRows = table.getDataCount();
                        const rowInfo = document.getElementById('row-info');
                        if (rowInfo) {
                            rowInfo.textContent = `Showing ${totalRows} rows`;
                        }
                    }, 100);
                }
            });
            
            // Store table reference globally
            window.tabulatorTable = table;
            
        } catch (error) {
            console.error('Error initializing Tabulator:', error);
            container.innerHTML = '<div class="text-center py-4 text-danger">Error loading table</div>';
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("tabulator-table", "className"),
    [Input("table-data-store", "children"),
     Input("page-size-dropdown", "value")]
)

# Clientside callback for page size updates
clientside_callback(
    """
    function(page_size) {
        if (window.tabulatorTable && page_size) {
            try {
                window.tabulatorTable.setPageSize(page_size);
            } catch (error) {
                console.error('Error updating page size:', error);
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("page-size-dropdown", "style"),
    Input("page-size-dropdown", "value")
)

# Server-side callbacks
@callback(
    Output("graph-dropdown", "options"),
    Input("graph-dropdown", "id")
)
def update_graph_options(_):
    """Update graph dropdown options"""
    return breakdown_controller.get_graph_options()

@callback(
    Output("row-info", "children"),
    [Input("graph-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_row_info(selected_graph, refresh_clicks):
    """Update the row information display"""
    if selected_graph:
        filtered_data = breakdown_controller.model.filter_by_graph(selected_graph)
    else:
        filtered_data = breakdown_controller.get_breakdown_data()
    
    total_rows = len(filtered_data)
    if total_rows == 0:
        return "No rows to display"
    
    return f"Loaded {total_rows} root items"

@callback(
    [Output("create-btn", "color"),
     Output("create-btn", "children")],
    Input("create-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_create_click(n_clicks):
    """Handle create button clicks"""
    if n_clicks and n_clicks > 0:
        result = breakdown_controller.model.create_new_item()
        if result and result.get("status") == "success":
            return "success", [html.I(className="bi bi-check-circle"), " Created"]
        else:
            return "danger", [html.I(className="bi bi-x-circle"), " Error"]
    return "primary", [html.I(className="bi bi-plus-circle"), " Create"]

@callback(
    [Output("delete-btn", "color"),
     Output("delete-btn", "children")],
    Input("delete-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_delete_click(n_clicks):
    """Handle delete button clicks"""
    if n_clicks and n_clicks > 0:
        selected_items = []  # This would come from the clientside callback
        result = breakdown_controller.model.delete_items(selected_items)
        if result and result.get("status") == "success":
            return "success", [html.I(className="bi bi-check-circle"), " Deleted"]
        else:
            return "danger", [html.I(className="bi bi-x-circle"), " Error"]
    return "warning", [html.I(className="bi bi-trash"), " Delete"]

@callback(
    Output("download-btn", "children"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_download_click(n_clicks):
    """Handle download button clicks"""
    if n_clicks and n_clicks > 0:
        result = breakdown_controller.model.export_data()
        if result and result.get("status") == "success":
            return [html.I(className="bi bi-check-circle"), " Downloaded"]
        else:
            return [html.I(className="bi bi-x-circle"), " Error"]
    return [html.I(className="bi bi-download"), " Download"]