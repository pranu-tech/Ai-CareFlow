"""Streamlit web application for Ai-CareFlow."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import streamlit as st
from careflow.processors.clinical_summarizer import ClinicalSummarizer
from careflow.processors.soap_generator import SOAPGenerator
from careflow.processors.workflow_suggester import WorkflowSuggester
from careflow.utils.validators import validate_clinical_text, check_text_quality
from careflow.utils.text_utils import clean_text


# Page configuration
st.set_page_config(
    page_title="Ai-CareFlow",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


def display_safety_disclaimer():
    """Display important safety and usage disclaimers."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Important Disclaimers")
    st.sidebar.warning(
        """
        **NOT FOR CLINICAL DIAGNOSIS**
        
        This tool is for documentation support only. 
        It does NOT provide medical advice, diagnosis, or treatment recommendations.
        
        **Key Points:**
        - Use synthetic/test data only
        - For educational purposes
        - All clinical decisions require professional judgment
        - Review and verify all outputs
        - Not a substitute for clinical expertise
        """
    )


def display_header():
    """Display application header."""
    st.title("🏥 Ai-CareFlow")
    st.markdown(
        """
        ### Healthcare Documentation & Workflow Assistant
        
        Transform clinical notes into structured documentation.
        Generate summaries, SOAP notes, and workflow suggestions.
        
        **⚠️ For demonstration with synthetic data only - Not for real patient data**
        """
    )


def main():
    """Main application function."""
    display_header()
    display_safety_disclaimer()
    
    # Initialize processors
    summarizer = ClinicalSummarizer()
    soap_generator = SOAPGenerator()
    workflow_suggester = WorkflowSuggester()
    
    # Sidebar controls
    st.sidebar.markdown("## 🎛️ Controls")
    
    # Processing options
    st.sidebar.markdown("### Select Outputs")
    generate_summary = st.sidebar.checkbox("Clinical Summary", value=True)
    generate_soap = st.sidebar.checkbox("SOAP Note", value=True)
    generate_workflow = st.sidebar.checkbox("Workflow Suggestions", value=True)
    
    # Sample data
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📝 Sample Data")
    if st.sidebar.button("Load Sample Clinical Note"):
        st.session_state['clinical_text'] = """Patient is a 45-year-old male presenting with complaint of chest discomfort for 2 days. Patient reports the pain as pressure-like, rated 6/10, occurring with exertion. Patient denies shortness of breath, nausea, or diaphoresis. History of hypertension, currently on Lisinopril 10mg daily. Patient denies smoking but reports occasional alcohol use. 

Vital signs: BP 142/88 mmHg, HR 78 bpm, Temp 98.6°F, RR 16, O2 sat 98% on room air.

Physical examination reveals patient is alert and oriented. Heart sounds regular without murmurs. Lungs clear to auscultation bilaterally. No peripheral edema noted.

Assessment: Atypical chest pain, likely musculoskeletal given characteristics. Rule out cardiac etiology given risk factors.

Plan: Order ECG and troponin levels. Start patient on aspirin 81mg daily. Recommend stress test as outpatient. Follow-up in 1 week or sooner if symptoms worsen. Patient education provided regarding warning signs. Patient verbalized understanding."""
    
    # Main input area
    st.markdown("---")
    st.markdown("## 📄 Clinical Text Input")
    
    # Get text from session state or use empty string
    default_text = st.session_state.get('clinical_text', '')
    
    clinical_text = st.text_area(
        "Enter clinical text (synthetic data only)",
        height=300,
        value=default_text,
        placeholder="Paste or type clinical notes here...",
        help="Enter synthetic clinical text for processing. Never use real patient data."
    )
    
    # Store in session state
    if clinical_text:
        st.session_state['clinical_text'] = clinical_text
    
    # Process button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        process_button = st.button("🔄 Process Text", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state['clinical_text'] = ''
        st.rerun()
    
    # Process clinical text
    if process_button:
        if not clinical_text:
            st.error("Please enter clinical text to process.")
            return
        
        # Validate input
        is_valid, error_msg = validate_clinical_text(clinical_text)
        if not is_valid:
            st.error(f"Validation Error: {error_msg}")
            return
        
        # Clean text
        cleaned_text = clean_text(clinical_text)
        
        # Quality check
        quality = check_text_quality(cleaned_text)
        
        st.markdown("---")
        st.markdown("## 📊 Results")
        
        # Display quality metrics
        with st.expander("📈 Text Quality Metrics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Words", quality['word_count'])
            with col2:
                st.metric("Sentences", quality['sentence_count'])
            with col3:
                st.metric("Avg Sentence Length", quality['avg_sentence_length'])
            with col4:
                st.metric("Quality Score", f"{quality['quality_score']}/100")
        
        # Generate Clinical Summary
        if generate_summary:
            st.markdown("### 📋 Clinical Summary")
            with st.spinner("Generating summary..."):
                summary_result = summarizer.summarize(cleaned_text)
                
                if summary_result['status'] == 'success':
                    st.info(summary_result['summary'])
                    
                    # Key points
                    key_points = summarizer.get_key_points(cleaned_text)
                    if key_points:
                        with st.expander("🔑 Key Points", expanded=False):
                            for i, point in enumerate(key_points, 1):
                                st.markdown(f"{i}. {point}")
                else:
                    st.warning("Could not generate summary.")
        
        # Generate SOAP Note
        if generate_soap:
            st.markdown("### 🩺 SOAP Note")
            with st.spinner("Generating SOAP note..."):
                soap_result = soap_generator.generate_soap(cleaned_text)
                
                if soap_result['status'] == 'success':
                    # Display SOAP sections in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["Subjective", "Objective", "Assessment", "Plan"])
                    
                    with tab1:
                        st.markdown("**Subjective:**")
                        st.write(soap_result['subjective'])
                    
                    with tab2:
                        st.markdown("**Objective:**")
                        st.write(soap_result['objective'])
                    
                    with tab3:
                        st.markdown("**Assessment:**")
                        st.write(soap_result['assessment'])
                    
                    with tab4:
                        st.markdown("**Plan:**")
                        st.write(soap_result['plan'])
                    
                    # Validation
                    validation = soap_generator.validate_soap(soap_result)
                    with st.expander("✅ SOAP Validation", expanded=False):
                        for section, is_complete in validation.items():
                            icon = "✅" if is_complete else "⚠️"
                            st.markdown(f"{icon} **{section.title()}**: {'Complete' if is_complete else 'Needs Review'}")
                else:
                    st.warning("Could not generate SOAP note.")
        
        # Generate Workflow Suggestions
        if generate_workflow:
            st.markdown("### 📌 Workflow Suggestions")
            with st.spinner("Generating workflow suggestions..."):
                workflow_result = workflow_suggester.suggest_workflows(cleaned_text)
                
                if workflow_result['status'] == 'success':
                    # Main suggestions
                    if workflow_result['suggestions']:
                        st.markdown("**Suggestions:**")
                        for suggestion in workflow_result['suggestions']:
                            st.markdown(f"- {suggestion}")
                    
                    # Priority items
                    if workflow_result['priority_items']:
                        st.markdown("**Priority Items:**")
                        for item in workflow_result['priority_items']:
                            st.warning(f"⚡ {item}")
                    
                    # Documentation checklist
                    if workflow_result['documentation_checklist']:
                        with st.expander("📋 Documentation Checklist", expanded=False):
                            for item in workflow_result['documentation_checklist']:
                                st.checkbox(item, key=f"check_{hash(item)}")
                    
                    # General reminders
                    with st.expander("💡 Documentation Reminders", expanded=False):
                        reminders = workflow_suggester.get_documentation_reminders()
                        for reminder in reminders:
                            st.markdown(f"- {reminder}")
                else:
                    st.warning("Could not generate workflow suggestions.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p><strong>Ai-CareFlow v0.1.0</strong> | Documentation Support Tool</p>
        <p>⚠️ Not for clinical use | For synthetic data only | Review all outputs</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
