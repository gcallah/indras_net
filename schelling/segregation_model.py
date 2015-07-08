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
        assert min_tol > 0.0 and min_tol < 1.0, "Tolerance must be 0 - 1"
        assert max_tol > 0.0 and max_tol < 1.0, "Tolerance must be 0 - 1"
        self.tolerance = random.uniform(max_tol, min_tol)

    def act(self):
        """
        We see if our neighborhood is OK, given our tolerance.
        If not, move and test again, until good hood is found.
        """
        super().act()
        (resembles_me, total_neighbors) = self.survey_env(self.my_view)
        if not self.evaluate_env(resembles_me, total_neighbors):
            found_good_hood = False
            max_tries = 4  # we don't want to keep looking forever!
            tries = 0
            while not found_good_hood and tries < max_tries:
                tries += 1
                # it is simplest just to move to a random spot,
                # and then see if it is OK; if not, move again
                self.env.move_to_empty(self)
                (resembles_me, total_neighbors) = self.survey_env(self.my_view)
                if self.evaluate_env(resembles_me, total_neighbors):
                    found_good_hood = True

    def evaluate_env(self, resembles_me, total_neighbors):
        """
        Use the results of surveying the env to decide what to do.
        """
        if total_neighbors > 0:
            return resembles_me / total_neighbors >= self.tolerance
        else:
            return True  # everyone is OK with no neighbors

    def survey_env(self, this_view):
        """
        Look around and see what our env holds for us.
        """
        resembles_me = 0
        total_neighbors = 0
        for neighbor in self.neighbor_iter(view=this_view):
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
