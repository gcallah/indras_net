"""
This file defines an Agent.
"""
import json
import logging
import sys
from collections import OrderedDict
from math import pi, sin
from random import random

import numpy as np

from indra.registry import register, get_registration

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

DEF_MAX_MOVE = None


def prob_state_trans(curr_state, states):
    """
    Do a probabilistic state transition.
    """
    new_state = curr_state
    r = random()
    cum_prob = 0.0
    for trans_state in range(len(states[curr_state])):
        cum_prob += states[curr_state][trans_state]
        if cum_prob >= r:
            new_state = trans_state
            break
    return new_state


def possible_trans(states, start_state, end_state):
    return states[start_state][end_state]


def ratio_to_sin(ratio):
    """
    Take a ratio of y to x and turn it into a sine.
    """
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
        logging.error("[Error] Attempt to place " + str(agent2)
                      + " in non-group " + str(agent1))
    else:
        agent1.add_member(agent2)
        agent2.add_group(agent1)


def split(agent1, agent2):
    """
    Break connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        logging.error("[Error] Attempt to remove " + str(agent2)
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
    We should begin passing env to all agents: we think it will
    simplify code. It should replace `locator`.
    """

    def __init__(self, name, attrs=None, action=None, duration=INF,
                 prim_group=None, serial_obj=None, env=None, reg=True):
        if serial_obj is not None:
            self.restore(serial_obj)
        else:
            # self.type gotta go!
            self.type = "agent"
            self.name = name
            # cut locator over to a property
            self.action_key = None
            self.action = action
            if action is not None:
                self.action_key = action.__name__
            self.duration = duration
            self.attrs = OrderedDict()
            self.neighbors = None
            if attrs is not None:
                self.attrs = attrs
            self.active = True
            self.pos = None

            # some thing we will fetch from registry:
            # for these, we only store the name but look up object
            self._env = None if env is None else env.name
            self._locator = None if self._env is None else self._env
            self._prim_group = None if prim_group is None else prim_group.name
            if prim_group is not None and is_space(prim_group):
                self.locator = prim_group

        if reg:
            register(self.name, self)

    @property
    def prim_group(self):
        """
        This is the prim_group property.
        We use the string _prim_group to look up the
        prim_group object in the registry.
        An agent may be in multiple groups: it appears in
        the groups `members` list. But it can have only
        one primary group.
        """
        return get_registration(self._prim_group)

    @prim_group.setter
    def prim_group(self, val):
        """
        Set our prim_group: if passed an agent, store its name.
        Else, it must be a string, and just store that.
        Don't try to register the val! Agents register themselves
        when constructed.
        """
        if isinstance(val, Agent):
            self._prim_group = val.name
        elif isinstance(val, str):
            self._prim_group = val
        else:
            # we must set up logging to handle these better:
            print("Bad type passed to prim_group:", str(val))

    @property
    def env(self):
        """
        This is the env property.
        We use the string _env to look up the
        env object in the registry.
        """
        return get_registration(self._env)

    @env.setter
    def env(self, val):
        """
        Set our env: if passed an agent, store its name.
        Else, it must be a string, and just store that.
        Don't try to register the val! Agents register themselves
        when constructed.
        """
        if isinstance(val, Agent):
            self._env = val.name
        elif isinstance(val, str):
            self._env = val
        elif val is None:
            self._env = None
        else:
            # we must set up logging to handle these better:
            print("Bad type passed to env:", str(val))

    @property
    def locator(self):
        """
        This is the locator property.
        We use the string _locator to look up the
        locator object in the registry.
        """
        return get_registration(self._locator)

    @locator.setter
    def locator(self, val):
        """
        Set our locator: if passed an agent, store its name.
        Else, it must be a string, and just store that.
        Don't try to register the val! Agents register themselves
        when constructed.
        """
        if isinstance(val, Agent):
            self._locator = val.name
        elif isinstance(val, str):
            self._locator = val
        else:
            # we must set up logging to handle these better:
            print("Bad type passed to locator:", str(val))

    def restore(self, serial_obj):
        self.from_json(serial_obj)

    def to_json(self):
        if not self.neighbors:
            nb = None
        else:
            nb = self.neighbors.name
        return {"name": self.name,
                "type": self.type,
                "duration": str(self.duration),
                "pos": self.pos,
                "attrs": self.attrs_to_dict(),
                "active": self.active,
                "prim_group": self.prim_group,
                "locator": self._locator,
                "env": self._env,
                "neighbors": nb,
                "action_key": self.action_key
                }

    def from_json(self, serial_agent):
        from models.run_dict_helper import action_dict
        self.action = None
        if serial_agent["action_key"] is not None:
            self.action = action_dict[serial_agent["action_key"]]
        self.action_key = serial_agent["action_key"]
        self.active = serial_agent["active"]
        self.attrs = OrderedDict(serial_agent["attrs"])
        if not serial_agent["pos"]:
            self.pos = None
        else:
            self.pos = tuple(serial_agent["pos"])
        self.duration = int(serial_agent["duration"])
        self.name = serial_agent["name"]
        self.neighbors = serial_agent["neighbors"]
        self._prim_group = serial_agent["prim_group"]
        self._locator = serial_agent["locator"]
        self._env = serial_agent["env"]
        self.type = serial_agent["type"]

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def primary_group(self):
        return self.prim_group

    def is_located(self):
        return self.pos is not None

    def set_pos(self, locator, x, y):
        self.locator = locator  # whoever sets my pos is my locator!
        # and my env, if I don't have one:
        if self.env is None:
            self.env = self.locator
        self.pos = (x, y)

    def get_pos(self):
        return self.pos

    def get_x(self):
        return self.pos[X]

    def get_y(self):
        return self.pos[Y]

    def __eq__(self, other):
        if type(self) != type(other) or len(self) != len(other):
            return False
        else:
            for key in self:
                if key not in other:
                    return False
                elif other[key] != self[key]:
                    return False
            return True

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.attrs[key]

    def get(self, key, default=None):
        if key in self.attrs:
            return self.__getitem__(key)
        else:
            return default

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __contains__(self, item):
        return item in self.attrs

    def __iter__(self):
        return iter(self.attrs)

    def __call__(self, **kwargs):
        """
        Agents will 'act' by being called as a function.
        If the agent has no `action()` function, do nothing.
        If returns False, by default agent will move.
        """
        self.duration -= 1
        acted = False
        moved = False
        if self.duration > 0:
            if self.action is not None:
                acted = True
                # the action was defined outside this class, so pass self:
                if not self.action(self, **kwargs):
                    # False return means agent is "unhappy" and
                    # so agent will move (if located).
                    max_move = DEF_MAX_MOVE
                    if "max_move" in self:
                        max_move = self["max_move"]
                    angle = None
                    if "angle" in self:
                        angle = self["angle"]
                    self.move(max_move=max_move, angle=angle)
                    moved = True
            elif DEBUG:
                print("I'm " + self.name
                      + " and I ain't got no action to do!")
        else:
            self.active = False
        return (acted, moved)

    def __iadd__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __isub__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __imul__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __add__(self, other):
        """
        Adds agent and group to make new group.
        """
        from indra import composite
        if isinstance(other, Agent):
            return composite.Composite(
                self.name + other.name,
                members=[self, other])
        else:
            return None

    def move(self, max_move=DEF_MAX_MOVE, angle=None):
        """
        Move this agent to a random pos within max_move
        of its current pos.
        """
        if (self.is_located() and self.locator is not None
                and not self.locator.is_full()):
            new_xy = None
            if angle is not None:
                if DEBUG:
                    print("Using angled move")
                new_xy = self.locator.point_from_vector(angle,
                                                        max_move, self.pos)
            self.locator.place_member(self, max_move=max_move, xy=new_xy)

    def is_active(self):
        return self.active

    def die(self):
        self.duration = 0
        self.active = False

    def attrs_to_dict(self):
        """
        Now attrs ARE a dict, so just return 'em.
        """
        return self.attrs

    def del_group(self, group):
        if group == self.prim_group:
            self.prim_group = None

    def add_group(self, group):
        if is_space(group):
            self.locator = group
        if self.prim_group is None:
            self.prim_group = group

    def switch_groups(self, g1, g2):
        self.del_group(g1)
        self.add_group(g2)
