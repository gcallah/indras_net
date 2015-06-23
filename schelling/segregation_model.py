# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@author: Brandon
"""

''' Segregation Model '''

import indra.grid_agent as ga
import indra.grid_env as grid

BLUE_AGENT = "BlueAgent"
RED_AGENT = "RedAgent"
GREEN_AGENT = "GreenAgent"


class SegregationAgent(ga.GridAgent):
    """
    An agent that moves location pending it's neighbors' types
    """
    def __init__(self, name, goal, tolerance, nsize=1):
        super().__init__(name, goal)
        assert tolerance > 0.0 and tolerance < 1.0, "Tolerance must be 0 - 1"
        self.tolerance = tolerance
        self.hood_size = nsize

    def act(self):
        like_me = 0
        total_neighbors = 0

        for neighbor in self.neighbor_iter(distance=self.hood_size):
            total_neighbors += 1
            if self.get_type() == neighbor.get_type():
                like_me += 1

        if total_neighbors > 0:
            if like_me / total_neighbors < self.tolerance:
                self.env.move_to_empty(self)


class BlueAgent(SegregationAgent):
    """
    Just a type with no code
    """


class RedAgent(SegregationAgent):
    """
    Just a type with no code
    """


class GreenAgent(SegregationAgent):
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
        self.agents.set_var_color(BLUE_AGENT, 'b')
        self.agents.set_var_color(RED_AGENT, 'r')
        self.num_moves = 0
        self.move_hist = []

    def move_to_empty(self, agent):
        super().move_to_empty(agent)
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
