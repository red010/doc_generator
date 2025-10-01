# Document Generation Test Suite

## 1. Project Overview

- **Purpose**: This repository is a comprehensive test suite and demonstration environment for experimenting with various libraries, tools, and workflows for automated document generation.
- **Scope**: The project explores different technology "stacks" for creating documents, primarily focusing on converting structured data and Markdown into formats like `.docx` and `.pdf`.
- **Current Status**: ✅ **Complete DOCX Stack with Advanced Features** - 3 working examples (basic, RichText, images)
- **Target Audience**: AI Agents, Developers, Document Automation Specialists.
- **Machine-Readable**: This `README.md` is optimized for machine parsing. Key information is structured using clear headers and bullet points.
- **Last Updated**: 2025-09-30

## 2. Directory Structure

The repository is organized into distinct modules, each representing a specific document generation stack.

### 2.1. Core Stack Directories

Each of the following root directories represents a self-contained technology stack for document generation. They contain source code (`src/`), guides (`guide/`), and other necessary assets.

- **/docx-stack-examples/**: ✅ **FULLY IMPLEMENTED & TESTED**
  - **Technology**: Python-based stack using `docxtpl` + manual template creation (not `python-docx` for templates).
  - **Purpose**: Generates Microsoft Word (`.docx`) documents from manually created templates and structured data.
  - **Key Achievement**: ✅ Resolved critical XML fragmentation issue that prevented template rendering.
  - **Contains**:
    - `src/`: 3 optimized Python scripts with complete examples:
      - `a1_docxtpl_basic.py`: Basic templating with JSON data
      - `a2_richtext.py`: RichText formatting with special `{{r }}` syntax
      - `a3_images.py`: Inline image insertion
    - `guide/`: Comprehensive documentation including troubleshooting and best practices
    - `templates/`: Manually created `.docx` template files (XML fragmentation-free)
    - `tools/`: Utility scripts for asset generation and testing
    - `tests/`: Golden file tests for output verification
    - `issues/`: Resolved issue documentation

- **/weasyprint-stack-examples/**:
  - **Technology**: `WeasyPrint` (Python library).
  - **Purpose**: Converts HTML and CSS into high-quality PDF documents.
  - **Contains**:
    - `guide/`: A Markdown file with specific notes on using WeasyPrint.
    - (Source files to be added).

- **/pandoc-stack-examples/**:
  - **Technology**: `Pandoc` (command-line utility).
  - **Purpose**: Universal document converter, used here for converting between formats like Markdown, HTML, and PDF.
  - **Contains**:
    - `guide/`: A Markdown file with an extended guide on Pandoc.
    - (Source files to be added).

- **/chromium-stack-examples/**:
  - **Technology**: Headless Chromium browser (e.g., via `Playwright` or `Puppeteer`).
  - **Purpose**: Renders web pages (HTML, CSS, JS) and "prints" them to PDF, ensuring high fidelity with web standards.
  - **Contains**:
    - `guide/`: A Markdown file with notes on this HTML-to-PDF approach.
    - (Source files to be added).

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

## 3. Quick Start - DOCX Stack

### Prerequisites
- Python 3.8+
- Required packages: `docxtpl`, `python-docx`, `docxcompose` (install via `pip`)

### Generate Sample Documents

```bash
# Navigate to the DOCX examples
cd docx-stack-examples

# Generate all example documents
python tools/run_all.py

# Or run individual examples:
python src/a1_docxtpl_basic.py         # Basic templating
python src/a2_richtext.py              # RichText formatting
python src/a3_images.py               # Image insertion
```

### Output Files
Generated documents will be saved in `docx-stack-examples/build/`:
- `out_a1_basic.docx`: Report with structured data
- `out_a2_richtext.docx`: Document with formatted text
- `out_a3_images.docx`: Document with embedded images

### Key Learning: Manual Template Creation
**Critical Discovery**: Templates must be created manually in Word/LibreOffice to avoid XML fragmentation. Programmatic template generation with `python-docx` causes Jinja2 tags to be split across multiple XML runs, making them invisible to `docxtpl`.

## 4. Project Achievements

### ✅ Major Issues Resolved
- **XML Fragmentation Problem**: Identified and solved the critical issue where Word automatically fragments Jinja2 tags in programmatically generated templates
- **RichText Syntax**: Discovered and documented the special `{{r variable }}` syntax for RichText objects
- **Template Creation**: Established best practices for manual template creation to ensure reliability

### 🎯 Current Status
- **DOCX Stack**: ✅ Complete and production-ready
- **Other Stacks**: 📋 Guides only (WeasyPrint, Pandoc, Chromium) - implementations pending

### 📚 Documentation
- Comprehensive guides with examples and troubleshooting
- Issue tracking with resolution documentation
- Best practices for template creation and maintenance