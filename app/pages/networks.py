# pages/networks.py
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import networkx as nx
import json
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import joinedload

# Import View and Model
from views.network_view import NetworkView
from models.model import Model, Node, Edge
from utils.network_utils import build_networkx_from_database, get_graph_roots

# Register the Page
dash.register_page(__name__, path="/network")


def networkx_to_cytoscape(G: nx.Graph) -> dict:
    elements = []

    # Add nodes from NetworkX graph
    for node_id, node_data in G.nodes(data=True):
        # Create label: "Identifier - Name" if identifier exists, otherwise just "Name"
        identifier = node_data.get("identifier", "")
        name = node_data.get("name", "")
        if identifier and name:
            label = f"{identifier} - {name}"
        elif name:
            label = name
        elif identifier:
            label = identifier
        else:
            label = "Unnamed"

        elements.append(
            {
                "group": "nodes",
                "data": {
                    "id": str(node_id),
                    "label": label,
                    "name": name,
                    "identifier": identifier,
                    "description": node_data.get("description", ""),
                },
            }
        )

    # Add edges from NetworkX graph
    for source, target, edge_data in G.edges(data=True):
        elements.append(
            {
                "group": "edges",
                "data": {
                    "id": str(edge_data.get("edge_id", f"{source}-{target}")),
                    "identifier": edge_data.get("identifier", ""),
                    "source": str(source),
                    "label": edge_data.get("relationship_type", "connects to"),
                    "target": str(target),
                    "description": edge_data.get("description", ""),
                },
            }
        )

    return {"elements": elements}


# ==================== LAYOUT ====================


def layout():
    print("[layout] Creating network layout with empty initial data")
    return NetworkView.create_layout({"elements": []})


# ==================== CALLBACKS ====================


@callback(
    Output("filter-graph-select", "options"),
    Input("cytoscape-data-div", "id"),
    prevent_initial_call=False,
)
def update_root_selector_options(_):
    """Update the root node selector options when the graph is loaded"""
    try:
        G = build_networkx_from_database()
        root_nodes = get_graph_roots(G) if G else []

        # Create options list
        options = [{"label": "All Roots", "value": "all"}]

        if root_nodes:
            for root_id in root_nodes:
                node_data = G.nodes.get(root_id, {})
                identifier = node_data.get("identifier", "")
                name = node_data.get("name", "")
                if identifier and name:
                    label = f"{identifier} - {name}"
                elif name:
                    label = name
                elif identifier:
                    label = identifier
                else:
                    label = f"Node {root_id}"
                options.append({"label": label, "value": root_id})

        return options
    except Exception as e:
        print(f"Error updating root selector options: {e}")
        return [{"label": "All Roots", "value": "all"}]


@callback(
    Output("filter-graph-select", "disabled"),
    Input("filter-graph-select", "options"),
    prevent_initial_call=False,
)
def update_root_selector_state(options):
    """Enable/disable the root selector based on available options"""
    return len(options) <= 1  # Disable if only "All Roots" option available


@callback(
    Output("cytoscape-data-div", "children"),
    Input("cytoscape-data-div", "id"),
    prevent_initial_call=False,
)
def load_cytoscape_data(_):
    try:
        G = build_networkx_from_database()
        cytoscape_data = networkx_to_cytoscape(G) if G else {"elements": []}
        return json.dumps(cytoscape_data)
    except Exception as e:
        print(f"Error loading network: {e}")
        return json.dumps({"elements": []})


@callback(
    Output("cytoscape-data-div", "children", allow_duplicate=True),
    Input("filter-graph-select", "value"),
    prevent_initial_call=True,
)
def filter_by_root_node(selected_root):
    """Filter the network to show only the subgraph from selected root node"""
    try:
        G = build_networkx_from_database()
        if not G or not selected_root or selected_root == "all":
            # Show full graph
            cytoscape_data = networkx_to_cytoscape(G) if G else {"elements": []}
        else:
            # Filter to show only the subgraph starting from the selected root
            if selected_root in G:
                # Get all descendants of the root node
                descendants = nx.descendants(G, selected_root)
                descendants.add(selected_root)  # Include the root itself

                # Create subgraph with only these nodes
                subgraph = G.subgraph(descendants)
                cytoscape_data = networkx_to_cytoscape(subgraph)
            else:
                cytoscape_data = {"elements": []}

        return json.dumps(cytoscape_data)
    except Exception as e:
        print(f"Error filtering by root node: {e}")
        return json.dumps({"elements": []})


# Register clientside callback to trigger Cytoscape rendering
clientside_callback(
    """
    function(networkDataJson, filteredValue, layoutAlgorithm) {
        return window.cytoscapeCallback(networkDataJson, filteredValue, layoutAlgorithm);
    }
    """,
    Output("cytoscape-trigger", "children"),
    Input("cytoscape-data-div", "children"),
    State("filter-value-input", "value"),
    State("layout-algorithm-select", "value"),
    prevent_initial_call=False,
)


# Add callback to re-render when layout algorithm changes
clientside_callback(
    """
    function(layoutAlgorithm, networkDataJson, filteredValue) {
        if (layoutAlgorithm && networkDataJson) {
            // Layout changes always require full recreation
            return window.cytoscapeCallback(networkDataJson, filteredValue, layoutAlgorithm);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("cytoscape-trigger", "children", allow_duplicate=True),
    Input("layout-algorithm-select", "value"),
    State("cytoscape-data-div", "children"),
    State("filter-value-input", "value"),
    prevent_initial_call=True,
)


@callback(
    Output("network-stats-display", "children"),
    Input("cytoscape-data-div", "children"),
    prevent_initial_call=False,
)
def update_network_stats(network_data_json):
    """Update network statistics display"""
    try:
        if not network_data_json:
            return "No network data available"

        network_data = json.loads(network_data_json)
        elements = network_data.get("elements", [])

        nodes = [e for e in elements if e.get("group") == "nodes"]
        edges = [e for e in elements if e.get("group") == "edges"]

        # Calculate some basic stats
        node_count = len(nodes)
        edge_count = len(edges)

        if node_count == 0:
            return "Network: 0 nodes, 0 edges"

        # Calculate average degree (approximate)
        avg_degree = (2 * edge_count) / node_count if node_count > 0 else 0

        return f"Network: {node_count} nodes, {edge_count} edges | Avg. degree: {avg_degree:.1f}"

    except Exception as e:
        print(f"Error calculating network stats: {e}")
        return "Error calculating network statistics"


# Reset filters callback - clear the search input and refresh the network
@callback(
    [
        Output("filter-value-input", "value"),
        Output("cytoscape-trigger", "children", allow_duplicate=True),
    ],
    Input("reset-element-btn", "n_clicks"),
    State("cytoscape-data-div", "children"),
    State("layout-algorithm-select", "value"),
    prevent_initial_call=True,
)
def reset_search_filter(n_clicks, network_data_json, layout_algorithm):
    """Reset the search filter input and refresh network when reset button is clicked"""
    if n_clicks:
        # Return empty string for input and trigger network refresh with no filter
        return "", ""
    return no_update, no_update


# Callback to refresh network when filter is reset (clientside)
clientside_callback(
    """
    function(filterValue, networkDataJson, layoutAlgorithm) {
        if (networkDataJson) {
            // Use the smart callback that chooses between search-only and full recreation
            if (window.smartCytoscapeCallback) {
                // Debounce the search to avoid too many re-renders while typing
                if (window.searchTimeout) {
                    clearTimeout(window.searchTimeout);
                }
                
                return new Promise((resolve) => {
                    window.searchTimeout = setTimeout(() => {
                        const result = window.smartCytoscapeCallback(networkDataJson, filterValue || "", layoutAlgorithm);
                        resolve(result);
                    }, 300); // Reduced to 300ms for faster response
                });
            } else {
                // Fallback to original callback if smart callback not available
                return window.cytoscapeCallback(networkDataJson, filterValue || "", layoutAlgorithm);
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("cytoscape-trigger", "children", allow_duplicate=True),
    Input("filter-value-input", "value"),
    State("cytoscape-data-div", "children"),
    State("layout-algorithm-select", "value"),
    prevent_initial_call=True,
)


# Export callbacks - these use clientside callbacks to interact with the Cytoscape instance
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && window.exportNetworkPNG) {
            window.exportNetworkPNG();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-png-btn", "children", allow_duplicate=True),
    Input("export-png-btn", "n_clicks"),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && window.exportNetworkSVG) {
            window.exportNetworkSVG();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-svg-btn", "children", allow_duplicate=True),
    Input("export-svg-btn", "n_clicks"),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && window.downloadNetworkJSON) {
            window.downloadNetworkJSON();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-json-btn", "children", allow_duplicate=True),
    Input("export-json-btn", "n_clicks"),
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks && window.exportNetworkHighResPNG) {
            window.exportNetworkHighResPNG();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("export-highres-png-btn", "children", allow_duplicate=True),
    Input("export-highres-png-btn", "n_clicks"),
    prevent_initial_call=True,
)


# Add toast store component for JavaScript communication
@callback(
    [
        Output("networks-toast-message", "is_open"),
        Output("networks-toast-message", "children"),
        Output("networks-toast-message", "header"),
        Output("networks-toast-message", "icon"),
    ],
    Input("toast-store", "data"),
    prevent_initial_call=True,
)
def update_toast(toast_data):
    """Update toast based on data from JavaScript"""
    if not toast_data:
        return False, "", "Notification", None

    message_type = toast_data.get("type", "info")
    message = toast_data.get("message", "")

    # Map message types to icons and headers
    icon_map = {
        "success": "success",
        "error": "danger",
        "warning": "warning",
        "info": "info",
    }

    header_map = {
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Information",
    }

    return (
        True,
        message,
        header_map.get(message_type, "Notification"),
        icon_map.get(message_type, None),
    )
