"""
Basic DOCX Template Rendering Example
Demonstrates fundamental docxtpl usage with JSON data and Jinja2 templating.
"""

from pathlib import Path
from typing import Optional
import json
from docxtpl import DocxTemplate

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

TEMPLATE = ROOT / "templates" / "a1_basic_template.docx"
DATA = ROOT / "data" / "a1_data.json"
OUT = BUILD / "out_a1_basic.docx"


def render(output_path: Optional[Path] = None) -> Path:
    """
    Render the basic template with JSON data.

    Args:
        output_path: Optional custom output path. Defaults to OUT.

    Returns:
        Path to the generated document.

    Raises:
        FileNotFoundError: If template or data files don't exist.
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

    # Validate data exists
    if not DATA.exists():
        raise FileNotFoundError(f"File dati mancante: {DATA}")

    print(f"📄 Caricamento template: {TEMPLATE.name}")
    print(f"📊 Caricamento dati: {DATA.name}")

    # Load data and template
    ctx = json.loads(Path(DATA).read_text(encoding="utf-8"))
    doc = DocxTemplate(str(TEMPLATE))

    # Validate template variables (if method exists)
    try:
        missing = doc.get_undeclared_template_variables(ctx)
        if missing:
            raise KeyError(f"Variabili non dichiarate nel contesto: {sorted(missing)}")
    except AttributeError:
        # get_undeclared_template_variables not available in all versions
        pass

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
