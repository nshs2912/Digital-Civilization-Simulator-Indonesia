import pytest
from src.civilization.ai import classify_answer_type, get_openai_api_key

def test_openai_key_is_read_from_secrets():
    assert get_openai_api_key({"OPENAI_API_KEY": "test-secret"}) == "test-secret"

def test_missing_key_fails_cleanly():
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        get_openai_api_key({})

def test_answer_type_whitelist():
    assert classify_answer_type("FACT") == "FACT"
    with pytest.raises(ValueError):
        classify_answer_type("MADE_UP")
