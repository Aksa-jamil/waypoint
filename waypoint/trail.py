from waypoint.distance import Distance


class Trail:
    """Domain model representing a hiking trail."""

    DEFAULT_UNIT = "km"

    ALLOWED_DIFFICULTIES = {
        "easy",
        "moderate",
        "hard",
    }

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

        if isinstance(distance, Distance):
            self._distance = distance
        else:
            self._distance = Distance(distance, self.DEFAULT_UNIT)

        self._elevation_gain_m = elevation_gain_m

        self.set_difficulty(difficulty)

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
    def elevation_gain_m(self):
        return self._elevation_gain_m

    @property
    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, difficulty):
        """Set difficulty after validating it."""

        self.validate_difficulty(difficulty)
        self._difficulty = difficulty

    @staticmethod
    def validate_difficulty(difficulty):
        """Validate a trail difficulty."""

        if difficulty not in Trail.ALLOWED_DIFFICULTIES:
            raise ValueError(
                f"Invalid difficulty: {difficulty}. "
                f"Choose from {Trail.ALLOWED_DIFFICULTIES}."
            )

    @staticmethod
    def validate_elevation_gain(elevation_gain_m):
        """Validate elevation gain."""

        if elevation_gain_m < 0:
            raise ValueError("Elevation gain cannot be negative.")

    @classmethod
    def from_dict(cls, data):
        """Create a Trail from an API-shaped dictionary."""

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

        return cls(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

    @classmethod
    def set_default_unit(cls, unit):
        """Change the platform default unit for newly created trails."""

        Distance._validate_unit(unit)
        cls.DEFAULT_UNIT = unit

    def __eq__(self, other):
        """Two trails are equal when they have the same ID."""

        if not isinstance(other, Trail):
            return NotImplemented

        return self._id == other._id

    def __str__(self):
        return (
            f"{self._name} - {self._distance}, "
            f"{self._difficulty}, "
            f"{self._elevation_gain_m} m elevation"
        )

    def __repr__(self):
        return (
            f"Trail("
            f"id={self._id!r}, "
            f"name={self._name!r}, "
            f"distance={self._distance!r}, "
            f"elevation_gain_m={self._elevation_gain_m!r}, "
            f"difficulty={self._difficulty!r})"
        )