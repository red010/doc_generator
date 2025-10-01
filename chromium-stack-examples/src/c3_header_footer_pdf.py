#!/usr/bin/env python
"""
Chromium Stack Example 3: PDF with Custom Headers and Footers
Generates PDF with HTML headers, footers, and page numbering.
"""

from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright
from datetime import datetime

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
OUT = BUILD / "out_c3_header_footer.pdf"

# HTML content with multiple pages to demonstrate headers/footers
REPORT_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Annual Report 2024</title>
    <style>
        @page {{
            size: A4;
            margin: 2in 1in 1.5in 1in;  /* Space for header/footer */
        }}

        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            font-size: 12pt;
        }}

        .title-page {{
            text-align: center;
            margin-top: 3in;
            page-break-after: always;
        }}

        .title-page h1 {{
            font-size: 36pt;
            margin-bottom: 0.5in;
            color: #2c3e50;
        }}

        .title-page .subtitle {{
            font-size: 18pt;
            color: #7f8c8d;
            margin-bottom: 1in;
        }}

        .title-page .meta {{
            font-size: 14pt;
            color: #34495e;
        }}

        .section {{
            margin-bottom: 1in;
            page-break-inside: avoid;
        }}

        .section h2 {{
            font-size: 24pt;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10pt;
            margin-bottom: 20pt;
            page-break-after: avoid;
        }}

        .section h3 {{
            font-size: 18pt;
            color: #34495e;
            margin-top: 30pt;
            margin-bottom: 15pt;
            page-break-after: avoid;
        }}

        .content {{
            text-align: justify;
            margin-bottom: 20pt;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20pt;
            margin: 30pt 0;
            page-break-inside: avoid;
        }}

        .stat-box {{
            border: 1px solid #bdc3c7;
            border-radius: 8pt;
            padding: 20pt;
            text-align: center;
            background: #f8f9fa;
        }}

        .stat-number {{
            font-size: 28pt;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 5pt;
        }}

        .stat-label {{
            font-size: 12pt;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 1pt;
        }}

        .break-before {{
            page-break-before: always;
        }}

        .break-after {{
            page-break-after: always;
        }}

        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20pt 0;
            page-break-inside: avoid;
        }}

        .table th, .table td {{
            border: 1px solid #bdc3c7;
            padding: 8pt;
            text-align: left;
        }}

        .table th {{
            background: #34495e;
            color: white;
            font-weight: bold;
        }}

        .table tbody tr:nth-child(even) {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <h1>Annual Report 2024</h1>
        <div class="subtitle">Performance & Achievements</div>
        <div class="meta">
            <div>Generated: {datetime.now().strftime('%B %d, %Y')}</div>
            <div>Company: TechCorp Inc.</div>
        </div>
    </div>

    <!-- Executive Summary -->
    <div class="section">
        <h2>Executive Summary</h2>
        <div class="content">
            <p>This comprehensive annual report covers the fiscal year 2024, highlighting key achievements, financial performance, and strategic initiatives that have positioned TechCorp Inc. as a leader in the technology sector.</p>

            <p>Throughout the year, we achieved significant milestones in innovation, market expansion, and operational excellence, resulting in record-breaking revenue growth and customer satisfaction metrics.</p>
        </div>

        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-number">$2.4B</div>
                <div class="stat-label">Annual Revenue</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">45%</div>
                <div class="stat-label">Year-over-Year Growth</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">15K</div>
                <div class="stat-label">New Customers</div>
            </div>
            <div class="stat-box">
                <div class="stat-box">
                <div class="stat-number">98%</div>
                <div class="stat-label">Customer Satisfaction</div>
            </div>
        </div>
    </div>

    <div class="break-before"></div>

    <!-- Financial Performance -->
    <div class="section">
        <h2>Financial Performance</h2>

        <h3>Revenue Breakdown</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Quarter</th>
                    <th>Revenue ($M)</th>
                    <th>Growth (%)</th>
                    <th>Margin (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Q1 2024</td>
                    <td>520</td>
                    <td>+12%</td>
                    <td>28%</td>
                </tr>
                <tr>
                    <td>Q2 2024</td>
                    <td>580</td>
                    <td>+18%</td>
                    <td>31%</td>
                </tr>
                <tr>
                    <td>Q3 2024</td>
                    <td>640</td>
                    <td>+22%</td>
                    <td>29%</td>
                </tr>
                <tr>
                    <td>Q4 2024</td>
                    <td>660</td>
                    <td>+15%</td>
                    <td>32%</td>
                </tr>
            </tbody>
        </table>

        <h3>Key Financial Metrics</h3>
        <div class="content">
            <p>Our financial performance in 2024 demonstrated robust growth across all major indicators. The company's strategic investments in emerging technologies and market expansion initiatives contributed to a 45% increase in annual revenue, reaching $2.4 billion.</p>

            <p>Operating margins improved significantly, reflecting enhanced operational efficiency and cost management strategies implemented throughout the year.</p>
        </div>
    </div>

    <div class="break-before"></div>

    <!-- Strategic Initiatives -->
    <div class="section">
        <h2>Strategic Initiatives</h2>

        <h3>Product Innovation</h3>
        <div class="content">
            <p>In 2024, we launched three major product lines and introduced over 50 new features across our existing platforms. Our AI-powered analytics suite received industry recognition for its innovative approach to business intelligence.</p>
        </div>

        <h3>Market Expansion</h3>
        <div class="content">
            <p>We successfully expanded into five new international markets, establishing regional headquarters in Asia-Pacific and European Union regions. This strategic expansion increased our global presence by 35%.</p>
        </div>

        <h3>Sustainability</h3>
        <div class="content">
            <p>Environmental responsibility remained a core focus, with the company achieving carbon neutrality across all data centers and reducing overall energy consumption by 28% through innovative cooling technologies.</p>
        </div>
    </div>

    <div class="break-before"></div>

    <!-- Future Outlook -->
    <div class="section">
        <h2>Future Outlook</h2>
        <div class="content">
            <p>Looking ahead to 2025, TechCorp Inc. is well-positioned for continued success. Our pipeline of innovative products and strategic market positions provide a strong foundation for sustained growth and market leadership.</p>

            <p>We remain committed to delivering exceptional value to our customers while maintaining our position as an industry innovator and responsible corporate citizen.</p>
        </div>
    </div>
</body>
</html>
"""

# Header and Footer templates
HEADER_TEMPLATE = """
<div style="font-size: 10px; width: 100%; text-align: center; font-family: Arial, sans-serif; color: #666;">
    <span style="font-weight: bold;">TechCorp Inc. - Annual Report 2024</span>
</div>
"""

FOOTER_TEMPLATE = """
<div style="font-size: 10px; width: 100%; text-align: center; font-family: Arial, sans-serif; color: #666;">
    <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    <br>
    <span>Confidential - Internal Use Only</span>
</div>
"""


def generate_report_with_headers_footers(output_path: Optional[Path] = None) -> Path:
    """
    Generate a professional report PDF with custom headers and footers.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated PDF file.
    """
    if output_path is None:
        output_path = OUT

    print("📄 Generating professional report with headers/footers...")
    print("🔧 Setting up page layout and styling...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set content
        page.set_content(REPORT_HTML)

        # Wait for content to load
        page.wait_for_load_state('networkidle')

        # Generate PDF with headers and footers
        print("📋 Adding headers and footers...")
        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=HEADER_TEMPLATE,
            footer_template=FOOTER_TEMPLATE,
            margin={
                "top": "1.5in",     # Space for header
                "bottom": "1.2in",  # Space for footer
                "left": "1in",
                "right": "1in"
            }
        )

        browser.close()

    print(f"✅ Professional report PDF generated: {output_path}")
    return output_path


def main():
    """Entry point"""
    try:
        result = generate_report_with_headers_footers()
        print("
🎉 Professional report generated!"        print(f"   Output: {result}")
        print("   Features: Custom headers, footers, page numbering, multi-page layout"
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
