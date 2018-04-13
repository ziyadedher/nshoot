"""Contains different strategies for players.

This module manages and executes the different strategies available for a player.
"""

from typing import Tuple, Optional

import pygame
from nshoot.utils import Direction


class Strategy:
    """Abstract strategy that a play can use to move and shoot.
    """
    player_info: tuple

    def get_move(self) -> Tuple[Tuple[float, float], Direction]:
        """Get the next move the player should make.
        """
        raise NotImplementedError

    def update_info(self, player_info: tuple) -> None:
        """Updates this strategy's state based on the given player information.
        """
        self.player_info = player_info


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

    def __init__(self,
                 move_keys: Tuple[int, int, int, int], shoot_keys: Tuple[int, int, int, int]) -> None:
        """Initializes this user input strategy
        with the given keys for movement and shooting in the order of WEST EAST NORTH SOUTH.
        """
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
