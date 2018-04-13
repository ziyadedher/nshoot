"""Game-wide configuration files.
"""

from typing import Tuple, List

from pygame import *

from nshoot.strategy import Strategy, IdleStrategy, UserInputStrategy


WIDTH: int = 800
HEIGHT: int = 800
SCREEN_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)
SCREEN_CAPTION: str = "nshoot"

MOVE_SOURCES: List[Tuple[int, int, int, int]] = [(K_a, K_d, K_w, K_s)]
SHOOT_SOURCES: List[Tuple[int, int, int, int]] = [(K_LEFT, K_RIGHT, K_UP, K_DOWN)]

DEFAULT_NUM_PLAYERS: int = 2
DEFAULT_STRATEGIES: List[Strategy] = [UserInputStrategy(MOVE_SOURCES[0], SHOOT_SOURCES[0]),
                                      IdleStrategy()]

DEFAULT_STATS: Tuple[int, int, int, int] = (10, 400, 100, 10)
DEFAULT_BULLET_SPEED: int = 800

REFRESH_RATE: int = 60
