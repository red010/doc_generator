#!/usr/bin/env python
"""
Run all WeasyPrint PDF generation examples.
"""

from pathlib import Path
import sys

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from w1_html_to_pdf_basic import main as w1_main
from w2_template_based_pdf import main as w2_main
from w3_external_resources import main as w3_main

if __name__ == "__main__":
    print("🌐 Executing all WeasyPrint PDF generation examples...\n")

    try:
        print("📄 Executing basic HTML to PDF...")
        result1 = w1_main()
        if result1 != 0:
            raise Exception("W1 failed")
        print()

        print("📝 Executing template-based PDF...")
        result2 = w2_main()
        if result2 != 0:
            raise Exception("W2 failed")
        print()

        print("🔗 Executing external resources example...")
        result3 = w3_main()
        if result3 != 0:
            raise Exception("W3 failed")
        print()

        print("🎉 All WeasyPrint examples completed successfully!")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)
