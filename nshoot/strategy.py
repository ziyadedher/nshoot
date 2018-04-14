"""Contains different strategies for players.

This module manages and executes the different strategies available for a player.
"""

from typing import Tuple, Optional

import pygame
from nshoot.info import GameInformation, PlayerInformation, BulletInformation
from nshoot.utils import Vector


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

    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make.
        """
        raise NotImplementedError

    def update_info(self, info: GameInformation) -> None:
        """Updates this strategy's state based on the given player information.
        """
        self.info = info

    def _select_random_target(self) -> str:
        """Selects a random target player.
        """
        for key in self.info.players.keys():
            if key != self.player_id:
                return key


class IdleStrategy(Strategy):
    """Idle strategy that causes any player using it to never make any move.
    """
    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make. It does nothing in the idle strategy.
        """
        return Vector.zero(), Vector.zero()


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

    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make. Gets user input in the user input strategy.
        """
        return self.get_user_input()

    def get_user_input(self) -> Tuple[Vector, Optional[Vector]]:
        """Gets the user raw input from all sources in a list.
        """
        pressed = pygame.key.get_pressed()

        move = [0.0, 0.0]
        if pressed[self.move_keys[0]]:
            move[0] -= 1
        if pressed[self.move_keys[1]]:
            move[0] += 1
        if pressed[self.move_keys[2]]:
            move[1] -= 1
        if pressed[self.move_keys[3]]:
            move[1] += 1

        shoot = [0.0, 0.0]
        if pressed[self.shoot_keys[0]]:
            shoot[0] -= 1
        if pressed[self.shoot_keys[1]]:
            shoot[0] += 1
        if pressed[self.shoot_keys[2]]:
            shoot[1] -= 1
        if pressed[self.shoot_keys[3]]:
            shoot[1] += 1

        return Vector(*move), Vector(*shoot)


class BounceStrategy(Strategy):
    """Bounce strategy were the player bounces from the top of the screen to the bottom and fires east.
    """
    going_down: bool

    def __init__(self, player_id: str) -> None:
        """Initializes this bounce strategy going down with the given <player_id>.
        """
        super().__init__(player_id)
        self.going_down = True

    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make.
        """
        position = self.info.players[self.player_id].position
        if self.going_down:
            if position.y >= 785:
                self.going_down = False
                return self.get_move()
            else:
                return Vector(0, 1), Vector(1, 0)
        else:
            if position.y <= 15:
                self.going_down = True
                return self.get_move()
            else:
                return Vector(0, -1), Vector(-1, 0)


class SemiSmartStrategy(Strategy):
    """Semi-smart strategy where the player lines up vertically and shoots to the correct direction of another player.
    """
    target_id: str

    def __init__(self, player_id: str) -> None:
        """Initializes this semi-smart strategy with itself as target and with the given <player_id>.
        """
        super().__init__(player_id)
        self.target_id = self.player_id

    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make.
        """
        player_pos = self.info.players[self.player_id].position
        target_pos = self.info.players[self._select_random_target()].position

        shoot = (0, 0)
        if target_pos.x < player_pos.x:
            shoot = (-1, 0)
        elif target_pos.x > player_pos.x:
            shoot = (1, 0)

        move = (0, 0)
        if target_pos.y > player_pos.y:
            move = (0, 1)
        elif target_pos.y < player_pos.y:
            move = (0, -1)

        return Vector(*move), Vector(*shoot)


class SmartStrategy(Strategy):
    """Smart strategy where the player dodges bullets vertically, lines up horizontally and vertically, and shoots
    to the correct direction of another player.
    """
    target_id: str

    def __init__(self, player_id: str) -> None:
        """Initializes this bounce strategy going down with the given <player_id>.
        """
        super().__init__(player_id)
        self.target_id = self.player_id

    def get_move(self) -> Tuple[Vector, Vector]:
        """Get the next move the player should make.
        """
        player = self.info.players[self.player_id]
        target = self.info.players[self._select_random_target()]
        bullet = self._get_closest_dangerous_bullet()

        move = Vector.zero()
        if bullet:
            bullet_dist = player.position.distance(bullet.position)
            projection = bullet.direction * bullet_dist + bullet.position
            margin = player.radius + bullet.radius + 100

            if player.position.x - margin <= projection.x <= player.position.x + margin:
                move.x += 1 * abs(bullet.direction.y) * (1 if projection.y < player.position.y else -1)
            if player.position.y - margin <= projection.y <= player.position.y + margin:
                move.y += 1 * abs(bullet.direction.x) * (1 if projection.y < player.position.y else -1)

        return move, Vector.zero()

    def _get_closest_dangerous_bullet(self) -> Optional[BulletInformation]:
        """Returns the bullet information of the closest bullet to the player's position travelling towards the player.
        """
        if len(self.info.bullets) == 0:
            return None

        player = self.info.players[self.player_id]

        dangerous_bullets = []
        for bullet in self.info.bullets:
            if player.position.distance(bullet.position) > \
                    player.position.distance(bullet.position + bullet.direction):
                    dangerous_bullets.append(bullet)

        return min(dangerous_bullets, key=lambda bullet: player.position.distance(bullet.position)) \
            if dangerous_bullets else None
