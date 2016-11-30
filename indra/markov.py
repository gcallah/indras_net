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


def create_iden_matrix(n):
    """
    Create a dim1 * dim2 identity matrix.

    Returns: the new matrix.
    """
    matrix_init = [[] for i in range(n)]
    for i in range(0, n): 
        for j in range(0, n): 
            if i == j:
                matrix_init[i].append(1)
            else:
                matrix_init[i].append(0)

    return np.matrix(matrix_init)


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
    It then returns the index of the element that is "on,"
    or None if none are.
    """
    i = 0
    for s in sv.flat:
        if s == 1:
            return i
        i += 1
    return None



def from_matrix(m):
    """
    Takes an numpy matrix and returns a prehension.
    """
    pre = MarkovPre("")
    pre.matrix = m
    return pre


def to_matrix(pre):
    return pre.matrix


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
        return str(self.matrix)

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        as a markov chain process.
        other: prehension to prehend
        """
        if self.matrix.shape[ROWS] == 1:
            return from_matrix(self.matrix * other.matrix)
        else:
            return from_matrix(other.matrix * self.matrix)
