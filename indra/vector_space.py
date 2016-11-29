"""
vector_space.py
The way agents interact is through prehensions.
This implements prehensions as vector spaces.
"""

import math
import numpy as np
import indra.prehension as pre
# import logging

# x and y indices
X = 0
Y = 1

# Set up constants for some common vectors: this will save time and memory.
X_VEC = np.array([1, 0])
Y_VEC = np.array([0, 1])
NULL_VEC = np.array([0, 0])
NEUT_VEC = np.array([.7071068, .7071068])


def from_vector(v):
    """
    Convenience method to turn a vector into a prehension.
    """
    vspace = VectorSpace()
    vspace.vector = v
    return vspace


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    else:
        return v / norm


class VectorSpace(pre.Prehension):
    """
    We need to put definition of a vector space here.
    """

# we must pre-declare these, then use them, then init them at the bottom
#  of the file.
    X_PRE = None
    Y_PRE = None
    NULL_PRE = None
    NEUT_PRE = None


    def __init__(self, x=0, y=0):
        super().__init__()
        self.vector = np.array([x, y])

    def __str__(self):
        return ("x: %f, y: %f" % (self.vector[X], self.vector[Y]))

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        through vector addition.
        other: prehension to prehend
        """
        return from_vector(self.vector + other.vector)

    def intensify(self, a):
        """
        Here this is scalar multiplication of a vector.
        a: scalar to multiply by.
        """
        return from_vector(self.vector * a)

    def direction(self):
        """
        This gets us the orientation of the vector: x, y, or neutral.
        We use it, for instance, to set an agent's market stance to
        buy or sell.
        """
        if self.vector[X] > self.vector[Y]:
            return VectorSpace.X_PRE
        elif self.vector[X] < self.vector[Y]:
            return VectorSpace.Y_PRE
        else:
            return VectorSpace.NEUT_PRE

    def project(self, x_or_y):
        """
        Projects the vector onto the x or y axis.
        Pass in X or Y as declared above.
        """
        return self.vector[x_or_y]

    def equals(self, other):
        """
        For prehensions of the base type, they are equal
        when their vetors are equal.
        """
        return np.array_equal(self.vector, other.vector)

    def reverse(self):
        """
        Reverse the vector.
        Reflection across line y = x.
        """
        new_vec = np.array(np.flipud(self.vector))
        return from_vector(new_vec)

    def normalize(self):
        """
        Return a normalized prehension.
        If we get the NULL prehension, just return it.
        """
        if self.equals(VectorSpace.NULL_PRE):
            return VectorSpace.NULL_PRE
        else:
            return from_vector(normalize(self.vector))


# Now we actually initialize the prehensions we declared above.
#  This can't be done earlier, since VectorSpace was just defined.
VectorSpace.X_PRE = from_vector(X_VEC)
VectorSpace.Y_PRE = from_vector(Y_VEC)
VectorSpace.NULL_PRE = from_vector(NULL_VEC)
VectorSpace.NEUT_PRE = from_vector(NEUT_VEC)


def stance_pct_to_pre(pct, x_or_y):
    """
    pct is our % of the way to the y-axis from
    the x-axis around the unit circle. (If x_or_y == Y, it is the opposite.)
    It will return the x, y coordinates of the point that % of the way.
    I.e., .5 returns NEUT_VEC, 0 returns X_VEC.
    """
    if x_or_y == Y:
        pct = 1 - pct
    if pct == 0:
        return VectorSpace.X_PRE
    elif pct == .5:
        return VectorSpace.NEUT_PRE
    elif pct == 1:
        return VectorSpace.Y_PRE
    else:
        angle = 90 * pct
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        return VectorSpace(x, y)
