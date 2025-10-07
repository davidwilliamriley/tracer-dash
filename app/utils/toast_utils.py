# utils / toaster.py

import dash_bootstrap_components as dbc
from typing import Optional

class ToastFactory:
    """Utility class for creating standardized toast notifications."""
    
    @staticmethod
    def create_toast(
        toast_id: str = "toast-message",
        header: str = "Notification",
        is_open: bool = False,
        dismissable: bool = True,
        duration: int = 4000,
        position: Optional[dict] = None,
        **kwargs
    ) -> dbc.Toast:
        """
        Create a toast notification with default styling.
        
        Args:
            toast_id: Unique identifier for the toast
            header: Toast header text
            is_open: Whether toast is initially visible
            dismissable: Whether toast can be dismissed
            duration: Auto-dismiss duration in milliseconds
            position: Custom position dict (overrides default)
            **kwargs: Additional dbc.Toast properties
            
        Returns:
            dbc.Toast component
        """
        default_position = {
            "position": "fixed",
            "top": 100,
            "left": 20,
            "width": 350,
            "zindex": 9999,
        }
        
        style = position if position is not None else default_position
        
        return dbc.Toast(
            id=toast_id,
            header=header,
            is_open=is_open,
            dismissable=dismissable,
            duration=duration,
            style=style,
            **kwargs
        )