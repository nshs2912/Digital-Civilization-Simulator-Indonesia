from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TimeContext:
    event_start: Optional[int] = None
    event_end: Optional[int] = None
    source_year: Optional[int] = None
    knowledge_year: Optional[int] = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.event_start is not None and self.event_end is not None:
            if self.event_end < self.event_start:
                errors.append("event_end cannot precede event_start")
        return errors
