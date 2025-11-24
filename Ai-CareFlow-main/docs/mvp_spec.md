# AI CareFlow – MVP Specification

## Inputs
- Text box for user to paste synthetic clinical text.
- Later: file upload.

## Outputs
1. Clinical Summary  
2. Draft SOAP Note  
3. Workflow Suggestions (high-level, non-diagnostic)

## Technical Requirements
- Python  
- Streamlit or FastAPI  
- LLM integration (OpenAI / Ollama)  
- Modular code  

## Non-Goals
- No real patient data
- No EHR integration
- No diagnostic decision-making
