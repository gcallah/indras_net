"""
This file defines an Agent.
"""
import sys
import numpy as np
import json
# from random import uniform
from collections import OrderedDict

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

LOW_RAND = .666
HI_RAND = 1.5

INF = sys.maxsize  # really any very big number would do here!


def type_hash(agent):
    """
    type_hash() will return an ID that identifies
    the ABM type of an entity.
    """
    return len(agent)  # temp solution!


def is_space(thing):
    return hasattr(thing, "height")


class AgentEncoder(json.JSONEncoder):
    """
    The JSON encoder base class for all descendants
    of Agent.
    """
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
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
                 groups=None):
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
        if groups is not None:
            self.groups = groups
        else:
            self.groups = {}
        self.pos = None
        self.locator = None
        if groups is not None:
            for grp in iter(groups.values()):
                if is_space(grp):
                    self.locator = grp

    def set_pos(self, x, y):
        self.pos = (x, y)

    def __eq__(self, other):
        if (type(self) != type(other) or self.type_sig != other.type_sig):
            return False
        else:
            return np.array_equal(self.val_vect, other.val_vect)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(self.to_json())

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.val_vect[self.attrs[key]]

    def __setitem__(self, key, value):
        if key not in self.attrs:
            raise KeyError(key)
        self.val_vect[self.attrs[key]] = value

    def __contains__(self, item):
        return item in self.attrs

    def __iter__(self):
        return iter(self.attrs)

    def __reversed__(self):
        return reversed(self.attrs)

    def __call__(self):
        """
        Agents will 'act' by being called as a function.
        If the agent has no `act()` function, do nothing.
        Agents should return True if they did, in fact,
        'do something,' or False if they did not.
        """
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                self.action(self)
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
                members={self.name: self, other.name: other})
        else:
            return None

# numpy doesn't implement this! must investigage.
#    def __idiv__(self, scalar):
#        self.val_vect /= scalar
#        return self

    def isactive(self):
        return self.active

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

    def join_group(self, group):
        if group.name not in self.groups:
            if DEBUG2:
                print("Join group being called on " + self.name
                      + " to join group: " + group.name)
            self.groups[group.name] = group
            if is_space(group):
                self.locator = group

    def to_json(self):
        grp_nms = ""
        for grp in self.groups:
            grp_nms += grp + " "
        return {"name": self.name,
                "duration": self.duration,
                "attrs": self.attrs_to_dict(),
                "groups": grp_nms
                }
