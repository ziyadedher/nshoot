"""Information about the game.

This module contains data holders that manage information about the game and players.
"""

from typing import List, Dict

from nshoot.utils import Vector, Bounds


class PlayerInformation:
    """Contains information about a player.
    """
    radius: int
    position: Vector
    bounds: Bounds

    def __init__(self, radius: int, position: Vector, bounds: Bounds) -> None:
        """Initialize this player information.
        """
        self.radius = radius
        self.position = position.duplicate()
        self.bounds = bounds.duplicate()


class BulletInformation:
    """Contains information about a bullet.
    """
    radius: int
    position: Vector
    direction: Vector

    def __init__(self, radius: int, position: Vector, direction: Vector) -> None:
        """Initialize this bullet information.
        """
        self.radius = radius
        self.position = position.duplicate()
        self.direction = direction.duplicate()


class GameInformation:
    """Contains information about the current game state.
    """
    players: Dict[str, PlayerInformation]
    bullets: List[BulletInformation]

    def __init__(self, players: Dict[str, PlayerInformation] = None,
                 bullets: List[BulletInformation] = None) -> None:
        """Initialize the information in the game.
        """
        self.players = players if players else {}
        self.bullets = bullets if bullets else []
