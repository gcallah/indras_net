# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@author: Brandon Logan
    Gene Callahan
Implements Thomas Schelling's segregation model.
An agent moves when she finds herself to be "too small"
of a minority in a particular neighborhood.
"""


import random
import indra.prehension as pre
import indra.prehension_agent as pa
import indra.grid_env as grid

BLUE = True
RED = False
BLUE_AGENT = "BlueAgent"
RED_AGENT = "RedAgent"


class SegregationAgent(pa.PrehensionAgent):
    """
    An agent that moves location based on its neighbors' types
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, max_move=max_move, max_detect=max_detect)
        self.tolerance = random.uniform(max_tol, min_tol)
        self.stance = None

    def eval_env(self, other_pre):
        """
        Use the results of surveying the env to decide what to do.
        """

    def respond_to_cond(self, env_vars=None):
        self.move_to_empty()


class BlueAgent(SegregationAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, min_tol, max_tol,
                         max_move=max_move, max_detect=max_detect)
        self.stance = pre.stance_pct_to_pre(self.tolerance, y=BLUE)


class RedAgent(SegregationAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, min_tol, max_tol,
                         max_move=max_move, max_detect=max_detect)
        self.stance = pre.stance_pct_to_pre(self.tolerance, y=RED)


class SegregationEnv(grid.GridEnv):

    def __init__(self, name, width, height, torus=False,
                 model_nm="Segregation"):

        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm)
        self.plot_title = name
        # setting our colors adds varieties as well!
        self.set_var_color(BLUE_AGENT, 'b')
        self.set_var_color(RED_AGENT, 'r')
        self.num_moves = 0
        self.move_hist = []

    def move_to_empty(self, agent, grid_view=None):
        super().move_to_empty(agent, grid_view)
        self.num_moves += 1

    def census(self, disp=True):
        """
        Take a census of number of moves.
        """

        self.move_hist.append(self.num_moves)
        self.user.tell("Moves per turn: " + str(self.move_hist))
        self.num_moves = 0

    def record_results(self, file_nm):
        f = open(file_nm, 'w')
        for num_moves in self.move_hist:
            f.write(str(num_moves) + '\n')
        f.close()
