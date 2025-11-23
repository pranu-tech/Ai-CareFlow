"""SOAP note generation module."""

from typing import Dict, Optional


class SOAPGenerator:
    """
    Generates draft SOAP notes (Subjective, Objective, Assessment, Plan).
    
    This is a starter implementation that provides basic SOAP note structure.
    Future enhancements can integrate AI/ML models for intelligent extraction.
    """
    
    def __init__(self):
        """Initialize the SOAP note generator."""
        self.subjective_keywords = [
            'complaint', 'reports', 'states', 'denies', 'feels', 
            'describes', 'history', 'patient says', 'patient reports'
        ]
        self.objective_keywords = [
            'vital signs', 'temperature', 'blood pressure', 'pulse', 'respiratory rate',
            'examination', 'observed', 'appears', 'findings', 'lab results', 'test'
        ]
        self.assessment_keywords = [
            'diagnosis', 'assessment', 'impression', 'condition', 'likely', 'possible'
        ]
        self.plan_keywords = [
            'plan', 'treatment', 'medication', 'prescribe', 'recommend', 
            'follow-up', 'referral', 'continue', 'start', 'discontinue'
        ]
    
    def generate_soap(self, clinical_text: str) -> Dict[str, str]:
        """
        Generate a draft SOAP note from clinical text.
        
        Args:
            clinical_text: Raw clinical text input
            
        Returns:
            Dictionary containing SOAP note sections
        """
        if not clinical_text or not clinical_text.strip():
            return {
                "subjective": "No clinical information provided.",
                "objective": "No clinical information provided.",
                "assessment": "No clinical information provided.",
                "plan": "No clinical information provided.",
                "status": "empty"
            }
        
        sentences = [s.strip() for s in clinical_text.split('.') if s.strip()]
        
        soap_note = {
            "subjective": self._extract_section(sentences, self.subjective_keywords, "S"),
            "objective": self._extract_section(sentences, self.objective_keywords, "O"),
            "assessment": self._extract_section(sentences, self.assessment_keywords, "A"),
            "plan": self._extract_section(sentences, self.plan_keywords, "P"),
            "status": "success"
        }
        
        return soap_note
    
    def _extract_section(self, sentences: list, keywords: list, section_label: str) -> str:
        """
        Extract sentences matching section keywords.
        
        Args:
            sentences: List of sentences from clinical text
            keywords: Keywords to match for this section
            section_label: Section label (S, O, A, P)
            
        Returns:
            Formatted section text
        """
        matching_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                matching_sentences.append(sentence + '.')
        
        if not matching_sentences:
            return f"[{section_label}] No specific information identified. Please review and complete manually."
        
        # Limit to 3 most relevant sentences per section
        return ' '.join(matching_sentences[:3])
    
    def validate_soap(self, soap_note: Dict[str, str]) -> Dict[str, bool]:
        """
        Validate SOAP note completeness.
        
        Args:
            soap_note: SOAP note dictionary
            
        Returns:
            Dictionary with validation results for each section
        """
        required_sections = ["subjective", "objective", "assessment", "plan"]
        validation = {}
        
        for section in required_sections:
            content = soap_note.get(section, "")
            # Check if section has meaningful content (not just placeholder)
            validation[section] = (
                len(content) > 50 and 
                "No specific information" not in content
            )
        
        return validation
