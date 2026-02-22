"""
Automated Report Generation Script
Reads data from CSV file, analyzes it, and generates a formatted PDF report
"""

import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors


def read_data(filename):
    """Read data from CSV file"""
    data = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f"✓ Read {len(data)} records from {filename}")
        return data
    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
        return []


def analyze_data(data):
    """Analyze the data and return statistics"""
    if not data:
        return None
    
    analysis = {
        'total_records': len(data),
        'columns': list(data[0].keys())
    }
    
    # Try to calculate numeric statistics
    for col in analysis['columns']:
        try:
            values = [float(row[col]) for row in data if row[col]]
            analysis[col] = {
                'average': sum(values) / len(values),
                'max': max(values),
                'min': min(values),
                'total': sum(values)
            }
        except (ValueError, TypeError):
            # Not numeric, skip
            pass
    
    print("✓ Data analysis completed")
    return analysis


def create_pdf_report(filename, data, analysis):
    """Create a formatted PDF report"""
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1  # center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e5c8a'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Add title
    elements.append(Paragraph("📊 Automated Data Report", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add metadata
    meta_text = f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><b>Total Records:</b> {analysis['total_records']}"
    elements.append(Paragraph(meta_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add summary statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    # Create statistics table
    stat_data = [['Metric', 'Value']]
    for col, stats in analysis.items():
        if isinstance(stats, dict) and 'average' in stats:
            stat_data.append([f"{col} (Avg)", f"{stats['average']:.2f}"])
            stat_data.append([f"{col} (Max)", f"{stats['max']:.2f}"])
            stat_data.append([f"{col} (Min)", f"{stats['min']:.2f}"])
    
    if len(stat_data) > 1:
        stat_table = Table(stat_data, colWidths=[3*inch, 2*inch])
        stat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(stat_table)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Add data table
    elements.append(Paragraph("Data Records", heading_style))
    
    # Create data table (limit to first 10 rows for readability)
    table_data = [list(data[0].keys())]
    for row in data[:10]:
        table_data.append(list(row.values()))
    
    data_table = Table(table_data, colWidths=[5.5*inch / len(data[0])] * len(data[0]))
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(data_table)
    
    # Add footer note
    elements.append(Spacer(1, 0.3*inch))
    if len(data) > 10:
        footer_text = f"<i>Showing first 10 of {len(data)} total records</i>"
        elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"✓ PDF report created: {filename}")


def main():
    """Main execution"""
    print("\n" + "="*50)
    print("  AUTOMATED REPORT GENERATOR")
    print("="*50 + "\n")
    
    # Input and output files
    input_file = "sample_data.csv"
    output_file = "report.pdf"
    
    # Execute pipeline
    data = read_data(input_file)
    if data:
        analysis = analyze_data(data)
        create_pdf_report(output_file, data, analysis)
        print("\n✓ Report generation completed!\n")
    else:
        print("\n✗ Cannot generate report without data\n")


if __name__ == "__main__":
    main()