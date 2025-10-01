#!/usr/bin/env python
"""
Pandoc Stack Example 1: Markdown to PDF with LaTeX Template
Converts Markdown documents to professional PDF using Pandoc and XeLaTeX.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Union

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
DATA = ROOT / "data"
MARKDOWN_DIR = DATA / "markdown"
TEMPLATES_DIR = DATA / "templates"
TEMPLATES_DIR.mkdir(exist_ok=True, parents=True)


class PandocConfig:
    """Configuration class for Pandoc PDF conversion."""

    def __init__(self):
        self.pdf_engine = "xelatex"
        self.geometry = "margin=1in"
        self.fontsize = "11pt"

        # Font configuration (None = use system defaults)
        # Using common system fonts that are typically available
        self.mainfont = "Times"  # Main text font (serif) - common system font
        self.sansfont = "Helvetica"   # Sans-serif font for headings - common system font
        self.monofont = "Courier"  # Monospace font for code - common system font
        self.cjkmainfont = None  # Font for CJK characters (disabled by default)
        self.mathfont = None  # Math font (optional)

        # Color and link settings
        self.colorlinks = True
        self.linkcolor = "blue"
        self.urlcolor = "blue"
        self.citecolor = "green"

        # Table of contents
        self.toc = True
        self.toc_depth = 3
        self.number_sections = True

    def to_args(self) -> List[str]:
        """Convert configuration to Pandoc command line arguments."""
        args = [
            "--pdf-engine", self.pdf_engine,
            "--variable", f"geometry:{self.geometry}",
            "--variable", f"fontsize={self.fontsize}",
        ]

        # Font configuration
        if self.mainfont:
            args.extend(["--variable", f"mainfont={self.mainfont}"])
        if self.sansfont:
            args.extend(["--variable", f"sansfont={self.sansfont}"])
        if self.monofont:
            args.extend(["--variable", f"monofont={self.monofont}"])
        if self.cjkmainfont:
            args.extend(["--variable", f"CJKmainfont={self.cjkmainfont}"])
        if self.mathfont:
            args.extend(["--variable", f"mathfont={self.mathfont}"])

        # Color and link settings
        if self.colorlinks:
            args.extend([
                "--variable", "colorlinks=true",
                "--variable", f"linkcolor={self.linkcolor}",
                "--variable", f"urlcolor={self.urlcolor}",
                "--variable", f"citecolor={self.citecolor}",
            ])

        # Table of contents
        if self.toc:
            args.extend([
                "--toc",
                "--toc-depth", str(self.toc_depth),
            ])

        if self.number_sections:
            args.append("--number-sections")

        return args

    @classmethod
    def customize_fonts(cls, mainfont: str = None, sansfont: str = None,
                       monofont: str = None, cjkmainfont: str = None,
                       mathfont: str = None) -> 'PandocConfig':
        """
        Create a customized font configuration.

        Args:
            mainfont: Main text font (serif)
            sansfont: Sans-serif font for headings
            monofont: Monospace font for code
            cjkmainfont: Font for CJK characters
            mathfont: Font for mathematical expressions

        Returns:
            PandocConfig: A new config instance with customized fonts
        """
        config = cls()

        if mainfont is not None:
            config.mainfont = mainfont
        if sansfont is not None:
            config.sansfont = sansfont
        if monofont is not None:
            config.monofont = monofont
        if cjkmainfont is not None:
            config.cjkmainfont = cjkmainfont
        if mathfont is not None:
            config.mathfont = mathfont

        return config

    @classmethod
    def create_minimal(cls) -> 'PandocConfig':
        """
        Create a minimal configuration without custom fonts.
        Useful when system fonts are not available or preferred.

        Returns:
            PandocConfig: A config with only essential settings
        """
        config = cls()
        # Disable custom fonts to use LaTeX defaults
        config.mainfont = None
        config.sansfont = None
        config.monofont = None
        config.cjkmainfont = None
        config.mathfont = None
        return config


class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass


class DependencyError(Exception):
    """Custom exception for missing dependencies."""
    pass


def check_dependencies() -> None:
    """Check if required dependencies are available."""
    # Check for pandoc
    if not shutil.which("pandoc"):
        raise DependencyError("pandoc is not installed or not in PATH. Please install pandoc.")

    # Check for xelatex
    if not shutil.which("xelatex"):
        raise DependencyError("xelatex is not installed or not in PATH. Please install a LaTeX distribution (e.g., TeX Live).")


def validate_file_path(file_path: Union[str, Path], must_exist: bool = True) -> Path:
    """Validate and convert file path."""
    path = Path(file_path)

    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if must_exist and not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return path


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if necessary."""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

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
    ensure_directory(MARKDOWN_DIR)
    markdown_file = MARKDOWN_DIR / "sample_report.md"

    try:
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_MARKDOWN)
        print(f"📝 Sample Markdown created: {markdown_file}")
    except IOError as e:
        raise ConversionError(f"Failed to create sample markdown file: {e}")

    return markdown_file


def convert_markdown_to_pdf(markdown_path: Union[str, Path], output_path: Union[str, Path], config: Optional[PandocConfig] = None) -> Path:
    """
    Convert Markdown to PDF using Pandoc with XeLaTeX.

    Args:
        markdown_path: Path to input Markdown file
        output_path: Output path for the PDF file
        config: Optional PandocConfig instance for customization

    Returns:
        Path to generated PDF

    Raises:
        ConversionError: If conversion fails
        DependencyError: If required dependencies are missing
    """
    # Validate inputs
    input_path = validate_file_path(markdown_path)
    output_path = Path(output_path)

    # Ensure output directory exists
    ensure_directory(output_path.parent)

    # Use default config if none provided
    if config is None:
        config = PandocConfig()

    print(f"📖 Converting Markdown to PDF: {input_path}")

    # Build Pandoc command
    cmd = ["pandoc", str(input_path), "-o", str(output_path)] + config.to_args()

    try:
        print("🔧 Running Pandoc conversion...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            print(f"✅ PDF generated successfully: {output_path}")
            return output_path
        else:
            error_msg = f"Pandoc returned non-zero exit code: {result.returncode}"
            if result.stderr:
                error_msg += f"\nError details: {result.stderr}"
            raise ConversionError(error_msg)

    except subprocess.CalledProcessError as e:
        error_msg = f"Pandoc conversion failed: {e}"
        if e.stderr:
            error_msg += f"\nError details: {e.stderr}"
        raise ConversionError(error_msg) from e
    except FileNotFoundError as e:
        raise DependencyError(f"Pandoc command not found: {e}") from e


def main() -> int:
    """Entry point for the Markdown to PDF conversion script.

    Usage:
        python p1_markdown_to_pdf.py [input_file.md]

    If no input file is provided, creates and uses a sample markdown file.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        print("🚀 Starting Markdown to PDF conversion...")
        print("=" * 50)

        # Check dependencies first
        check_dependencies()

        # Check for command line argument
        if len(sys.argv) > 1:
            input_file = Path(sys.argv[1])
            if not input_file.exists():
                raise FileNotFoundError(f"Input file not found: {input_file}")

            # Use provided file
            markdown_file = validate_file_path(input_file)
            print(f"📁 Using input file: {markdown_file}")
        else:
            # Create sample markdown if it doesn't exist
            markdown_file = create_sample_markdown()

        # Generate output filename based on input
        input_name = markdown_file.stem
        output_file = BUILD / f"out_{input_name}.pdf"

        # Convert to PDF
        result = convert_markdown_to_pdf(markdown_file, output_file)

        print("\n🎉 Conversion completed successfully!")
        print(f"   Input:  {markdown_file}")
        print(f"   Output: {result}")
        print("   Engine: Pandoc + XeLaTeX")

        # Verify output file was created
        if result.exists():
            file_size = result.stat().st_size
            print(f"   Size: {file_size / 1024:.1f} KB")
        else:
            print("   ⚠️  Warning: Output file was not found after conversion")

        return 0

    except DependencyError as e:
        print(f"\n❌ Dependency Error: {e}")
        print("Please install the required dependencies and try again.")
        return 1
    except ConversionError as e:
        print(f"\n❌ Conversion Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Conversion interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return 1


if __name__ == "__main__":
    exit(main())
