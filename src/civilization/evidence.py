from dataclasses import dataclass
from enum import Enum


class EvidenceType(str, Enum):
    ARCHAEOLOGICAL = "ARCHAEOLOGICAL"
    EPIGRAPHIC = "EPIGRAPHIC"
    ARCHIVAL = "ARCHIVAL"
    LITERARY = "LITERARY"
    ORAL = "ORAL"
    SCIENTIFIC = "SCIENTIFIC"
    MATERIAL = "MATERIAL"
    DIGITAL = "DIGITAL"


class EvidenceStrength(str, Enum):
    DIRECT = "DIRECT"
    INDIRECT = "INDIRECT"
    CONTEXTUAL = "CONTEXTUAL"
    INFERRED = "INFERRED"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    evidence_type: EvidenceType
    strength: EvidenceStrength
    description: str
    source_ids: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.evidence_id:
            errors.append("evidence_id is required")
        if not self.description:
            errors.append("description is required")
        if not self.source_ids:
            errors.append("evidence must reference at least one source")
        return errors
