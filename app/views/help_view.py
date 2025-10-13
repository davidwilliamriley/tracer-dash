# views/help_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_info_card(title, content, icon_class="bi bi-info-circle"):
    """Create an information card with icon"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon_class} text-primary me-3", style={"fontSize": "1.5rem"}),
                html.H3(title, className="card-title d-inline-block mb-3")
            ], className="d-flex align-items-center"),
            html.P(content, className="card-text")
        ])
    ], className="mb-3 shadow-sm")


def create_edge_table():
    """Create the edge table structure"""
    return dbc.Table([
        html.Colgroup([
            html.Col(style={"width": "5%"}),
            html.Col(style={"width": "20%"}),
            html.Col(style={"width": "20%"}),
            html.Col(style={"width": "10%"}),
            html.Col(style={"width": "10%"}),
            html.Col(style={"width": "35%"}),
        ]),
        html.Thead([
            html.Tr([
                html.Th("Item", scope="col"),
                html.Th("Field", scope="col"),
                html.Th("Type", scope="col"),
                html.Th("Unique", scope="col"),
                html.Th("Null", scope="col"),
                html.Th("Default", scope="col"),
            ], className="table-primary")
        ]),
        html.Tbody([
            html.Tr([
                html.Th("1", scope="row"),
                html.Td(html.Code("edge_id")),
                html.Td("GUID"),
                html.Td(html.Span("YES", className="badge bg-success")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td(html.Em("None")),
            ]),
            html.Tr([
                html.Th("2", scope="row"),
                html.Td(html.Code("edge_source_fk")),
                html.Td("GUID LU from Nodes Table"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td(html.Em("None")),
            ]),
            html.Tr([
                html.Th("3", scope="row"),
                html.Td(html.Code("edge_relation_fk")),
                html.Td("GUID LU from Relations Table"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td(html.Em("None")),
            ]),
            html.Tr([
                html.Th("4", scope="row"),
                html.Td(html.Code("edge_weight")),
                html.Td("integer"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td("1"),
            ]),
            html.Tr([
                html.Th("5", scope="row"),
                html.Td(html.Code("edge_target_fk")),
                html.Td("GUID LU from Nodes Table"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td(html.Em("None")),
            ]),
            html.Tr([
                html.Th("6", scope="row"),
                html.Td(html.Code("changed_at")),
                html.Td("datetime"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td("UTC Date & Time"),
            ]),
            html.Tr([
                html.Th("7", scope="row"),
                html.Td(html.Code("changed_by")),
                html.Td("text"),
                html.Td(html.Span("NO", className="badge bg-secondary")),
                html.Td(html.Span("NO", className="badge bg-danger")),
                html.Td("User Name"),
            ]),
        ])
    ], striped=True, hover=True, responsive=True, className="mb-4")


def create_schema_content():
    """Create the complete schema content for the accordion"""
    return html.Div([
        # Application Data Overview
        html.Div([
            html.H3([
                html.I(className="bi bi-database me-2 text-primary"),
                "Application Data"
            ], className="mt-3 mb-3"),
            html.P("Configuration Items, Configuration Information, Properties and Values form the core data structure of the PCM Application.", 
                   className="lead mb-4")
        ]),
        
        # Data Model Components
        dbc.Row([
            dbc.Col([
                create_info_card(
                    "Configuration Items",
                    "Configuration Items are the primary objects in the PCM Application. They represent the core entities that need to be managed and tracked within the system.",
                    "bi bi-box-seam"
                )
            ], md=6),
            dbc.Col([
                create_info_card(
                    "Configuration Information",
                    "Configuration Information provides additional context and details for the Configuration Items, enriching them with relevant metadata and descriptive information.",
                    "bi bi-info-square"
                )
            ], md=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                create_info_card(
                    "Properties",
                    "Properties are used to provide structured attributes for Configuration Items and Configuration Information, enabling flexible data modeling.",
                    "bi bi-tags"
                )
            ], md=6),
            dbc.Col([
                create_info_card(
                    "Values",
                    "Properties have Values that store the actual data content, providing the specific information associated with each property.",
                    "bi bi-file-text"
                )
            ], md=6)
        ], className="mb-4"),
        
        # Edge Objects Structure
        html.Div([
            html.H3([
                html.I(className="bi bi-table me-2 text-primary"),
                "Edge Objects Structure"
            ], className="mt-4 mb-3"),
            html.P("Edges are comprised of 2 Nodes and 1 Relation, and are used to create Graphs and Networks.", 
                   className="mb-3"),
            create_edge_table()
        ]),
    ])


class HelpView:
    def __init__(self, help_sections):
        self.help_sections = help_sections
    
    def create_feature_accordion_item(self, feature, index):
        # Special handling for Schema section
        if feature['title'] == 'Schema':
            return dbc.AccordionItem([
                html.Div([
                    html.P(feature['description'], className="mt-3 mb-4"),
                    create_schema_content()
                ])
            ], title=[
                html.I(className=feature['icon'], style={"marginRight": "10px"}),
                html.Span(feature['title'])
            ], item_id=f"item-{index}")
        else:
            # Default accordion item for other sections
            return dbc.AccordionItem([
                html.Div([
                    html.P(feature['description'], className="mt-3"),
                    dcc.Link([
                        html.Span("Learn More", className="link-text"),
                        html.I(className="bi bi-chevron-right")
                    ], 
                    href=feature['link'],
                    className="icon-link mt-2"
                    )
                ])
            ], title=[
                html.I(className=feature['icon'], style={"marginRight": "10px"}),
                html.Span(feature['title'])
            ], item_id=f"item-{index}")
    
    def create_rows(self):
        all_items = []
        index = 0
        
        for row_data in self.help_sections:
            for feature in row_data:
                all_items.append(self.create_feature_accordion_item(feature, index))
                index += 1
        
        return [dbc.Accordion(all_items, start_collapsed=True, always_open=False)]
    
    def render(self):
        return dbc.Container([
            dbc.Row([
                # dbc.Col([
                #     html.Nav([
                #         html.Ol([
                #             html.Li(html.A("Home", href="#"), className="breadcrumb-item"),
                #             html.Li("Help", className="breadcrumb-item active"),
                #         ], className="breadcrumb mb-2 mt-2")
                #     ]),
                html.H1([html.I(className="bi bi-question-circle me-2"), "Help & Resources"], className="my-4 text-primary"),
                html.P("Resources to assist you working with Tracer", className="text-muted mb-4")
            ]),
            dbc.Row([
                dbc.Col([
                    *self.create_rows()
                ])
            ])
        ], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '100px', 'display': 'flex', 'flexDirection': 'column'})
