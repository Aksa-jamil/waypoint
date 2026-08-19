import pytest

from waypoint.distance import Distance
from waypoint.trail import Trail


def test_trail_creation():
    trail = Trail(
        1,
        "Blue Mountain",
        Distance(8, "km"),
        250,
        "moderate",
    )

    assert trail.id == 1
    assert trail.name == "Blue Mountain"
    assert trail.distance.magnitude == 8
    assert trail.distance.unit == "km"
    assert trail.elevation_gain_m == 250
    assert trail.difficulty == "moderate"


def test_trail_rejects_invalid_difficulty():
    with pytest.raises(ValueError):
        Trail(
            1,
            "Blue Mountain",
            Distance(8, "km"),
            250,
            "extreme",
        )


def test_set_difficulty_validates():
    trail = Trail(
        1,
        "Blue Mountain",
        Distance(8, "km"),
        250,
        "easy",
    )

    trail.set_difficulty("hard")

    assert trail.difficulty == "hard"


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

    trail = Trail.from_dict(data)

    assert trail.id == 10
    assert trail.name == "API Trail"
    assert trail.distance.magnitude == 12.5
    assert trail.distance.unit == "km"
    assert trail.elevation_gain_m == 400
    assert trail.difficulty == "hard"


def test_same_id_means_same_trail():
    trail1 = Trail(
        1,
        "Trail A",
        Distance(5, "km"),
        100,
        "easy",
    )

    trail2 = Trail(
        1,
        "Completely Different Trail",
        Distance(50, "mi"),
        900,
        "hard",
    )

    assert trail1 == trail2


def test_different_ids_are_not_equal():
    trail1 = Trail(
        1,
        "Trail A",
        Distance(5, "km"),
        100,
        "easy",
    )

    trail2 = Trail(
        2,
        "Trail A",
        Distance(5, "km"),
        100,
        "easy",
    )

    assert trail1 != trail2


def test_default_unit_only_affects_new_trails():
    Trail.set_default_unit("km")

    old_trail = Trail(
        1,
        "Old Trail",
        10,
        100,
        "easy",
    )

    Trail.set_default_unit("mi")

    new_trail = Trail(
        2,
        "New Trail",
        10,
        100,
        "easy",
    )

    assert old_trail.distance.unit == "km"
    assert new_trail.distance.unit == "mi"

    Trail.set_default_unit("km")