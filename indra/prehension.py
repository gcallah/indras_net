"""
prehension.py
The way agents interact is through prehensions.
entity.py currently has another notion of prehension: that one
and this one must be combined in the future.
The base implementation of a prehension is as a vector.
Sub-class this to instantiate another implementation.
"""

import numpy as np
# import logging


class Prehension():
    """
    All prehensions must have the following properties:
        The operation +, which we will call “prehend”, accepts two prehensions
            as arguments and produces a third prehension.
        Axioms:
            a.  Closure: Every prehending involving two prehensions will produce
                a prehension.
            b.  Associativity: (a + b) + c = a + (b + c)
            In a typical agent model, this will mean that we must ensure that,
                say, a neighborhood can interact with a neighborhood (b + c),
                and then with an agent (a + (b + c)). Furthermore, this must
                produce an identical prehension to that produced by an agent
                interacting with one neighborhood and then another one
                ((a + b) + c).
            c.  Identity: Any prehension prehending the null prehension produces
                itself.
            d.  Invertibility: For any prehension, there is another prehension
                that combines with it to produce the null prehension.
        The operation *, which we will call “intensify” (although it may also
            de-intensify) accepts an element of R and an element of G
            (a prehension), and produces an element of G.
        Axioms:
            a.  a, b member G:
                i.  (a + b)x = ax + bx
                ii. a(x + y) = ax + ay

    """

    @classmethod
    def from_vector(cls, v):
        p = Prehension()
        p.vector = v
        return p

    def __init__(self, x=0, y=0):
        self.vector = np.array([x, y])

    def prehend(self, other):
        return Prehension.from_vector(self.vector + other.vector)

    def intensify(self, a):
        return Prehension.from_vector(self.vector * a)
