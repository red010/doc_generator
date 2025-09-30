---

title: "DOCX avanzato: templating con docxtpl e composizione modulare con docxcompose"
description: "Architettura, vantaggi, quando scegliere lo stack, pitfalls e script Python completi per generare documenti DOCX (templating Jinja) e comporre/mergiare sezioni in reportistica modulare."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-09-30"
  version: "1.0"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["docx", "docxtpl", "docxcompose", "python-docx", "templating", "merging", "reportistica", "office"]

---

# DOCX – Operazioni avanzate e composizione (docxtpl + docxcompose)

> Obiettivo: creare **documenti Word editabili** partendo da **template DOCX** (Jinja) e **assemblare** più sezioni/moduli in **un unico fascicolo**, preservando **stili, header/footer e interruzioni**.

---

## 1) Componenti dello stack

* **`docxtpl` (python-docx-template)**
  Usa file **.docx** come **template Jinja**: sostituisce variabili, supporta cicli/condizionali e componenti avanzati (RichText, immagini). Internamente si appoggia a **`python-docx`** per leggere/scrivere DOCX. È la scelta naturale per generare *singoli modelli* con dati dinamici. ([docxtpl.readthedocs.io][1])

* **`python-docx`**
  API low-level per **creare/aggiornare DOCX**: paragrafi, run, tabelle, stili, proprietà documento, header/footer, page-break (a livello di *run*), ecc. Fondamentale per personalizzazioni e piccoli ritocchi “dopo il render”. ([python-docx.readthedocs.io][2])

* **`docxcompose`**
  Libreria specializzata per **append/concatenate** più **.docx** in **ordine** preservando **formattazioni**, **stili** e (tipicamente) header/footer. Espone la classe `Composer` per fare *merge* modulare in poche righe. ([GitHub][3])

---

## 2) Quando scegliere questo stack

Sceglilo quando:

* I **destinatari devono poter modificare in Word** (contratti, verbali, perizie, offerte).
* Devi produrre **report modulari**: capitoli generati separatamente (es. “Dati”, “Analisi”, “Allegati”) e poi **assemblati** in un unico fascicolo.
* Vuoi **separazione pulita** *template ↔ dati* + **riuso** dei moduli (stessa sezione in più report).
* Ti serve **coerenza visiva** (stili Word, header/footer) **preservata nel merge**. ([GitHub][3])

Evitalo quando:

* Vuoi solo PDF “di stampa” (senza editing Word) → considera **HTML→PDF** (WeasyPrint) o **Pandoc→(LaTeX/Typst)**.
* Richiedi controlli tipografici millimetrici o moduli PDF compilabili → conviene pipeline **PDF-native** (ReportLab/fpdf2).

---

## 3) Architettura e vantaggi

**Pattern consigliato**:

1. **Render dei moduli** con `docxtpl` (uno per capitolo) ⇒ ottieni N `.docx` coerenti. ([docxtpl.readthedocs.io][1])
2. **Composizione** con `docxcompose` nell’ordine desiderato ⇒ 1 documento finale. ([GitHub][3])
3. **Ritocchi** opzionali con `python-docx` (metadati, page-break extra, proprietà sezione). ([python-docx.readthedocs.io][2])

**Benefici**:

* **Manutenibilità**: i template sono file Word, curabili da non-sviluppatori. ([docxtpl.readthedocs.io][1])
* **Affidabilità nel merge**: `docxcompose` evita di “copiare paragrafo per paragrafo” e **preserva stili**/formati meglio di script manuali. ([Stack Overflow][4])
* **Scalabilità**: costruisci librerie di moduli riutilizzabili (legali, tecnici, marketing), componibili a runtime.

---

## 4) Requisiti (requirements.txt)

```txt
# templating
docxtpl>=0.16
jinja2>=3.1

# basso livello DOCX
python-docx>=1.2

# merge/append DOCX
docxcompose>=1.4
```

> Consiglio: **pinna** le versioni nel tuo progetto (lockfile) e crea test di regressione su un set di “golden docs”. ([python-docx.readthedocs.io][2])

---

## 5) Esempi completi

### 5.1 Templating base con `docxtpl` (variabili, loop, immagini)

**Template Word (`template.docx`)**
Crea il file **manualmente** in Word (non generarlo con `python-docx`!):

```text
Titolo: {{ title }}

{% for row in items %}
- {{ row.name }} — {{ row.qty }}
{% endfor %}

Testo formattato: {{r rich_content }}

Immagine: {{ image }}
```

#### ❌ SBAGLIATO - Non fare così

```python
# NON USARE python-docx per creare template con tag Jinja2!
from docx import Document
doc = Document()
doc.add_paragraph("Titolo: {{ title }}")  # Questo frammenta i tag!
doc.save("template.docx")  # Template non funzionerà con docxtpl
```

#### ✅ CORRETTO - Crea il template manualmente in Word

### Render Python

```python
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm

# Crea contenuto RichText
rt = RichText()
rt.add("Questo è ", italic=True)
rt.add("grassetto", bold=True)
rt.add(" e ")
rt.add("colorato", color="FF0000")

# Crea immagine inline
image = InlineImage(tpl, "product.png", width=Mm(60))

data = {
    "title": "Rapporto 2025",
    "items": [{"name": "Voce A", "qty": 2}, {"name": "Voce B", "qty": 5}],
    "rich_content": rt,  # RichText object
    "image": image,  # InlineImage object
}

tpl = DocxTemplate("template.docx")  # Template creato manualmente in Word
tpl.render(data)
tpl.save("modulo_intro.docx")
```

`docxtpl` processa Jinja dentro il `.docx` e salva un documento editabile in Word. ([docxtpl.readthedocs.io][1])

---

### 5.2 Composizione modulare con `docxcompose` (merge in ordine)

```python
from docx import Document
from docxcompose.composer import Composer

def merge_docs(output_path, *input_paths):
    master = Document(input_paths[0])
    composer = Composer(master)
    for part in input_paths[1:]:
        composer.append(Document(part))
    composer.save(output_path)

merge_docs(
    "Fascicolo_finale.docx",
    "modulo_intro.docx",
    "modulo_dati.docx",
    "modulo_analisi.docx",
    "modulo_allegati.docx",
)
```

`docxcompose` fa append preservando stili e struttura molto meglio di script manuali. ([GitHub][3])

---

### 5.3 Page break tra i moduli (con `python-docx`)

A volte vuoi **iniziare ogni modulo su pagina nuova**. Due approcci:

**A) Inserire il page break nell’output** (dopo ogni append)

```python
from docx import Document
from docxcompose.composer import Composer
from docx.enum.text import WD_BREAK

def merge_with_breaks(output_path, *input_paths):
    master = Document(input_paths[0])
    composer = Composer(master)
    for part in input_paths[1:]:
        # append modulo
        composer.append(Document(part))
        # aggiungi page break al termine
        p = master.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)
    master.save(output_path)

merge_with_breaks(
    "Fascicolo_breaks.docx",
    "modulo_intro.docx",
    "modulo_dati.docx",
    "modulo_analisi.docx",
)
```

`WD_BREAK.PAGE` inserisce un’interruzione **a livello di run**; è la via standard in `python-docx`. ([python-docx.readthedocs.io][5])

**B) Mettere l’interruzione nel **modulo** stesso**
Se ogni modulo **inizia con “Sezione successiva / Pagina nuova”** (break di Word), il merge risulta già segmentato. (Ricorda: i **section break** sono entità diverse dai page break e non si inseriscono arbitrariamente via API in mezzo al documento.) ([python-docx.readthedocs.io][6])

---

### 5.4 Pipeline “render moduli con docxtpl → merge con docxcompose” (completa)

```python
from pathlib import Path
from docxtpl import DocxTemplate
from docx import Document
from docxcompose.composer import Composer

TMP = Path("build")
TMP.mkdir(exist_ok=True)

# 1) RENDER dei moduli
def render_module(template_path, context, out_path):
    tpl = DocxTemplate(template_path)
    tpl.render(context)
    tpl.save(out_path)

render_module("tpl_intro.docx", {"title": "Report X"}, TMP/"1_intro.docx")
render_module("tpl_dati.docx", {"rows": [{"k":"A","v":10},{"k":"B","v":20}]}, TMP/"2_dati.docx")
render_module("tpl_analisi.docx", {"score": 87}, TMP/"3_analisi.docx")

# 2) MERGE
master = Document(TMP/"1_intro.docx")
composer = Composer(master)
composer.append(Document(TMP/"2_dati.docx"))
composer.append(Document(TMP/"3_analisi.docx"))
composer.save("Report_finale.docx")
```

Questo è il **pattern di produzione** più comune per reportistica modulare. ([docxtpl.readthedocs.io][1])

---

### 5.5 Ritocchi finali: proprietà, header/footer, layout (quick wins)

```python
from docx import Document

doc = Document("Report_finale.docx")
# Proprietà "core"
props = doc.core_properties
props.author = "Ufficio Studi"
props.title = "Report finale 2025"
props.subject = "Analisi trimestrale"

# Accesso a sezione corrente (margini, orientamento, header/footer)
section = doc.sections[0]
section.header.is_linked_to_previous = False
section.footer.is_linked_to_previous = False

doc.save("Report_finale_meta.docx")
```

`python-docx` espone **core properties** e sezioni (margini, header/footer). ([python-docx.readthedocs.io][7])

---

## 6) Linee guida per template & composizione

### 6.1 Template Creation Best Practices

* **🔴 Mai generare template programmaticamente**: **NON** usare `python-docx` per creare template con tag Jinja2. Anche usando `add_run()` per "forzare" singoli runs, Word frammenta inevitabilmente i tag in multiple runs XML, rendendoli invisibili a `docxtpl`.

* **✅ Crea template manualmente**: Usa sempre Microsoft Word o LibreOffice per creare template. Inserisci direttamente i tag Jinja2 (es. `{{ variable }}`, `{% for item in list %}`) nel testo - questo garantisce che ogni tag esista in un singolo run XML continuo.

* **Tag Jinja2 supportati**:
  * `{{ variable }}` - variabili semplici
  * `{% for item in list %}{{ item }}{% endfor %}` - loop su liste
  * `{%p for item in list %}{{ item }}{%p endfor %}` - loop paragrafo
  * `{%tr for row in table %}{{ row.field }}{%tr endfor %}` - loop righe tabella

* **Stili Word**: definisci *Titolo 1/2/…*, Corpo, Elenchi; evita formattazioni "a mano". I moduli con stili coerenti **si fondono meglio**.

* **Breaks**: usa **Page Break** o **Section Break (Next Page)** per forzare nuovi capitoli; ricorda la distinzione **page vs section**. ([python-docx.readthedocs.io][6])

* **Header/Footer**: decidi **chi domina** (master o modulo). Talvolta conviene usare un **master** con header/footer "ufficiali" e moduli senza.

* **Immagini & tabelle**: prediligi **stili tabella** consistenti; evita elementi fluttuanti complessi tra moduli.

* **Subdocumenti `docxtpl`**: utili, ma con formattazioni complesse possono comparire edge case (stili persi). Valuta `docxcompose` per merge robusto. ([GitHub][8])

* **Test di regressione**: mantieni *golden docs* e verifica pagine, heading, TOC, numerazione.

---

## 7) Pitfall & soluzioni

* **🔴 Template programmatici falliscono con `docxtpl`** → **NON** generare template DOCX con `python-docx` contenenti tag Jinja2. La generazione programmatica causa **frammentazione XML** dei tag in multiple "runs", rendendoli invisibili a `docxtpl`. **Soluzione**: crea sempre template **manualmente** con Word/LibreOffice per garantire che i tag Jinja2 esistano in singoli runs XML continui.
* **🔴 RichText richiede sintassi speciale** → Per **RichText objects**, usa **`{{r variable }}`** invece di `{{ variable }}`. La sintassi `{{r }}` è necessaria perché docxtpl tratta RichText in modo diverso per preservare la formattazione.
* **Page break non dove previsto** → inserisci `WD_BREAK.PAGE` **dopo** l’`append` o struttura i moduli con *section/page break* all’inizio. ([Stack Overflow][9])
* **Sezioni/Orientamento misti** (portrait/landscape) → gestisci **section breaks** nei moduli (python-docx **non** inserisce section break in mezzo al documento via API). ([Stack Overflow][10])
* **Stili confliggenti** tra moduli → unifica i nomi stile nei template; se necessario, usa un **master** che “impone” stili globali.
* **Formattazioni perse con subdoc** → preferisci `docxcompose` per inglobare documenti “ricchi”. ([GitHub][8])

---

## 8) Struttura di progetto consigliata

```text
project/
  templates/
    tpl_intro.docx
    tpl_dati.docx
    tpl_analisi.docx
  src/
    render_modules.py
    merge_docs.py
  build/
    (output temporanei .docx dei moduli)
  requirements.txt
  README.md
```

---

## 9) Conclusioni

Per **report Word modulari** l’accoppiata **docxtpl → docxcompose** è una soluzione **matura e manutenuta**, ma richiede **disciplina assoluta** nella creazione dei template:

* **🔴 Regola fondamentale**: Crea sempre template **manualmente** con Word/LibreOffice. **Mai** generare template programmaticamente con `python-docx` - causa frammentazione XML irreversibile dei tag Jinja2.

* *docxtpl* per generare moduli da template Jinja con dati dinamici (template creati **manualmente**);
* *docxcompose* per **comporre** in un unico documento preservando **formati e stili**;
* *python-docx* per i **ritocchi finali** (metadati, page break, header/footer).

Con template ben progettati **(manualmente)**, test di regressione e versionamento, ottieni pipeline solide, ripetibili e friendly per chi dovrà **continuare a lavorare in Word**. ([docxtpl.readthedocs.io][1])

**Ricorda**: se i campi sono vuoti nel documento finale, il 99% delle volte è perché il template è stato generato programmaticamente invece che creato manualmente.

[1]: https://docxtpl.readthedocs.io/?utm_source=chatgpt.com "Welcome to python-docx-template's documentation! — python ..."
[2]: https://python-docx.readthedocs.io/?utm_source=chatgpt.com "python-docx — python-docx 1.2.0 documentation - Read the ..."
[3]: https://github.com/4teamwork/docxcompose?utm_source=chatgpt.com "4teamwork/docxcompose: Append/Concatenate .docx ..."
[4]: https://stackoverflow.com/questions/24872527/combine-word-document-using-python-docx?utm_source=chatgpt.com "combine word document using python docx"
[5]: https://python-docx.readthedocs.io/en/latest/api/text.html?utm_source=chatgpt.com "Text-related objects — python-docx 1.2.0 documentation"
[6]: https://python-docx.readthedocs.io/en/latest/dev/analysis/features/sections.html?utm_source=chatgpt.com "Sections — python-docx 1.2.0 documentation - Read the Docs"
[7]: https://python-docx.readthedocs.io/en/latest/api/document.html?utm_source=chatgpt.com "Document objects - python-docx - Read the Docs"
[8]: https://github.com/elapouya/python-docx-template/issues/388?utm_source=chatgpt.com "Formatting lost when using subdoc() · Issue #388"
[9]: https://stackoverflow.com/questions/48654715/page-break-via-python-docx-in-ms-word-docx-file-appears-only-at-the-end?utm_source=chatgpt.com "Page break via python-docx in MS Word docx file appears ..."
[10]: https://stackoverflow.com/questions/68093852/how-to-add-a-sectional-break-in-word-using-python-docx?utm_source=chatgpt.com "How to add a Sectional Break in word using python-docx"
