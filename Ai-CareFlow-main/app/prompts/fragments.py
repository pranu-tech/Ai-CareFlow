"""Reusable prompt fragments for AI CareFlow.

These small text snippets are composed into full prompts by
:mod:`app.prompts.careflow`. Keeping them here makes it easier to
update safety language and formatting in a single place.
"""


def get_system_prompt_base() -> str:
    """Return the base system prompt for AI CareFlow.

    This emphasizes non-diagnostic, documentation-focused behavior.
    """
    return (
        "You are an AI assistant helping with clinical documentation and workflow. "
        "You MUST NOT provide diagnoses or treatment instructions. "
        "You only help summarize information, draft documentation in SOAP format, "
        "and suggest high-level, non-diagnostic workflow steps.\n\n"
        "Always assume the input text is synthetic or de-identified."
    )


def get_json_response_instructions() -> str:
    """Return instructions for the desired JSON response format."""
    return (
        "Please respond in STRICT JSON with the following keys:\n\n"
        "{\n"
        "  \"summary\": \"2-4 bullet points summarizing the visit.\",\n"
        "  \"soap_note\": {\n"
        "    \"subjective\": \"...\",\n"
        "    \"objective\": \"...\",\n"
        "    \"assessment\": \"... (high-level, non-diagnostic)\",\n"
        "    \"plan\": \"... (high-level, non-prescriptive)\"\n"
        "  },\n"
        "  \"workflow_suggestions\": [\n"
        "    \"One high-level follow-up or documentation step\",\n"
        "    \"Another high-level administrative or workflow step\"\n"
        "  ]\n"
        "}\n\n"
        "Do NOT include any extra text or explanations outside the JSON."
    )
