---

title: "WeasyPrint avanzato: dipendenze di sistema, deployment (Ubuntu/macOS/Docker), font fallback e hyphenation"
description: "Come mettere in produzione WeasyPrint nel 2025 senza sorprese: ruolo di Pango/pydyf, stato (post-Cairo), cosa installare su Ubuntu e macOS, Dockerfile di riferimento, gestione font (CJK/RTL/emoji), hyphenation e script Python completi."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-09-29"
  version: "1.0"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["weasyprint", "html-to-pdf", "pango", "harfbuzz", "pydyf", "docker", "ubuntu", "macOS", "fonts", "CJK", "RTL", "emoji", "hyphenation"]

---

# WeasyPrint: guida avanzata a dipendenze & deployment

> **Messaggio chiave**: le versioni moderne di **WeasyPrint (≥53)** **non dipendono più da Cairo/GDK-Pixbuf** per generare PDF: il backend è **pydyf**; l’unica dipendenza nativa fondamentale rimane **Pango** (con HarfBuzz) per layout e shaping del testo. Le immagini sono gestite via **Pillow**. Questo cambia radicalmente i prerequisiti di OS/CI rispetto alle guide storiche. ([courtbouillon.org][1])

---

## 1) Componenti dello stack (oggi)

* **WeasyPrint (core)**
  Motore **HTML/CSS → PDF** con layout da stampa; espone CLI e API Python (`HTML(...).write_pdf(...)`). Dalla 53 in poi usa **pydyf** come generatore PDF. ([doc.courtbouillon.org][2])

* **Pango (+ HarfBuzz)**
  Libreria di **impaginazione e rendering del testo** con enfasi su internazionalizzazione (shaping complesso, script CJK, marcatura bidi per RTL). È **il** prerequisito di sistema primario per WeasyPrint moderno. ([The GTK Team][3])

* **pydyf**
  Generatore PDF **low-level** in Python creato dal team WeasyPrint per rimpiazzare Cairo; rimuove una grossa dipendenza C e rende i deploy più semplici. ([courtbouillon.org][1])

* **Pillow / fontTools / Pyphen**
  Immagini (JPEG/PNG/WebP/OpenJPEG) via Pillow; gestione font e subset via fontTools; **hyphenation** tramite Pyphen (serve `lang` + `hyphens: auto`). ([doc.courtbouillon.org][4])

> Nota storica: fino alla 52.x WeasyPrint richiedeva **Cairo** (disegno 2D, includendo backend PDF) e spesso **GDK-Pixbuf** per immagini. Oggi **non più**: pydyf ha sostituito Cairo; le immagini passano da Pillow. ([courtbouillon.org][1])

---

## 2) Quando scegliere WeasyPrint (vs. un browser headless)

**Scegli WeasyPrint se…**

* il tuo layout è **HTML+CSS di stampa** (paginazione, `@page`, margini, header/footer CSS) **senza JS da eseguire**;
* vuoi un **runtime leggero** (niente Chromium) e deploy lineare in **CI/Docker**;
* hai documenti testuali lunghi (report, fatture, bollettini) dove contano hyphenation, giustificazione e la resa tipografica di Pango. ([doc.courtbouillon.org][4])

**Meglio Chromium headless se…** devi “**fotografare**” UI/grafici **generati da JS** prima dello snapshot (Chart.js, mappe, componenti web).

---

## 3) Dipendenze di sistema aggiornate (2025)

### 3.1 Riepilogo “moderno”

* **Obbligatorie**: **Pango** recente (≥1.44 secondo docs), runtime Python 3.9+, e librerie Python (pydyf, tinyhtml5, tinycss2, cssselect2, Pillow, fontTools, Pyphen). ([doc.courtbouillon.org][4])
* **Non più richieste**: **Cairo** e **GDK-Pixbuf** per PDF. (Attenzione a guide legacy e a problemi in ambienti che impongono versioni vecchie.) ([courtbouillon.org][1])

### 3.2 Ubuntu / Debian (server & CI)

Verifica versioni:

```bash
python3 --version
pango-view --version
```

Installazione minima (Ubuntu ≥ 20.04) **con wheels**:

```bash
sudo apt update
sudo apt install -y python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0
python3 -m venv venv && source venv/bin/activate
pip install weasyprint
weasyprint --info
```

Se **senza wheels** (build locale di alcune dipendenze Python):

```bash
sudo apt install -y libffi-dev libjpeg-dev libopenjp2-7-dev
```

(Nelle distro recenti è disponibile anche `apt install weasyprint`.) ([doc.courtbouillon.org][4])

> Ambiente con **Pango troppo vecchio**? La doc raccomanda di usare **WeasyPrint 52.5** (ancora compatibile con Pango datato), ma è una soluzione di **retro-compatibilità**. ([doc.courtbouillon.org][4])

### 3.3 macOS

La via più semplice per CLI:

```bash
brew install weasyprint
```

Per uso **Python** in venv:

```bash
python3 -m venv venv && source venv/bin/activate
pip install weasyprint
weasyprint --info
```

Se macOS **non trova le librerie** (raro ma possibile), imposta:

```bash
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH
```

([doc.courtbouillon.org][4])

### 3.4 Docker (Debian/Ubuntu slim)

Esempio **Dockerfile** minimal con font Noto inclusi:

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libharfbuzz-subset0 \
    fonts-noto fonts-noto-cjk fonts-noto-color-emoji \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt && weasyprint --info

COPY . .
CMD ["python", "main.py"]
```

I pacchetti Pango/Harfbuzz elencati sono quelli raccomandati nelle istruzioni per Ubuntu/Debian; includere i **font Noto** evita fallback “a quadratini” e dà copertura CJK/emoji in CI. ([doc.courtbouillon.org][4])

---

## 4) Font fallback, CJK/RTL, emoji & hyphenation

### 4.1 Regole generali

* WeasyPrint usa i **font visti da Pango** (di sistema o dichiarati via `@font-face`) e li **incorpora automaticamente nel PDF**. ([doc.courtbouillon.org][5])
* Per evitare glyph mancanti: installa famiglie **Noto** (`fonts-noto`, `fonts-noto-cjk`, `fonts-noto-color-emoji`) o dichiara esplicitamente `@font-face` con font inclusi nel progetto. ([doc.courtbouillon.org][4])
* Per **risorse relative** (immagini, CSS, font) passate come stringa, ricordati `base_url=...`. ([doc.courtbouillon.org][6])

### 4.2 Hyphenation (a capo sillabico)

Abilita con CSS e lingua del documento:

```html
<html lang="it">
<style>
  html { hyphens: auto; }
</style>
```

WeasyPrint usa **Pyphen** e l’attributo `lang` per caricare i pattern corretti; puoi disattivare con `hyphens: manual`. ([doc.courtbouillon.org][7])

### 4.3 CJK

Per cinese/giapponese/coreano, tipicamente non si usa hyphenation ma le regole di line-breaking. Lato font, installa **Noto Sans CJK** e definisci uno stack che copra i set richiesti. (Pango gestisce shaping e line breaking per script CJK.) ([The GTK Team][3])

### 4.4 RTL (arabo/ebraico)

WeasyPrint si appoggia a Pango per bidi e shaping; il supporto RTL è **in miglioramento** (fix recenti su giustificazione e selezione testo), ma permangono **casi edge**. Imposta `lang`/`dir="rtl"` e **verifica** i casi complessi. ([doc.courtbouillon.org][8])

### 4.5 Emoji

Installa **Noto Color Emoji** o dichiara un font emoji via `@font-face`. Sono stati corretti problemi con versioni Pango più vecchie; in CI usa Pango aggiornato. ([doc.courtbouillon.org][8])

---

## 5) Esempi Python completi

### 5.1 HTML string → PDF con font incorporati e hyphenation

```python
from pathlib import Path
from weasyprint import HTML, CSS

BASE = Path(__file__).parent

HTML_STRING = """
<!doctype html><html lang="it"><meta charset="utf-8">
<style>
  @font-face {
    font-family: "NotoSerif";
    src: url("assets/fonts/NotoSerif-Regular.ttf") format("truetype");
  }
  body { font-family: "NotoSerif", serif; line-height: 1.35; }
  html { hyphens: auto; } /* abilita hyphenation quando lang è presente */
  h1 { margin: 0 0 8pt 0; }
</style>
<body>
  <h1>WeasyPrint demo</h1>
  <p>Questo paragrafo dimostra la sillabazione automatica su parole molto-lunghe
  e la corretta incorporazione del font specificato via @font-face.</p>
</body></html>
"""

def render_pdf(out="out.pdf"):
    HTML(string=HTML_STRING, base_url=str(BASE)).write_pdf(out)

if __name__ == "__main__":
    render_pdf()
```

> `base_url` risolve correttamente i path relativi per font/immagini/CSS; i font referenziati sono **embed** nel PDF. ([doc.courtbouillon.org][6])

---

### 5.2 Template + CSS separati (best practice)

```python
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

BASE = Path(__file__).parent
env = Environment(loader=FileSystemLoader(BASE/"templates"), autoescape=True)

def make_report(data: dict, out="report.pdf"):
    html = env.get_template("report.html").render(data=data)
    styles = [
        CSS(filename=str(BASE/"styles"/"print.css")),
        CSS(filename=str(BASE/"styles"/"fonts.css")),
    ]
    HTML(string=html, base_url=str(BASE)).write_pdf(out, stylesheets=styles)

if __name__ == "__main__":
    make_report({"items": [{"k": "A", "v": 10}, {"k": "B", "v": 20}]})
```

> Puoi anche passare stylesheet remoti o oggetti `CSS(string=...)`. ([doc.courtbouillon.org][4])

---

### 5.3 Risorse protette: URL fetcher personalizzato

```python
from weasyprint import HTML
from weasyprint.default_url_fetcher import default_url_fetcher

def auth_fetcher(url):
    """Esempio: aggiunge header a richieste HTTP per CSS/immagini/font."""
    res = default_url_fetcher(url)
    if res["string"] is None and res["file_obj"] is None and res["redirected_url"].startswith("https://api.example"):
        # qui potresti usare requests per scaricare con auth e restituire res["string"] = bytes
        pass
    return res

HTML("https://example.com/report.html").write_pdf(
    "secured.pdf",
    url_fetcher=auth_fetcher
)
```

> WeasyPrint permette un **URL fetcher** custom per gestire autenticazione/cookie nell’accesso a risorse esterne. ([doc.courtbouillon.org][9])

---

## 6) Requirements

### 6.1 `requirements.txt` (Python)

```txt
weasyprint>=66
jinja2>=3.1   # opzionale per templating
```

> WeasyPrint porta già con sé dipendenze come pydyf, Pillow, fontTools, Pyphen, tinycss2/tinyhtml5/cssselect2. ([doc.courtbouillon.org][4])

### 6.2 Pacchetti di sistema (riassunto)

* **Ubuntu/Debian minimi** (con wheels): `libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libharfbuzz-subset0`
  **Extra build** (senza wheels): `libffi-dev libjpeg-dev libopenjp2-7-dev`
  **Font consigliati**: `fonts-noto fonts-noto-cjk fonts-noto-color-emoji`. ([doc.courtbouillon.org][4])

* **macOS**: `brew install weasyprint` (CLI). Per libreria Python: `pip install weasyprint` in venv; usa la variabile `DYLD_FALLBACK_LIBRARY_PATH` solo se necessario. ([doc.courtbouillon.org][4])

---

## 7) Troubleshooting rapido

* **“cannot load library …” su macOS/Windows**
  Verifica istruzioni e, se serve, imposta `DYLD_FALLBACK_LIBRARY_PATH` (macOS) o `WEASYPRINT_DLL_DIRECTORIES` (Windows / MSYS2). ([doc.courtbouillon.org][4])

* **Test ambiente**
  `weasyprint --info` stampa versione e librerie rilevate. ([doc.courtbouillon.org][4])

* **Mancano font / quadratini**
  Installa font di sistema o dichiara `@font-face` con URL locali/remoti per forzare la famiglia. ([doc.courtbouillon.org][4])

* **Resource not found** (immagini/CSS/font non caricati)
  Imposta **`base_url`** quando passi HTML come stringa. ([doc.courtbouillon.org][6])

* **RTL irregolare o giustificazione**
  Supporto in evoluzione (fix recenti); verifica su casi reali e tieni WeasyPrint aggiornato. ([doc.courtbouillon.org][8])

---

## 8) Glossario (termini tecnici chiariti)

* **Pango**: libreria per **layout e rendering del testo** con forte supporto internazionale (bidi, shaping). WeasyPrint la usa per impaginare il testo. ([The GTK Team][3])
* **HarfBuzz**: motore di **shaping** usato da Pango per trasformare caratteri in glifi corretti per script complessi. ([https://docs.gtk.org][10])
* **Cairo** *(storico)*: libreria 2D multi-backend (anche PDF). **Non è più** richiesta dalle versioni moderne di WeasyPrint. ([cairographics.org][11])
* **GDK-Pixbuf** *(storico)*: libreria per **caricamento/scaling** immagini usata nel mondo GTK; non richiesta in WeasyPrint moderno. ([https://docs.gtk.org][12])
* **pydyf**: generatore **PDF in Python** creato per WeasyPrint al posto di Cairo. ([courtbouillon.org][1])
* **Hyphenation**: gestione della **sillabazione automatica** in base alla lingua; in WeasyPrint si attiva con `hyphens: auto` + `lang`, basata su **Pyphen**. ([doc.courtbouillon.org][7])

---

## 9) Checklist di produzione

* [ ] **Installa Pango** (e HarfBuzz) nel container/VM; verifica con `pango-view --version`. ([doc.courtbouillon.org][4])
* [ ] **Font Noto** completi (Latin + CJK + Emoji) o `@font-face` locali; evita dipendenza da CDN. ([doc.courtbouillon.org][4])
* [ ] Aggiungi `lang` sull’`<html>` e `hyphens: auto` per testi giustificati. ([doc.courtbouillon.org][7])
* [ ] Usa `base_url` quando rendi HTML da stringhe. ([doc.courtbouillon.org][6])
* [ ] Integra **test** in CI che aprono il PDF generato e controllano presenza di glifi/emoji critici (smoke test).
* [ ] Se supporti **RTL**, verifica i casi reali e monitora i changelog WeasyPrint. ([doc.courtbouillon.org][8])

---

## 10) Appendice: perché molte guide parlano ancora di Cairo/GDK-Pixbuf?

Perché prima della **versione 53 (2021)** WeasyPrint **usava Cairo** per generare PDF (spesso con GDK-Pixbuf per immagini). Il team ha rimosso tale dipendenza introducendo **pydyf**, semplificando notevolmente deploy e CI. Se stai seguendo articoli datati, aggiorna i prerequisiti: oggi è **Pango-centrico**. ([courtbouillon.org][1])

---

**Riferimenti principali**: Documentazione WeasyPrint “First Steps” e “API Reference” (dipendenze, install su Linux/macOS, hyphenation, font embedding), blog post ufficiale sul passaggio a pydyf, changelog recente (fix RTL/emoji), e documentazione Pango/Cairo/GDK-Pixbuf per il ruolo delle librerie. ([doc.courtbouillon.org][4])

[1]: https://www.courtbouillon.org/blog/00008-weasyprint-53-beta/?utm_source=chatgpt.com "WeasyPrint Without Cairo: Beta Time - CourtBouillon"
[2]: https://doc.courtbouillon.org/weasyprint/stable/?utm_source=chatgpt.com "WeasyPrint 66.0 documentation - CourtBouillon"
[3]: https://www.gtk.org/docs/architecture/pango?utm_source=chatgpt.com "Pango"
[4]: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html "First Steps - WeasyPrint 66.0 documentation"
[5]: https://doc.courtbouillon.org/weasyprint/v61.1/api_reference.html?utm_source=chatgpt.com "API Reference — WeasyPrint 61.1 documentation"
[6]: https://doc.courtbouillon.org/weasyprint/v56.1/api_reference.html?utm_source=chatgpt.com "API Reference — WeasyPrint 56.1 documentation"
[7]: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html?utm_source=chatgpt.com "API Reference - WeasyPrint 66.0 documentation - CourtBouillon"
[8]: https://doc.courtbouillon.org/weasyprint/stable/changelog.html?utm_source=chatgpt.com "Changelog - WeasyPrint 66.0 documentation"
[9]: https://doc.courtbouillon.org/weasyprint/latest/first_steps.html?utm_source=chatgpt.com "First Steps - WeasyPrint 66.0 documentation - CourtBouillon"
[10]: https://docs.gtk.org/Pango/pango_bidi.html?utm_source=chatgpt.com "Pango – 1.0: Bidirectional and Vertical Text"
[11]: https://www.cairographics.org/?utm_source=chatgpt.com "Cairo graphics library"
[12]: https://docs.gtk.org/gdk-pixbuf/?utm_source=chatgpt.com "GdkPixbuf – 2.0"
