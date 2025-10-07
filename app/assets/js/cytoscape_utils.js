// assets/js/cytoscape_utils.js
// Utility functions for Cytoscape network visualization

/**
 * Clear all highlighting and selections from the network
 */
function clearHighlighting() {
    if (!window.cy) return;
    
    window.cy.elements().unselect();
    window.cy.elements().removeClass('connected faded highlighted');
}

/**
 * Apply filter highlighting to specified elements
 * @param {Set} filteredElementIds - Set of element IDs to highlight
 */
function applyFilterHighlighting(filteredElementIds) {
    if (!window.cy) return;
    
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

/**
 * Get network statistics
 * @returns {Object} Network statistics
 */
function getNetworkStats() {
    if (!window.cy) {
        return {
            nodes: 0,
            edges: 0,
            connectedComponents: 0,
            averageDegree: '0.00'
        };
    }
    
    const nodes = window.cy.nodes();
    const edges = window.cy.edges();
    
    // Calculate connected components using BFS
    const visited = new Set();
    let components = 0;
    
    nodes.forEach(node => {
        if (!visited.has(node.id())) {
            components++;
            const queue = [node];
            
            while (queue.length > 0) {
                const current = queue.shift();
                if (!visited.has(current.id())) {
                    visited.add(current.id());
                    current.neighborhood('node').forEach(neighbor => {
                        if (!visited.has(neighbor.id())) {
                            queue.push(neighbor);
                        }
                    });
                }
            }
        }
    });
    
    // Calculate average degree
    const totalDegree = nodes.reduce((sum, node) => sum + node.degree(), 0);
    const avgDegree = nodes.length > 0 ? (totalDegree / nodes.length).toFixed(2) : '0.00';
    
    return {
        nodes: nodes.length,
        edges: edges.length,
        connectedComponents: components,
        averageDegree: avgDegree
    };
}

/**
 * Format node data as an HTML table
 * @param {Object} nodeData - Node data object
 * @returns {string} HTML table string
 */
function formatNodeDataTable(nodeData) {
    const formattedData = Object.entries(nodeData)
        .map(([key, value]) => {
            const displayValue = typeof value === 'object' 
                ? JSON.stringify(value, null, 2) 
                : escapeHtml(String(value));
            
            return `<tr>
                <td class="fw-bold">${escapeHtml(key)}</td>
                <td>${displayValue}</td>
            </tr>`;
        })
        .join('');
    
    return `<div class="table-responsive">
        <table class="table table-striped table-hover">
            <thead class="table-primary">
                <tr><th>Property</th><th>Value</th></tr>
            </thead>
            <tbody>${formattedData}</tbody>
        </table>
    </div>`;
}

/**
 * Format edge information as HTML
 * @param {Object} edge - Cytoscape edge object
 * @returns {string} HTML string
 */
function formatEdgeInfo(edge) {
    const source = edge.source().data('label') || edge.source().data('id');
    const target = edge.target().data('label') || edge.target().data('id');
    const edgeData = edge.data();
    
    let edgeInfoContent = `
        <div class="d-flex justify-content-center mb-3">
            <div class="text-center p-3 border rounded bg-light">
                <div class="fw-bold text-primary">${escapeHtml(source)}</div>
                <i class="bi bi-arrow-down text-primary fs-3"></i>
                <div class="fw-bold text-primary">${escapeHtml(target)}</div>
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
            const displayValue = typeof value === 'object' 
                ? JSON.stringify(value, null, 2) 
                : escapeHtml(String(value));
            
            edgeInfoContent += `
                <tr>
                    <td class="fw-bold">${escapeHtml(key)}</td>
                    <td>${displayValue}</td>
                </tr>`;
        }
    }
    
    edgeInfoContent += `</tbody></table></div>`;
    return edgeInfoContent;
}

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show context menu at specified position
 * @param {number} x - X coordinate
 * @param {number} y - Y coordinate
 * @param {Array} items - Menu items array
 */
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
    
    // Position adjustment to keep menu on screen
    const rect = menu.getBoundingClientRect();
    if (rect.right > window.innerWidth) {
        menu.style.left = `${x - rect.width}px`;
    }
    if (rect.bottom > window.innerHeight) {
        menu.style.top = `${y - rect.height}px`;
    }
}

/**
 * Hide context menu
 */
function hideContextMenu() {
    const menu = document.getElementById('cytoscape-context-menu');
    if (menu) {
        menu.remove();
    }
}

/**
 * Show modal dialog
 * @param {string} title - Modal title
 * @param {string} content - Modal content (HTML)
 * @param {string} size - Modal size class (modal-sm, modal-lg, modal-xl)
 */
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
                    <h5 class="modal-title">${escapeHtml(title)}</h5>
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
        
        // Cleanup on hide
        modalDiv.addEventListener('hidden.bs.modal', () => {
            modalDiv.remove();
        });
    }
}

/**
 * Download network as JSON
 */
function downloadNetworkJSON() {
    if (!window.cy) return;
    
    const networkData = {
        elements: window.cy.json().elements,
        metadata: {
            exportDate: new Date().toISOString(),
            nodeCount: window.cy.nodes().length,
            edgeCount: window.cy.edges().length
        }
    };
    
    const dataStr = JSON.stringify(networkData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `network-export-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    URL.revokeObjectURL(url);
}

/**
 * Export network as PNG image
 * @param {Object} options - Export options
 */
function exportNetworkPNG(options = {}) {
    if (!window.cy) {
        console.error('Cytoscape instance not available');
        showExportError('Network not available for export');
        return;
    }
    
    try {
        const defaultOptions = {
            output: 'blob',
            bg: 'white',
            full: true,
            scale: 2,
            maxWidth: 2000,
            maxHeight: 2000
        };
        
        const exportOptions = { ...defaultOptions, ...options };
        const png = window.cy.png(exportOptions);
        
        const url = URL.createObjectURL(png);
        const link = document.createElement('a');
        link.href = url;
        link.download = `network-export-${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        showExportSuccess('PNG image downloaded successfully');
    } catch (error) {
        console.error('PNG export error:', error);
        showExportError('Failed to export PNG image');
    }
}

/**
 * Export network as SVG image
 */
function exportNetworkSVG() {
    if (!window.cy) {
        console.error('Cytoscape instance not available');
        showExportError('Network not available for export');
        return;
    }
    
    try {
        // Check if SVG export is available
        if (typeof window.cy.svg !== 'function') {
            console.warn('SVG export not available, falling back to PNG');
            showExportWarning('SVG export not available, using PNG instead');
            exportNetworkPNG();
            return;
        }
        
        const svg = window.cy.svg({
            output: 'blob',
            bg: 'white',
            full: true
        });
        
        const url = URL.createObjectURL(svg);
        const link = document.createElement('a');
        link.href = url;
        link.download = `network-export-${Date.now()}.svg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        showExportSuccess('SVG image downloaded successfully');
    } catch (error) {
        console.error('SVG export error:', error);
        showExportWarning('SVG export failed, using PNG instead');
        exportNetworkPNG();
    }
}

/**
 * Export high-resolution PNG image
 */
function exportNetworkHighResPNG() {
    if (!window.cy) {
        console.error('Cytoscape instance not available');
        showExportError('Network not available for export');
        return;
    }
    
    try {
        const highResOptions = {
            output: 'blob',
            bg: 'white',
            full: true,
            scale: 4,
            maxWidth: 4000,
            maxHeight: 4000
        };
        
        const png = window.cy.png(highResOptions);
        
        const url = URL.createObjectURL(png);
        const link = document.createElement('a');
        link.href = url;
        link.download = `network-highres-export-${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
        showExportSuccess('High-resolution PNG downloaded successfully');
    } catch (error) {
        console.error('High-res PNG export error:', error);
        showExportError('Failed to export high-resolution PNG');
    }
}

/**
 * Show export success message
 * @param {string} message - Success message
 */
function showExportSuccess(message) {
    showToast(message, 'success');
}

/**
 * Show export error message
 * @param {string} message - Error message
 */
function showExportError(message) {
    showToast(message, 'error');
}

/**
 * Show export warning message
 * @param {string} message - Warning message
 */
function showExportWarning(message) {
    showToast(message, 'warning');
}

/**
 * Show toast notification
 * @param {string} message - Message to show
 * @param {string} type - Toast type (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    // Try to use Dash toast if available
    if (window.dash_clientside && window.dash_clientside.callback_context) {
        // This would require a Dash callback to handle, so for now use browser alert
        console.log(`${type.toUpperCase()}: ${message}`);
    }
    
    // Create a simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${getBootstrapAlertClass(type)} alert-dismissible fade show`;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '10001';
    toast.style.minWidth = '300px';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

/**
 * Get Bootstrap alert class for toast type
 * @param {string} type - Toast type
 * @returns {string} Bootstrap class
 */
function getBootstrapAlertClass(type) {
    switch (type) {
        case 'success': return 'success';
        case 'error': return 'danger';
        case 'warning': return 'warning';
        case 'info': return 'info';
        default: return 'info';
    }
}

/**
 * Load network from JSON
 * @param {string} jsonString - JSON string of network data
 */
function loadNetworkFromJSON(jsonString) {
    if (!window.cy) return;
    
    try {
        const networkData = JSON.parse(jsonString);
        
        if (networkData.elements) {
            window.cy.elements().remove();
            window.cy.add(networkData.elements);
            window.cy.layout({ name: 'fcose', animate: true }).run();
            
            console.log('Network loaded successfully');
        }
    } catch (error) {
        console.error('Error loading network:', error);
        alert('Failed to load network data. Please check the JSON format.');
    }
}

/**
 * Find shortest path between two nodes
 * @param {Object} sourceNode - Source node
 * @param {Object} targetNode - Target node
 * @returns {Array} Path as array of elements
 */
function findShortestPath(sourceNode, targetNode) {
    if (!window.cy || !sourceNode || !targetNode) return null;
    
    const dijkstra = window.cy.elements().dijkstra(sourceNode, (edge) => 1);
    const path = dijkstra.pathTo(targetNode);
    
    return path;
}

/**
 * Highlight path between nodes
 * @param {Object} path - Cytoscape path collection
 */
function highlightPath(path) {
    if (!path || path.length === 0) return;
    
    // Clear previous highlights
    clearHighlighting();
    
    // Fade all elements
    window.cy.elements().addClass('faded');
    
    // Highlight path
    path.removeClass('faded').addClass('highlighted');
}

// Click anywhere to hide context menu
document.addEventListener('click', hideContextMenu);