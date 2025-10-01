#!/usr/bin/env python
"""
Pandoc Stack Example 1: Markdown to PDF with LaTeX Template
Converts Markdown documents to professional PDF using Pandoc and LaTeX.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
MARKDOWN_DIR = DATA / "markdown"
TEMPLATES_DIR = DATA / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True, parents=True)
OUT = BUILD / "out_p1_markdown_to_pdf.pdf"

# Sample Markdown content
SAMPLE_MARKDOWN = """
---
title: "Technical Report: Advanced Document Processing"
author:
  - "Dr. Enrico Busto"
  - "AI Research Team"
date: "2024-12-31"
abstract: |
  This comprehensive report explores advanced document processing techniques,
  focusing on automated generation and conversion of various document formats.
  We present methodologies for creating professional documents from structured data.

geometry: margin=1in
fontsize: 11pt
lang: en-US
---

# Executive Summary

This technical report presents cutting-edge methodologies for automated document generation and processing. Our research demonstrates significant improvements in document quality, consistency, and production efficiency.

## Key Achievements

- **Automated PDF Generation**: High-fidelity document creation with consistent formatting
- **Multi-format Support**: Seamless conversion between Markdown, HTML, DOCX, and PDF
- **Template-driven Processing**: Reusable document templates for various use cases
- **Quality Assurance**: Automated testing and validation of generated documents

# Technical Architecture

## Core Components

### Document Generation Engine

The system employs a modular architecture with the following key components:

1. **Template Processor**: Handles variable substitution and conditional content
2. **Format Converter**: Manages conversion between different document formats
3. **Quality Validator**: Ensures output meets specified standards
4. **Batch Processor**: Handles multiple document generation jobs

### Data Flow

```mermaid
graph TD
    A[Input Data] --> B[Template Processor]
    B --> C[Format Converter]
    C --> D[Quality Validator]
    D --> E[Output Document]
    F[Configuration] --> B
    G[Template Files] --> B
```

## Implementation Details

### Template System

Our template system supports:

- **Variable Substitution**: `{{variable_name}}` syntax
- **Conditional Blocks**: `{% if condition %}` logic
- **Loops**: `{% for item in list %}` iteration
- **Includes**: Reusable template components

### Quality Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Rendering Accuracy | 99.5% | 99.2% | ✅ Good |
| Format Consistency | 100% | 99.8% | ✅ Excellent |
| Processing Speed | <2s | 1.3s | ✅ Excellent |

# Results and Analysis

## Performance Benchmarks

The system demonstrates excellent performance across various document types and sizes.

### Document Size Analysis

- **Small Documents** (< 10 pages): Processing time < 1 second
- **Medium Documents** (10-50 pages): Processing time 1-3 seconds
- **Large Documents** (> 50 pages): Processing time 3-8 seconds

### Quality Assessment

Document quality was evaluated using the following criteria:

1. **Visual Consistency**: 98% accuracy
2. **Content Accuracy**: 99.9% accuracy
3. **Format Preservation**: 97% accuracy
4. **Accessibility**: 95% compliance

## Case Studies

### Technical Documentation

A major software company implemented our system for API documentation generation, resulting in:

- 60% reduction in documentation creation time
- 40% improvement in documentation consistency
- 80% reduction in formatting errors

### Financial Reporting

A financial services firm adopted the system for quarterly report generation:

- 50% faster report production
- 100% elimination of manual formatting errors
- Improved compliance with regulatory standards

# Future Developments

## Planned Enhancements

### Advanced Features

1. **AI-powered Content Generation**: Integration with language models for content creation
2. **Real-time Collaboration**: Multi-user document editing capabilities
3. **Advanced Analytics**: Document usage and performance tracking
4. **Mobile Optimization**: Responsive document generation for mobile devices

### Research Directions

- **Natural Language Processing**: Enhanced semantic understanding
- **Computer Vision**: Image and diagram processing
- **Machine Learning**: Automated template optimization

# Conclusion

This research demonstrates the viability and effectiveness of automated document generation systems. The implemented solution provides a robust, scalable platform for professional document creation with significant improvements in efficiency and quality.

The modular architecture ensures flexibility and extensibility, making it suitable for a wide range of document processing applications.

---

*This report was generated using Pandoc and LaTeX from Markdown source.*
"""


def create_sample_markdown() -> Path:
    """Create sample Markdown file for conversion."""
    markdown_file = MARKDOWN_DIR / "sample_report.md"
    MARKDOWN_DIR.mkdir(exist_ok=True, parents=True)

    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(SAMPLE_MARKDOWN)

    return markdown_file


def convert_markdown_to_pdf(markdown_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert Markdown to PDF using Pandoc with LaTeX.

    Args:
        markdown_path: Path to input Markdown file
        output_path: Optional output path, defaults to OUT

    Returns:
        Path to generated PDF
    """
    if output_path is None:
        output_path = OUT

    print(f"📖 Converting Markdown to PDF: {markdown_path}")

    # Pandoc command for Markdown to PDF
    cmd = [
        "pandoc",
        str(markdown_path),
        "-o", str(output_path),
        "--pdf-engine=pdflatex",
        "--variable", "geometry:margin=1in",
        "--variable", "fontsize=11pt",
        "--variable", "colorlinks=true",
        "--variable", "linkcolor=blue",
        "--variable", "urlcolor=blue",
        "--variable", "citecolor=green",
        "--toc",
        "--toc-depth=3",
        "--number-sections"
    ]

    try:
        print("🔧 Running Pandoc conversion...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            print(f"✅ PDF generated successfully: {output_path}")
            return output_path
        else:
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc conversion failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        raise


def main():
    """Entry point"""
    try:
        # Create sample markdown if it doesn't exist
        markdown_file = create_sample_markdown()
        print(f"📝 Sample Markdown created: {markdown_file}")

        # Convert to PDF
        result = convert_markdown_to_pdf(markdown_file)

        print("
🎉 Conversion completed!"        print(f"   Input: {markdown_file}")
        print(f"   Output: {result}")
        print("   Engine: Pandoc + LaTeX"
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
