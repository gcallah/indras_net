"""
markov_env.py

An environment for Markov chain interactions.

"""

# pylint: disable=invalid-name

import indra.grid_env as ge
import indra.markov as markov

class MarkovEnv(ge.GridEnv):
    """
    """

    def __init__(self, name, width, height, dim, torus=False,
                 model_nm=None, preact=False, postact=False):
        """
        Create a new markov env
        """
        super().__init__(name, width, height, torus, preact, postact, model_nm)
        self.trans_matrix = MarkovPre(dim, dim)

    def get_pre(self):
        return self.trans_matrix
