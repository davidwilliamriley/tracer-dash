# pages/breakdowns.py
import base64
import dash
from dash import callback, dcc, Input, Output, html, State, register_page, clientside_callback
import json
from typing import Dict, Any, List, Optional
from views.breakdown_view import BreakdownView, DropdownOption

# Import your real utilities
from utils.network_utils import (build_breakdown_from_graph, get_graph_roots, get_network)
from utils.pdf_utils import generate_breakdown_pdf

register_page(__name__, path="/breakdowns", name="Breakdowns", title="Tracer - Breakdowns")

breakdown_view = BreakdownView()


class BreakdownModel:
    """Real model that fetches data from NetworkX graph"""

    def __init__(self):
        self.network = None
        self._load_network()

    def _load_network(self):
        """Load the NetworkX graph from cache"""
        try:
            self.network = get_network()
            if self.network:
                print(f"Loaded network with {self.network.number_of_nodes()} nodes and {self.network.number_of_edges()} edges")
            else:
                print("Warning: No network loaded from cache")
        except Exception as e:
            print(f"Error loading network: {e}")
            self.network = None

    def refresh_network(self):
        """Reload the network from cache/database"""
        self._load_network()

    def get_breakdown_options(self) -> List[DropdownOption]:
        """Get all root nodes as dropdown options"""
        try:
            if not self.network:
                self._load_network()
            
            if not self.network:
                return []
            
            roots = get_graph_roots(self.network)
            
            options = []
            for root_id in roots:
                node_data = self.network.nodes.get(root_id, {})
                identifier = node_data.get('identifier', '')
                name = node_data.get('name', f'Root {root_id}')
                
                label = f"{identifier} - {name}" if identifier else name
                
                options.append({
                    "label": label,
                    "value": str(root_id),
                    "disabled": False,
                })
            
            print(f"Found {len(options)} root nodes")
            return sorted(options, key=lambda x: x['label'])
            
        except Exception as e:
            print(f"Error getting breakdown options: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_breakdown_data(self, root_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get hierarchical breakdown data for a specific root"""
        try:
            if not root_id:
                return []
            
            if not self.network:
                self._load_network()
            
            if not self.network:
                print("No network available")
                return []
            
            # Convert root_id to the appropriate type (try int first, then string)
            try:
                root_id_converted = int(root_id)
            except ValueError:
                root_id_converted = root_id
            
            if root_id_converted not in self.network:
                print(f"Root {root_id_converted} not found in network")
                return []
            
            # Get the breakdown using your utility function
            breakdown_data = build_breakdown_from_graph(self.network, root_node=root_id_converted)
            
            print(f"Built breakdown for root {root_id_converted}: {len(breakdown_data)} root items")
            
            # Transform to match Tabulator expected format
            return self._transform_to_tabulator_format(breakdown_data)
            
        except Exception as e:
            print(f"Error getting breakdown data for root {root_id}: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _transform_to_tabulator_format(self, breakdown_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform the breakdown data to Tabulator format with Element numbering"""
        
        def add_element_numbers(items, prefix="", level=0):
            """Recursively add element numbers like 1.0, 1.1, 1.1.1"""
            result = []
            
            for idx, item in enumerate(items, start=1):
                # Generate element number based on level
                if level == 0:
                    # Root level: 1.0, 2.0, 3.0
                    element = f"{idx}.0"
                    next_prefix = str(idx)  # For children, use just "1", "2", etc.
                elif level == 1:
                    # Second level: 1.1, 1.2, 1.3 (children of root)
                    element = f"{prefix}.{idx}"
                    next_prefix = element
                else:
                    # Third level and beyond: 1.1.1, 1.1.2, etc.
                    element = f"{prefix}.{idx}"
                    next_prefix = element
                
                # Transform the item
                transformed = {
                    "id": item.get('id'),
                    "Element": element,
                    "Relation": item.get('edge_label', item.get('edge_type', '')),
                    "Weight": str(item.get('weight', '')) if item.get('weight') else '1',
                    "Identifier": item.get('identifier', ''),
                    "Name": item.get('name', ''),
                    "Description": item.get('description', ''),
                }
                
                # Process children recursively
                children = item.get('_children', [])
                if children:
                    transformed['_children'] = add_element_numbers(children, next_prefix, level + 1)
                
                result.append(transformed)
            
            return result
        
        return add_element_numbers(breakdown_data)

    def create_new_item(self) -> Dict[str, str]:
        """Placeholder for create functionality"""
        return {"status": "success", "message": "Item created successfully"}

    def delete_items(self, items: List[Dict]) -> Dict[str, str]:
        """Placeholder for delete functionality"""
        return {"status": "success", "message": f"Deleted {len(items)} items"}

    def export_data(self, format_type: str = "json") -> Dict[str, Any]:
        """Placeholder for export functionality"""
        return {"status": "success", "message": "Export functionality coming soon"}


class BreakdownController:
    def __init__(self, model=None):
        self.model = model or BreakdownModel()
        self.view = BreakdownView()

    def get_layout(self):
        breakdown_options = self.model.get_breakdown_options()
        return self.view.create_layout(breakdown_options)

    def get_breakdown_data(self, root_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get breakdown data from the model"""
        return self.model.get_breakdown_data(root_id)

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
    prevent_initial_call=False
)
def update_table_data(selected_graph: Optional[str], refresh_clicks: Optional[int]):
    """Update the data that will be used by Tabulator"""
    print(f"update_table_data called: selected_graph={selected_graph}, refresh_clicks={refresh_clicks}")
    
    # If refresh button was clicked, reload the network
    ctx = dash.callback_context
    if ctx.triggered and 'refresh-nodes-btn' in ctx.triggered[0]['prop_id']:
        print("Refreshing network from database...")
        breakdown_controller.model.refresh_network()
    
    if not selected_graph:
        return json.dumps([])
    
    try:
        filtered_data = breakdown_controller.get_breakdown_data(selected_graph)
        print(f"Loaded {len(filtered_data)} root items for graph {selected_graph}")
        
        # Pretty print first item for debugging
        if filtered_data:
            import pprint
            print("First item structure:")
            pprint.pprint(filtered_data[0], depth=3)
        
        return json.dumps(filtered_data)
    except Exception as e:
        print(f"Error in update_table_data: {e}")
        import traceback
        traceback.print_exc()
        return json.dumps([])


@callback(
    Output("breakdown-dropdown", "options"), 
    [Input("breakdown-dropdown", "id"), Input("refresh-nodes-btn", "n_clicks")],
)
def populate_graph_options(_: str, refresh_clicks: Optional[int]):
    """Populate graph dropdown options"""
    # If refresh button was clicked, reload options
    ctx = dash.callback_context
    if ctx.triggered and 'refresh-nodes-btn' in ctx.triggered[0]['prop_id']:
        breakdown_controller.model.refresh_network()
    
    options = breakdown_controller.get_graph_options()
    print(f"Loaded {len(options)} breakdown options")
    return options


@callback(
    Output("row-info", "children"),
    [Input("breakdown-dropdown", "value"), Input("refresh-nodes-btn", "n_clicks")],
    prevent_initial_call=False
)
def update_row_info(selected_graph: Optional[str], refresh_clicks: Optional[int]):
    """Update the row information display"""
    if not selected_graph:
        return "Select a Breakdown to view the Data"
    
    try:
        filtered_data = breakdown_controller.get_breakdown_data(selected_graph)
        total_roots = len(filtered_data)
        
        # Count total nodes including children
        def count_all_nodes(items):
            count = len(items)
            for item in items:
                if item.get('_children'):
                    count += count_all_nodes(item['_children'])
            return count
        
        total_nodes = count_all_nodes(filtered_data) if filtered_data else 0
        
        return (
            "No data available" if total_roots == 0 
            else f"Loaded {total_roots} Root item(s) for Total of {total_nodes} Nodes"
        )
    except Exception as e:
        print(f"Error in update_row_info: {e}")
        return "Error loading data"


@callback(
    Output("breakdown-dropdown", "value"),
    Input("reset-filter-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_dropdown(n_clicks: Optional[int]):
    """Reset the breakdown dropdown"""
    if n_clicks:
        return None
    return dash.no_update

# Add this callback for the Print button
@callback(
    Output("download-pdf", "data"),
    Input("print-nodes-btn", "n_clicks"),
    State("breakdown-dropdown", "value"),
    State("table-data-store", "children"),
    prevent_initial_call=True,
)
def handle_print_pdf(n_clicks: Optional[int], selected_graph: Optional[str], table_data_json: Optional[str]):
    """Handle PDF print button clicks"""
    if not n_clicks or not table_data_json:
        return None
    
    try:
        data = json.loads(table_data_json)
        
        if not data:
            return None
        
        # Get the graph name for the title
        graph_options = breakdown_controller.get_graph_options()
        graph_name = "Breakdown"
        for opt in graph_options:
            if opt['value'] == selected_graph:
                graph_name = opt['label']
                break
        
        # Generate PDF
        pdf_result = generate_breakdown_pdf(
            data=data,
            title=f"Breakdown: {graph_name}",
            filename=f"breakdown_{selected_graph}"
        )
        
        # Return as dict for dcc.Download
        return {
            "content": pdf_result['content'],
            "filename": pdf_result['filename'],
            "base64": True
        }
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return None
    
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
            container.innerHTML = '<div class="text-center py-4 text-muted">No available Data. Select an Option to view the Breakdown.</div>';
            return "table-empty";
        }
        
        try {
            const table = new Tabulator("#tabulator-table", {
                data: data,
                layout: "fitDataStretch",
                dataTree: true,
                dataTreeStartExpanded: true,
                dataTreeChildField: "_children",
                dataTreeElementColumn: "Element",
                // height: "600px",
                pagination: "local",
                paginationSize: 25,
                columns: [
                    {title: "Element", field: "Element", headerFilter: "input"},
                    {title: "Edge Type", field: "Relation", headerFilter: "input"},
                    {title: "Weight", field: "Weight", headerFilter: "input", hozAlign: "center"},
                    {title: "Identifier", field: "Identifier", headerFilter: "input"},
                    {title: "Name", field: "Name", headerFilter: "input"},
                    {title: "Description", field: "Description", headerFilter: "input", minWidth: 250}
                ],
                rowClick: function(e, row) {
                    console.log("Row clicked:", row.getData());
                }
            });
            
            window.tabulatorTable = table;
            
            console.log('Tabulator table loaded successfully');
            
            return "table-loaded";
            
        } catch (error) {
            console.error('Error initializing Tabulator:', error);
            container.innerHTML = '<div class="text-center py-4 text-danger">Error loading table: ' + error.message + '</div>';
            return "table-error";
        }
    }
    """,
    Output("tabulator-table", "data-status"),
    Input("table-data-store", "children"),
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
def handle_create_click(n_clicks: Optional[int]):
    """Handle create button clicks"""
    if n_clicks and n_clicks > 0:
        result = breakdown_controller.model.create_new_item()
        if result.get("status") == "success":
            return True, result.get("message"), "Success"
        return True, result.get("message", "An error occurred"), "Error"
    return False, "", ""