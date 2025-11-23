"""Ai-CareFlow: Healthcare documentation and workflow assistant."""

__version__ = "0.1.0"
__author__ = "pranu"

from .processors.clinical_summarizer import ClinicalSummarizer
from .processors.soap_generator import SOAPGenerator
from .processors.workflow_suggester import WorkflowSuggester

__all__ = [
    "ClinicalSummarizer",
    "SOAPGenerator",
    "WorkflowSuggester",
]
