"""
prehension.py
The way agents interact is through prehensions.
This is an abstract implementation of a prehension.
Sub-class this to instantiate an implementation.
"""

from abc import abstractmethod
# import logging


class Prehension:
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
                unchanged.
            d.  Invertibility: For any prehension, there is another prehension
                that combines with it to produce the null prehension.
        prehensions MAY also have another operator, *, such that:
        The operation *, which we will call “intensify” (although it may also
            de-intensify) accepts an element of R and an element of G
            (a prehension), and produces an element of G.
        Axioms:
            a.  a, b member G:
                i.  (a + b)x = ax + bx
                ii. a(x + y) = ax + ay

    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def prehend(self, other):
        """
        A prehension prehends another prehension.
        Must return a prehension.
        """
        return Prehension()


    def equals(self, other):
        """
        However descendants decide if prehensions are equal.
        """
        return True
