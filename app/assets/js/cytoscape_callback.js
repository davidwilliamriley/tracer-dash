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
}

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

// Note: getCytoscapeStyles() is defined in cytoscape_styles.js

// Note: applyFilterHighlighting() is defined in cytoscape_utils.js

// Note: setupEventHandlers() is defined in cytoscape_events.js

// Note: setupContextMenus() is defined in cytoscape_events.js

// Note: Helper functions (showContextMenu, hideContextMenu, showModal, etc.) are defined in cytoscape_utils.js

// Click anywhere to hide context menu
document.addEventListener('click', hideContextMenu);