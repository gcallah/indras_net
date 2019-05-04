"""
    This is wolfram model re-written in indra.
"""

from indra.env import Env


X = 0
Y = 1

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# agent condition strings
BLACK = "Black"
WHITE = "White"

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
    wolfframEnv = Env("wolfframEnv", height=GRID_HEIGHT, width=GRID_WIDTH)
    return wolfframEnv


def main():
    setup()
