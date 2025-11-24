"""Layout utilities for the AI CareFlow Streamlit UI.

This module defines high-level page layout functions that orchestrate
how different sections (inputs, outputs, settings) are arranged.

At this stage, the functions are placeholders and do not depend on
Streamlit directly. The goal is to keep `main.py` thin and delegate
layout concerns here over time.
"""

from typing import Any, Dict


def build_main_page_layout() -> None:
    """Placeholder hook to render the main AI CareFlow page layout.

    In the future, this function can:
    - Accept a Streamlit-like API object (e.g., `st`) as a parameter.
    - Compose input, output, and sidebar sections using components
      defined in `components.py`.
    """

    # TODO: Integrate with Streamlit components from `components.py`.
    pass


def get_default_sections() -> Dict[str, Any]:
    """Return a description of default UI sections used by the app.

    This is useful as a declarative representation of the UI layout
    that can be inspected or reused in tests.
    """
    return {
        "header": {
            "title": "AI CareFlow (Prototype)",
            "subtitle": "Clinical documentation & workflow assistant (research only)",
        },
        "input": {
            "label": "Paste a synthetic clinical scenario:",
            "height": 180,
        },
        "output": {
            "sections": [
                "summary",
                "soap_note",
                "workflow_suggestions",
            ]
        },
    }
