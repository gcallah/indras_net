"""
obst_model.py
Testing obstacle detection.
"""
# import logging
import random
import indra.grid_agent as ga

LEFT = (-1, 0)
UP = (0, 1)
RIGHT = (1, 0)
DOWN = (0, -1)
MOVES = [LEFT, UP, RIGHT, DOWN]


def get_rand_vector_mag(dist):
    vector_mag = random.randint(0, dist)
    return vector_mag


def get_rand_direction():
    return random.choice(MOVES)


def new_coord(old, mag, mult, bound):
    return max(0, min(old + mag * mult, bound))


class ObstacleAgent(ga.GridAgent):
    """
    An agent that avoids obstacles in its env.
    """

    def __init__(self, name, goal, max_move=2, max_detect=2):
        super().__init__(name, goal, max_move=max_move,
                         max_detect=max_detect)
        self.wbound = None
        self.hbound = None

    def add_env(self, env):
        super().add_env(env)
        self.wbound = self.env.get_width() - 1
        self.hbound = self.env.get_height() - 1

    def act(self):
        (x, y) = self.get_pos()
        print("In oa act(); max_move = %i" % self.max_move)
        vector_mag = get_rand_vector_mag(self.max_move)
        (x_mult, y_mult) = get_rand_direction()
        new_x = new_coord(x, vector_mag, x_mult, self.wbound)
        new_y = new_coord(y, vector_mag, y_mult, self.hbound)
        print("In oa act(); x = %i, y = %i, new_x = %i, new_y = %i"
              % (x, y, new_x, new_y))
        self.env.move(self, new_x, new_y)
