#!/usr/bin/env python
"""
Chromium Stack Example 2: Dashboard with Charts
Generates PDF from HTML dashboard with interactive Chart.js charts.
"""

from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright
import json

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
HTML_DIR = DATA / "html"
HTML_DIR.mkdir(exist_ok=True, parents=True)
OUT = BUILD / "out_c2_dashboard.pdf"

# HTML dashboard with Chart.js
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @page {
            size: A4;
            margin: 0.5in;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e9ecef;
        }
        .chart-card h3 {
            margin: 0 0 20px 0;
            color: #495057;
            font-size: 1.2em;
            font-weight: 600;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .full-width-chart {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        canvas {
            max-width: 100%;
            height: auto !important;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Q4 2024 Performance Report</p>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value" id="totalRevenue">$284K</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="totalUsers">12.5K</div>
            <div class="metric-label">Active Users</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="conversionRate">3.2%</div>
            <div class="metric-label">Conversion Rate</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" id="avgOrderValue">$127</div>
            <div class="metric-label">Avg Order Value</div>
        </div>
    </div>

    <div class="dashboard-grid">
        <div class="chart-card">
            <h3>📈 Monthly Revenue</h3>
            <canvas id="revenueChart" width="400" height="300"></canvas>
        </div>
        <div class="chart-card">
            <h3>👥 User Growth</h3>
            <canvas id="usersChart" width="400" height="300"></canvas>
        </div>
    </div>

    <div class="full-width-chart">
        <h3>📊 Traffic Sources</h3>
        <canvas id="trafficChart" width="800" height="400"></canvas>
    </div>

    <div class="footer">
        Generated with Chromium headless PDF generation | Data as of Q4 2024
    </div>

    <script>
        // Sample data - in real app this would come from API
        const revenueData = {
            labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Revenue ($)',
                data: [45000, 52000, 48000, 61000, 55000, 78000],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4,
                fill: true
            }]
        };

        const usersData = {
            labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Active Users',
                data: [8500, 9200, 8800, 10100, 11500, 12500],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4,
                fill: true
            }]
        };

        const trafficData = {
            labels: ['Organic Search', 'Direct', 'Social Media', 'Email', 'Paid Ads', 'Referrals'],
            datasets: [{
                label: 'Traffic Sources',
                data: [35, 25, 20, 10, 7, 3],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ],
                borderWidth: 1
            }]
        };

        // Create charts
        new Chart(document.getElementById('revenueChart'), {
            type: 'line',
            data: revenueData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + (value / 1000) + 'K';
                            }
                        }
                    }
                }
            }
        });

        new Chart(document.getElementById('usersChart'), {
            type: 'line',
            data: usersData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return (value / 1000) + 'K';
                            }
                        }
                    }
                }
            }
        });

        new Chart(document.getElementById('trafficChart'), {
            type: 'doughnut',
            data: trafficData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });

        // Signal that dashboard is ready for PDF generation
        window.dashboardReady = true;
    </script>
</body>
</html>
"""


def generate_dashboard_pdf(output_path: Optional[Path] = None) -> Path:
    """
    Generate a dashboard PDF with Chart.js charts using Playwright/Chromium.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated PDF file.
    """
    if output_path is None:
        output_path = OUT

    print("📊 Starting Chromium for dashboard rendering...")
    print("🎨 Loading dashboard with Chart.js...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set content
        page.set_content(DASHBOARD_HTML)

        # Wait for charts to render
        print("⏳ Waiting for charts to render...")
        page.wait_for_function("window.dashboardReady === true")

        # Give extra time for animations
        page.wait_for_timeout(1000)

        # Generate PDF
        print("📄 Generating dashboard PDF...")
        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={
                "top": "0.5in",
                "bottom": "0.5in",
                "left": "0.5in",
                "right": "0.5in"
            }
        )

        browser.close()

    print(f"✅ Dashboard PDF generated: {output_path}")
    return output_path


def main():
    """Entry point"""
    try:
        result = generate_dashboard_pdf()
        print("
🎉 Dashboard PDF generated successfully!"        print(f"   Output: {result}")
        print("   Features: Interactive Chart.js charts, responsive design"
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
