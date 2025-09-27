# pages/networks.py - MVC refactored version
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import json
from typing import Any, Dict, List

# Import MVC components
from views.networks_view import NetworksView
from controllers.networks_controller import NetworksController
from utils.graph_cache_utils import GraphCacheUtils

# Register the page
dash.register_page(__name__, path='/networks')

# Initialize controller
controller = NetworksController()

def layout():
    """Main layout function - delegates to view"""
    # Get the visualization data (Cytoscape format) instead of raw NetworkX graph
    networks_data = controller.get_network_visualization_data()
    return NetworksView.create_layout(networks_data)

# Client-side callback for Cytoscape visualization
clientside_callback(
    NetworksView.get_cytoscape_client_callback(),
    Output('cytoscape-container', 'data-dummy'),
    [Input('network-data-store', 'data'),
     Input('filter-value-input', 'value')]
)

# Callback to manage graph cache
@callback(
    [Output('graph-cache-store', 'data'),
     Output('graph-metadata-store', 'data'),
     Output('cache-timestamp-store', 'data')],
    [Input('network-data-store', 'data')],
    [State('graph-cache-store', 'data'),
     State('graph-metadata-store', 'data'),
     State('cache-timestamp-store', 'data')]
)
def manage_graph_cache(network_data, cached_graph, cached_metadata, cached_timestamp):
    """
    Manage graph caching using dcc.Store components.
    This callback checks if we need to update the cache based on the network data.
    """
    if not network_data:
        return no_update, no_update, no_update
    
    try:
        # Check if cache is still valid
        if cached_metadata and GraphCacheUtils.is_cache_valid({'metadata': cached_metadata}, max_age_seconds=300):
            # Cache is still valid, no need to update
            return no_update, no_update, no_update
        
        # Convert Cytoscape data to NetworkX for caching
        graph = GraphCacheUtils.convert_cytoscape_to_networkx(network_data)
        
        # Serialize the graph for storage
        serialized_graph = GraphCacheUtils.serialize_networkx_graph(graph)
        
        # Create metadata
        metadata = controller.get_cache_metadata()
        
        # Update timestamp
        timestamp_data = {
            'last_updated': metadata.get('timestamp'),
            'cache_version': '1.0'
        }
        
        return serialized_graph, metadata, timestamp_data
        
    except Exception as e:
        print(f"Error in graph cache management: {e}")
        return no_update, no_update, no_update

# Note: Removed the circular dependency callback that was causing:
# "Dependency Cycle Found: network-data-store.data -> graph-cache-store.data -> network-data-store.data"
# The callback was not functional (only returned no_update) and created a circular reference.