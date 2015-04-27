"""
obst_model.py
Testing obstacle detection.
"""
# import logging
import random
import indra.grid_agent as ga

X = 0
Y = 1


def get_rand_coord(coord, dist, low_lim, high_lim):
    new_coord = random.randint(max(coord - dist, low_lim),
                               min(coord + dist, high_lim))
    return new_coord


class ObstacleAgent(ga.GridAgent):
    """
    An agent that avoids obstacles in its env.
    """

    def __init__(self, name, goal, max_move=2, max_detect=2):
        super().__init__(name, goal, max_move=max_move,
                         max_detect=max_detect)

    def act(self):
        (x, y) = self.pos
        w = self.env.get_width()
        h = self.env.get_height()
        print("In oa act(); max_move = %i" % self.max_move)
        new_x = get_rand_coord(x, self.max_move, 0, w)
        new_y = get_rand_coord(y, self.max_move, 0, h)
        print("In oa act(); x = %i, y = %i, new_x = %i, new_y = %i"
              % (x, y, new_x, new_y))
        self.pos = (new_x, new_y)
