"""Player in the game.

This module manages all aspects of players in the game.
"""

from typing import Optional


class Position:
    """A position object.
    """
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Initialize a position with the given <x> and <y> values.
        """
        self.x = x
        self.y = y

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
    """Bounds for x, y.
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
        if x_min > x_max or y_min > y_max:
            # TODO: handle invalid bounds
            pass

        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

    def bound_position(self, position: Position) -> None:
        """Bound the given position using this bounding object in place.
        """
        # Adjust x and y in position to inside of the bounds
        if position.x < self.x_min:
            position.x = self.x_min
        elif position.x > self.x_max:
            position.x = self.x_max
        if position.y < self.y_min:
            position.y = self.y_min
        elif position.y > self.y_max:
            position.y = self.y_max

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


class Player:
    """A player in the game.
    """
    damage: int
    health: int
    speed: int
    position: Position
    bounds: Bounds

    def __init__(self, damage: int, speed: int, position: Optional[Position]) -> None:
        """Initializes a new player with the given damage, speed, and starting position.
        """
        self.damage = damage
        self.speed = speed
        self.position = position if position else Position(0, 0)
