#!/usr/bin/env python
"""
DOCX Stack Example A6: Advanced Templating with PDF Output
Generates a DOCX document from template and converts it to PDF using docx2pdf (LibreOffice/Word).
Falls back to Pandoc if docx2pdf is not available.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Literal
from docxtpl import DocxTemplate
from jinja2 import Environment

# Configuration
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

# Custom Jinja2 environment for docxtpl with custom delimiters
JINJA_ENV = Environment(
    variable_start_string='[[',
    variable_end_string=']]',
    block_start_string='[%',
    block_end_string='%]',
    autoescape=False,
)

# Conversion methods
ConversionMethod = Literal["libreoffice", "pandoc", "auto"]


def detect_office_backend() -> Optional[str]:
    """
    Detect available Office backend for docx2pdf conversion.
    
    Returns:
        Backend name ("libreoffice", "msword", or None)
    """
    # Check for LibreOffice (macOS paths)
    libreoffice_paths = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/opt/homebrew/bin/soffice",
        "/usr/local/bin/soffice",
        "/usr/bin/soffice"
    ]
    
    for path in libreoffice_paths:
        if Path(path).exists():
            return "libreoffice"
    
    # Check for Microsoft Word (macOS)
    if Path("/Applications/Microsoft Word.app").exists():
        return "msword"
    
    return None


def check_docx2pdf_available() -> bool:
    """
    Check if docx2pdf library is available.
    
    Returns:
        True if docx2pdf can be imported, False otherwise
    """
    try:
        import docx2pdf
        return True
    except ImportError:
        return False


def check_dependencies(method: ConversionMethod = "auto") -> ConversionMethod:
    """
    Check if required dependencies are available and determine conversion method.
    
    Args:
        method: Desired conversion method ("libreoffice", "pandoc", or "auto")
    
    Returns:
        The conversion method to use
        
    Raises:
        RuntimeError: If required dependencies are not available
    """
    # Check LibreOffice availability
    office_backend = detect_office_backend()
    
    # Check pandoc availability
    has_pandoc = False
    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        has_pandoc = True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Determine conversion method
    if method == "auto":
        if office_backend:
            return "libreoffice"
        elif has_pandoc:
            return "pandoc"
        else:
            raise RuntimeError(
                "No PDF conversion method available. Please install either:\n"
                "  1. LibreOffice (recommended for formatting preservation)\n"
                "     macOS: brew install --cask libreoffice\n"
                "     Linux: sudo apt-get install libreoffice\n"
                "  2. pandoc + xelatex (faster but may lose formatting)"
            )
    elif method == "libreoffice":
        if not office_backend:
            raise RuntimeError(
                "LibreOffice not found. Please install LibreOffice:\n"
                "  macOS: brew install --cask libreoffice\n"
                "  Linux: sudo apt-get install libreoffice"
            )
        return "libreoffice"
    elif method == "pandoc":
        if not has_pandoc:
            raise RuntimeError("pandoc is not installed. Please install pandoc.")
        # Check for xelatex
        try:
            subprocess.run(
                ["xelatex", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "xelatex is not installed. Please install a LaTeX distribution (e.g., TeX Live)."
            )
        return "pandoc"
    
    return method


def validate_file_path(file_path: Path, must_exist: bool = True) -> Path:
    """
    Validate and convert file path.
    
    Args:
        file_path: Path to validate
        must_exist: Whether the file must already exist
        
    Returns:
        Validated Path object
        
    Raises:
        FileNotFoundError: If file doesn't exist and must_exist is True
        ValueError: If path is not a file
    """
    if must_exist and not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if must_exist and not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return file_path


def convert_docx_to_pdf_with_libreoffice(docx_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert DOCX to PDF using LibreOffice directly (headless mode).
    This method preserves all formatting from the original DOCX.
    
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
    
    print(f"📄 Converting DOCX to PDF using LibreOffice (preserves all formatting)")
    print(f"   Input:  {input_path}")
    print(f"   Output: {output_path}")
    
    # Find LibreOffice executable
    libreoffice_paths = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/opt/homebrew/bin/soffice",
        "/usr/local/bin/soffice",
        "/usr/bin/soffice"
    ]
    
    soffice_path = None
    for path in libreoffice_paths:
        if Path(path).exists():
            soffice_path = path
            break
    
    if not soffice_path:
        raise RuntimeError("LibreOffice executable not found")
    
    print(f"   LibreOffice: {soffice_path}")
    
    try:
        print("🔧 Running LibreOffice conversion...")
        
        # Delete existing PDF if it exists (LibreOffice won't overwrite)
        if output_path.exists():
            output_path.unlink()
        
        # LibreOffice command for DOCX to PDF conversion
        # --headless: run without GUI
        # --convert-to pdf: convert to PDF format
        # --outdir: output directory
        cmd = [
            soffice_path,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_path.parent),
            str(input_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=120  # 2 minutes timeout for large files
        )
        
        # LibreOffice creates the PDF with the same name as the input
        expected_pdf = output_path.parent / f"{input_path.stem}.pdf"
        
        # Rename if needed
        if expected_pdf != output_path and expected_pdf.exists():
            expected_pdf.rename(output_path)
        
        # Validate that PDF was actually created
        if not output_path.exists():
            raise RuntimeError(f"PDF file was not created: {output_path}")
        
        # Validate that PDF has content
        if output_path.stat().st_size == 0:
            raise RuntimeError(f"PDF file is empty: {output_path}")
        
        print(f"✅ PDF generated successfully: {output_path}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
        return output_path
        
    except subprocess.CalledProcessError as e:
        error_msg = f"LibreOffice conversion failed with return code {e.returncode}"
        if e.stderr:
            error_msg += f"\nError details: {e.stderr}"
        if e.stdout:
            error_msg += f"\nOutput: {e.stdout}"
        print(f"❌ Error: {error_msg}")
        raise RuntimeError(error_msg) from e
    except subprocess.TimeoutExpired:
        raise RuntimeError("LibreOffice conversion timed out after 120 seconds")
    except Exception as e:
        error_msg = f"LibreOffice conversion failed: {e}"
        print(f"❌ Error: {error_msg}")
        raise RuntimeError(error_msg) from e


def convert_docx_to_pdf_with_pandoc(docx_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert DOCX to PDF using Pandoc with XeLaTeX.
    Note: This method may lose some advanced formatting from the original DOCX.

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

    print(f"📄 Converting DOCX to PDF using Pandoc (may lose some formatting)")
    print(f"   Input:  {input_path}")
    print(f"   Output: {output_path}")

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
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=60  # 60 second timeout for large files
        )

        # Validate that PDF was actually created
        if not output_path.exists():
            raise RuntimeError(f"PDF file was not created: {output_path}")
        
        # Validate that PDF has content
        if output_path.stat().st_size == 0:
            raise RuntimeError(f"PDF file is empty: {output_path}")

        print(f"✅ PDF generated successfully: {output_path}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
        return output_path

    except subprocess.CalledProcessError as e:
        error_msg = f"Pandoc conversion failed with return code {e.returncode}"
        if e.stderr:
            error_msg += f"\nError details: {e.stderr}"
        print(f"❌ Error: {error_msg}")
        raise RuntimeError(error_msg) from e
    except subprocess.TimeoutExpired:
        raise RuntimeError("Pandoc conversion timed out after 60 seconds")
    except FileNotFoundError as e:
        raise RuntimeError(f"Pandoc command not found: {e}") from e


def convert_docx_to_pdf(
    docx_path: Path,
    output_path: Optional[Path] = None,
    method: ConversionMethod = "auto"
) -> Path:
    """
    Convert DOCX to PDF using the specified or auto-detected method.
    
    Args:
        docx_path: Path to input DOCX file
        output_path: Optional output path, defaults to BUILD directory
        method: Conversion method ("libreoffice", "pandoc", or "auto")
    
    Returns:
        Path to generated PDF
        
    Raises:
        RuntimeError: If conversion fails or required dependencies are missing
    """
    # Determine the best conversion method
    actual_method = check_dependencies(method)
    
    print(f"\n📋 Using conversion method: {actual_method}")
    
    if actual_method == "libreoffice":
        return convert_docx_to_pdf_with_libreoffice(docx_path, output_path)
    elif actual_method == "pandoc":
        return convert_docx_to_pdf_with_pandoc(docx_path, output_path)
    else:
        raise RuntimeError(f"Unknown conversion method: {actual_method}")


def get_template_context() -> Dict[str, Any]:
    """
    Get the template context data.
    
    Returns:
        Dictionary containing template variables
    """
    return {
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


def generate_docx_from_template() -> Path:
    """
    Generate DOCX document from template using docxtpl.

    Returns:
        Path to generated DOCX file
        
    Raises:
        FileNotFoundError: If template file is not found
        RuntimeError: If DOCX generation fails
    """
    print("📝 Generating DOCX from template...")

    # Load template
    template_path = DATA / "Template-OFF-V003-Jinja.docx"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    tpl = DocxTemplate(str(template_path))

    # Get template data
    context = get_template_context()

    # Render template with custom Jinja2 environment
    tpl.render(context, jinja_env=JINJA_ENV)

    # Save DOCX
    docx_output = BUILD / "out_a6_advanced.docx"
    tpl.save(str(docx_output))
    
    # Validate that DOCX was created successfully
    if not docx_output.exists():
        raise RuntimeError(f"DOCX file was not created: {docx_output}")
    
    # Validate that DOCX has content
    if docx_output.stat().st_size == 0:
        raise RuntimeError(f"DOCX file is empty: {docx_output}")

    print(f"✅ DOCX generated: {docx_output}")
    print(f"   File size: {docx_output.stat().st_size / 1024:.1f} KB")
    return docx_output


def main(conversion_method: ConversionMethod = "auto") -> int:
    """
    Main function to orchestrate document generation.
    
    Args:
        conversion_method: PDF conversion method to use ("libreoffice", "pandoc", or "auto")
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        print("🚀 Starting Advanced DOCX Templating with PDF Output...")
        print("=" * 60)

        # Detect available conversion methods
        print("\n🔍 Detecting available conversion methods...")
        backend = detect_office_backend()
        
        if backend:
            print(f"   ✅ LibreOffice available (backend: {backend})")
        else:
            print(f"   ❌ LibreOffice not available")
        
        try:
            subprocess.run(["pandoc", "--version"], capture_output=True, check=True, timeout=5)
            print(f"   ✅ pandoc available")
        except:
            print(f"   ❌ pandoc not available")

        # Generate DOCX from template
        print("\n" + "=" * 60)
        docx_file = generate_docx_from_template()

        # Convert DOCX to PDF (method will be auto-selected or use specified method)
        print("\n" + "=" * 60)
        pdf_file = convert_docx_to_pdf(docx_file, method=conversion_method)

        print("\n" + "=" * 60)
        print("🎉 Document generation completed successfully!")
        print(f"\n📁 Generated files:")
        print(f"   DOCX: {docx_file.name} ({docx_file.stat().st_size / 1024:.1f} KB)")
        print(f"   PDF:  {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
        print(f"\n📂 Output directory: {BUILD}")

        return 0

    except (RuntimeError, FileNotFoundError, ValueError) as e:
        print(f"\n❌ Generation Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⏹️  Generation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
