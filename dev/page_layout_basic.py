import dash
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for the table
table_data = [
    {"id": 1, "name": "Item 1", "value": 100},
    {"id": 2, "name": "Item 2", "value": 200},
    {"id": 3, "name": "Item 3", "value": 300},
]

table_columns = [
    {"name": "ID", "id": "id"},
    {"name": "Name", "id": "name"},
    {"name": "Value", "id": "value"},
]

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        dbc.NavItem(dbc.NavLink("About", href="#")),
        dbc.NavItem(dbc.NavLink("Contact", href="#")),
    ],
    brand="My Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
    className="mb-3"
)

# Main content with stacked elements
main_content = dbc.Container([
    # Header row
    dbc.Row([
        dbc.Col([
            html.H2("Page Header", className="text-left my-3")
        ])
    ]),
    
    # Text row
    dbc.Row([
        dbc.Col([
            html.P(
                "This is a sample text section. You can add any descriptive "
                "text or information here. The layout uses Dash Bootstrap Components "
                "for responsive design.",
                className="mb-4 text-muted"
            )
        ])
    ]),

    # Text row with select and button
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id="select-dropdown",
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": "Option 3", "value": "3"},
                ],
                value="1",
                className="mb-2"
            )
        ], width=10),
        dbc.Col([
            dbc.Button("Reset", id="reset-button", color="secondary", className="w-100")
        ], width=2)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("Button 1", color="primary"),
                dbc.Button("Button 2", color="primary"),
                dbc.Button("Button 3", color="primary"),
            ])
        ], width="auto"),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("Action 1", color="success"),
                dbc.Button("Action 2", color="success"),
            ])
        ], width="auto", className="ms-auto")
    ], className="mb-4"),

    # Table row
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table',
                columns=table_columns,  # type: ignore
                data=table_data,  # type: ignore
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])
    ])
], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '60px'})

# Sticky footer
footer = html.Footer([
    dbc.Container([
        html.Hr(),
        html.P("© 2025 My Dashboard. All rights reserved.", 
               className="text-end text-muted")
    ])
], style={
    'position': 'fixed',
    'bottom': '0',
    'width': '100%',
    'backgroundColor': 'white',
    'padding': '10px 0'
})

# Show the Complete Layout
app.layout = html.Div([
    navbar,                                                                                                           
    main_content,
    footer
])

if __name__ == '__main__':
    app.run(debug=True)