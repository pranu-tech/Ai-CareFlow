"""Tests for clinical text processors."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from careflow.processors.clinical_summarizer import ClinicalSummarizer
from careflow.processors.soap_generator import SOAPGenerator
from careflow.processors.workflow_suggester import WorkflowSuggester


class TestClinicalSummarizer:
    """Tests for ClinicalSummarizer."""
    
    def test_summarize_empty_text(self):
        """Test summarization with empty text."""
        summarizer = ClinicalSummarizer()
        result = summarizer.summarize("")
        assert result['status'] == 'empty'
        assert 'summary' in result
    
    def test_summarize_valid_text(self):
        """Test summarization with valid text."""
        summarizer = ClinicalSummarizer()
        text = "Patient presents with headache. Vital signs are normal. Diagnosis is tension headache."
        result = summarizer.summarize(text)
        assert result['status'] == 'success'
        assert len(result['summary']) > 0
        assert 'word_count' in result or 'original_word_count' in result
    
    def test_get_key_points(self):
        """Test key points extraction."""
        summarizer = ClinicalSummarizer()
        text = "Patient has a history of diabetes. Current complaint is fever. Assessment shows infection."
        points = summarizer.get_key_points(text)
        assert isinstance(points, list)
        assert len(points) <= 5


class TestSOAPGenerator:
    """Tests for SOAPGenerator."""
    
    def test_generate_soap_empty_text(self):
        """Test SOAP generation with empty text."""
        generator = SOAPGenerator()
        result = generator.generate_soap("")
        assert result['status'] == 'empty'
        assert 'subjective' in result
    
    def test_generate_soap_valid_text(self):
        """Test SOAP generation with valid text."""
        generator = SOAPGenerator()
        text = """Patient reports chest pain. Vital signs: BP 120/80. 
                  Assessment: likely cardiac. Plan: ECG and follow-up."""
        result = generator.generate_soap(text)
        assert result['status'] == 'success'
        assert 'subjective' in result
        assert 'objective' in result
        assert 'assessment' in result
        assert 'plan' in result
    
    def test_validate_soap(self):
        """Test SOAP note validation."""
        generator = SOAPGenerator()
        soap_note = {
            'subjective': 'Patient reports pain for 2 days with no relief from medication',
            'objective': 'BP 140/90, HR 80, Temp 98.6F, examination shows tenderness',
            'assessment': 'Likely muscular strain based on presentation and examination findings',
            'plan': 'Start NSAIDs, physical therapy referral, follow-up in one week'
        }
        validation = generator.validate_soap(soap_note)
        assert isinstance(validation, dict)
        assert 'subjective' in validation


class TestWorkflowSuggester:
    """Tests for WorkflowSuggester."""
    
    def test_suggest_workflows_empty_text(self):
        """Test workflow suggestions with empty text."""
        suggester = WorkflowSuggester()
        result = suggester.suggest_workflows("")
        assert result['status'] == 'empty'
        assert 'suggestions' in result
    
    def test_suggest_workflows_valid_text(self):
        """Test workflow suggestions with valid text."""
        suggester = WorkflowSuggester()
        text = "Patient needs follow-up. Lab work ordered. Referral to specialist required."
        result = suggester.suggest_workflows(text)
        assert result['status'] == 'success'
        assert 'suggestions' in result
        assert isinstance(result['suggestions'], list)
        assert 'priority_items' in result
        assert 'documentation_checklist' in result
    
    def test_get_documentation_reminders(self):
        """Test documentation reminders."""
        suggester = WorkflowSuggester()
        reminders = suggester.get_documentation_reminders()
        assert isinstance(reminders, list)
        assert len(reminders) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
