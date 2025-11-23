# Ai-CareFlow Usage Guide

## Getting Started

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pranu-tech/Ai-CareFlow.git
cd Ai-CareFlow
```

2. **Set up Python environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Using the run script (Linux/Mac)
```bash
./run.sh
```

#### Option 2: Direct Streamlit command
```bash
streamlit run app/streamlit_app.py
```

The application will open automatically in your default browser at `http://localhost:8501`.

## Using the Web Interface

### 1. Input Clinical Text

The main interface provides a text area for entering clinical notes:

- **Manual Entry**: Type or paste clinical text directly
- **Sample Data**: Click "Load Sample Clinical Note" in the sidebar for demo data
- **Supported Format**: Plain text, unstructured clinical notes

**Important**: Only use synthetic/test data. Never enter real patient information.

### 2. Select Output Options

Use the sidebar checkboxes to choose which outputs to generate:

- ☑ **Clinical Summary**: Concise summary with key points
- ☑ **SOAP Note**: Structured medical documentation
- ☑ **Workflow Suggestions**: Documentation reminders and checklists

All options are enabled by default.

### 3. Process Text

Click the **"🔄 Process Text"** button to analyze the input.

The application will:
1. Validate the input text
2. Check text quality metrics
3. Generate selected outputs
4. Display results in organized sections

### 4. Review Results

#### Clinical Summary
- **Summary**: Condensed version of the clinical text
- **Key Points**: Bullet-point highlights of important information
- **Metrics**: Word counts and quality scores

#### SOAP Note
- **Tabs**: Navigate between Subjective, Objective, Assessment, Plan sections
- **Content**: Automatically categorized clinical information
- **Validation**: Check marks indicate section completeness

#### Workflow Suggestions
- **Suggestions**: General documentation recommendations
- **Priority Items**: High-priority action items (highlighted)
- **Checklist**: Interactive documentation checklist
- **Reminders**: Best practices for clinical documentation

### 5. Clear and Reset

Click the **"🗑️ Clear"** button to reset the input area and start fresh.

## Sample Data

The application includes three types of sample clinical notes:

1. **Chest Pain Presentation**: Cardiac-related visit
2. **Routine Checkup**: Annual physical examination
3. **Upper Respiratory Infection**: Common illness visit

Access sample data through the "Load Sample Clinical Note" button in the sidebar.

## Tips for Best Results

### Input Quality

✅ **Good Inputs:**
- Complete sentences
- Clinical terminology
- Organized information
- 50-5000 words ideal

❌ **Poor Inputs:**
- Extremely short text (<10 words)
- Excessive length (>50,000 characters)
- Random characters
- Only whitespace

### Understanding Outputs

**Clinical Summary:**
- First 3 key sentences extracted
- May need manual refinement
- Review for completeness

**SOAP Note:**
- Keyword-based categorization
- May need reordering
- Some sections may require manual completion
- Always validate accuracy

**Workflow Suggestions:**
- Based on content patterns
- General recommendations only
- Not patient-specific advice
- Use professional judgment

## Command-Line Usage

### Using the Python API

```python
from careflow import ClinicalSummarizer, SOAPGenerator, WorkflowSuggester

# Initialize processors
summarizer = ClinicalSummarizer()
soap_gen = SOAPGenerator()
workflow = WorkflowSuggester()

# Input text
text = "Patient presents with..."

# Generate outputs
summary = summarizer.summarize(text)
soap = soap_gen.generate_soap(text)
suggestions = workflow.suggest_workflows(text)

# Access results
print(summary['summary'])
print(soap['subjective'])
print(suggestions['suggestions'])
```

See [API.md](API.md) for complete API documentation.

## Troubleshooting

### Application Won't Start

**Problem**: `streamlit: command not found`
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: Port 8501 already in use
```bash
# Use a different port
streamlit run app/streamlit_app.py --server.port 8502
```

### Processing Errors

**Error**: "Validation Error: Text is too short"
- **Solution**: Enter at least 10 characters of meaningful text

**Error**: "Could not generate summary"
- **Solution**: Ensure text contains complete sentences with clinical content

### Display Issues

**Problem**: UI elements not showing properly
- **Solution**: Clear browser cache and refresh
- **Solution**: Try a different browser (Chrome, Firefox recommended)

**Problem**: Text area not updating
- **Solution**: Click "Clear" and re-enter text
- **Solution**: Refresh the page

## Running Tests

### All Tests
```bash
pytest tests/
```

### Specific Test File
```bash
pytest tests/test_processors.py -v
```

### With Coverage
```bash
pytest tests/ --cov=src/careflow --cov-report=html
```

## Development Mode

### Watch for Changes
```bash
streamlit run app/streamlit_app.py --server.runOnSave true
```

### Debug Mode
Add to the top of `streamlit_app.py`:
```python
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('client.showErrorDetails', True)
```

## Best Practices

### Input Preparation
1. Remove any real patient identifiers
2. Use only synthetic test data
3. Keep text focused and relevant
4. Include key sections (symptoms, vitals, assessment, plan)

### Output Review
1. Always review generated content
2. Verify accuracy of categorization
3. Complete any placeholder sections
4. Add missing clinical details
5. Ensure professional quality

### Documentation Workflow
1. Input clinical encounter notes
2. Review generated summary for accuracy
3. Validate SOAP note sections
4. Check workflow suggestions
5. Manually refine as needed
6. Use as documentation support only

## Keyboard Shortcuts

In the Streamlit interface:

- `Ctrl/Cmd + Enter`: Submit text (from input area)
- `Ctrl/Cmd + K`: Clear input
- `Tab`: Navigate between elements
- `Ctrl/Cmd + R`: Reload page

## Privacy and Safety

### Data Handling
- ✅ All processing is local
- ✅ No data sent to external servers
- ✅ No logging of input content
- ✅ Session-based only (no persistence)

### Safety Reminders
- ⚠️ For demonstration purposes only
- ⚠️ Not for real clinical use
- ⚠️ Not for diagnosis or treatment
- ⚠️ Always use professional judgment
- ⚠️ Review and verify all outputs

## Additional Resources

- **Full Documentation**: [docs/README.md](README.md)
- **API Reference**: [docs/API.md](API.md)
- **Source Code**: [src/careflow/](../src/careflow/)
- **Tests**: [tests/](../tests/)
- **GitHub Issues**: [Report issues](https://github.com/pranu-tech/Ai-CareFlow/issues)

## Getting Help

If you encounter issues:

1. Check this usage guide
2. Review the [README](README.md)
3. Check [API documentation](API.md)
4. Search [GitHub Issues](https://github.com/pranu-tech/Ai-CareFlow/issues)
5. Open a new issue with:
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Screenshots if applicable

---

**Remember**: This is a demonstration tool. Always apply professional clinical judgment and review all generated content.
