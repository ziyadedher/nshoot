"""Contains different strategies for players.

This module manages and executes the different strategies available for a player.
"""

from typing import Tuple, Optional

import pygame
from nshoot.info import GameInformation
from nshoot.utils import Direction


class Strategy:
    """Abstract strategy that a play can use to move and shoot.
    """
    player_id: str
    info: GameInformation

    def __init__(self, player_id: str) -> None:
        """Initializes this strategy with empty game information and the given <player_id>.
        """
        self.player_id = player_id
        self.info = GameInformation()

    def get_move(self) -> Tuple[Tuple[float, float], Direction]:
        """Get the next move the player should make.
        """
        raise NotImplementedError

    def update_info(self, info: GameInformation) -> None:
        """Updates this strategy's state based on the given player information.
        """
        self.info = info


class IdleStrategy(Strategy):
    """Idle strategy that causes any player using it to never make any move.
    """
    def get_move(self) -> Tuple[Tuple[float, float], Optional[Direction]]:
        """Get the next move the player should make. It does nothing in the idle strategy.
        """
        return (0.0, 0.0), None


class UserInputStrategy(Strategy):
    """User input strategy that gets user input to determine the next move.
    """
    move_keys: Tuple[int, int, int, int]
    shoot_keys: Tuple[int, int, int, int]

    def __init__(self, player_id: str,
                 move_keys: Tuple[int, int, int, int], shoot_keys: Tuple[int, int, int, int]) -> None:
        """Initializes this user input strategy with the given <player_id> and
        with the given keys for movement and shooting in the order of WEST EAST NORTH SOUTH.
        """
        super().__init__(player_id)
        self.move_keys = move_keys
        self.shoot_keys = shoot_keys

    def get_move(self) -> Tuple[Tuple[float, float], Optional[Direction]]:
        """Get the next move the player should make. Gets user input in the user input strategy.
        """
        return self.get_user_input()

    def get_user_input(self) -> Tuple[Tuple[float, float], Optional[Direction]]:
        """Gets the user raw input from all sources in a list.
        """
        pressed = pygame.key.get_pressed()

        source_input = [0.0, 0.0]
        if pressed[self.move_keys[0]]:
            source_input[0] -= 1
        if pressed[self.move_keys[1]]:
            source_input[0] += 1
        if pressed[self.move_keys[2]]:
            source_input[1] -= 1
        if pressed[self.move_keys[3]]:
            source_input[1] += 1
        move = (source_input[0], source_input[1])

        shoot = None
        if pressed[self.shoot_keys[0]]:
            shoot = Direction.WEST
        elif pressed[self.shoot_keys[1]]:
            shoot = Direction.EAST
        elif pressed[self.shoot_keys[2]]:
            shoot = Direction.NORTH
        elif pressed[self.shoot_keys[3]]:
            shoot = Direction.SOUTH

        return move, shoot


class BounceStrategy(Strategy):
    """Bounce strategy were the player bounces from the top of the screen to the bottom and fires east.
    """
    going_down: bool

    def __init__(self, player_id: str) -> None:
        """Initializes this bounce strategy going down with the given <player_id>.
        """
        super().__init__(player_id)
        self.going_down = True

    def get_move(self) -> Tuple[Tuple[float, float], Optional[Direction]]:
        """Get the next move the player should make.
        """
        position = self.info.players[self.player_id].position
        if self.going_down:
            if position.y >= 785:
                self.going_down = False
                return self.get_move()
            else:
                return (0, 1.0), Direction.EAST
        else:
            if position.y <= 15:
                self.going_down = True
                return self.get_move()
            else:
                return (0, -1.0), Direction.EAST


class SemiSmartStrategy(Strategy):
    """Semi-smart strategy where the player lines up vertically and shoots to the correct direction of another player.
    """
    target_id: str

    def __init__(self, player_id: str) -> None:
        """Initializes this bounce strategy going down with the given <player_id>.
        """
        super().__init__(player_id)

    def get_move(self) -> Tuple[Tuple[float, float], Optional[Direction]]:
        """Get the next move the player should make.
        """
        target_id = self.player_id
        for key in self.info.players.keys():
            if key != target_id:
                target_id = key
                break

        player_pos = self.info.players[self.player_id].position
        target_pos = self.info.players[target_id].position

        shoot = None
        if target_pos.x < player_pos.x:
            shoot = Direction.WEST
        elif target_pos.x > player_pos.x:
            shoot = Direction.EAST

        move = (0.0, 0.0)
        if target_pos.y > player_pos.y:
            move = (0.0, 1.0)
        elif target_pos.y < player_pos.y:
            move = (0.0, -1.0)

        return move, shoot





