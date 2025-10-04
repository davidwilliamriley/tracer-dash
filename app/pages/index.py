# pages/index.py

# Imports
import dash

# MVC Imports
from views.index_view import IndexView

dash.register_page(__name__, path='/')

def layout():
    return IndexView().get_layout()