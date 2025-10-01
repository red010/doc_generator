# Document Generation Test Suite

## 1. Project Overview

- **Purpose**: This repository is a comprehensive test suite and demonstration environment for experimenting with various libraries, tools, and workflows for automated document generation.
- **Scope**: The project explores different technology "stacks" for creating documents, primarily focusing on converting structured data and Markdown into formats like `.docx` and `.pdf`.
- **Current Status**: ✅ **Complete Multi-Stack Document Generation System** - DOCX, Chromium, Pandoc, WeasyPrint stacks fully implemented
- **Target Audience**: AI Agents, Developers, Document Automation Specialists.
- **Machine-Readable**: This `README.md` is optimized for machine parsing. Key information is structured using clear headers and bullet points.
- **Last Updated**: 2025-10-01 (All syntax fixes completed, system fully operational)

## 2. Directory Structure

The repository is organized into distinct modules, each representing a specific document generation stack.

### 2.1. Core Stack Directories

Each of the following root directories represents a self-contained technology stack for document generation. They contain source code (`src/`), guides (`guide/`), and other necessary assets.

- **/docx-stack-examples/**: ✅ **FULLY IMPLEMENTED & TESTED**
  - **Technology**: Python-based stack using `docxtpl` + manual template creation (not `python-docx` for templates).
  - **Purpose**: Generates Microsoft Word (`.docx`) documents from manually created templates and structured data.
  - **Key Achievement**: ✅ Resolved critical XML fragmentation issue that prevented template rendering.
  - **Contains**:
    - `src/`: 4 optimized Python scripts with complete examples:
      - `a1_docxtpl_basic.py`: Basic templating with JSON data
      - `a2_richtext.py`: RichText formatting with special `{{r }}` syntax
      - `a3_images.py`: Inline image insertion
      - `a5_python_docx_only.py`: Markdown-to-DOCX converter (no templates)
    - `guide/`: Comprehensive documentation including troubleshooting and best practices
    - `templates/`: Manually created `.docx` template files (XML fragmentation-free)
    - `tools/`: Utility scripts for asset generation and testing
    - `tests/`: Golden file tests for output verification
    - `issues/`: Resolved issue documentation

- **/chromium-stack-examples/**: ✅ **FULLY IMPLEMENTED & TESTED**
  - **Technology**: Playwright + Chromium headless for HTML-to-PDF conversion.
  - **Purpose**: Generates high-fidelity PDFs from HTML content, including JavaScript-rendered charts and complex layouts.
  - **Key Achievement**: ✅ Professional PDF generation with headers, footers, and interactive content support.
  - **Contains**:
    - `src/`: 3 optimized Python scripts with complete examples:
      - `c1_html_to_pdf_basic.py`: Basic HTML to PDF conversion
      - `c2_dashboard_with_charts.py`: Interactive dashboards with Chart.js
      - `c3_header_footer_pdf.py`: Professional reports with headers/footers
    - `data/`: HTML templates and assets for examples
    - `tools/`: Batch execution and utility scripts

- **/pandoc-stack-examples/**: ✅ **FULLY IMPLEMENTED & TESTED**
  - **Technology**: Pandoc + LaTeX/PDF engines for universal document conversion.
  - **Purpose**: Converts between multiple document formats (Markdown ↔ PDF/DOCX/HTML/EPUB) with advanced formatting, font configuration, and batch processing.
  - **Key Achievement**: ✅ Universal document conversion with professional typography, advanced font management, article combination, and EPUB support.
  - **Contains**:
    - `src/`: 5 optimized Python scripts with complete examples:
      - `p1_markdown_to_pdf.py`: Markdown to PDF with LaTeX templates and font configuration
      - `p1_font_examples.py`: Advanced font configuration examples (Times, Helvetica, custom fonts)
      - `p2_markdown_to_docx.py`: Markdown to DOCX with styling
      - `p3_batch_conversion.py`: Parallel batch processing of multiple documents
      - `p4_combine_articles_to_pdf.py`: Combine multiple articles into single PDF with proper formatting
      - `p5_epub_to_pdf.py`: Convert EPUB files to professional PDF
    - `data/`: Markdown sources, EPUB files, article collections, and conversion templates
    - `tools/`: Batch execution and utility scripts
    - `guide/`: Comprehensive guides for font configuration and extended Pandoc usage

- **/weasyprint-stack-examples/**: ✅ **FULLY IMPLEMENTED & TESTED**
  - **Technology**: WeasyPrint for print-optimized HTML-to-PDF conversion.
  - **Purpose**: Generates high-quality PDFs with precise CSS layout control and professional typography.
  - **Key Achievement**: ✅ Print-optimized PDF generation with advanced CSS support and external resources.
  - **Contains**:
    - `src/`: 3 optimized Python scripts with complete examples:
      - `w1_html_to_pdf_basic.py`: Basic HTML to PDF with @page rules
      - `w2_template_based_pdf.py`: Jinja2 templating with dynamic data
      - `w3_external_resources.py`: External CSS, fonts, and asset handling
    - `data/`: HTML/CSS templates and external assets
    - `tools/`: Batch execution and utility scripts

### 2.2. General & Archived Content

- **/_guides/**:
  - **Purpose**: Contains general, high-level documentation and notes about document generation principles that apply across multiple stacks.
  - **Files**:
    - `01_doc_generation.md`: General notes.
    - `font_noto.md`: Notes on font usage.

- **/_archive/**:
  - **Purpose**: Contains legacy scripts and configuration files. This directory is for historical reference and is not part of the active, modularized test suites.
  - **Files**:
    - `make_templates.py`: Archived programmatic template generator (caused XML fragmentation issues)
    - Other legacy scripts for historical reference.

## 3. Quick Start - All Technology Stacks

### Available Technology Stacks

This repository provides **4 complete technology stacks** for document generation:

1. **DOCX Stack** (`docxtpl`): Template-based Word document generation
2. **Chromium Stack** (`playwright`): High-fidelity HTML-to-PDF with JavaScript support
3. **Pandoc Stack** (`pandoc`): Universal document format conversion
4. **WeasyPrint Stack** (`weasyprint`): Print-optimized HTML-to-PDF conversion

### Prerequisites (All Stacks)
- Python 3.8+
- Required packages vary by stack (see individual stack directories for requirements.txt)

### Running Examples

Each stack has its own directory with complete examples. Navigate to any stack directory and run:

```bash
# For any stack (docx, chromium, pandoc, weasyprint)
cd [stack-name]-stack-examples
python tools/run_all.py  # Run all examples in the stack
```

### DOCX Stack Examples (docxtpl + Manual Templates)

```bash
cd docx-stack-examples

# Generate all DOCX examples
python tools/run_all.py

# Or run individual examples:
python src/a1_docxtpl_basic.py         # Basic templating with JSON data
python src/a2_richtext.py              # RichText formatting with {{r }} syntax
python src/a3_images.py               # Inline image insertion
python src/a5_python_docx_only.py      # Markdown-to-DOCX (no templates)
```

**Output files** (in `docx-stack-examples/build/`):
- `out_a1_basic.docx`: Report with structured data
- `out_a2_richtext.docx`: Document with formatted text
- `out_a3_images.docx`: Document with embedded images
- `out_a5_markdown_to_docx.docx`: DOCX converted from Markdown (no templates)

### Chromium Stack Examples (Playwright + Chromium)

```bash
cd chromium-stack-examples

# Generate all PDF examples with Chromium
python tools/run_all.py

# Or run individual examples:
python src/c1_html_to_pdf_basic.py     # Basic HTML to PDF conversion
python src/c2_dashboard_with_charts.py # Interactive dashboards with Chart.js
python src/c3_header_footer_pdf.py     # Professional reports with headers/footers
```

**Output files** (in `chromium-stack-examples/build/`):
- `out_c1_basic.pdf`: Basic HTML to PDF conversion
- `out_c2_dashboard.pdf`: Dashboard with interactive Chart.js charts
- `out_c3_header_footer.pdf`: Professional report with headers/footers

### Pandoc Stack Examples (Universal Conversion)

```bash
cd pandoc-stack-examples

# Generate all format conversion examples
python tools/run_all.py

# Or run individual examples:
python src/p1_markdown_to_pdf.py       # Markdown to PDF with LaTeX and font config
python src/p1_font_examples.py         # Advanced font configuration examples
python src/p2_markdown_to_docx.py      # Markdown to DOCX with styling
python src/p3_batch_conversion.py      # Parallel batch processing
python src/p4_combine_articles_to_pdf.py  # Combine articles into single PDF
python src/p5_epub_to_pdf.py           # Convert EPUB to PDF
```

**Output files** (in `pandoc-stack-examples/build/`):
- `out_p1_markdown_to_pdf.pdf`: Markdown to PDF with LaTeX and custom fonts
- `esempio_classici.pdf`, `esempio_minimal.pdf`, `esempio_yaml.pdf`: Font examples
- `out_p2_markdown_to_docx.docx`: Markdown to DOCX with styling
- Multiple converted files from batch processing
- `combined_articles.pdf`: Combined article collection (350KB+)
- `LP 500 Best Places to See.pdf`: Converted EPUB file (39MB)

### WeasyPrint Stack Examples (Print-Optimized PDF)

```bash
cd weasyprint-stack-examples

# Generate all print-optimized PDF examples
python tools/run_all.py

# Or run individual examples:
python src/w1_html_to_pdf_basic.py     # HTML to PDF with @page rules
python src/w2_template_based_pdf.py    # Jinja2 templating with dynamic data
python src/w3_external_resources.py    # External CSS, fonts, and assets
```

**Output files** (in `weasyprint-stack-examples/build/`):
- `out_w1_basic.pdf`: Basic HTML to PDF with @page rules
- `out_w2_template_based.pdf`: Template-based PDF with dynamic data
- `out_w3_external_resources.pdf`: PDF with external resources
- Additional demo files for different resource handling approaches

### Key Learning: Manual Template Creation
**Key Learnings:**
- **Manual Template Creation**: Templates must be created manually in Word/LibreOffice to avoid XML fragmentation. Programmatic template generation with `python-docx` causes Jinja2 tags to be split across multiple XML runs, making them invisible to `docxtpl`.
- **Template-less Generation**: Direct `python-docx` enables Markdown-to-DOCX conversion and programmatic document creation without templates.
- **RichText Syntax**: Use `{{r variable}}` for RichText objects in docxtpl templates.

## 4. Project Achievements

### ✅ Major Achievements

#### Technology Stack Implementation
- **DOCX Stack**: Complete implementation with 4 examples (templating, RichText, images, template-less conversion)
- **Chromium Stack**: Complete implementation with 3 examples (basic PDF, dashboards with charts, professional reports)
- **Pandoc Stack**: Complete implementation with 5 examples (PDF/LaTeX, font config, DOCX, batch processing, article combination, EPUB conversion)
- **WeasyPrint Stack**: Complete implementation with 3 examples (print-optimized PDF, templating, external resources)

#### Critical Issues Resolved
- **XML Fragmentation Problem**: Identified and solved the critical issue where Word automatically fragments Jinja2 tags in programmatically generated templates
- **RichText Syntax**: Discovered and documented the `{{r variable}}` syntax for RichText objects in docxtpl
- **Template Creation Best Practices**: Established manual template creation as the gold standard

### 🎯 Current Status
- **DOCX Stack**: ✅ Complete and production-ready (4 examples)
- **Chromium Stack**: ✅ Complete and production-ready (3 examples)
- **Pandoc Stack**: ✅ Complete and production-ready (5 examples)
- **WeasyPrint Stack**: ✅ Complete and production-ready (3 examples)
- **Total Examples**: 15 complete, tested implementations across 4 technology stacks

### 📚 Documentation
- Comprehensive guides with examples and troubleshooting
- Issue tracking with resolution documentation
- Best practices for template creation and maintenance

### 🔧 Critical Fixes Applied
- **Syntax Errors**: Resolved unterminated string literals across all stack scripts (10+ files fixed)
- **Unicode Support**: Upgraded Pandoc from pdflatex to xelatex for full Unicode compatibility
- **Template Issues**: Fixed DOCX template reference errors in batch processing
- **Function Errors**: Corrected invalid attribute access in WeasyPrint scripts
- **Documentation**: Updated all references to reflect current script count and functionality