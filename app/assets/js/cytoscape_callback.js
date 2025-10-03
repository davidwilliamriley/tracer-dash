// assets/js/cytoscape_callback.js
// Cytoscape client-side callback for network visualization

window.cytoscapeCallback = function(networkDataJson, filteredValue) {
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
    
    // Get container center position
    const containerRect = container.getBoundingClientRect();
    const centerX = containerRect.width / 2;
    const centerY = containerRect.height / 2;
    
    // Set all nodes to start at center with zero opacity
    elements.forEach(ele => {
        if (ele.group === 'nodes') {
            ele.position = { x: centerX, y: centerY };
            ele.style = { opacity: 0 };
        } else if (ele.group === 'edges') {
            ele.style = { opacity: 0 };
        }
    });
    
    // Initialize Cytoscape with preset layout first (simpler, more compatible)
    window.cy = cytoscape({
        container: container,
        elements: elements,
        style: getCytoscapeStyles(),
        layout: {
            name: 'preset',
            animate: false
        }
    });

    // Then run fcose after initialization
    setTimeout(() => {
        const layoutConfig = {
            name: 'fcose',
            quality: 'default',
            randomize: true,
            animate: true,
            animationDuration: 1000,
            animationEasing: 'ease-out',
            fit: true,
            padding: 30,
            nodeSeparation: 75,
            idealEdgeLength: 100,
            edgeElasticity: 0.45,
            nestingFactor: 0.1,
            gravity: 0.25,
            numIter: 2500,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        };
        
        const layout = window.cy.layout(layoutConfig);
        layout.run();
            
        // Fade in elements as they animate to position
        window.cy.nodes().animate({
            style: { opacity: 1 },
            duration: 800,
            easing: 'ease-in'
        });
        
        window.cy.edges().animate({
            style: { opacity: 1 },
            duration: 1000,
            easing: 'ease-in'
        });
    }, 100);
    
    // Apply filter highlighting after layout completes
    setTimeout(() => {
        if (filteredValue && filteredValue.trim() && filteredElementIds.size > 0) {
            applyFilterHighlighting(filteredElementIds);
        }
    }, 1200);
    
    // Setup event handlers
    setupEventHandlers(filteredValue);
    setupContextMenus();
    
    // Override browser's context menu
    container.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        return false;
    });
    
    return '';
};

// Cytoscape styles configuration
function getCytoscapeStyles() {
    return [
        {
            selector: 'node',
            style: {
                'background-color': '#e3f2fd',
                'border-color': '#0d6efd',
                'border-width': '3px',
                'height': '40px',
                'width': '40px',
                'label': 'data(label)',
                'text-valign': 'top',
                'text-halign': 'right',
                'font-size': '12px',
                'color': '#6c757d',
                'opacity': 1
            }
        },
        {
            selector: ':selected',
            style: {
                'background-color': '#0d6efd',
                'border-color': '#0b5ed7',
                'border-width': '4px'
            }
        },
        {
            selector: '.connected',
            style: {
                'background-color': '#b3d9ff',
                'border-color': '#0d6efd',
                'border-width': '3px'
            }
        },
        {
            selector: 'edge',
            style: {
                'curve-style': 'bezier',
                'line-color': '#0d6efd',
                'target-arrow-color': '#0d6efd',
                'target-arrow-shape': 'triangle',
                'width': '3px',
                'opacity': 1
            }
        },
        {
            selector: 'edge[label]',
            style: {
                'color': '#6c757d',
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
                'line-color': '#0b5ed7',
                'target-arrow-color': '#0b5ed7',
                'width': '4px'
            }
        },
        {
            selector: 'edge.connected',
            style: {
                'line-color': '#4da6ff',
                'target-arrow-color': '#4da6ff',
                'width': '3px'
            }
        },
        {
            selector: '.faded',
            style: {
                'opacity': 0.2,
                'text-opacity': 0.2
            }
        }
    ];
}

// Apply filter highlighting
function applyFilterHighlighting(filteredElementIds) {
    window.cy.elements().removeClass('connected faded');
    
    const filteredElements = window.cy.elements().filter(ele => {
        return filteredElementIds.has(ele.id());
    });
    
    if (filteredElements.length > 0) {
        const neighborhood = filteredElements.neighborhood();
        const allConnectedElements = filteredElements.union(neighborhood);
        
        filteredElements.addClass('connected');
        neighborhood.addClass('connected');
        window.cy.elements().difference(allConnectedElements).addClass('faded');
        filteredElements.select();
    }
}

// Setup event handlers
function setupEventHandlers(filteredValue) {
    // Node selection
    window.cy.on('select', 'node', function(event) {
        const selectedNode = event.target;
        
        if (!filteredValue || !filteredValue.trim()) {
            window.cy.elements().removeClass('connected faded');
            const neighborhood = selectedNode.neighborhood();
            const connectedElements = neighborhood.union(selectedNode);
            neighborhood.addClass('connected');
            window.cy.elements().difference(connectedElements).addClass('faded');
        }
    });
    
    // Edge selection
    window.cy.on('select', 'edge', function(event) {
        const selectedEdge = event.target;
        
        if (!filteredValue || !filteredValue.trim()) {
            window.cy.elements().removeClass('connected faded');
            const sourceNode = selectedEdge.source();
            const targetNode = selectedEdge.target();
            const connectedNodes = sourceNode.union(targetNode);
            connectedNodes.addClass('connected');
            const connectedElements = connectedNodes.union(selectedEdge);
            window.cy.elements().difference(connectedElements).addClass('faded');
        }
    });
    
    // Unselect
    window.cy.on('unselect', function(event) {
        if (window.cy.$(':selected').length === 0 && (!filteredValue || !filteredValue.trim())) {
            window.cy.elements().removeClass('connected faded');
        }
    });
    
    // Background tap
    window.cy.on('tap', function(event) {
        if (event.target === window.cy) {
            if (filteredValue && filteredValue.trim()) {
                window.cy.elements().unselect();
            } else {
                window.cy.elements().unselect();
                window.cy.elements().removeClass('connected faded');
            }
        }
    });
}

// Setup context menus
function setupContextMenus() {
    // Node context menu
    window.cy.on('cxttap', 'node', function(event) {
        event.preventDefault();
        const node = event.target;
        const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
        
        showContextMenu(renderedPosition.x, renderedPosition.y, [
            {
                label: 'Show ID',
                action: () => {
                    showModal('Node ID', `<p class="mb-0">ID: <strong>${node.data('id')}</strong></p>`);
                }
            },
            {
                label: 'Show Label',
                action: () => {
                    showModal('Node Label', `<p class="mb-0">Label: <strong>${node.data('label') || 'No label'}</strong></p>`);
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
                                    <tr><th>Property</th><th>Value</th></tr>
                                </thead>
                                <tbody>${formattedData}</tbody>
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
                                    <tr><th>Property</th><th>Value</th></tr>
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
                    
                    edgeInfoContent += `</tbody></table></div>`;
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
                                                    Nodes <span class="badge bg-primary rounded-pill">${nodes}</span>
                                                </li>
                                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                                    Edges <span class="badge bg-primary rounded-pill">${edges}</span>
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
}

// Helper: Show context menu
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

// Helper: Hide context menu
function hideContextMenu() {
    const menu = document.getElementById('cytoscape-context-menu');
    if (menu) {
        menu.remove();
    }
}

// Helper: Show modal
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
                <div class="modal-body">${content}</div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modalDiv);
    
    if (typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalDiv);
        modal.show();
    }
}

// Click anywhere to hide context menu
document.addEventListener('click', hideContextMenu);