"""
This file defines Space, which is a collection
of agents related spatially.
"""
import json
import math
import sys
from functools import wraps
from math import sqrt
from random import randint

from indra.agent import is_composite, AgentEncoder, X, Y
from indra.composite import Composite
from registry.registry import register, get_registration, get_group
from indra.user import user_debug, user_log, user_log_warn

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
    return (x < x1 or x >= x2
            or y < y1 or y >= y2)


def bound(point, lower, upper):
    return min(max(point, lower), upper)


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
    """
    Check whether the distance between two objects is smaller than
    the given distance
    """
    d = distance(agent, other)
    if DEBUG2:
        print("Distance between " + str(agent)
              + " and " + str(other) + " is "
              + str(d))
    return d < hood_sz


def use_saved_hood(hood_func):
    @wraps(hood_func)
    def wrapper(*args, **kwargs):
        agent = args[1]
        if (agent.get("save_neighbors", False) and agent.neighbors is not
                None):
            return agent.neighbors
        return hood_func(*args, **kwargs)

    return wrapper


def fill_neighbor_coords(agent, height, include_self):
    agent_x = agent.get_x()
    agent_y = agent.get_y()
    neighbor_y_coords = []
    for i in range(-height, 0):
        neighbor_y_coords.append(i)
    if include_self:
        neighbor_y_coords.append(0)
    for i in range(1, height + 1):
        neighbor_y_coords.append(i)
    return agent_x, agent_y, neighbor_y_coords


class Space(Composite):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width=DEF_WIDTH, height=DEF_HEIGHT,
                 attrs=None, members=None, action=None,
                 random_placing=True, serial_obj=None, reg=True):
        super().__init__(name, attrs=attrs, members=members,
                         action=action, serial_obj=serial_obj,
                         reg=False)

        self.type = type(self).__name__

        if serial_obj is not None:
            self.restore(serial_obj)
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
        if reg:
            register(self.name, self)

    def restore(self, serial_obj):
        self.from_json(serial_obj)

    def to_json(self):
        rep = super().to_json()
        rep["type"] = self.type
        rep["width"] = self.width
        rep["height"] = self.height
        rep["locations"] = self.locations

        return rep

    def from_json(self, serial_space):
        super().from_json(serial_space)
        self.width = serial_space["width"]
        self.height = serial_space["height"]
        self.locations = serial_space["locations"]

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
                    if curr_col < self.width:
                        self.place_member(mbr, xy=(curr_col, curr_row))
                        if DEBUG:
                            print("Placing member at (" + str(curr_col) + ","
                                  + str(curr_row) + ")")
                        curr_col += 1
                    if curr_col == self.width:
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

    def get_row_view(self, x, y, distance):
        pass

    def get_col_view(self, x, y, distance):
        pass

    def get_moore_hood_idx(self, x, y, distance=1):
        """
        J & K: THIS WILL GO AWAY!
        Return set of coords (x1, x2, y1, y2) that are the
        corners of a square... *unless* those corners could
        be off the grid. In that case, pull them back in bounds.
        """
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
        if max_move is not None and mbr.is_located():
            low_x = self.constrain_x(mbr.get_x() - max_move)
            high_x = self.constrain_x(mbr.get_x() + max_move)
            low_y = self.constrain_y(mbr.get_y() - max_move)
            high_y = self.constrain_y(mbr.get_y() + max_move)
        x = self.rand_x(low_x, high_x)
        y = self.rand_y(low_y, high_y)
        return x, y

    def is_empty(self, x, y):
        """
        See if cell x,y is empty.
        Always make location a str for serialization.
        """
        return str((x, y)) not in self.locations

    def get_agent_at(self, x, y):
        """
        Return agent at cell x,y
        If cell is empty return None.
        Always make location a str for serialization.
        """
        if self.is_empty(x, y):
            return None
        agent_nm = self.locations[str((x, y))]
        return get_registration(agent_nm)

    def place_member(self, mbr, max_move=None, xy=None):
        """
        By default, locate a member at a random x, y spot in our grid.
        `max_move` constrains where that can be.
        Setting `xy` picks a particular spot to place member.
        `xy` must be a tuple!
        """
        if self.is_full():
            user_log("Can't fit no more folks in this space!")
            return None
        if not is_composite(mbr):
            if xy is not None:
                (x, y) = xy
            else:
                (x, y) = self.gen_new_pos(mbr, max_move)
            if self.is_empty(x, y):
                if mbr.is_located():
                    self.move_location(x, y, mbr.get_x(),
                                       mbr.get_y(), mbr.name)
                else:
                    self.add_location(x, y, mbr)
                # if I am setting pos, I am agent's locator!
                mbr.set_pos(self, x, y)
                return x, y
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
        locations{} stores agents by name, to look up in registry.
        """
        self.locations[str((x, y))] = member.name

    def move_location(self, nx, ny, ox, oy, agent_name="NA"):
        """
        Move a member to a new position, if that position
        is not already occupied.
        """
        old_loc = str((ox, oy))
        new_loc = str((nx, ny))
        if old_loc not in self.locations:
            user_log_warn("Trying to move unlocated agent "
                          + agent_name + " at " + old_loc)
        elif new_loc not in self.locations:
            self.locations[new_loc] = self.locations[old_loc]
            del self.locations[old_loc]
        else:
            user_debug("Trying to place agent in occupied space.")

    def remove_location(self, x, y):
        """
        Remove a member from the locations.
        """
        del self.locations[str((x, y))]

    def get_row_hood(self, row_num, pred=None, save_neighbors=False):
        """
        Collects all agents in row `row_num` into a Composite
        and returns it.
        """
        if row_num < 0 or row_num >= self.height:
            return None
        else:
            agent = self.get_agent_at(self.width // 2, row_num)
            row_hood = self.get_x_hood(agent, self.width - 1,
                                       include_self=True)
            row_hood.name = "Row neighbors"
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
            agent_x, agent_y, neighbor_x_coords \
                = fill_neighbor_coords(agent,
                                       width,
                                       include_self)
            for i in neighbor_x_coords:
                neighbor_x = agent_x + i
                if not out_of_bounds(neighbor_x, agent_y, 0, 0,
                                     self.width, self.height):
                    x_hood += self.get_agent_at(neighbor_x, agent_y)
            if save_neighbors:
                agent.neighbors = x_hood
            return x_hood

    # for now, let's slow down and not use the saved hood!
    @use_saved_hood
    def get_y_hood(self, agent, height=1, pred=None, include_self=False,
                   save_neighbors=False):
        """
        Takes in an agent and returns a Composite
        of its y neighbors.
        For example, if the agent is located at (0, 0),
        get_y_hood would return agents at (0, 2) and (0, 1).
        """
        y_hood = Composite("y neighbors")
        agent_x, agent_y, neighbor_y_coords \
            = fill_neighbor_coords(agent,
                                   height,
                                   include_self)
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
        region = Region(space=self, center=(agent.get_x(), agent.get_y()),
                        size=hood_size)
        members = region.get_agents(exclude_self=True, pred=None)
        return Composite("Moore neighbors", members=members)

    def get_square_hood(self, agent, pred=None, save_neighbors=False,
                        include_self=False, hood_size=1):
        """
        Get a list of the nearby agents in a square neighborhood.
        The size of the hood is given by hood_size.
        We can filter with pred.
        We may or may not save this hood.
        """
        return self.get_moore_hood(agent,
                                   pred=pred,
                                   save_neighbors=save_neighbors,
                                   include_self=include_self,
                                   hood_size=hood_size)

    def get_neighbor_of_groupX(self, agent, group, save_neighbors=False,
                               hood_size=1):
        """
        If the agent has any neighbors in group X, return the first one
        encountered.
        We may get the groupX object itself, or we may get passed
        its name.
        """
        hood = self.get_square_hood(agent, save_neighbors=save_neighbors,
                                    hood_size=hood_size)
        if isinstance(group, str):
            # lookup group by name
            group = get_group(group)
            if group is None:
                return None
        for agent_name in hood:
            if group.ismember(agent_name):
                return group[agent_name]
        return None

    def get_closest_agent(self, agent):
        """
        Get the agent' closest to agent on grid.
        """
        closest = None
        min_distance_seen = MAX_WIDTH * MAX_HEIGHT
        for key, other_nm in self.locations.items():
            other = get_registration(other_nm)
            if other is agent or other is None:
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
        (new_x, new_y) = xy
        #  Calculate the new coordinates
        new_x += int(math.cos(math.radians(angle)) * max_move)
        new_y += int(math.sin(math.radians(angle)) * max_move)
        return self.constrain_x(new_x), self.constrain_y(new_y)


class Region():
    """
    This is the base of all regions used for neighborhoods, obstacles,
    and other sub-divisions of space.

    Region(space, NW=(2, 3), NE=(4, 5), SW=(7, 8), SE=(8, 9))
    or
    Region(space, xy=(2, 3), size=7)
    """

    def __init__(self, space=None, NW=None, NE=None, SW=None,
                 SE=None, center=None, size=None):
        if (center is not None and size is not None):
            if (NW is not None or NE is not None or SW is not None
                    or SE is not None):
                raise Exception("Extra coordinate entered")
            if (space is None):
                raise Exception("Space not added as parameter")
            self.NW = (center[X] - size, center[Y] + size)
            self.NE = (center[X] + size + 1, center[Y] + size)
            self.SW = (center[X] - size, center[Y] - size - 1)
            self.SE = (center[X] + size + 1, center[Y] - size - 1)
            self.width = size * 2 + 1
            self.height = size * 2 + 1
            self.center = center
            self.space = space
        else:
            if (center is not None or size is not None):
                raise Exception("center or size added when not necessary")
            if (space is None):
                raise Exception("Space not added as parameter")
            self.NW = NW
            self.NE = NE
            self.SW = SW
            self.SE = SE
            self.width = abs(self.NW[X] - self.NE[X])
            self.height = abs(self.NW[Y] - self.SW[Y])
            self.center = None
            self.space = space
        self.check_bounds()

    def contains(self, coord):
        if (coord[X] >= self.NW[X]) and (coord[X] < self.NE[X]):
            if(coord[Y] >= self.SW[Y]) and (coord[Y] < self.NE[Y]):
                return True
        return False

    def check_bounds(self):
        self.NW = (self.space.constrain_x(self.NW[X]),
                   self.space.constrain_y(self.NW[Y]))
        self.NE = (self.space.constrain_x(self.NE[X]) + 1,
                   self.space.constrain_y(self.NE[Y]))
        self.SW = (self.space.constrain_x(self.SW[X]),
                   self.space.constrain_y(self.SW[Y]) - 1)
        self.SE = (self.space.constrain_x(self.SE[X]) + 1,
                   self.space.constrain_y(self.SE[Y]) - 1)

    def get_agents(self, exclude_self=False, pred=None):
        agent_ls = []
        if DEBUG2:
            print("width: " + str(self.width))
            print("height: " + str(self.height))
            print("============")
            print("NW: " + str(self.NW))
            print("NE: " + str(self.NE))
            print("SW: " + str(self.SW))
            print("SE: " + str(self.SE))
            print("===========")
        for y in range(self.height):
            y_coord = self.SW[Y] + y + 1
            for x in range(self.width):
                x_coord = self.SW[X] + x
                if DEBUG2:
                    print("(x,y): " + str((x_coord, y_coord)))
                potential_neighbor = self.space.get_agent_at(x_coord, y_coord)
                if potential_neighbor is not None:
                    if pred is None or pred(potential_neighbor):
                        if (x_coord, y_coord) is self.center:
                            if exclude_self is False:
                                agent_ls.append(potential_neighbor)
                        else:
                            agent_ls.append(potential_neighbor)
        return agent_ls

    def exists_neighbor(self, exclude_self=False, pred=None):
        if DEBUG2:
            print("width: " + str(self.width))
            print("height: " + str(self.height))
            print("============")
            print("NW: " + str(self.NW))
            print("NE: " + str(self.NE))
            print("SW: " + str(self.SW))
            print("SE: " + str(self.SE))
            print("===========")
        for y in range(self.height):
            y_coord = self.SW[Y] + y + 1
            for x in range(self.width):
                x_coord = self.SW[X] + x
                if DEBUG2:
                    print("(x,y): " + str((x_coord, y_coord)))
                potential_neighbor = self.space.get_agent_at(x_coord, y_coord)
                if potential_neighbor is not None:
                    if pred is None or pred(potential_neighbor):
                        if (x_coord, y_coord) is self.center:
                            if exclude_self is False:
                                return True
                        else:
                            return True
        return False

    def get_ratio(self, pred_one=None, pred_two=None):
        if pred_one is None and pred_two is None:
            raise Exception("Enter at least single group")
        elif pred_one is not None and pred_two is not None:
            group_one_num = len(self.get_agents(exclude_self=True,
                                pred=pred_one))
            group_two_num = len(self.get_agents(exclude_self=True,
                                pred=pred_two))
            return group_one_num / group_two_num
        elif pred_one is None or pred_two is None:
            agent_num = len(self.get_agents(exclude_self=True, pred=None))
            if DEBUG2:
                print("agent_num length: " + str(agent_num))
            if agent_num == 0:
                raise 1
            if pred_two is None:
                group_num = len(self.get_agents(exclude_self=True,
                                pred=pred_one))
            elif pred_one is None:
                group_num = len(self.get_agents(exclude_self=True,
                                pred=pred_two))
            return group_num / agent_num

    def calc_heat(self, group, coord):
        heat_strength = 0
        for heat in group:
            distance = sqrt(
                ((coord[X] - group[heat].get_x()) ** 2)
                + ((coord[Y] - group[heat].get_y()) ** 2)
            )
            if distance != 0:
                heat_strength += 1 / ((distance) ** 2)
            else:
                heat_strength += sys.maxsize
        heat_strength *= -1
        return heat_strength

    def heatmap(self, group):
        heat_map_ls = []
        for y in range(self.height):
            for x in range(self.width):
                heat_map_ls.append(self.calc_heat(group, (x, y)))
        return heat_map_ls


class CircularRegion(Region):
    def __init__(self, space, center, radius):
        self.space = space
        self.center = center
        self.radius = radius

    def check_out_bounds(self, coord):
        return out_of_bounds(coord[X], coord[Y], 0, 0,
                             self.space.width,
                             self.space.height)

    def contains(self, coord):
        if ((coord[X] - self.center[X]) ** 2
                + (coord[Y] - self.center[Y]) ** 2 < self.radius ** 2
                and not self.check_out_bounds(coord)):
            return True
        return False

    def get_agents(self, exclude_self=False, pred=None):
        agent_ls = []
        for coord in self.space.locations:
            # Need to convert coord string into an x and a y value:
            conv_coord = [0, 0]
            curr_num = ""
            for curr_char in coord:
                if curr_char.isdigit():
                    curr_num += curr_char
                elif curr_char == ",":
                    conv_coord[X] = int(curr_num)
                    curr_num = ""
                elif curr_char == ")":
                    conv_coord[Y] = int(curr_num)
            if self.contains(conv_coord):
                potential_agent = self.space.get_agent_at(conv_coord[X],
                                                          conv_coord[Y])
                if pred is None or pred is True:
                    if (conv_coord == self.center) and (exclude_self is False):
                        agent_ls.append(potential_agent)
                    else:
                        agent_ls.append(potential_agent)
        return agent_ls


class CompositeRegion(Region):

    def __init__(self, region_set=None):
        if region_set is None:
            self.composite = {}
        else:
            self.composite = region_set

    def contains(self, coord):
        for region in self.composite:
            if (region.contains(coord)):
                return True
        return False

    def get_agents(self, exclude_self=False, pred=None):
        agent_ls = []
        for region in self.composite:
            sub_agent_ls = region.get_agents(exclude_self=False, pred=pred)
            agent_ls.extend(sub_agent_ls)
        return agent_ls

    def exists_neighbor(self, exclude_self=False, pred=None):
        for region in self.composite:
            if region.exists_neighbor(exclude_self=False, pred=pred):
                return True
        return False

    def add_region(self, region):
        self.composite.add(region)

    def remove_region(self, region):
        self.composite.remove(region)
