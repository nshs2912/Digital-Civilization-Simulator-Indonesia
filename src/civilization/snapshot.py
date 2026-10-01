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
        entities = tuple(graph._entities.keys())
        relationships = [
            r for r in graph.relationships()
            if (r.valid_from is None or r.valid_from <= time)
            and (r.valid_to is None or time <= r.valid_to)
        ]
        return cls(
            civilization_id=civilization_id,
            time=time,
            place_id=place_id,
            entity_ids=entities,
            relationship_count=len(relationships),
            metadata={"derived": True},
        )
