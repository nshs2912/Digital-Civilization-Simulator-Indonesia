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
    time_context: TimeContext | None
    spatial_context: SpatialContext | None
    evidence: tuple[Evidence, ...]
    sources: tuple[Source, ...]
    provenance: tuple[Provenance, ...]
    metadata: dict[str, Any]

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.record_id or not str(self.record_id).strip():
            errors.append("record_id is required")
        if not self.claim_id or not str(self.claim_id).strip():
            errors.append("claim_id is required")
        if self.time_context is None:
            errors.append("time_context is required")
        else:
            errors.extend(f"time: {error}" for error in self.time_context.validate())
        if self.spatial_context is not None:
            errors.extend(f"spatial: {error}" for error in self.spatial_context.validate())

        evidence = self.evidence or ()
        sources = self.sources or ()
        evidence_ids = {item.evidence_id for item in evidence}
        source_ids = {item.source_id for item in sources if getattr(item, "source_id", None)}

        for item in evidence:
            errors.extend(f"evidence: {error}" for error in item.validate())
            missing = set(item.source_ids) - source_ids
            if missing:
                errors.append(
                    f"evidence {item.evidence_id} references missing sources: {sorted(missing)}"
                )

        for item in self.provenance or ():
            errors.extend(f"provenance: {error}" for error in item.validate())
            if item.claim_id != self.claim_id:
                errors.append(
                    f"provenance {item.provenance_id} points to another claim"
                )
            if item.evidence_id not in evidence_ids:
                errors.append(
                    f"provenance {item.provenance_id} references missing evidence"
                )
            if item.source_id not in source_ids:
                errors.append(
                    f"provenance {item.provenance_id} references missing source"
                )

        return errors
