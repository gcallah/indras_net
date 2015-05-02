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
DIRECTIONS = [WEST, NW, NORTH, NE, EAST, SE, SOUTH, SW]


def get_rand_vector_mag(dist):
    vector_mag = random.randint(1, dist)
    return vector_mag


def get_rand_direction():
    return random.choice(DIRECTIONS)


def get_steps(x, y, vector_mag, x_step, y_step):
    steps = []
    print("vector_mag = %i" % (vector_mag))
    for i in range(0, vector_mag):
        x += x_step
        y += y_step
        steps.append((x, y))
    print(str(steps))
    return steps


class Obstacle(ga.GridAgent):
    """
    An obstacle.
    """

    def __init__(self, name, goal="Be in the way."):
        super().__init__(name, goal, max_move=0, max_detect=0)

    def act(self):
        pass


class ObstacleAgent(ga.GridAgent):
    """
    An agent that avoids obstacles in its env.
    Properties:
        max_move: the furthest agent can move in one turn
        tolerance: how close we feel OK getting near an obstacle
    """

    def __init__(self, name, goal, max_move=2, max_detect=2,
                 tolerance=1):
        super().__init__(name, goal, max_move=max_move,
                         max_detect=max_detect)
        self.tolerance = tolerance
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
        Our act is to move to a random cell,
        on a straight line or a diagonal.
        """
        (x, y) = self.get_pos()
        print("In oa act(); max_move = %i" % self.max_move)
        vector_mag = get_rand_vector_mag(self.max_move)
        (x_step, y_step) = get_rand_direction()
        steps = get_steps(x, y, vector_mag, x_step, y_step)
        (new_x, new_y) = self._check_for_obst(steps, x, y)
        print("In oa act(); x = %i, y = %i, new_x = %i, new_y = %i"
              % (x, y, new_x, new_y))
        self.env.move(self, new_x, new_y)

    def _check_for_obst(self, steps, clear_x, clear_y):
        """
        Look for obstacles in the path 'steps'
        and stop short if they are there.
        clear_x and clear_y start out as the agent's current pos,
        which must, of course, be clear for this agent to occupy!
        """
        for (x, y) in steps:
            if not self.env.is_cell_empty(x, y):
                return (clear_x, clear_y)
            else:
                clear_x = x
                clear_y = y
        return (clear_x, clear_y)
