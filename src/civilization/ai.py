from __future__ import annotations

from typing import Any

def get_openai_api_key(secrets: Any | None = None) -> str:
    """Read the key from Streamlit Secrets; never hard-code credentials."""
    if secrets is None:
        try:
            import streamlit as st
            secrets = st.secrets
        except Exception:
            secrets = {}
    key = secrets.get("OPENAI_API_KEY") if hasattr(secrets, "get") else None
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Add it to Streamlit Secrets."
        )
    return str(key)

def classify_answer_type(answer_type: str) -> str:
    allowed = {"FACT", "INTERPRETATION", "SIMULATION", "COUNTERFACTUAL", "UNKNOWN"}
    if answer_type not in allowed:
        raise ValueError(f"Unsupported answer type: {answer_type}")
    return answer_type
