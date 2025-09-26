# controllers/dashboards_controller.py

# Imports
from typing import Dict, Any, Optional
import pandas as pd
from dash import callback, Input, Output, State

class DashboardController:   
    def __init__(self, model):
        self.model = model
    
    def get_dashboard_data(self):
        pass