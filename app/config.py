"""Configuration settings for Ai-CareFlow application."""

import os
from pathlib import Path


class Config:
    """Application configuration."""
    
    # Application settings
    APP_NAME = "Ai-CareFlow"
    APP_VERSION = "0.1.0"
    APP_DESCRIPTION = "Healthcare Documentation & Workflow Assistant"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    DOCS_DIR = BASE_DIR / "docs"
    
    # Text processing limits
    MIN_TEXT_LENGTH = 10
    MAX_TEXT_LENGTH = 50000
    MAX_SUMMARY_LENGTH = 500
    
    # Feature flags
    ENABLE_SUMMARY = True
    ENABLE_SOAP = True
    ENABLE_WORKFLOW = True
    
    # UI settings
    PAGE_TITLE = "Ai-CareFlow"
    PAGE_ICON = "🏥"
    LAYOUT = "wide"
    
    # Safety disclaimers
    SAFETY_DISCLAIMER = """
    ⚠️ IMPORTANT DISCLAIMERS:
    
    This tool is for documentation support only.
    NOT for clinical diagnosis or medical advice.
    
    - Use synthetic/test data only
    - For educational and demonstration purposes
    - All clinical decisions require professional judgment
    - Review and verify all outputs manually
    - Not a substitute for clinical expertise
    - Never use with real patient data
    """
    
    @classmethod
    def get_env(cls, key: str, default: any = None) -> any:
        """Get environment variable."""
        return os.getenv(key, default)
