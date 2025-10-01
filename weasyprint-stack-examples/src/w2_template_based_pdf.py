#!/usr/bin/env python
"""
WeasyPrint Stack Example 2: Template-based PDF Generation
Uses Jinja2 templates with WeasyPrint for dynamic document generation.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
TEMPLATES_DIR = DATA / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True, parents=True)
OUT = BUILD / "out_w2_template_based.pdf"

# Sample data for template rendering
SAMPLE_DATA = {
    "company": {
        "name": "TechCorp Solutions",
        "logo": "logo.png",
        "address": "123 Business St, Tech City, TC 12345",
        "phone": "(555) 123-4567",
        "email": "info@techcorp.com"
    },
    "report": {
        "title": "Monthly Performance Report",
        "period": "November 2024",
        "generated_date": "December 1, 2024",
        "author": "Sarah Johnson",
        "version": "1.0"
    },
    "metrics": [
        {
            "name": "Revenue",
            "value": "$1,250,000",
            "change": "+12.5%",
            "status": "excellent"
        },
        {
            "name": "Active Users",
            "value": "45,230",
            "change": "+8.3%",
            "status": "good"
        },
        {
            "name": "Conversion Rate",
            "value": "3.2%",
            "change": "-0.1%",
            "status": "neutral"
        },
        {
            "name": "Customer Satisfaction",
            "value": "4.8/5",
            "change": "+0.2",
            "status": "excellent"
        }
    ],
    "projects": [
        {
            "name": "E-commerce Platform Redesign",
            "status": "completed",
            "completion_date": "Nov 15, 2024",
            "budget": "$180,000",
            "actual_cost": "$165,000",
            "roi": "340%"
        },
        {
            "name": "Mobile App Development",
            "status": "in_progress",
            "completion_date": "Jan 30, 2025",
            "budget": "$250,000",
            "actual_cost": "$198,000",
            "roi": "N/A"
        },
        {
            "name": "Data Analytics Dashboard",
            "status": "planning",
            "completion_date": "Mar 15, 2025",
            "budget": "$95,000",
            "actual_cost": "$0",
            "roi": "N/A"
        }
    ],
    "charts": {
        "revenue_trend": "revenue_trend.png",
        "user_growth": "user_growth.png"
    }
}


def create_html_template() -> Path:
    """Create HTML template with Jinja2 syntax."""
    template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ report.title }}</title>
    <style>
        @page {
            size: A4;
            margin: 2.5cm 2cm 2cm 2cm;
            @top-right {
                content: "{{ report.title }} - {{ report.period }}";
                font-size: 9pt;
                color: #666;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }

        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #333;
            margin: 0;
            padding: 0;
        }

        .header {
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20pt;
            margin-bottom: 30pt;
        }

        .company-info {
            display: table;
            width: 100%;
            margin-bottom: 20pt;
        }

        .company-name {
            display: table-cell;
            font-size: 24pt;
            font-weight: bold;
            color: #2c3e50;
            vertical-align: bottom;
        }

        .report-info {
            display: table-cell;
            text-align: right;
            vertical-align: bottom;
            font-size: 10pt;
            color: #666;
        }

        .report-title {
            font-size: 18pt;
            color: #34495e;
            margin: 15pt 0;
            font-weight: normal;
        }

        .section {
            margin-bottom: 25pt;
            page-break-inside: avoid;
        }

        .section h2 {
            font-size: 14pt;
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5pt;
            margin-bottom: 15pt;
            font-weight: bold;
        }

        .metrics-grid {
            display: table;
            width: 100%;
            border-collapse: collapse;
            margin: 20pt 0;
            page-break-inside: avoid;
        }

        .metric-row {
            display: table-row;
        }

        .metric-cell {
            display: table-cell;
            padding: 12pt;
            border: 1px solid #ddd;
            text-align: center;
            width: 25%;
            vertical-align: top;
        }

        .metric-name {
            font-size: 10pt;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
            margin-bottom: 8pt;
        }

        .metric-value {
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 5pt;
        }

        .metric-change {
            font-size: 9pt;
            padding: 2pt 6pt;
            border-radius: 3pt;
            display: inline-block;
        }

        .metric-change.excellent { background: #d4edda; color: #155724; }
        .metric-change.good { background: #d1ecf1; color: #0c5460; }
        .metric-change.neutral { background: #fff3cd; color: #856404; }
        .metric-change.warning { background: #f8d7da; color: #721c24; }

        .projects-table {
            display: table;
            width: 100%;
            border-collapse: collapse;
            margin: 20pt 0;
            font-size: 9pt;
        }

        .projects-header {
            display: table-row;
            background: #f8f9fa;
        }

        .projects-header > div {
            display: table-cell;
            padding: 8pt;
            font-weight: bold;
            border: 1px solid #ddd;
            text-align: left;
        }

        .project-row {
            display: table-row;
        }

        .project-row > div {
            display: table-cell;
            padding: 6pt 8pt;
            border: 1px solid #ddd;
            vertical-align: top;
        }

        .status-badge {
            display: inline-block;
            padding: 2pt 6pt;
            border-radius: 3pt;
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-completed { background: #d4edda; color: #155724; }
        .status-in_progress { background: #cce7ff; color: #004085; }
        .status-planning { background: #fff3cd; color: #856404; }

        .footer {
            margin-top: 40pt;
            padding-top: 15pt;
            border-top: 1px solid #bdc3c7;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }

        .disclaimer {
            background: #f8f9fa;
            padding: 10pt;
            border-left: 4pt solid #ffc107;
            margin: 20pt 0;
            font-size: 9pt;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="company-info">
            <div class="company-name">{{ company.name }}</div>
            <div class="report-info">
                Report Period: {{ report.period }}<br>
                Generated: {{ report.generated_date }}<br>
                Version: {{ report.version }}
            </div>
        </div>
        <div class="report-title">{{ report.title }}</div>
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <p>This report provides a comprehensive overview of {{ company.name }}'s performance during {{ report.period }}. All key metrics show positive trends, with particular strength in revenue growth and customer satisfaction.</p>

        <div class="disclaimer">
            <strong>Confidential:</strong> This document contains sensitive business information and should not be distributed without authorization.
        </div>
    </div>

    <div class="section">
        <h2>Key Performance Indicators</h2>

        <div class="metrics-grid">
            {% for metric in metrics %}
            <div class="metric-cell">
                <div class="metric-name">{{ metric.name }}</div>
                <div class="metric-value">{{ metric.value }}</div>
                <span class="metric-change {{ metric.status }}">{{ metric.change }}</span>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="section">
        <h2>Project Portfolio</h2>

        <div class="projects-table">
            <div class="projects-header">
                <div>Project Name</div>
                <div>Status</div>
                <div>Completion Date</div>
                <div>Budget</div>
                <div>Actual Cost</div>
                <div>ROI</div>
            </div>
            {% for project in projects %}
            <div class="project-row">
                <div>{{ project.name }}</div>
                <div><span class="status-badge status-{{ project.status }}">{{ project.status|replace('_', ' ') }}</span></div>
                <div>{{ project.completion_date }}</div>
                <div>{{ project.budget }}</div>
                <div>{{ project.actual_cost }}</div>
                <div>{{ project.roi }}</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="section">
        <h2>Strategic Outlook</h2>
        <p>{{ company.name }} continues to demonstrate strong performance across all operational areas. The completion of major projects and positive metric trends position the company for continued success in the coming quarters.</p>

        <p>Key focus areas for the next period include technology modernization, market expansion, and customer experience enhancement.</p>
    </div>

    <div class="footer">
        <div>{{ company.name }} | {{ company.address }}</div>
        <div>{{ company.phone }} | {{ company.email }}</div>
        <div>Report generated by automated systems | Author: {{ report.author }}</div>
    </div>
</body>
</html>
"""

    template_file = TEMPLATES_DIR / "report_template.html"
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_content)

    return template_file


def render_template_with_data(template_path: Path, data: Dict[str, Any]) -> str:
    """
    Render Jinja2 template with provided data.

    Args:
        template_path: Path to template file
        data: Data dictionary for template rendering

    Returns:
        Rendered HTML string
    """
    # Set up Jinja2 environment
    template_dir = template_path.parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template(template_path.name)

    # Render template
    return template.render(**data)


def convert_template_to_pdf(template_path: Path, data: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
    """
    Render template with data and convert to PDF using WeasyPrint.

    Args:
        template_path: Path to Jinja2 template
        data: Data for template rendering
        output_path: Optional output path

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        output_path = OUT

    print(f"📝 Rendering template: {template_path}")
    print("🔄 Processing data with Jinja2...")

    # Render template
    html_content = render_template_with_data(template_path, data)

    print("📄 Converting to PDF with WeasyPrint...")

    # Create HTML object from string
    html_doc = HTML(string=html_content)

    # Generate PDF
    html_doc.write_pdf(str(output_path))

    print(f"✅ Template-based PDF generated: {output_path}")
    return output_path


def main():
    """Entry point"""
    try:
        # Create template
        template_file = create_html_template()
        print(f"📄 Template created: {template_file}")

        # Render with sample data
        pdf_file = convert_template_to_pdf(template_file, SAMPLE_DATA)

        print("
🎉 Template-based PDF generation completed!"        print(f"   Template: {template_file}")
        print(f"   Data variables: {len(SAMPLE_DATA)}")
        print(f"   Output: {pdf_file}")

        print("
🎯 Template features demonstrated:"        print("   • Jinja2 templating with dynamic data")
        print("   • Complex CSS layouts and tables")
        print("   • Conditional styling and formatting")
        print("   • Professional document structure")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
