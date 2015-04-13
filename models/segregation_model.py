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
    An agent that prints its neighbors when asked to act
    """
    def __init__(self, name, goal, tolerance):
        super().__init__(name, goal)
        self.tolerance = tolerance

    def act(self):
        like_me = 0
        total_neighbors = 0
        (x, y) = self.env.get_pos_components(self)
        for neighbor in self.env.neighbor_iter(x, y):
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

        super().__init__("Segregation", height, width, torus=False,
                         model_nm=model_nm)

        self.plot_title = "Segregation"

        # setting our colors adds varieties as well!
        self.agents.set_var_color(BLUE_AGENT, 'b')
        self.agents.set_var_color(RED_AGENT, 'r')
        # self.agents.set_var_color(GREEN_AGENT, 'g')
