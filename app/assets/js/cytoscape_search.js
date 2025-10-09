// assets/js/cytoscape_search.js
// Search functionality for Cytoscape network visualization - optimized for performance

/**
 * Apply search filter without recreating the graph
 * @param {string} searchValue - The search term
 * @returns {boolean} - True if search was applied, false if no Cytoscape instance
 */
function applySearchFilter(searchValue) {
    if (!window.cy) {
        console.warn('No Cytoscape instance available for search');
        return false;
    }
    
    console.log(`Applying search filter: "${searchValue}"`);
    
    // Clear existing highlighting first
    if (typeof clearHighlighting === 'function') {
        clearHighlighting();
    } else {
        window.cy.elements().removeClass('connected faded highlighted search-match');
        window.cy.elements().unselect();
    }
    
    if (!searchValue || !searchValue.trim()) {
        // Empty search - show all elements normally, ensure nothing is faded
        window.cy.elements().removeClass('faded connected search-match highlighted');
        console.log('Empty search term, showing all elements normally');
        return true;
    }
    
    const filterValue = searchValue.toLowerCase().trim();
    
    // Find matching nodes with detailed logging
    const matchingNodes = window.cy.nodes().filter(node => {
        const data = node.data();
        const matches = (data.label && data.label.toLowerCase().includes(filterValue)) ||
                       (data.name && data.name.toLowerCase().includes(filterValue)) ||
                       (data.identifier && data.identifier.toLowerCase().includes(filterValue)) ||
                       (data.description && data.description.toLowerCase().includes(filterValue));
        
        if (matches) {
            console.log(`Matching node: ${data.label || data.name || data.identifier || data.id}`);
        }
        return matches;
    });
    
    // Find matching edges with detailed logging
    const matchingEdges = window.cy.edges().filter(edge => {
        const data = edge.data();
        const matches = (data.label && data.label.toLowerCase().includes(filterValue)) ||
                       (data.name && data.name.toLowerCase().includes(filterValue)) ||
                       (data.type && data.type.toLowerCase().includes(filterValue)) ||
                       (data.identifier && data.identifier.toLowerCase().includes(filterValue)) ||
                       (data.description && data.description.toLowerCase().includes(filterValue));
        
        if (matches) {
            console.log(`Matching edge: ${data.label || data.name || data.type || data.id}`);
        }
        return matches;
    });
    
    console.log(`Search for "${filterValue}" found ${matchingNodes.length} nodes and ${matchingEdges.length} edges`);
    
    if (matchingNodes.length === 0 && matchingEdges.length === 0) {
        // No matches found - fade everything and show message
        window.cy.elements().addClass('faded');
        showToast(`No elements found matching "${searchValue}"`, 'warning');
        return true;
    }
    
    // Combine all matching elements
    const allMatches = matchingNodes.union(matchingEdges);
    
    // Get neighborhood of matching elements for context
    const neighborhood = allMatches.neighborhood();
    const allHighlighted = allMatches.union(neighborhood);
    
    // Apply highlighting classes
    matchingNodes.addClass('search-match');
    matchingEdges.addClass('search-match');
    neighborhood.addClass('connected');
    
    // Fade everything that's not highlighted
    window.cy.elements().difference(allHighlighted).addClass('faded');
    
    // Select the direct matches for better visibility
    allMatches.select();
    
    console.log(`Highlighted ${allMatches.length} direct matches and ${neighborhood.length} connected elements`);
    
    // Show success feedback
    const totalMatches = matchingNodes.length + matchingEdges.length;
    showToast(`Found ${totalMatches} matching elements for "${searchValue}"`, 'success');
    
    return true;
}

/**
 * Optimized callback for search operations - doesn't recreate the graph
 * @param {string} networkDataJson - JSON string of network data (for compatibility)
 * @param {string} filteredValue - The search term
 * @param {string} layoutAlgorithm - Layout algorithm (ignored for search-only operations)
 * @returns {string} - Empty string to satisfy Dash callback requirements
 */
function cytoscapeSearchCallback(networkDataJson, filteredValue, layoutAlgorithm) {
    console.log('cytoscapeSearchCallback called with search term:', filteredValue);
    
    // If no Cytoscape instance exists, fall back to full callback
    if (!window.cy) {
        console.log('No Cytoscape instance, falling back to full callback');
        if (window.cytoscapeCallback) {
            return window.cytoscapeCallback(networkDataJson, filteredValue, layoutAlgorithm);
        } else {
            console.error('No cytoscapeCallback function available');
            return '';
        }
    }
    
    // Apply search without recreating the graph
    applySearchFilter(filteredValue);
    
    return '';
}

/**
 * Check if the current operation requires a full graph recreation
 * @param {string} networkDataJson - Current network data
 * @param {string} previousNetworkData - Previous network data
 * @returns {boolean} - True if graph structure has changed
 */
function requiresGraphRecreation(networkDataJson, previousNetworkData) {
    if (!previousNetworkData || !networkDataJson) {
        return true;
    }
    
    try {
        const current = JSON.parse(networkDataJson);
        const previous = JSON.parse(previousNetworkData);
        
        // Compare element counts as a quick check
        const currentElements = current.elements || [];
        const previousElements = previous.elements || [];
        
        if (currentElements.length !== previousElements.length) {
            return true;
        }
        
        // Compare element IDs to detect structural changes
        const currentIds = new Set(currentElements.map(el => el.data.id));
        const previousIds = new Set(previousElements.map(el => el.data.id));
        
        if (currentIds.size !== previousIds.size) {
            return true;
        }
        
        for (const id of currentIds) {
            if (!previousIds.has(id)) {
                return true;
            }
        }
        
        return false;
    } catch (e) {
        console.warn('Error comparing network data, assuming recreation needed:', e);
        return true;
    }
}

// Store previous network data for comparison
window.previousNetworkData = null;

/**
 * Smart callback that chooses between search-only and full recreation
 * @param {string} networkDataJson - JSON string of network data
 * @param {string} filteredValue - The search term
 * @param {string} layoutAlgorithm - Layout algorithm
 * @returns {string} - Empty string to satisfy Dash callback requirements
 */
function smartCytoscapeCallback(networkDataJson, filteredValue, layoutAlgorithm) {
    console.log('smartCytoscapeCallback called');
    
    // Check if we need to recreate the graph
    const needsRecreation = requiresGraphRecreation(networkDataJson, window.previousNetworkData);
    
    if (needsRecreation) {
        console.log('Graph structure changed, performing full recreation');
        window.previousNetworkData = networkDataJson;
        
        // Perform full recreation
        const result = window.cytoscapeCallback(networkDataJson, "", layoutAlgorithm);
        
        // Apply search filter after recreation if there's a search term
        if (filteredValue && filteredValue.trim()) {
            setTimeout(() => {
                console.log('Applying search filter after graph recreation');
                applySearchFilter(filteredValue);
            }, 1300); // Slightly after the layout completes
        }
        
        return result;
    } else {
        console.log('Graph structure unchanged, applying search filter only');
        return cytoscapeSearchCallback(networkDataJson, filteredValue, layoutAlgorithm);
    }
}

// Export functions for global use
if (typeof window !== 'undefined') {
    window.applySearchFilter = applySearchFilter;
    window.cytoscapeSearchCallback = cytoscapeSearchCallback;
    window.smartCytoscapeCallback = smartCytoscapeCallback;
    window.requiresGraphRecreation = requiresGraphRecreation;
}