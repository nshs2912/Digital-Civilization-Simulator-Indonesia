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
    claim_type: ClaimType | str
    evidence_ids: tuple[str, ...] = ()
    confidence: float | None = None
    lifecycle: ClaimLifecycle = ClaimLifecycle.PROPOSED

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.claim_id or not str(self.claim_id).strip():
            errors.append("claim_id is required")
        if not self.subject_id or not str(self.subject_id).strip():
            errors.append("subject_id is required")
        if not self.predicate or not str(self.predicate).strip():
            errors.append("predicate is required")
        if not self.claim_text or not str(self.claim_text).strip():
            errors.append("claim_text is required")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            errors.append("confidence must be between 0 and 1")
        claim_type = self.claim_type.value if isinstance(self.claim_type, Enum) else str(self.claim_type).strip().upper()
        if claim_type == ClaimType.FACT.value and not self.evidence_ids:
            errors.append("FACT claims require evidence")
        return errors
