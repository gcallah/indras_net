"""
This file defines Space, which is a collection
of agents related spatially.
"""
from random import randint
from math import sqrt
from indra.agent import is_composite
from indra.composite import Composite

DEF_WIDTH = 10
DEF_HEIGHT = 10

MAX_WIDTH = 200
MAX_HEIGHT = 200

DEF_MAX_MOVE = 2

DEBUG = False
DEBUG2 = False


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2?
    """
    return(x < x1 or x >= x2
           or y < y1 or y >= y2)


def bound(point, lower, upper):
    return min(max(point, lower), upper - 1)


def distance(a1, a2):
    """
    We're going to return the distance between two objects. That calculation
    is easy if they are both located in space, but what if one of them is
    not? For now, we will return 0, but is that right?
    """
    if (not a1.islocated()) or (not a2.islocated()):
        return 0.0
    else:
        return sqrt(
            ((a2.get_x() - a1.get_x()) ** 2)
            + ((a2.get_y() - a1.get_y()) ** 2)
        )


def in_hood(agent, other, hood_sz):
    d = distance(agent, other)
    if DEBUG2:
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
                 attrs=None, members=None, action=None):
        super().__init__(name, attrs=attrs, members=members,
                         action=action)
        self.width = width
        self.height = height

        # the location of members in the space
        self.locations = {}

        # by making two class methods for place_members and
        # place_member, we allow two places to override
        self.place_members(self.members)

    def grid_size(self):
        """
        How big is da grid?
        """
        return self.width * self.height

    def is_full(self):
        """
        Is da grid full?
        """
        return len(self.locations) >= self.grid_size()

    def place_members(self, members, max_move=None):
        """
        Locate all members of this space in x, y grid.
        Default is to randomly place members.
        """
        if members is not None:
            for nm, mbr in members.items():
                if not is_composite(mbr):  # by default don't locate groups
                    self.place_member(mbr, max_move)
                else:  # place composite's members
                    self.place_members(mbr.members, max_move)

    def rand_x(self, low=0, high=None):
        """
        Return a random x-value between 0 and this space's width,
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.width if high is None else high
        return randint(low, high - 1)

    def rand_y(self, low=0, high=None):
        """
        Return a random y-value between 0 and this space's height
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.height if high is None else high
        return randint(low, high - 1)

    def constrain_x(self, x):
        """
        Pull x in bounds if it ain't.
        """
        return bound(x, 0, self.width)

    def constrain_y(self, y):
        """
        Pull y in bounds if it ain't.
        """
        return bound(y, 0, self.height)

    def gen_new_pos(self, mbr, max_move):
        """
        Generate new random position within max_move of current pos.
        """
        low_x = 0
        high_x = self.width
        low_y = 0
        high_y = self.height
        if max_move is not None and mbr.islocated():
            low_x = self.constrain_x(mbr.get_x() - max_move)
            high_x = self.constrain_x(mbr.get_x() + max_move)
            low_y = self.constrain_y(mbr.get_y() - max_move)
            high_y = self.constrain_y(mbr.get_y() + max_move)
        x = self.rand_x(low_x, high_x)
        y = self.rand_y(low_y, high_y)
        return (x, y)

    def is_empty(self, x, y):
        """
        See if cell x,y is empty.
        """
        return (x, y) not in self.locations

    def get_agent_at(self, x, y):
        """
        Return agent at cell x,y
        If cell is empty return None.
        """
        if self.is_empty(x, y):
            return None
        return self.locations[(x, y)]

    def place_member(self, mbr, max_move=None, xy=None):
        """
        By default, locate a member at a random x, y spot in our grid.
        `max_move` constrains where that can be.
        Setting `xy` picks a particular spot to place member.
        `xy` must be a tuple!
        """
        if self.is_full():
            self.user.log("Can't fit no more folks in this space!")
            return None

        if not is_composite(mbr):
            if xy is not None:
                (x, y) = xy  # it had better be a tuple!
            else:
                (x, y) = self.gen_new_pos(mbr, max_move)
            if self.is_empty(x, y):
                if mbr.islocated():
                    self.move_location(x, y, mbr.get_x(), mbr.get_y())
                else:
                    self.add_location(x, y, mbr)
                # if I am setting pos, I am agent's locator!
                mbr.set_pos(self, x, y)
                return (x, y)
            elif (max_move is None) and (xy is None):
                # if the random position is already taken,
                # find the member a new position
                # but if max_move is not None, the hood might be filled!
                # so we need something to detect a full neighborhood as well.
                # and if xy is not None, the user asked for a particular
                # spot: don't give them another, but return None.
                return self.place_member(mbr, max_move)
        else:
            return self.place_members(mbr.members, max_move)

    def __iadd__(self, other):
        super().__iadd__(other)
        self.place_member(other)
        return self

    def add_location(self, x, y, member):
        """
        Add a new member to the locations of positions of members.
        """
        self.locations[(x, y)] = member

    def move_location(self, nx, ny, ox, oy):
        """
        Move a member to a new position, if that position
        is not already occupied.
        """
        if (nx, ny) not in self.locations:
            self.locations[(nx, ny)] = self.locations[(ox, oy)]
            del self.locations[(ox, oy)]

    def remove_location(self, x, y):
        """
        Remove a member from the locations.
        """
        del self.locations[(x, y)]

    def get_moore_hood(self, agent):
        """
        To be written!
        """
        pass

    def get_neighbors(self, agent, width, height):
        lst = []
        agent_dict = {"neighbors": lst}
        dx = [0, 0, 1, -1]
        dy = [-1, 1, 0, 0]
        agent_x = agent.get_x()
        agent_y = agent.get_y()

        for i in range(len(dx)):
            neighbor_x = agent_x + dx[i]
            neighbor_y = agent_y + dy[i]
            if not out_of_bounds(neighbor_x, neighbor_y, 0, 0, width, height):  # Change so that the gird is not hard coded but depends on the WIDTH and HEIGHT  # noqa E501
                agent_dict["neighbors"].append(self.get_agent_at(neighbor_x, neighbor_y))  # noqa E501
        if DEBUG:
            print("In get_neighbors")
            for i in agent_dict["neighbors"]:
                print("Neighbor to agent located in (", agent_x, ",", agent_y, "): (", i.get_x(), ",", i.get_y(), ")")  # noqa E501
        return agent_dict
        # return grp_from_nm_dict("Vonneuman neighbors", agent_dict["neighbors"])  # noqa E501
        dx = [0, 0, 1, -1]
        dy = [-1, 1, 0, 0]
        agent_x = agent.get_x()
        agent_y = agent.get_y()

        for i in range(len(dx)):
            neighbor_x = agent_x + dx[i]
            neighbor_y = agent_y + dy[i]
            if not out_of_bounds(neighbor_x, neighbor_y, 0, 0, 5, 5): # Change so that the gird is not hard coded but depends on the WIDTH and HEIGHT  # noqa E501
                agent_dict["neighbors"].append(self.get_agent_at(neighbor_x, neighbor_y))  # noqa E501
        if DEBUG:
            print("In get_neighbors")
            for i in agent_dict["neighbors"]:
                print("Neighbor to agent located in (", agent_x, ",", agent_y, "): (", i.get_x(), ",", i.get_y(), ")")  # noqa E501
        return agent_dict
        # return grp_from_nm_dict("Vonneuman neighbors", agent_dict["neighbors"])  # noqa E501

    def get_vonneumann_hood(self, agent, width, height):
        """
        Takes in an agent and returns a the group of its vonneuman neighbors
        """
        if DEBUG:
            print("In get_vonneumann_hood")
        return self.get_neighbors(agent, width, height)
