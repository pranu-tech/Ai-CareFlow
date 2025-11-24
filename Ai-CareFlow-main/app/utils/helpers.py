import json
import re
from typing import Any, Dict, Optional


# -----------------------------
# JSON-safe model parsing
# -----------------------------


def safe_json_parse(raw_content: str, fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Safely parse model output as JSON.

    - Tries direct ``json.loads`` first.
    - Strips markdown code fences like ```json ... ``` if present.
    - On failure, returns a dict with the raw content plus any ``fallback`` keys.
    """
    if fallback is None:
        fallback = {}

    if not isinstance(raw_content, str):
        return {"raw": str(raw_content), **fallback}

    cleaned = raw_content.strip()

    fence_pattern = r"^```(?:json)?\s*(.*)```$"
    match = re.match(fence_pattern, cleaned, flags=re.DOTALL | re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"raw": cleaned, **fallback}


# -----------------------------
# Reusable prompt fragments
# -----------------------------


def get_disclaimer_fragment() -> str:
    """Standard safety / disclaimer fragment for prompts."""
    return (
        "You are assisting with clinical documentation and workflow ONLY. "
        "You MUST NOT provide diagnoses, medication choices, or treatment plans. "
        "Focus on summarization, documentation structure (e.g., SOAP), and "
        "high-level, non-prescriptive workflow suggestions. "
        "Assume all input is synthetic or de-identified."
    )


def get_soap_instruction_fragment() -> str:
    """Instruction fragment describing SOAP note structure."""
    return (
        "Produce documentation using the SOAP format:\n"
        "- Subjective: Patient-reported history, symptoms, and concerns.\n"
        "- Objective: Observable findings, exam results, key vitals or tests.\n"
        "- Assessment: High-level clinical impressions WITHOUT firm diagnoses.\n"
        "- Plan: High-level, non-prescriptive next steps (e.g., 'consider further "
        "evaluation', 'document X more clearly'), without specific treatments."
    )


def build_careflow_user_prompt(scenario: str) -> str:
    """Build the user prompt body for AI CareFlow using fragments."""
    disclaimer = get_disclaimer_fragment()
    soap_fragment = get_soap_instruction_fragment()

    return f"""
{disclaimer}

{soap_fragment}

Here is a synthetic clinical scenario:

\"\"\"{scenario}\"\"\"

Please respond in STRICT JSON with the following shape:

{{
  "summary": "2-4 bullet points summarizing the visit.",
  "soap_note": {{
    "subjective": "...",
    "objective": "...",
    "assessment": "... (high-level, non-diagnostic)",
    "plan": "... (high-level, non-prescriptive)"
  }},
  "workflow_suggestions": [
    "One high-level follow-up or documentation step",
    "Another high-level administrative or workflow step"
  ]
}}

Do NOT include any text or explanations outside the JSON.
"""


# -----------------------------
# Text sanitization helpers
# -----------------------------


def sanitize_text_input(text: str, max_length: int = 6000) -> str:
    """Basic sanitization for user-provided clinical scenarios.

    - Ensures text is a string.
    - Normalizes newlines.
    - Removes most control characters.
    - Truncates to ``max_length`` characters.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned = "".join(
        ch for ch in cleaned if ch == "\n" or ch == "\t" or (32 <= ord(ch) <= 126)
    )

    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned.strip()
