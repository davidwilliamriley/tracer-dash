# utils / toaster.py

import dash_bootstrap_components as dbc
from dash import html
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
        toast_type: Optional[str] = None,
        **kwargs
    ) -> dbc.Toast:
        """
        Create a toast notification with Bootstrap styling and icons.
        
        Args:
            toast_id: Unique identifier for the toast
            header: Toast header text
            is_open: Whether toast is initially visible
            dismissable: Whether toast can be dismissed
            duration: Auto-dismiss duration in milliseconds
            position: Custom position dict (overrides default)
            toast_type: Type for CSS styling (success, warning, danger, info)
            **kwargs: Additional dbc.Toast properties
            
        Returns:
            dbc.Toast component with custom header and no default icon
        """
        default_position = {
            "position": "fixed",
            "top": 100,
            "left": 20,
            "width": 350,
            "zindex": 9999,
        }
        
        style = position if position is not None else default_position
        
        # Add toast type class for CSS styling
        class_name = f"toast-{toast_type}" if toast_type else ""
        
        return dbc.Toast(
            id=toast_id,
            header=header,
            is_open=is_open,
            dismissable=dismissable,
            duration=duration,
            style=style,
            icon=None,  # Remove default icon
            className=class_name,
            **kwargs
        )
    
    @staticmethod
    def create_success_header(message: str = "Success") -> html.Div:
        """Create a success header with Bootstrap icon."""
        return html.Div(
            [
                html.I(className="bi bi-check-circle-fill me-2"),
                message
            ],
            className="header-content"
        )
    
    @staticmethod
    def create_error_header(message: str = "Error") -> html.Div:
        """Create an error header with Bootstrap icon."""
        return html.Div(
            [
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                message
            ],
            className="header-content"
        )
    
    @staticmethod
    def create_warning_header(message: str = "Warning") -> html.Div:
        """Create a warning header with Bootstrap icon."""
        return html.Div(
            [
                html.I(className="bi bi-exclamation-circle-fill me-2"),
                message
            ],
            className="header-content"
        )
    
    @staticmethod
    def create_info_header(message: str = "Information") -> html.Div:
        """Create an info header with Bootstrap icon."""
        return html.Div(
            [
                html.I(className="bi bi-info-circle-fill me-2"),
                message
            ],
            className="header-content"
        )
    
    @staticmethod
    def get_header_by_type(header_type: str, message: Optional[str] = None) -> html.Div:
        """Get header component by type string."""
        default_messages = {
            "success": "Success",
            "warning": "Warning", 
            "danger": "Error",
            "error": "Error",
            "info": "Information"
        }
        
        header_message = message or default_messages.get(header_type, "Notification")
        
        if header_type == "success":
            return ToastFactory.create_success_header(header_message)
        elif header_type in ["warning"]:
            return ToastFactory.create_warning_header(header_message)
        elif header_type in ["danger", "error"]:
            return ToastFactory.create_error_header(header_message)
        elif header_type == "info":
            return ToastFactory.create_info_header(header_message)
        else:
            # Default fallback
            return ToastFactory.create_info_header(header_message)