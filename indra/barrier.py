"""
This file defines barrier, a type of composite,
which blocks agent's movement
"""
from indra.composite import Composite


class Barrier(Composite):
    """
    The barrier class
    """

    def __init__(self, name, permeable=False):
        """
        Should include, dimension of the barrier like height and width,
        or a list of coordinates for the inital barrier?
        permeable-can agents "jump" over the barrier?
        """

    def is_blocked(self, coord):
        """
        Check if a coordinate is blocked or not
        """

    def place_barrier(self, coord):
        """
        Inserts a barrier agent at the given coordinate if it is
        not occupied
        """

    def remove_barrier(self, coord):
        """
        Remove a barrier agent at the given coordinate
        """
