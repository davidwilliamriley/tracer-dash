# main.py

""" Main entry point for the Dash-based Tracer Application. """

# Imports
from dash import Dash
from models.model import Model
from views.view import View
from controllers.controller import Controller

import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

def create_app():
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = "Tracer"

    model = Model()
    controller = Controller(model, None)
    view = View(controller, app)
    controller.view = view

    app.layout = view.layout

    controller.register_callbacks(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)