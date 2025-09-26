# views/networks_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any

class NetworksView:
    """View layer for networks page - handles UI layout and components"""
    
    @staticmethod
    def create_layout(networks_data: Dict[str, Any]) -> html.Div:
        """Create the main layout for the networks page"""
        return html.Div([
            # Toast notification component
            NetworksView._create_toast(),
            
            # Data store for network data
            dcc.Store(id='network-data-store', data=networks_data),
            
            # Main container
            html.Div([
                NetworksView._create_visualization_section(),
            ], className="container-fluid px-4 py-5"),
            
        ])
    
    @staticmethod
    def _create_toast() -> dbc.Toast:
        """Create toast notification component"""
        return dbc.Toast(
            id="networks-toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000, 
            style={"position": "fixed", "bottom": 20, "left": 20, "width": 350, "z-index": 9999}
        )
    
    @staticmethod
    def _create_visualization_section() -> html.Div:
        """Create the network visualization section"""
        return html.Div([
            html.H4("Network Visualization", className="mb-3"),
            
            # Filter input
            html.Div([
                dbc.Input(
                    id="filter-value-input",
                    placeholder="Filter nodes by name or identifier...",
                    type="text",
                    className="mb-3"
                )
            ]),
            
            NetworksView._create_cytoscape_container(),
            
        ], className="mb-5")
    
    @staticmethod
    def _create_cytoscape_container() -> html.Div:
        """Create the cytoscape visualization container"""
        return html.Div([
            html.Div(
                id="cytoscape-container",
                style={
                    "width": "100%", 
                    "height": "60vh",
                    "border": "2px solid #dee2e6",
                    "border-radius": "0.375rem",
                    "background-color": "#f8f9fa"
                }
            )
        ], className="mb-4")
        
    @staticmethod
    def get_cytoscape_client_callback() -> str:
        """Return the JavaScript code for Cytoscape client-side callback"""
        return """
        function(networkData, filteredValue) {
            if (!networkData || !networkData.elements) {
                return window.dash_clientside.no_update;
            }
            
            // Initialize or update Cytoscape
            const container = document.getElementById('cytoscape-container');
            if (!container) {
                return window.dash_clientside.no_update;
            }
            
            // Destroy existing instance
            if (window.cy) {
                window.cy.destroy();
            }
            
            // Filter elements if filter value is provided
            let elements = networkData.elements;
            if (filteredValue && filteredValue.trim()) {
                const filterValue = filteredValue.toLowerCase();
                // Get filtered nodes
                const filteredNodes = networkData.elements.filter(ele => {
                    if (ele.group === 'nodes') {
                        return (ele.data.label && ele.data.label.toLowerCase().includes(filterValue)) ||
                               (ele.data.name && ele.data.name.toLowerCase().includes(filterValue)) ||
                               (ele.data.identifier && ele.data.identifier.toLowerCase().includes(filterValue));
                    }
                    return false;
                });
                
                // Get the IDs of filtered nodes
                const nodeIds = new Set(filteredNodes.map(node => node.data.id));
                
                // Include edges that connect filtered nodes
                const filteredEdges = networkData.elements.filter(ele => {
                    if (ele.group === 'edges') {
                        return nodeIds.has(ele.data.source) && nodeIds.has(ele.data.target);
                    }
                    return false;
                });
                
                elements = [...filteredNodes, ...filteredEdges];
            }
            
            // Initialize Cytoscape
            window.cy = cytoscape({
                container: container,
                elements: elements,
                style: [
                    {
                        selector: 'node',
                        style: {
                            'background-color': '#cbe2e1',
                            'border-color': '#00ada9',
                            'border-width': '3px',
                            'height': '40px',
                            'width': '40px',
                            'label': 'data(label)',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'font-size': '12px',
                            'color': 'gray'
                        }
                    },
                    {
                        selector: ':selected',
                        style: {
                            'background-color': '#00ada9',
                            'border-color': '#00ada9',
                            'border-width': '4px'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'curve-style': 'bezier',
                            'line-color': '#00ada9',
                            'target-arrow-color': '#00ada9',
                            'target-arrow-shape': 'triangle',
                            'width': '3px'
                        }
                    },
                    {
                        selector: 'edge[label]',
                        style: {
                            'color': 'gray',
                            'font-size': '10px',
                            'label': 'data(label)',
                            'text-rotation': 'autorotate',
                            'text-background-color': 'white',
                            'text-background-opacity': 0.8
                        }
                    }
                ],
                layout: {
                    name: 'cose',
                    animate: true,
                    padding: 30,
                    nodeRepulsion: 400000,
                    idealEdgeLength: 100,
                    avoidOverlap: true
                }
            });
            
            return '';
        }
        """