# Guida alla Configurazione Font e Parametri Tipografici

Questa guida spiega come personalizzare **font** e **parametri tipografici** nel sistema di conversione Pandoc PDF.

## 🎨 Metodi di Configurazione

### 1. Configurazione Programmatica (Python)

```python
from p1_markdown_to_pdf import PandocConfig

# Font personalizzati
config = PandocConfig.customize_fonts(
    mainfont="Times",        # Font principale (serif)
    sansfont="Helvetica",    # Font titoli (sans-serif)
    monofont="Courier",      # Font codice (monospace)
    cjkmainfont=None,        # Font CJK (opzionale)
    mathfont=None           # Font matematica (opzionale)
)

# Conversione con configurazione personalizzata
convert_markdown_to_pdf("input.md", "output.pdf", config)
```

### 2. Configurazione via YAML Front Matter

Nel documento Markdown, aggiungi nel front matter:

```yaml
---
title: "Il Mio Documento"
author: "Nome Autore"

# Configurazione font
mainfont: "Times New Roman"
sansfont: "Arial"
monofont: "Courier New"
fontsize: 12pt

# Parametri tipografici
geometry: margin=2cm
lang: it-IT
colorlinks: true
linkcolor: blue
toc: true
toc-depth: 2
number-sections: true
---
```

### 3. Configurazione Minimale (Default LaTeX)

```python
config = PandocConfig.create_minimal()
# Usa i font di default di LaTeX, senza personalizzazioni
```

## 📝 Parametri Disponibili

### Font

| Parametro | Descrizione | Esempio | Default |
|-----------|-------------|---------|---------|
| `mainfont` | Font principale del testo | `"Times"`, `"Georgia"` | `"Times"` |
| `sansfont` | Font sans-serif per titoli | `"Helvetica"`, `"Arial"` | `"Helvetica"` |
| `monofont` | Font monospace per codice | `"Courier"`, `"Menlo"` | `"Courier"` |
| `cjkmainfont` | Font per caratteri CJK | `"Noto Sans CJK SC"` | `None` |
| `mathfont` | Font per formule matematiche | `"TeX Gyre Termes Math"` | `None` |

### Tipografia

| Parametro | Descrizione | Esempio | Default |
|-----------|-------------|---------|---------|
| `fontsize` | Dimensione carattere principale | `"11pt"`, `"12pt"` | `"11pt"` |
| `geometry` | Margini e layout pagina | `"margin=1in"`, `"margin=2cm"` | `"margin=1in"` |
| `lang` | Lingua del documento | `"it-IT"`, `"en-US"` | Sistema |

### Colori e Link

| Parametro | Descrizione | Esempio | Default |
|-----------|-------------|---------|---------|
| `colorlinks` | Abilita colori per i link | `true`, `false` | `true` |
| `linkcolor` | Colore link interni | `"blue"`, `"red"` | `"blue"` |
| `urlcolor` | Colore URL | `"blue"`, `"green"` | `"blue"` |
| `citecolor` | Colore citazioni | `"green"`, `"purple"` | `"green"` |

### Sommario e Sezioni

| Parametro | Descrizione | Esempio | Default |
|-----------|-------------|---------|---------|
| `toc` | Abilita indice | `true`, `false` | `true` |
| `toc-depth` | Profondità indice | `2`, `3`, `4` | `3` |
| `number-sections` | Numera sezioni | `true`, `false` | `true` |

## 🔧 Font Raccomandati

### Font di Sistema (Sempre Disponibili)

```python
config = PandocConfig.customize_fonts(
    mainfont="Times",      # Serif classico
    sansfont="Helvetica",  # Sans-serif standard
    monofont="Courier"     # Monospace tradizionale
)
```

### Font Moderni (se Installati)

```python
config = PandocConfig.customize_fonts(
    mainfont="Georgia",    # Serif moderno
    sansfont="Verdana",    # Sans-serif moderno
    monofont="Consolas"    # Monospace moderno (solo Windows)
)
```

### Font Noto (Raccomandati per Unicode Completo)

```python
config = PandocConfig.customize_fonts(
    mainfont="Noto Serif",
    sansfont="Noto Sans",
    monofont="DejaVu Sans Mono",
    cjkmainfont="Noto Sans CJK SC"
)
```

## 📋 Esempi Pratici

### Documento Accademico

```yaml
---
title: "Tesi di Laurea"
mainfont: "Times New Roman"
sansfont: "Arial"
fontsize: 12pt
geometry: margin=2.5cm
lang: it-IT
toc: true
toc-depth: 3
number-sections: true
---
```

### Report Tecnico

```yaml
---
title: "Report Tecnico"
mainfont: "Helvetica"
sansfont: "Helvetica"
monofont: "Courier New"
fontsize: 11pt
geometry: margin=1in
colorlinks: true
---
```

### Documento Minimal

```python
# Usa solo configurazione minima
config = PandocConfig.create_minimal()
```

## ⚠️ Risoluzione Problemi

### Font Non Trovati

**Errore**: `The font "NomeFont" cannot be found`

**Soluzioni**:
1. Verifica che il font sia installato nel sistema
2. Usa nomi di font di sistema comuni
3. Usa `PandocConfig.create_minimal()` per configurazione minima

### Caratteri Speciali

**Errore**: Problemi con Unicode/emoji

**Soluzioni**:
1. Installa font Noto per supporto Unicode completo
2. Specifica `cjkmainfont` per caratteri CJK
3. Usa XeLaTeX (già configurato) invece di pdflatex

### Layout Non Corretto

**Problema**: Margini o spaziatura non come atteso

**Soluzioni**:
1. Regola il parametro `geometry`
2. Verifica che `fontsize` sia appropriato
3. Controlla le impostazioni `toc-depth`

## 🚀 Utilizzo Avanzato

### Configurazione Dinamica

```python
def create_config_for_document(doc_type: str) -> PandocConfig:
    if doc_type == "academic":
        return PandocConfig.customize_fonts(
            mainfont="Times",
            sansfont="Helvetica",
            fontsize="12pt"
        )
    elif doc_type == "technical":
        return PandocConfig.customize_fonts(
            mainfont="Helvetica",
            sansfont="Helvetica",
            monofont="Courier"
        )
    else:
        return PandocConfig.create_minimal()
```

### Batch Processing con Font Diversi

```python
configs = {
    "report.pdf": PandocConfig.customize_fonts(mainfont="Times"),
    "presentation.pdf": PandocConfig.customize_fonts(mainfont="Helvetica"),
    "code.pdf": PandocConfig.customize_fonts(monofont="Menlo")
}

for output_name, config in configs.items():
    convert_markdown_to_pdf("input.md", f"build/{output_name}", config)
```

## 📚 Risorse Aggiuntive

- [Documentazione Pandoc](https://pandoc.org/MANUAL.html)
- [Fontspec Package](https://ctan.org/pkg/fontspec)
- [LaTeX Font Catalogue](https://tug.org/FontCatalogue/)
- [Noto Fonts](https://fonts.google.com/noto)
