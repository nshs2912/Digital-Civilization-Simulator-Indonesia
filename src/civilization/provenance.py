from dataclasses import dataclass


@dataclass(frozen=True)
class Provenance:
    provenance_id: str
    claim_id: str
    evidence_id: str
    source_id: str
    method: str
    created_by: str
    review_status: str
    created_at: str

    def validate(self) -> list[str]:
        errors: list[str] = []
        for name, value in (
            ("provenance_id", self.provenance_id),
            ("claim_id", self.claim_id),
            ("evidence_id", self.evidence_id),
            ("source_id", self.source_id),
            ("method", self.method),
            ("created_by", self.created_by),
            ("review_status", self.review_status),
            ("created_at", self.created_at),
        ):
            if not value:
                errors.append(f"{name} is required")
        return errors
