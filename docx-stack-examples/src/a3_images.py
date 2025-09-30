"""
Image Template Rendering Example
Demonstrates inline image insertion with docxtpl InlineImage objects.
"""

from pathlib import Path
from typing import Optional
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

TEMPLATE = ROOT / "templates" / "a3_images_template.docx"
IMG = ROOT / "data" / "images" / "product.png"
OUT = BUILD / "out_a3_images.docx"


def create_inline_image(doc_template: DocxTemplate, image_path: Path, width_mm: int = 60) -> InlineImage:
    """
    Create an InlineImage object with specified dimensions.

    Args:
        doc_template: The DocxTemplate instance
        image_path: Path to the image file
        width_mm: Width in millimeters (default: 60mm)

    Returns:
        InlineImage object ready for template rendering
    """
    return InlineImage(doc_template, str(image_path), width=Mm(width_mm))


def render(output_path: Optional[Path] = None) -> Path:
    """
    Render the image template with inline image and caption.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated document.

    Raises:
        FileNotFoundError: If template or image files don't exist.
    """
    if output_path is None:
        output_path = OUT

    # Validate template exists
    if not TEMPLATE.exists():
        raise FileNotFoundError(
            f"Template mancante: {TEMPLATE}\n"
            "Crea il template manualmente seguendo la guida:\n"
            "docx-stack-examples/guide/create_manual_template_guide.md"
        )

    # Validate image exists
    if not IMG.exists():
        raise FileNotFoundError(
            f"Immagine mancante: {IMG}\n"
            "Genera le immagini eseguendo:\n"
            "python tools/make_assets.py"
        )

    print(f"📄 Caricamento template: {TEMPLATE.name}")
    doc = DocxTemplate(str(TEMPLATE))

    # Create inline image
    print(f"🖼️ Caricamento immagine: {IMG.name}")
    image = create_inline_image(doc, IMG, width_mm=60)

    # Prepare context data
    ctx = {
        "image": image,  # InlineImage object
        "caption": "Figura 1 — Immagine di prodotto (60mm).",
    }

    # Render and save
    print(f"⚙️ Rendering documento...")
    doc.render(ctx)
    doc.save(str(output_path))

    print(f"✅ Documento generato: {output_path}")
    return output_path


if __name__ == "__main__":
    try:
        result = render()
        print(f"\n🎉 Successo! File creato: {result}")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        exit(1)
