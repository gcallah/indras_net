"""
This file defines Space, which is a collection
of agents related spatially.
"""
from random import randint
from composite import Composite, is_composite


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
        # by making tow class methods for place_members and
        # place_member, we allow two places to override
        self.place_members()

    def distance(self, agent1, agent2):
        return 0

    def place_members(self):
        """
        Locate all members of this space in x,y grid.
        Default is to randomly place members.
        """
        if self.members is not None:
            for mbr in self.members:
                if not is_composite(mbr):  # by default don't locate groups
                    self.place_member(mbr)

    def rand_x(self):
        """
        Return a random x-value between 0 and this space's width.
        """
        return randint(0, self.width)

    def rand_y(self):
        """
        Return a random y-value between 0 and this space's height.
        """
        return randint(0, self.height)

    def place_member(self, mbr):
        """
        By default, locate a member at a random x,y spot in our grid.
        """
        mbr.set_pos(self.rand_x(), self.rand_y())
