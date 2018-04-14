"""Information about the game.

This module contains data holders that manage information about the game and players.
"""

from typing import List, Dict

from nshoot.utils import Position


class PlayerInformation:
    """Contains information about a player.
    """
    position: Position

    def __init__(self, position: Position) -> None:
        """Initialize this player information.
        """
        self.position = position.duplicate()


class BulletInformation:
    """Contains information about a bullet.
    """
    position: Position

    def __init__(self, position: Position) -> None:
        """Initialize this bullet information.
        """
        self.position = position.duplicate()


class GameInformation:
    """Contains information about the current game state.
    """
    players: Dict[str, PlayerInformation]
    bullet_information: List[BulletInformation]

    def __init__(self, player_information: Dict[str, PlayerInformation],
                 bullet_information: List[BulletInformation]) -> None:
        """Initialize the information in the game.
        """
        self.player_information = player_information
        self.bullet_information = bullet_information
