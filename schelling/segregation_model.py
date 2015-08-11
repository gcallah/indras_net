# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@author: Brandon
"""

''' Segregation Model '''

import random
import indra.grid_agent as ga
import indra.grid_env as grid

BLUE_AGENT = "BlueAgent"
RED_AGENT = "RedAgent"


class SegregationAgent(ga.GridAgent):
    """
    An agent that moves location based on its neighbors' types
    """
    def __init__(self, name, goal, min_tol, max_tol, max_detect=1):
        super().__init__(name, goal, max_detect=max_detect)
        self.tolerance = random.uniform(max_tol, min_tol)

    def eval_env(self, env_vars):
        """
        Use the results of surveying the env to decide what to do.
        """
        (resembles_me, total_neighbors) = env_vars
        if total_neighbors > 0:
            return resembles_me / total_neighbors < self.tolerance
        else:
            return False  # everyone is OK with no neighbors

    def respond_to_cond(self):
        self.move_to_empty()

    def survey_env(self):
        """
        Look around and see what our env holds for us.
        """
        super().survey_env()
        resembles_me = 0
        total_neighbors = 0
        for neighbor in self.neighbor_iter(view=self.my_view):
            total_neighbors += 1
            if self.get_type() == neighbor.get_type():
                resembles_me += 1
        return (resembles_me, total_neighbors)


class BlueAgent(SegregationAgent):
    """
    Just a type with no code
    """


class RedAgent(SegregationAgent):
    """
    Just a type with no code
    """


class SegregationEnv(grid.GridEnv):

    def __init__(self, name, height, width, torus=False,
                 model_nm="Segregation"):

        super().__init__(name, height, width, torus=False,
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
