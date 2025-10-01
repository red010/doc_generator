#!/usr/bin/env python
"""
WeasyPrint Stack Example 1: Basic HTML to PDF
Converts HTML content to PDF using WeasyPrint for print-optimized layouts.
"""

from pathlib import Path
from typing import Optional
from weasyprint import HTML, CSS

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
HTML_DIR = DATA / "html"
CSS_DIR = DATA / "css"
CSS_DIR.mkdir(exist_ok=True, parents=True)
OUT = BUILD / "out_w1_basic.pdf"

# HTML content with print-optimized CSS
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Professional Report</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @top-center {
                content: "Professional Report";
                font-size: 10pt;
                font-weight: bold;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
            }
        }

        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #333;
            max-width: none;
        }

        .header {
            text-align: center;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20pt;
            margin-bottom: 30pt;
        }

        .header h1 {
            font-size: 24pt;
            color: #2c3e50;
            margin: 0;
            font-weight: normal;
        }

        .header .subtitle {
            font-size: 14pt;
            color: #7f8c8d;
            margin: 10pt 0 0 0;
        }

        .metadata {
            text-align: center;
            font-size: 10pt;
            color: #666;
            margin-bottom: 40pt;
        }

        .section {
            margin-bottom: 25pt;
        }

        .section h2 {
            font-size: 16pt;
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5pt;
            margin-bottom: 15pt;
            font-weight: normal;
        }

        .content {
            text-align: justify;
            margin-bottom: 15pt;
        }

        .highlight {
            background-color: #f8f9fa;
            padding: 10pt;
            border-left: 4pt solid #3498db;
            margin: 15pt 0;
        }

        .metrics {
            display: table;
            width: 100%;
            margin: 20pt 0;
            border-collapse: collapse;
        }

        .metric-row {
            display: table-row;
        }

        .metric-cell {
            display: table-cell;
            padding: 8pt;
            border: 1px solid #ddd;
            text-align: center;
            width: 25%;
        }

        .metric-value {
            font-size: 18pt;
            font-weight: bold;
            color: #e74c3c;
        }

        .metric-label {
            font-size: 9pt;
            color: #666;
            text-transform: uppercase;
        }

        .footer {
            margin-top: 40pt;
            padding-top: 20pt;
            border-top: 1px solid #bdc3c7;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Professional Report</h1>
        <div class="subtitle">Q4 2024 Performance Analysis</div>
    </div>

    <div class="metadata">
        Generated: December 31, 2024 | Confidential
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <div class="content">
            This comprehensive report analyzes organizational performance for the fourth quarter of 2024. Our analysis reveals significant achievements across multiple key performance indicators, demonstrating strong operational excellence and strategic growth.
        </div>

        <div class="highlight">
            <strong>Key Achievement:</strong> The organization exceeded all quarterly targets by an average of 15%, setting new records in customer satisfaction and operational efficiency.
        </div>
    </div>

    <div class="section">
        <h2>Performance Metrics</h2>

        <div class="metrics">
            <div class="metric-row">
                <div class="metric-cell">
                    <div class="metric-value">$2.4M</div>
                    <div class="metric-label">Revenue</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-value">94%</div>
                    <div class="metric-label">Satisfaction</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-value">1.2M</div>
                    <div class="metric-label">Users</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-value">99.9%</div>
                    <div class="metric-label">Uptime</div>
                </div>
            </div>
        </div>

        <div class="content">
            Our performance metrics demonstrate consistent excellence across all operational domains. Revenue growth of 18% quarter-over-quarter reflects successful market penetration strategies and enhanced product offerings.
        </div>
    </div>

    <div class="section">
        <h2>Strategic Initiatives</h2>
        <div class="content">
            Several strategic initiatives were launched during Q4, focusing on digital transformation and customer experience enhancement. These initiatives include:
        </div>

        <div class="content">
            <strong>Digital Transformation:</strong> Implementation of advanced analytics platforms and automation tools resulted in 30% improvement in operational efficiency.
        </div>

        <div class="content">
            <strong>Customer Experience:</strong> Launch of personalized service offerings increased customer retention by 25% and improved satisfaction scores.
        </div>
    </div>

    <div class="section">
        <h2>Future Outlook</h2>
        <div class="content">
            Looking ahead to 2025, the organization is well-positioned for continued success. Strategic investments in emerging technologies and market expansion will drive sustained growth and competitive advantage.
        </div>
    </div>

    <div class="footer">
        This report was generated using WeasyPrint | All rights reserved © 2024
    </div>
</body>
</html>
"""


def create_html_file() -> Path:
    """Create HTML file for conversion."""
    HTML_DIR.mkdir(exist_ok=True, parents=True)
    html_file = HTML_DIR / "professional_report.html"

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)

    return html_file


def convert_html_to_pdf(html_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert HTML to PDF using WeasyPrint with print-optimized CSS.

    Args:
        html_path: Path to input HTML file
        output_path: Optional output path, defaults to OUT

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        output_path = OUT

    print(f"🌐 Converting HTML to PDF: {html_path}")

    try:
        # Create HTML object
        html_doc = HTML(filename=str(html_path))

        # Generate PDF
        print("📄 Generating PDF with WeasyPrint...")
        html_doc.write_pdf(str(output_path))

        print(f"✅ PDF generated successfully: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ WeasyPrint conversion failed: {e}")
        raise


def convert_html_string_to_pdf(html_string: str, output_path: Optional[Path] = None) -> Path:
    """
    Convert HTML string directly to PDF.

    Args:
        html_string: HTML content as string
        output_path: Optional output path

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        output_path = BUILD / "out_w1_string_to_pdf.pdf"

    print("🔤 Converting HTML string to PDF...")

    try:
        # Create HTML object from string
        html_doc = HTML(string=html_string)

        # Generate PDF
        html_doc.write_pdf(str(output_path))

        print(f"✅ PDF from string generated: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ String conversion failed: {e}")
        raise


def main():
    """Entry point"""
    try:
        # Create HTML file
        html_file = create_html_file()
        print(f"📄 HTML file created: {html_file}")

        # Convert file to PDF
        pdf_file = convert_html_to_pdf(html_file)
        print("
🎉 File conversion completed!"        print(f"   Input: {html_file}")
        print(f"   Output: {pdf_file}")

        # Also demonstrate string conversion
        pdf_from_string = convert_html_to_pdf.__wrapped__.__defaults__[0].parent / "demo_string.pdf"
        convert_html_string_to_pdf(HTML_CONTENT, pdf_from_string)
        print("
📝 String conversion completed!"        print(f"   Output: {pdf_from_string}")

        print("
🎯 WeasyPrint features demonstrated:"        print("   • Print-optimized CSS (@page rules)")
        print("   • Automatic page headers/footers")
        print("   • Professional typography")
        print("   • Table-based layouts")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
