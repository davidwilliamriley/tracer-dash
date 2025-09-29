# pages/networks.py - MVC refactored version
import dash
from dash import callback, Input, Output, State, no_update, clientside_callback, dcc
import json
from typing import Any, Dict, List

# Import MVC components
from views.networks_view import NetworksView
from controllers.networks_controller import NetworksController

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
