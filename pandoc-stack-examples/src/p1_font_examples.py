#!/usr/bin/env python
"""
Esempi di utilizzo di configurazioni font personalizzate con p1_markdown_to_pdf.py
Dimostra diverse modalità per configurare font e parametri tipografici.
"""

from pathlib import Path
from p1_markdown_to_pdf import PandocConfig, convert_markdown_to_pdf

# Directory del progetto
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)

def esempio_font_classici():
    """Esempio con font classici (Times, Helvetica, Courier)"""
    print("🎨 Esempio 1: Font classici")

    config = PandocConfig.customize_fonts(
        mainfont="Times",
        sansfont="Helvetica",
        monofont="Courier"
    )

    input_file = ROOT / "data/markdown/sample_report.md"
    output_file = BUILD / "esempio_classici.pdf"

    convert_markdown_to_pdf(input_file, output_file, config)
    print(f"   ✅ Generato: {output_file}")


def esempio_font_moderni():
    """Esempio con tentativo di font moderni (se disponibili)"""
    print("\n🎨 Esempio 2: Font moderni (fallback automatico)")

    config = PandocConfig.customize_fonts(
        mainfont="Georgia",  # Serif moderno
        sansfont="Verdana",  # Sans-serif moderno
        monofont="Consolas"  # Monospace moderno
    )

    input_file = ROOT / "data/markdown/sample_report.md"
    output_file = BUILD / "esempio_moderni.pdf"

    try:
        convert_markdown_to_pdf(input_file, output_file, config)
        print(f"   ✅ Generato: {output_file}")
    except Exception as e:
        print(f"   ⚠️  Font moderni non disponibili, usando fallback: {e}")


def esempio_senza_font():
    """Esempio senza font personalizzati (usa default LaTeX)"""
    print("\n🎨 Esempio 3: Senza font personalizzati")

    config = PandocConfig.create_minimal()

    input_file = ROOT / "data/markdown/sample_report.md"
    output_file = BUILD / "esempio_minimal.pdf"

    convert_markdown_to_pdf(input_file, output_file, config)
    print(f"   ✅ Generato: {output_file}")


def esempio_yaml_frontmatter():
    """Esempio usando configurazione nel front matter YAML"""
    print("\n🎨 Esempio 4: Configurazione via YAML front matter")

    # Usa configurazione di default, ma il documento può sovrascrivere
    # tramite il proprio front matter YAML
    config = PandocConfig()

    input_file = ROOT / "data/markdown/sample_with_fonts.md"
    output_file = BUILD / "esempio_yaml.pdf"

    convert_markdown_to_pdf(input_file, output_file, config)
    print(f"   ✅ Generato: {output_file}")
    print("   📝 I font sono definiti nel front matter YAML del documento")


def main():
    """Esegui tutti gli esempi"""
    print("🚀 Esempi di configurazione font per Pandoc PDF")
    print("=" * 50)

    try:
        esempio_font_classici()
        esempio_font_moderni()
        esempio_senza_font()
        esempio_yaml_frontmatter()

        print("\n🎉 Tutti gli esempi completati!")
        print("\n📁 File generati nella directory build/:")
        for pdf in BUILD.glob("esempio_*.pdf"):
            print(f"   • {pdf.name}")

    except Exception as e:
        print(f"\n❌ Errore: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
