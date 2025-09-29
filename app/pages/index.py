# pages/index.py
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from views.index_view import IndexView

dash.register_page(__name__, path='/')

def layout():
    return IndexView().get_layout()