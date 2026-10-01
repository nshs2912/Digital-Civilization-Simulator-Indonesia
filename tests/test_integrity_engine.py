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
    claim = KnowledgeClaim(
        "claim:unsupported",
        "person:1",
        "LIVED_AT",
        "place:1",
        "Person lived here",
        "FACT",
        (),
        0.9,
    )
    issues = HistoricalIntegrityEngine.validate_claim_evidence((claim,))
    assert issues[0].code == "UNSUPPORTED_CLAIM"


def test_detects_temporal_conflict():
    issues = HistoricalIntegrityEngine.validate_temporal_range(900, 800, "relationship")
    assert issues[0].code == "TEMPORAL_CONFLICT"


def test_detects_confidence_mismatch():
    issues = HistoricalIntegrityEngine.validate_confidence(
        "INFERRED", 0.99, "inferred claim"
    )
    assert issues[0].code == "CONFIDENCE_MISMATCH"
    assert issues[0].severity == "WARNING"


def test_blocks_simulation_as_fact():
    issues = HistoricalIntegrityEngine.validate_simulation_boundary(
        "FACT", True, "simulation result"
    )
    assert issues[0].code == "SIMULATION_AS_FACT"


def test_flags_spatial_conflict():
    issues = HistoricalIntegrityEngine.validate_spatial_pair(
        "place:borobudur", "place:prambanan", "claim"
    )
    assert issues[0].code == "SPATIAL_CONFLICT"
