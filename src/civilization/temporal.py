from dataclasses import dataclass
from enum import Enum


class TemporalPrecision(str, Enum):
    EXACT = "EXACT"
    YEAR = "YEAR"
    RANGE = "RANGE"
    PERIOD = "PERIOD"
    APPROXIMATE = "APPROXIMATE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class TimeContext:
    event_start: int | None = None
    event_end: int | None = None
    source_year: int | None = None
    knowledge_year: int | None = None
    period_id: str | None = None
    calendar_system: str | None = None
    precision: TemporalPrecision | str = TemporalPrecision.UNKNOWN
    confidence: float | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.event_start is not None and self.event_end is not None and self.event_end < self.event_start:
            errors.append("event_end cannot precede event_start")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            errors.append("confidence must be between 0 and 1")
        precision = self.precision.value if isinstance(self.precision, Enum) else str(self.precision).upper()
        if precision == TemporalPrecision.PERIOD.value and not self.period_id:
            errors.append("PERIOD precision requires period_id")
        return errors

    def contains(self, year: int) -> bool:
        if year is None:
            return False
        if self.event_start is not None and self.event_end is not None:
            return self.event_start <= year <= self.event_end
        if self.event_start is not None:
            return year >= self.event_start
        if self.event_end is not None:
            return year <= self.event_end
        return False
