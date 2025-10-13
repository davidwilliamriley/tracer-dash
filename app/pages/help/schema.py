# pages/help/schema.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# # Register this page
# dash.register_page(__name__, path="/help/modelling", name="Data Modelling")

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

def layout():
    return dbc.Container([
        # Page Header with breadcrumb
        html.Div([
            dbc.Breadcrumb(
                items=[
                    {"label": "Help", "href": "/help", "external_link": True},
                    {"label": "Data Modelling", "active": True}
                ], 
                className="mb-3"
            ),
            
            html.Div([
                html.I(className="bi bi-diagram-3 text-primary me-3", style={"fontSize": "2rem"}),
                html.Div([
                    html.H1("Data Modelling", className="display-6 mb-0"),
                    html.P("This page describes the approach to Modelling in Tracer.", 
                           className="fs-5 text-muted")
                ])
            ], className="d-flex align-items-center mb-4")
        ]),
        
        # Application Data Overview
        html.Div([
            html.H2([
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
        ], className="mb-5"),
        
        # Optional: Uncomment to show schema diagram
        # dbc.Alert([
        #     html.H4("Schema Diagram", className="alert-heading"),
        #     html.P("The visual representation of the data schema is currently being updated."),
        #     html.Hr(),
        #     html.P("Please refer to the textual descriptions above for the current model structure.", className="mb-0")
        # ], color="info", className="mb-4"),
        
        # Optional: Include the edge table if needed
        # html.Div([
        #     html.H2([
        #         html.I(className="bi bi-table me-2 text-primary"),
        #         "Edge Objects Structure"
        #     ], className="mt-5 mb-3"),
        #     html.P("Edges are comprised of 2 Nodes and 1 Relation, and are used to create Graphs and Networks.", 
        #            className="mb-3"),
        #     create_edge_table()
        # ]),
        
        # Navigation
        html.Hr(className="mt-5"),
        dbc.Row([
            dbc.Col([
                dcc.Link([
                    html.I(className="bi bi-arrow-left me-2"),
                    "Back to Help"
                ], href="/help", className="btn btn-outline-primary")
            ], width="auto"),
            dbc.Col([
                dcc.Link([
                    "Data Schema",
                    html.I(className="bi bi-arrow-right ms-2")
                ], href="/help/schema", className="btn btn-outline-secondary")
            ], width="auto")
        ], justify="between", className="mb-4")
        
    ], className="px-4 py-5", id="modelling-page")