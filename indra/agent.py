"""
This file defines an Agent.
"""
import sys
import numpy as np
from math import pi, sin
import json
# from random import uniform
from collections import OrderedDict

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# x and y indices
X = 0
Y = 1
NEUTRAL = .7071068

# Set up constants for some common vectors: this will save time and memory.
X_VEC = np.array([1, 0])
Y_VEC = np.array([0, 1])
NULL_VEC = np.array([0, 0])
NEUT_VEC = np.array([NEUTRAL, NEUTRAL])

INF = sys.maxsize  # really any very big number would do here!

DEF_MAX_MOVE = 2


def ratio_to_sin(ratio):
    return sin(ratio * pi / 2)


def type_hash(agent):
    """
    type_hash() will return an ID that identifies
    the ABM type of an entity.
    """
    return len(agent)  # temp solution!


def is_composite(thing):
    """
    Is this thing a composite?
    """
    return hasattr(thing, 'members')


def is_space(thing):
    """
    How do we determine if a group we are a member of is a space?
    """
    return hasattr(thing, "height")


def join(agent1, agent2):
    """
        Create connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        print("Attempt to place " + str(agent2)
              + " in non-group " + str(agent1))
    else:
        agent1.add_member(agent2)
        agent2.add_group(agent1)


def split(agent1, agent2):
    """
        Break connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        print("Attempt to remove " + str(agent2)
              + " from non-group " + str(agent1))
    else:
        agent1.del_member(agent2)
        agent2.del_group(agent1)


def switch(agent, grp1, grp2):
    """
        Move agent from grp1 to grp2.
    """
    split(grp1, agent)
    join(grp2, agent)


class AgentEncoder(json.JSONEncoder):
    """
    The JSON encoder base class for all descendants
    of Agent.
    """
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        elif isinstance(o, np.int64):
            return int(o)
        else:
            return json.JSONEncoder.default(self, o)


class Agent(object):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """
    def __init__(self, name, attrs=None, action=None, duration=INF,
                 prim_group=None):
        self.name = name
        self.action = action
        self.duration = duration
        self.attrs = OrderedDict()
        if attrs is not None:
            for i, (k, v) in enumerate(attrs.items()):
                self.attrs[k] = i  # store index into np.array!
                self.val_vect = np.array(list(attrs.values()))
        else:
            self.val_vect = np.array([])
        self.type_sig = type_hash(self)
        self.active = True
        self.groups = {}
        self.pos = None
        self.locator = None
        self.prim_group = prim_group
        if self.prim_group is not None:
            self.groups[str(self.prim_group)] = self.prim_group
            if is_space(self.prim_group):
                self.locator = self.prim_group

    def primary_group(self):
        return self.prim_group

    def islocated(self):
        return self.pos is not None

    def set_pos(self, locator, x, y):
        self.locator = locator  # whoever sets my pos is my locator!
        self.pos = (x, y)

    def get_pos(self):
        return self.pos

    def get_x(self):
        return self.pos[X]

    def get_y(self):
        return self.pos[Y]

    def __eq__(self, other):
        if (type(self) != type(other) or self.type_sig != other.type_sig):
            return False
        else:
            return np.array_equal(self.val_vect, other.val_vect)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.val_vect[self.attrs[key]]

    def __setitem__(self, key, value):
        if key not in self.attrs:
            raise KeyError(key)
        index = self.attrs[key]
        self.val_vect[index] = value

    def __contains__(self, item):
        return item in self.attrs

    def __iter__(self):
        return iter(self.attrs)

    def __reversed__(self):
        return reversed(self.attrs)

    def __call__(self):
        """
        Agents will 'act' by being called as a function.
        If the agent has no `action()` function, do nothing.
        If returns False, by default agent will move.
        """
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                if not self.action(self):
                    # False return means agent is "unhappy" and
                    # so agent will move (if located).
                    self.move()
                return True
            elif DEBUG:
                print("I'm " + self.name + " and I ain't got no action to do!")
        else:
            self.active = False
        return False

    def __iadd__(self, scalar):
        self.val_vect += scalar
        return self

    def __isub__(self, scalar):
        self.val_vect -= scalar
        return self

    def __imul__(self, scalar):
        self.val_vect *= scalar
        return self

    def __add__(self, other):
        import composite
        if isinstance(other, Agent):
            return composite.Composite(
                self.name + other.name,
                members=[self, other])
        else:
            return None

# numpy doesn't implement this! must investigage.
#    def __idiv__(self, scalar):
#        self.val_vect /= scalar
#        return self

    def move(self, max_move=DEF_MAX_MOVE):
        """
        Move this agent to a random pos within max_move
        of its current pos.
        """
        if (self.islocated() and self.locator is not None
                and not self.locator.is_full()):
            self.locator.place_member(self, max_move)

    def isactive(self):
        return self.active

    def die(self):
        self.duration = 0
        self.active = False

    def magnitude(self):
        return np.linalg.norm(self.val_vect)

    def sum(self):
        return self.val_vect.sum()

    def attrs_to_dict(self):
        d = OrderedDict()
        for key in self.attrs:
            d[key] = self[key]
        return d

    def same_type(self, other):
        return self.type_sig == other.type_sig

    def del_group(self, group):
        if str(group) in self.groups:
            del self.groups[str(group)]

        if group == self.prim_group:
            self.prim_group = None

    def add_group(self, group):
        if str(group) not in self.groups:
            if DEBUG2:
                print("Join group being called on " + self.name
                      + " to join group: " + group.name)
            self.groups[group.name] = group
            if is_space(group):
                self.locator = group

            if self.prim_group is None:
                self.prim_group = group

    def switch_groups(self, g1, g2):
        self.leave_group(g1)
        self.add_group(g2)

    def to_json(self):
        grp_nms = ""
        for grp in self.groups:
            grp_nms += grp + " "
        return {"name": self.name,
                "duration": self.duration,
                "pos": self.pos,
                "attrs": self.attrs_to_dict(),
                "groups": grp_nms,
                "locator": self.locator,
                "prim_group": self.prim_group,
                "active": self.active,
                "type_sig": self.type_sig,
                "action": self.action
                }
