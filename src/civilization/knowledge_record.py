from dataclasses import dataclass
from typing import Any

from .evidence import Evidence
from .provenance import Provenance
from .source import Source
from .spatial import SpatialContext
from .temporal import TimeContext


@dataclass(frozen=True)
class HistoricalKnowledgeRecord:
    record_id: str
    claim_id: str
    time_context: TimeContext
    spatial_context: SpatialContext | None
    evidence: tuple[Evidence, ...]
    sources: tuple[Source, ...]
    provenance: tuple[Provenance, ...]
    metadata: dict[str, Any]

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.record_id:
            errors.append("record_id is required")
        if not self.claim_id:
            errors.append("claim_id is required")
        errors.extend(f"time: {e}" for e in self.time_context.validate())
        if self.spatial_context is not None:
            errors.extend(f"spatial: {e}" for e in self.spatial_context.validate())
        evidence_ids = {e.evidence_id for e in self.evidence}
        source_ids = {s.source_id for s in self.sources}
        for item in self.evidence:
            errors.extend(f"evidence: {e}" for e in item.validate())
            missing = set(item.source_ids) - source_ids
            if missing:
                errors.append(
                    f"evidence {item.evidence_id} references missing sources: {sorted(missing)}"
                )
        for item in self.provenance:
            errors.extend(f"provenance: {e}" for e in item.validate())
            if item.claim_id != self.claim_id:
                errors.append(f"provenance {item.provenance_id} points to another claim")
            if item.evidence_id not in evidence_ids:
                errors.append(f"provenance {item.provenance_id} references missing evidence")
            if item.source_id not in source_ids:
                errors.append(f"provenance {item.provenance_id} references missing source")
        return errors
