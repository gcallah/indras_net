"""
markov.py
The way agents interact is through prehensions.
This implements prehensions as markov chains.
"""

import math
import numpy as np
import random
import indra.prehension as pre
# import logging

ROWS = 0
COLS = 1


def state_vector(vlen, init_state):
    vals = ""
    for i in range(vlen):
        if i == init_state:
            vals = vals + "1 "
        else:
            vals = vals + "0 "
    return np.matrix(vals)


def probvec_to_state(pv):
    state_vec = None
    cum_prob = 0.0
    r = random.random()
    l = pv.shape[COLS]
    for i in range(l):
        cum_prob += pv.item(i)
        if cum_prob >= r:
            state_vec = state_vector(l, i)
            break
    return state_vec


class MarkovPre(pre.Prehension):
    """
    This class manages taking a state vector and a transition matrix
    and turning them into a new state vector, as well as
    creating matrices more easily than numpy.
    """

    def __init__(self, dim1, dim2):
        super().__init__()
        self.dim1 = dim1
        self.dim2 = dim2
        if dim1 == 1:
            self.matrix = np.matrix("1 0 0 0") # for now
        else:
            self.matrix = np.matrix(".95 .05 0 0; 0 0 1 0; "
                                    "0 0 .95 .05; 1 0 0 0")

    def __str__(self):
        return ("markov chain")

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        as a markov chain process.
        other: prehension to prehend
        """
        if self.dim1 == 1:
            return self.matrix * other.matrix
        else:
            return other.matrix * self.matrix
