# controllers/reports_controller.py

from typing import Dict, Any, List

class ReportController:   
    def __init__(self, model):
        self.model = model
    
    def get_report_data(self):
        pass

    def get_pdf_viewer_url(self, selected_report: str) -> str:
        if not selected_report:
            return "/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/dummy.pdf"
        
        return f"/assets/pdfjs/pdfjs-4.8.69-dist/web/viewer.html?file=/assets/pdf/{selected_report}"
    
    def get_available_reports(self) -> List[Dict[str, Any]]:
        """
        Get list of available reports
        
        Returns:
            List of report options for dropdown
        """
        return [
            {
                "label": "Select a Report Option...",
                "value": "",
                "disabled": True
            },
            {
                "label": "Project Scope Allocation Matrix",
                "value": "Report_00.pdf",
            },
            {
                "label": "System Breakdown Structure",
                "value": "Report_02.pdf",
            },
            {
                "label": "Interface Register",
                "value": "Report_03.pdf",
            },
            {
                "label": "System Definition",
                "value": "Report_01.pdf",
            },
            {
                "label": "Assurance Case",
                "value": "Report_04.pdf",
            },
            {
                "label": "Safety Case",
                "value": "Report_05.pdf",
            },
            {
                "label": "Completions Checklist",
                "value": "Report_06.pdf",
            },
        ]