#!/usr/bin/env python
"""
Run all DOCX generation examples.
"""

from pathlib import Path
import sys

# Add src directory to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from a1_docxtpl_basic import render as r1
from a2_richtext import render as r2
from a3_images import render as r3
from a5_python_docx_only import create_document_from_scratch as r5

if __name__ == "__main__":
    print("🚀 Esecuzione di tutti gli esempi DOCX...\n")

    try:
        print("📄 Eseguendo esempio base...")
        result1 = r1()
        print(f"✅ {result1}\n")

        print("🎨 Eseguendo esempio RichText...")
        result2 = r2()
        print(f"✅ {result2}\n")

        print("🖼️ Eseguendo esempio immagini...")
        result3 = r3()
        print(f"✅ {result3}\n")

        print("🏗️ Eseguendo esempio generazione senza template...")
        result5 = r5()
        print(f"✅ {result5}\n")

        print("🎉 Tutti gli esempi completati con successo!")

    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)