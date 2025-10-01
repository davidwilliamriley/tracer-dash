# views/help_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc


class HelpView:
    def __init__(self, help_sections):
        self.help_sections = help_sections
    
    def create_feature_accordion_item(self, feature, index):
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
                html.H1([html.I(className="bi bi-question-circle me-2"), "Help & Resources"], className="my-4"),
                html.P("Resources to assist you working with Tracer", className="text-muted mb-4")
            ]),
            dbc.Row([
                dbc.Col([
                    *self.create_rows()
                ])
            ])
        ], style={'minHeight': 'calc(100vh - 120px)', 'paddingBottom': '100px', 'display': 'flex', 'flexDirection': 'column'})
