// assets/js/cytoscape_styles.js
// Cytoscape style definitions

/**
 * Get Cytoscape stylesheet based on configuration
 * @returns {Array} Cytoscape style array
 */
function getCytoscapeStyles() {
    const config = window.CytoscapeConfig || {};
    const colors = config.colors || {};
    const nodeConfig = config.node || {};
    const edgeConfig = config.edge || {};
    const opacity = config.opacity || {};

    return [
        // Base node style
        {
            selector: 'node',
            style: {
                'background-color': colors.node?.background,
                'border-color': colors.node?.border,
                'border-width': colors.node?.borderWidth,
                'height': nodeConfig.height,
                'width': nodeConfig.width,
                'label': 'data(label)',
                'text-valign': 'top',
                'text-halign': 'right',
                'font-size': nodeConfig.fontSize,
                'color': colors.text?.primary,
                'opacity': opacity.normal
            }
        },
        
        // Selected node style
        {
            selector: ':selected',
            style: {
                'background-color': colors.node?.selected,
                'border-color': colors.node?.selectedBorder,
                'border-width': '4px'
            }
        },
        
        // Connected node style (when filtering/selecting)
        {
            selector: '.connected',
            style: {
                'background-color': colors.node?.connected,
                'border-color': colors.node?.border,
                'border-width': colors.node?.borderWidth
            }
        },
        
        // Base edge style
        {
            selector: 'edge',
            style: {
                'curve-style': edgeConfig.curveStyle,
                'line-color': colors.edge?.line,
                'target-arrow-color': colors.edge?.arrow,
                'target-arrow-shape': 'triangle',
                'width': colors.edge?.width,
                'opacity': opacity.normal
            }
        },
        
        // Edge with label
        {
            selector: 'edge[label]',
            style: {
                'color': colors.text?.primary,
                'font-size': edgeConfig.fontSize,
                'label': 'data(label)',
                'text-rotation': 'autorotate',
                'text-background-color': colors.text?.background,
                'text-background-opacity': 0.8
            }
        },
        
        // Selected edge style
        {
            selector: 'edge:selected',
            style: {
                'line-color': colors.edge?.selected,
                'target-arrow-color': colors.edge?.selected,
                'width': '4px'
            }
        },
        
        // Connected edge style
        {
            selector: 'edge.connected',
            style: {
                'line-color': colors.edge?.connected,
                'target-arrow-color': colors.edge?.connected,
                'width': colors.edge?.width
            }
        },
        
        // Edge creation source node
        {
            selector: '.edge-creation-source',
            style: {
                'border-width': 3,
                'border-color': colors.edge?.creation
            }
        },
        
        // Edge creation preview
        {
            selector: '.edge-creation-preview',
            style: {
                'line-color': colors.edge?.creation,
                'target-arrow-color': colors.edge?.creation,
                'curve-style': edgeConfig.curveStyle,
                'target-arrow-shape': 'triangle',
                'width': 3,
                'line-style': 'dashed'
            }
        },
        
        // Faded elements (when filtering)
        {
            selector: '.faded',
            style: {
                'opacity': opacity.faded,
                'text-opacity': opacity.faded
            }
        },
        
        // Filtered out elements (grayed out but still visible)
        {
            selector: '.filtered-out',
            style: {
                'opacity': 0.5,
                'text-opacity': 0.3,
                'background-color': '#f5f5f5',
                'border-color': '#e0e0e0',
                'line-color': '#e0e0e0',
                'target-arrow-color': '#e0e0e0',
                'source-arrow-color': '#e0e0e0',
                'color': '#bbbbbb',
                'transition-property': 'opacity, background-color, line-color, border-color',
                'transition-duration': '0.3s'
            }
        },
        
        // Hidden elements
        {
            selector: '.hidden',
            style: {
                'display': 'none'
            }
        },
        
        // Highlighted elements
        {
            selector: '.highlighted',
            style: {
                'background-color': colors.highlight?.background,
                'line-color': colors.highlight?.line,
                'target-arrow-color': colors.highlight?.arrow,
                'transition-property': 'background-color, line-color',
                'transition-duration': '0.3s'
            }
        },
        
        // Search match elements (direct matches from search)
        {
            selector: '.search-match',
            style: {
                'background-color': colors.search?.matchBackground || '#ffeb3b',
                'border-color': colors.search?.matchBorder || '#ff9800',
                'border-width': '3px',
                'line-color': colors.search?.matchLine || '#ff9800',
                'target-arrow-color': colors.search?.matchArrow || '#ff9800',
                'text-background-color': colors.search?.textBackground || '#fff',
                'text-background-opacity': 0.9,
                'transition-property': 'background-color, border-color, line-color',
                'transition-duration': '0.3s'
            }
        }
    ];
}

/**
 * Get layout configuration by name
 * @param {string} layoutName - Name of the layout algorithm
 * @returns {Object} Layout configuration object
 */
function getLayoutConfig(layoutName) {
    const config = window.CytoscapeConfig || {};
    const layouts = config.layout || {};
    const animation = config.animation || {};
    
    const layoutConfig = layouts[layoutName] || layouts.fcose || {};
    
    // Add animation settings
    return {
        ...layoutConfig,
        animationDuration: animation.layoutDuration,
        animationEasing: animation.layoutEasing
    };
}