// assets/js/cytoscape_config.js
// Configuration for Cytoscape visualization

const CytoscapeConfig = {
    // Animation settings
    animation: {
        layoutDuration: 1000,
        layoutEasing: 'ease-out',
        nodeFadeDuration: 800,
        edgeFadeDuration: 1000,
        fadeEasing: 'ease-in',
        initialDelay: 100,
        filterDelay: 1200
    },
    
    // Layout settings
    layout: {
        fcose: {
            name: 'fcose',
            animate: true,
            padding: 30,
            randomize: true,
            nodeRepulsion: 400000,
            idealEdgeLength: 100,
            avoidOverlap: true,
            gravity: 80
        },
        breadthfirst: {
            name: 'breadthfirst',
            animate: true,
            padding: 30
        },
        circle: {
            name: 'circle',
            animate: true,
            padding: 30
        },
        concentric: {
            name: 'concentric',
            animate: true,
            padding: 30
        },
        cose: {
            name: 'cose',
            animate: true,
            padding: 30
        },
        grid: {
            name: 'grid',
            animate: true,
            padding: 30
        }
    },
    
    // Color scheme (Bootstrap theme)
    colors: {
        node: {
            background: '#e3f2fd',
            border: '#0d6efd',
            borderWidth: '3px',
            selected: '#0d6efd',
            selectedBorder: '#0b5ed7',
            connected: '#b3d9ff'
        },
        edge: {
            line: '#0d6efd',
            arrow: '#0d6efd',
            width: '3px',
            selected: '#0b5ed7',
            connected: '#4da6ff',
            creation: '#dc3545'
        },
        text: {
            primary: '#6c757d',
            background: 'white'
        }
    },
    
    // Node settings
    node: {
        height: '40px',
        width: '40px',
        fontSize: '12px'
    },
    
    // Edge settings
    edge: {
        fontSize: '10px',
        curveStyle: 'bezier'
    },
    
    // Opacity settings
    opacity: {
        normal: 1,
        faded: 0.2,
        hidden: 0
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CytoscapeConfig;
}