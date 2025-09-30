"""
RichText Template Rendering Example
Demonstrates advanced text formatting with docxtpl RichText objects.
"""

from pathlib import Path
from typing import Optional
from docxtpl import DocxTemplate, RichText

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

TEMPLATE = ROOT / "templates" / "a2_richtext_template.docx"
OUT = BUILD / "out_a2_richtext.docx"


def create_rich_text_content() -> RichText:
    """
    Create a RichText object with various formatting styles.
    Demonstrates: italic, bold, colors, and multi-line content.
    """
    rt = RichText()

    # First line with mixed formatting
    rt.add("Questo è ", italic=True)
    rt.add("grassetto", bold=True)
    rt.add(" e ")
    rt.add("rosso", color="FF0000")
    rt.add(".\n")

    # Second line with normal text
    rt.add("Nuova linea con testo normale.\n")

    # Third line with more formatting combinations
    rt.add("E ")
    rt.add("corsivo", italic=True)
    rt.add(" + ")
    rt.add("grassetto", bold=True)
    rt.add(" insieme.")

    return rt


def render(output_path: Optional[Path] = None) -> Path:
    """
    Render the RichText template with formatted content.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated document.

    Raises:
        FileNotFoundError: If template file doesn't exist.
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

    print(f"📄 Caricamento template: {TEMPLATE.name}")
    doc = DocxTemplate(str(TEMPLATE))

    # Create RichText content
    print("🎨 Creazione contenuto RichText...")
    rich_content = create_rich_text_content()

    # Prepare context data
    ctx = {
        "intro": "Esempio di testo formattato con docxtpl.RichText.",
        "rich_paragraph": rich_content,
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
