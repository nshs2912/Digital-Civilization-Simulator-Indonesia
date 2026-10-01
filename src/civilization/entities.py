from dataclasses import dataclass
from enum import Enum
from typing import Any


class EntityType(str, Enum):
    CIVILIZATION = "Civilization"
    HISTORICAL_PERIOD = "HistoricalPeriod"
    PERSON = "Person"
    COMMUNITY = "Community"
    PLACE = "Place"
    EVENT = "Event"
    INSTITUTION = "Institution"
    CULTURE = "Culture"
    TECHNOLOGY = "Technology"
    ECONOMIC_ACTIVITY = "EconomicActivity"
    ARTIFACT = "Artifact"
    ENVIRONMENT = "Environment"
    CLAIM = "KnowledgeClaim"
    EVIDENCE = "Evidence"
    SOURCE = "Source"


@dataclass(frozen=True)
class Entity:
    entity_id: str
    entity_type: EntityType
    name: str
    metadata: dict[str, Any] | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.entity_id.strip():
            errors.append("entity_id is required")
        if not self.name.strip():
            errors.append("name is required")
        return errors
