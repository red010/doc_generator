# Issue 01: `docxtpl` Fails to Render Context into Programmatically Generated Template

- **Status**: `Resolved`
- **Priority**: `Critical`
- **Assignee**: `AI Agent`
- **Resolution Date**: `2025-09-30`

---

## 1. Objective

The primary goal is to successfully generate a `.docx` document using the `docxtpl` library. The process involves:
1.  A Python script (`a1_docxtpl_basic.py`) that reads a JSON data file (`a1_data.json`).
2.  The script loads a `.docx` template (`a1_basic_template.docx`).
3.  The script renders the JSON data into the template.
4.  The final output (`out_a1_basic.docx`) should be a fully populated document.

## 2. Core Problem Description

Despite multiple attempts to align the data source and the template, the final generated document (`out_a1_basic.docx`) contains empty fields. The `docxtpl` rendering process completes without errors, but the Jinja2 variables and loops (`{{...}}`, `{%...%}`) within the template are not being replaced with the context data.

## 3. Affected Files & Their Roles

- **Execution Script**: `docx-stack-examples/src/a1_docxtpl_basic.py`
  - **Role**: Orchestrates the document generation process. Loads data and template, calls the `.render()` method, and saves the output.

- **Data Source**: `docx-stack-examples/data/a1_data.json`
  - **Role**: Provides the structured context data (as JSON) to be rendered into the template.

- **Template Generator**: `docx-stack-examples/tools/make_templates.py`
  - **Role**: Programmatically generates the `a1_basic_template.docx` file using the `python-docx` library. This script is the suspected source of the issue.

- **Template File**: `docx-stack-examples/templates/a1_basic_template.docx`
  - **Role**: The `.docx` template containing Jinja2 placeholders. It is the output of the `make_templates.py` script.

- **Output File**: `docx-stack-examples/build/out_a1_basic.docx`
  - **Role**: The final, generated document which currently exhibits the issue (empty fields).

## 4. Problem Deep Dive & Current Hypothesis

The root cause is **not** in the data (`.json`) or the rendering script (`.py`). The issue lies in the structural integrity of the programmatically generated template (`.docx`).

**Hypothesis**: The `make_templates.py` script, while creating a visually correct document, generates a `.docx` file with an underlying XML structure that is incompatible with `docxtpl`.

According to `docxtpl` documentation, a Jinja2 tag (e.g., `{{ report_title }}`) **must** exist within a single, continuous XML "run" (`<w:r>`) inside the `document.xml` file that is part of the `.docx` archive.

When `python-docx` is used to create paragraphs (e.g., `doc.add_paragraph("{{ report_title }}")`), Microsoft Word's own logic can, and often does, fragment that string across multiple "runs". For example, it might create one run for `{{`, another for `report_title`, and a third for `}}`.

When `docxtpl` parses this, it does not see a valid Jinja2 tag and therefore silently ignores it, resulting in the placeholder text being rendered as-is or as an empty string. The last attempted solution tried to fix this by using lower-level functions to enforce single "runs" and by using `docxtpl`-specific syntax for loops (`{%p ... %}` and `{%tr ... %}`), but it still failed. This suggests the programmatic creation via `python-docx` is inherently fragile and unreliable for this purpose.

## 5. Attempted Solutions (Chronological Log)

1.  **Attempt 1: Fix `FileNotFoundError`**
    -   **Action**: Created an initial, simple `a1_data.json` file.
    -   **Result**: Failure. Solved the file not found error, but the subsequent run produced an empty document.
    -   **Analysis**: Data structure did not match the template.

2.  **Attempt 2: Align Data with Assumed Template**
    -   **Action**: Replaced the simple JSON with a rich, complex data structure matching a typical report.
    -   **Result**: Failure. Output document fields remained empty.
    -   **Analysis**: The template's placeholders were incorrect.

3.  **Attempt 3: Programmatic Template Generation**
    -   **Action**: Modified `make_templates.py` to generate a template whose placeholders matched the rich JSON data.
    -   **Result**: Failure. Fields remained empty.
    -   **Analysis**: The generated template was syntactically incorrect for `docxtpl` loops and likely had the XML "run" fragmentation issue.

4.  **Attempt 4: Advanced Programmatic Template Generation**
    -   **Action**: Completely rewrote the template generation function in `make_templates.py` to handle XML "runs" carefully and use `docxtpl`-specific loop syntax.
    -   **Result**: Failure. The problem persists, indicating this approach is fundamentally flawed.

## 6. Recommended Strategy for Resolution

The programmatic generation of the template via `python-docx` is the point of failure. The recommended strategy is to abandon this method and adopt the official, most reliable workflow.

1.  **Action: Manual Template Creation**.
    -   **Instruction**: Create the `a1_basic_template.docx` file **manually** using a word processor like Microsoft Word or LibreOffice.
    -   **Process**: Open a blank document, type the Jinja2 tags directly into the document where they should appear, and save the file. This guarantees that the underlying XML structure is valid and that each tag exists in a single "run".
    -   **Reference**: Use the keys from `a1_data.json` as the variable names.

2.  **Action: Deprecate the Template Generator**.
    -   **Instruction**: The script `docx-stack-examples/tools/make_templates.py` should be considered a failed experiment and should not be used. It can be deleted or moved to an archive to prevent future confusion.

3.  **Action: Re-run the Core Script**.
    -   **Instruction**: After the manually created template is in place, execute `python docx-stack-examples/src/a1_docxtpl_basic.py`.
    -   **Expected Outcome**: The generation process should now succeed, producing a fully populated document.

## 7. Resolution Summary

The issue has been **successfully resolved** by implementing the recommended strategy.

### Actions Taken:

1.  **Archived the Programmatic Template Generator**:
    -   Moved `docx-stack-examples/tools/make_templates.py` to `_archive/` folder.
    -   This file is now deprecated and should not be used.

2.  **Removed the Problematic Template**:
    -   Deleted the programmatically generated `a1_basic_template.docx` that contained fragmented Jinja2 tags.

3.  **Created Manual Template**:
    -   A new `a1_basic_template.docx` was created manually using Microsoft Word.
    -   All Jinja2 tags were inserted directly into single XML runs, ensuring `docxtpl` compatibility.
    -   Template includes proper formatting with headings, paragraphs, and list structures.

4.  **Verified Solution**:
    -   Executed `python docx-stack-examples/src/a1_docxtpl_basic.py`
    -   **Result**: ✅ **SUCCESS** - All template variables are now properly rendered
    -   Generated document contains all expected content: titles, sections, loops, and data

### Key Learnings:

-   **Programmatic template generation with `python-docx` is fundamentally unreliable** for `docxtpl` compatibility due to XML run fragmentation.
-   **Manual template creation ensures proper XML structure** and guarantees that Jinja2 tags exist in single runs.
-   **This approach is more maintainable** as templates become editable Word documents that non-developers can modify.

### Files Affected:

-   **Archived**: `_archive/make_templates.py`
-   **Created**: `docx-stack-examples/templates/a1_basic_template.docx` (manual)
-   **Generated**: `docx-stack-examples/build/out_a1_basic.docx` (fully populated)
-   **Updated**: This issue documentation

The docx generation pipeline is now fully functional and ready for production use.
