"""
obst_model.py
Testing obstacle detection.
"""
# import logging
import random
import indra.grid_agent as ga

WEST = (-1, 0)
NW = (-1, 1)
NORTH = (0, 1)
NE = (1, 1)
EAST = (1, 0)
SE = (1, -1)
SOUTH = (0, -1)
SW = (-1, -1)
MOVES = [WEST, NW, NORTH, NE, EAST, SE, SOUTH, SW]


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
        """
        We capture our env's dimensions so we don't
        have to keep fetching them.
        If we create envs that re-size themselves,
        this code must change!
        """
        super().add_env(env)
        self.wbound = self.env.get_width() - 1
        self.hbound = self.env.get_height() - 1

    def act(self):
        """
        Our act is to move to a random cell.
        """
        (x, y) = self.get_pos()
        print("In oa act(); max_move = %i" % self.max_move)
        vector_mag = get_rand_vector_mag(self.max_move)
        (x_mult, y_mult) = get_rand_direction()
        new_x = new_coord(x, vector_mag, x_mult, self.wbound)
        new_y = new_coord(y, vector_mag, y_mult, self.hbound)
        if (new_x != x) or (new_y != y):  # we are moving
            (new_x, new_y) = self._premove(x, y, new_x, new_y)
        print("In oa act(); x = %i, y = %i, new_x = %i, new_y = %i"
              % (x, y, new_x, new_y))
        self.env.move(self, new_x, new_y)

    def _getdir(self, diff):
        if diff > 0:
            return 1
        elif diff == 0:
            return 0
        else:
            return -1

    def _premove(self, x, y, new_x, new_y):
        """
        Look for obstacles in the path to new_x, new_y,
        and stop short if they are there.
        """
        x_diff = new_x - x
        y_diff = new_y - y
        x_dir = self._getdir(x_diff)
        y_dir = self._getdir(y_diff)
        last_x = x
        last_y = y
        pot_x = x + x_dir
        pot_y = y + y_dir
        while x_diff != 0 and y_diff != 0:
            if not self.env.is_cell_empty(pot_x, pot_y):
                return (last_x, last_y)
            if(x_diff > 0):
                x_diff -= x_dir
            if(y_diff > 0):
                y_diff -= y_dir
            last_x = pot_x
            last_y = pot_y
            pot_x += x_dir
            pot_y += y_dir

        return (new_x, new_y)
