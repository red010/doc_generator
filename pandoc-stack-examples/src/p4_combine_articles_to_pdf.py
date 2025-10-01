#!/usr/bin/env python
"""
Pandoc Stack Example 4: Combine Articles to Single PDF
Combines multiple Markdown articles into a single PDF with proper formatting.
Each article gets its title and date as subtitle, with page breaks between articles.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import re

# Configuration
ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = ROOT / "data/test_articles"
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
OUTPUT_PDF = BUILD / "combined_articles.pdf"

def parse_filename(filename: str) -> Tuple[str, str]:
    """
    Parse filename in format 'YYYY-MM-DD - [TITLE].md'
    Handles variations like 'YYYY-MM-DD CODE - [TITLE].md'
    Returns (date, title)
    """
    # Match pattern: YYYY-MM-DD [optional_code] - [TITLE].md
    pattern = r'^(\d{4}-\d{2}-\d{2})(?:\s+[^\s-]+)?\s*-\s*(.+)\.md$'
    match = re.match(pattern, filename)

    if match:
        date = match.group(1)
        title = match.group(2).strip()
        return date, title
    else:
        # Fallback: try to extract date and use rest as title
        date_pattern = r'^(\d{4}-\d{2}-\d{2})'
        date_match = re.match(date_pattern, filename)
        if date_match:
            date = date_match.group(1)
            # Remove date and extension, clean up the title
            title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*', '', filename)
            title = re.sub(r'\.md$', '', title)
            title = title.strip()
            return date, title
        else:
            raise ValueError(f"Could not parse date from filename '{filename}'")


def extract_article_content(file_path: Path) -> str:
    """
    Extract article content, removing the YAML front matter.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML front matter (between --- markers)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Return content after the second ---
            return parts[2].strip()
        else:
            # No closing ---, return content after first ---
            return parts[1].strip()

    return content.strip()


def create_combined_markdown(articles_dir: Path) -> str:
    """
    Create a combined Markdown document from all articles.
    """
    # Get all .md files and sort by date
    md_files = sorted(articles_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"No .md files found in {articles_dir}")

    combined_content = []

    # Add document title
    combined_content.append("# Raccolta Articoli di Ricerca")
    combined_content.append("*Documenti tecnici e articoli di ricerca combinati*")
    combined_content.append("")
    combined_content.append("\\newpage")
    combined_content.append("")

    for i, file_path in enumerate(md_files):
        try:
            # Parse filename
            date, title = parse_filename(file_path.name)

            # Extract content (without YAML front matter)
            content = extract_article_content(file_path)

            # Add article section
            combined_content.append(f"# {title}")
            combined_content.append(f"## {date}")
            combined_content.append("")
            combined_content.append(content)

            # Add page break (except for the last article)
            if i < len(md_files) - 1:
                combined_content.append("")
                combined_content.append("\\newpage")
                combined_content.append("")

        except Exception as e:
            print(f"⚠️  Warning: Error processing {file_path.name}: {e}")
            continue

    return "\n".join(combined_content)


def convert_to_pdf(markdown_content: str, output_path: Path) -> None:
    """
    Convert combined Markdown to PDF using Pandoc with XeLaTeX.
    """
    # Create temporary markdown file
    temp_md = output_path.parent / "temp_combined.md"
    try:
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Pandoc command for PDF conversion
        cmd = [
            "pandoc",
            str(temp_md),
            "-o", str(output_path),
            "--pdf-engine=xelatex",
            "--variable=geometry:margin=1in",
            "--variable=fontsize=11pt",
            "--variable=colorlinks=true",
            "--variable=linkcolor=blue",
            "--variable=urlcolor=blue",
            "--variable=citecolor=green",
            "--toc",
            "--toc-depth=2",
            "--number-sections"
        ]

        print(f"📖 Converting combined document to PDF: {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            print(f"✅ PDF generated successfully: {output_path}")
        else:
            raise RuntimeError(f"Pandoc conversion failed: {result.stderr}")

    finally:
        # Clean up temporary file
        if temp_md.exists():
            temp_md.unlink()


def main() -> int:
    """Main function."""
    try:
        print("🚀 Starting article combination and PDF conversion...")
        print("=" * 60)

        # Check if articles directory exists
        if not ARTICLES_DIR.exists():
            raise FileNotFoundError(f"Articles directory not found: {ARTICLES_DIR}")

        # Count articles
        md_files = list(ARTICLES_DIR.glob("*.md"))
        print(f"📁 Found {len(md_files)} articles in {ARTICLES_DIR}")

        # Create combined markdown
        print("📝 Creating combined Markdown document...")
        combined_markdown = create_combined_markdown(ARTICLES_DIR)

        # Convert to PDF
        convert_to_pdf(combined_markdown, OUTPUT_PDF)

        # Show result
        print("\n🎉 Combined PDF creation completed!")
        print(f"   Articles processed: {len(md_files)}")
        print(f"   Output: {OUTPUT_PDF}")

        if OUTPUT_PDF.exists():
            file_size = OUTPUT_PDF.stat().st_size
            print(f"   Size: {file_size / 1024:.1f} KB")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return 1


if __name__ == "__main__":
    exit(main())
