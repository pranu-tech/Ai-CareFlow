"""Workflow suggestion module for documentation support."""

from typing import Dict, List, Optional


class WorkflowSuggester:
    """
    Provides simple workflow suggestions for clinical documentation.
    
    NOTE: This is for documentation support only - NOT for clinical diagnosis.
    All suggestions are non-diagnostic administrative workflow helpers.
    """
    
    def __init__(self):
        """Initialize the workflow suggester."""
        self.documentation_triggers = {
            'incomplete_history': [
                'history', 'allergies', 'medications', 'surgical history'
            ],
            'missing_vitals': [
                'vital signs', 'blood pressure', 'temperature', 'pulse', 'respiratory rate'
            ],
            'follow_up_needed': [
                'follow-up', 'recheck', 'return', 'monitor', 'reassess'
            ],
            'lab_work': [
                'lab', 'test', 'bloodwork', 'imaging', 'x-ray', 'mri', 'ct scan'
            ],
            'referral': [
                'specialist', 'referral', 'consult'
            ]
        }
    
    def suggest_workflows(self, clinical_text: str) -> Dict[str, List[str]]:
        """
        Generate workflow suggestions based on clinical text.
        
        Args:
            clinical_text: Raw clinical text input
            
        Returns:
            Dictionary containing workflow suggestions by category
        """
        if not clinical_text or not clinical_text.strip():
            return {
                "suggestions": [],
                "priority_items": [],
                "documentation_checklist": [],
                "status": "empty"
            }
        
        text_lower = clinical_text.lower()
        suggestions = []
        priority_items = []
        documentation_checklist = []
        
        # Check for incomplete documentation areas
        if self._check_triggers(text_lower, self.documentation_triggers['incomplete_history']):
            suggestions.append("Consider completing patient history section")
            priority_items.append("Review and complete: Medical history, allergies, current medications")
        
        if self._check_triggers(text_lower, self.documentation_triggers['missing_vitals']):
            suggestions.append("Ensure vital signs are documented")
            documentation_checklist.append("Vital signs: BP, Temp, Pulse, RR, O2 sat")
        
        if self._check_triggers(text_lower, self.documentation_triggers['follow_up_needed']):
            suggestions.append("Schedule follow-up appointment")
            priority_items.append("Set follow-up reminder and document timeframe")
        
        if self._check_triggers(text_lower, self.documentation_triggers['lab_work']):
            suggestions.append("Lab work or imaging mentioned - verify orders placed")
            documentation_checklist.append("Confirm test orders in system")
        
        if self._check_triggers(text_lower, self.documentation_triggers['referral']):
            suggestions.append("Referral mentioned - complete referral documentation")
            priority_items.append("Submit referral request with supporting documentation")
        
        # Add general documentation reminders
        documentation_checklist.extend([
            "Chief complaint documented",
            "Assessment and plan clearly stated",
            "Patient education provided",
            "Consent obtained if needed"
        ])
        
        return {
            "suggestions": suggestions if suggestions else ["Documentation appears complete. Review for accuracy."],
            "priority_items": priority_items,
            "documentation_checklist": documentation_checklist,
            "status": "success"
        }
    
    def _check_triggers(self, text: str, triggers: List[str]) -> bool:
        """
        Check if any trigger keywords are present in text.
        
        Args:
            text: Clinical text (lowercase)
            triggers: List of trigger keywords
            
        Returns:
            True if any trigger is found
        """
        return any(trigger in text for trigger in triggers)
    
    def get_documentation_reminders(self) -> List[str]:
        """
        Get general documentation reminders.
        
        Returns:
            List of documentation best practices
        """
        return [
            "Ensure all sections of the note are complete",
            "Verify patient demographics and identifiers",
            "Document time spent on patient care",
            "Review and sign note before finalizing",
            "Check for required quality metrics documentation",
            "Verify billing/coding information if applicable"
        ]
