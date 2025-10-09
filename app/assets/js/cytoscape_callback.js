// assets/js/cytoscape_callback.js
// Cytoscape client-side callback for network visualization
//
// Dependencies (must be loaded before this script):
// - cytoscape_config.js    : Configuration constants and settings
// - cytoscape_styles.js    : getCytoscapeStyles() function
// - cytoscape_utils.js     : Utility functions (applyFilterHighlighting, showModal, etc.)
// - cytoscape_events.js    : Event handlers (setupEventHandlers, setupContextMenus, etc.)

// Register Cytoscape extensions if they're available
if (typeof cytoscape !== 'undefined') {
    // Register SVG extension if available
    if (typeof window.cytoscapeSvg !== 'undefined') {
        cytoscape.use(window.cytoscapeSvg);
        console.log('Cytoscape SVG extension registered');
    } else if (typeof cytoscapeSvg !== 'undefined') {
        cytoscape.use(cytoscapeSvg);
        console.log('Cytoscape SVG extension registered');
    } else {
        console.warn('Cytoscape SVG extension not found');
    }

    // Register Dagre extension
    if (typeof window.cytoscapeDagre !== 'undefined') {
        cytoscape.use(window.cytoscapeDagre);
        console.log('Cytoscape Dagre extension registered');
    } else if (typeof cytoscapeDagre !== 'undefined') {
        cytoscape.use(cytoscapeDagre);
        console.log('Cytoscape Dagre extension registered');
    }

    // Register Klay extension
    if (typeof window.cytoscapeKlay !== 'undefined') {
        cytoscape.use(window.cytoscapeKlay);
        console.log('Cytoscape Klay extension registered');
    } else if (typeof cytoscapeKlay !== 'undefined') {
        cytoscape.use(cytoscapeKlay);
        console.log('Cytoscape Klay extension registered');
    }

    // Register COLA extension
    if (typeof window.cytoscapeCola !== 'undefined') {
        cytoscape.use(window.cytoscapeCola);
        console.log('Cytoscape COLA extension registered');
    } else if (typeof cytoscapeCola !== 'undefined') {
        cytoscape.use(cytoscapeCola);
        console.log('Cytoscape COLA extension registered');
    }

    // Log available layouts for debugging
    console.log('Available Cytoscape layouts:', cytoscape.default ? 
        Object.keys(cytoscape.default.use._extensions?.layout || {}) : 
        'Unable to detect layouts');
}

// Utility functions that might not be loaded from cytoscape_utils.js
if (typeof showToast === 'undefined') {
    window.showToast = function(message, type = 'info') {
        const toastStore = document.getElementById('toast-store');
        if (toastStore && window.dash_clientside) {
            window.dash_clientside.set_props('toast-store', {
                data: {
                    message: message,
                    type: type,
                    timestamp: Date.now()
                }
            });
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    };
}

if (typeof clearHighlighting === 'undefined') {
    window.clearHighlighting = function() {
        if (!window.cy) return;
        window.cy.elements().unselect();
        window.cy.elements().removeClass('connected faded highlighted search-match');
        window.cy.elements().style({
            'opacity': 1,
            'text-opacity': 1
        });
        console.log('Cleared all highlighting (fallback function)');
    };
}

window.cytoscapeCallback = function(networkDataJson, filteredValue, layoutAlgorithm) {
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
    
    // Default to fcose if no algorithm specified
    layoutAlgorithm = layoutAlgorithm || 'fcose';
    console.log('Applying layout algorithm:', layoutAlgorithm);
        
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
        
        // Find matching nodes - search in multiple fields
        const matchingNodes = networkData.elements.filter(ele => {
            if (ele.group === 'nodes') {
                const data = ele.data;
                return (data.label && data.label.toLowerCase().includes(filterValue)) ||
                       (data.name && data.name.toLowerCase().includes(filterValue)) ||
                       (data.identifier && data.identifier.toLowerCase().includes(filterValue)) ||
                       (data.description && data.description.toLowerCase().includes(filterValue));
            }
            return false;
        });
        
        // Find matching edges - search in multiple fields  
        const matchingEdges = networkData.elements.filter(ele => {
            if (ele.group === 'edges') {
                const data = ele.data;
                return (data.label && data.label.toLowerCase().includes(filterValue)) ||
                       (data.name && data.name.toLowerCase().includes(filterValue)) ||
                       (data.type && data.type.toLowerCase().includes(filterValue)) ||
                       (data.identifier && data.identifier.toLowerCase().includes(filterValue)) ||
                       (data.description && data.description.toLowerCase().includes(filterValue));
            }
            return false;
        });
        
        // Collect IDs of all matching elements
        matchingNodes.forEach(node => filteredElementIds.add(node.data.id));
        matchingEdges.forEach(edge => filteredElementIds.add(edge.data.id));
        
        // Also include connected nodes/edges for better context
        const connectedElements = new Set();
        matchingNodes.forEach(node => {
            networkData.elements.forEach(edge => {
                if (edge.group === 'edges' && 
                    (edge.data.source === node.data.id || edge.data.target === node.data.id)) {
                    connectedElements.add(edge.data.id);
                    // Add the other connected node
                    const connectedNodeId = edge.data.source === node.data.id ? 
                        edge.data.target : edge.data.source;
                    connectedElements.add(connectedNodeId);
                }
            });
        });
        
        // Add connected elements to filtered set for better visualization context
        connectedElements.forEach(id => filteredElementIds.add(id));
        
        console.log(`Search for "${filterValue}" found ${matchingNodes.length} nodes and ${matchingEdges.length} edges`);
        console.log(`Total highlighted elements (including connections): ${filteredElementIds.size}`);
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

    // Then run the selected layout after initialization
    setTimeout(() => {
        let layoutConfig;
        
        console.log('Attempting to apply layout:', layoutAlgorithm);
        
        switch(layoutAlgorithm) {
            case 'dagre':
                layoutConfig = {
                    name: 'dagre',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    nodeSep: 50,
                    edgeSep: 10,
                    rankSep: 50,
                    rankDir: 'TB',
                    ranker: 'longest-path'
                };
                break;
            case 'breadthfirst':
                layoutConfig = {
                    name: 'breadthfirst',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    directed: true,
                    spacingFactor: 1.75
                };
                break;
            case 'circle':
                layoutConfig = {
                    name: 'circle',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    radius: Math.min(containerRect.width, containerRect.height) / 3
                };
                break;
            case 'cola':
                // Check if COLA extension is available
                try {
                    layoutConfig = {
                        name: 'cola',
                        animate: true,
                        animationDuration: 1000,
                        animationEasing: 'ease-out',
                        fit: true,
                        padding: 30,
                        nodeSpacing: 50,
                        edgeLength: 100,
                        edgeSymDiffLength: 100,
                        jaccardLinkLengths: true,
                        edgeJaccardLengthRatio: 0.7,
                        unconstrIter: 30,
                        userConstIter: 0,
                        allConstIter: 5,
                        infinite: false
                    };
                    console.log('Using COLA layout');
                } catch (e) {
                    console.warn('COLA layout not available, using cose alternative');
                    layoutConfig = {
                        name: 'cose',
                        animate: true,
                        animationDuration: 1000,
                        animationEasing: 'ease-out',
                        fit: true,
                        padding: 30,
                        nodeSeparation: 75,
                        idealEdgeLength: 100,
                        edgeElasticity: 100,
                        nestingFactor: 5,
                        gravity: 250,
                        numIter: 100,
                        initialTemp: 200,
                        coolingFactor: 0.95,
                        minTemp: 1.0
                    };
                }
                break;
            case 'concentric':
                layoutConfig = {
                    name: 'concentric',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    concentric: function(node) {
                        return node.degree();
                    },
                    levelWidth: function(nodes) {
                        return 2;
                    }
                };
                break;
            case 'cose':
                layoutConfig = {
                    name: 'cose',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    nodeSeparation: 75,
                    idealEdgeLength: 100,
                    edgeElasticity: 100,
                    nestingFactor: 5,
                    gravity: 250,
                    numIter: 100,
                    initialTemp: 200,
                    coolingFactor: 0.95,
                    minTemp: 1.0
                };
                break;
            case 'grid':
                layoutConfig = {
                    name: 'grid',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30,
                    rows: Math.ceil(Math.sqrt(networkData.elements.filter(e => e.group === 'nodes').length)),
                    cols: undefined
                };
                break;
            case 'klay':
                // Check if Klay extension is available, otherwise use breadthfirst as alternative
                try {
                    // Test if klay layout is available
                    const testLayout = window.cy.layout({name: 'klay'});
                    layoutConfig = {
                        name: 'klay',
                        animate: true,
                        animationDuration: 1000,
                        animationEasing: 'ease-out',
                        fit: true,
                        padding: 30,
                        nodePlacement: 'BRANDES_KOEPF',
                        nodeLayering: 'NETWORK_SIMPLEX',
                        edgeRouting: 'ORTHOGONAL',
                        edgeSpacingFactor: 0.5,
                        inLayerSpacingFactor: 1.0,
                        layoutHierarchy: true,
                        intCoordinates: true,
                        thoroughness: 7,
                        direction: 'DOWN'
                    };
                    console.log('Using Klay layout');
                } catch (e) {
                    console.warn('Klay layout not available, using breadthfirst alternative');
                    layoutConfig = {
                        name: 'breadthfirst',
                        animate: true,
                        animationDuration: 1000,
                        animationEasing: 'ease-out',
                        fit: true,
                        padding: 30,
                        directed: true,
                        spacingFactor: 2.0,
                        circle: false,
                        grid: false,
                        avoidOverlap: true
                    };
                }
                break;
            case 'random':
                layoutConfig = {
                    name: 'random',
                    animate: true,
                    animationDuration: 1000,
                    animationEasing: 'ease-out',
                    fit: true,
                    padding: 30
                };
                break;
            case 'fcose':
            default:
                layoutConfig = {
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
                break;
        }
        
        console.log('Layout config:', layoutConfig);
        
        try {
            const layout = window.cy.layout(layoutConfig);
            layout.run();
            console.log('Layout applied successfully:', layoutAlgorithm);
        } catch (error) {
            console.error('Error applying layout:', layoutAlgorithm, error);
            // Fallback to fcose if the layout fails
            const fallbackLayout = window.cy.layout({
                name: 'fcose',
                quality: 'default',
                randomize: true,
                animate: true,
                animationDuration: 1000,
                animationEasing: 'ease-out',
                fit: true,
                padding: 30
            });
            fallbackLayout.run();
            console.log('Applied fallback fcose layout');
        }
            
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
    
    // For initial layout, don't apply any search filtering - let the search system handle it
    // This prevents conflicts between layout and search highlighting
    setTimeout(() => {
        console.log('Layout completed, ready for search operations');
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

// Note: getCytoscapeStyles() is defined in cytoscape_styles.js

// Note: applyFilterHighlighting() is defined in cytoscape_utils.js

// Note: setupEventHandlers() is defined in cytoscape_events.js

// Note: setupContextMenus() is defined in cytoscape_events.js

// Note: Helper functions (showContextMenu, hideContextMenu, showModal, etc.) are defined in cytoscape_utils.js

// Click anywhere to hide context menu
document.addEventListener('click', hideContextMenu);