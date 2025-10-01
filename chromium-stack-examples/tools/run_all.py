#!/usr/bin/env python
"""
Run all Chromium PDF generation examples.
"""

from pathlib import Path
import sys

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from c1_html_to_pdf_basic import generate_basic_pdf as c1
from c2_dashboard_with_charts import generate_dashboard_pdf as c2
from c3_header_footer_pdf import generate_report_with_headers_footers as c3

if __name__ == "__main__":
    print("🌐 Executing all Chromium PDF generation examples...\n")

    try:
        print("📄 Executing basic HTML to PDF...")
        result1 = c1()
        print(f"✅ {result1}\n")

        print("📊 Executing dashboard with charts...")
        result2 = c2()
        print(f"✅ {result2}\n")

        print("📋 Executing report with headers/footers...")
        result3 = c3()
        print(f"✅ {result3}\n")

        print("🎉 All Chromium examples completed successfully!")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)
