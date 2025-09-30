# views/help_view.py

from dash import html, dcc
import dash_bootstrap_components as dbc


class HelpView:
    def __init__(self, help_sections):
        self.help_sections = help_sections
    
    def create_feature_card(self, feature):
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
    
    def create_rows(self):
        rows = []
        for row_data in self.help_sections:
            cols = [self.create_feature_card(feature) for feature in row_data]
            
            rows.append(
                dbc.Row(cols, className="g-4 py-4")
            )
        
        return rows
    
    def render(self):
        return dbc.Container([
            html.H1("Help Center", className="mb-4 text-left"),
            html.Hr(),
            *self.create_rows()
        ], className="px-4 py-5", id="help-page")

HELP_PAGE_STYLES = """
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
"""