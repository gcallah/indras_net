"""
This file defines Space, which is a collection
of agents related spatially.
"""
# from random import randint
from composite import Composite


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2?
    """
    return(x < x1 or x >= x2
           or y < y1 or y >= y2)


class Space(Composite):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width, height, attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)
        self.width = width
        self.height = height
        # default is to randomly place members:
        if self.members is not None:
            for mbr in self.members:
                pass

    def distance(self, agent1, agent2):
        return 0
