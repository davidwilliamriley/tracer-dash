# views/networks_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_tabulator
from typing import List, Dict, Any
import json


class NetworkView:
    """View layer for networks page - handles UI layout and components"""

    def __init__(self):
        pass

    @staticmethod
    def _create_toast() -> dbc.Toast:
        return dbc.Toast(
            id="networks-toast-message",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            style={
                "position": "fixed",
                "bottom": 20,
                "left": 20,
                "width": 350,
                "z-index": 9999,
            },
        )

    @staticmethod
    def create_layout(networks_data: Dict[str, Any]) -> dbc.Container:
        return dbc.Container(
            [
                NetworkView._create_toast(),

                html.Div(id="cytoscape-data-div",  children=json.dumps(networks_data), style={"display": "none"}),

                html.H1([html.I(className="bi bi-bezier2 me-2"), "Network"], className="my-4 text-primary"),
                html.P("Visualise and Analyse the Network.", className="mb-4 text-muted"),

                NetworkView._create_filters(),
            ],
            style={
                "minHeight": "calc(100vh - 120px)",
                "paddingBottom": "100px",
                "display": "flex",
                "flexDirection": "column",
            },
        )

    @staticmethod
    def _create_filters() -> html.Div:
        return html.Div([
            dbc.Card([
                dbc.CardBody([

                    # First Row - Graph Root Select
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="filter-graph-select",
                                options=[
                                    {"label": "All Roots", "value": "all"},
                                    {"label": "Root 1", "value": "root1"},
                                    {"label": "Root 2", "value": "root2"},
                                    {"label": "Root 3", "value": "root3"},
                                ],
                                placeholder="Select a Graph Root Node...",
                                disabled=True
                            ),
                            width=12,
                            className="mb-3",
                        ),
                    ]),

                    # Filter Row - Element, "include", Property, Value, Apply, Reset
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="filter-element-select",
                                options=[
                                    {"label": "All Elements", "value": "all"},
                                    {"label": "Edges", "value": "edges"},
                                    {"label": "Nodes", "value": "nodes"},
                                ],
                                value="all",
                                disabled=True,
                            ),
                            width=12,
                            lg=2,
                            className="mb-3 mb-lg-0",
                        ),

                        # label
                        dbc.Col(
                            html.Div("include", className="text-center text-muted", 
                                    style={"lineHeight": "38px"}),
                            lg=1,
                            className="d-none d-lg-block",
                        ),

                        dbc.Col(
                            dbc.Select(
                                id="filter-property-select",
                                options=[{"label": "All Properties", "value": "all"}],
                                value="all",
                                disabled=True,
                            ),
                            width=12,
                            lg=2,
                            className="mb-3 mb-lg-0",
                        ),

                        dbc.Col(
                            dbc.Input(
                                id="filter-value-input",
                                placeholder="Add Search Terms",
                            ),
                            width=12,
                            lg=5,
                            className="mb-3 mb-lg-0",
                        ),

                        dbc.Col(
                            dbc.Button([html.I(className="bi bi-filter me-1"), "Apply"],
                                id="apply-element-btn",
                                outline=True,
                                color="primary",
                                size="md",
                                className="w-100",
                            ),
                            width=6,
                            lg=1,
                            className="mb-3 mb-lg-0 pe-1",
                        ),
                        
                        dbc.Col(
                            dbc.Button([html.I(className="bi bi-arrow-clockwise me-1"), "Reset"],
                                id="reset-element-btn",
                                outline=True,
                                color="secondary",
                                size="md",
                                className="w-100",
                            ),
                            width=6,
                            lg=1,
                            className="ps-1",
                        ),
                    ], className="align-items-center g-3"),
                    
                    # Layout Algorithm Row
                    dbc.Row([
                        dbc.Col(
                            dbc.Select(
                                id="layout-algorithm-select",
                                options=[
                                    {"label": "fCoSE (Force-directed)", "value": "fcose"},
                                    {"label": "Breadthfirst", "value": "breadthfirst"},
                                    {"label": "Circle", "value": "circle"},
                                    {"label": "Concentric", "value": "concentric"},
                                    {"label": "Cose (Force-directed)", "value": "cose"},
                                    {"label": "Grid", "value": "grid"},
                                ],
                                placeholder="Select a Layout Algorithm...",
                                value="fcose",
                                disabled=True
                            ),
                            width=12,
                            className="mt-3",
                        ),
                    ]),
                ]),
            ], className="mb-4"),
            
            # Network Graph Container
            NetworkView._create_cytoscape_container(),     
        ])

    @staticmethod
    def _create_cytoscape_container() -> dbc.Card:
        return dbc.Card([
            # dbc.CardHeader(html.H5("Network Graph", className="mb-0")),
                dbc.CardBody([
                        dbc.Spinner(
                            html.Div(
                                id="cytoscape-container",
                                style={
                                    "width": "100%",
                                    "height": "70vh",
                                    "border-radius": "0.375rem",
                                    "background-color": "white",
                                    "position": "relative"
                                },
                            ),
                            id="cytoscape-spinner",
                            color="primary"
                        ),
                        html.Div(id="cytoscape-trigger", style={"display": "none"})
                    ], className="p-0",  
                ),
            ], className="mb-4",
        )
    
    @staticmethod
    def get_cytoscape_client_callback() -> str:
        """Return the JavaScript code for Cytoscape client-side callback with Bootstrap blue theme"""
        return """
        function(networkDataJson, filteredValue) {
            // Parse the JSON data
            let networkData;
            try {
                networkData = JSON.parse(networkDataJson);
            } catch (e) {
                console.error('Failed to parse network data:', e);
                return window.dash_clientside.no_update;
            }
            
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
            
            // Keep all elements but identify filtered ones for highlighting
            let elements = networkData.elements;
            let filteredElementIds = new Set();
            
            if (filteredValue && filteredValue.trim()) {
                const filterValue = filteredValue.toLowerCase();
                
                // Find matching nodes
                const matchingNodes = networkData.elements.filter(ele => {
                    if (ele.group === 'nodes') {
                        return (ele.data.label && ele.data.label.toLowerCase().includes(filterValue)) ||
                               (ele.data.name && ele.data.name.toLowerCase().includes(filterValue)) ||
                               (ele.data.identifier && ele.data.identifier.toLowerCase().includes(filterValue));
                    }
                    return false;
                });
                
                // Find matching edges
                const matchingEdges = networkData.elements.filter(ele => {
                    if (ele.group === 'edges') {
                        return (ele.data.label && ele.data.label.toLowerCase().includes(filterValue)) ||
                               (ele.data.name && ele.data.name.toLowerCase().includes(filterValue)) ||
                               (ele.data.type && ele.data.type.toLowerCase().includes(filterValue));
                    }
                    return false;
                });
                
                // Collect IDs of all matching elements
                matchingNodes.forEach(node => filteredElementIds.add(node.data.id));
                matchingEdges.forEach(edge => filteredElementIds.add(edge.data.id));
            }
            
            // Initialize Cytoscape with Bootstrap blue theme
            window.cy = cytoscape({
                container: container,
                elements: elements,
                style: [
                    {
                        selector: 'node',
                        style: {
                            'background-color': '#e3f2fd',  // Light blue background
                            'border-color': '#0d6efd',      // Bootstrap primary blue
                            'border-width': '3px',
                            'height': '40px',
                            'width': '40px',
                            'label': 'data(label)',
                            'text-valign': 'top',
                            'text-halign': 'right',
                            'font-size': '12px',
                            'color': '#6c757d'              // Bootstrap secondary gray
                        }
                    },
                    {
                        selector: ':selected',
                        style: {
                            'background-color': '#0d6efd',  // Bootstrap primary blue
                            'border-color': '#0b5ed7',      // Darker blue for border
                            'border-width': '4px'
                        }
                    },
                    {
                        selector: '.connected',
                        style: {
                            'background-color': '#b3d9ff',  // Lighter blue for connected nodes
                            'border-color': '#0d6efd',      // Bootstrap primary blue
                            'border-width': '3px'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'curve-style': 'bezier',
                            'line-color': '#0d6efd',        // Bootstrap primary blue
                            'target-arrow-color': '#0d6efd',
                            'target-arrow-shape': 'triangle',
                            'width': '3px'
                        }
                    },
                    {
                        selector: 'edge[label]',
                        style: {
                            'color': '#6c757d',             // Bootstrap secondary gray
                            'font-size': '10px',
                            'label': 'data(label)',
                            'text-rotation': 'autorotate',
                            'text-background-color': 'white',
                            'text-background-opacity': 0.8
                        }
                    },
                    {
                        selector: 'edge:selected',
                        style: {
                            'line-color': '#0b5ed7',        // Darker blue for selected edges
                            'target-arrow-color': '#0b5ed7',
                            'width': '4px'
                        }
                    },
                    {
                        selector: 'edge.connected',
                        style: {
                            'line-color': '#4da6ff',        // Medium blue for connected edges
                            'target-arrow-color': '#4da6ff',
                            'width': '3px'
                        }
                    },
                    {
                        selector: '.edge-creation-source',
                        style: {
                            'border-width': 3,
                            'border-color': '#dc3545'      // Bootstrap danger red for edge creation
                        }
                    },
                    {
                        selector: '.edge-creation-preview',
                        style: {
                            'line-color': '#dc3545',       // Bootstrap danger red
                            'target-arrow-color': '#dc3545',
                            'curve-style': 'bezier',
                            'target-arrow-shape': 'triangle',
                            'width': 3,
                            'line-style': 'dashed'
                        }
                    },
                    {
                        selector: '.faded',
                        style: {
                            'opacity': 0.2,
                            'text-opacity': 0.2
                        }
                    }
                ],
                layout: {
                    name: 'fcose',
                    animate: true,
                    padding: 30,
                    randomize: true,
                    nodeRepulsion: 400000,
                    idealEdgeLength: 100,
                    avoidOverlap: true,
                    gravity: 80
                }
            });
            
            // Apply filter highlighting if filter value was provided
            if (filteredValue && filteredValue.trim() && filteredElementIds.size > 0) {
                // Clear any existing selection highlighting first
                window.cy.elements().removeClass('connected faded');
                
                // Apply filter highlighting
                const filteredElements = window.cy.elements().filter(ele => {
                    return filteredElementIds.has(ele.id());
                });
                
                if (filteredElements.length > 0) {
                    // Get neighborhood of all filtered elements
                    const neighborhood = filteredElements.neighborhood();
                    const allConnectedElements = filteredElements.union(neighborhood);
                    
                    // Add connected class to filtered elements and their neighbors
                    filteredElements.addClass('connected');
                    neighborhood.addClass('connected');
                    
                    // Fade everything else
                    window.cy.elements().difference(allConnectedElements).addClass('faded');
                    
                    // Select the filtered elements to show they are the focus
                    filteredElements.select();
                }
            }
            
            // Add selection highlighting functionality
            window.cy.on('select', 'node', function(event) {
                const selectedNode = event.target;
                
                // Only apply selection highlighting if no filter is active
                if (!filteredValue || !filteredValue.trim()) {
                    // Clear previous classes
                    window.cy.elements().removeClass('connected faded');
                    
                    // Get connected elements (neighbors + connecting edges)
                    const neighborhood = selectedNode.neighborhood();
                    const connectedElements = neighborhood.union(selectedNode);
                    
                    // Add connected class to neighbors and connecting edges
                    neighborhood.addClass('connected');
                    
                    // Fade all other elements
                    window.cy.elements().difference(connectedElements).addClass('faded');
                }
            });
            
            window.cy.on('select', 'edge', function(event) {
                const selectedEdge = event.target;
                
                // Only apply selection highlighting if no filter is active
                if (!filteredValue || !filteredValue.trim()) {
                    // Clear previous classes
                    window.cy.elements().removeClass('connected faded');
                    
                    // Get source and target nodes
                    const sourceNode = selectedEdge.source();
                    const targetNode = selectedEdge.target();
                    const connectedNodes = sourceNode.union(targetNode);
                    
                    // Add connected class to source and target nodes
                    connectedNodes.addClass('connected');
                    
                    // Fade all other elements except selected edge and connected nodes
                    const connectedElements = connectedNodes.union(selectedEdge);
                    window.cy.elements().difference(connectedElements).addClass('faded');
                }
            });
            
            // Clear highlighting when nothing is selected (only if no filter is active)
            window.cy.on('unselect', function(event) {
                // Check if anything is still selected and no filter is active
                if (window.cy.$(':selected').length === 0 && (!filteredValue || !filteredValue.trim())) {
                    window.cy.elements().removeClass('connected faded');
                }
            });
            
            // Background tap behavior
            window.cy.on('tap', function(event) {
                if (event.target === window.cy) {
                    if (filteredValue && filteredValue.trim()) {
                        // If filter is active, just unselect but keep filter highlighting
                        window.cy.elements().unselect();
                    } else {
                        // If no filter, clear everything
                        window.cy.elements().unselect();
                        window.cy.elements().removeClass('connected faded');
                    }
                }
            });
            
            // Add context menu functionality
            window.cy.on('cxttap', 'node', function(event) {
                event.preventDefault();
                const node = event.target;
                const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
                
                // Show context menu for nodes
                showContextMenu(renderedPosition.x, renderedPosition.y, [
                    {
                        label: 'Show ID',
                        action: () => {
                            showModal(
                                'Node ID',
                                `<p class="mb-0">ID: <strong>${node.data('id')}</strong></p>`
                            );
                        }
                    },
                    {
                        label: 'Show Label',
                        action: () => {
                            showModal(
                                'Node Label',
                                `<p class="mb-0">Label: <strong>${node.data('label') || 'No label'}</strong></p>`
                            );
                        }
                    },
                    {
                        label: 'Show Properties',
                        action: () => {
                            const nodeData = node.data();
                            const formattedData = Object.entries(nodeData).map(([key, value]) => {
                                return `<tr>
                                    <td class="fw-bold">${key}</td>
                                    <td>${typeof value === 'object' ? JSON.stringify(value) : value}</td>
                                </tr>`;
                            }).join('');
                            
                            showModal(
                                'Node Properties',
                                `<div class="table-responsive">
                                    <table class="table table-striped table-hover">
                                        <thead class="table-primary">
                                            <tr>
                                                <th>Property</th>
                                                <th>Value</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${formattedData}
                                        </tbody>
                                    </table>
                                </div>`,
                                'modal-lg'
                            );
                        }
                    },
                    {
                        label: 'Delete Node',
                        action: () => {
                            node.remove();
                            console.log('Node deleted');
                        }
                    }
                ]);
                
                return false;
            });
            
            // Edge context menu
            window.cy.on('cxttap', 'edge', function(event) {
                event.preventDefault();
                const edge = event.target;
                const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
                
                showContextMenu(renderedPosition.x, renderedPosition.y, [
                    {
                        label: 'Show Edge Info',
                        action: () => {
                            const source = edge.source().data('label') || edge.source().data('id');
                            const target = edge.target().data('label') || edge.target().data('id');
                            const edgeData = edge.data();
                            
                            let edgeInfoContent = `
                                <div class="d-flex justify-content-center mb-3">
                                    <div class="text-center p-3 border rounded bg-light">
                                        <div class="fw-bold text-primary">${source}</div>
                                        <i class="bi bi-arrow-down text-primary fs-3"></i>
                                        <div class="fw-bold text-primary">${target}</div>
                                    </div>
                                </div>
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead class="table-primary">
                                            <tr>
                                                <th>Property</th>
                                                <th>Value</th>
                                            </tr>
                                        </thead>
                                        <tbody>`;
                            
                            for (const [key, value] of Object.entries(edgeData)) {
                                if (key !== 'source' && key !== 'target') {
                                    edgeInfoContent += `
                                        <tr>
                                            <td class="fw-bold">${key}</td>
                                            <td>${typeof value === 'object' ? JSON.stringify(value) : value}</td>
                                        </tr>`;
                                }
                            }
                            
                            edgeInfoContent += `
                                        </tbody>
                                    </table>
                                </div>`;
                            
                            showModal('Edge Information', edgeInfoContent, 'modal-lg');
                        }
                    },
                    {
                        label: 'Delete Edge',
                        action: () => {
                            edge.remove();
                            console.log('Edge deleted');
                        }
                    }
                ]);
                
                return false;
            });
            
            // Background context menu
            window.cy.on('cxttap', function(event) {
                if (event.target === window.cy) {
                    event.preventDefault();
                    const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
                    
                    showContextMenu(renderedPosition.x, renderedPosition.y, [
                        {
                            label: 'Add Node',
                            action: () => {
                                const id = 'node-' + Date.now();
                                window.cy.add({
                                    group: 'nodes',
                                    data: { id, label: 'New Node' },
                                    position: event.position
                                });
                                console.log('Node added');
                            }
                        },
                        {
                            label: 'Reset View',
                            action: () => {
                                window.cy.fit();
                                console.log('View reset');
                            }
                        },
                        {
                            label: 'Show Network Info',
                            action: () => {
                                const nodes = window.cy.nodes().length;
                                const edges = window.cy.edges().length;
                                
                                const statsContent = `
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="card border-primary">
                                                <div class="card-body">
                                                    <h5 class="card-title text-primary">Network Statistics</h5>
                                                    <ul class="list-group list-group-flush">
                                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                                            Nodes
                                                            <span class="badge bg-primary rounded-pill">${nodes}</span>
                                                        </li>
                                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                                            Edges
                                                            <span class="badge bg-primary rounded-pill">${edges}</span>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="card border-info">
                                                <div class="card-body">
                                                    <h5 class="card-title text-info">Network Overview</h5>
                                                    <p>This network visualization displays the relationships between different entities.</p>
                                                    <div class="alert alert-info">
                                                        <i class="bi bi-info-circle-fill me-2"></i>
                                                        Right-click on nodes or edges to see more options.
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>`;
                                
                                showModal('Network Information', statsContent, 'modal-lg');
                            }
                        }
                    ]);
                    
                    return false;
                }
            });
            
            // Override browser's context menu
            container.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                return false;
            });
            
            // Helper functions for context menu and modals
            function showContextMenu(x, y, items) {
                hideContextMenu();
                
                const menu = document.createElement('div');
                menu.id = 'cytoscape-context-menu';
                menu.classList.add('dropdown-menu', 'show');
                menu.style.position = 'fixed';
                menu.style.left = `${x}px`;
                menu.style.top = `${y}px`;
                menu.style.zIndex = '10000';
                
                items.forEach(item => {
                    const menuItem = document.createElement('a');
                    menuItem.classList.add('dropdown-item');
                    menuItem.href = '#';
                    menuItem.textContent = item.label;
                    
                    menuItem.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        hideContextMenu();
                        item.action();
                    });
                    
                    menu.appendChild(menuItem);
                });
                
                document.body.appendChild(menu);
                
                // Position adjustment
                const rect = menu.getBoundingClientRect();
                if (rect.right > window.innerWidth) {
                    menu.style.left = `${x - rect.width}px`;
                }
                if (rect.bottom > window.innerHeight) {
                    menu.style.top = `${y - rect.height}px`;
                }
            }
            
            function hideContextMenu() {
                const menu = document.getElementById('cytoscape-context-menu');
                if (menu) {
                    menu.remove();
                }
            }
            
            function showModal(title, content, size = '') {
                const existingModal = document.getElementById('network-info-modal');
                if (existingModal) {
                    existingModal.remove();
                }
                
                const modalDiv = document.createElement('div');
                modalDiv.id = 'network-info-modal';
                modalDiv.classList.add('modal', 'fade');
                modalDiv.setAttribute('tabindex', '-1');
                
                modalDiv.innerHTML = `
                    <div class="modal-dialog ${size}">
                        <div class="modal-content">
                            <div class="modal-header bg-primary text-white">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                ${content}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modalDiv);
                
                // Initialize and show the modal (assuming Bootstrap 5)
                if (typeof bootstrap !== 'undefined') {
                    const modal = new bootstrap.Modal(modalDiv);
                    modal.show();
                }
            }
            
            // Click anywhere to hide context menu
            document.addEventListener('click', hideContextMenu);
            
            return '';
        }
        """