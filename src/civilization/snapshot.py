from dataclasses import dataclass
from typing import Any

from .graph import KnowledgeGraph


@dataclass(frozen=True)
class CivilizationSnapshot:
    civilization_id: str
    time: int
    place_id: str
    entity_ids: tuple[str, ...]
    relationship_count: int
    metadata: dict[str, Any]

    @classmethod
    def build(
        cls, graph: KnowledgeGraph, civilization_id: str, time: int, place_id: str
    ) -> "CivilizationSnapshot":
        relationships = [
            relationship
            for relationship in graph.relationships()
            if (relationship.valid_from is None or relationship.valid_from <= time)
            and (relationship.valid_to is None or time <= relationship.valid_to)
        ]
        return cls(
            civilization_id=civilization_id,
            time=time,
            place_id=place_id,
            entity_ids=graph.entity_ids(),
            relationship_count=len(relationships),
            metadata={"derived": True},
        )
