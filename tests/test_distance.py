import pytest

from waypoint.distance import Distance


def test_distance_accepts_positive_magnitude():
    distance = Distance(10, "km")

    assert distance.magnitude == 10
    assert distance.unit == "km"


def test_distance_rejects_negative_magnitude():
    with pytest.raises(ValueError):
        Distance(-5, "km")


def test_distance_rejects_invalid_unit():
    with pytest.raises(ValueError):
        Distance(5, "meters")


def test_km_to_miles_conversion():
    distance = Distance(10, "km")

    converted = distance.convert("mi")

    assert converted.unit == "mi"
    assert converted.magnitude == pytest.approx(6.21371, rel=1e-5)


def test_conversion_round_trip():
    original = Distance(10, "km")

    miles = original.convert("mi")
    kilometres = miles.convert("km")

    assert kilometres.magnitude == pytest.approx(
        original.magnitude,
        rel=1e-5,
    )


def test_magnitude_is_read_only():
    distance = Distance(10, "km")

    with pytest.raises(AttributeError):
        distance.magnitude = 20