# AI CareFlow

AI CareFlow is an open-source AI assistant designed to help reduce healthcare administrative burden by supporting clinical documentation and workflow tasks. The goal is to streamline note creation, summarize patient information, and provide safe, non-diagnostic workflow suggestions — helping clinicians save time and reduce burnout.

---

## Vision

The U.S. healthcare system faces a severe documentation burden. Clinicians spend hours charting, navigating EHRs, and writing notes, leading to burnout and reduced patient time.

**AI CareFlow aims to:**
- Summarize patient visit information  
- Generate structured draft clinical notes (e.g., SOAP format)  
- Provide safe follow-up task suggestions  
- Improve workflow efficiency  
- Support clinicians, not replace clinical judgment  

All processing uses **synthetic or publicly available data only**.

---

## MVP Features

1. **Visit Summary Generator**  
2. **SOAP Note Draft Generator**  
3. **Simple Workflow Suggestions (high-level, non-diagnostic)**  
4. Clean, simple web UI (Streamlit or FastAPI)

---

## Roles

**Pranu Sharma **  
- User research & workflow mapping  
- UX design & safety considerations  
- Documentation & publications  
- Vision, planning, and leadership   
- Backend development  
- LLM integration  
- Architecture & deployment  

---

## Project Structure (planned)
ai-careflow/
app/
docs/
tests/
README.md
LICENSE 

## Architecture

AI CareFlow is structured as a modular Streamlit + OpenAI application:

- `app/main.py` – Streamlit UI, user input, and result display
- `app/core/` – model client and end-to-end CareFlow pipeline
- `app/prompts/` – system and user prompt templates
- `app/utils/` – helpers for JSON parsing and text sanitization
- `app/config/` – app and model settings (API key, model name)
- `app/ui/` – layout and UI components (sidebar, sections)

The project is designed and led by **Pranu Sharma** as an open-source research and educational initiative focused on AI-assisted clinical documentation and workflow support.

---

## Disclaimer

AI CareFlow is for **research and educational** purposes only.  
It is **not** a diagnostic tool and must not be used for medical decision-making.

---

## Status

Early development. MVP coming soon.


