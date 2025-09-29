# pages/home.py
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from app.controllers.index_controller import Controller
from app.views.index_view import HomeView

dash.register_page(__name__, path='/')

def layout():
    return HomeView().get_layout()

