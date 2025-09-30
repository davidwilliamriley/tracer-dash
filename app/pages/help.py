# pages/help.py

import dash
from views.help_view import HelpView

dash.register_page(__name__, path="/help", name="Help")

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

help_view = HelpView(help_sections)

def layout():
    return help_view.render()