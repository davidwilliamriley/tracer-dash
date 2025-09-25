# app.py

# imports
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# External stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
]

app = dash.Dash(
    __name__, 
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="Tracer"
)

def get_header():
    return html.Header([
        html.Div([
            html.Div([
                html.Div([
                    html.H2("Tracer", className="d-flex align-items-center my-lg-0 me-lg-auto text-white text-decoration-none fw-light"),
                    html.Ul([
                        html.Li(html.A([html.I(className="bi bi-house-door-fill"), " Home"], href="/", className="nav-link text-secondary")),
                        html.Li(html.A([html.I(className="bi bi-speedometer"), " Dashboards"], href="/dashboards", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-file-earmark-richtext"), " Reports"], href="/reports", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-bezier2"), " Networks"], href="/networks", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-diagram-2"), " Graphs"], href="/graphs", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-arrow-repeat"), " Edges"], href="/edges", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-plus-circle"), " Nodes"], href="/nodes", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-link-45deg"), " Edge Types"], href="/edge-types", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-gear"), " Settings"], href="/settings", className="nav-link text-white")),
                        html.Li(html.A([html.I(className="bi bi-question-circle"), " Help"], href="/help", className="nav-link text-white")),
                    ], className="nav col-12 col-lg-auto justify-content-center my-md-0 text-small", role="navigation")
                ], className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start")
            ], className="container-fluid")
        ], className="text-bg-dark px-4 py-3")
    ], className="header")

def get_footer():
    return html.Footer([
        html.Div([
            # html.P("Created by Rail Engineering & Integration (REI) @ John Holland Group Pty. Ltd.", className="text-muted")
        ], className="container-fluid d-flex justify-content-end p-3")
    ], className="footer")

app.layout = html.Div([
    get_header(),
    html.Main([
        dash.page_container
    ], className="content"),
    get_footer()
])

if __name__ == '__main__':
    app.run(debug=True)