from src.civilization.spatial import SpatialContext, SpatialContextType
from src.civilization.temporal import TemporalPrecision, TimeContext


def test_temporal_range_validation():
    context = TimeContext(event_start=900, event_end=800)
    assert "event_end cannot precede event_start" in context.validate()


def test_period_requires_period_id():
    context = TimeContext(precision=TemporalPrecision.PERIOD)
    assert "PERIOD precision requires period_id" in context.validate()


def test_temporal_contains():
    context = TimeContext(event_start=750, event_end=850)
    assert context.contains(800)
    assert not context.contains(900)


def test_spatial_coordinates_are_validated():
    context = SpatialContext(
        "place:borobudur",
        SpatialContextType.ARCHAEOLOGICAL,
        latitude=-100,
    )
    assert "latitude out of range" in context.validate()


def test_historical_and_current_contexts_are_distinct():
    historical = SpatialContext(
        "place:borobudur",
        SpatialContextType.HISTORICAL,
    )
    current = SpatialContext(
        "place:borobudur",
        SpatialContextType.CURRENT,
    )
    assert historical.context_type != current.context_type
