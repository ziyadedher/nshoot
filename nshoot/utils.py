"""Utility classes.

This module consists of utility classes to aid the main game classes.
"""

from typing import Optional

from enum import Enum


class Direction(Enum):
    """A direction in the game.
    """
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


class Position:
    """Represents a position in the game with x- and y- coordinates.
    """
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Initialize a position with the given <x> and <y> values.
        """
        self.x = x
        self.y = y

    def duplicate(self) -> 'Position':
        """Returns a duplicate of this position.
        """
        return Position(self.x, self.y)

    def __round__(self, n=None) -> 'Position':
        """Returns a new position rounded to the nearest whole coordinates.
        """
        return Position(round(self.x), round(self.y))

    def __eq__(self, other: object) -> bool:
        """Returns whether or not two position objects are equal.
        """
        if not type(self) == type(other):
            return False
        other: Position
        return other.x == self.x and other.y == self.y

    def __str__(self) -> str:
        """Return a human-readable representation of this position object.

        In the form ```Position (<x>, <y>)```.
        """
        return "Position({}, {})".format(str(self.x), str(self.y))

    def __repr__(self) -> str:
        """Return a mechanical representation of this position object.

        In the form ```<nshoot.player.Position (x=<x>, y=<y>)>```.
        """
        return "<nshoot.player.Position (x={}, y={})>".format(str(self.x), str(self.y))


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
                # TODO: handle invalid bounds
                pass
        if y_min is not None and y_max is not None:
            if y_min > y_max:
                # TODO: handle invalid bounds
                pass

        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

    def bound_position(self, position: Position, padding: int) -> None:
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

        In the form ```<nshoot.player.Bounds (x:<x_min>-<x_max>, y:<y_min>-<y_max>)>```.
        """
        return "<nshoot.player.Bounds (x:{}-{}, y:{}-{})>".format(str(self.x_min), str(self.x_max),
                                                                  str(self.y_min), str(self.y_max))