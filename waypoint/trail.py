from abc import ABC, abstractmethod

from waypoint.distance import Distance


class Trail(ABC):
    """Abstract base class representing a trail."""

    ALLOWED_DIFFICULTIES = {"easy", "moderate", "hard"}
    DEFAULT_UNIT = "km"

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
    ):
        self._id = trail_id
        self._name = name
        self._distance = self._make_distance(distance)
        self._elevation_gain_m = elevation_gain_m

        self.validate_elevation_gain(elevation_gain_m)
        self.validate_difficulty(difficulty)

        self._difficulty = difficulty

    # =========================================================
    # Properties
    # =========================================================

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def distance(self):
        return self._distance

    @property
    def elevation_gain(self):
        return self._elevation_gain_m

    @property
    def elevation_gain_m(self):
        return self._elevation_gain_m

    @property
    def difficulty(self):
        return self._difficulty

    # =========================================================
    # Distance handling
    # =========================================================

    @classmethod
    def _make_distance(cls, distance):
        """Convert a numeric distance into a Distance object."""

        if isinstance(distance, Distance):
            return distance

        return Distance(distance, cls.DEFAULT_UNIT)

    def distance_in_km(self):
        """Return the trail distance in kilometres."""

        if self.distance.unit == "km":
            return self.distance.magnitude

        if self.distance.unit == "mi":
            return self.distance.magnitude * Distance.MI_TO_KM

        raise ValueError(
            f"Unsupported distance unit: {self.distance.unit}"
        )

    # =========================================================
    # Validation
    # =========================================================

    @classmethod
    def validate_elevation_gain(cls, elevation_gain_m):
        """Validate elevation gain."""

        if elevation_gain_m < 0:
            raise ValueError("Elevation gain cannot be negative.")

    @classmethod
    def validate_difficulty(cls, difficulty):
        """Validate trail difficulty."""

        if difficulty not in cls.ALLOWED_DIFFICULTIES:
            raise ValueError(
                f"Difficulty must be one of: "
                f"{', '.join(sorted(cls.ALLOWED_DIFFICULTIES))}"
            )

    def set_difficulty(self, difficulty):
        """Change difficulty after validating the new value."""

        self.validate_difficulty(difficulty)
        self._difficulty = difficulty

    # =========================================================
    # Default distance unit
    # =========================================================

    @classmethod
    def set_default_unit(cls, unit):
        """Set the default unit for numeric distances."""

        if unit not in Distance.ALLOWED_UNITS:
            raise ValueError(f"Unsupported distance unit: {unit}")

        cls.DEFAULT_UNIT = unit

    # =========================================================
    # Dictionary conversion
    # =========================================================

    @classmethod
    def from_dict(cls, data):
        """Create a trail from dictionary/API data."""

        trail_id = data["id"]
        name = data["name"]
        elevation_gain_m = data["elevation_gain_m"]
        difficulty = data["difficulty"]

        distance_data = data["distance"]

        if isinstance(distance_data, dict):
            distance = Distance(
                distance_data["magnitude"],
                distance_data["unit"],
            )
        else:
            distance = Distance(
                distance_data,
                cls.DEFAULT_UNIT,
            )

        cls.validate_elevation_gain(elevation_gain_m)
        cls.validate_difficulty(difficulty)

        return cls(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

    # =========================================================
    # Equality
    # =========================================================

    def __eq__(self, other):
        """Trails with the same ID are considered equal."""

        if not isinstance(other, Trail):
            return NotImplemented

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # =========================================================
    # Abstract methods
    # =========================================================

    @abstractmethod
    def estimated_time(self):
        """Return estimated completion time."""
        pass

    @abstractmethod
    def summary(self):
        """Return a summary of the trail."""
        pass


# =============================================================
# DayHike
# =============================================================


class DayHike(Trail):
    """A trail intended to be completed during one day."""

    PACE_KM_PER_HOUR = 4

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty,
        )

    def estimated_time(self):
        """Estimate time using a 4 km/hour hiking pace."""

        distance_km = self.distance_in_km()

        return distance_km / self.PACE_KM_PER_HOUR

    def summary(self):
        return (
            f"Day hike: {self.name}, "
            f"{self.distance}, "
            f"difficulty: {self.difficulty}"
        )


# =============================================================
# BackpackingRoute
# =============================================================


class BackpackingRoute(Trail):
    """A multi-day backpacking route."""

    PACE_KM_PER_HOUR = 3

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
        days,
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty,
        )

        if days <= 0:
            raise ValueError("Days must be greater than zero.")

        self._days = days

    @property
    def days(self):
        return self._days

    def estimated_time(self):
        """Estimate time using a 3 km/hour hiking pace."""

        distance_km = self.distance_in_km()

        return distance_km / self.PACE_KM_PER_HOUR

    def summary(self):
        return (
            f"Backpacking route: {self.name}, "
            f"{self.distance}, "
            f"{self.days} days, "
            f"difficulty: {self.difficulty}"
        )


# =============================================================
# TrailRun
# =============================================================


class TrailRun(Trail):
    """A trail intended for running."""

    PACE_KM_PER_HOUR = 8

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty,
        )

    def estimated_time(self):
        """Estimate time using an 8 km/hour running pace."""

        distance_km = self.distance_in_km()

        return distance_km / self.PACE_KM_PER_HOUR

    def summary(self):
        return (
            f"Trail run: {self.name}, "
            f"{self.distance}, "
            f"difficulty: {self.difficulty}"
        )


# =============================================================
# GuidedDayHike
# =============================================================


class GuidedDayHike(DayHike):
    """A day hike led by a guide."""

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
        guide_name,
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty,
        )

        self._guide_name = guide_name

    @property
    def guide_name(self):
        return self._guide_name

    def summary(self):
        """Extend the DayHike summary rather than replacing it."""

        return (
            f"{super().summary()}, "
            f"guide: {self.guide_name}"
        )


# =============================================================
# ElevationMixin
# =============================================================


class ElevationMixin:
    """Mixin that provides average trail grade."""

    @property
    def grade_percent(self):
        """Calculate average grade percentage."""

        distance_km = self.distance_in_km()

        if distance_km == 0:
            return 0

        distance_m = distance_km * 1000

        return (self.elevation_gain_m / distance_m) * 100


# =============================================================
# RatingMixin
# =============================================================


class RatingMixin:
    """Mixin that provides an average star rating."""

    def __init__(self, *args, rating=0, **kwargs):
        super().__init__(*args, **kwargs)

        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5.")

        self._rating = rating

    @property
    def rating(self):
        return self._rating


# =============================================================
# RatedDayHike
# =============================================================


class RatedDayHike(ElevationMixin, RatingMixin, DayHike):
    """Day hike using both elevation and rating mixins."""

    def __init__(
        self,
        trail_id,
        name,
        distance,
        elevation_gain_m,
        difficulty,
        rating=0,
    ):
        super().__init__(
            trail_id,
            name,
            distance,
            elevation_gain_m,
            difficulty,
            rating=rating,
        )

    def summary(self):
        """Extend the inherited DayHike summary."""

        return (
            f"{super().summary()}, "
            f"grade: {self.grade_percent:.1f}%, "
            f"rating: {self.rating:.1f}"
        )