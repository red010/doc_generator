---

title: "Font locali con WeasyPrint: Noto (Latin+CJK+Emoji), @font-face e perché evitare i CDN"
description: "Guida operativa per ottenere PDF coerenti e riproducibili con WeasyPrint: scelta e packaging dei font (Noto), fallback per CJK/RTL/Emoji, embedding via @font-face, niente dipendenze da CDN. Include esempi completi (CSS, Python), note Docker/CI e glossario (CDN, glyph, subsetting, ecc.)."
authors:

* "Enrico Busto"
* "ChatGPT (GPT-5 Thinking)"
  last_updated: "2025-09-29"
  version: "1.0"
  status: "stable"
  license: "CC BY 4.0"
  tags: ["weasyprint", "fonts", "noto", "emoji", "CJK", "RTL", "hyphenation", "embedding", "subsetting", "docker", "cdn", "offline"]

---

# Font Noto completi o `@font-face` locali; evita dipendenza da CDN

## Obiettivo

Garantire che i PDF generati da **WeasyPrint** risultino **identici, completi e stabili** in tutti gli ambienti (dev, CI/CD, produzione), **senza quadratini (“tofu”)** né sorprese dovute a risorse di rete esterne.

---

## 1) Perché portare i font “in casa”

* **Coerenza visiva**: se i font **non sono locali**, il layout può cambiare (font fallback diversi per sistema, aggiornamenti remoti non controllati).
* **Assenza di “tofu”**: i set **Noto** coprono Latin + **CJK** (Cinese/Giapponese/Coreano) + **Emoji**, minimizzando i glifi mancanti.
* **Riproducibilità**: i **font versionati nel repo/container** rendono i build deterministici.
* **Sicurezza/Privacy/Compliance**: nessuna chiamata verso terze parti durante la generazione (utile in reti **air-gapped** o con policy restrittive).
* **Performance**: zero round-trip di rete in CI; meno punti di rottura (**SPOF**).

**In sintesi**: includi i font nel progetto e dichiara gli stack via `@font-face`. Non affidarti a **CDN** per i font a runtime.

---

## 2) Set consigliato (copertura ampia)

* **Latin e alfabeti vicini**: `Noto Serif`, `Noto Sans`, `Noto Mono`
* **CJK**: `Noto Sans CJK SC/TC/JP/KR` (scegli in base ai testi)
* **Emoji**: `Noto Color Emoji` (supporto colore dipende dal viewer PDF)

> Se i documenti sono multilingue, potresti includere più varianti CJK (SC/TC/JP/KR). In alternativa, caricale “on demand” con `unicode-range` (vedi più avanti).

---

## 3) Architettura dei font nel progetto

```
project/
  assets/fonts/
    NotoSerif-Regular.ttf
    NotoSans-Regular.ttf
    NotoMono-Regular.ttf
    NotoSansCJKsc-Regular.otf
    NotoColorEmoji.ttf
  styles/
    fonts.css
    print.css
  templates/
    report.html
  generate.py
```

---

## 4) CSS: embedding e fallback intelligenti

**styles/fonts.css**

```css
/* Base Latin */
@font-face {
  font-family: "NotoSerifLocal";
  src: url("../assets/fonts/NotoSerif-Regular.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

/* Monospace per codice */
@font-face {
  font-family: "NotoMonoLocal";
  src: url("../assets/fonts/NotoMono-Regular.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

/* CJK (SC = Chinese Semplificato). Carica solo quando serve */
@font-face {
  font-family: "NotoSansCJKLocal";
  src: url("../assets/fonts/NotoSansCJKsc-Regular.otf") format("opentype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  /* Limita ai blocchi Unicode CJK principali: usato solo se compaiono ideogrammi */
  unicode-range: U+3400-4DBF, U+4E00-9FFF;
}

/* Emoji (colore) */
@font-face {
  font-family: "NotoColorEmojiLocal";
  src: url("../assets/fonts/NotoColorEmoji.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

**styles/print.css**

```css
/* Stack di fallback: Latin → CJK → Emoji → serif */
:root {
  --font-body: "NotoSerifLocal", "NotoSansCJKLocal", "NotoColorEmojiLocal", serif;
  --font-code: "NotoMonoLocal", monospace;
}

html { font-family: var(--font-body); line-height: 1.35; }
code, pre { font-family: var(--font-code); }

/* Hyphenation: sillabazione automatica (richiede lang sull'HTML) */
html[lang="it"] { hyphens: auto; }
```

**templates/report.html**

```html
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8" />
  <title>Report con font locali</title>
  <link rel="stylesheet" href="../styles/fonts.css" />
  <link rel="stylesheet" href="../styles/print.css" />
</head>
<body>
  <h1>Copertura internazionale</h1>
  <p>Italiano con sillabazione automatica: stra-or-di-na-ria.</p>
  <p>Cinese (SC): 示例文本。日本語: 例文。한국어 예문.</p>
  <p>RTL (arabo): <span dir="rtl">هذا نص عربي تجريبي</span></p>
  <p>Emoji: ✅ 🔥 🚀</p>
  <pre><code>codice_monospazio();</code></pre>
</body>
</html>
```

---

## 5) Esempio Python (WeasyPrint)

```python
from pathlib import Path
from weasyprint import HTML, CSS

BASE = Path(__file__).parent

def build_pdf():
    html_file = BASE / "templates" / "report.html"
    css_fonts = CSS(filename=str(BASE / "styles" / "fonts.css"))
    css_print = CSS(filename=str(BASE / "styles" / "print.css"))
    out = BASE / "out.pdf"

    HTML(filename=str(html_file)).write_pdf(
        target=str(out),
        stylesheets=[css_fonts, css_print],
    )
    print("PDF generato:", out.resolve())

if __name__ == "__main__":
    build_pdf()
```

**Perché funziona bene**

* Font **locali** referenziati con `@font-face` ⇒ WeasyPrint li **incorpora** nel PDF (subset automatico dei glifi usati).
* `lang="it"` + `hyphens: auto` ⇒ sillabazione corretta in italiano.
* Fallback CJK/Emoji ⇒ niente tofu anche con ideogrammi o emoji.

---

## 6) Quando usare questa strategia

Usala **sempre** quando:

* vuoi **PDF identici** tra dev/CI/prod e in futuro (determinismo);
* lavori in **CI/CD** o in ambienti **offline/air-gapped**;
* i documenti includono **lingue miste** (CJK/RTL) o **emoji**;
* hai policy di **sicurezza** che vietano chiamate a terzi durante la build.

---

## 7) Note su Docker/CI

Aggiungi i font **Noto** nel container (o versionali dentro `assets/fonts/`). Esempio Debian/Ubuntu slim:

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libharfbuzz-subset0 \
 && rm -rf /var/lib/apt/lists/*

# Se preferisci installare pacchetti font di sistema:
# RUN apt-get update && apt-get install -y fonts-noto fonts-noto-cjk fonts-noto-color-emoji

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "generate.py"]
```

> **Opzione A**: porti i TTF/OTF nel repo e li referenzi via `@font-face`.
> **Opzione B**: installi pacchetti font di sistema (più semplice, ma attenzione a versioni diverse tra ambienti).

---

## 8) Perché evitare i **CDN** (approfondito)

* **CDN** (“Content Delivery Network”): rete di server distribuiti che consegna contenuti statici (es. **Google Fonts**) in modo veloce e vicino all’utente.
* **Problemi in pipeline PDF**:

  * **Indeterminismo**: i file sul CDN possono cambiare o diventare temporaneamente non disponibili ⇒ la stessa build produce PDF diversi o fallisce.
  * **Affidabilità**: dipendi da rete, DNS, firewall, blocchi geografici.
  * **Sicurezza/Privacy**: chiamate esterne durante la generazione violano policy in aziende/PA o in ambienti **air-gapped**.
  * **Prestazioni**: round-trip extra in CI ⇒ più lenti e fragili.
  * **Licenze & audit**: meglio includere nel progetto i file che effettivamente usi, con versioni note.

**Se proprio usi un CDN in sviluppo**, **“vendorizza”** i font: scaricali in **fase di build** e referenziali **in locale** in produzione.

---

## 9) Pitfall comuni (e rimedi)

* **Quadratini (tofu)** → manca il glifo: aggiungi font adeguati o amplia lo stack (`NotoSansCJK`, emoji).
* **PDF pesante** → i font CJK sono grandi: lo **subsetting** riduce, ma considera `unicode-range` per caricarli **solo se servono**.
* **Emoji in b/n** → dipende da supporto colore del viewer/catena; accetta il fallback o usa icone SVG locali.
* **Aspetti diversi tra ambienti** → assicurati di usare **gli stessi file di font** (repo o immagine Docker).
* **Hyphenation non attiva** → manca `lang` o `hyphens: auto`; imposta entrambi.

---

## 10) Requirements

**requirements.txt**

```txt
weasyprint>=66
jinja2>=3.1     # se usi templating
```

**Sistema (Debian/Ubuntu)**
`libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libharfbuzz-subset0`
*(facoltativo)* `fonts-noto fonts-noto-cjk fonts-noto-color-emoji`

---

## 11) Glossario dei termini

* **CDN (Content Delivery Network)**: rete di server globali che distribuisce contenuti statici (file font, JS, immagini). Vantaggiosa per siti web pubblici; **sconsigliata** in pipeline PDF/CI per determinismo e sicurezza.
* **Fallback di font**: catena di famiglie in `font-family`; se il primo font non ha il glifo, si passa al successivo.
* **Embedding**: incorporare i font **dentro** il PDF, così il file visualizza correttamente il testo ovunque.
* **Subsetting**: includere nel PDF **solo i glifi effettivamente usati**, per ridurre la dimensione del file.
* **Glyph (glifo)**: la “forma” concreta di un carattere in un font (ad es. la lettera “A” in una data famiglia).
* **Shaping**: trasformazione di sequenze di caratteri in glifi corretti per lingua/script (es. legature, diacritici, arabo).
* **CJK**: Chinese–Japanese–Korean; script con set Unicode estesi e regole di a capo diverse.
* **RTL (Right-To-Left)**: direzione di scrittura da destra a sinistra (es. arabo, ebraico).
* **Hyphenation**: sillabazione automatica; in CSS si attiva con `hyphens: auto` e richiede `lang` corretto.
* **Air-gapped**: ambiente senza accesso a internet (o con accesso fortemente controllato).
* **SPOF (Single Point Of Failure)**: componente unico la cui indisponibilità blocca l’intero sistema.
* **Vendorizzare (vendor/vendoring)**: includere nel progetto (o nell’immagine) copie locali di librerie/font invece di puntare a risorse esterne (CDN).
* **unicode-range**: direttiva `@font-face` per indicare quali intervalli Unicode copre un dato file font; abilita caricamento mirato.

---

## 12) In breve (checklist)

* [ ] Metti i **font Noto** nel repo/immagine o installa i pacchetti `fonts-noto*`.
* [ ] Dichiara `@font-face` e **stack di fallback** con Latin → CJK → Emoji.
* [ ] Imposta `lang` e `hyphens: auto` quando vuoi sillabazione.
* [ ] **Non** richiamare **CDN** a runtime: se servono in dev, **vendorizza** in build.
* [ ] Testa casi CJK/RTL/Emoji in CI per evitare regressioni.
