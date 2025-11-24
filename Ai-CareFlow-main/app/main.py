import os
import streamlit as st

from app.config.settings import load_settings
from app.core.models import OpenAIChatModelClient
from app.core.pipeline import run_careflow_pipeline
from app.utils.helpers import sanitize_text_input
from app.prompts.careflow import build_careflow_prompts
from app.utils.io import (
    format_soap_note_as_markdown,
    to_pretty_json_bytes,
    build_pdf_from_output,
    generate_docx,
)

# Global layout styling
settings = load_settings()

if not settings.openai_api_key:
    st.error(
        "OPENAI_API_KEY environment variable is not set.\n\n"
        "In your terminal, run:\n"
        'export OPENAI_API_KEY="your_key_here"\n'
        "and then restart the app."
    )
    st.stop()

model_client = OpenAIChatModelClient(model_name=settings.model.model_name)

# Sidebar: basic info
st.sidebar.title("AI CareFlow v0.1")
st.sidebar.write("by **Pranu Sharma**")

st.sidebar.markdown(
    "**About**\n\n"
    "AI CareFlow is an open-source research & educational project "
    "exploring AI-assisted clinical documentation and workflow support. "
    "It is designed for learning, prototyping, and discussion only."
)

st.sidebar.markdown(
    "**Disclaimer**\n\n"
    "This tool is **not** a diagnostic system and must not be used "
    "for real clinical decisions or patient care."
)

# Sidebar: session history
if "history" not in st.session_state:
    st.session_state["history"] = []

st.sidebar.markdown("---")
st.sidebar.subheader("Session History")
st.sidebar.caption("History clears when app reloads.")

history = st.session_state["history"]
if history:
    # Show up to last 5 scenarios, most recent first
    for idx, entry in enumerate(reversed(history[-5:])):
        label = entry.get("label", f"Scenario {idx+1}")
        preview = entry.get("input_text", "")[:50].replace("\n", " ")
        if preview:
            button_label = f"{label}: {preview}..."
        else:
            button_label = label
        if st.sidebar.button(button_label, key=f"history_{idx}"):
            st.session_state["careflow_result"] = {
                "summary": entry.get("summary"),
                "soap_note": entry.get("soap"),
                "workflow_suggestions": entry.get("workflow"),
                "missing_information": entry.get("missing_info"),
            }
else:
    st.sidebar.caption("No history yet.")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(90deg, #0f766e, #0284c7);
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #0f172a;
        margin-bottom: 0.75rem;
    }
    .accent-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">AI CareFlow (Prototype)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Created by: <strong>Pranu Sharma</strong></div>', unsafe_allow_html=True)

st.markdown(
    "> AI CareFlow is a research & educational project only. "
    "It is **not** a diagnostic tool and must not be used for real clinical decisions."
)

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Input"

tabs = st.tabs(["Input", "Outputs", "Export"])
tab_input, tab_outputs, tab_export = tabs

with tab_input:
    with st.container():
        st.markdown("#### How to use AI CareFlow")
        st.markdown(
            "1. Paste any free-text clinical information (messy notes, bullet points, or partial EMR text) in the box below.  \n"
            "2. Optionally upload a **de-identified** screenshot or image of notes; AI CareFlow will try to extract readable text.  \n"
            "3. Click **Generate Output** on the Outputs tab to see a structured Summary, SOAP note draft, Workflow Suggestions, and Missing Information.  \n"
            "4. Use the Export tab to download the note as Markdown, JSON, or PDF for further editing or discussion."
        )

    st.markdown("---")

    with st.container():
        st.markdown("#### Input")
        uploaded_image = st.file_uploader(
            "Upload an image (optional)", type=["png", "jpg", "jpeg"]
        )
        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption="Uploaded image preview",
                use_container_width=True,
            )
            st.caption(
                "Image text extraction is enabled. Any readable text found in the uploaded image "
                "will be appended to the scenario for documentation purposes only."
            )

        text_input = st.text_area(
            "Paste any free-text clinical information:",
            height=200,
        )

    st.markdown("---")
    st.caption(
        "This tool is for research and educational purposes only and must not be used for real clinical decisions."
    )

    generate_clicked = st.button("Generate Output")

    # Initialize shared result container once
    if "careflow_result" not in st.session_state:
        st.session_state["careflow_result"] = None

    if generate_clicked:
        scenario_text = text_input.strip()

        if not scenario_text and uploaded_image is None:
            st.warning("Please enter text or upload an image.")
            st.stop()

        cleaned_scenario = sanitize_text_input(scenario_text)

        ocr_warning: str | None = None

        with st.spinner("Calling OpenAI and generating documentation..."):
            try:
                result = run_careflow_pipeline(
                    scenario=cleaned_scenario,
                    model_client=model_client,
                    uploaded_image=uploaded_image,
                )
            except Exception:
                # If something goes wrong with OCR or the vision path,
                # fall back to text-only processing.
                ocr_warning = (
                    "Image text extraction failed. Proceeding with text-only input."
                )
                result = run_careflow_pipeline(
                    scenario=cleaned_scenario,
                    model_client=model_client,
                )

        # Save latest result
        st.session_state["careflow_result"] = result
        # Append to in-memory history
        from datetime import datetime

        run_index = len(st.session_state["history"]) + 1
        entry = {
            "input_text": scenario_text,
            "summary": result.get("summary"),
            "soap": result.get("soap_note"),
            "workflow": result.get("workflow_suggestions"),
            "missing_info": result.get("missing_information"),
            "label": f"Scenario {run_index}",
        }
        st.session_state["history"].append(entry)
        st.session_state["active_tab"] = "Outputs"

        if uploaded_image is not None:
            st.markdown(
                "_Image text extraction enabled. Any readable text found in the "
                "uploaded image has been included in the scenario. "
                "Please go to the **Outputs** tab to see the generated output._"
            )
        if ocr_warning is not None:
            st.warning(ocr_warning)

with tab_outputs:
    result = st.session_state.get("careflow_result")

    if result is None:
        st.info("Provide input in the Input tab and click Generate Output to see results here.")
    else:
        with st.expander("Summary", expanded=True):
            summary = result.get("summary", "")
            if isinstance(summary, list):
                for item in summary:
                    st.markdown(f"- {item}")
            else:
                st.write(summary)

        with st.expander("SOAP Note Draft", expanded=True):
            soap = result.get("soap_note", {})
            st.markdown("**Subjective**")
            st.write(soap.get("subjective", ""))

            st.markdown("**Objective**")
            st.write(soap.get("objective", ""))

            st.markdown("**Assessment**")
            st.write(soap.get("assessment", ""))

            st.markdown("**Plan**")
            st.write(soap.get("plan", ""))

        with st.expander("Workflow Suggestions", expanded=False):
            suggestions = result.get("workflow_suggestions", [])
            if suggestions:
                for s in suggestions:
                    st.markdown(f"- {s}")
            else:
                st.write("No suggestions returned.")

        with st.expander("Missing Information", expanded=False):
            missing_items = result.get("missing_information", [])
            if missing_items:
                for item in missing_items:
                    st.markdown(f"- {item}")
            else:
                st.write("No clearly missing information identified.")

with tab_export:
    st.subheader("Export")
    st.write("Choose your preferred format.")

    result = st.session_state.get("careflow_result")
    if result is None:
        st.info("Generate an output first from the Outputs tab to enable exports.")
    else:
        pdf_bytes = build_pdf_from_output(result)
        docx_bytes = generate_docx(result)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download full output as PDF",
                data=pdf_bytes,
                file_name="ai_careflow_output.pdf",
                mime="application/pdf",
            )
        with col2:
            st.download_button(
                label="Download as DOCX",
                data=docx_bytes,
                file_name="ai_careflow_soap_note.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        st.info(
            "AI CareFlow is for research and educational purposes only. "
            "Outputs are approximate and must not be used for real patient care."
        )
