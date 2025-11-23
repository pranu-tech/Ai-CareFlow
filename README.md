# Ai-CareFlow

AI-powered healthcare documentation & workflow assistant designed to reduce administrative burden, streamline clinical note writing, and alleviate clinician burnout.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚠️ Important Notice

**This tool is for demonstration and educational purposes only.**
- Use synthetic/test data only
- NOT for clinical diagnosis or medical advice
- NOT for real patient data
- All outputs require manual review and verification
- Not a substitute for clinical expertise

## Features

🩺 **Clinical Summarization** - Generate concise summaries from clinical text  
📋 **SOAP Note Generation** - Automatically structure notes into Subjective, Objective, Assessment, Plan format  
📌 **Workflow Suggestions** - Get non-diagnostic documentation workflow recommendations  
✅ **Quality Validation** - Text quality metrics and SOAP note completeness checks  
🎨 **Clean UI** - User-friendly Streamlit interface  
🔧 **Modular Architecture** - Extensible and maintainable codebase  

## Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pranu-tech/Ai-CareFlow.git
cd Ai-CareFlow
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit web application:
```bash
streamlit run app/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Usage

1. Enter or paste synthetic clinical text into the input area
2. Click "Load Sample Clinical Note" to try with demo data
3. Select which outputs to generate (Summary, SOAP, Workflow)
4. Click "Process Text" to analyze
5. Review the generated outputs

## Project Structure

```
Ai-CareFlow/
├── app/                    # Web application
│   ├── streamlit_app.py   # Main Streamlit UI
│   └── config.py          # Configuration
├── src/                    # Source code
│   └── careflow/
│       ├── processors/     # Core processing modules
│       │   ├── clinical_summarizer.py
│       │   ├── soap_generator.py
│       │   └── workflow_suggester.py
│       └── utils/          # Utilities
│           ├── text_utils.py
│           └── validators.py
├── data/                   # Sample data
├── tests/                  # Tests
├── docs/                   # Documentation
│   ├── README.md          # Detailed documentation
│   └── API.md             # API reference
├── requirements.txt        # Dependencies
└── setup.py               # Package setup
```

## Documentation

- [Detailed Documentation](docs/README.md) - Full setup and usage guide
- [API Reference](docs/API.md) - Complete API documentation
- [Sample Data](data/sample_notes.py) - Example synthetic clinical notes

## Development

### Code Quality

Format code:
```bash
black src/ app/ tests/
```

Lint code:
```bash
flake8 src/ app/ tests/
```

Type checking:
```bash
mypy src/
```

### Testing

Run tests:
```bash
pytest tests/
```

## Architecture

The application follows a modular, extensible architecture:

- **Processors**: Core business logic for text analysis
- **Utils**: Reusable utility functions
- **App**: User interface layer
- **Data**: Sample data and configurations

Each component is independent and can be extended or replaced.

## Future Enhancements

- Integration with AI/ML models (OpenAI, Anthropic, etc.)
- Advanced NER and entity extraction
- Multi-language support
- Export to EHR formats
- Voice input transcription
- Enhanced security and compliance features

## Safety & Compliance

This is a **demonstration tool** designed for:
- Educational purposes
- Workflow concept demonstration
- Synthetic data processing

**NOT intended for:**
- Clinical diagnosis
- Real patient data
- Production healthcare environments
- Medical advice or treatment

Always ensure compliance with HIPAA, GDPR, and other relevant regulations in your jurisdiction.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and patterns
- All tests pass
- Documentation is updated
- Safety disclaimers are maintained

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/pranu-tech/Ai-CareFlow/issues)
- **Documentation**: See `docs/` directory
- **Examples**: See `data/sample_notes.py`

## Acknowledgments

This project aims to reduce clinician burnout by streamlining documentation workflows and administrative tasks, allowing healthcare professionals to focus more on patient care.

---

**Remember: This tool supports but does not replace clinical judgment. Always review and verify all outputs.**
