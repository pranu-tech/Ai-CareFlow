# AI CareFlow

AI CareFlow is an open-source AI assistant designed to help reduce healthcare administrative burden by supporting **clinical documentation** and **workflow** tasks. It focuses on streamlining note creation, summarizing patient information, and providing safe, non-diagnostic workflow suggestions — helping clinicians save time and reduce burnout.

## Vision

Clinicians spend significant time charting, navigating EHRs, and writing notes, which contributes to burnout and reduces direct patient time.

AI CareFlow aims to:

- Summarize patient visit information.
- Generate structured **draft** clinical notes (SOAP format).
- Highlight clearly **missing information** in the source note.
- Provide high-level, non-diagnostic **workflow suggestions**.
- Support clinicians, **not** replace clinical judgment.

All processing is designed for **synthetic, de-identified, or publicly available data only**.

## Current MVP Features

- **Visit Summary Generator** (bullet-style summary).
- **SOAP Note Draft Generator** (Subjective, Objective, Assessment, Plan).
- **Missing Information Detector**  
  e.g., “No vital signs documented.” / “No allergies documented.”
- **Workflow Suggestions**  
  Documentation and follow-up task ideas (non-diagnostic, no treatment advice).
- **Vision/OCR Support**  
  Optional de-identified screenshots or images of notes; extracted text is appended to the scenario.
- **Exports**
  - PDF (full output)
  - DOCX (SOAP note–oriented draft)
- **Session History** sidebar
  - Last few scenarios, quickly reloadable without re-calling the model.
- **Streamlit UI** with separate **Input**, **Outputs**, and **Export** tabs.

## Getting Started

### Prerequisites

- Python 3.13 (or compatible 3.x).
- An OpenAI API key.

### Install dependencies

## AI CareFlow

AI CareFlow is an open-source AI assistant designed to help reduce healthcare administrative burden by supporting **clinical documentation** and **workflow** tasks. It focuses on streamlining note creation, summarizing patient information, and providing safe, non-diagnostic workflow suggestions — helping clinicians save time and reduce burnout.

This repository contains an MVP prototype implemented in Python and Streamlit, using OpenAI models with strict safety and non-diagnostic constraints.

---

## Vision

Clinicians spend significant time charting, navigating EHRs, and writing notes, which contributes to burnout and reduces direct patient time.

AI CareFlow aims to:

- Summarize patient visit information.
- Generate structured **draft** clinical notes in SOAP format.
- Highlight clearly **missing information** in the source note.
- Provide high-level, non-diagnostic **workflow suggestions**.
- Support clinicians, **not** replace clinical judgment.

All processing is designed for **synthetic, de-identified, or publicly available data only**.

---

## AI CareFlow Aims To

At a high level, this project aims to:

- **Reduce administrative burden** by turning messy visit notes into structured drafts clinicians can quickly review and edit.
- **Support safer documentation** by calling out obvious missing elements (e.g., no vitals, no allergies, no follow-up plan).
- **Prototype clinician-friendly UX** that feels lightweight and fast: paste a scenario or upload an image, click generate, and see structured outputs.
- **Demonstrate responsible AI use** in healthcare documentation by enforcing strong non-diagnostic, non-treatment rules and transparent limitations.

This MVP is meant as a starting point for further iteration with clinicians, informaticists, and engineers.

---

## Current MVP Features

- **Visit Summary Generator** – succinct, bullet-style summary of the scenario.
- **SOAP Note Draft Generator** – structured output with Subjective, Objective, Assessment, and Plan sections, clearly marked as a *draft*.
- **Missing Information Detector** – highlights obvious documentation gaps, such as:
  - “No vital signs documented.”
  - “No allergies documented.”
  - “No follow-up plan documented.”
- **Workflow Suggestions** – non-diagnostic, non-treatment suggestions focused on documentation completeness, handoffs, and follow-up tasks.
- **Vision/OCR Support** – optional de-identified screenshots or images of notes; extracted text is appended to the scenario before generation.
- **Exports**
  - PDF (summary, SOAP, workflow suggestions, missing information + disclaimer).
  - DOCX (SOAP note–oriented draft suitable for copy/paste into a note).
- **Session History** sidebar
  - Keeps a list of recent “Scenario N: preview...” entries so you can reload prior outputs without re-calling the model.
- **Streamlit UI**
  - Three main tabs: **Input**, **Outputs**, and **Export**.
  - Sidebar for About, Disclaimer, and Session History.

---

## Roles

- **Founder / Developer**: Pranu Sharma

This project is open to collaboration and review from clinicians, informaticists, and other engineers interested in safe, assistive AI for healthcare workflows.

---

## Project Structure

High-level layout of the repository:

- `app/main.py` – Streamlit entry point and UI controller.
  - Renders the three-tab layout (Input, Outputs, Export).
  - Manages sidebar (About, Disclaimer, Session History).
  - Stores and retrieves results in `st.session_state` (`careflow_result`, `history`).
- `app/core/` – core logic and pipeline.
  - `pipeline.py` – orchestrates the end-to-end flow from scenario (and optional image) to structured outputs using OpenAI models.
  - `models.py` – data models and structures used by the pipeline.
  - `safety.py` – centralizes safety rules and checks (non-diagnostic behavior, constraints).
- `app/prompts/` – prompt templates and fragments.
  - `careflow.py` – builds the main system and user prompts, including:
    - Non-diagnostic instructions.
    - Age-handling rules (no inferred ages; only use age if explicitly stated).
    - Requirements to always identify missing information.
  - `fragments.py` – smaller reusable prompt pieces.
- `app/utils/` – helpers and export utilities.
  - `io.py` – functions for JSON formatting, SOAP-as-Markdown, PDF, and DOCX generation.
  - `helpers.py` – parsing, text cleanup, and other small helpers.
  - `pdf_utils_stub.txt` – placeholder / stub for future PDF-specific utilities.
- `app/config/` – configuration and settings.
  - `settings.py` – dataclass-based configuration for model names, API keys, and other options.
- `app/ui/` – UI components and layout helpers.
  - `components.py` – reusable UI pieces (e.g., section headers, disclaimer blocks).
  - `layout.py` – higher-level layout helpers for consistent look and feel.
- `docs/` – design and product documentation.
  - `vision.md` – broader vision and roadmap ideas.
  - `mvp_spec.md` – initial MVP specification and scope.
  - `sample_scenarios.md` – example scenarios for testing and demonstration.

---

## Architecture

Conceptually, AI CareFlow is organized into three layers:

1. **UI Layer (Streamlit)**
   - Handles user interaction (text input, file upload, button clicks).
   - Shows outputs across tabs and controls export/download actions.
   - Uses `st.session_state` to persist the latest result and session history.

2. **Core Pipeline Layer**
   - `run_careflow_pipeline` in `app/core/pipeline.py` is the main orchestrator:
     - Optionally runs vision/OCR on uploaded images.
     - Builds prompts using `app/prompts/careflow.py`.
     - Calls OpenAI models via the Python SDK.
     - Parses and validates JSON-like responses into structured results.
   - Safety rules (e.g., no diagnoses, no treatment recommendations) are enforced via prompts and checks.

3. **Utility & Export Layer**
   - Handles formatting and export of results to Markdown, PDF, and DOCX.
   - Abstracts away details of libraries like `fpdf` and `python-docx`.

This separation keeps UI concerns, model orchestration, and export logic decoupled and easier to evolve.

---

## Getting Started

### Prerequisites

- Python 3.13 (or compatible 3.10+).
- An OpenAI API key with access to the relevant models.

### Install dependencies

From the project root:

```bash
python -m pip install --upgrade pip
python -m pip install streamlit openai fpdf python-docx
```

Set your OpenAI API key in your environment. On Windows PowerShell, for example:

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

### Run the app

From the project root:

```bash
python -m streamlit run app/main.py
```

Then open the URL printed in the terminal (usually `http://localhost:8501`).

---

## Disclaimer

- AI CareFlow is a **prototype** for exploration and education.
- It is **not** a medical device and is **not** approved for clinical use.
- It must **not** be used to make diagnoses, recommend treatments, or replace clinician judgment.
- All examples, scenarios, and data should be **synthetic, de-identified, or publicly sourced**.

Always verify and critically review any output before using it in any real-world context.

---

## Status

- **MVP prototype implemented**: core pipeline, prompts, Streamlit UI, vision/OCR support, exports, and session history are working.
- **Next steps** (future work, not yet implemented):
  - Tighter EHR-like workflows and templates.
  - More robust evaluation and benchmarking with synthetic datasets.
  - Additional export formats and integration patterns.

Contributions, feedback, and issue reports are welcome.

