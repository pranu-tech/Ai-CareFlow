"""Validation utilities for clinical text."""

from typing import Any, Dict, Tuple


def validate_clinical_text(text: str) -> Tuple[bool, str]:
    """
    Validate clinical text input.
    
    Args:
        text: Clinical text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text:
        return False, "Text cannot be empty"
    
    if not text.strip():
        return False, "Text cannot be only whitespace"
    
    if len(text) < 10:
        return False, "Text is too short (minimum 10 characters)"
    
    if len(text) > 50000:
        return False, "Text is too long (maximum 50,000 characters)"
    
    return True, ""


def validate_text_length(text: str, min_length: int = 10, max_length: int = 50000) -> bool:
    """
    Validate text length.
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        True if valid
    """
    if not text:
        return False
    
    text_len = len(text.strip())
    return min_length <= text_len <= max_length


def check_text_quality(text: str) -> Dict[str, Any]:
    """
    Check quality metrics for clinical text.
    
    Args:
        text: Clinical text
        
    Returns:
        Dictionary with quality metrics
    """
    if not text:
        return {
            "has_content": False,
            "word_count": 0,
            "sentence_count": 0,
            "avg_sentence_length": 0,
            "quality_score": 0
        }
    
    words = text.split()
    sentences = [s for s in text.split('.') if s.strip()]
    
    word_count = len(words)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Simple quality scoring
    quality_score = 0
    if word_count >= 20:
        quality_score += 25
    if sentence_count >= 3:
        quality_score += 25
    if 10 <= avg_sentence_length <= 30:
        quality_score += 25
    if word_count <= 5000:  # Not too long
        quality_score += 25
    
    return {
        "has_content": True,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "quality_score": quality_score
    }
