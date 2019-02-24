"""
This file defines Space, which is a collection
of agents related spatially.
"""
from random import randint
from math import sqrt
from indra2.composite import Composite, is_composite

DEF_WIDTH = 10
DEF_HEIGHT = 10

DEBUG = True


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2?
    """
    return(x < x1 or x >= x2
           or y < y1 or y >= y2)


def distance(a1, a2):
    """
    We're going to return the distance between two objects. That calculation
    is easy if they are both located in space, but what if one of them is
    not? For now, we will return 0, but is that right?
    """
    if (not a1.is_located()) or (not a2.is_located()):
        return 0.0
    else:
        return sqrt(
            ((a2.get_x() - a1.get_x()) ** 2)
            + ((a2.get_y() - a1.get_y()) ** 2)
        )


def in_hood(agent, other, hood_sz):
    d = distance(agent, other)
    if DEBUG:
        print("Distance between " + str(agent)
              + " and " + str(other) + " is "
              + str(d))
    return d < hood_sz


class Space(Composite):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width=DEF_WIDTH, height=DEF_HEIGHT,
                 attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)
        self.width = width
        self.height = height
        # by making two class methods for place_members and
        # place_member, we allow two places to override
        self.place_members(self.members)

    def place_members(self, members):
        """
        Locate all members of this space in x,y grid.
        Default is to randomly place members.
        """
        if members is not None:
            for nm, mbr in members.items():
                if not is_composite(mbr):  # by default don't locate groups
                    self.place_member(mbr)
                else:  # place composite's members
                    self.place_members(mbr.members)

    def rand_x(self):
        """
        Return a random x-value between 0 and this space's width.
        """
        return randint(0, self.width - 1)

    def rand_y(self):
        """
        Return a random y-value between 0 and this space's height.
        """
        return randint(0, self.height - 1)

    def place_member(self, mbr):
        """
        By default, locate a member at a random x,y spot in our grid.
        """
        if not is_composite(mbr):
            mbr.set_pos(self.rand_x(), self.rand_y())
        else:
            self.place_members(mbr.members)

    def __iadd__(self, other):
        super().__iadd__(other)
        self.place_member(other)
        return self

    def neighborhood(self, agent, distance=1.0):
        """
        This will return a subset of this space that is within
        `distance` of `agent`.
        """
        hood = Composite()
        return hood
