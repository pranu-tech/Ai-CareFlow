"""Core orchestration pipeline for AI CareFlow.

This module defines high-level functions that coordinate:
- input preparation
- prompt construction
- model invocation
- output post-processing

`main.py` or other front-ends should call into this layer rather than
interacting with models or prompts directly.
"""

from typing import Any, Dict, List, Protocol

from app.prompts.careflow import build_careflow_prompts
from app.utils.helpers import safe_json_parse
from app.core.models import VisionModelClient


class ModelClient(Protocol):
    """Protocol describing the minimal interface of a model client.

    This allows us to type-hint interactions with OpenAI or other
    backends without committing to a specific implementation.
    """

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response given a list of chat messages."""


def run_careflow_pipeline(
    scenario: str,
    model_client: ModelClient,
    uploaded_image: Any | None = None,
) -> Dict[str, Any]:
    """Run the end-to-end AI CareFlow pipeline for a single scenario.

    Parameters
    ----------
    scenario:
        Synthetic or de-identified clinical text describing a case.
    model_client:
        An object implementing the :class:`ModelClient` protocol.
    uploaded_image:
        Optional uploaded image object (e.g., from Streamlit) to be
        processed via OCR. When provided, any extracted text is appended
        to the scenario before prompt construction.

    Returns
    -------
    dict
        A dictionary containing ``summary``, ``soap_note``, and
        ``workflow_suggestions`` fields suitable for direct use by the
        Streamlit UI.
    """

    # Optionally enrich the scenario with OCR text from an uploaded
    # image. This is strictly text extraction; no interpretation.
    if uploaded_image is not None:
        try:
            vision_client = VisionModelClient()
            extracted_text = vision_client.extract_text(uploaded_image.read())
            if extracted_text.strip():
                scenario = (
                    f"{scenario}\n\n[Extracted text from image]:\n{extracted_text}"
                )
            else:
                scenario = f"{scenario}\n\n[Extracted text from image]:\n(No readable text detected.)"
        except Exception:
            # If OCR fails, we ignore the image and continue with text
            # only; the UI can surface a warning separately.
            pass

    system_prompt, user_prompt = build_careflow_prompts(scenario)

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    raw_content = model_client.generate(messages)

    # Fallback structure mirrors what the UI expects if parsing fails.
    fallback = {
        "summary": raw_content,
        "soap_note": {
            "subjective": "",
            "objective": "",
            "assessment": "",
            "plan": "",
        },
        "workflow_suggestions": [],
        "missing_information": [],
    }

    parsed = safe_json_parse(raw_content, fallback=fallback)

    return {
        "summary": parsed.get("summary", fallback["summary"]),
        "soap_note": parsed.get("soap_note", fallback["soap_note"]),
        "workflow_suggestions": parsed.get(
            "workflow_suggestions", fallback["workflow_suggestions"]
        ),
        "missing_information": parsed.get(
            "missing_information", fallback["missing_information"]
        ),
    }
