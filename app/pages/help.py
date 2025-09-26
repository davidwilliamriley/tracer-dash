# pages/help.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register this page
dash.register_page(__name__, path="/help", name="Help")

# Define the help sections data
help_sections = [
    # Row 1
    [
        {
            'icon': 'bi bi-search',
            'title': 'About PCM',
            'description': 'Read about the background, and purpose of PCM.',
            'link': '/help/about'
        }
    ],
    # Row 2
    [
        {
            'icon': 'bi bi-diagram-3',
            'title': 'Systems Engineering',
            'description': 'A (very) brief introduction to Systems Engineering.',
            'link': '/help/systems'
        },
        {
            'icon': 'bi bi-person-gear',
            'title': 'Role of the Architect',
            'description': 'Read about the role of the System Architect.',
            'link': '/help/architect'
        }
    ],
    # Row 3
    [
        {
            'icon': 'bi bi-database',
            'title': 'Data Schema',
            'description': 'Read about the Tracer Data Schema.',
            'link': '/help/schema'
        },
        {
            'icon': 'bi bi-diagram-3',
            'title': 'Data Modelling',
            'description': 'Read about Modelling in Tracer.',
            'link': '/help/modelling'
        }
    ],
    # Row 4
    [
        {
            'icon': 'bi bi-speedometer',
            'title': 'Dashboards',
            'description': 'Read about Dashboards in Tracer.',
            'link': '/help/dashboards'
        },
        {
            'icon': 'bi bi-file-earmark-richtext',
            'title': 'Reports',
            'description': 'Read about Reports in PCM.',
            'link': '/help/reports'
        }
    ],
    # Row 5
    [
        {
            'icon': 'bi bi-bezier2',
            'title': 'Networks',
            'description': 'Read about Graphs in Tracer.',
            'link': '/help/networks'
        },
        {
            'icon': 'bi bi-bar-chart',
            'title': 'Graphs',
            'description': 'Information about the tools available in Tracer.',
            'link': '/help/graphs'
        }
    ],
    # Row 6
    [
        {
            'icon': 'bi bi-arrow-repeat',
            'title': 'Edges',
            'description': 'Details about configuration options and settings...',
            'link': '/help/edges'
        },
        {
            'icon': 'bi bi-plus-circle',
            'title': 'Nodes',
            'description': 'Information about the tools available in Tracer.',
            'link': '/help/nodes'
        },
        {
            'icon': 'bi bi-link-45deg',
            'title': 'Relations',
            'description': 'Overview of analytics and reporting features...',
            'link': '/help/relations'
        }
    ],
    # Row 7
    [
        {
            'icon': 'bi bi-gear',
            'title': 'Settings',
            'description': 'Learn about the Configuration Settings.',
            'link': '/help/settings'
        }
    ]
]

def create_feature_card(feature):
    """Create a feature card component"""
    return dbc.Col([
        html.Div([
            html.Div([
                html.I(className=feature['icon'])
            ], className="feature-icon"),
            
            html.H3(feature['title'], className="fs-2 text-body-emphasis mt-2"),
            
            html.P(feature['description']),
            
            dcc.Link([
                html.Span("Learn More", className="link-text"),
                html.I(className="bi bi-chevron-right")
            ], 
            href=feature['link'],
            className="icon-link mt-2"
            )
        ], className="feature")
    ], className="col-12 col-md-6 col-lg-4 mb-4")

# Create the layout
def layout():
    # Create rows
    rows = []
    for row_data in help_sections:
        # Create columns for this row
        cols = []
        for feature in row_data:
            cols.append(create_feature_card(feature))
        
        # Create the row
        rows.append(
            dbc.Row(cols, className="g-4 py-4")
        )
    
    return dbc.Container([
        html.H1("Help Center", className="mb-4 text-center"),
        html.Hr(),
        *rows
    ], className="px-4 py-5", id="help-page")

# Custom CSS styles (add this to your main app or assets folder)
help_page_styles = """
<style>
.feature-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 4rem;
    height: 4rem;
    margin-bottom: 1rem;
    font-size: 2rem;
    color: #fff;
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    border-radius: 0.75rem;
    box-shadow: 0 4px 6px rgba(0, 123, 255, 0.1);
}

.feature {
    padding: 1.5rem;
    height: 100%;
    border-radius: 0.5rem;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    background: #fff;
    border: 1px solid #e9ecef;
}

.feature:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.icon-link {
    display: inline-flex;
    align-items: center;
    text-decoration: none;
    font-weight: 500;
    color: #007bff;
    transition: color 0.2s ease;
}

.icon-link:hover {
    color: #0056b3;
    text-decoration: none;
}

.icon-link i {
    margin-left: 0.5rem;
    font-size: 0.875rem;
    transition: transform 0.2s ease;
}

.icon-link:hover i {
    transform: translateX(2px);
}

.fs-2 {
    font-size: calc(1.325rem + 0.9vw) !important;
}

.text-body-emphasis {
    color: var(--bs-emphasis-color) !important;
}

#help-page {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    min-height: calc(100vh - 200px);
    border-radius: 0.5rem;
}
</style>
"""