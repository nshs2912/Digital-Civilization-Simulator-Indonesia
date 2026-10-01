from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    severity: str
    message: str

def detect_anachronism(
    *,
    person_lived_until: int,
    technology_introduced: int,
    relationship: str,
) -> IntegrityIssue | None:
    if relationship == "USED" and technology_introduced > person_lived_until:
        return IntegrityIssue(
            code="ANACHRONISM",
            severity="ERROR",
            message="The relationship requires a technology after the person's recorded lifetime.",
        )
    return None

def validate_required_evidence(claims: Iterable[object]) -> list[IntegrityIssue]:
    issues: list[IntegrityIssue] = []
    for claim in claims:
        errors = claim.validate()
        for error in errors:
            issues.append(IntegrityIssue("CLAIM_INVALID", "ERROR", error))
    return issues
