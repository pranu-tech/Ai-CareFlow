"""Text processing utilities."""

import re
from typing import List, Set


def clean_text(text: str) -> str:
    """
    Clean and normalize clinical text input.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep medical notation
    # Keep: periods, commas, hyphens, slashes, parentheses
    text = re.sub(r'[^\w\s.,\-/()\':;]', '', text)
    
    # Normalize line breaks
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    return text.strip()


def extract_key_terms(text: str) -> List[str]:
    """
    Extract potentially relevant clinical terms from text.
    
    Args:
        text: Clinical text
        
    Returns:
        List of key terms
    """
    if not text:
        return []
    
    # Common clinical terms to look for (starter list)
    clinical_patterns = [
        r'\b\d+/\d+\b',  # Blood pressure
        r'\b\d+\s*bpm\b',  # Heart rate
        r'\b\d+\s*°[CF]\b',  # Temperature
        r'\b\d+\s*mg\b',  # Medication dosage
        r'\b\d+\s*mmHg\b',  # Pressure measurements
    ]
    
    key_terms = []
    text_lower = text.lower()
    
    # Extract pattern-based terms
    for pattern in clinical_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        key_terms.extend(matches)
    
    # Extract capitalized terms (potential proper nouns/medical terms)
    words = text.split()
    for word in words:
        # Look for words that are consistently capitalized (medical terms)
        if word and word[0].isupper() and len(word) > 3:
            key_terms.append(word.strip('.,;:'))
    
    # Remove duplicates while preserving order
    seen: Set[str] = set()
    unique_terms = []
    for term in key_terms:
        if term.lower() not in seen:
            seen.add(term.lower())
            unique_terms.append(term)
    
    return unique_terms[:20]  # Return top 20 terms


def truncate_text(text: str, max_length: int = 200, add_ellipsis: bool = True) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        add_ellipsis: Whether to add ellipsis
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    truncated = text[:max_length].rsplit(' ', 1)[0]
    if add_ellipsis:
        truncated += '...'
    
    return truncated


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count
        
    Returns:
        Word count
    """
    if not text:
        return 0
    return len(text.split())


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text: Text to split
        
    Returns:
        List of sentences
    """
    if not text:
        return []
    
    # Simple sentence splitting (can be enhanced with NLP libraries)
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]
