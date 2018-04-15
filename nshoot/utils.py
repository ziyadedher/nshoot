"""Utility classes.

This module consists of utility classes to aid the main game classes.
"""

from typing import Any, Optional

import math


class Vector:
    """Represents a vector in the game with x- and y- values.
    """

    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Initialize a vector with the given <x> and <y> values.
        """
        self.x = x
        self.y = y

    @staticmethod
    def zero() -> 'Vector':
        """Returns the zero vector.
        """
        return Vector(0, 0)

    @property
    def magnitude(self) -> float:
        """Returns the magnitude of the vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self) -> float:
        """Returns the angle of this vector in radians from the positive horizontal counter-clockwise.
        """
        return math.tan(self.y / self.x)

    def distance(self, vector: 'Vector') -> float:
        """Returns the distance between this vector and the given <vector> in space.
        """
        return math.hypot(self.x - vector.x, self.y - vector.y)

    def duplicate(self) -> 'Vector':
        """Returns a duplicate of this position.
        """
        return Vector(self.x, self.y)

    def seminormalize(self, magnitude: float) -> 'Vector':
        """Returns a new vector in the same direction but with magnitude <magnitude> if and only if the vector has
        magnitude more than <magnitude>. Otherwise returns the vector."""
        return self * (magnitude / self.magnitude) if self.magnitude > magnitude else self

    def normalize(self) -> 'Vector':
        """Returns a new vector in the same direction but with magnitude 1, or the zero vector.
        """
        return self / self.magnitude if self.magnitude != 0 else Vector(0, 0)

    def __round__(self, n=None) -> 'Vector':
        """Returns a new position rounded to the nearest whole coordinates.
        """
        return Vector(round(self.x), round(self.y))

    def __neg__(self) -> 'Vector':
        """Returns a new vector of the same magnitude but opposite direction.
        """
        return Vector(-self.x, -self.y)

    def __add__(self, other: Any) -> 'Vector':
        """Returns a new vector which is the result of adding each component of the vectors if it is a vector or
        adding the number to all components of the vector otherwise.
        """
        return Vector(self.x + other.x, self.y + other.y) \
            if isinstance(other, Vector) else Vector(self.x + other, self.y + other)

    def __iadd__(self, other: Any) -> 'Vector':
        """Modifies this vector to the result of adding each component of the vectors if it is a vector or
        adding the number to all components of the vector otherwise.
        """
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other: Any) -> 'Vector':
        """Returns a new vector which is the result of subtracting each component of the vectors if it is a vector or
        subtracting the number to all components of the vector otherwise.
        """
        return Vector(self.x - other.x, self.y - other.y) \
            if isinstance(other, Vector) else Vector(self.x - other, self.y - other)

    def __isub__(self, other: Any) -> 'Vector':
        """Modifies this vector to the result of subtracting each component of the vectors if it is a vector or
        subtracting the number to all components of the vector otherwise.
        """
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other: Any) -> 'Vector':
        """Returns a new vector which is the result of multiplying each component of the vectors if it is a vector or
        multiplying the number to all components of the vector otherwise.
        """
        return Vector(self.x * other.x, self.y * other.y) \
            if isinstance(other, Vector) else Vector(self.x * other, self.y * other)

    def __imul__(self, other: Any) -> 'Vector':
        """Modifies this vector to the result of multiplying each component of the vectors if it is a vector or
        multiplying the number to all components of the vector otherwise.
        """
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __truediv__(self, other: Any) -> 'Vector':
        """Returns a new vector which is the result of dividing each of the coordinates by the given.
        """
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other: Any) -> bool:
        """Returns whether or not two position objects are equal.
        """
        if not isinstance(other, Vector):
            return False
        return other.x == self.x and other.y == self.y

    def __str__(self) -> str:
        """Return a human-readable representation of this position object.

        In the form ```Vector (<x>, <y>)```.
        """
        return "Vector({}, {})".format(str(self.x), str(self.y))

    def __repr__(self) -> str:
        """Return a mechanical representation of this vector object.

        In the form ```<nshoot.utils.Vector (x=<x>, y=<y>)>```.
        """
        return "<nshoot.utils.Vector (x={}, y={})>".format(str(self.x), str(self.y))


class Bounds:
    """Bounds for a player that has methods to restrict positioning.
    """
    x_max: Optional[float]
    x_min: Optional[float]
    y_max: Optional[float]
    y_min: Optional[float]

    def __init__(self, *,
                 x_max: Optional[float] = None, x_min: Optional[float] = None,
                 y_max: Optional[float] = None, y_min: Optional[float] = None) -> None:
        """Initialize a bounds object with the given bounds. Only keyword arguments are accepted.
        """
        if x_min is not None and x_max is not None:
            if x_min > x_max:
                raise ValueError("Invalid bounds input!")
        if y_min is not None and y_max is not None:
            if y_min > y_max:
                raise ValueError("Invalid bounds input!")

        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

    def bound_position(self, position: Vector, padding: int) -> None:
        """Bound the given <position> using this bounding object in place, with the given <padding> on any side
        of the position.
        """
        if self.x_min is not None:
            x_min_padding = self.x_min + padding
            if position.x < x_min_padding:
                position.x = x_min_padding
        if self.x_max is not None:
            x_max_padding = self.x_max - padding
            if position.x > x_max_padding:
                position.x = x_max_padding
        if self.y_min is not None:
            y_min_padding = self.y_min + padding
            if position.y < y_min_padding:
                position.y = y_min_padding
        if self.y_max is not None:
            y_max_padding = self.y_max - padding
            if position.y > y_max_padding:
                position.y = y_max_padding

    def duplicate(self) -> 'Bounds':
        """Returns a duplicate of this Bounds.
        """
        return Bounds(x_max=self.x_max, x_min=self.x_min, y_max=self.y_max, y_min=self.y_min)

    def __eq__(self, other: object) -> bool:
        """Returns whether or not two bounds objects are equal.
        """
        if not type(self) == type(other):
            return False
        other: Bounds
        return (self.x_max == other.x_max and self.x_min == other.x_min
                and self.y_max == other.y_max and self.y_min == other.y_min)

    def __str__(self) -> str:
        """Return a human-readable representation of this bounds object.

        In the form ```Bounds (<x_min> - <x_max>, <y_min> - <y_max>)```.
        """
        return "Bounds ({} - {}, {} - {})".format(str(self.x_min), str(self.x_max),
                                                  str(self.y_min), str(self.y_max))

    def __repr__(self) -> str:
        """Return a mechanical representation of this bounds object.

        In the form ```<nshoot.utils.Bounds (x=<x_min>-<x_max>, y=<y_min>-<y_max>)>```.
        In the form ```<nshoot.utils.Bounds (x:<x_min>-<x_max>, y:<y_min>-<y_max>)>```.
        """
        return "<nshoot.utils.Bounds (x:{}-{}, y:{}-{})>".format(str(self.x_min), str(self.x_max),
                                                                 str(self.y_min), str(self.y_max))
