"""Begin the standalone game.

This module begins execution of the game as a standalone program. It should never be imported,
only executed directly to begin the standalone program.
"""

from nshoot import game, config


if __name__ == "__main__":
    view = game.GameView(config.SCREEN_SIZE, config.SCREEN_CAPTION)
    view.start()
