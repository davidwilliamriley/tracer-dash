# controllers/breakdowns_controller.py

# Imports
from typing import Dict, Any, Optional
import pandas as pd
from dash import callback, Input, Output, State

class BreakdownController:   
    def __init__(self, model):
        self.model = model
    
    def get_breakdown_data(self):
        pass