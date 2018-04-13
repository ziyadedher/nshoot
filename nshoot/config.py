"""Game-wide configuration files.
"""

from typing import Tuple, List

from pygame import *


SCREEN_SIZE = WIDTH, HEIGHT = (800, 800)
SCREEN_CAPTION = "nshoot"

NUM_PLAYERS = 2
MOVE_SOURCES: List[Tuple[int, int, int, int]] = [(K_a, K_d, K_w, K_s)]
SHOOT_SOURCES: List[Tuple[int, int, int, int]] = [(K_LEFT, K_RIGHT, K_UP, K_DOWN)]
USER_PLAYERS: int = min(len(MOVE_SOURCES), len(SHOOT_SOURCES))

DEFAULT_STATS = (10, 400, 100)

REFRESH_RATE: int = 60
