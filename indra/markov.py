"""
markov.py
The way agents interact is through prehensions.
This implements prehensions as markov chains.
"""

import math
import numpy as np
import indra.prehension as pre
# import logging


class MarkovPre(pre.Prehension):
    """
    This class manages taking a state vector and a transition matrix
    and turning them into a new state vector, as well as
    creating matrices more easily than numpy.
    """

    @classmethod
    def state_vector(vlen, init_state):
        m = MarkovPre(1, vlen)
        vals = ""
        for i in range(vlen):
            if i = init_state:
                vals = vals + "1 "
            else
                vals = vals + "0 "
        m.matrix = np.matrix(vals)
        return m

    def __init__(self, dim1, dim2):
        super().__init__()
        self.dim1 = dim1
        self.dim2 = dim2
        if dim1 == 1:
            self.matrix = np.matrix("1 0 0 0") # for now
        else:
            self.matrix = np.matrix(".95 .05 0 0; 0 0 1 0;
                                    0 0 .95 .05; 1 0 0 0")

    def __str__(self):
        return ("markov chain")

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        a markov chain
        other: prehension to prehend
        """
        if self.dim1 == 1:
            return self.matrix * other.matrix
        else
            return other.matrix * self.matrix
