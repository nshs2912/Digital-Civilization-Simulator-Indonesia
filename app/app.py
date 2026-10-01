from pathlib import Path
import sys

import streamlit as st


# Streamlit Cloud executes this file from the app/ directory. Add the
# repository root explicitly so the civilization package is importable.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.civilization.ai import get_openai_api_key  # noqa: E402


st.set_page_config(
    page_title="Digital Civilization Simulator Indonesia",
    page_icon="🌏",
    layout="wide",
)

st.title("🌏 DIGITAL CIVILIZATION SIMULATOR INDONESIA")
st.caption("AI-Powered. Across Time. Experience the Civilization of Nusantara.")

with st.expander("🇮🇩 Bahasa Indonesia / 🇬🇧 English"):
    st.write(
        "Platform eksplorasi peradaban berbasis AI/ML, evidence, time, place, and simulation."
    )
    st.write("AI/ML-powered exploration of Nusantara civilization across time.")

st.info(
    "Foundation build: Civilization Ontology + Evidence + Integrity Engine + AI security."
)

try:
    openai_api_key = get_openai_api_key()
except RuntimeError:
    openai_api_key = None

if openai_api_key:
    st.success(
        "🟢 OpenAI API configured — Civilization AI is ready for the next integration stage."
    )
else:
    st.warning(
        "Configure OPENAI_API_KEY in Streamlit Secrets before enabling AI features."
    )

st.divider()
st.subheader("🧭 Civilization Platform / Platform Peradaban")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Evidence First", "ON")
    st.caption("Knowledge must remain traceable to evidence and sources.")

with col2:
    st.metric("Temporal Integrity", "ON")
    st.caption("Historical claims are checked against time context.")

with col3:
    st.metric("AI Security", "ON")
    st.caption("API credentials remain outside source code.")

st.caption(
    "🔐 API key status is displayed only as configured/not configured. "
    "The secret value is never shown."
)
