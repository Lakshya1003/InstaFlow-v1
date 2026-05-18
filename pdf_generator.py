"""
Insta Flow — PDF Report Generator
Generates professional executive-style PDF reports using ReportLab.
Always uses ALL-TIME date range regardless of current dashboard filter.
"""
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

BRAND_BLUE = colors.HexColor('#2563eb')
BRAND_DARK = colors.HexColor('#1e293b')
BRAND_GRAY = colors.HexColor('#64748b')
BRAND_LIGHT = colors.HexColor('#f8fafc')
BRAND_BORDER = colors.HexColor('#e2e8f0')


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold',
        fontSize=22, textColor=BRAND_DARK, spaceAfter=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='ReportSubtitle', fontName='Helvetica',
        fontSize=10, textColor=BRAND_GRAY, spaceAfter=20, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='SectionHead', fontName='Helvetica-Bold',
        fontSize=13, textColor=BRAND_BLUE, spaceBefore=16, spaceAfter=8))
    styles.add(ParagraphStyle(name='BodyText2', fontName='Helvetica',
        fontSize=9.5, textColor=BRAND_DARK, leading=14, spaceAfter=6))
    styles.add(ParagraphStyle(name='SmallGray', fontName='Helvetica',
        fontSize=8, textColor=BRAND_GRAY, alignment=TA_CENTER))
    return styles


def generate_pdf_report(df, date_col, numeric_cols, categorical_cols,
                        kpis, analytics_summary, ai_summary, chart_figures=None):
    """Generate a professional PDF report. Returns bytes buffer."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm, topMargin=20*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    # Title
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Insta Flow", styles['ReportTitle']))
    elements.append(Paragraph("AI-Assisted Business Analytics Report", styles['ReportSubtitle']))
    elements.append(HRFlowable(width="100%", thickness=1, color=BRAND_BORDER))
    elements.append(Spacer(1, 12))

    date_min = df[date_col].min().strftime('%B %d, %Y')
    date_max = df[date_col].max().strftime('%B %d, %Y')
    gen_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    meta_data = [
        ['Report Type', 'All-Time Business Analytics'],
        ['Analysis Period', f'{date_min} — {date_max}'],
        ['Total Records', f'{len(df):,}'],
        ['Generated On', gen_date],
    ]
    meta_table = Table(meta_data, colWidths=[120, 340])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), BRAND_GRAY),
        ('TEXTCOLOR', (1,0), (1,-1), BRAND_DARK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 20))

    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['SectionHead']))
    if ai_summary:
        for line in ai_summary.split('\n'):
            line = line.strip()
            if line:
                line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                line = line.lstrip('*-– ')
                elements.append(Paragraph(f"  {line}", styles['BodyText2']))
    else:
        elements.append(Paragraph("AI summary not available. Connect Gemini API for insights.", styles['BodyText2']))
    elements.append(Spacer(1, 10))

    # KPI Table
    elements.append(Paragraph("Key Performance Indicators", styles['SectionHead']))
    kpi_rows = [['Metric', 'Total', 'Average', 'Min', 'Max']]
    for col, vals in kpis.items():
        kpi_rows.append([col, f"{vals['total']:,.2f}", f"{vals['mean']:,.2f}",
                         f"{vals['min']:,.2f}", f"{vals['max']:,.2f}"])

    kpi_table = Table(kpi_rows, colWidths=[100, 95, 95, 85, 85])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BRAND_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR', (0,1), (-1,-1), BRAND_DARK),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BRAND_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BRAND_LIGHT]),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 12))

    # Analytics Details
    elements.append(Paragraph("Detailed Analytics", styles['SectionHead']))
    for line in analytics_summary.split('\n'):
        line = line.strip()
        if line:
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(line, styles['BodyText2']))
    elements.append(Spacer(1, 10))

    # Charts
    if chart_figures:
        elements.append(PageBreak())
        elements.append(Paragraph("Visual Analytics", styles['SectionHead']))
        for i, fig in enumerate(chart_figures):
            try:
                img_bytes = fig.to_image(format="png", width=800, height=400, scale=2)
                img_buf = io.BytesIO(img_bytes)
                img = Image(img_buf, width=460, height=230)
                elements.append(img)
                elements.append(Spacer(1, 14))
            except Exception:
                elements.append(Paragraph(f"Chart {i+1} could not be rendered.", styles['BodyText2']))

    # Footer
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_BORDER))
    elements.append(Paragraph(
        f"Generated by Insta Flow Analytics  {gen_date}  All-Time Analysis",
        styles['SmallGray']))

    doc.build(elements)
    buf.seek(0)
    return buf
