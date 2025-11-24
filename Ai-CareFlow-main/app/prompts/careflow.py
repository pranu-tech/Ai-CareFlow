"""Prompt builders specific to the AI CareFlow use cases.

This module defines high-level functions that craft system and user
prompts for the core clinical documentation & workflow tasks.

It is designed to build on top of smaller fragments defined in
app.prompts.fragments.
"""

from typing import Tuple

from app.prompts.fragments import (
    get_system_prompt_base,
    get_json_response_instructions,
)


def build_careflow_prompts(scenario: str) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt) for a given free-text scenario.

    The scenario may be messy free text, partial EMR content, bullet
    points, or any other unstructured notes. The model is instructed to
    organize and structure the information without inventing details.
    """
    system_prompt = get_system_prompt_base()

    user_prompt = (
           "You will receive free-text clinical information that may be messy,\n"
           "partially structured, or in bullet points. It may include fragments of\n"
           "notes, partial EMR text, or shorthand.\n\n"
           "Safety and scope rules:\n"
           "- Do NOT provide diagnoses.\n"
           "- Do NOT provide medical advice or treatment recommendations.\n"
           "- Focus only on documentation, organization of information, and workflow support.\n"
           "- When describing the patient, do NOT calculate or infer age from dates of birth.\n"
           "  Use neutral phrases such as 'adult male', 'adult female', 'middle-aged male patient',\n"
           "  or simply 'adult patient'.\n"
           "  Only include a numeric age if the input explicitly gives it (e.g. '48-year-old male').\n\n"
           "Your tasks are:\n"
           "1. Expanded Summary (5–7 bullet points)\n"
           "   - Capture all key information from the input.\n"
           "   - Do NOT invent or guess details that are not clearly stated.\n\n"
        "2. Detailed, non-diagnostic SOAP note\n"
        "   - Subjective: symptoms, history, context, and functional impact, in\n"
        "     clear prose.\n"
        "   - Objective: if explicit vitals or physical exam findings are present in\n"
        "     the source, rewrite them clearly. If such objective data is not\n"
        "     documented in the source text, clearly state that and then provide a\n"
        "     short, neutral placeholder exam for drafting and educational purposes\n"
        "     only. For example: 'Objective findings are not documented in the source\n"
        "     note. The following is a neutral placeholder exam for drafting and\n"
        "     educational purposes only: Patient appears in no acute distress,\n"
        "     speaking in full sentences, breathing comfortably, with no obvious\n"
        "     focal deficits observed.' Do NOT include diagnoses, treatments, or\n"
        "     specific disease labels in this placeholder.\n"
           "   - Assessment: high-level concerns only, using language such as "
           "\"Potential contributing factors may include...\" and "
           "\"Areas of concern for further evaluation include...\". "
           "Do NOT provide firm diagnoses.\n"
           "   - Plan: workflow and documentation actions only — what to document,\n"
           "     what to monitor, what to prepare for clinician review. "
           "No prescriptions, medication choices, or treatment instructions.\n\n"
           "3. Workflow Suggestions (3–5 items)\n"
           "   - Suggest concrete documentation and workflow tasks, such as\n"
           "     clarifying certain history details, organizing data for clinician\n"
           "     review, or preparing follow-up documentation.\n\n"
        "4. Missing Information\n"
        "   - The JSON response must always include a 'missing_information' array.\n"
        "   - List only items that are clearly missing based on common clinical\n"
        "     documentation sections, such as: 'No vital signs documented.',\n"
        "     'No allergies documented.', 'No physical exam findings documented.',\n"
        "     'No family history documented.', 'No social history documented.',\n"
        "     'No medication list documented.', 'No surgical history documented.',\n"
        "     'No past medical history documented.', 'No review of systems\n"
        "     documented.'\n"
        "   - Even if you generate a neutral placeholder Objective section, still\n"
        "     mark the original objective data as missing (for example,\n"
        "     'No vital signs documented in original note.' or\n"
        "     'No physical exam findings documented in original note.'). Do NOT\n"
        "     treat placeholder content as real documentation.\n"
        "   - Do NOT speculate or infer details that are not present. Only state\n"
        "     that such information is missing when it is not mentioned.\n\n"
        "If any information is missing or not clearly stated in the input,\n"
        "explicitly write \"Not specified\" in the relevant SOAP fields rather than guessing.\n\n"
           "Here is the free-text clinical information:\n\n"
           f"'''{scenario}'''\n\n"
           f"{get_json_response_instructions()}\n"
    )

    return system_prompt, user_prompt 