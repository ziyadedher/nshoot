"""Information about the game.

This module contains data holders that manage information about the game and players.
"""

from typing import List, Dict

from nshoot.utils import Vector


class PlayerInformation:
    """Contains information about a player.
    """
    position: Vector

    def __init__(self, position: Vector) -> None:
        """Initialize this player information.
        """
        self.position = position.duplicate()


class BulletInformation:
    """Contains information about a bullet.
    """
    position: Vector

    def __init__(self, position: Vector) -> None:
        """Initialize this bullet information.
        """
        self.position = position.duplicate()


class GameInformation:
    """Contains information about the current game state.
    """
    players: Dict[str, PlayerInformation]
    bullet_information: List[BulletInformation]

    def __init__(self, players: Dict[str, PlayerInformation] = None,
                 bullet_information: List[BulletInformation] = None) -> None:
        """Initialize the information in the game.
        """
        self.players = players if players else {}
        self.bullet_information = bullet_information if bullet_information else []
