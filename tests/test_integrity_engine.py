from src.civilization.claims import KnowledgeClaim
from src.civilization.integrity import HistoricalIntegrityEngine
from tests.test_knowledge_record import make_record


def test_detects_anachronism():
    issue = HistoricalIntegrityEngine.detect_anachronism(800, 900, "USED")
    assert issue is not None
    assert issue.code == "ANACHRONISM"


def test_valid_record_has_no_integrity_errors():
    issues = HistoricalIntegrityEngine.validate_knowledge_record(make_record())
    assert not [item for item in issues if item.severity == "ERROR"]


def test_fact_without_evidence_is_invalid():
    claim = KnowledgeClaim("claim:unsupported", "person:1", "LIVED_AT", "place:1",
                            "Person lived here", "FACT", (), 0.9)
    issues = HistoricalIntegrityEngine.validate_claim_evidence((claim,))
    assert issues[0].code == "UNSUPPORTED_CLAIM"
