#!/usr/bin/env python
"""
Esempio: Creazione documento DOCX da zero con python-docx
Dimostra come generare documenti senza template, ma con limitazioni.
"""

from pathlib import Path
from typing import Optional
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuration
ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
OUT = BUILD / "out_a5_python_docx_only.docx"


def create_document_from_scratch(output_path: Optional[Path] = None) -> Path:
    """
    Crea un documento DOCX completamente da zero usando solo python-docx.
    Mostra i limiti rispetto all'approccio template-based.
    """
    if output_path is None:
        output_path = OUT

    print("🏗️ Creazione documento da zero con python-docx...")

    # Crea un nuovo documento vuoto
    doc = Document()

    # Aggiungi un titolo
    title = doc.add_heading('Rapporto di Esempio', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Aggiungi una sezione introduttiva
    intro = doc.add_paragraph()
    intro.add_run('Questo documento è stato generato completamente da zero ')
    intro.add_run('usando python-docx').bold = True
    intro.add_run(', senza utilizzare template.')

    # Aggiungi una tabella
    doc.add_heading('Dati di Esempio', level=1)

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    # Header della tabella
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Nome'
    header_cells[1].text = 'Valore'
    header_cells[2].text = 'Stato'

    # Dati della tabella (simulati)
    data = [
        ('Temperatura', '25°C', 'Normale'),
        ('Pressione', '1013 hPa', 'Normale'),
        ('Umidità', '60%', 'Elevata')
    ]

    for nome, valore, stato in data:
        row_cells = table.add_row().cells
        row_cells[0].text = nome
        row_cells[1].text = valore
        row_cells[2].text = stato

    # Aggiungi una lista
    doc.add_heading('Osservazioni', level=1)

    observations = [
        "Il sistema funziona correttamente",
        "Nessun errore rilevato nei log",
        "Performance entro i parametri normali"
    ]

    for obs in observations:
        doc.add_paragraph(obs, style='List Bullet')

    # Aggiungi un'immagine (se esiste)
    try:
        img_path = ROOT / "tools" / "assets" / "product.png"
        if img_path.exists():
            doc.add_heading('Immagine di Esempio', level=1)
            doc.add_picture(str(img_path), width=Inches(3))
            doc.add_paragraph('Immagine inserita dinamicamente').italic = True
    except Exception as e:
        print(f"⚠️ Impossibile aggiungere immagine: {e}")

    # Salva il documento
    doc.save(str(output_path))
    print(f"✅ Documento creato: {output_path}")

    return output_path


def main():
    """Entry point"""
    try:
        result = create_document_from_scratch()
        print(f"\n🎉 Successo! Documento creato: {result}")
        print("\n📋 Limiti dell'approccio senza template:")
        print("- Molto codice per layout semplici")
        print("- Difficile gestire stili complessi")
        print("- Non scalabile per documenti grandi")
        print("- Nessuna separazione tra logica e presentazione")
        print("\n💡 Template + docxtpl = approccio consigliato!")

    except Exception as e:
        print(f"\n❌ Errore: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
