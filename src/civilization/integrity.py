from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    severity: str
    message: str


class HistoricalIntegrityEngine:
    @staticmethod
    def detect_anachronism(person_lived_until: int, technology_introduced: int, relationship: str):
        if technology_introduced > person_lived_until:
            return IntegrityIssue(
                "ANACHRONISM", "ERROR",
                f"{relationship} is temporally impossible for the stated lifetime.",
            )
        return None

    @staticmethod
    def validate_claim_evidence(claims) -> list[IntegrityIssue]:
        issues = []
        for claim in claims:
            if claim.claim_type == "FACT" and not claim.evidence_ids:
                issues.append(IntegrityIssue(
                    "UNSUPPORTED_CLAIM", "ERROR",
                    f"Claim {claim.claim_id} is marked FACT without evidence.",
                ))
        return issues

    @staticmethod
    def validate_knowledge_record(record) -> list[IntegrityIssue]:
        issues = [
            IntegrityIssue("KNOWLEDGE_RECORD_INVALID", "ERROR", error)
            for error in record.validate()
        ]
        if not record.evidence:
            issues.append(IntegrityIssue(
                "MISSING_EVIDENCE", "ERROR",
                f"Record {record.record_id} has no evidence.",
            ))
        if record.spatial_context is None:
            issues.append(IntegrityIssue(
                "MISSING_SPATIAL_CONTEXT", "WARNING",
                f"Record {record.record_id} has no spatial context.",
            ))
        return issues
