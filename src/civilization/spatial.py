from dataclasses import dataclass
from enum import Enum


class SpatialContextType(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    ARCHAEOLOGICAL = "ARCHAEOLOGICAL"
    CULTURAL_REGION = "CULTURAL_REGION"
    ADMINISTRATIVE = "ADMINISTRATIVE"


@dataclass(frozen=True)
class SpatialContext:
    place_id: str
    context_type: SpatialContextType | str
    latitude: float | None = None
    longitude: float | None = None
    geometry: str | None = None
    valid_from: int | None = None
    valid_to: int | None = None
    precision_meters: float | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.place_id or not str(self.place_id).strip():
            errors.append("place_id is required")
        if self.latitude is not None and not -90 <= self.latitude <= 90:
            errors.append("latitude out of range")
        if self.longitude is not None and not -180 <= self.longitude <= 180:
            errors.append("longitude out of range")
        if self.valid_from is not None and self.valid_to is not None and self.valid_to < self.valid_from:
            errors.append("valid_to cannot precede valid_from")
        if self.precision_meters is not None and self.precision_meters < 0:
            errors.append("precision_meters cannot be negative")
        return errors
