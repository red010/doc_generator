#!/usr/bin/env python
"""
Run all DOCX generation examples.
"""

from pathlib import Path
import sys

# Add src directory to path for finding scripts
src_dir = Path(__file__).parent.parent / "src"

import subprocess

# Use conda run to execute scripts in the correct environment
CONDA_ENV = "doc_gen"

if __name__ == "__main__":
    print("🚀 Esecuzione di tutti gli esempi DOCX...\n")

    try:
        print("📄 Eseguendo esempio base...")
        result1 = subprocess.run(["conda", "run", "-n", CONDA_ENV, "python", str(src_dir / "a1_docxtpl_basic.py")],
                                capture_output=True, text=True, cwd=src_dir.parent.parent)
        if result1.returncode == 0:
            print("✅ Esempio base completato con successo\n")
        else:
            print(f"❌ Errore nell'esempio base: {result1.stderr}\n")

        print("🎨 Eseguendo esempio RichText...")
        result2 = subprocess.run(["conda", "run", "-n", CONDA_ENV, "python", str(src_dir / "a2_richtext.py")],
                                capture_output=True, text=True, cwd=src_dir.parent.parent)
        if result2.returncode == 0:
            print("✅ Esempio RichText completato con successo\n")
        else:
            print(f"❌ Errore nell'esempio RichText: {result2.stderr}\n")

        print("🖼️ Eseguendo esempio immagini...")
        result3 = subprocess.run(["conda", "run", "-n", CONDA_ENV, "python", str(src_dir / "a3_images.py")],
                                capture_output=True, text=True, cwd=src_dir.parent.parent)
        if result3.returncode == 0:
            print("✅ Esempio immagini completato con successo\n")
        else:
            print(f"❌ Errore nell'esempio immagini: {result3.stderr}\n")

        print("🏗️ Eseguendo esempio generazione senza template...")
        result5 = subprocess.run(["conda", "run", "-n", CONDA_ENV, "python", str(src_dir / "a5_python_docx_only.py")],
                                capture_output=True, text=True, cwd=src_dir.parent.parent)
        if result5.returncode == 0:
            print("✅ Esempio generazione senza template completato con successo\n")
        else:
            print(f"❌ Errore nell'esempio generazione: {result5.stderr}\n")

        print("📄 Eseguendo esempio avanzato con output PDF...")
        result6 = subprocess.run(["conda", "run", "-n", CONDA_ENV, "python", str(src_dir / "a6_docxtpl_advanced.py")],
                                capture_output=True, text=True, cwd=src_dir.parent.parent)
        if result6.returncode == 0:
            print("✅ Esempio avanzato completato con successo\n")
        else:
            print(f"❌ Errore nell'esempio avanzato: {result6.stderr}\n")

        print("🎉 Tutti gli esempi completati con successo!")

    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)