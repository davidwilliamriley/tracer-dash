# pages/help.py

import dash
from views.help_view import HelpView

dash.register_page(__name__, path="/help", name="Help")

help_sections = [
    # Row 1
    [
        {
            'icon': 'bi bi-search',
            'title': 'Tracer',
            'description': 'Read about the background, and purpose Tracer.',
            # 'link': '/help/about',
            'link': '#'
        }
    ],
    # Row 2
    # [
    #     {
    #         'icon': 'bi bi-diagram-3',
    #         'title': 'Systems Engineering',
    #         'description': 'A (very) brief introduction to Systems Engineering.',
    #         'link': '/help/systems'
    #     },
    #     {
    #         'icon': 'bi bi-person-gear',
    #         'title': 'Role of the Architect',
    #         'description': 'Read about the role of the System Architect.',
    #         'link': '/help/architect'
    #     }
    # ],
    # Row 3
    [
        {
            'icon': 'bi bi-database',
            'title': 'Schema',
            'description': 'The Tracer Schema.',
            'link': '/help/schema',
            'link': '#'
        },
        # {
        #     'icon': 'bi bi-diagram-3',
        #     'title': 'Data Modelling',
        #     'description': 'Read about Modelling in Tracer.',
        #     'link': '/help/modelling'
        # }
    ],
    # Row 4
    [
        {
            'icon': 'bi bi-speedometer',
            'title': 'Dashboards',
            'description': 'Dashboards in Tracer.',
            # 'link': '/help/dashboards',
            'link': '#'
        },
        # {
        #     'icon': 'bi bi-file-earmark-richtext',
        #     'title': 'Reports',
        #     'description': 'Read about Reports in PCM.',
        #     'link': '/help/reports'
        # }
    ],
    # Row 5
    [
        {
            'icon': 'bi bi-bezier2',
            'title': 'Graphs',
            'description': 'Graphs in Tracer.',
            # 'link': '/help/graphs',
            'link': '#'
        },
        {
            'icon': 'bi bi-bar-chart',
            'title': 'Components',
            'description': 'Components in Tracer.',
            # 'link': '/help/components',
            'link': '#'
        }
    ],
    # Row 6
    [
        {
            'icon': 'bi bi-arrow-repeat',
            'title': 'Edges',
            'description': 'Edges in Tracer.',
            # 'link': '/help/edges',
            'link': '#'
        },
        {
            'icon': 'bi bi-link-45deg',
            'title': "Edge Types",
            'description': 'Edge Types in Tracer.',
            # 'link': '/help/edge_types',
            'link': '#'
        },
        {
            'icon': 'bi bi-plus-circle',
            'title': 'Nodes',
            'description': 'Nodes in Tracer.',
            # 'link': '/help/nodes',
            'link': '#'
        },
    ],
    # Row 7
    [
        {
            'icon': 'bi bi-gear',
            'title': 'Settings',
            'description': 'Application Settings.',
            # 'link': '/help/settings',
            'link': '#'
        },
    ]
]

help_view = HelpView(help_sections)

def layout():
    return help_view.render()