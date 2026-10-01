from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
    subject_id: str
    predicate: str
    object_id: Optional[str]
    claim_text: str
    claim_type: ClaimType
    lifecycle: ClaimLifecycle
    evidence_ids: tuple[str, ...] = ()
    confidence: Optional[float] = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.subject_id:
            errors.append("subject_id is required")
        if not self.predicate:
            errors.append("predicate is required")
        if not self.claim_text:
            errors.append("claim_text is required")
        if not 0 <= self.confidence <= 1 if self.confidence is not None else False:
            errors.append("confidence must be between 0 and 1")
        if self.claim_type == ClaimType.FACT and not self.evidence_ids:
            errors.append("FACT claims require evidence")
        return errors
