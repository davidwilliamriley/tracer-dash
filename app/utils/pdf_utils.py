# utils/pdf_generator.py

import io
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional, Union 
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import stringWidth

class NumberedCanvas:
    def __init__(self):
        self.page_count = 0

def _header_footer(canvas, doc, title: str, filename: str, page_tracker):
    canvas.saveState()

    width, height = landscape(A3)

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(30, height - 30, title)

    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(width - 30, height - 30, filename)
        
    page_num = canvas.getPageNumber()

    if page_num > page_tracker.page_count:
        page_tracker.page_count = page_num    
    
    footer_text = f"Page {page_num} of Pages"
    canvas.drawRightString(width - 30, 30, footer_text)
    
    canvas.restoreState()

def _final_header_footer(canvas, doc, title: str, filename: str, total_pages: int):
    canvas.saveState()

    width, height = landscape(A3)

    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(30, height - 30, title)

    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(width - 30, height - 30, filename)

    canvas.setFont('Helvetica', 10)
    page_num = canvas.getPageNumber()

    footer_text = f"Page {page_num} of {total_pages} Pages"
    canvas.drawRightString(width - 30, 30, footer_text)

    canvas.restoreState()

def _calculate_col_widths(table_data: List[List[Any]], available_width: float, num_columns: int) -> List[float]:
    item_width: float = 40.0
    cell_padding: float = 20.0

    col_widths: List[float] = [item_width]

    expanding_column_idx = 2

    for col_idx in range(1, num_columns):
        if col_idx == expanding_column_idx:
            col_widths.append(0.0)
            continue

        max_width: float = 0.0
        for row in table_data:
            if col_idx < len(row):
                text = str(row[col_idx])
                if table_data.index(row) == 0:
                    text_width = stringWidth(text, 'Helvetica-Bold', 10)
                else:
                    text_width = stringWidth(text, 'Helvetica', 10)
                max_width = max(max_width, text_width)
        
        col_widths.append(max_width + cell_padding)
    
    used_width: float = sum(w for i, w in enumerate(col_widths) if i != expanding_column_idx)
    remaining_width: float = available_width - used_width
    
    # Ensure last column has at least some Minimum Width
    expanding_col_width: float = max(remaining_width, 100.0)
    col_widths[expanding_column_idx] = expanding_col_width

    return col_widths
    
def generate_table_pdf(data: List[Dict[str, Any]], title: str, columns_to_exclude: Optional[List[str]] = None, filename: str = "table_export") -> Dict[str, Any]:
    """Generate a PDF from Table Data"""
    if columns_to_exclude is None:
        columns_to_exclude = []
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Remove excluded columns
    for col in columns_to_exclude:
        if col in df.columns:
            df = df.drop(col, axis=1)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{timestamp}_{filename}.pdf"

    page_width, page_height = landscape(A3)
    available_width = page_width - 60
    
    # Create PDF in Memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A3),
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=40,
    )
    
    # Container for Flowable
    elements = []
    
    # Add the Title
    styles = getSampleStyleSheet()
    # title_para = Paragraph(f"<b>{title}</b>", styles['Title'])
    # elements.append(title_para)
    elements.append(Spacer(1, 12))

    num_columns = len(df.columns) + 1
    
    header_row = ["Item"] + df.columns.tolist()
    
    # Prepare the Table Data
    table_data = [header_row]
    for idx, row in enumerate(df.values.tolist(), start=1):
        table_data.append([str(idx)] + row)
    
    # col_widths = [available_width / num_columns] * num_columns
    col_widths = _calculate_col_widths(table_data, available_width, num_columns)

    # Create Table
    t = Table(table_data, colWidths=col_widths, repeatRows=1)

    header_blue = colors.HexColor("#0d6efd")
    alt_row_color = colors.HexColor('#D9E2F3')
    
    # Add Style to the Table
    page_styles = [
        # Header Styling
        ('BACKGROUND', (0, 0), (-1, 0), header_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Body Styling (Rows 1+)
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, alt_row_color])
    ]
    
    elements.append(t)

    page_tracker = NumberedCanvas()
    doc.build(
        elements,
        onFirstPage=lambda c, d: _header_footer(c, d, title, filename, page_tracker),
        onLaterPages=lambda c, d: _header_footer(c, d, title, filename, page_tracker)
    )
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A3),
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=40,
    )

    elements = []
    # title_para = Paragraph(f"<b>{title}</b>", styles['Title'])
    # elements.append(title_para)
    elements.append(Spacer(1, 12))

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(page_styles))
    elements.append(t)

    total_pages = page_tracker.page_count
    doc.build(
        elements,
        onFirstPage=lambda c, d: _final_header_footer(c, d, title, filename, total_pages),
        onLaterPages=lambda c, d: _final_header_footer(c, d, title, filename, total_pages)
    )   

    # Encode to base64
    buffer.seek(0)
    pdf_data = buffer.read()
    encoded = base64.b64encode(pdf_data).decode('utf-8')
        
    return {
        "content": encoded,
        "filename": filename,
        "base64": True
    }

# Generate Breakdown PDF

def generate_breakdown_pdf(
    data: List[Dict[str, Any]], 
    title: str, 
    filename: str = "breakdown_export"
) -> Dict[str, Any]:
    """Generate a PDF from hierarchical breakdown data with indentation"""
    
    def flatten_hierarchy(items: List[Dict[str, Any]], level: int = 0) -> List[Dict[str, Any]]:
        """Flatten hierarchical data while preserving tree structure with indentation"""
        flattened = []
        
        for item in items:
            # Create a copy of the item
            flat_item = {
                'level': level,
                'Element': item.get('Element', ''),
                'Relation': item.get('Relation', ''),
                'Weight': item.get('Weight', ''),
                'Identifier': item.get('Identifier', ''),
                'Name': item.get('Name', ''),
                'Description': item.get('Description', '')
            }
            flattened.append(flat_item)
            
            # Process children recursively
            children = item.get('_children', [])
            if children:
                flattened.extend(flatten_hierarchy(children, level + 1))
        
        return flattened
    
    # Flatten the hierarchical data
    flat_data = flatten_hierarchy(data)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{timestamp}_{filename}.pdf"

    page_width, page_height = landscape(A3)
    available_width = page_width - 60
    
    # Create PDF in Memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A3),
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=40,
    )
    
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Spacer(1, 12))

    # Define columns (Element renamed to Item, no separate Item number column)
    columns = ['Item', 'Relation', 'Weight', 'Identifier', 'Name', 'Description']
    header_row = columns
    
    # Prepare the Table Data with indentation
    table_data = [header_row]
    
    for row_data in flat_data:
        level = row_data['level']
        indent = '    ' * level  # 4 spaces per level
        
        # Add indentation to the Item column (formerly Element)
        item_text = indent + row_data['Element']
        
        row = [
            item_text,  # Item (with indentation)
            row_data['Relation'],
            row_data['Weight'],
            row_data['Identifier'],
            row_data['Name'],
            row_data['Description']
        ]
        table_data.append(row)
    
    # Calculate column widths for breakdown (Item column needs special handling for indentation)
    num_columns = len(columns)
    
    cell_padding = 20.0
    col_widths = []
    
    # Item column - wider to accommodate indentation (formerly Element column)
    col_widths.append(120)  # Fixed width for indented items
    
    # Relation, Weight, Identifier - fit to content
    for col_idx in [1, 2, 3]:  # Relation, Weight, Identifier
        max_width = 0.0
        for row in table_data:
            if col_idx < len(row):
                text = str(row[col_idx])
                if table_data.index(row) == 0:
                    text_width = stringWidth(text, 'Helvetica-Bold', 10)
                else:
                    text_width = stringWidth(text, 'Helvetica', 10)
                max_width = max(max_width, text_width)
        col_widths.append(max_width + cell_padding)
    
    # Name & Description - split remaining space
    used_width = sum(col_widths)
    remaining_width = available_width - used_width
    col_widths.append(max(remaining_width * 0.4, 100.0))  # Name gets 40%
    col_widths.append(max(remaining_width * 0.6, 150.0))  # Description gets 60%

    # Create Table
    t = Table(table_data, colWidths=col_widths, repeatRows=1)

    header_blue = colors.HexColor("#0d6efd")
    alt_row_color = colors.HexColor('#D9E2F3')
    
    # Add Style to the Table (matching table report format)
    table_style = [
        # Header Styling
        ('BACKGROUND', (0, 0), (-1, 0), header_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Body Styling (matching table report - use Helvetica not Courier)
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                
        # Alternating row colors (matching table report)
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, alt_row_color])
    ]
    
    t.setStyle(TableStyle(table_style))
    elements.append(t)

    # Build PDF with page numbers
    page_tracker = NumberedCanvas()
    doc.build(
        elements,
        onFirstPage=lambda c, d: _header_footer(c, d, title, filename, page_tracker),
        onLaterPages=lambda c, d: _header_footer(c, d, title, filename, page_tracker)
    )
    
    # Rebuild with correct page count
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A3),
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=40,
    )

    elements = []
    elements.append(Spacer(1, 12))
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(table_style))
    elements.append(t)

    total_pages = page_tracker.page_count
    doc.build(
        elements,
        onFirstPage=lambda c, d: _final_header_footer(c, d, title, filename, total_pages),
        onLaterPages=lambda c, d: _final_header_footer(c, d, title, filename, total_pages)
    )   

    # Encode to base64
    buffer.seek(0)
    pdf_data = buffer.read()
    encoded = base64.b64encode(pdf_data).decode('utf-8')
        
    return {
        "content": encoded,
        "filename": filename,
        "base64": True
    }