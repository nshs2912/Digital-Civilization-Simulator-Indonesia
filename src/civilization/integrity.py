from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    severity: str
    message: str


class HistoricalIntegrityEngine:
    @staticmethod
    def detect_anachronism(
        person_lived_until: int,
        technology_introduced: int,
        relationship: str,
    ) -> IntegrityIssue | None:
        if technology_introduced > person_lived_until:
            return IntegrityIssue(
                "ANACHRONISM",
                "ERROR",
                f"{relationship} is temporally impossible for the stated lifetime.",
            )
        return None

    @staticmethod
    def validate_claim_evidence(claims) -> list[IntegrityIssue]:
        return [
            IntegrityIssue(
                "UNSUPPORTED_CLAIM",
                "ERROR",
                f"Claim {claim.claim_id} is marked FACT without evidence.",
            )
            for claim in claims
            if claim.claim_type == "FACT" and not claim.evidence_ids
        ]

    @staticmethod
    def validate_temporal_range(
        valid_from: int | None,
        valid_to: int | None,
        label: str,
    ) -> list[IntegrityIssue]:
        if valid_from is not None and valid_to is not None and valid_to < valid_from:
            return [
                IntegrityIssue(
                    "TEMPORAL_CONFLICT",
                    "ERROR",
                    f"{label} has valid_to earlier than valid_from.",
                )
            ]
        return []

    @staticmethod
    def validate_confidence(
        evidence_strength: str,
        model_confidence: float | None,
        label: str,
    ) -> list[IntegrityIssue]:
        if model_confidence is None:
            return []
        if not 0 <= model_confidence <= 1:
            return [
                IntegrityIssue(
                    "CONFIDENCE_MISMATCH",
                    "ERROR",
                    f"{label} has model confidence outside 0..1.",
                )
            ]
        if evidence_strength in {"INFERRED", "CONTEXTUAL"} and model_confidence > 0.95:
            return [
                IntegrityIssue(
                    "CONFIDENCE_MISMATCH",
                    "WARNING",
                    f"{label} has very high model confidence for non-direct evidence.",
                )
            ]
        return []

    @staticmethod
    def validate_simulation_boundary(
        claim_type: str,
        simulation: bool,
        label: str,
    ) -> list[IntegrityIssue]:
        if simulation and claim_type == "FACT":
            return [
                IntegrityIssue(
                    "SIMULATION_AS_FACT",
                    "ERROR",
                    f"{label} is marked FACT but originates from simulation.",
                )
            ]
        return []

    @staticmethod
    def validate_spatial_pair(
        first_place_id: str | None,
        second_place_id: str | None,
        label: str,
    ) -> list[IntegrityIssue]:
        if first_place_id and second_place_id and first_place_id != second_place_id:
            return [
                IntegrityIssue(
                    "SPATIAL_CONFLICT",
                    "WARNING",
                    f"{label} references different spatial contexts.",
                )
            ]
        return []

    @staticmethod
    def validate_knowledge_record(record) -> list[IntegrityIssue]:
        issues = [
            IntegrityIssue("KNOWLEDGE_RECORD_INVALID", "ERROR", error)
            for error in record.validate()
        ]
        if not record.evidence:
            issues.append(
                IntegrityIssue(
                    "MISSING_EVIDENCE",
                    "ERROR",
                    f"Record {record.record_id} has no evidence.",
                )
            )
        if record.spatial_context is None:
            issues.append(
                IntegrityIssue(
                    "MISSING_SPATIAL_CONTEXT",
                    "WARNING",
                    f"Record {record.record_id} has no spatial context.",
                )
            )
        return issues
