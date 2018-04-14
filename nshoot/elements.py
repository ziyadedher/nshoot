"""Manages players in the game.

This module manages all aspects of players in the game from movement to drawing.
"""

from typing import Any, Optional, Tuple, Dict

import time

import pygame
from nshoot import config
from nshoot.strategy import Strategy
from nshoot.info import PlayerInformation
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
    damage: int
    speed: int

    def __init__(self, origin: Position, direction: Direction, damage: int, speed: int) -> None:
        """Initializes a bullet travelling from an <origin> in a given <direction> at a given <speed>.
        """
        self.position = origin
        self.direction = direction
        self.damage = damage
        self.speed = speed

    def move(self, delta_time: float) -> None:
        """Moves this bullet in its direction with the given <delta_time> modifier.
        """
        self.position.x += self.speed * delta_time * self.direction.value[0]
        self.position.y += self.speed * delta_time * self.direction.value[1]

    def out_of_bounds(self) -> bool:
        """Returns whether or not this bullet is out of bounds of the screen.
        """
        x_out = self.position.x > config.WIDTH or self.position.x < 0
        y_out = self.position.y > config.HEIGHT or self.position.y < 0
        return x_out or y_out

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the bullet to the given <surface>.
        """
        pos = round(self.position)
        pygame.draw.circle(surface, self.COLOR, (pos.x, pos.y), self.RADIUS)


class Player(Element):
    """A player in the game.
    """
    BASE_COLOR: pygame.Color = pygame.Color("cornsilk")
    HURT_COLOR: pygame.Color = pygame.Color("indianred")
    RADIUS: int = 15

    damage: int
    max_health: int
    health: int

    speed: int
    firerate: int

    last_shot_time: float
    position: Position
    bounds: Bounds
    strategy: Strategy

    color: pygame.Color

    def __init__(self, player_id: str,
                 damage: int, speed: int, max_health: int, firerate: int, strategy: Strategy) -> None:
        """Initializes a new player <player_id> with the given <damage>, <speed>, <max_health> and <firerate>.
        Can also take a <strategy> that determines how the player will play.
        """
        self._player_id = player_id

        self.damage = damage
        self.max_health = max_health
        self.health = self.max_health

        self.speed = speed
        self.firerate = firerate

        self.last_shot_time = time.time()
        self.position = Position(0, 0)
        self.bounds = Bounds()
        self.strategy = strategy

        self.color = pygame.Color(self.BASE_COLOR.r, self.BASE_COLOR.g, self.BASE_COLOR.b, self.BASE_COLOR.a)

    @property
    def player_id(self) -> str:
        return self._player_id

    def get_info(self) -> PlayerInformation:
        """Gets important information about this player.
        """
        return PlayerInformation(self.position)

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

    def shoot(self, direction: Direction) -> Optional[Bullet]:
        """Shoots a bullet in the given <direction> and returns the shot bullet.
        """
        if time.time() < self.last_shot_time + (1 / self.firerate):
            return None

        self.last_shot_time = time.time()
        origin = Position(self.position.x + direction.value[0] * (self.RADIUS + Bullet.RADIUS + 1),
                          self.position.y + direction.value[1] * (self.RADIUS + Bullet.RADIUS + 1))
        return Bullet(origin, direction, self.damage, config.DEFAULT_BULLET_SPEED)

    def hit(self, bullet: Bullet) -> None:
        """Registers a hit on this player by the given <bullet>.
        """
        self.health -= bullet.damage
        if self.health <= 0:
            self.health = 0

        health_percent = self.health / self.max_health
        self.color.r = int(self.HURT_COLOR.r + health_percent * (self.BASE_COLOR.r - self.HURT_COLOR.r))
        self.color.g = int(self.HURT_COLOR.g + health_percent * (self.BASE_COLOR.g - self.HURT_COLOR.g))
        self.color.b = int(self.HURT_COLOR.b + health_percent * (self.BASE_COLOR.b - self.HURT_COLOR.b))
        self.color.a = int(self.HURT_COLOR.a + health_percent * (self.BASE_COLOR.a - self.HURT_COLOR.a))

    def is_dead(self) -> bool:
        """Returns whether or not this player is dead.
        """
        return self.health <= 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draws the player to the given <surface>.
        """
        pos = round(self.position)
        pygame.draw.circle(surface, self.color, (pos.x, pos.y), self.RADIUS)
