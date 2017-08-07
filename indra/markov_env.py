"""
markov_env.py

An environment for Markov chain interactions.

"""

# pylint: disable=invalid-name

import indra.grid_env as ge
import indra.markov as markov

X = 0
Y = 1


class MarkovCell(ge.Cell):
    """
    A grid cell that also has a transition matrix
    specific to it.

    Attribute:
        trans_matrix: a transition matrix
    """
    def __init__(self, coords, contents=None, trans_matrix=None):
        super().__init__(coords, contents)
        self.trans_matrix = trans_matrix

    def __str__(self):
        return str(self.trans_matrix)


class MarkovEnv(ge.GridEnv):
    """
    An env that holds transition matrix for each cell, though strictly speaking,
    it isn't required that the transition matricies must be aquired through
    accessing this cell.
    """

    def __init__(self, name, width, height, trans_str=None, torus=False,
                 matrix_dim=2, model_nm=None, preact=False, postact=False,
                 mobile_agents=False, props=None):
        """
        Create a new markov env. By default the transition matrix is identity.
        """
        if trans_str is None:
            self.def_trans_matrix = markov.from_matrix(markov.create_iden_matrix(matrix_dim))
        else:
            self.def_trans_matrix = markov.MarkovPre(trans_str)
        super().__init__(name, width, height, torus, preact,
                         postact, model_nm=model_nm, props=props)

    def __new_cell__(self, coords):
        return MarkovCell(coords, trans_matrix=self.def_trans_matrix)

    def get_pre(self, agent, n_census):
        cell = self._get_cell(agent.pos[X], agent.pos[Y])
        return cell.trans_matrix

    def set_trans(self, coords, trans):
        cell = self._get_cell(coords[X], coords[Y])
        cell.trans_matrix = trans

    def neighborhood_census(self, agent):
        """
        Counts number of each type in a neighborhood. Stores
        the result in a dictionary.
        """
        n_census = {}

        for neighbor in agent.neighbor_iter():
            if neighbor.ntype in n_census:
                n_census[neighbor.ntype] += 1
            else:
                n_census[neighbor.ntype] = 1

        return n_census
