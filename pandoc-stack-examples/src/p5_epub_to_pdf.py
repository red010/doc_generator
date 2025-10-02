#!/usr/bin/env python
"""
Pandoc Stack Example 5: EPUB to PDF Conversion
Converts EPUB files to professional PDF using Pandoc and XeLaTeX.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

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


def convert_epub_to_pdf(epub_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert EPUB to PDF using Pandoc with XeLaTeX.

    Args:
        epub_path: Path to input EPUB file
        output_path: Optional output path, defaults to BUILD directory

    Returns:
        Path to generated PDF

    Raises:
        RuntimeError: If conversion fails
    """
    # Validate inputs
    input_path = validate_file_path(epub_path)

    if output_path is None:
        # Generate output filename based on input
        input_name = input_path.stem
        output_path = BUILD / f"{input_name}.pdf"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📖 Converting EPUB to PDF: {input_path}")
    print(f"📄 Output: {output_path}")

    # Build Pandoc command for EPUB conversion
    cmd = [
        "pandoc",
        str(input_path),
        "-o", str(output_path),
        "--pdf-engine=xelatex",
        "--variable=geometry:margin=1in",
        "--variable=fontsize=11pt",
        "--variable=colorlinks=true",
        "--variable=linkcolor=blue",
        "--variable=urlcolor=blue",
        "--variable=citecolor=green",
        # EPUB specific options
        "--extract-media=./images",  # Extract images to subdirectory
        "--wrap=none",  # Don't wrap lines
        "--toc",  # Generate table of contents
        "--toc-depth=3",
        "--number-sections",  # Number sections
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


def main() -> int:
    """Main function."""
    try:
        print("🚀 Starting EPUB to PDF conversion...")
        print("=" * 50)

        # Check dependencies first
        check_dependencies()

        # Define input EPUB file
        epub_file = DATA / "LP 500 Best Places to See.epub"

        if not epub_file.exists():
            print(f"❌ Error: EPUB file not found: {epub_file}")
            print(f"Please ensure the file exists at: {epub_file}")
            return 1

        # Convert to PDF
        result = convert_epub_to_pdf(epub_file)

        print("\n🎉 EPUB to PDF conversion completed!")
        print(f"   Input:  {epub_file}")
        print(f"   Output: {result}")

        # Show file info
        if result.exists():
            file_size = result.stat().st_size
            print(f"   Size: {file_size / (1024*1024):.1f} MB")

            # Check if images directory was created
            images_dir = BUILD / "images"
            if images_dir.exists():
                image_count = len(list(images_dir.glob("*")))
                print(f"   Images extracted: {image_count}")
        else:
            print("   ⚠️  Warning: Output file was not found after conversion")

        return 0

    except RuntimeError as e:
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

