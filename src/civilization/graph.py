from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Relationship:
    subject_id: str
    predicate: str
    object_id: str
    valid_from: int | None = None
    valid_to: int | None = None
    evidence_ids: tuple[str, ...] = ()
    model_confidence: float | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.subject_id or not self.object_id:
            errors.append("relationship endpoints are required")
        if not self.predicate:
            errors.append("predicate is required")
        if self.valid_from is not None and self.valid_to is not None:
            if self.valid_to < self.valid_from:
                errors.append("valid_to cannot precede valid_from")
        if self.model_confidence is not None and not 0 <= self.model_confidence <= 1:
            errors.append("model_confidence must be between 0 and 1")
        return errors


class KnowledgeGraph:
    def __init__(self) -> None:
        self._entities: dict[str, object] = {}
        self._relationships: list[Relationship] = []

    def add_entity(self, entity: object) -> None:
        entity_id = getattr(entity, "entity_id", None)
        if not entity_id:
            raise ValueError("entity must have an entity_id")
        if entity_id in self._entities:
            raise ValueError(f"duplicate entity_id: {entity_id}")
        self._entities[entity_id] = entity

    def add_relationship(self, relationship: Relationship) -> None:
        if relationship.validate():
            raise ValueError("; ".join(relationship.validate()))
        if relationship.subject_id not in self._entities:
            raise KeyError(f"unknown subject: {relationship.subject_id}")
        if relationship.object_id not in self._entities:
            raise KeyError(f"unknown object: {relationship.object_id}")
        self._relationships.append(relationship)

    def entity(self, entity_id: str) -> object:
        return self._entities[entity_id]

    def relationships(self) -> tuple[Relationship, ...]:
        return tuple(self._relationships)

    def neighbors(self, entity_id: str) -> tuple[Relationship, ...]:
        return tuple(
            r for r in self._relationships
            if r.subject_id == entity_id or r.object_id == entity_id
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        errors.extend(
            f"ENTITY:{entity_id}:{error}"
            for entity_id, entity in self._entities.items()
            for error in getattr(entity, "validate", lambda: [])()
        )
        errors.extend(
            f"RELATIONSHIP:{i}:{error}"
            for i, relationship in enumerate(self._relationships)
            for error in relationship.validate()
        )
        return errors
