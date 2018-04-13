"""Manages all aspects of displaying and interacting with the game.

This module manages interaction of the user with the game, including viewing and input.
"""
from typing import List, Tuple, Optional

import sys

import pygame
from nshoot.elements import Player, Bullet
from nshoot.utils import Position, Bounds, Direction


class Game:
    """A game instance that controls all underlying aspects of the game including simulation.
    """
    NUM_PLAYERS: int = 2
    players: List[Player]
    bullets: List[Bullet]

    def __init__(self):
        """Initializes this game instance.
        """
        self.players = []
        self.bullets = []

        for _ in range(self.NUM_PLAYERS):
            player = Player(10, 400)

            screen_size = pygame.display.get_surface().get_size()
            bounds = Bounds(x_max=screen_size[1], x_min=0, y_max=screen_size[0], y_min=0)
            position = Position(screen_size[1] // 2, screen_size[0] // 2)

            player.set_bounds(bounds)
            player.set_position(position)

            self.players.append(player)

    def update(self, delta_time: float,
               move_inputs: List[Tuple[float, float]],
               shoot_inputs: List[Optional[Direction]]) -> None:
        """Update the game based on the given <delta_time>.
        Also <move_inputs> and <shoot_inputs> corresponding to each player.
        """
        for _ in range(self.NUM_PLAYERS - len(move_inputs)):
            move_inputs.append((0.0, 0.0))
        for _ in range(self.NUM_PLAYERS - len(shoot_inputs)):
            shoot_inputs.append(None)

        for i, player in enumerate(self.players):
            player.move(move_inputs[i], delta_time)
            if shoot_inputs[i] is not None:
                self.bullets.append(player.shoot(shoot_inputs[i]))

        for bullet in self.bullets:
            bullet.move(delta_time)
            if (bullet.position.x > pygame.display.get_surface().get_width() or bullet.position.x < 0
                    or bullet.position.y > pygame.display.get_surface().get_height() or bullet.position.y < 0):
                    self.bullets.remove(bullet)

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
    MOVE_SOURCES: List[Tuple[int, int, int, int]] = [(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)]
    SHOOT_SOURCES: List[Tuple[int, int, int, int]] = [(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)]
    USER_PLAYERS: int = 2

    REFRESH_RATE: int = 60
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
            if since_last_refresh > 1 / self.REFRESH_RATE:
                self.refresh()
                since_last_refresh = 0

    def update(self, delta_time: float) -> None:
        """Updates the game with the given <delta_time> which is the time elapsed since the last frame in seconds.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        move_inputs, shoot_inputs = self.get_user_input()
        self.game.update(delta_time, move_inputs[:self.USER_PLAYERS], shoot_inputs[:self.USER_PLAYERS])

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
        for source in self.MOVE_SOURCES:
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
        for source in self.SHOOT_SOURCES:
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
