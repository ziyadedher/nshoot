"""Begin the standalone game.

This module begins execution of the game as a standalone program. It should never be imported,
only executed directly to begin the standalone program.
"""
from nshoot import game


if __name__ == "__main__":
    view = game.GameView((800, 800), "nshoot")
    view.start()
