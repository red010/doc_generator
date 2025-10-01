---

title: "Pipeline Pandoc → (XeLaTeX/LuaLaTeX | Tectonic) & Pandoc → Typst — guida estesa 2025"
description: "Come trasformare Markdown in PDF con Pandoc e motori moderni: TeX Live (XeLaTeX/LuaLaTeX), Tectonic per build riproducibili e la pipeline Pandoc → Typst. Spiegazioni dei concetti, font CJK/RTL/emoji, esempi Python completi, checklist e troubleshooting."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-10-01"
  version: "1.2"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["pandoc", "latex", "xelatex", "lualatex", "tectonic", "typst", "pdf", "markdown", "fontspec", "polyglossia", "babel", "CJK", "RTL", "emoji", "python", "riproducibilità"]

---

# Pipeline Pandoc → (XeLaTeX/LuaLaTeX | Tectonic) & Pandoc → Typst

> Obiettivo: ottenere **PDF tipograficamente solidi** a partire da **Markdown**, scegliendo consapevolmente tra:
>
> * **TeX Live + XeLaTeX/LuaLaTeX** (ecosistema LaTeX completo);
> * **Tectonic** (LaTeX moderno, **build riproducibili** senza installazioni pesanti);
> * **Pandoc → Typst** (linguaggio di impaginazione **moderno e veloce**).

---

## 1) Panoramica dei componenti

### 1.1 Pandoc (convertitore “universale”)

* **Cosa fa**: legge Markdown (e molti altri formati), lo normalizza in un **AST interno** e lo riscrive nel formato di destinazione (LaTeX, Typst, HTML, DOCX, ecc.).
* **Perché è centrale**: è il collante tra **testo sorgente** (Markdown) e **motore di impaginazione** (LaTeX/Typst).
* **Opzioni chiave**:

  * `--pdf-engine=<engine>`: seleziona il motore PDF quando si produce direttamente un PDF (es. `xelatex`, `lualatex`, `tectonic`).
  * `-t typst`: produce **codice Typst** (`.typ`) invece del PDF, per poi compilarlo con **Typst**.
  * **Metadati/YAML**: front matter nel Markdown per titolo, autore, font, variabili template.
  * **Template**: file LaTeX/Typst personalizzati richiamati da Pandoc.

### 1.2 TeX Live + XeLaTeX / LuaLaTeX

* **TeX Live**: la “distribuzione” che fornisce eseguibili (xelatex, lualatex, pdflatex…) e **pacchetti** LaTeX.
* **XeLaTeX**:

  * Supporto **Unicode** e **font di sistema** tramite **fontspec**.
  * Ottimo per **CJK** (Cinese/Giapponese/Coreano) con **xeCJK** e per lingue **RTL** (right-to-left) via **polyglossia/bidi**.
* **LuaLaTeX**:

  * Simile a XeLaTeX per font e Unicode, ma con il motore **LuaTeX** (estendibile via Lua).
  * Per CJK: **luatexja**; per lingue: **babel**/**polyglossia**.
* **Perché usarli**: compatibilità massima con l’ecosistema LaTeX (pacchetti maturi: BibLaTeX, TikZ, microtype, tabelle complesse, matematica).

### 1.3 Tectonic (engine LaTeX “self-contained”)

* **Cosa fa**: compila LaTeX scaricando **on-demand** i pacchetti necessari e mantenendo un **bundle** coerente.
* **Vantaggi**: setup minimo, **build riproducibili**, perfetto in **CI/CD** o Docker.
* **Nota**: è un **motore LaTeX** alternativo a xelatex/lualatex; si seleziona da Pandoc con `--pdf-engine=tectonic`.

### 1.4 Typst (linguaggio di impaginazione moderno)

* **Cosa è**: un linguaggio e motore di composizione **snello e veloce**, alternativo a LaTeX.
* **Come si integra**: Pandoc può produrre **`.typ`** (writer Typst). Poi si compila a PDF:

  * via **CLI**: `typst compile input.typ output.pdf`
  * via **Python**: **typst-py** (binding che invoca il compilatore).
* **Perché usarlo**: ottimo equilibrio tra **semplicità, velocità e qualità** con template moderni; curva apprendimento più dolce di LaTeX.

---

## 2) Quando scegliere cosa (con esempi di scenario)

**Scegli TeX Live (XeLaTeX/LuaLaTeX) se:**

* Devi usare **pacchetti LaTeX avanzati** (TikZ complessi, pacchetti tabellari particolari, BibLaTeX con stili editoriali specifici).
* Hai **requisiti tipografici raffinati** ereditati da flussi LaTeX esistenti.
* Gestisci **documenti accademici**/editoriali con bibliografie, glossari, indici, tabelle lunghe, note a piè di pagina complesse.

**Scegli Tectonic se:**

* Vuoi **riproducibilità** e build **deterministici** (stesso output ovunque, senza “drift” del TeX tree).
* Operi in **CI/CD**, Docker o ambienti dove installare l’intero TeX Live è oneroso.
* Non ti servono pacchetti esotici non ancora supportati nel bundle Tectonic.

**Scegli Pandoc → Typst se:**

* Cerchi **velocità**, **template puliti** e manutenzione semplice.
* L’impaginato è strutturato (report, white paper, manuali) senza dipendenze profonde da macro/pacchetti LaTeX.
* Vuoi una pipeline **Markdown → (Pandoc) .typ → (Typst) PDF** più **snella** del mondo LaTeX.

---

## 3) Font fallback, CJK/RTL, emoji — linee guida pratiche

### 3.1 Scelta font “universale”

* Preferisci famiglie **Noto** per copertura ampia:

  * **Noto Serif** / **Noto Sans** / **Noto Mono**
  * **Noto Sans CJK** (SC/TC/JP/KR) per Cinese/Giapponese/Coreano
  * **Noto Color Emoji** per emoji
* **DejaVu** è un’alternativa valida per latino/greco/cirillico (meno copertura CJK).

### 3.2 Con XeLaTeX/LuaLaTeX (via `fontspec`)

* Imposta i font nel **front matter YAML** o con `-V` (variabili Pandoc):

  ```yaml
  ---
  title: "Esempio Internazionale"
  lang: it
  mainfont: "Noto Serif"
  sansfont: "Noto Sans"
  monofont: "DejaVu Sans Mono"
  CJKmainfont: "Noto Sans CJK SC"
  mathfont: "TeX Gyre Termes Math"
  mainfontoptions: "Ligatures=TeX"
  ---
  ```
* **CJK**: con XeLaTeX usa **xeCJK** (caricato dal template), con LuaLaTeX **luatexja**.
* **RTL (arabo/ebraico)**: usa **polyglossia** (o **babel**) e assicurati che il template carichi i pacchetti giusti (bidi).

### 3.3 Con Typst

* Definisci i font nel template `.typ`:

  ```typ
  #set text(font: "Noto Serif")
  #let code = text.with(font: "DejaVu Sans Mono")
  #set heading(level: 1, text: text.with(font: "Noto Sans"))
  ```
* Per CJK/emoji, installa i relativi font nel sistema/container e dichiarali nel template.
* Tip: crea **stili** tipst per titoli/codice/tabelle e riusali.

---

## 4) Flussi operativi (CLI) essenziali

### 4.1 Markdown → PDF con XeLaTeX

```bash
pandoc input.md -o out.pdf --pdf-engine=xelatex \
  -V mainfont="Noto Serif" -V monofont="DejaVu Sans Mono"
```

### 4.2 Markdown → PDF con LuaLaTeX

```bash
pandoc input.md -o out.pdf --pdf-engine=lualatex \
  -V mainfont="Noto Serif" -V monofont="DejaVu Sans Mono"
```

### 4.3 Markdown → PDF con Tectonic (build riproducibile)

```bash
pandoc input.md -o out.pdf --pdf-engine=tectonic
```

### 4.4 Box “Esperto” — Markdown → Typst → PDF

```bash
# 1) Genera codice Typst
pandoc input.md -t typst -o out.typ

# 2) Compila a PDF con Typst
typst compile out.typ out.pdf
```

---

## 5) Esempi Python completi

> Gli esempi assumono che **pandoc** e (a seconda del caso) **xelatex / lualatex / tectonic / typst** siano nel PATH.

### 5.1 `subprocess` + Pandoc (XeLaTeX/Tectonic)

```python
import subprocess
from pathlib import Path

def md_to_pdf(md_path: str, pdf_path: str, engine: str = "tectonic"):
    """
    Compila un Markdown in PDF usando Pandoc e il motore selezionato.
    engine: "xelatex", "lualatex" oppure "tectonic".
    """
    cmd = [
        "pandoc", md_path, "-o", pdf_path,
        "--pdf-engine", engine,
        "-V", "mainfont=Noto Serif",
        "-V", "monofont=DejaVu Sans Mono",
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    Path("out").mkdir(exist_ok=True)
    md_to_pdf("input.md", "out/tectonic.pdf", engine="tectonic")
    md_to_pdf("input.md", "out/xelatex.pdf", engine="xelatex")
```

### 5.2 `pypandoc` (facilitatore Python)

```python
import pypandoc

def md_to_pdf_pypandoc(md_path: str, pdf_path: str, engine: str = "lualatex"):
    pypandoc.convert_file(
        source_file=md_path,
        to="pdf",
        outputfile=pdf_path,
        extra_args=[
            f"--pdf-engine={engine}",
            "-V", "mainfont=Noto Serif",
            "-V", "monofont=DejaVu Sans Mono",
        ],
    )

if __name__ == "__main__":
    md_to_pdf_pypandoc("input.md", "out_lualatex.pdf", engine="lualatex")
```

### 5.3 Pipeline Pandoc → Typst + **typst-py** (solo Python)

```python
from pathlib import Path
import subprocess
import typst  # typst-py

BASE = Path("build"); BASE.mkdir(exist_ok=True)

# 1) Markdown -> Typst (.typ)
subprocess.run(["pandoc", "input.md", "-t", "typst", "-o", BASE/"doc.typ"], check=True)

# 2) Compilazione Typst -> PDF via typst-py
typst.compile(str(BASE/"doc.typ"), output=str(BASE/"doc.pdf"))
print("PDF generato:", (BASE/"doc.pdf").resolve())
```

---

## 6) Template di partenza

### 6.1 Template LaTeX per Pandoc (estratto minimo)

Salva come `template.tex` e passalo a Pandoc con `--template=template.tex`:

```tex
\documentclass[12pt]{article}
\usepackage{fontspec} % XeLaTeX/LuaLaTeX
\usepackage{polyglossia}
\setmainlanguage{italian}

% Font (sostituisci con le tue famiglie installate)
\setmainfont{Noto Serif}
\setsansfont{Noto Sans}
\setmonofont{DejaVu Sans Mono}

% CJK (XeLaTeX): \usepackage{xeCJK} \setCJKmainfont{Noto Sans CJK SC}
% CJK (LuaLaTeX): \usepackage{luatexja}

% Margini e microtipografia
\usepackage[margin=2.2cm]{geometry}
\usepackage{microtype}

\begin{document}

$if(title)$\section*{$title$}$endif$
$body$

\end{document}
```

### 6.2 Template Typst di base (`layout.typ`)

```typ
#set page(size: "a4", margin: 2.2cm)
#set text(font: "Noto Serif", size: 12pt)
#let code = text.with(font: "DejaVu Sans Mono", size: 10.5pt)
#set heading(level: 1, text: text.with(font: "Noto Sans", weight: "bold", size: 18pt))

// Titolo (se passato come variabile)
#if defined(title) [
  = [#title]
]

#show: doc => {
  doc
}
```

Uso con Pandoc → Typst:

```bash
pandoc input.md -t typst -o out.typ --template=layout.typ
typst compile out.typ out.pdf
```

---

## 7) Requirements

### 7.1 `requirements.txt` (Python)

```txt
pypandoc>=1.13      # opzionale: wrapper Python per pandoc
typst>=0.8          # "typst-py", binding Python al compilatore Typst
```

> **Nota**: `pypandoc` non installa Pandoc; serve l’eseguibile nel PATH.

### 7.2 Strumenti esterni (da installare nel sistema/CI)

* **pandoc** (consigliata una versione 3.x)
* **TeX Live** (per usare `xelatex`/`lualatex`) **oppure** **Tectonic**
* **typst** (se preferisci il CLI a `typst-py`)

---

## 8) Consigli per CI/Docker & riproducibilità

* **Tectonic** semplifica moltissimo la pipeline: nessuna installazione TeX Live pesante, pacchetti scaricati on-demand e **output deterministico**.
* **Cache**: conserva la cache pacchetti (Tectonic/TeX Live) per build più rapidi.
* **Font**: installa i font nelle immagini Docker e documenta **esattamente** i nomi.
* **Pin**: fissa versioni di template, pandoc e tool; aggiungi test di regressione (checksum del PDF o estrazione testo con `pdftotext` + diff).

---

## 9) Troubleshooting

* **Caratteri quadratini o mancanti**

  * Installa i font necessari (Noto CJK/Emoji).
  * Con XeLaTeX/LuaLaTeX imposta `mainfont`/`CJKmainfont` nel YAML o con `-V`.
* **Sillabazione/lingua errata**

  * Assicurati di impostare `lang` nel front matter e caricare **polyglossia/babel** nel template.
* **Errori LaTeX su tabelle/figure**

  * Semplifica la tabella o usa filtri Pandoc per generare ambienti dedicati.
* **Build lenta/variabile con TeX Live**

  * Prova **Tectonic** (`--pdf-engine=tectonic`).
* **Vuoi un setup più semplice**

  * Valuta **Typst**: meno dipendenze, compila velocemente, template moderni.

---

## 10) Glossario dei termini tecnici (chiari e concisi)

* **AST (Abstract Syntax Tree)**: rappresentazione strutturata del documento che Pandoc usa internamente per trasformare formati.
* **Template**: file (LaTeX/Typst) con segnaposto che Pandoc riempie usando i metadati del documento.
* **Metadati / YAML Front Matter**: blocco all’inizio del Markdown con chiavi/valori (titolo, autore, font, variabili).
* **fontspec**: pacchetto LaTeX (XeLaTeX/LuaLaTeX) per usare font di sistema in modo nativo.
* **polyglossia/babel**: pacchetti LaTeX per gestione lingue (sillabazione, convenzioni); polyglossia è più moderno con XeLaTeX.
* **CJK**: lingue Cinese-Giapponese-Coreano. Richiedono font dedicati e pacchetti specifici.
* **RTL**: “Right-To-Left”; direzione di scrittura per lingue come arabo/ebraico.
* **Tectonic bundle**: insieme coerente di pacchetti che garantiscono build riproducibili.
* **Typst**: linguaggio e motore per impaginazione moderna; sintassi dichiarativa, rendering veloce.
* **Riproducibilità**: proprietà per cui **stessa sorgente + stesso ambiente** → **stesso PDF**.

---

## 11) Riepilogo decisionale

* **Ecosistema LaTeX completo & tipografia fine** → **XeLaTeX/LuaLaTeX (TeX Live)**
* **CI, portabilità, build deterministici** → **Tectonic**
* **Semplicità, velocità, template moderni** → **Pandoc → Typst**

> Mantieni i **template separati dal contenuto**, cura i **font** (Noto/DejaVu + CJK/emoji), e aggiungi **test** in CI per evitare regressioni di layout.

---

## 12) Sviluppi Recenti e Nuove Funzionalità (v1.2)

### 12.1 Nuovi Script Implementati

Il sistema Pandoc è stato esteso con **5 script completi** che dimostrano funzionalità avanzate:

#### **p1_markdown_to_pdf.py** - Markdown to PDF Avanzato
- ✅ Conversione Markdown → PDF con motore XeLaTeX
- ✅ **Configurazione font avanzata** programmatica e via YAML
- ✅ Supporto Unicode completo (caratteri speciali, emoji)
- ✅ Layout professionale con TOC e numerazione sezioni

#### **p1_font_examples.py** - Esempi Configurazione Font
- ✅ Dimostrazione di diverse configurazioni font
- ✅ Font classici (Times, Helvetica, Courier)
- ✅ Font moderni (Georgia, Verdana, Consolas)
- ✅ Configurazione minima (fallback LaTeX)
- ✅ Font via YAML front matter

#### **p2_markdown_to_docx.py** - Markdown to DOCX
- ✅ Conversione Markdown → DOCX con styling
- ✅ TOC automatico e numerazione sezioni
- ✅ Syntax highlighting per codice

#### **p3_batch_conversion.py** - Conversione Batch Parallela
- ✅ Processamento multiplo di documenti
- ✅ Conversione simultanea in PDF, DOCX, HTML
- ✅ Report automatici di conversione
- ✅ Gestione errori robusta

#### **p4_combine_articles_to_pdf.py** - Combinazione Articoli
- ✅ Unione di articoli multipli in singolo PDF
- ✅ Parsing intelligente dei nomi file (YYYY-MM-DD - Titolo)
- ✅ Struttura automatica: Titolo → Sottotitolo data → Contenuto
- ✅ Page break tra articoli
- ✅ TOC generale del documento combinato

#### **p5_epub_to_pdf.py** - Conversione EPUB
- ✅ Conversione EPUB → PDF professionale
- ✅ Estrazione automatica immagini
- ✅ Layout ottimizzato con XeLaTeX
- ✅ Mantenimento struttura e formattazione

### 12.2 Miglioramenti Architetturali

#### **Sistema di Configurazione Font Avanzato**
```python
# Configurazione programmatica
config = PandocConfig.customize_fonts(
    mainfont="Times New Roman",
    sansfont="Arial",
    monofont="Courier New"
)

# O via YAML front matter
---
mainfont: "Times New Roman"
sansfont: "Arial"
fontsize: 12pt
---
```

#### **Gestione Errori Migliorata**
- ✅ Validazione dipendenze automatica
- ✅ Messaggi di errore informativi
- ✅ Fallback graceful per font mancanti
- ✅ Recupero da errori di conversione

#### **Automazione Completa**
- ✅ Script `tools/run_all.py` per esecuzione batch
- ✅ Generazione automatica di report
- ✅ Verifica integrità output
- ✅ Logging dettagliato delle operazioni

### 12.3 Integrazione Multi-Stack

Il Pandoc Stack ora si integra perfettamente con il sistema **multi-stack** completo:

- **DOCX Stack**: 4 esempi (docxtpl + templates manuali)
- **Chromium Stack**: 3 esempi (HTML → PDF con JavaScript)
- **Pandoc Stack**: 5 esempi (conversioni universali)
- **WeasyPrint Stack**: 3 esempi (PDF print-optimized)

**Totale: 15 esempi implementati** across 4 technology stacks.

### 12.4 Best Practices Aggiornate

#### **Per Font e Unicode**
- Usa **XeLaTeX** invece di pdflatex per supporto Unicode completo
- Preferisci famiglie **Noto** per copertura universale
- Configura font via YAML per documenti auto-contenuti

#### **Per Conversione Batch**
- Utilizza `tools/run_all.py` per test completi
- Monitora i report di conversione generati automaticamente
- Gestisci dipendenze esterne (Pandoc, XeLaTeX) appropriatamente

#### **Per Combinazione Documenti**
- Struttura nomi file: `YYYY-MM-DD - Titolo.md`
- Utilizza YAML front matter per metadati
- Verifica page break automatici tra sezioni

### 12.5 Troubleshooting Aggiornato

#### **Errori Font Comuni**
```
! Package fontspec Error: The font "NomeFont" cannot be found
```
**Soluzioni:**
- Verifica installazione font nel sistema
- Usa font di sistema comuni (Times, Helvetica, Courier)
- Configura `PandocConfig.create_minimal()` per fallback LaTeX

#### **Errori EPUB**
- Assicurati che Pandoc supporti il formato EPUB sorgente
- Verifica encoding UTF-8 dei file
- Controlla dipendenze XeLaTeX per caratteri speciali

#### **Errori Batch Processing**
- Verifica percorsi relativi corretti negli script
- Controlla permessi di scrittura nelle directory build
- Monitora log di errore per identificare file problematici

---

## 13) Roadmap e Futuri Sviluppi

### **Funzionalità Pianificate**
- Integrazione con **Typst** per rendering moderno
- Supporto **LuaLaTeX** avanzato con pacchetti custom
- **API REST** per conversione remota
- Integrazione **CI/CD** con GitHub Actions

### **Ottimizzazioni Previste**
- Conversione **parallela massiva** per grandi volumi
- **Caching intelligente** dei risultati di conversione
- **Validazione automatica** dell'output PDF
- **Metriche di performance** e benchmarking

### **Estensioni Possibili**
- Supporto **Markdown avanzato** (tabelle, note a piè pagina)
- **Template personalizzati** per settori specifici
- Integrazione con **database** per contenuti dinamici
- **API web** per generazione on-demand

---

*Questa guida è stata aggiornata per riflettere gli ultimi sviluppi del sistema Pandoc Stack. Per domande o contributi, consulta la documentazione principale del progetto.*
