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
                'background-color': colors.node?.background || '#e3f2fd',
                'border-color': colors.node?.border || '#0d6efd',
                'border-width': colors.node?.borderWidth || '3px',
                'height': nodeConfig.height || '40px',
                'width': nodeConfig.width || '40px',
                'label': 'data(label)',
                'text-valign': 'top',
                'text-halign': 'right',
                'font-size': nodeConfig.fontSize || '12px',
                'color': colors.text?.primary || '#6c757d',
                'opacity': opacity.normal || 1
            }
        },
        
        // Selected node style
        {
            selector: ':selected',
            style: {
                'background-color': colors.node?.selected || '#0d6efd',
                'border-color': colors.node?.selectedBorder || '#0b5ed7',
                'border-width': '4px'
            }
        },
        
        // Connected node style (when filtering/selecting)
        {
            selector: '.connected',
            style: {
                'background-color': colors.node?.connected || '#b3d9ff',
                'border-color': colors.node?.border || '#0d6efd',
                'border-width': '3px'
            }
        },
        
        // Base edge style
        {
            selector: 'edge',
            style: {
                'curve-style': edgeConfig.curveStyle || 'bezier',
                'line-color': colors.edge?.line || '#0d6efd',
                'target-arrow-color': colors.edge?.arrow || '#0d6efd',
                'target-arrow-shape': 'triangle',
                'width': colors.edge?.width || '3px',
                'opacity': opacity.normal || 1
            }
        },
        
        // Edge with label
        {
            selector: 'edge[label]',
            style: {
                'color': colors.text?.primary || '#6c757d',
                'font-size': edgeConfig.fontSize || '10px',
                'label': 'data(label)',
                'text-rotation': 'autorotate',
                'text-background-color': colors.text?.background || 'white',
                'text-background-opacity': 0.8
            }
        },
        
        // Selected edge style
        {
            selector: 'edge:selected',
            style: {
                'line-color': colors.edge?.selected || '#0b5ed7',
                'target-arrow-color': colors.edge?.selected || '#0b5ed7',
                'width': '4px'
            }
        },
        
        // Connected edge style
        {
            selector: 'edge.connected',
            style: {
                'line-color': colors.edge?.connected || '#4da6ff',
                'target-arrow-color': colors.edge?.connected || '#4da6ff',
                'width': '3px'
            }
        },
        
        // Edge creation source node
        {
            selector: '.edge-creation-source',
            style: {
                'border-width': 3,
                'border-color': colors.edge?.creation || '#dc3545'
            }
        },
        
        // Edge creation preview
        {
            selector: '.edge-creation-preview',
            style: {
                'line-color': colors.edge?.creation || '#dc3545',
                'target-arrow-color': colors.edge?.creation || '#dc3545',
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'width': 3,
                'line-style': 'dashed'
            }
        },
        
        // Faded elements (when filtering)
        {
            selector: '.faded',
            style: {
                'opacity': opacity.faded || 0.2,
                'text-opacity': opacity.faded || 0.2
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
                'background-color': '#fff176',
                'line-color': '#fbc02d',
                'target-arrow-color': '#fbc02d',
                'transition-property': 'background-color, line-color',
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
    
    const layoutConfig = layouts[layoutName] || layouts.fcose;
    
    // Add animation settings
    return {
        ...layoutConfig,
        animationDuration: animation.layoutDuration || 1000,
        animationEasing: animation.layoutEasing || 'ease-out'
    };
}