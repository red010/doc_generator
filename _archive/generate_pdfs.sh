#!/bin/bash
# PDF Generation Wrapper Script
# Imposta DYLD_LIBRARY_PATH per WeasyPrint su macOS

# Imposta il path delle librerie GTK per macOS
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Determina automaticamente la directory reports del progetto corrente
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_DIR="$(pwd)"

# Cerca la directory reports partendo dalla directory corrente
PROJECT_ROOT="$CURRENT_DIR"
REPORTS_DIR=""

# Cerca nella directory corrente e in quelle superiori
for i in {1..5}; do
    if [ -d "$PROJECT_ROOT/analysis/reports" ]; then
        REPORTS_DIR="$PROJECT_ROOT/analysis/reports"
        break
    elif [ -d "$PROJECT_ROOT/reports" ]; then
        REPORTS_DIR="$PROJECT_ROOT/reports"
        break
    fi
    PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
done

if [ -z "$REPORTS_DIR" ]; then
    echo "❌ Directory reports non trovata"
    echo "   Directory corrente: $CURRENT_DIR"
    echo "   Cerca in: ./analysis/reports o ./reports (fino a 5 livelli superiori)"
    echo ""
    echo "💡 Suggerimenti:"
    echo "   • Esegui questo script dalla radice del progetto"
    echo "   • O specifica manualmente: ./generate_pdfs.sh --reports-dir /percorso/reports"
    exit 1
fi

echo "📁 Directory reports rilevata: $REPORTS_DIR"

# Verifica se è stato specificato manualmente --reports-dir
if [[ "$*" == *--reports-dir* ]]; then
    # Usa il percorso specificato dall'utente
    python "$SCRIPT_DIR/report_pdf_generator.py" "$@"
else
    # Usa il percorso rilevato automaticamente
    python "$SCRIPT_DIR/report_pdf_generator.py" --reports-dir "$REPORTS_DIR" "$@"
fi
