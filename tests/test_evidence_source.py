from src.civilization.evidence import Evidence, EvidenceStrength, EvidenceType
from src.civilization.source import Source


def test_evidence_requires_source():
    evidence = Evidence(
        "evidence:1", EvidenceType.ARCHAEOLOGICAL,
        EvidenceStrength.DIRECT, "Material evidence", (),
    )
    assert "evidence must reference at least one source" in evidence.validate()


def test_source_has_provenance_fields():
    source = Source(
        "source:1", "Example source", author="Author",
        publication="Publisher", language="id", publication_year=2020,
    )
    assert source.validate() == []
