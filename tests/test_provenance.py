from src.civilization.provenance import Provenance


def test_provenance_requires_full_trace():
    item = Provenance(
        "prov:1", "claim:1", "evidence:1", "source:1",
        "manual_review", "reviewer", "REVIEWED", "2026-10-01",
    )
    assert item.validate() == []


def test_provenance_rejects_missing_source():
    item = Provenance(
        "prov:1", "claim:1", "evidence:1", "",
        "manual_review", "reviewer", "REVIEWED", "2026-10-01",
    )
    assert "source_id is required" in item.validate()
