"""
This file defines Space, which is a collection
of entities related spatially.
"""
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
    """

    def __init__(self, name, width, height, attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)
        self.width = width
        self.height = height

    def distance(self, ent1, ent2):
        return 0
