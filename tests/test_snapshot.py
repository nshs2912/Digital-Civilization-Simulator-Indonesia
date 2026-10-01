from src.civilization.entities import Entity, EntityType
from src.civilization.graph import KnowledgeGraph, Relationship
from src.civilization.snapshot import CivilizationSnapshot


def test_snapshot_is_derived_from_graph_state():
    graph = KnowledgeGraph()
    graph.add_entity(Entity("place:borobudur", EntityType.PLACE, "Borobudur"))
    graph.add_entity(Entity("period:1", EntityType.HISTORICAL_PERIOD, "Historical period"))
    graph.add_relationship(
        Relationship("place:borobudur", "ASSOCIATED_WITH", "period:1", valid_from=750, valid_to=850)
    )

    snapshot = CivilizationSnapshot.build(graph, "civilization:nusantara", 800, "place:borobudur")
    assert snapshot.relationship_count == 1
    assert snapshot.metadata["derived"] is True
