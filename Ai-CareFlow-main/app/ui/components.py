"""Reusable UI component definitions for AI CareFlow.

This module is intended to hold small, composable UI helpers that
`layout.py` or `main.py` can call into.

These are currently framework-agnostic placeholders; later they can be
wired to Streamlit or another front-end framework.
"""

from typing import Any, Dict, List, Optional


def make_alert_config(message: str, level: str = "info") -> Dict[str, str]:
    """Return a simple configuration dict for an alert/banner component.

    Parameters
    ----------
    message:
        Human-readable alert message.
    level:
        Severity level such as ``"info"``, ``"warning"``, or ``"error"``.
    """
    return {"message": message, "level": level}


def make_bullet_list(items: List[str]) -> List[str]:
    """Transform a list of strings into bullet-point-like entries.

    This does not render anything; it simply prepares the data so
    a downstream UI adapter can decide how to display it.
    """
    return [f"- {item}" for item in items]


def make_section_header(title: str, subtitle: Optional[str] = None) -> Dict[str, Any]:
    """Return a configuration dictionary for a section header.

    This keeps visual metadata (titles, subtitles) separate from the
    underlying rendering technology.
    """
    data: Dict[str, Any] = {"title": title}
    if subtitle is not None:
        data["subtitle"] = subtitle
    return data
