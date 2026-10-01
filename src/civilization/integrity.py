from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    severity: str
    message: str


class HistoricalIntegrityEngine:
    @staticmethod
    def _normalize(value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, Enum):
            return value.value
        return str(value).strip().upper()

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
        issues: list[IntegrityIssue] = []
        for claim in claims:
            claim_type = HistoricalIntegrityEngine._normalize(getattr(claim, "claim_type", ""))
            evidence_ids = getattr(claim, "evidence_ids", ()) or ()
            if claim_type == "FACT" and not evidence_ids:
                issues.append(
                    IntegrityIssue(
                        "UNSUPPORTED_CLAIM",
                        "ERROR",
                        f"Claim {claim.claim_id} is marked FACT without evidence.",
                    )
                )
        return issues

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
        strength = HistoricalIntegrityEngine._normalize(evidence_strength)
        if strength in {"INFERRED", "CONTEXTUAL"} and model_confidence > 0.95:
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
        if simulation and HistoricalIntegrityEngine._normalize(claim_type) == "FACT":
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
        if first_place_id and second_place_id and str(first_place_id).strip() != str(second_place_id).strip():
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
            for error in getattr(record, "validate", lambda: [])()
        ]
        if not getattr(record, "evidence", ()):
            issues.append(
                IntegrityIssue(
                    "MISSING_EVIDENCE",
                    "ERROR",
                    f"Record {record.record_id} has no evidence.",
                )
            )
        if getattr(record, "spatial_context", None) is None:
            issues.append(
                IntegrityIssue(
                    "MISSING_SPATIAL_CONTEXT",
                    "WARNING",
                    f"Record {record.record_id} has no spatial context.",
                )
            )
        return issues
