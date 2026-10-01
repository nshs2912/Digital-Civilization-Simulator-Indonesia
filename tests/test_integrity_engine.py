from src.civilization.claims import ClaimLifecycle, ClaimType, KnowledgeClaim
from src.civilization.integrity import detect_anachronism, validate_required_evidence

def test_fact_requires_evidence():
    claim = KnowledgeClaim(
        "person:1", "USED", "technology:1", "A person used a technology.",
        ClaimType.FACT, ClaimLifecycle.REVIEWED,
    )
    issues = validate_required_evidence([claim])
    assert issues[0].code == "CLAIM_INVALID"

def test_anachronism_is_detected():
    issue = detect_anachronism(
        person_lived_until=800,
        technology_introduced=1000,
        relationship="USED",
    )
    assert issue is not None
    assert issue.code == "ANACHRONISM"

def test_valid_claim_with_evidence():
    claim = KnowledgeClaim(
        "place:borobudur", "ASSOCIATED_WITH", "period:1",
        "Borobudur is associated with a historical period.",
        ClaimType.FACT, ClaimLifecycle.SUPPORTED, ("evidence:1",), 0.9,
    )
    assert validate_required_evidence([claim]) == []
