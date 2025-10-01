#!/usr/bin/env python
"""
WeasyPrint Stack Example 3: External Resources and Assets
Demonstrates handling of external CSS, images, and fonts in PDF generation.
"""

from pathlib import Path
from typing import Optional
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
ASSETS_DIR = DATA / "assets"
ASSETS_DIR.mkdir(exist_ok=True, parents=True)
OUT = BUILD / "out_w3_external_resources.pdf"

# Create sample CSS file
EXTERNAL_CSS = """
/* Professional stylesheet for business reports */
@page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2cm;
    @top-left {
        content: "Confidential Report";
        font-size: 8pt;
        color: #666;
    }
    @top-right {
        content: "Page " counter(page);
        font-size: 8pt;
        color: #666;
    }
    @bottom-center {
        content: "© 2024 TechCorp Solutions";
        font-size: 7pt;
        color: #999;
    }
}

/* Import Google Fonts (WeasyPrint can handle web fonts) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #2d3748;
    background: white;
    margin: 0;
    padding: 0;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30pt 0;
    text-align: center;
    margin-bottom: 30pt;
}

.header h1 {
    font-size: 24pt;
    font-weight: 600;
    margin: 0 0 10pt 0;
    letter-spacing: -0.5pt;
}

.header .tagline {
    font-size: 12pt;
    opacity: 0.9;
    font-weight: 400;
}

.content-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30pt;
    margin-bottom: 40pt;
}

.main-content {
    background: white;
    padding: 25pt;
    border-radius: 8pt;
    box-shadow: 0 2pt 8pt rgba(0, 0, 0, 0.1);
}

.sidebar {
    background: #f7fafc;
    padding: 25pt;
    border-radius: 8pt;
    border: 1pt solid #e2e8f0;
}

.section {
    margin-bottom: 25pt;
    page-break-inside: avoid;
}

.section h2 {
    font-size: 16pt;
    font-weight: 600;
    color: #1a202c;
    margin: 0 0 15pt 0;
    border-bottom: 2pt solid #e2e8f0;
    padding-bottom: 8pt;
}

.section h3 {
    font-size: 13pt;
    font-weight: 600;
    color: #2d3748;
    margin: 20pt 0 10pt 0;
}

.metric-card {
    background: white;
    padding: 20pt;
    border-radius: 6pt;
    box-shadow: 0 1pt 3pt rgba(0, 0, 0, 0.1);
    border-left: 4pt solid #667eea;
    margin-bottom: 15pt;
}

.metric-title {
    font-size: 11pt;
    font-weight: 500;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    margin-bottom: 8pt;
}

.metric-value {
    font-size: 18pt;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 5pt;
}

.metric-change {
    font-size: 9pt;
    padding: 3pt 8pt;
    border-radius: 12pt;
    font-weight: 500;
}

.metric-change.positive {
    background: #c6f6d5;
    color: #22543d;
}

.metric-change.negative {
    background: #fed7d7;
    color: #742a2a;
}

.metric-change.neutral {
    background: #e2e8f0;
    color: #4a5568;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15pt 0;
    font-size: 9pt;
    background: white;
    border-radius: 4pt;
    overflow: hidden;
    box-shadow: 0 1pt 3pt rgba(0, 0, 0, 0.1);
}

.data-table th {
    background: #f7fafc;
    color: #4a5568;
    font-weight: 600;
    padding: 12pt 15pt;
    text-align: left;
    border-bottom: 1pt solid #e2e8f0;
}

.data-table td {
    padding: 10pt 15pt;
    border-bottom: 1pt solid #f1f5f9;
}

.data-table tbody tr:hover {
    background: #f8fafc;
}

.status-badge {
    display: inline-block;
    padding: 4pt 10pt;
    border-radius: 20pt;
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}

.status-completed { background: #c6f6d5; color: #22543d; }
.status-active { background: #bee3f8; color: #2a4365; }
.status-pending { background: #fef5e7; color: #744210; }

.chart-placeholder {
    background: #f8fafc;
    border: 2pt dashed #cbd5e0;
    border-radius: 8pt;
    padding: 40pt;
    text-align: center;
    color: #a0aec0;
    font-style: italic;
    margin: 20pt 0;
}

.footer-note {
    background: #fffef7;
    border: 1pt solid #fbbf24;
    border-radius: 4pt;
    padding: 15pt;
    margin: 25pt 0;
    font-size: 9pt;
}

.footer-note strong {
    color: #92400e;
}

.disclaimer {
    font-size: 8pt;
    color: #718096;
    text-align: center;
    margin-top: 30pt;
    padding-top: 20pt;
    border-top: 1pt solid #e2e8f0;
    font-style: italic;
}

/* Print-specific optimizations */
@media print {
    .metric-card {
        break-inside: avoid;
    }

    .section {
        break-inside: avoid;
    }
}
"""

# Create sample HTML with external resources
HTML_WITH_RESOURCES = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TechCorp Analytics Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <h1>Analytics Dashboard</h1>
        <div class="tagline">Q4 2024 Performance Overview</div>
    </header>

    <div class="content-grid">
        <main class="main-content">
            <section class="section">
                <h2>Revenue Performance</h2>

                <div class="metric-card">
                    <div class="metric-title">Total Revenue</div>
                    <div class="metric-value">$2,847,392</div>
                    <span class="metric-change positive">+12.4% vs last quarter</span>
                </div>

                <div class="metric-card">
                    <div class="metric-title">Monthly Recurring Revenue</div>
                    <div class="metric-value">$1,234,567</div>
                    <span class="metric-change positive">+8.7% vs last quarter</span>
                </div>

                <div class="chart-placeholder">
                    📊 Revenue Trend Chart<br>
                    <small>Interactive chart would be displayed here</small>
                </div>
            </section>

            <section class="section">
                <h2>Customer Metrics</h2>

                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Segment</th>
                            <th>Users</th>
                            <th>Growth</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Enterprise</td>
                            <td>1,247</td>
                            <td>+15.2%</td>
                            <td><span class="status-badge status-active">Active</span></td>
                        </tr>
                        <tr>
                            <td>Professional</td>
                            <td>3,891</td>
                            <td>+8.9%</td>
                            <td><span class="status-badge status-active">Active</span></td>
                        </tr>
                        <tr>
                            <td>Starter</td>
                            <td>12,456</td>
                            <td>+22.1%</td>
                            <td><span class="status-badge status-completed">Completed</span></td>
                        </tr>
                        <tr>
                            <td>Free Tier</td>
                            <td>45,231</td>
                            <td>-3.2%</td>
                            <td><span class="status-badge status-pending">Pending</span></td>
                        </tr>
                    </tbody>
                </table>
            </section>
        </main>

        <aside class="sidebar">
            <section class="section">
                <h2>Quick Stats</h2>

                <div class="metric-card">
                    <div class="metric-title">Active Projects</div>
                    <div class="metric-value">24</div>
                    <span class="metric-change neutral">+2 this month</span>
                </div>

                <div class="metric-card">
                    <div class="metric-title">Team Members</div>
                    <div class="metric-value">156</div>
                    <span class="metric-change positive">+12 this quarter</span>
                </div>

                <div class="metric-card">
                    <div class="metric-title">System Uptime</div>
                    <div class="metric-value">99.97%</div>
                    <span class="metric-change positive">+0.02% improvement</span>
                </div>
            </section>

            <section class="section">
                <h2>Recent Updates</h2>

                <div class="footer-note">
                    <strong>🚀 New Feature:</strong> Advanced analytics dashboard now available for Enterprise customers with real-time data visualization.
                </div>

                <div class="footer-note">
                    <strong>🔧 Maintenance:</strong> Scheduled system maintenance completed successfully with zero downtime.
                </div>
            </section>
        </aside>
    </div>

    <div class="disclaimer">
        This report contains confidential business information. Distribution is restricted to authorized personnel only.
        Generated automatically on December 2024.
    </div>
</body>
</html>
"""


def create_external_resources() -> tuple[Path, Path]:
    """Create external CSS and HTML files."""
    # Create CSS file
    css_file = ASSETS_DIR / "styles.css"
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(EXTERNAL_CSS)

    # Create HTML file
    html_file = DATA / "html" / "dashboard.html"
    html_file.parent.mkdir(exist_ok=True, parents=True)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(HTML_WITH_RESOURCES)

    return css_file, html_file


def convert_html_with_external_resources(html_path: Path, css_path: Optional[Path] = None, output_path: Optional[Path] = None) -> Path:
    """
    Convert HTML with external resources to PDF using WeasyPrint.

    Args:
        html_path: Path to HTML file
        css_path: Optional path to external CSS file
        output_path: Optional output path

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        output_path = OUT

    print(f"🌐 Converting HTML with external resources: {html_path}")

    try:
        # Create HTML object with base URL for relative paths
        html_doc = HTML(filename=str(html_path), base_url=str(html_path.parent))

        # Prepare CSS styles
        stylesheets = []

        # Add external CSS if provided
        if css_path and css_path.exists():
            print(f"🎨 Loading external CSS: {css_path}")
            stylesheets.append(CSS(filename=str(css_path)))

        # Add inline CSS for additional styling
        additional_css = CSS(string="""
            .resource-note {
                background: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
                font-size: 9px;
                color: #2e7d32;
            }
        """)
        stylesheets.append(additional_css)

        # Configure font handling
        font_config = FontConfiguration()

        # Generate PDF with external resources
        print("📄 Generating PDF with external resources...")
        html_doc.write_pdf(
            str(output_path),
            stylesheets=stylesheets,
            font_config=font_config
        )

        print(f"✅ PDF with external resources generated: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ External resources conversion failed: {e}")
        raise


def demonstrate_different_resource_handling() -> None:
    """Demonstrate different ways to handle external resources."""
    print("\n🔍 Demonstrating resource handling approaches:")

    # 1. Direct HTML string (no external resources)
    html_string = """
    <html>
    <head><style>body { font-family: Arial; } h1 { color: blue; }</style></head>
    <body><h1>Direct HTML String</h1><p>No external resources needed.</p></body>
    </html>
    """

    output1 = BUILD / "demo_string.pdf"
    HTML(string=html_string).write_pdf(str(output1))
    print(f"   ✅ String-based: {output1}")

    # 2. HTML file with local CSS
    css_content = "body { background: #f0f0f0; } h1 { color: red; }"
    css_file = ASSETS_DIR / "demo.css"
    with open(css_file, 'w') as f:
        f.write(css_content)

    html_with_css = f"""
    <html>
    <head><link rel="stylesheet" href="{css_file.name}"></head>
    <body><h1>HTML with Local CSS</h1><p>Using external CSS file.</p></body>
    </html>
    """

    html_file = ASSETS_DIR / "demo.html"
    with open(html_file, 'w') as f:
        f.write(html_with_css)

    output2 = BUILD / "demo_css.pdf"
    HTML(filename=str(html_file), base_url=str(ASSETS_DIR)).write_pdf(
        str(output2),
        stylesheets=[CSS(filename=str(css_file))]
    )
    print(f"   ✅ Local CSS: {output2}")

    # 3. HTML with web fonts (Google Fonts)
    html_with_fonts = """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Roboto', sans-serif; }
            h1 { font-weight: 700; color: #333; }
        </style>
    </head>
    <body><h1>HTML with Web Fonts</h1><p>Using Google Fonts.</p></body>
    </html>
    """

    output3 = BUILD / "demo_fonts.pdf"
    HTML(string=html_with_fonts).write_pdf(str(output3))
    print(f"   ✅ Web Fonts: {output3}")


def main():
    """Entry point"""
    try:
        # Create external resources
        css_file, html_file = create_external_resources()
        print(f"📄 HTML created: {html_file}")
        print(f"🎨 CSS created: {css_file}")

        # Convert with external resources
        pdf_file = convert_html_with_external_resources(html_file, css_file)

        print("
🎉 External resources PDF generation completed!"        print(f"   HTML: {html_file}")
        print(f"   CSS: {css_file}")
        print(f"   Output: {pdf_file}")

        # Demonstrate different approaches
        demonstrate_different_resource_handling()

        print("
🎯 External resources features demonstrated:"        print("   • External CSS files")
        print("   • Web fonts (Google Fonts)")
        print("   • Base URL for relative paths")
        print("   • Multiple stylesheets")
        print("   • Font configuration")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
