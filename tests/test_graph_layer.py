import pytest

from src.civilization.entities import Entity, EntityType
from src.civilization.graph import KnowledgeGraph, Relationship


def test_graph_rejects_duplicate_entity():
    graph = KnowledgeGraph()
    graph.add_entity(Entity("place:borobudur", EntityType.PLACE, "Borobudur"))
    with pytest.raises(ValueError, match="duplicate"):
        graph.add_entity(Entity("place:borobudur", EntityType.PLACE, "Borobudur"))


def test_graph_requires_known_relationship_endpoints():
    graph = KnowledgeGraph()
    graph.add_entity(Entity("place:borobudur", EntityType.PLACE, "Borobudur"))
    with pytest.raises(KeyError):
        graph.add_relationship(Relationship("place:borobudur", "LOCATED_AT", "place:missing"))


def test_graph_neighbors():
    graph = KnowledgeGraph()
    graph.add_entity(Entity("place:borobudur", EntityType.PLACE, "Borobudur"))
    graph.add_entity(Entity("period:sailendra", EntityType.HISTORICAL_PERIOD, "Sailendra period"))
    graph.add_relationship(
        Relationship(
            "place:borobudur", "ASSOCIATED_WITH", "period:sailendra",
            valid_from=750, valid_to=850, evidence_ids=("evidence:1",),
        )
    )
    assert len(graph.neighbors("place:borobudur")) == 1
    assert graph.validate() == []


def test_invalid_confidence_is_rejected():
    relationship = Relationship("a", "RELATED", "b", model_confidence=1.5)
    assert relationship.validate() == ["model_confidence must be between 0 and 1"]
