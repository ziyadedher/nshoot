"""Manages all aspects of displaying and interacting with the game.

This module manages interaction of the user with the game, including viewing and input.
"""
from typing import List, Tuple

import sys

import pygame
from nshoot.player import Player, Bounds, Position


class Game:
    """A game instance that controls all underlying aspects of the game including simulation.
    """
    NUM_PLAYERS: int = 2
    players: List[Player]

    def __init__(self):
        """Initializes this game instance.
        """
        self.players = []

        for _ in range(self.NUM_PLAYERS):
            player = Player(10, 400, 10)

            screen_size = pygame.display.get_surface().get_size()
            bounds = Bounds(x_max=screen_size[1], x_min=0, y_max=screen_size[0], y_min=0)
            position = Position(screen_size[1] // 2, screen_size[0] // 2)

            player.set_bounds(bounds)
            player.set_position(position)

            self.players.append(player)

    def update(self, delta_time: float, raw_inputs: List[Tuple[float, float]]) -> None:
        """Update the game based on the given <delta_time> and <raw_inputs> corresponding to each player.
        """
        for _ in range(self.NUM_PLAYERS - len(raw_inputs)):
            raw_inputs.append((0.0, 0.0))
        for i, player in enumerate(self.players):
            player.move(raw_inputs[i], delta_time)


    def draw(self, surface: pygame.Surface) -> None:
        """Draws all objects in this game to the given <surface>.
        """
        for player in self.players:
            player.draw(surface)


class GameView:
    """A game view which controls all displaying and interaction with the game.
    """
    SOURCES: List[list] = [[pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
                           [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]]
    USER_PLAYERS: int = 2

    REFRESH_RATE: int = 60
    COLOR: pygame.Color = pygame.Color("black")

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

        raw_inputs = self.get_user_input()[:self.USER_PLAYERS]
        self.game.update(delta_time, raw_inputs)

    def refresh(self) -> None:
        """Refreshes the display to redraw everything.
        """
        self.surface.fill(self.COLOR)
        self.game.draw(self.surface)
        pygame.display.flip()

    def get_user_input(self) -> List[Tuple[float, float]]:
        """Gets the user raw input from all sources in a list.
        """
        pressed = pygame.key.get_pressed()

        raw_inputs = []

        for source in self.SOURCES:
            source_input = [0.0, 0.0]
            if pressed[source[0]]:
                source_input[0] -= 1
            if pressed[source[1]]:
                source_input[0] += 1
            if pressed[source[2]]:
                source_input[1] -= 1
            if pressed[source[3]]:
                source_input[1] += 1
            raw_inputs.append((source_input[0], source_input[1]))

        for joystick in self.joysticks:
            raw_inputs.append((joystick.get_axis(0), joystick.get_axis(1)))

        return raw_inputs
