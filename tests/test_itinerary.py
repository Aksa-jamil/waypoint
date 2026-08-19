import pytest

from waypoint.distance import Distance
from waypoint.itinerary import Itinerary
from waypoint.trail import Trail


def make_trail(trail_id, distance):
    return Trail(
        trail_id,
        f"Trail {trail_id}",
        Distance(distance, "km"),
        100,
        "easy",
    )


def test_itinerary_total_distance():
    trail1 = make_trail(1, 5)
    trail2 = make_trail(2, 10)
    trail3 = make_trail(3, 15)

    itinerary = Itinerary()

    itinerary.add_trail(trail1)
    itinerary.add_trail(trail2)
    itinerary.add_trail(trail3)

    total = itinerary.total_distance()

    assert total.magnitude == pytest.approx(30)
    assert total.unit == "km"


def test_itinerary_preserves_order():
    trail1 = make_trail(1, 5)
    trail2 = make_trail(2, 10)

    itinerary = Itinerary()

    itinerary.add_trail(trail1)
    itinerary.add_trail(trail2)

    assert itinerary.trails == (trail1, trail2)


def test_itineraries_are_independent():
    trail1 = make_trail(1, 5)

    itinerary1 = Itinerary()
    itinerary2 = Itinerary()

    itinerary1.add_trail(trail1)

    assert len(itinerary1) == 1
    assert len(itinerary2) == 0


def test_total_distance_can_be_requested_in_miles():
    trail1 = make_trail(1, 10)

    itinerary = Itinerary()
    itinerary.add_trail(trail1)

    total = itinerary.total_distance("mi")

    assert total.unit == "mi"
    assert total.magnitude == pytest.approx(6.21371, rel=1e-5)