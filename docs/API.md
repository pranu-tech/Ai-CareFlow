# Ai-CareFlow API Documentation

## Core Processors

### ClinicalSummarizer

Generates concise clinical summaries from input text.

#### Class: `ClinicalSummarizer`

##### Methods

###### `summarize(clinical_text: str) -> Dict[str, str]`

Generate a concise clinical summary from input text.

**Parameters:**
- `clinical_text` (str): Raw clinical text input

**Returns:**
- `dict`: Dictionary containing:
  - `summary` (str): Generated summary
  - `original_word_count` (int): Word count of original text
  - `summary_word_count` (int): Word count of summary
  - `status` (str): Processing status ('success', 'empty', 'error')

**Example:**
```python
from careflow.processors import ClinicalSummarizer

summarizer = ClinicalSummarizer()
result = summarizer.summarize("Patient presents with...")
print(result['summary'])
```

###### `get_key_points(clinical_text: str) -> list`

Extract key points from clinical text.

**Parameters:**
- `clinical_text` (str): Raw clinical text input

**Returns:**
- `list`: List of key point strings (max 5)

**Example:**
```python
key_points = summarizer.get_key_points("Patient presents with...")
for point in key_points:
    print(f"- {point}")
```

---

### SOAPGenerator

Generates structured SOAP notes from clinical text.

#### Class: `SOAPGenerator`

##### Methods

###### `generate_soap(clinical_text: str) -> Dict[str, str]`

Generate a draft SOAP note from clinical text.

**Parameters:**
- `clinical_text` (str): Raw clinical text input

**Returns:**
- `dict`: Dictionary containing:
  - `subjective` (str): Subjective findings
  - `objective` (str): Objective findings
  - `assessment` (str): Clinical assessment
  - `plan` (str): Treatment plan
  - `status` (str): Processing status

**Example:**
```python
from careflow.processors import SOAPGenerator

generator = SOAPGenerator()
soap = generator.generate_soap("Patient presents with...")
print(f"S: {soap['subjective']}")
print(f"O: {soap['objective']}")
print(f"A: {soap['assessment']}")
print(f"P: {soap['plan']}")
```

###### `validate_soap(soap_note: Dict[str, str]) -> Dict[str, bool]`

Validate SOAP note completeness.

**Parameters:**
- `soap_note` (dict): SOAP note dictionary

**Returns:**
- `dict`: Validation results for each section (True/False)

**Example:**
```python
validation = generator.validate_soap(soap)
for section, is_valid in validation.items():
    print(f"{section}: {'✓' if is_valid else '✗'}")
```

---

### WorkflowSuggester

Provides workflow suggestions for documentation support.

#### Class: `WorkflowSuggester`

##### Methods

###### `suggest_workflows(clinical_text: str) -> Dict[str, List[str]]`

Generate workflow suggestions based on clinical text.

**Parameters:**
- `clinical_text` (str): Raw clinical text input

**Returns:**
- `dict`: Dictionary containing:
  - `suggestions` (list): General workflow suggestions
  - `priority_items` (list): High-priority action items
  - `documentation_checklist` (list): Documentation checklist items
  - `status` (str): Processing status

**Example:**
```python
from careflow.processors import WorkflowSuggester

suggester = WorkflowSuggester()
workflows = suggester.suggest_workflows("Patient presents with...")
for suggestion in workflows['suggestions']:
    print(f"- {suggestion}")
```

###### `get_documentation_reminders() -> List[str]`

Get general documentation reminders.

**Returns:**
- `list`: List of documentation best practices

**Example:**
```python
reminders = suggester.get_documentation_reminders()
for reminder in reminders:
    print(f"• {reminder}")
```

---

## Utility Functions

### text_utils

Text processing and manipulation utilities.

#### Functions

##### `clean_text(text: str) -> str`

Clean and normalize clinical text input.

**Parameters:**
- `text` (str): Raw text input

**Returns:**
- `str`: Cleaned text

**Example:**
```python
from careflow.utils import clean_text

cleaned = clean_text("  Patient   presents\n\nwith...  ")
```

##### `extract_key_terms(text: str) -> List[str]`

Extract potentially relevant clinical terms.

**Parameters:**
- `text` (str): Clinical text

**Returns:**
- `list`: List of key terms (max 20)

##### `truncate_text(text: str, max_length: int = 200, add_ellipsis: bool = True) -> str`

Truncate text to specified length.

##### `count_words(text: str) -> int`

Count words in text.

##### `split_into_sentences(text: str) -> List[str]`

Split text into sentences.

---

### validators

Input validation utilities.

#### Functions

##### `validate_clinical_text(text: str) -> Tuple[bool, str]`

Validate clinical text input.

**Parameters:**
- `text` (str): Clinical text to validate

**Returns:**
- `tuple`: (is_valid: bool, error_message: str)

**Example:**
```python
from careflow.utils import validate_clinical_text

is_valid, error = validate_clinical_text(user_input)
if not is_valid:
    print(f"Error: {error}")
```

##### `validate_text_length(text: str, min_length: int = 10, max_length: int = 50000) -> bool`

Validate text length.

##### `check_text_quality(text: str) -> Dict[str, any]`

Check quality metrics for clinical text.

**Returns:**
- `dict`: Quality metrics including:
  - `has_content` (bool)
  - `word_count` (int)
  - `sentence_count` (int)
  - `avg_sentence_length` (float)
  - `quality_score` (int): 0-100

---

## Usage Examples

### Complete Workflow

```python
from careflow import ClinicalSummarizer, SOAPGenerator, WorkflowSuggester
from careflow.utils import validate_clinical_text, clean_text

# Input text
clinical_text = """
Patient is a 45-year-old male presenting with chest discomfort...
"""

# Validate
is_valid, error = validate_clinical_text(clinical_text)
if not is_valid:
    print(f"Validation error: {error}")
    exit(1)

# Clean
cleaned_text = clean_text(clinical_text)

# Process
summarizer = ClinicalSummarizer()
soap_gen = SOAPGenerator()
workflow = WorkflowSuggester()

# Get results
summary = summarizer.summarize(cleaned_text)
soap = soap_gen.generate_soap(cleaned_text)
suggestions = workflow.suggest_workflows(cleaned_text)

# Display
print("Summary:", summary['summary'])
print("\nSOAP Note:")
print("S:", soap['subjective'])
print("O:", soap['objective'])
print("A:", soap['assessment'])
print("P:", soap['plan'])
print("\nWorkflow Suggestions:")
for s in suggestions['suggestions']:
    print(f"- {s}")
```

### Custom Processing

```python
from careflow.processors import ClinicalSummarizer

# Custom configuration
summarizer = ClinicalSummarizer()
summarizer.max_summary_length = 300  # Customize

# Process multiple texts
texts = ["text1...", "text2...", "text3..."]
summaries = [summarizer.summarize(t) for t in texts]

# Batch key points
all_key_points = []
for text in texts:
    points = summarizer.get_key_points(text)
    all_key_points.extend(points)
```

---

## Error Handling

All processors handle errors gracefully and return status indicators:

```python
result = summarizer.summarize(text)
if result['status'] == 'empty':
    print("No text provided")
elif result['status'] == 'error':
    print("Processing error occurred")
elif result['status'] == 'success':
    print("Success:", result['summary'])
```

---

## Extension Points

### Custom Processors

Create custom processors by following the existing patterns:

```python
class CustomProcessor:
    """Custom clinical text processor."""
    
    def __init__(self):
        """Initialize processor."""
        pass
    
    def process(self, text: str) -> dict:
        """Process clinical text."""
        # Implementation
        return {"result": "...", "status": "success"}
```

### Custom Validators

Add custom validation logic:

```python
def validate_custom_requirement(text: str) -> bool:
    """Custom validation."""
    # Implementation
    return True
```

---

## Configuration

Processors use default configurations but can be customized:

```python
# Via config.py
from app.config import Config

Config.MAX_SUMMARY_LENGTH = 1000
Config.ENABLE_WORKFLOW = False
```

---

## Notes

- All functions handle empty/None inputs gracefully
- Text cleaning is automatic in most processors
- Validation is recommended before processing
- All outputs should be manually reviewed
- Extensible architecture allows easy customization

---

For more information, see the main [README](README.md) and source code documentation.
