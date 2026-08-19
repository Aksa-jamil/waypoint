class Distance:
    """A value type representing a distance in kilometres or miles."""

    KM_TO_MI = 0.621371
    MI_TO_KM = 1.609344

    ALLOWED_UNITS = {"km", "mi"}

    def __init__(self, magnitude, unit):
        self._validate_magnitude(magnitude)
        self._validate_unit(unit)

        self._magnitude = float(magnitude)
        self._unit = unit

    @staticmethod
    def _validate_magnitude(magnitude):
        if magnitude < 0:
            raise ValueError("Distance cannot be negative.")

    @staticmethod
    def _validate_unit(unit):
        if unit not in Distance.ALLOWED_UNITS:
            raise ValueError("Unit must be 'km' or 'mi'.")

    @property
    def magnitude(self):
        """Read-only access to the distance magnitude."""
        return self._magnitude

    @property
    def unit(self):
        """Read-only access to the distance unit."""
        return self._unit

    def convert(self, target_unit):
        """Return this distance converted to the target unit."""

        self._validate_unit(target_unit)

        if target_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        if self._unit == "km" and target_unit == "mi":
            converted = self._magnitude * self.KM_TO_MI
        else:
            converted = self._magnitude * self.MI_TO_KM

        return Distance(converted, target_unit)

    def __str__(self):
        return f"{self._magnitude:g} {self._unit}"

    def __repr__(self):
        return f"Distance({self._magnitude!r}, {self._unit!r})"