---

title: "Guida pratica 2025 alla generazione programmatica di documenti"
description: "Stack, workflow e best practice per creare DOCX e PDF (HTML/CSS/JS → PDF, canvas → PDF, Markdown → PDF via Pandoc/LaTeX/Typst), con accessibilità, firme digitali, test e deploy."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-09-29"
  version: "2.0"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["docx", "pdf", "weasyprint", "playwright", "reportlab", "fpdf2", "pandoc", "tectonic", "typst", "pypdf", "pikepdf", "pyhanko", "docxtpl", "docxcompose", "a11y", "pdf/ua", "pdf/a"]

---

# Guida pratica 2025 alla generazione programmatica di documenti

> Obiettivo: fornire scelte “pronte per la produzione”, con esempi minimi e checklist, per generare **DOCX** e **PDF** in modo riproducibile, accessibile e manutenibile.

---

## 0) Mappa rapida degli scenari

* **DOCX (Office-editabile)**

  * *Templating con campi Jinja*: **`docxtpl`**
  * *Manipolazione a basso livello*: **`python-docx`**
  * *Merge/append di documenti*: **`docxcompose`**
  * *Alternative commerciali*: Aspose/Spire (valuta licenze/costi)

* **PDF (tre vie principali)**

  1. **HTML/CSS → PDF**

     * **WeasyPrint**: fedeltà CSS di stampa, ottimo per report statici/semantici
     * **Chromium headless (Playwright)**: quando serve **rendering JS** (grafici interattivi, mappe, componenti web)
  2. **Canvas → PDF (senza HTML)**

     * **ReportLab** (ricco, include **AcroForm**), **fpdf2** (leggero e pythonico)
  3. **Markdown → PDF**

     * **Pandoc → LaTeX** (consigliato con **Tectonic** per build riproducibili)
     * **Pandoc → Typst** (tipografia moderna, pipeline snella)

* **Post-processing PDF**: **`pypdf`** / **`pikepdf`** (merge/split/metadata)

* **Firme digitali (PAdES)**: **`pyHanko`**

* **Accessibilità e conservazione**: **PDF/UA**, **PDF/A** (struttura semantica + variant del motore PDF)

---

## 1) Quando scegliere cosa (Decision tree)

1. **Il destinatario deve modificare il file in Word?**
   → **DOCX** con `docxtpl`.
   Se devi comporre fascicoli modulari: aggiungi `docxcompose`.

2. **Serve un PDF “pubblicazione” da HTML/CSS?**

   * Pagina statica, semantica, CSS di stampa → **WeasyPrint**
   * Necessario eseguire JS (grafici client-side, componenti React/Vue già idratati) → **Playwright (Chromium)**

3. **Serve controllo millimetrico di layout, disegni, moduli compilabili?**
   → **ReportLab** (form, canvas ricco) o **fpdf2** (snello, ottimo per tabelle/etichette).

4. **Parti da Markdown e vuoi pipeline testabile, riproducibile, tipografia “editoriale”?**
   → **Pandoc**:

   * **→ LaTeX con Tectonic** per riproducibilità
   * **→ Typst** se vuoi velocità e template moderni

---

## 2) Tabella di confronto (Decision matrix)

| Esigenza / Stack              |    WeasyPrint (HTML/CSS) |           Playwright (Chromium) |     ReportLab |    fpdf2 |            Pandoc→LaTeX (Tectonic) |    Pandoc→Typst |
| ----------------------------- | -----------------------: | ------------------------------: | ------------: | -------: | ---------------------------------: | --------------: |
| Fedeltà CSS di stampa         |                 **Alta** |                  Alta (browser) |           N/A |      N/A |         Media (via template LaTeX) |      Media-alta |
| Supporto JS                   |                       No |                          **Sì** |           N/A |      N/A |                                 No |              No |
| A11y (PDF/UA)                 |               **Buona*** | Buona (dipende da HTML taggato) |       Manuale |  Manuale | Buona (con pacchetti LaTeX e cura) |     In crescita |
| Moduli compilabili (AcroForm) |                       No |                              No |        **Sì** | Parziale |                                 No |              No |
| Tipografia editoriale         |                    Buona |                           Buona |       Manuale |  Manuale |                     **Eccellente** | **Molto buona** |
| Curva di apprendimento        |                    Bassa |                           Media |         Media |    Bassa |                              Media |           Media |
| Dipendenze di sistema         |              Cairo/Pango |                         Browser | Nessuna extra |  Nessuna |              TeX engine (Tectonic) |           Typst |
| Performance batch server      |                   Ottima |                 Media (browser) |        Ottima |   Ottima |                              Media |          Ottima |
| Requisiti dati dinamici       | Ottimo (templating HTML) |                Ottimo (app web) |         Buono |    Buono |        Ottimo (markdown/templates) |          Ottimo |

* PDF/UA/PDF/A: richiede HTML semantico e configurazione del motore; vedi § Accessibilità.

---

## 3) Best practice trasversali

### 3.1 Separazione **template ↔ dati**

* Mantieni i **template** (DOCX/HTML/LaTeX/Typst) versionati a parte.
* Serializza i **dati** in JSON/YAML; usa schemi (pydantic) per validare.
* Predisponi **preflight checks**: dati completi, risorse esistono (font/immagini), variabili non nulle.

### 3.2 Font, localizzazione e script complessi

* Scegli **famiglie Noto** (Sans/Serif/Mono + CJK + emoji) per copertura multilingue.
* Pre-embed dei font e definisci fallback; abilita hyphenation della lingua.
* RTL/CJK: preferisci **XeLaTeX/LuaLaTeX** in Pandoc o font completi in HTML/CSS.

### 3.3 Sicurezza

* Sanifica HTML se proviene da input esterni.
* Browser headless: isola in container, disabilita rete/file scheme, usa timeouts e quote.

### 3.4 Test e qualità

* **Visual regression**: rasterizza i PDF e fai diff (Ghostscript/ImageMagick o `diff-pdf`).
* **Test semantici**: controlla outline, segnalibri, metadata XMP, numero pagine, presenza/ordine capitoli (con `pypdf`/`pikepdf`).
* Genera **snapshot goldens** per i template principali.

### 3.5 Performance & scalabilità

* Reusa istanze Playwright; usa code/queue per batch.
* Cache di font, immagini e partials Jinja.
* Parallelizza composizioni indipendenti; fondi output in coda con `pypdf`.

### 3.6 Deploy & riproducibilità

* **WeasyPrint**: richiede **Cairo + Pango + GDK-PixBuf** (vedi Docker più sotto).
* **Tectonic** scarica i pacchetti TeX on-demand e rende i build riproducibili.
* Pin delle dipendenze (`requirements.txt` / `pyproject.toml` + lock).
* CI: step di build + test + diff visivo + artefatti.

---

## 4) Ricette (snippet minimi)

> Gli snippet sono volutamente concisi; estendili con gestione errori e logging.

### 4.1 DOCX – Templating con `docxtpl`

```python
from docxtpl import DocxTemplate
data = {
    "title": "Rapporto 2025",
    "items": [{"name": "Voce A", "qty": 2}, {"name": "Voce B", "qty": 5}],
}
tpl = DocxTemplate("template.docx")  # contiene {{ title }} e un {% for item in items %}...
tpl.render(data)
tpl.save("output.docx")
```

**Consigli**

* Nei template, usa **stili Word** corretti (Titolo 1/2, elenchi) per coerenza.
* Per immagini dinamiche, usa `InlineImage` di `docxtpl`.

### 4.2 DOCX – Merge con `docxcompose`

```python
from docx import Document
from docxcompose.composer import Composer

result = Document("capitolo_1.docx")
composer = Composer(result)

for path in ["capitolo_2.docx", "capitolo_3.docx"]:
    composer.append(Document(path))

composer.save("fascicolo.docx")
```

> Ottimo per fascicoli modulari, allegati, contratti a blocchi.

---

### 4.3 HTML/CSS → PDF con **WeasyPrint**

**HTML (Jinja)**

```html
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <style>
    @page { size: A4; margin: 20mm; }
    h1 { page-break-after: avoid; }
    .page-break { page-break-before: always; }
  </style>
</head>
<body>
  <h1>{{ title }}</h1>
  <ul>
    {% for row in items %}
      <li>{{ row.name }} — {{ row.qty }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

**Render Python**

```python
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

env = Environment(loader=FileSystemLoader("."))
tpl = env.get_template("report.html")
html = tpl.render(title="Rapporto 2025", items=[{"name":"A","qty":1}])

HTML(string=html, base_url=".").write_pdf("report.pdf")  # base_url per risorse relative
```

**Note**

* Installa a livello OS: **cairo, pango, gdk-pixbuf** e font necessari.
* Per varianti **PDF/A** o **PDF/UA**, usa le opzioni del motore e un HTML semantico (landmarks, table headers, alt text).

---

### 4.4 HTML/JS → PDF con **Playwright (Chromium)**

```python
from playwright.sync_api import sync_playwright

html = """
<!doctype html><html><head>
  <meta charset="utf-8">
  <style>@page{size:A4;margin:20mm}</style>
</head><body>
  <div id="app"></div>
  <script>
    document.getElementById('app').innerText = 'Grafico renderizzato via JS...';
    // qui potresti istanziare chart.js / eCharts, ecc.
  </script>
</body></html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html, wait_until="load")  # 'networkidle' se carichi risorse esterne
    page.pdf(path="report_js.pdf", format="A4", print_background=True)
    browser.close()
```

**Tip**

* Riutilizza browser e page per batch; disabilita rete se non serve.
* Cura l’**HTML semantico** per migliorare accessibilità del PDF risultante.

---

### 4.5 Canvas → PDF con **fpdf2** (snello)

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=16)
pdf.cell(0, 10, "Titolo", ln=1)
pdf.set_font("Helvetica", size=12)
for i in range(1, 6):
    pdf.cell(0, 8, f"Riga {i}", ln=1)
pdf.output("fpdf2_simple.pdf")
```

**Uso ideale**: fatture, etichette, documenti strutturati ripetitivi.

---

### 4.6 Canvas → PDF con **ReportLab** + **AcroForm**

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("reportlab_form.pdf", pagesize=A4)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 800, "Modulo di esempio")

# Campo di testo (AcroForm)
c.acroForm.textfield(
    name="nome", tooltip="Nome",
    x=50, y=760, width=200, height=18,
    borderStyle="inset", borderColor=None, fillColor=None
)

c.showPage()
c.save()
```

**Uso ideale**: moduli compilabili, timbri, grafica vettoriale precisa.

---

### 4.7 Markdown → PDF con **Pandoc → LaTeX (Tectonic)**

**file.md**

```markdown
---
title: "Rapporto 2025"
author: "Team"
lang: it
geometry: margin=2.0cm
---

# Introduzione

Testo *Markdown* con tabelle, figure e riferimenti.
```

**Build (CLI)**

```bash
# Assumi che 'pandoc' e 'tectonic' siano installati
pandoc file.md -o out.pdf --pdf-engine=tectonic
```

**Note**

* Per font e lingua, usa template LaTeX con `xelatex`/`lualatex` se preferisci (in alternativa a Tectonic).
* Ottimo per documentazione e white paper con bibliografie.

---

### 4.8 Markdown → PDF con **Pandoc → Typst**

**file.md**

```markdown
---
title: "Rapporto 2025"
author: "Team"
lang: it
---

# Introduzione

Contenuto Markdown → Typst tramite Pandoc.
```

**Build (CLI)**

```bash
# Richiede pandoc con writer Typst e il binario 'typst'
pandoc file.md -t typst -o out.typ
typst compile out.typ out.pdf
```

**Perché Typst**

* Sintassi moderna, template puliti, build veloci.
* Ecosistema in crescita (ottimo per tesi, report, schede prodotto).

---

### 4.9 Post-processing PDF con **pypdf/pikepdf**

```python
from pypdf import PdfReader, PdfWriter

merger = PdfWriter()
for src in ["cap1.pdf", "cap2.pdf", "allegato.pdf"]:
    merger.append(PdfReader(src))
merger.add_metadata({"/Title": "Fascicolo 2025"})
with open("fascicolo.pdf", "wb") as f:
    merger.write(f)
```

> Usa `pikepdf` se ti servono operazioni approfondite sugli oggetti PDF (basato su QPDF).

---

### 4.10 Firma digitale (PAdES) con **pyHanko** (minimo illustrativo)

```bash
# Esempio a riga di comando (chiave e certificato già disponibili)
pyhanko sign addsig --field Sig1 --timestamp-url http://tsa.example.org \
  --signer-key signer.key --signer-cert chain.pem \
  input.pdf output_signed.pdf
```

> Integrazione Python e profili avanzati (LTV/OCSP/CRL) sono disponibili; valuta HSM se necessario.

---

## 5) Accessibilità e conformità (PDF/UA, PDF/A)

* **Progetta i template con semantica**: titoli (h1..h6), liste, tabelle con `thead`/`scope`, alternative testuali immagini, landmarks (banner/main/contentinfo).
* **Contrasto e colori**: rispetta WCAG; evita informazione solo cromatica.
* **Ordine di lettura**: evitare layout “spezzati”; usa page-break coerenti.
* **Varianti PDF**:

  * **PDF/UA**: documento taggato e fruibile da tecnologie assistive.
  * **PDF/A**: per archiviazione a lungo termine (embedding font, profili colore).
* **Testing**: screen reader + validatori (es. PAC), controllo manuale di heading/alt text.

> Nota: il supporto alla generazione **PDF/UA** è in crescita in più motori (WeasyPrint, LaTeX, ecc.). La qualità finale dipende moltissimo dal **template**.

---

## 6) Docker & deploy (snippet)

### 6.1 WeasyPrint in container

```dockerfile
FROM python:3.12-slim

# deps di sistema per WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
    fonts-dejavu fonts-noto-core fonts-noto-cjk fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml poetry.lock* requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt  # oppure poetry/pdm/uv

COPY . .
CMD ["python", "main.py"]
```

### 6.2 Playwright (Chromium) in container

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir playwright && playwright install chromium
# opzionale: --with-deps per installare dipendenze sistema dell’engine
```

### 6.3 Pandoc + Tectonic

* Installa `pandoc` (pacchetto di sistema) e `tectonic` (binario).
* In CI, cache dei pacchetti TeX scaricati da Tectonic per build più rapidi.

---

## 7) Pitfall comuni (e soluzioni)

* **Font mancanti/garbled text** → Embedding esplicito, dichiarazione `@font-face`, usa famiglie Noto complete.
* **Page break imprevisti in HTML→PDF** → Imposta `@page`, evita margini “strani”, usa classi `.page-break`.
* **Liste/elenchi DOCX non coerenti** → Definisci stili Word corretti; in casi difficili, compila elenchi come blocchi separati.
* **Browser headless lento** → Riutilizza il browser, limita risorse remote, pre-render server-side se possibile.
* **PDF accessibile incompleto** → Migliora semantica sorgente, rivedi ordine DOM, verifica con validatori.
* **Merge PDF “corrotto”** → Usa `pikepdf`/`pypdf` aggiornati; normalizza metadata; evita input con protezioni.
* **Immagini pesanti** → Pre-ridimensiona/comprimi; preferisci SVG per vettoriale in HTML; controlla DPI in ReportLab.

---

## 8) Checklist “pronta per prod”

* [ ] Scelto lo **stack** secondo il decision tree.
* [ ] Template separati dai dati + validazione schema.
* [ ] **Font** predisposti (fallback CJK/emoji) e incorporati.
* [ ] **A11y**: struttura semantica, alt text, contrasto, ordine lettura.
* [ ] **PDF variant** richiesta (PDF/A, PDF/UA) definita e testata.
* [ ] **Firme**: profilo PAdES, TSA/OCSP/CRL, eventuale HSM.
* [ ] **Test**: visual regression + test semantici automatizzati.
* [ ] **CI/CD**: container con dipendenze OS, caching, artefatti.
* [ ] **Sicurezza**: sandbox, timeouts, input sanitization.
* [ ] **Osservabilità**: logging strutturato, trace dei template usati, audit trail.

---

## 9) Pacchetti suggeriti (Python)

```text
# Core
docxtpl
python-docx
docxcompose

weasyprint
jinja2

playwright  # (python)  -> ricordarsi 'playwright install chromium'
# oppure: pyppeteer (alternativa più leggera, meno completa)

reportlab
fpdf2

pandocfilters  # se fai estensioni; in genere invii comandi a 'pandoc' CLI
# per riproducibilità LaTeX: tectonic (binario)
# per Typst: typst (binario)

pypdf
pikepdf

pyhanko
```

> Gestione pacchetti: `uv`/`pdm`/`poetry` o `pip+venv`/`conda`. Preferisci lockfile, build riproducibili e immagini Docker minimali.

---

## 10) Glossario essenziale

* **PDF/UA**: standard per accessibilità PDF (tagging, ordine di lettura, alternative testuali).
* **PDF/A**: profilo per archiviazione a lungo termine (embedding font, colori, no elementi dinamici).
* **PAdES**: firma digitale avanzata per PDF (ETSI), estendibile con timestamp/OCSP/CRL.
* **AcroForm**: modulo compilabile dentro un PDF (campi testo, checkbox, radio, combo).
* **Tectonic**: motore LaTeX “zero-config” con caching pacchetti per build riproducibili.
* **Typst**: linguaggio e motore di composizione moderno, alternativo a LaTeX.

---

## 11) Modello di progetto (cartella tipo)

```text
project/
  templates/
    docx/
      contract.docx
    html/
      report.html
    latex/
      template.tex
    typst/
      layout.typ
  data/
    samples/
      report_001.json
  src/
    generate_docx.py
    generate_pdf_html.py
    generate_pdf_canvas.py
    generate_pdf_pandoc.py
    postprocess_pdf.py
  tests/
    visual/
      goldens/
  fonts/
    NotoSans-Regular.ttf
    NotoSansCJK-Regular.otf
  Dockerfile
  pyproject.toml
  README.md
```

---

## 12) Esempi di comandi utili (varie)

```bash
# Diff visivo tra due PDF (raster)
# (richiede utilità esterne: 'diff-pdf' o pipeline Ghostscript/ImageMagick)
diff-pdf --output-diff=out.png old.pdf new.pdf

# Estrarre testo per assert semantici
pdftotext in.pdf out.txt

# Contare pagine via pypdf (python -c)
python -c "from pypdf import PdfReader; print(len(PdfReader('in.pdf').pages))"
```

---

## 13) Licenze & note legali

* Verifica le **licenze** dei font (es. Noto → SIL OFL per molti set) e dei pacchetti usati.
* Per **firme digitali** con certificati qualificati, rispetta eIDAS e policy dell’ente.
* Per **dati personali** nei PDF, applica minimizzazione e policy privacy (GDPR).

---

### Conclusione

Questa guida ti permette di scegliere rapidamente lo **stack** giusto (DOCX, HTML→PDF, Canvas, Markdown→PDF) e di metterlo in produzione con **accessibilità**, **firme**, **test** e **deploy** solidi. Parti dai **template** e dalla **semantica**, aggiungi i motori adatti (WeasyPrint/Chromium, ReportLab/fpdf2, Pandoc→Tectonic/Typst) e integra post-processing (`pypdf`/`pikepdf`) e firma (`pyHanko`) quando richiesto.
