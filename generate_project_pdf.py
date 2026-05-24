import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib import colors

def get_tree_structure(dir_path, prefix=""):
    """Returns a string representation of the folder tree."""
    tree_str = ""
    if prefix == "":
        tree_str += f"{os.path.basename(dir_path)}/\n"
        
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return tree_str
        
    # filter out some dirs like __pycache__, .git
    entries = [e for e in entries if e not in ('.git', '__pycache__', '.venv', 'venv')]
    
    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        
        tree_str += f"{prefix}{connector}{entry}\n"
        
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            tree_str += get_tree_structure(path, prefix=prefix + extension)
            
    return tree_str

def create_project_pdf(project_dir, output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path, 
        pagesize=letter,
        leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30
    )
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    
    # Custom style for code
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.black,
        backColor=colors.whitesmoke,
        wordWrap='CJK', # Allows breaking long lines
    )
    
    tree_style = ParagraphStyle(
        'TreeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leading=12,
    )

    story = []
    
    # 1. Title
    story.append(Paragraph("Project Source Code and Structure", title_style))
    story.append(Spacer(1, 20))
    
    # 2. Directory Tree
    story.append(Paragraph("Directory Tree Structure", subtitle_style))
    story.append(Spacer(1, 10))
    
    tree_str = get_tree_structure(project_dir)
    story.append(Preformatted(tree_str, tree_style))
    story.append(PageBreak())
    
    # 3. Files Content
    files_to_include = [
        'README.md', 'requirements.txt', 'app.py', 'analytics_engine.py',
        'chart_builder.py', 'data_processor.py', 'gemini_handler.py',
        'pdf_generator.py', 'styles.py'
    ]
    
    for filename in files_to_include:
        filepath = os.path.join(project_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        story.append(Paragraph(f"File: {filename}", subtitle_style))
        story.append(Spacer(1, 10))
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Escape HTML characters for ReportLab
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Use Preformatted for preserving whitespace and formatting
            story.append(Preformatted(content, code_style))
        except Exception as e:
            story.append(Paragraph(f"Error reading file: {str(e)}", styles['Normal']))
            
        story.append(PageBreak())
        
    doc.build(story)
    print(f"PDF successfully generated at: {output_pdf_path}")

if __name__ == "__main__":
    project_dir = r"f:\6th sem minor\InsightFlow-v1"
    output_pdf = os.path.join(project_dir, "Project_Source_Code.pdf")
    create_project_pdf(project_dir, output_pdf)
