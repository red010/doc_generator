---

title: "HTML/JS → PDF con Chromium headless: guida pratica Playwright/Pyppeteer (2025)"
description: "Come generare PDF ‘snapshot’ di dashboard e componenti client-side con Chromium headless. Architettura, vantaggi, quando usarlo, setup, esempi Python completi e checklist di produzione."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-09-29"
  version: "1.0"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["pdf", "chromium", "playwright", "pyppeteer", "printToPDF", "dashboard", "chartjs", "weasyprint", "headless", "docker"]

---

# HTML/JS → PDF con Chromium headless (Playwright / Pyppeteer)

> **Use case**: produrre un **PDF fedele al browser** partendo da pagine che **richiedono JavaScript** (dashboard, grafici client-side, mappe, componenti React/Vue) renderizzate prima dello “snapshot”.

## 1) Componenti dello stack

* **Chromium headless**
  Motore di rendering che esegue HTML/CSS/JS **come un browser reale** e fornisce l’API `printToPDF` (DevTools Protocol). Opzioni chiave: `printBackground`, `margin`, `format`, `headerTemplate`, `footerTemplate`, `scale`, `preferCSSPageSize`. Alcuni default importanti (es. `printBackground: false`). ([chromedevtools.github.io][1])

* **Playwright (Python)**
  Driver moderno e manutenuto (Microsoft) che controlla Chromium. L’API `page.pdf()` espone direttamente le opzioni PDF (header/footer, scala, `prefer_css_page_size`, `print_background`, `page_ranges`, `outline`, `tagged`, ecc.). Supporta anche `page.emulate_media("screen")` per applicare i CSS “schermo” prima della stampa. ([playwright.dev][2])

* **Pyppeteer (alternativa leggera)**
  Porting Python di Puppeteer; consente `page.pdf()` e `page.emulateMedia('screen')`. Oggi è usato quando si vuole **solo Chromium via CDP** con un ingombro minimo; per progetti enterprise si preferisce Playwright per mantenibilità e feature. ([miyakogi.github.io][3])

* **(Complementare) WeasyPrint**
  Ottimo quando il layout è **HTML/CSS di stampa** senza JS. Per contenuti dinamici, Playwright/Chromium è più adatto perché **esegue** il JS (grafici, dati dal browser). (Riferimenti Playwright per confronto e install: `install --with-deps`, Docker, CI.) ([playwright.dev][4])

## 2) Vantaggi principali

* **Fedeltà 1:1 con il browser**: identico a ciò che vedrebbe l’utente, incluse librerie JS client-side. ([chromedevtools.github.io][1])
* **Stampa avanzata**: header/footer HTML, numerazione, margini/format, rispetto di `@page` con `prefer_css_page_size=True`. ([playwright.dev][2])
* **Controllo del ciclo di rendering**: attese su selettori/eventi, mocking rete, preload script e CSS. ([playwright.dev][5])
* **Opzione PDF “tagged”** (accessibilità): `tagged=True` in `page.pdf()` (qualità dipende dalla semantica del DOM). ([playwright.dev][2])

## 3) Quando scegliere questo stack (e quando no)

**Sceglilo se**:

* Devo catturare **grafici/mappe** generati via JS (Chart.js, ECharts, Mapbox, React/Vue) **prima dello snapshot**.
* Mi serve **fedeltà al browser** (es. kit UI complessi) o CSS non pienamente supportati da motori non-browser.
* Voglio header/footer dinamici, range pagine, margini e **background** stampati (logo, temi). ([playwright.dev][2])

**Evitalo se**:

* Documento “editoriale” con forte **tipografia di stampa** e **niente JS** → meglio **WeasyPrint** (CSS di stampa) o **Pandoc→(LaTeX/Typst)**.
* Ho requisiti **PDF/UA** stringenti: Playwright offre `tagged`, ma l’accessibilità di alta qualità è più prevedibile da pipeline pensate ad hoc per PDF/UA.

> Nota su “prontezza pagina”: Playwright sconsiglia affidarsi ciecamente a `wait_until="networkidle"`; meglio attendere **selettori o condizioni esplicite** (`wait_for_selector`, `wait_for_function`). ([playwright.dev][2])

---

## 4) Setup & requisiti

### 4.1 Requirements (Python)

```txt
# requirements.txt
playwright>=1.47
jinja2>=3.1    # se vuoi templating HTML
```

Poi **installa i browser** (e dipendenze OS, in Linux) con il CLI Python:

```bash
python -m pip install -r requirements.txt
python -m playwright install --with-deps  # installa Chromium e le dipendenze di sistema (Linux/CI)
```

(Per CI vedi la guida ufficiale Playwright Python alla sezione “Continuous Integration”.) ([playwright.dev][4])

### 4.2 Docker (base)

Usa l’immagine Playwright o segui la loro guida: include browser + dipendenze di sistema; tu aggiungi solo il tuo codice Python. ([playwright.dev][6])

---

## 5) Pattern & opzioni cruciali

* **Media type**: `page.emulate_media("screen")` per usare i CSS “screen”; senza, `page.pdf()` usa `print`. ([playwright.dev][2])
* **Sfondo**: `print_background=True` (default è `false`). ([playwright.dev][2])
* **@page**: `prefer_css_page_size=True` per rispettare la dimensione definita in CSS. ([playwright.dev][2])
* **Header/Footer**: abilita `display_header_footer=True` + `header_template`/`footer_template` (limitazioni: niente script ed eredità stili ridotta). ([playwright.dev][2])
* **Attese affidabili**: preferisci `wait_for_selector(...)` o `wait_for_function(...)` legati al **momento in cui il grafico è pronto**, rispetto a `networkidle`. ([playwright.dev][2])
* **Mock rete**: usa routing/mocking Playwright per dati deterministici. ([playwright.dev][5])

---

## 6) Esempi completi (Python)

### 6.1 HTML stringa → PDF (sincrono)

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <style>
    @page { size: A4; margin: 18mm; }
    body { font-family: system-ui, sans-serif; }
    h1 { margin: 0 0 12px 0; }
    .chart { height: 320px; border: 1px solid #ddd; display:flex; align-items:center; justify-content:center; }
  </style>
</head>
<body>
  <h1>Report “snapshot”</h1>
  <p>Questa pagina è renderizzata da Chromium headless.</p>
  <div class="chart">[placeholder grafico]</div>
</body>
</html>
"""

def main():
    out = Path("report.pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()  # puoi impostare locale, deviceScaleFactor, ecc.
        page = context.new_page()
        page.set_content(HTML, wait_until="load")
        page.emulate_media(media="screen")
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
        )
        browser.close()
    print(f"OK: {out.resolve()}")

if __name__ == "__main__":
    main()
```

(Opzioni e comportamenti `page.pdf()` documentati nell’API Playwright Python.) ([playwright.dev][2])

---

### 6.2 URL → PDF con Header/Footer e page ranges

```python
from playwright.sync_api import sync_playwright

HEADER = """
<div style="font-size:10px; width:100%; text-align:center;">
  <span class="title"></span>
</div>
"""

FOOTER = """
<div style="font-size:10px; width:100%; text-align:center;">
  Pagina <span class="pageNumber"></span> / <span class="totalPages"></span>
</div>
"""

def url_to_pdf(url: str, out_path: str = "url_snapshot.pdf"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="load")
        page.emulate_media(media="screen")
        page.pdf(
            path=out_path,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template=HEADER,
            footer_template=FOOTER,
            page_ranges="1-2",     # es.: solo prime due pagine
            prefer_css_page_size=True,
            margin={"top": "15mm", "bottom": "15mm"}
        )
        browser.close()

if __name__ == "__main__":
    url_to_pdf("https://example.com")
```

(Limiti header/footer: **niente `<script>`**, stili pagina non ereditati.) ([playwright.dev][2])

---

### 6.3 Dashboard con Chart.js (asset locali) → PDF (attesa “grafico pronto”)

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent
HTML = (BASE / "dashboard.html").read_text(encoding="utf-8")

def snapshot_dashboard(out="dashboard.pdf"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(base_url="file://" + str(BASE) + "/")

        # Carico HTML con riferimenti locali (chart.min.js, css locali, ecc.)
        page.set_content(HTML, wait_until="load")

        # Inietta Chart.js locale se preferisci farlo a runtime:
        # page.add_script_tag(path=str(BASE / "static" / "chart.min.js"))

        # Attendi un "segnale" dal tuo codice quando il grafico è pronto
        page.wait_for_function("window.dashboardReady === true")

        page.emulate_media(media="screen")
        page.pdf(
            path=out,
            format="A4",
            print_background=True,
            prefer_css_page_size=True
        )
        browser.close()

if __name__ == "__main__":
    snapshot_dashboard()
```

> Suggerimento: nel tuo JS, dopo aver renderizzato i grafici, imposta `window.dashboardReady = true;` e/o aggiungi un attributo `data-ready="1"` su un elemento e aspetta con `page.wait_for_selector('[data-ready="1"]')`. Evita di basarti solo su `networkidle`. ([playwright.dev][2])

---

### 6.4 Mock dei dati di rete (determinismo)

```python
from playwright.sync_api import sync_playwright
import json

def print_with_mock():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Mock di una API GET
        def handle(route, request):
            if "api/metrics" in request.url:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"series": [1,2,3,4,5]})
                )
            else:
                route.continue_()

        page.route("**/*", handle)
        page.goto("http://localhost:3000/dashboard", wait_until="load")
        page.wait_for_selector("#chart-ready")
        page.pdf(path="mocked.pdf", format="A4", print_background=True)
        browser.close()

if __name__ == "__main__":
    print_with_mock()
```

(Mock/middleware di rete documentati nell’API Playwright.) ([playwright.dev][5])

---

### 6.5 Variante **Pyppeteer** (async)

```python
import asyncio
from pyppeteer import launch

async def pyppeteer_pdf():
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    await page.setContent("<h1>Hello from Pyppeteer</h1>")
    await page.emulateMediaType("screen")      # usa CSS 'screen'
    await page.pdf(path="pyppeteer.pdf", format="A4", printBackground=True)
    await browser.close()

asyncio.get_event_loop().run_until_complete(pyppeteer_pdf())
```

(Nota: `pdf()` + `emulateMedia('screen')` sono parte dell’API standard Pyppeteer.) ([miyakogi.github.io][3])

---

## 7) Checklist di produzione

* [ ] **Determinismo**: mock rete, asset **locali** (niente CDN in produzione). ([playwright.dev][5])
* [ ] **Attese robuste**: `wait_for_selector`/`wait_for_function` invece di `networkidle`. ([playwright.dev][2])
* [ ] **Stampa**: `print_background=True`, `prefer_css_page_size=True`, margini e formato appropriati. ([playwright.dev][2])
* [ ] **Header/Footer**: usa solo HTML/CSS “self-contained”, niente script. ([playwright.dev][2])
* [ ] **Accessibilità**: se serve, `tagged=True` (qualità dipende dal DOM). ([playwright.dev][2])
* [ ] **CI/Docker**: usa `python -m playwright install --with-deps` o l’immagine Docker ufficiale. ([playwright.dev][4])

---

## 8) Note su CI e Docker

* **CLI Python**: `python -m playwright install --with-deps` installa **browser e dipendenze OS** (Linux). Esempi ufficiali nelle guide CI Playwright Python. ([playwright.dev][4])
* **Docker**: parti dal Dockerfile Playwright o dalle loro immagini pronte (contengono i browser e le system deps). ([playwright.dev][6])

---

## 9) Limiti e caveat

* **Header/Footer**: i template **non eseguono script** e non ereditano pienamente gli stili della pagina. ([playwright.dev][2])
* **Default “print” media**: senza `emulate_media("screen")` i CSS applicati potrebbero differire (colori, media queries). ([playwright.dev][2])
* **Background off di default**: ricordati `print_background=True`. ([chromedevtools.github.io][1])

---

## 10) Conclusioni

Per **documenti dinamici** che nascono nel browser (JS), **Chromium headless via Playwright** è oggi la via più matura: **esegue** i tuoi componenti, **rispetta** le regole di stampa del browser (con le opzioni giuste) e si integra bene in **CI/Docker**. Mantieni i template/asset sotto controllo, **attendi lo stato “pronto”** in modo esplicito e usa `print_background` + `prefer_css_page_size` per ottenere PDF coerenti e ripetibili. ([playwright.dev][2])

[1]: https://chromedevtools.github.io/devtools-protocol/tot/Page/?utm_source=chatgpt.com "Page domain - Chrome DevTools Protocol"
[2]: https://playwright.dev/python/docs/api/class-page "Page | Playwright Python"
[3]: https://miyakogi.github.io/pyppeteer/reference.html?utm_source=chatgpt.com "API Reference — Pyppeteer 0.0.25 documentation"
[4]: https://playwright.dev/python/docs/ci?utm_source=chatgpt.com "Continuous Integration | Playwright Python"
[5]: https://playwright.dev/python/docs/network?utm_source=chatgpt.com "Network | Playwright Python"
[6]: https://playwright.dev/docs/docker?utm_source=chatgpt.com "Docker"
