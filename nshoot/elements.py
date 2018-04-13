"""Manages players in the game.

This module manages all aspects of players in the game from movement to drawing.
"""

from typing import Optional, Tuple

import pygame

from nshoot.utils import Position, Direction, Bounds


class Element:
    """An element in the game that can be drawn.
    """
    def draw(self, surface: pygame.Surface) -> None:
        """Draws this element to the surface.
        """
        raise NotImplementedError


class Bullet(Element):
    """A bullet in the game.
    """
    COLOR: pygame.Color = pygame.Color("lightcoral")
    RADIUS: int = 5

    direction: Direction
    position: Position
    speed: int

    def __init__(self, origin: Position, direction: Direction, speed: int = 800) -> None:
        """Initializes a bullet travelling from an <origin> in a given <direction> at a given <speed>.
        """
        self.position = origin
        self.direction = direction
        self.speed = speed

    def move(self, delta_time: float) -> None:
        """Moves this bullet in its direction with the given <delta_time> modifier.
        """
        self.position.x += self.speed * delta_time * self.direction.value[0]
        self.position.y += self.speed * delta_time * self.direction.value[1]

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the bullet to the given <surface>.
        """
        pos = round(self.position)
        pygame.draw.circle(surface, self.COLOR, (pos.x, pos.y), self.RADIUS)


class Player(Element):
    """A player in the game.
    """
    COLOR: pygame.Color = pygame.Color("cornsilk")
    RADIUS: int = 15

    damage: int
    health: int
    speed: int

    position: Position
    bounds: Bounds

    def __init__(self, damage: int, speed: int) -> None:
        """Initializes a new player with the given <damage> and <speed>.
        """
        self.damage = damage
        self.speed = speed
        self.position = Position(0, 0)
        self.bounds = Bounds()

    def _update_position(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """Updates the position of this player while satisfying bounds.
        """
        if x is None:
            x = self.position.x
        if y is None:
            y = self.position.y

        self.position.x = x
        self.position.y = y
        self.bounds.bound_position(self.position, self.RADIUS)

    def set_position(self, position: Position) -> None:
        """Sets the position of this player.
        """
        self._update_position(position.x, position.y)

    def set_bounds(self, bounds: Bounds) -> None:
        """Sets the bounds of this player.
        """
        self.bounds = bounds
        self._update_position()

    def move(self, raw_input: Tuple[float, float], delta_time: float) -> None:
        """Move the player in the direction specified by the <raw_input> and with the given <delta_time> modifier.

        The <raw_input> is a tuple of (x, y) input floats. The <delta_time> is the time in seconds
        since the last frame update.
        """
        self._update_position(self.position.x + self.speed * delta_time * raw_input[0],
                              self.position.y + self.speed * delta_time * raw_input[1])

    def shoot(self, direction: Direction) -> Bullet:
        """Shoots a bullet in the given <direction> and returns the shot bullet.
        """
        origin = Position(self.position.x + direction.value[0] * self.RADIUS,
                          self.position.y + direction.value[1] * self.RADIUS)
        return Bullet(origin, direction)

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the player to the given <surface>.
        """
        pos = round(self.position)
        pygame.draw.circle(surface, self.COLOR, (pos.x, pos.y), self.RADIUS)
