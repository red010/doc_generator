#!/usr/bin/env python
"""
DOCX Stack Example A6: Advanced Templating with PDF Output
Generates a DOCX document from template and converts it to PDF using Pandoc.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from docxtpl import DocxTemplate
from jinja2 import Environment

# Configuration
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)


def check_dependencies() -> None:
    """Check if required dependencies are available."""
    # Check for pandoc
    try:
        result = subprocess.run(["pandoc", "--version"],
                              capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("pandoc is not installed or not in PATH. Please install pandoc.")

    # Check for xelatex
    try:
        result = subprocess.run(["xelatex", "--version"],
                              capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("xelatex is not installed or not in PATH. Please install a LaTeX distribution (e.g., TeX Live).")


def validate_file_path(file_path: Path, must_exist: bool = True) -> Path:
    """Validate and convert file path."""
    if must_exist and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if must_exist and not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return file_path


def convert_docx_to_pdf(docx_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert DOCX to PDF using Pandoc with XeLaTeX.

    Args:
        docx_path: Path to input DOCX file
        output_path: Optional output path, defaults to BUILD directory

    Returns:
        Path to generated PDF

    Raises:
        RuntimeError: If conversion fails
    """
    # Validate inputs
    input_path = validate_file_path(docx_path)

    if output_path is None:
        # Generate output filename based on input
        input_name = input_path.stem
        output_path = BUILD / f"{input_name}.pdf"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📄 Converting DOCX to PDF: {input_path}")
    print(f"📄 Output: {output_path}")

    # Build Pandoc command for DOCX to PDF conversion with maximum formatting preservation
    cmd = [
        "pandoc",
        str(input_path),
        "-o", str(output_path),
        "--pdf-engine=xelatex",
        # Enhanced typography and layout preservation
        "--variable=geometry:margin=1in",
        "--variable=fontsize=11pt",
        "--variable=mainfont=Times",  # Use available system fonts
        "--variable=sansfont=Arial",
        "--variable=monofont=Courier New",
        # Document structure and styling
        "--variable=documentclass=article",
        "--variable=linestretch=1.15",  # Standard line spacing
        "--variable=parskip=0pt",  # Preserve paragraph spacing
        "--variable=parindent=0pt",  # No paragraph indentation
        # Advanced DOCX formatting preservation options
        "--extract-media=./images",  # Extract images to subdirectory
        "--wrap=preserve",  # Preserve line breaks and spacing
        "--preserve-tabs"  # Preserve tab characters
    ]

    try:
        print("🔧 Running Pandoc conversion...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            print(f"✅ PDF generated successfully: {output_path}")
            return output_path
        else:
            error_msg = f"Pandoc conversion failed: {result.stderr}"
            print(f"❌ Error details: {error_msg}")
            raise RuntimeError(error_msg)

    except subprocess.CalledProcessError as e:
        error_msg = f"Pandoc conversion failed: {e}"
        if e.stderr:
            error_msg += f"\nError details: {e.stderr}"
        print(f"❌ Error: {error_msg}")
        raise RuntimeError(error_msg) from e
    except FileNotFoundError as e:
        raise RuntimeError(f"Pandoc command not found: {e}") from e


def generate_docx_from_template() -> Path:
    """
    Generate DOCX document from template using docxtpl.

    Returns:
        Path to generated DOCX file
    """
    print("📝 Generating DOCX from template...")

    # Load template
    template_path = DATA / "Template-OFF-V003-Jinja.docx"
    tpl = DocxTemplate(str(template_path))

    # Create custom Jinja2 environment for docxtpl 0.19.0
    from jinja2 import Environment
    custom_env = Environment(
        variable_start_string='[[',
        variable_end_string=']]',
        block_start_string='[%',
        block_end_string='%]',
        autoescape=False,
    )

    # Template data
    context = {
        "azienda": {
            "ragione_sociale": "Rossi S.r.l.",
            "indirizzo1": "Via Roma 1",
            "indirizzo2": "10100 Torino (TO)",
        },
        "offerta": {
            "numero": "251002A-001",
            "data": "02/10/2025",
        },
        "condizioni": [
            {"oggetto": "Consulenza AI", "importo": "1.200€ + IVA"},
            {"oggetto": "Formazione FastAPI (8h)", "importo": "900€ + IVA"},
        ],
        "fatturazione": {
            "acconto_importo": "1.050€ + IVA",
            "saldo_importo": "1.050€ + IVA",
        },
        "contatti": {"email": "amministrazione@ar-tik.com"},
    }

    # Render template with custom Jinja2 environment
    tpl.render(context, jinja_env=custom_env)

    # Save DOCX
    docx_output = BUILD / "out_a6_advanced.docx"
    tpl.save(str(docx_output))

    print(f"✅ DOCX generated: {docx_output}")
    return docx_output


def main() -> int:
    """Main function."""
    try:
        print("🚀 Starting Advanced DOCX Templating with PDF Output...")
        print("=" * 60)

        # Check dependencies first
        check_dependencies()

        # Generate DOCX from template
        docx_file = generate_docx_from_template()

        # Convert DOCX to PDF using Pandoc (reliable cross-platform solution)
        pdf_file = convert_docx_to_pdf(docx_file)

        print("\n🎉 Document generation completed!")
        print(f"   DOCX: {docx_file}")
        print(f"   PDF:  {pdf_file}")

        # Show file info
        for file_path in [docx_file, pdf_file]:
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"   {file_path.name}: {file_size / 1024:.1f} KB")

        return 0

    except RuntimeError as e:
        print(f"\n❌ Generation Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Generation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return 1


if __name__ == "__main__":
    exit(main())
