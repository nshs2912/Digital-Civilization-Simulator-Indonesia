from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_bilingual_foundation_exists():
    required = [
        "README.md",
        "docs/constitution/historical_constitution.id.md",
        "docs/constitution/historical_constitution.en.md",
        "docs/ontology/civilization_ontology.id.md",
        "docs/ontology/civilization_ontology.en.md",
    ]
    assert all((ROOT / p).is_file() for p in required)


def test_historical_period_and_time_model_are_documented():
    ontology = (ROOT / "docs/ontology/civilization_ontology.id.md").read_text()
    constitution = (ROOT / "docs/constitution/historical_constitution.id.md").read_text()
    assert "HistoricalPeriod" in ontology
    assert "Event Time" in constitution
    assert "Source Time" in constitution
    assert "Knowledge Time" in constitution


def test_evidence_and_model_confidence_are_separate():
    text = (ROOT / "docs/governance/evidence_policy.id.md").read_text()
    assert "Kekuatan evidence" in text
    assert "model confidence" in text
