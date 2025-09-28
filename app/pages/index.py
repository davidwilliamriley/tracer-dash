# pages/home.py
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from controllers.app_controller import Controller
from views.app_view import View

dash.register_page(__name__, path='/')

def layout():
    return View().get_layout()

