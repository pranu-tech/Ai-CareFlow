"""Tests for utility functions."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from careflow.utils.text_utils import (
    clean_text, extract_key_terms, truncate_text, 
    count_words, split_into_sentences
)
from careflow.utils.validators import (
    validate_clinical_text, validate_text_length, check_text_quality
)


class TestTextUtils:
    """Tests for text utility functions."""
    
    def test_clean_text_empty(self):
        """Test clean_text with empty input."""
        result = clean_text("")
        assert result == ""
    
    def test_clean_text_whitespace(self):
        """Test clean_text removes extra whitespace."""
        text = "Text   with    extra    spaces"
        result = clean_text(text)
        assert "   " not in result
        assert result == "Text with extra spaces"
    
    def test_extract_key_terms(self):
        """Test key terms extraction."""
        text = "BP 120/80, HR 72 bpm, Temperature 98.6°F"
        terms = extract_key_terms(text)
        assert isinstance(terms, list)
    
    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a long text " * 20
        result = truncate_text(text, max_length=50)
        assert len(result) <= 53  # 50 + '...'
    
    def test_count_words(self):
        """Test word counting."""
        text = "This is a test sentence"
        count = count_words(text)
        assert count == 5
    
    def test_split_into_sentences(self):
        """Test sentence splitting."""
        text = "First sentence. Second sentence! Third sentence?"
        sentences = split_into_sentences(text)
        assert len(sentences) == 3


class TestValidators:
    """Tests for validation functions."""
    
    def test_validate_clinical_text_empty(self):
        """Test validation with empty text."""
        is_valid, error = validate_clinical_text("")
        assert not is_valid
        assert "empty" in error.lower()
    
    def test_validate_clinical_text_too_short(self):
        """Test validation with too short text."""
        is_valid, error = validate_clinical_text("Short")
        assert not is_valid
        assert "short" in error.lower()
    
    def test_validate_clinical_text_valid(self):
        """Test validation with valid text."""
        text = "This is a valid clinical text with enough content."
        is_valid, error = validate_clinical_text(text)
        assert is_valid
        assert error == ""
    
    def test_validate_text_length(self):
        """Test text length validation."""
        text = "Valid length text"
        assert validate_text_length(text, min_length=5, max_length=100)
        assert not validate_text_length(text, min_length=50, max_length=100)
    
    def test_check_text_quality(self):
        """Test text quality checking."""
        text = "This is a test. It has multiple sentences. Quality should be good."
        quality = check_text_quality(text)
        assert 'word_count' in quality
        assert 'sentence_count' in quality
        assert 'quality_score' in quality
        assert quality['has_content']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
