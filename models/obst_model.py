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
        (new_x, new_y) = self._premove(x, y, new_x, new_y)
        print("In oa act(); x = %i, y = %i, new_x = %i, new_y = %i"
              % (x, y, new_x, new_y))
        self.env.move(self, new_x, new_y)

    def _premove(self, x, y, new_x, new_y):
        """
        Look for obstacles in the path to new_x, new_y,
        and stop short if they are there.
        """
        x_diff = new_x - x
        y_diff = new_y - y
        # we have four cases: no move, movement on x, on y, or on diagonal
        if y_diff == 0 and x_diff == 0:
            return (new_x, new_y)
        elif y_diff == 0:
            # we walk the x-axis looking for an obstacle
            x_dir = 1
            if x_diff < 0:
                x_dir = -1
            last_x = x
            for potential_x in range(x + x_dir, new_x + x_dir, x_dir):
                if not self.env.is_cell_empty(potential_x, y):
                    return (last_x, y)
                last_x = potential_x
            return (new_x, new_y)
        elif x_diff == 0:
            # we walk the y-axis looking for an obstacle
            y_dir = 1
            if y_diff < 0:
                y_dir = -1
            last_y = y
            for potential_y in range(y + y_dir, new_y + y_dir, y_dir):
                if not self.env.is_cell_empty(x, potential_y):
                    return (x, last_y)
                last_y = potential_y
            return (new_x, new_y)
        else:
            # we walk a diagonal looking for an obstacle
            while x_diff != 0 and y_diff != 0:
                pass
        return (new_x, new_y)
