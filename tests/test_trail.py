import pytest

from waypoint.distance import Distance
from waypoint.trail import (
    Trail,
    DayHike,
    BackpackingRoute,
    TrailRun,
    GuidedDayHike,
    ElevationMixin,
    RatingMixin,
    RatedDayHike,
)


def make_day_hike(
    trail_id=1,
    name="Blue Mountain",
    distance=8,
    elevation_gain=250,
    difficulty="moderate",
):
    return DayHike(
        trail_id,
        name,
        Distance(distance, "km"),
        elevation_gain,
        difficulty,
    )


# ============================================================
# Week 7 functionality
# ============================================================


def test_trail_is_abstract():
    """Trail cannot be instantiated directly in Week 8."""

    with pytest.raises(TypeError):
        Trail(
            1,
            "Blue Mountain",
            Distance(8, "km"),
            250,
            "moderate",
        )


def test_trail_creation():
    """A concrete trail type can still be created."""

    trail = make_day_hike()

    assert trail.id == 1
    assert trail.name == "Blue Mountain"
    assert trail.distance.magnitude == 8
    assert trail.distance.unit == "km"
    assert trail.elevation_gain_m == 250
    assert trail.difficulty == "moderate"


def test_trail_rejects_invalid_difficulty():
    with pytest.raises(ValueError):
        DayHike(
            1,
            "Blue Mountain",
            Distance(8, "km"),
            250,
            "extreme",
        )


def test_set_difficulty_validates():
    trail = make_day_hike()

    trail.set_difficulty("hard")

    assert trail.difficulty == "hard"

    with pytest.raises(ValueError):
        trail.set_difficulty("extreme")


def test_negative_elevation_gain_is_rejected():
    with pytest.raises(ValueError):
        DayHike(
            1,
            "Blue Mountain",
            Distance(8, "km"),
            -100,
            "moderate",
        )


def test_from_dict_creates_trail():
    data = {
        "id": 10,
        "name": "API Trail",
        "distance": {
            "magnitude": 12.5,
            "unit": "km",
        },
        "elevation_gain_m": 400,
        "difficulty": "hard",
    }

    trail = DayHike.from_dict(data)

    assert trail.id == 10
    assert trail.name == "API Trail"
    assert trail.distance.magnitude == 12.5
    assert trail.distance.unit == "km"
    assert trail.elevation_gain_m == 400
    assert trail.difficulty == "hard"


def test_same_id_means_same_trail():
    trail1 = make_day_hike(
        trail_id=1,
        name="Trail A",
        distance=5,
    )

    trail2 = make_day_hike(
        trail_id=1,
        name="Trail B",
        distance=10,
    )

    assert trail1 == trail2


def test_different_ids_are_not_equal():
    trail1 = make_day_hike(
        trail_id=1,
        name="Trail A",
        distance=5,
    )

    trail2 = make_day_hike(
        trail_id=2,
        name="Trail B",
        distance=5,
    )

    assert trail1 != trail2


def test_default_unit_only_affects_new_trails():
    DayHike.set_default_unit("km")

    old_trail = DayHike(
        1,
        "Old Trail",
        10,
        100,
        "easy",
    )

    DayHike.set_default_unit("mi")

    new_trail = DayHike(
        2,
        "New Trail",
        10,
        100,
        "easy",
    )

    assert old_trail.distance.unit == "km"
    assert new_trail.distance.unit == "mi"

    # Reset the class default for other tests.
    DayHike.set_default_unit("km")


def test_invalid_default_unit_is_rejected():
    with pytest.raises(ValueError):
        DayHike.set_default_unit("meters")


# ============================================================
# WP-201 — Different trail types
# ============================================================


def test_day_hike_estimated_time():
    trail = DayHike(
        1,
        "Day Hike",
        Distance(8, "km"),
        200,
        "moderate",
    )

    assert trail.estimated_time() == 2


def test_backpacking_route_estimated_time():
    trail = BackpackingRoute(
        2,
        "Backpacking Route",
        Distance(12, "km"),
        500,
        "hard",
        3,
    )

    assert trail.estimated_time() == 4
    assert trail.days == 3


def test_trail_run_estimated_time():
    trail = TrailRun(
        3,
        "Trail Run",
        Distance(8, "km"),
        150,
        "moderate",
    )

    assert trail.estimated_time() == 1


def test_each_trail_type_has_summary():
    day_hike = DayHike(
        1,
        "Day Hike",
        Distance(8, "km"),
        200,
        "easy",
    )

    backpacking = BackpackingRoute(
        2,
        "Backpacking",
        Distance(12, "km"),
        500,
        "hard",
        3,
    )

    trail_run = TrailRun(
        3,
        "Trail Run",
        Distance(8, "km"),
        150,
        "moderate",
    )

    assert "Day hike" in day_hike.summary()
    assert "Backpacking route" in backpacking.summary()
    assert "Trail run" in trail_run.summary()


def test_subclass_missing_abstract_method_cannot_be_instantiated():
    class IncompleteTrail(Trail):
        def estimated_time(self):
            return 1

    with pytest.raises(TypeError):
        IncompleteTrail(
            1,
            "Incomplete",
            Distance(5, "km"),
            100,
            "easy",
        )


# ============================================================
# WP-203 — Multilevel inheritance and super()
# ============================================================


def test_guided_day_hike_extends_day_hike():
    trail = GuidedDayHike(
        1,
        "Guided Mountain",
        Distance(8, "km"),
        250,
        "moderate",
        "Sarah",
    )

    assert isinstance(trail, DayHike)
    assert isinstance(trail, Trail)
    assert trail.guide_name == "Sarah"


def test_guided_day_hike_uses_parent_summary():
    trail = GuidedDayHike(
        1,
        "Guided Mountain",
        Distance(8, "km"),
        250,
        "moderate",
        "Sarah",
    )

    summary = trail.summary()

    assert "Day hike" in summary
    assert "Guided Mountain" in summary
    assert "Sarah" in summary


# ============================================================
# WP-204 — Method overriding
# ============================================================


def test_trail_run_has_different_pacing_than_day_hike():
    day_hike = DayHike(
        1,
        "Trail",
        Distance(8, "km"),
        100,
        "easy",
    )

    trail_run = TrailRun(
        2,
        "Trail",
        Distance(8, "km"),
        100,
        "easy",
    )

    assert day_hike.estimated_time() == 2
    assert trail_run.estimated_time() == 1


# ============================================================
# WP-205 — Mixins
# ============================================================


def test_elevation_mixin_calculates_grade():
    trail = RatedDayHike(
        1,
        "Mountain",
        Distance(10, "km"),
        500,
        "hard",
        rating=4.5,
    )

    assert trail.grade_percent == 5


def test_rating_mixin_stores_rating():
    trail = RatedDayHike(
        1,
        "Mountain",
        Distance(10, "km"),
        500,
        "hard",
        rating=4.5,
    )

    assert trail.rating == 4.5


def test_rating_must_be_between_zero_and_five():
    with pytest.raises(ValueError):
        RatedDayHike(
            1,
            "Mountain",
            Distance(10, "km"),
            500,
            "hard",
            rating=6,
        )


def test_rated_day_hike_summary_uses_super():
    trail = RatedDayHike(
        1,
        "Mountain",
        Distance(10, "km"),
        500,
        "hard",
        rating=4.5,
    )

    summary = trail.summary()

    assert "Day hike" in summary
    assert "grade: 5.0%" in summary
    assert "rating: 4.5" in summary


def test_rated_day_hike_mro():
    mro = RatedDayHike.__mro__

    assert mro[0] is RatedDayHike
    assert ElevationMixin in mro
    assert RatingMixin in mro
    assert DayHike in mro
    assert Trail in mro
    assert object in mro