from src.civilization.evidence import Evidence
from src.civilization.knowledge_record import HistoricalKnowledgeRecord
from src.civilization.provenance import Provenance
from src.civilization.source import Source
from src.civilization.spatial import SpatialContext, SpatialContextType
from src.civilization.temporal import TimeContext, TemporalPrecision


def make_record():
    source = Source("source:borobudur", "Archaeological Study", "Researcher",
                    "Publication", "1", "id", 2020, "citation", "archive")
    evidence = Evidence("evidence:1", "direct", "strong",
                        "inscription evidence", ("source:borobudur",))
    provenance = Provenance("prov:1", "claim:1", "evidence:1", "source:borobudur",
                            "manual_review", "reviewer", "REVIEWED", "2026-10-01")
    return HistoricalKnowledgeRecord(
        "record:1", "claim:1",
        TimeContext(event_start=800, event_end=850, precision=TemporalPrecision.RANGE),
        SpatialContext("place:borobudur", SpatialContextType.ARCHAEOLOGICAL),
        (evidence,), (source,), (provenance,), {"domain": "architecture"},
    )


def test_knowledge_record_validates_trace():
    assert make_record().validate() == []


def test_missing_source_is_detected():
    record = make_record()
    evidence = Evidence("evidence:2", "indirect", "moderate", "secondary", ("source:missing",))
    invalid = HistoricalKnowledgeRecord(record.record_id, record.claim_id, record.time_context,
                                        record.spatial_context, (evidence,), record.sources,
                                        record.provenance, record.metadata)
    assert any("missing sources" in item for item in invalid.validate())
