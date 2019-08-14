"""
This file defines Space, which is a collection
of agents related spatially.
"""
from functools import wraps
from random import randint
import random
from math import sqrt
from indra.agent import is_composite, AgentEncoder
from indra.composite import Composite
import json
import math

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
    return min(max(point, lower), upper)


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


def gaussian_distribution(default_target, sigma):
    new_target = random.gauss(default_target, sigma)
    if new_target < 0:
        new_target *= -1
    return new_target


class Space(Composite):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width=DEF_WIDTH, height=DEF_HEIGHT,
                 attrs=None, members=None, action=None,
                 random_placing=True, serial_obj=None):
        super().__init__(name, attrs=attrs, members=members,
                         action=action, serial_obj=serial_obj)

        self.type = "space"

        if serial_obj is not None:
            self.restore_space(serial_obj)
        else:
            self.width = width
            self.height = height
            # the location of members in the space {(tuple):Agent}
            self.locations = {}

            # by making two class methods for rand_place_members and
            # place_member, we allow two places to override
            if random_placing:
                self.rand_place_members(self.members)
            else:
                self.consec_place_members(self.members)

    def restore_space(self, serial_obj):
        self.from_json(serial_obj)

    def to_json(self):
        rep = super().to_json()
        rep["type"] = self.type
        rep["width"] = self.width
        rep["height"] = self.height
        rep["locations"] = {}
        for loc in self.locations:
            rep["locations"][self.locations[loc].name] = loc

        return rep

    def from_json(self, serial_space):
        super().from_json(serial_space)
        self.width = serial_space["width"]
        self.height = serial_space["height"]
        # construct self.location
        self.locations = {}
        for nm in self.registry:
            if self.registry[nm].type == "agent":
                self.locations[self.registry[nm].pos] = self.registry[nm]

        # set up self.neighbors
        for nm in self.registry:
            s = self.registry[nm].neighbors
            if not s and s in self.registry:
                self.registry[nm].neighbors = self.registry[s]

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

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

    def rand_place_members(self, members, max_move=None):
        """
        Locate all members of this space in x, y grid.
        This randomly places members.
        """
        if members is not None:
            for nm, mbr in members.items():
                if not is_composite(mbr):  # by default don't locate groups
                    self.place_member(mbr, max_move)
                else:  # place composite's members
                    self.rand_place_members(mbr.members, max_move)

    def consec_place_members(self, members, curr_col=0, curr_row=0):
        """
        Locate all members of this space in x, y grid.
        Place members consecutively, starting from (0, 0) and
        moving to (1, 0), (2, 0), etc
        """
        if members is not None:
            for nm, mbr in members.items():
                if not is_composite(mbr):
                    if (curr_col < self.width):
                        self.place_member(mbr, xy=(curr_col, curr_row))
                        if DEBUG:
                            print("Placing member at (" + str(curr_col) + ","
                                  + str(curr_row) + ")")
                        curr_col += 1
                    if (curr_col == self.width):
                        if DEBUG:
                            print("Moving up a row from", curr_row,
                                  "to", curr_row + 1)
                        curr_col = 0
                        curr_row += 1
                else:  # place composite's members
                    self.consec_place_members(mbr.members, curr_col, curr_row)

    def rand_x(self, low=0, high=None):
        """
        Return a random x-value between 0 and this space's width,
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.width if high is None else high
        return randint(low, high)

    def rand_y(self, low=0, high=None):
        """
        Return a random y-value between 0 and this space's height
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.height if high is None else high
        return randint(low, high)

    def constrain_x(self, x):
        """
        Pull x in bounds if it ain't.
        """
        return bound(x, 0, self.width - 1)

    def constrain_y(self, y):
        """
        Pull y in bounds if it ain't.
        """
        return bound(y, 0, self.height - 1)

    def get_square_view(self, x, y, distance):
        low_x = x - distance
        high_x = x + distance
        low_y = y - distance
        high_y = y + distance
        return (self.constrain_x(low_x), self.constrain_x(high_x),
                self.constrain_y(low_y), self.constrain_y(high_y))

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
            print("     is_full")
            self.user.log("Can't fit no more folks in this space!")
            return None
        if not is_composite(mbr):
            if xy is not None:
                (x, y) = xy
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
                # if the random position is already taken,x
                # find the member a new position
                # but if max_move is not None, the hood might be filled!
                # so we need something to detect
                # a full neighborhood as well.
                # and if xy is not None, the user asked for a particular
                # spot: don't give them another, but return None.
                return self.place_member(mbr, max_move)
        else:
            return self.rand_place_members(mbr.members, max_move)

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

    def use_saved_hood(hood_func):
        @wraps(hood_func)
        def wrapper(*args, **kwargs):
            agent = args[1]
            if (agent.get("save_neighbors", False) and agent.neighbors is not
                    None):
                return agent.neighbors
            return hood_func(*args, **kwargs)
        return wrapper

    def get_row_hood(self, row_num, pred=None, save_neighbors=False):
        """
        Collects all agents in row `row_num` into a Composite
        and returns it.
        """
        if row_num < 0 or row_num >= self.height:
            return None
        else:
            row_hood = Composite("Row neighbors")
            agent = self.get_agent_at(self.width // 2, row_num)
            row_hood = self.get_x_hood(agent, self.width - 1,
                                       include_self=True)
            return row_hood

    @use_saved_hood
    def get_x_hood(self, agent, width=1, pred=None, include_self=False,
                   save_neighbors=False):
        """
        Takes in an agent  and returns a Composite
        of its x neighbors.
        For example, if the agent is located at (0, 0),
        get_x_hood would return (-1, 0) and (1, 0).
        """
        if agent is not None:
            x_hood = Composite("x neighbors")
            agent_x = agent.get_x()
            agent_y = agent.get_y()
            neighbor_x_coords = []
            for i in range(-width, 0):
                neighbor_x_coords.append(i)
            if (include_self):
                neighbor_x_coords.append(0)
            for i in range(1, width + 1):
                neighbor_x_coords.append(i)
            for i in neighbor_x_coords:
                neighbor_x = agent_x + i
                if not out_of_bounds(neighbor_x, agent_y, 0, 0,
                                     self.width, self.height):
                    x_hood += self.get_agent_at(neighbor_x, agent_y)
            if save_neighbors:
                agent.neighbors = x_hood
            return x_hood

    @use_saved_hood
    def get_y_hood(self, agent, height=1, pred=None, include_self=False,
                   save_neighbors=False):
        """
        Takes in an agent and returns a Composite
        of its y neighbors.
        For example, if the agent is located at (0, 0),
        get_y_hood would return (0, -1) and (0, 1).
        """
        y_hood = Composite("y neighbors")
        agent_x = agent.get_x()
        agent_y = agent.get_y()
        neighbor_y_coords = []
        for i in range(-height, 0):
            neighbor_y_coords.append(i)
        if (include_self):
            neighbor_y_coords.append(0)
        for i in range(1, height + 1):
            neighbor_y_coords.append(i)
        for i in neighbor_y_coords:
            neighbor_y = agent_y + i
            if not out_of_bounds(agent_x, neighbor_y, 0, 0,
                                 self.width, self.height):
                y_hood += (self.get_agent_at(agent_x, neighbor_y))
        if save_neighbors:
            agent.neighbors = y_hood
        return y_hood

    @use_saved_hood
    def get_vonneumann_hood(self, agent, pred=None, save_neighbors=False):
        """
        Takes in an agent and returns a Composite of its
        Von Neumann neighbors.
        """
        vonneumann_hood = self.get_x_hood(agent) + self.get_y_hood(agent)
        if agent.get("save_neighbors", False):
            agent.neighbors = vonneumann_hood
        return vonneumann_hood

    @use_saved_hood
    def get_moore_hood(self, agent, pred=None, save_neighbors=False,
                       include_self=False, hood_size=1):
        """
        Takes in an agent and returns a Composite of its Moore neighbors.
        """
        moore_hood = Composite("Moore neighbors")
        x1, x2, y1, y2 = self.get_square_view(agent.get_x(),
                                              agent.get_y(),
                                              hood_size)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                neighbor = self.get_agent_at(x, y)
                if neighbor is not None and (agent.get_x() != x
                                             or agent.get_y() != y):
                    moore_hood += neighbor
        if include_self:
            moore_hood += self.get_agent_at(agent.get_x(), agent.get_y())

        if DEBUG:
            print(agent)
            for agents in moore_hood:
                print("  ", moore_hood[agents])

        if agent.get("save_neighbors", False):
            agent.neighbors = moore_hood
        return moore_hood

    def get_closest_agent(self, agent):
        """
        Get the agent' closest to agent on grid.
        """
        closest = None
        min_distance_seen = MAX_WIDTH * MAX_HEIGHT
        for key, other in self.locations.items():
            if other is agent:
                continue
            d = distance(agent, other)
            if d < min_distance_seen:
                min_distance_seen = d
                closest = other
        return closest

    def get_max_distance(self):
        return sqrt((self.height ** 2) + (self.width ** 2))

    def point_from_vector(self, angle, max_move, xy, vector_start=(0, 0)):
        """
        Given a vector with one end at the origin, find
        the other end -- if off grid, pull it back onto the
        grid.
        """
        (prev_x, prev_y) = xy
        (cur_x, cur_y) = xy
        #  Calculate the coordinates
        if math.cos(angle) < 0:
            cur_x = prev_x * (-1)
        if math.sin(angle) < 0:
            cur_y = prev_y * (-1)
        cur_x = math.cos(angle) * max_move + cur_x
        cur_y = math.sin(angle) * max_move + cur_y

        #  Adjust if the cur_x and cur_y are out of range
        if out_of_bounds(cur_x, cur_y, 0, 0, self.width, self.height):
            if (cur_x == prev_x):
                if (cur_y < 0):
                    return (cur_x, 0)
                else:
                    return (cur_x, self.height - 1)

            if (cur_y == prev_y):
                if (cur_x < 0):
                    return (0, cur_y)
                else:
                    return (self.width - 1, cur_y)

            if (cur_x != prev_x and cur_y != prev_y):
                slope = float((cur_y - prev_y) / (cur_x - prev_x))

                # Calculate the intersection of the vector and Ox and Oy axes
                y_intercept = float(cur_y - slope * cur_x)
                x_intercept = float(y_intercept / slope) * (-1)

                # Calculate the intersection of the vector and grid axes
                x_vertical = self.width - 1
                y_vertical = float(slope * x_vertical) + y_intercept
                y_horizontal = self.height - 1
                x_horizontal = float((y_horizontal - y_intercept) / slope)

            #  Adjust the out of bound coordinates
            #  1. If both coordinates < 0
            #  2. If both coordinates > grid size
            #  3. If only one coordinate < 0
            #  4. If only one coordinate > grid size

            if (cur_y < 0 and cur_x < 0):
                if x_intercept > 0:
                    return (x_intercept, 0)
                else:
                    return (0, y_intercept)

            elif (cur_y >= self.height and cur_x >= self.width):
                if x_horizontal < self.width:
                    cur_x = x_horizontal
                    cur_y = y_horizontal
                else:
                    cur_x = x_vertical
                    cur_y = y_vertical
                return (cur_x, cur_y)

            elif (cur_y * cur_x < 0):
                if cur_x < 0:
                    cur_x = 0
                    cur_y = y_intercept
                else:
                    cur_y = 0
                    cur_x = x_intercept
                return (cur_x, cur_y)

            elif (cur_x >= self.width or cur_y >= self.height):
                if cur_x >= self.width:
                    cur_x = x_vertical
                    cur_y = y_vertical
                else:
                    cur_x = x_horizontal
                    cur_y = y_horizontal
                return (cur_x, cur_y)
        else:
            return (cur_x, cur_y)
