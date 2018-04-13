"""Manages all aspects of displaying and interacting with the game.

This module manages interaction of the user with the game, including viewing and input.
"""
from typing import List, Tuple, Optional

import sys
import math
import random

import pygame
from nshoot import config
from nshoot.elements import Player, Bullet
from nshoot.utils import Position, Bounds, Direction


class Game:
    """A game instance that controls all underlying aspects of the game including simulation.
    """
    num_players: int
    players: List[Player]
    bullets: List[Bullet]

    def __init__(self, num_players: int = config.NUM_PLAYERS, stats: Optional[List[Tuple[int, int]]] = None):
        """Initializes this game instance with the given number of players <num_players>
        and the attributes of each player in a list of tuples of damage by speed <stats>.
        """
        self.num_players = num_players
        self.players = []
        self.bullets = []

        stats = stats + [config.DEFAULT_STATS] * (num_players - len(stats))\
            if stats else [config.DEFAULT_STATS] * num_players
        for i in range(self.num_players):
            player = Player(*stats[i])

            bounds = Bounds(x_max=config.WIDTH, x_min=0, y_max=config.HEIGHT, y_min=0)
            position = Position(random.randint(0, config.WIDTH), random.randint(0, config.HEIGHT))

            player.set_bounds(bounds)
            player.set_position(position)

            self.players.append(player)

    def _register_hits(self) -> None:
        """Registers hits from all bullets.
        """
        dead_bullets = []

        for bullet in self.bullets:
            if bullet.out_of_bounds():
                dead_bullets.append(bullet)
                continue

            for player in self.players:
                dist = math.hypot(player.position.x - bullet.position.x,
                                  player.position.y - bullet.position.y)
                if dist <= player.RADIUS + bullet.RADIUS:
                    player.hit(bullet)
                    dead_bullets.append(bullet)
                    break

        for bullet in dead_bullets:
            self.bullets.remove(bullet)

    def update(self, delta_time: float,
               move_inputs: List[Tuple[float, float]],
               shoot_inputs: List[Optional[Direction]]) -> None:
        """Update the game based on the given <delta_time>.
        Also <move_inputs> and <shoot_inputs> corresponding to each player.
        """
        for _ in range(self.num_players - len(move_inputs)):
            move_inputs.append((0.0, 0.0))
        for _ in range(self.num_players - len(shoot_inputs)):
            shoot_inputs.append(None)

        for i, player in enumerate(self.players):
            player.move(move_inputs[i], delta_time)

            for other_player in self.players:
                if other_player == player:
                    continue
                dist = math.hypot(player.position.x - other_player.position.x,
                                  player.position.y - other_player.position.y)
                if dist <= player.RADIUS + other_player.RADIUS:
                    player.move((-move_inputs[i][0], -move_inputs[i][1]), delta_time)
                    break

            if shoot_inputs[i] is not None:
                bullet = player.shoot(shoot_inputs[i])
                if bullet is not None:
                    self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.move(delta_time)

        self._register_hits()

    def draw(self, surface: pygame.Surface) -> None:
        """Draws all objects in this game to the given <surface>.
        """
        for player in self.players:
            player.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)


class GameView:
    """A game view which controls all displaying and interaction with the game.
    """
    COLOR: pygame.Color = pygame.Color('cadetblue4')

    surface: pygame.Surface
    clock: pygame.time.Clock
    game: Game
    joysticks: List[pygame.joystick.Joystick]

    def __init__(self, size: Tuple[int, int], caption: str) -> None:
        """Initializes this game view with the given `x` by `y` <size> and the given <caption>.
        """
        pygame.init()
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.game = Game()

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()

    def start(self) -> None:
        """Start this game view and the underlying game.
        """
        since_last_refresh = 0

        while True:
            delta_time = self.clock.get_time() / 1000
            since_last_refresh += delta_time
            self.clock.tick()

            self.update(delta_time)
            if since_last_refresh > 1 / config.REFRESH_RATE:
                self.refresh()
                since_last_refresh = 0

    def update(self, delta_time: float) -> None:
        """Updates the game with the given <delta_time> which is the time elapsed since the last frame in seconds.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        move_inputs, shoot_inputs = self.get_user_input()
        self.game.update(delta_time, move_inputs[:config.USER_PLAYERS], shoot_inputs[:config.USER_PLAYERS])

    def refresh(self) -> None:
        """Refreshes the display to redraw everything.
        """
        self.surface.fill(self.COLOR)
        self.game.draw(self.surface)
        pygame.display.flip()

    def get_user_input(self) -> Tuple[List[Tuple[float, float]], List[Optional[Direction]]]:
        """Gets the user raw input from all sources in a list.
        """
        pressed = pygame.key.get_pressed()

        move_inputs = []
        for source in config.MOVE_SOURCES:
            source_input = [0.0, 0.0]
            if pressed[source[0]]:
                source_input[0] -= 1
            if pressed[source[1]]:
                source_input[0] += 1
            if pressed[source[2]]:
                source_input[1] -= 1
            if pressed[source[3]]:
                source_input[1] += 1
            move_inputs.append((source_input[0], source_input[1]))
        for joystick in self.joysticks:
            move_inputs.append((joystick.get_axis(0), joystick.get_axis(1)))

        shoot_inputs = []
        for source in config.SHOOT_SOURCES:
            if pressed[source[0]]:
                shoot_inputs.append(Direction.WEST)
                continue
            elif pressed[source[1]]:
                shoot_inputs.append(Direction.EAST)
                continue
            elif pressed[source[2]]:
                shoot_inputs.append(Direction.NORTH)
                continue
            elif pressed[source[3]]:
                shoot_inputs.append(Direction.SOUTH)
                continue
            else:
                shoot_inputs.append(None)

        return move_inputs, shoot_inputs
