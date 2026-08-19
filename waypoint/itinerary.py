from waypoint.distance import Distance


class Itinerary:
    """An ordered collection of trails."""

    def __init__(self, trails=None):
        """Create an itinerary with an optional initial collection of trails."""

        if trails is None:
            self._trails = []
        else:
            self._trails = list(trails)

    @property
    def trails(self):
        """Read-only view of the itinerary's trails."""

        return tuple(self._trails)

    def add_trail(self, trail):
        """Add a trail to the itinerary."""

        self._trails.append(trail)

    def total_distance(self, unit=None):
        """Return the total distance of all trails."""

        if not self._trails:
            return Distance(0, unit or "km")

        if unit is None:
            unit = self._trails[0].distance.unit

        total = 0.0

        for trail in self._trails:
            converted = trail.distance.convert(unit)
            total += converted.magnitude

        return Distance(total, unit)

    def __len__(self):
        return len(self._trails)

    def __repr__(self):
        return f"Itinerary(trails={self._trails!r})"