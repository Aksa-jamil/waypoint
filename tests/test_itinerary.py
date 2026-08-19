from waypoint.distance import Distance
from waypoint.itinerary import Itinerary
from waypoint.trail import DayHike


def make_trail(trail_id, distance):
    return DayHike(
        trail_id,
        f"Trail {trail_id}",
        Distance(distance, "km"),
        100,
        "easy",
    )


def test_itinerary_total_distance():
    trail1 = make_trail(1, 5)
    trail2 = make_trail(2, 7)

    itinerary = Itinerary([trail1, trail2])

    total = itinerary.total_distance()

    assert total == Distance(12, "km")


def test_itinerary_preserves_order():
    trail1 = make_trail(1, 5)
    trail2 = make_trail(2, 7)

    itinerary = Itinerary([trail1, trail2])

    assert itinerary.trails[0] == trail1
    assert itinerary.trails[1] == trail2


def test_itineraries_are_independent():
    trail1 = make_trail(1, 5)
    trail2 = make_trail(2, 7)

    itinerary1 = Itinerary([trail1])
    itinerary2 = Itinerary([trail2])

    assert itinerary1.trails != itinerary2.trails
    assert itinerary1.total_distance() == Distance(5, "km")
    assert itinerary2.total_distance() == Distance(7, "km")


def test_total_distance_can_be_requested_in_miles():
    trail1 = make_trail(1, 10)
    trail2 = make_trail(2, 10)

    itinerary = Itinerary([trail1, trail2])

    total = itinerary.total_distance(unit="mi")

    assert total.unit == "mi"
    assert total.magnitude == 20 * Distance.KM_TO_MI