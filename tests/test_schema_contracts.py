import json
from pathlib import Path

SCHEMA_DIR = Path(__file__).parents[1] / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def test_knowledge_record_schema_requires_typed_provenance():
    schema = load_schema("knowledge_record.schema.json")
    assert schema["properties"]["evidence"]["items"]["$ref"] == "evidence.schema.json"
    assert schema["properties"]["sources"]["items"]["$ref"] == "source.schema.json"
    assert schema["properties"]["provenance"]["items"]["$ref"] == "provenance.schema.json"
    assert schema["properties"]["evidence"]["minItems"] == 1


def test_supporting_schemas_are_strict_objects():
    for name in ("evidence.schema.json", "source.schema.json", "provenance.schema.json"):
        schema = load_schema(name)
        assert schema["type"] == "object"
        assert schema["additionalProperties"] is False
