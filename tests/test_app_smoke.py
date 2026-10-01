def test_streamlit_app_source_is_importable():
    from pathlib import Path

    app_path = Path(__file__).parents[1] / "app" / "app.py"
    source = app_path.read_text(encoding="utf-8")
    assert "import streamlit as st" in source
    assert "st.set_page_config" in source
