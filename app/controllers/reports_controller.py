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
        return [
            # {
            #     "label": "Select a Report...",
            #     "value": "",
            #     "disabled": True
            # },
            {
                "label": "System Requirements Specification",
                "value": "Report_00.pdf",
                "disabled": False
            },
            {
                "label": "System Definition",
                "value": "Report_01.pdf",
                "disabled": True
            },
            {
                "label": "System Breakdown Structure",
                "value": "Report_02.pdf",
                "disabled": True
            },
            {
                "label": "Interface Register",
                "value": "Report_03.pdf",
                "disabled": True
            },
            {
                "label": "Project Scope Allocation Matrix",
                "value": "Report_04.pdf",
                "disabled": False
            },
            {
                "label": "Assurance Case",
                "value": "Report_05.pdf",
                "disabled": True
            },
            {
                "label": "Safety Case",
                "value": "Report_06.pdf",
                "disabled": True
            },
            {
                "label": "Completions Checklist",
                "value": "Report_07.pdf",
                "disabled": True
            },
        ]