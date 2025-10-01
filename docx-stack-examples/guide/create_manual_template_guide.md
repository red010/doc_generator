# Guida per Creazione Template Manuale

## Problema Risolto
Il template precedente era generato programmaticamente con `python-docx`, causando frammentazione dei tag Jinja2 in multiple "runs" XML che li rendeva invisibili a `docxtpl`.

## Soluzione: Template Manuale

### Template A1 - Report Base

#### 1. Apri Microsoft Word o LibreOffice Writer

#### 2. Inserisci il Contenuto del Template

Copia e incolla esattamente questo testo nel documento (mantieni la formattazione):

```
{{ report_title }}

Company: {{ company_name }}
Date: {{ publication_date }}    Version: {{ version }}

Executive Summary
{{ executive_summary }}

Introduction
{{ introduction }}

Overview
{%p for section in sections %}
{{ section.title }}
{{ section.content }}
{%p endfor %}

Sales Details by Region

{%tr for row in sales_by_region %}
{{ row.region }}    {{ row.revenue_k_eur }}    {{ row.change_vs_q2 }}
{%tr endfor %}

Key Achievements
{%p for item in key_achievements %}
• {{ item }}
{%p endfor %}

Conclusion
{{ conclusion }}
```

#### 3. Formattazione Consigliata

- **Titoli**: Usa "Heading 1" per `{{ report_title }}`
- **Sottotitoli**: Usa "Heading 2" per "Executive Summary", "Introduction", etc.
- **Lista**: Usa "List Bullet" per gli elementi in `{%p for item in key_achievements %}`

#### 4. Conversione Tabella (Opzionale ma Raccomandato)

Per la sezione "Sales Details by Region", converti le righe dopo l'header in una tabella vera:

1. Seleziona le righe:
   ```
   {%tr for row in sales_by_region %}
   {{ row.region }}    {{ row.revenue_k_eur }}    {{ row.change_vs_q2 }}
   {%tr endfor %}
   ```

2. In Word: `Insert` → `Table` → Converti testo in tabella (separato da tabulazioni)
3. Aggiungi header: "Region", "Revenue (k€)", "Change vs Q2"

#### 5. Salvataggio

- **Nome file**: `a1_basic_template.docx`
- **Posizione**: `docx-stack-examples/templates/`
- **Formato**: DOCX (non DOC)

---

### Template A2 - RichText Demo

#### ✅ **SOLUZIONE: Sintassi RichText Corretta**

Per **RichText objects**, usa la sintassi speciale `{{r variable }}` invece di `{{ variable }}`. Questo risolve il problema di frammentazione XML!

#### 1. Apri Microsoft Word o LibreOffice Writer

#### 2. Inserisci il Contenuto del Template

Crea un documento con esattamente questo contenuto:

```
RichText demo

Intro: {{ intro }}

{{r rich_paragraph }}
```

#### 3. Formattazione Semplice

- **Titolo**: Usa "Heading 1" per "RichText demo"
- **Paragrafi normali** per gli altri due paragrafi con i tag Jinja2

#### 4. Salvataggio

- **Nome file**: `a2_richtext_template.docx`
- **Posizione**: `docx-stack-examples/templates/`
- **Formato**: DOCX (non DOC)

#### 5. Sintassi RichText Essenziale

- **`{{ variable }}`** → Per testo semplice e variabili normali
- **`{{r variable }}`** → **Specificamente per RichText objects** (risolve frammentazione!)
- Lascia che il codice Python gestisca tutta la formattazione avanzata

### Template A3 - Immagini con InlineImage

#### 1. Apri Microsoft Word o LibreOffice Writer

#### 2. Inserisci il Contenuto del Template

Crea un documento con esattamente questo contenuto:

```
Immagini con InlineImage

{{ image }}

Caption: {{ caption }}
```

#### 3. Formattazione Semplice

- **Titolo**: Usa "Heading 1" per "Immagini con InlineImage"
- **Paragrafi normali** per gli altri due paragrafi con i tag Jinja2

#### 4. Salvataggio

- **Nome file**: `a3_images_template.docx`
- **Posizione**: `docx-stack-examples/templates/`
- **Formato**: DOCX (non DOC)

#### 5. Note per Immagini

- Il tag `{{ image }}` verrà sostituito con l'immagine effettiva (nome semplificato per evitare frammentazione)
- Il tag `{{ caption }}` conterrà il testo della didascalia
- Le immagini vengono ridimensionate automaticamente dal codice Python

### 6. Importante (Per Tutti i Template)

- **NON** modificare i tag Jinja2 dopo averli inseriti
- **NON** applicare formattazione diretta ai tag (grassetto, corsivo, etc.)
- I tag devono rimanere testo semplice all'interno dei paragrafi
- Ogni tag deve esistere in un singolo "run" XML (per questo creiamo manualmente)

### 7. Test

Dopo aver creato il template, testa con:
```bash
python docx-stack-examples/src/a1_docxtpl_basic.py    # Template base
python docx-stack-examples/src/a2_richtext.py         # RichText
python docx-stack-examples/src/a3_images.py          # Immagini
```

Il documento generato dovrebbe ora avere tutti i campi popolati correttamente.
