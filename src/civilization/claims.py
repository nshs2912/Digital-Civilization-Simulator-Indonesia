from dataclasses import dataclass
from enum import Enum


class ClaimType(str, Enum):
    FACT = "FACT"
    INTERPRETATION = "INTERPRETATION"
    HYPOTHESIS = "HYPOTHESIS"
    DISPUTED = "DISPUTED"
    UNKNOWN = "UNKNOWN"


class ClaimLifecycle(str, Enum):
    PROPOSED = "PROPOSED"
    EVIDENCE_ATTACHED = "EVIDENCE_ATTACHED"
    REVIEWED = "REVIEWED"
    SUPPORTED = "SUPPORTED"
    DISPUTED = "DISPUTED"
    REVISED = "REVISED"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class KnowledgeClaim:
    claim_id: str
    subject_id: str
    predicate: str
    object_id: str | None
    claim_text: str
    claim_type: ClaimType
    evidence_ids: tuple[str, ...] = ()
    confidence: float | None = None
    lifecycle: ClaimLifecycle = ClaimLifecycle.PROPOSED

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.claim_id:
            errors.append("claim_id is required")
        if not self.subject_id:
            errors.append("subject_id is required")
        if not self.predicate:
            errors.append("predicate is required")
        if not self.claim_text:
            errors.append("claim_text is required")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            errors.append("confidence must be between 0 and 1")
        if self.claim_type == ClaimType.FACT and not self.evidence_ids:
            errors.append("FACT claims require evidence")
        return errors
