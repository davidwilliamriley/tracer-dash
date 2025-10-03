// assets/js/cytoscape_events.js
// Event handlers for Cytoscape network visualization

/**
 * Setup all event handlers for the Cytoscape instance
 * @param {string} filteredValue - Current filter value
 */
function setupEventHandlers(filteredValue) {
    if (!window.cy) return;
    
    setupSelectionEvents(filteredValue);
    setupUnselectionEvents(filteredValue);
    setupTapEvents(filteredValue);
}

/**
 * Setup selection event handlers
 * @param {string} filteredValue - Current filter value
 */
function setupSelectionEvents(filteredValue) {
    // Node selection
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
    
    // Edge selection
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
}

/**
 * Setup unselection event handlers
 * @param {string} filteredValue - Current filter value
 */
function setupUnselectionEvents(filteredValue) {
    // Clear highlighting when nothing is selected (only if no filter is active)
    window.cy.on('unselect', function(event) {
        // Check if anything is still selected and no filter is active
        if (window.cy.$(':selected').length === 0 && (!filteredValue || !filteredValue.trim())) {
            window.cy.elements().removeClass('connected faded');
        }
    });
}

/**
 * Setup tap/click event handlers
 * @param {string} filteredValue - Current filter value
 */
function setupTapEvents(filteredValue) {
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
    
    // Double tap on node
    window.cy.on('dbltap', 'node', function(event) {
        const node = event.target;
        // Center and zoom to node
        window.cy.animate({
            center: { eles: node },
            zoom: 2,
            duration: 500,
            easing: 'ease-in-out'
        });
    });
}

/**
 * Setup context menu handlers
 */
function setupContextMenus() {
    if (!window.cy) return;
    
    // Node context menu
    window.cy.on('cxttap', 'node', handleNodeContextMenu);
    
    // Edge context menu
    window.cy.on('cxttap', 'edge', handleEdgeContextMenu);
    
    // Background context menu
    window.cy.on('cxttap', handleBackgroundContextMenu);
    
    // Override browser's context menu
    const container = document.getElementById('cytoscape-container');
    if (container) {
        container.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            return false;
        });
    }
}

/**
 * Handle node context menu
 * @param {Object} event - Cytoscape event object
 */
function handleNodeContextMenu(event) {
    event.preventDefault();
    const node = event.target;
    const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
    
    showContextMenu(renderedPosition.x, renderedPosition.y, [
        {
            label: 'Show ID',
            action: () => {
                showModal(
                    'Node ID',
                    `<p class="mb-0">ID: <strong>${escapeHtml(node.data('id'))}</strong></p>`
                );
            }
        },
        {
            label: 'Show Label',
            action: () => {
                showModal(
                    'Node Label',
                    `<p class="mb-0">Label: <strong>${escapeHtml(node.data('label') || 'No label')}</strong></p>`
                );
            }
        },
        {
            label: 'Show Properties',
            action: () => {
                showModal(
                    'Node Properties',
                    formatNodeDataTable(node.data()),
                    'modal-lg'
                );
            }
        },
        {
            label: 'Show Neighbors',
            action: () => {
                const neighbors = node.neighborhood('node');
                const neighborInfo = neighbors.map(n => 
                    n.data('label') || n.data('id')
                ).join(', ');
                
                showModal(
                    'Node Neighbors',
                    `<p>This node has <strong>${neighbors.length}</strong> neighbors:</p>
                     <p class="text-muted">${escapeHtml(neighborInfo)}</p>`
                );
            }
        },
        {
            label: 'Center on Node',
            action: () => {
                window.cy.animate({
                    center: { eles: node },
                    zoom: 2,
                    duration: 500,
                    easing: 'ease-in-out'
                });
            }
        },
        {
            label: 'Delete Node',
            action: () => {
                if (confirm(`Delete node "${node.data('label') || node.data('id')}"?`)) {
                    node.remove();
                    console.log('Node deleted:', node.data('id'));
                }
            }
        }
    ]);
    
    return false;
}

/**
 * Handle edge context menu
 * @param {Object} event - Cytoscape event object
 */
function handleEdgeContextMenu(event) {
    event.preventDefault();
    const edge = event.target;
    const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
    
    showContextMenu(renderedPosition.x, renderedPosition.y, [
        {
            label: 'Show Edge Info',
            action: () => {
                showModal('Edge Information', formatEdgeInfo(edge), 'modal-lg');
            }
        },
        {
            label: 'Highlight Path',
            action: () => {
                // Clear previous highlights
                window.cy.elements().removeClass('highlighted');
                
                // Highlight the edge and its nodes
                const source = edge.source();
                const target = edge.target();
                edge.addClass('highlighted');
                source.addClass('highlighted');
                target.addClass('highlighted');
                
                // Center on edge
                window.cy.animate({
                    center: { eles: edge },
                    zoom: 1.5,
                    duration: 500
                });
            }
        },
        {
            label: 'Delete Edge',
            action: () => {
                if (confirm('Delete this edge?')) {
                    edge.remove();
                    console.log('Edge deleted:', edge.data('id'));
                }
            }
        }
    ]);
    
    return false;
}

/**
 * Handle background context menu
 * @param {Object} event - Cytoscape event object
 */
function handleBackgroundContextMenu(event) {
    if (event.target === window.cy) {
        event.preventDefault();
        const renderedPosition = event.renderedPosition || event.cyRenderedPosition;
        
        showContextMenu(renderedPosition.x, renderedPosition.y, [
            {
                label: 'Add Node',
                action: () => {
                    const id = 'node-' + Date.now();
                    const newNode = window.cy.add({
                        group: 'nodes',
                        data: { id, label: 'New Node' },
                        position: event.position
                    });
                    
                    // Animate the new node
                    newNode.style('opacity', 0);
                    newNode.animate({
                        style: { opacity: 1 },
                        duration: 500
                    });
                    
                    console.log('Node added:', id);
                }
            },
            {
                label: 'Reset View',
                action: () => {
                    window.cy.animate({
                        fit: { padding: 30 },
                        duration: 500,
                        easing: 'ease-in-out'
                    });
                    console.log('View reset');
                }
            },
            {
                label: 'Clear Selections',
                action: () => {
                    clearHighlighting();
                    console.log('Selections cleared');
                }
            },
            {
                label: 'Show Network Info',
                action: () => {
                    showNetworkInfoModal();
                }
            },
            {
                label: 'Export as JSON',
                action: () => {
                    downloadNetworkJSON();
                    console.log('Network exported');
                }
            }
        ]);
        
        return false;
    }
}

/**
 * Show network information modal
 */
function showNetworkInfoModal() {
    const stats = getNetworkStats();
    
    const statsContent = `
        <div class="row">
            <div class="col-md-6">
                <div class="card border-primary mb-3">
                    <div class="card-body">
                        <h5 class="card-title text-primary">
                            <i class="bi bi-graph-up me-2"></i>Network Statistics
                        </h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Total Nodes
                                <span class="badge bg-primary rounded-pill">${stats.nodes}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Total Edges
                                <span class="badge bg-primary rounded-pill">${stats.edges}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Connected Components
                                <span class="badge bg-info rounded-pill">${stats.connectedComponents}</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Average Degree
                                <span class="badge bg-success rounded-pill">${stats.averageDegree}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card border-info mb-3">
                    <div class="card-body">
                        <h5 class="card-title text-info">
                            <i class="bi bi-info-circle me-2"></i>Network Overview
                        </h5>
                        <p>This network visualization displays the relationships between different entities.</p>
                        <div class="alert alert-info mb-2">
                            <strong>Interaction Tips:</strong>
                            <ul class="mb-0 mt-2">
                                <li>Right-click on nodes or edges for options</li>
                                <li>Double-click a node to center on it</li>
                                <li>Drag nodes to reposition them</li>
                                <li>Scroll to zoom in/out</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card border-secondary">
                    <div class="card-body">
                        <h5 class="card-title text-secondary">
                            <i class="bi bi-keyboard me-2"></i>Keyboard Shortcuts
                        </h5>
                        <div class="row">
                            <div class="col-md-6">
                                <ul class="list-unstyled">
                                    <li><kbd>Ctrl+A</kbd> - Select all</li>
                                    <li><kbd>Delete</kbd> - Delete selected</li>
                                    <li><kbd>Esc</kbd> - Clear selection</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <ul class="list-unstyled">
                                    <li><kbd>Ctrl+F</kbd> - Fit to screen</li>
                                    <li><kbd>Ctrl+0</kbd> - Reset zoom</li>
                                    <li><kbd>Ctrl+S</kbd> - Export network</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;
    
    showModal('Network Information', statsContent, 'modal-xl');
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        if (!window.cy) return;
        
        // Ctrl+A - Select all
        if (event.ctrlKey && event.key === 'a') {
            event.preventDefault();
            window.cy.elements().select();
        }
        
        // Delete - Delete selected elements
        if (event.key === 'Delete') {
            const selected = window.cy.$(':selected');
            if (selected.length > 0) {
                if (confirm(`Delete ${selected.length} selected element(s)?`)) {
                    selected.remove();
                }
            }
        }
        
        // Esc - Clear selection
        if (event.key === 'Escape') {
            clearHighlighting();
        }
        
        // Ctrl+F - Fit to screen
        if (event.ctrlKey && event.key === 'f') {
            event.preventDefault();
            window.cy.fit(30);
        }
        
        // Ctrl+0 - Reset zoom
        if (event.ctrlKey && event.key === '0') {
            event.preventDefault();
            window.cy.zoom(1);
            window.cy.center();
        }
        
        // Ctrl+S - Export network
        if (event.ctrlKey && event.key === 's') {
            event.preventDefault();
            downloadNetworkJSON();
        }
    });
}

// Initialize keyboard shortcuts when the script loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupKeyboardShortcuts);
} else {
    setupKeyboardShortcuts();
}