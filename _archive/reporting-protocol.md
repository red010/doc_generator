# Reporting Protocol

This document defines the mandatory standards for creating the final reports for every analysis project. The goal is to produce high-quality, clear, and audience-specific documentation.

---

### 🚨 **Core Principle: Proactive and Exhaustive Depth**

This is the primary directive for all report generation. The agent **MUST** override its default tendency for conciseness and adopt a proactive, exhaustive, and detailed writing style. The goal is not to summarize, but to provide a complete, self-contained narrative that guides the reader through every step of the reasoning process.

#### **Rule Set for `final_analysis_report.md` (Technical Report):**

-   **Justify Every Decision**: For every methodological choice (e.g., algorithm, preprocessing technique, evaluation metric), the agent **MUST** explain not only *what* was done, but *why* it was the optimal choice compared to considered alternatives.
-   **Interpret, Do Not Just Present**: The agent **MUST NOT** simply state a result (e.g., "Recall is 95%"). It **MUST** explain its practical meaning and implications (e.g., "A 95% Recall means the model correctly identifies 19 out of 20 real-world failures, only missing one event. This provides a high degree of confidence in...").
-   **Detail the Data Journey**: The agent **MUST** provide a comprehensive description of the initial dataset, all cleaning and transformation steps, and the final data structure used for model training. Key code snippets **MUST** be included to clarify complex steps.
-   **Narrate All Visuals**: Every figure or table **MUST** be introduced in the preceding text, described in detail, and followed by a comment on its key takeaway. The reader must be told what to look for and what conclusion to draw from the visual.

#### **Rule Set for `executive_summary.md` (Business Report):**

-   **Translate to Business Value**: Every technical finding **MUST** be translated into its direct business impact. Instead of "optimized the threshold," the agent **MUST** write "the system was fine-tuned to drastically reduce unforeseen equipment failures, leading to a potential saving of X machine-downtime hours per year."
-   **Explain Key Concepts Simply**: Abstract concepts (e.g., "Precision," "Recall") **MUST** be explained using simple, business-oriented analogies (e.g., "Recall is our system's ability to 'catch' all true equipment failures. Precision is our ability to ensure that what we 'catch' is a real failure and not a false alarm.").
-   **Formulate Actionable Recommendations**: Conclusions **MUST** be a list of clear, specific, and measurable actions. Example: "Recommendation 1: Deploy the model on Machine X by Q4. Required resources: ...". Generic suggestions are forbidden.

---

## 📜 The Three Standard Reports

Every analysis project must produce **two mandatory reports**. A third is optional and generated only under specific circumstances.

### 🔤 Language Rules

The language of each report is strictly defined:

-   **Full Technical Report**: **ITALIAN** 🇮🇹
-   **Executive Summary**: **ITALIAN** 🇮🇹
-   **Analysis Issues & Improvements**: **ENGLISH** 🇬🇧

---

### 1. Full Technical Report (Mandatory)

-   **File Name**: `final_analysis_report.md`
-   **Location**: `analysis_XX/reports/`
-   **Audience**: Expert Data Analysts, Data Scientists, AI Agents.
-   **Purpose**: To provide a deeply technical, exhaustive, and fully reproducible documentation of the entire analysis process. It must serve as a complete technical archive that allows an expert to replicate and build upon the work.

#### Required Content:
-   ✅ **Exhaustive Methodological Detail**: A granular explanation of every technical choice, including data cleaning steps, feature engineering rationales, model selection criteria, hyperparameter tuning strategies, and validation techniques.
-   ✅ **Complete Results**: Must include **all** tables and figures generated during the analysis. No simplification is allowed.
-   ✅ **In-depth Technical Interpretation**: Every result, plot, and table must be accompanied by a detailed technical interpretation, discussing statistical significance, model behavior (e.g., SHAP value analysis), and potential limitations.
-   ✅ **Code Snippets**: Where relevant, include key code snippets to illustrate complex transformations or model configurations.
-   ✅ **Full Reproducibility Appendix**: A complete list of library versions (`requirements.txt`), references to the exact scripts used for each phase, and any relevant configuration details.
-   ✅ **Self-Contained Technical Narrative**: The document must be a complete and exhaustive technical record of the analysis.

---

### 2. Executive Summary (Mandatory)

-   **File Name**: `executive_summary.md`
-   **Location**: `analysis_XX/reports/`
-   **Audience**: Management, C-Level Executives, Board of Directors.
-   **Purpose**: To provide a self-contained, strategic document that translates the results of the data analysis into clear, actionable business insights for a non-technical audience.

#### Required Content:

-   ✅ **Detailed Context and Goals**: A thorough description of the business context, the problem that initiated the analysis, and the specific, measurable goals that were set.
-   ✅ **Exhaustive but Accessible Explanation of Insights**: A complete and detailed narrative of all key findings. The language must be sober and professional, avoiding technical jargon but without oversimplifying. It must explain *what* was discovered, *why* it is significant, and *how* this conclusion was reached in terms understandable to management.
-   ✅ **Strategic Implications**: For each insight, a clear explanation of its impact on the business.
-   ✅ **Actionable, Data-Driven Recommendations**: Conclude with a list of concrete, specific, and measurable actions that the management can undertake, directly supported by the analysis findings.
-   ✅ **Self-Contained**: The document must be fully understandable on its own, without needing to reference the technical report.

---

### 2. Mandatory Log File: `interim_analysis_log.md`

To ensure project continuity and traceability, a single, standardized analysis log is a mandatory output for every project. This file is the **sole source of truth** for the analysis history.

-   **Filename**: The log must be named `interim_analysis_log.md` and reside in the `analysis_XX/reports/` directory.
-   **Language**: This document **must** be written strictly in **English**.
-   **Format**: The log must be structured to be **machine-readable**. It is an **append-only** file where each entry is a self-contained block with a YAML frontmatter header. Existing entries must never be modified or deleted.
-   **Purpose**:
    1.  **Continuity**: Allows a new agent to parse the file and resume work precisely from where it was left.
    2.  **Traceability**: Serves as the primary source for the final report, documenting key findings and the rationale behind analytical choices.

#### Log Block Structure for `interim_analysis_log.md`

Each entry must follow this structure:

```markdown
---
timestamp: YYYY-MM-DD_HHMMSS
type: [SYSTEM_EVENT | PHASE_SUMMARY | STRATEGY_DECISION | EXPERIMENT_RESULT]
phase: [00_validation | 01_understanding | 02_eda | 03_preprocessing | 04_modeling | 05_conclusions]
status: [SUCCESS | FAILURE | INFO]
author: AGENT
---

### Summary Title of the Event

**Description:**
A human-readable explanation of the action performed.

**Key Results / Metrics:** (Optional)
```yaml
# Structured data in YAML format for easy parsing
key: value
```

**Artifacts Generated:** (Optional)
- `relative/path/to/artifact.png`
---
```

---

### 3. Mandatory Feedback Log: `analysis_issues_and_improvements.md`

This file serves as an immutable, timestamped log for all user-requested issues, annotations, and strategic course-corrections. It is a chronological record of the human-in-the-loop feedback that shapes the project.

-   **Filename**: `analysis_issues_and_improvements.md`
-   **Location**: `analysis_XX/reports/`
-   **Language**: Strictly **ENGLISH** 🇬🇧
-   **Format**: This is an **append-only** file. Each entry is a self-contained block with a YAML frontmatter header. Existing entries must never be modified or deleted.

#### Log Block Structure for `analysis_issues_and_improvements.md`

```markdown
---
timestamp: YYYY-MM-DD_HHMMSS
type: [ISSUE_RAISED | ISSUE_RESOLVED]
author: [USER | AGENT]
references: [YYYY-MM-DD_HHMMSS] # Optional, to link a resolution to an issue
---

### Summary Title of the Feedback or Resolution

A detailed description of the user's feedback, the identified issue, or the action taken to resolve a previously recorded issue.
---
```

---

## 🖼️ Guidelines for Visualizations

-   **Mandatory Inclusion**: Reports with insufficient or irrelevant images will be considered incomplete.
-   **Clear Captions**: All images must have a descriptive caption.
-   **High Quality**: Use high-quality formats (e.g., PNG).

---

## 📊 Guidelines for Tables

-   **Conciseness**: Tables must be concise and directly relevant to the report's narrative. Avoid including raw data dumps or overly long lists.
-   **Size Limits**: To ensure readability, tables should not exceed **20 rows** or **6 columns**. For larger data, present an aggregated summary or a relevant subset.
-   **Formatting**: Tables must be correctly formatted in Markdown to render properly. Ensure that content does not cause horizontal scrolling or break the page layout in the final PDF.

## ⚙️ PDF Generation

Markdown reports must be converted to PDF using the centralized utility. For instructions, see **[PDF Generation Utility](./pdf-generation-utility.md)**.

**Note**: The log files (`interim_analysis_log.md` and `analysis_issues_and_improvements.md`) are intended for machine-readability and project tracking; they **do not** require PDF conversion.
