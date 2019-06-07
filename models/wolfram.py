"""
    This is rm -f ./.git/index.lock re-written in indra.
"""

from indra.env import Env
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE

X = 0
Y = 1

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# states
B = 1
W = 0

STATE_MAP = {B: BLACK, W: WHITE}

# Some rule dictionaries:
RULE30 = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

GRID_WIDTH = 30
GRID_HEIGHT = 30


def setup():
    black = Composite("black", {"color": BLACK})
    white = Composite("white", {"color": WHITE})
    wolframEnv = Env("wolframEnv", height=GRID_HEIGHT, width=GRID_WIDTH)
    return (black, white, wolframEnv)


def main():
    (black, white, wolframEnv) = setup()
    wolframEnv()
    return 0


if __name__ == "__main__":
    main()
