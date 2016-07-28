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

def get_state(sv):
    """
    This method takes a state vector, sv.
    It then return the index of the element that is "on,"
    or None if none are.
    """
    i = 0
    for s in sv.flat:
        if s == 1:
            return i
        i += 1
    return None


class MarkovPre(pre.Prehension):
    """
    This class manages taking a state vector and a transition matrix
    and turning them into a new state vector, as well as
    creating matrices more easily than numpy.
    """

    def __init__(self, str_matrix):
        """
        str_matrix is the matrix represented as a string in numpy fashion.
        """
        super().__init__()
        self.matrix = np.matrix(str_matrix)

    def __str__(self):
        return ("markov chain")

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        as a markov chain process.
        other: prehension to prehend
        """
        if self.matrix.shape[ROWS] == 1:
            return self.matrix * other.matrix
        else:
            return other.matrix * self.matrix
