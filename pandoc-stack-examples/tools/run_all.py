#!/usr/bin/env python
"""
Run all Pandoc document conversion examples.
"""

from pathlib import Path
import sys

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from p1_markdown_to_pdf import main as p1_main
from p1_font_examples import main as p1_font_main
from p2_markdown_to_docx import main as p2_main
from p3_batch_conversion import main as p3_main
from p4_combine_articles_to_pdf import main as p4_main
from p5_epub_to_pdf import main as p5_main

if __name__ == "__main__":
    print("📄 Executing all Pandoc conversion examples...\n")

    try:
        print("📖 Executing Markdown to PDF conversion...")
        result1 = p1_main()
        if result1 != 0:
            raise Exception("P1 failed")
        print()

        print("🔤 Executing font configuration examples...")
        result1_font = p1_font_main()
        if result1_font != 0:
            raise Exception("P1 Font examples failed")
        print()

        print("📝 Executing Markdown to DOCX conversion...")
        result2 = p2_main()
        if result2 != 0:
            raise Exception("P2 failed")
        print()

        print("🔄 Executing batch conversion...")
        result3 = p3_main()
        if result3 != 0:
            raise Exception("P3 failed")
        print()

        print("📚 Executing article combination...")
        result4 = p4_main()
        if result4 != 0:
            raise Exception("P4 failed")
        print()

        print("📖 Executing EPUB to PDF conversion...")
        result5 = p5_main()
        if result5 != 0:
            raise Exception("P5 failed")
        print()

        print("🎉 All Pandoc examples completed successfully!")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)
