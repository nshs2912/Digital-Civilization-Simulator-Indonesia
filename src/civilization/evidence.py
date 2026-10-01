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
    evidence_type: EvidenceType | str
    strength: EvidenceStrength | str
    description: str
    source_ids: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.evidence_id or not str(self.evidence_id).strip():
            errors.append("evidence_id is required")
        if not self.description or not str(self.description).strip():
            errors.append("description is required")
        if not self.source_ids:
            errors.append("evidence must reference at least one source")
        return errors
