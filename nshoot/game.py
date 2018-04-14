"""Manages all aspects of displaying and interacting with the game.

This module manages interaction of the user with the game, including viewing and input.
"""

from typing import List, Tuple, Optional

import sys
import math
import random

import pygame
from nshoot import config
from nshoot.info import GameInformation
from nshoot.strategy import Strategy
from nshoot.elements import Player, Bullet
from nshoot.utils import Position, Bounds


class Game:
    """A game instance that controls all underlying aspects of the game including simulation.
    """
    players: List[Player]
    bullets: List[Bullet]

    def __init__(self, num_players: int = config.DEFAULT_NUM_PLAYERS,
                 player_ids: List[str] = config.DEFAULT_PLAYER_IDS,
                 stats: Optional[List[Tuple[int, int, int, int]]] = None,
                 strategies: List[Strategy] = config.DEFAULT_STRATEGIES):
        """Initializes this game instance with the given number of players <num_players>
        and the statistics of each player <stats> with the strategy of each player <strategy>.
        """
        self.players = []
        self.bullets = []

        stats = stats + [config.DEFAULT_STATS] * (num_players - len(stats))\
            if stats else config.DEFAULT_PLAYER_STATS
        for i in range(num_players):
            player = Player(player_ids[i], *stats[i], strategy=strategies[i])

            bounds = Bounds(x_max=config.WIDTH, x_min=0, y_max=config.HEIGHT, y_min=0)
            position = Position(random.randint(0, config.WIDTH), random.randint(0, config.HEIGHT))

            player.set_bounds(bounds)
            player.set_position(position)

            self.players.append(player)

    def _get_game_information(self) -> GameInformation:
        """Gets the information about this game.
        """
        player_information = {}
        for player in self.players:
            player_information[player.player_id] = player.get_info()

        bullet_information = []
        for bullet in self.bullets:
            bullet_information.append(bullet.get_info())

        return GameInformation(player_information, bullet_information)

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

    def _register_dead(self) -> None:
        """Registers any players that should be dead.
        """
        for player in self.players:
            if player.is_dead():
                self.players.remove(player)

    def update(self, delta_time: float) -> None:
        """Update the game internal state taking into consideration the given <delta_time>.
        """
        game_info = self._get_game_information()

        for player in self.players:
            player.strategy.update_info(game_info)
            move_vector, shoot_vector = player.strategy.get_move()
            player.move(move_vector, delta_time)

            # TODO: fix horrible code
            for other_player in self.players:
                if other_player == player:
                    continue
                dist = math.hypot(player.position.x - other_player.position.x,
                                  player.position.y - other_player.position.y)
                if dist <= player.RADIUS + other_player.RADIUS:
                    player.move((-move_vector[0], -move_vector[1]), delta_time)
                    break

            if shoot_vector is not None:
                bullet = player.shoot(shoot_vector)
                if bullet is not None:
                    self.bullets.append(bullet)

        for bullet in self.bullets:
            bullet.move(delta_time)

        self._register_hits()
        self._register_dead()

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
        """Updates the game view considering the given given <delta_time>
        which is the time elapsed since the last frame in seconds.
        """
        self.game.update(delta_time)

    def refresh(self) -> None:
        """Refreshes the display to redraw everything.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed = pygame.key.get_pressed()
        if any(pressed[key] for key in sum(config.SHOOT_SOURCES, ())):
            pygame.mixer.Sound('bang.ogg').play()

        self.surface.fill(self.COLOR)
        self.game.draw(self.surface)
        pygame.display.flip()
