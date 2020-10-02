"""
This file defines an Agent.
"""
import types
import json
import sys
from math import pi, sin
from random import random
from functools import wraps

import numpy as np

from registry.registry import register, get_registration, get_env
from registry.registry import get_group, user_log_notif, user_log_err
from registry.execution_registry import EXEC_KEY, \
    CLI_EXEC_KEY
from indra.utils import get_func_name

DEBUG = False  # turns debugging code on or off
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

MOVE = False
DONT_MOVE = True


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


def set_trans(states, curr_state, poss_state, val,
              compl_state=None):
    """
    Change the probability of transitioning from
    curr_state to poss_state to val.
    If compl_state is passed, set it equal to 1 - val.
    At present it is assumed that states is a matrix.
    All of the casting to int() is JSON nonsense.
    """
    states[int(curr_state)][int(poss_state)] = val
    if compl_state is not None:
        states[int(curr_state)][int(compl_state)] = 1.0 - val


def ratio_to_sin(ratio):
    """
    Take a ratio of y to x and turn it into a sine.
    """
    return sin(ratio * pi / 2)


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
        user_log_err("Attempt to place " + str(agent2)
                     + " in non-group " + str(agent1))
        return False
    else:
        if not agent1.add_member(agent2):
            user_log_notif("Could not add mbr " + str(agent2)
                           + " to " + str(agent1))
        if not agent2.add_group(agent1):
            user_log_notif("Could not add grp "
                           + str(agent2)
                           + " to "
                           + str(agent1))
        return True


def split(agent1, agent2):
    """
    Break connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        user_log_err("Attempt to remove " + str(agent2)
                     + " from non-group " + str(agent1))
        return False
    else:
        agent1.del_member(agent2)
        agent2.del_group(agent1)
        return True


def switch(agent_nm, grp1_nm, grp2_nm, execution_key=None):
    """
    Move agent from grp1 to grp2.
    We first must recover agent objects from the registry.
    """
    agent = get_registration(agent_nm, execution_key=execution_key)
    if agent is None:
        user_log_notif("In switch; could not find agent: " + str(agent))
    grp1 = get_group(grp1_nm, execution_key=execution_key)
    if grp1 is None:
        user_log_notif("In switch; could not find from group: " + str(grp1))
    grp2 = get_group(grp2_nm, execution_key=execution_key)
    if grp2 is None:
        user_log_notif("In switch; could not find to group: " + str(grp2))
    split_em = split(grp1, agent)
    joined_em = join(grp2, agent)
    if DEBUG and split_em and joined_em:
        user_log_notif("Switched agent " + str(agent)
                       + " from grp " + grp1_nm
                       + "(id: " + str(id(grp1)) + ")"
                       + " to grp " + grp2_nm
                       + "(id: " + str(id(grp2)) + ")")


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
        elif isinstance(o, types.FunctionType):
            return get_func_name(o)  # can't JSON a function!
        else:
            return json.JSONEncoder.default(self, o)


class Agent(object):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    We are going to stop passing `env` around: we can call
    `env.get_env()` to get it when needed. So *soon* the
    env param here should go away, but only when every model
    is using the new call.
    """

    def __init__(self, name, attrs=None, action=None, duration=INF,
                 prim_group=None, serial_obj=None, reg=True, **kwargs):
        self.registry = {}

        self.execution_key = CLI_EXEC_KEY

        if EXEC_KEY in kwargs:
            self.execution_key = kwargs[EXEC_KEY]

        if serial_obj is not None:
            self.restore(serial_obj)
        else:  # or build it anew:
            self._construct_anew(name, attrs=attrs, action=action,
                                 duration=duration, prim_group=prim_group,
                                 reg=reg)
        if reg:
            register(self.name, self, execution_key=self.execution_key)

    def _construct_anew(self, name, attrs=None, action=None,
                        duration=INF, prim_group=None, reg=True):
        self.type = type(self).__name__
        self.name = name
        self.action_key = None
        self.action = action
        if action is not None:
            self.action_key = get_func_name(action)
        self.duration = duration
        self.neighbors = None
        self.attrs = {}
        if attrs is not None:
            self.attrs = attrs
        self.active = True
        self.pos = None
        self.prim_group = None if prim_group is None else str(prim_group)

    def set_prim_group(self, group):
        """
        We want this to store the name of the group.
        The str() of the group is its name.
        The str() of the name is itself.
        If we are passed None, set to blank.
        """
        if group is None:
            group = ""
        self.prim_group = str(group)

    def prim_group_nm(self):
        """
        prim_group is just a name, but we don't want models
        going straight at it!
        """
        return self.prim_group

    @property
    def env(self):
        """
        This is the env property.
        We use `registry.get_env()` to return whatever
        the registry has.
        """
        return get_env(execution_key=self.execution_key)

    @property
    def locator(self):
        """
        This is the locator property.
        We are cutting this over to just be the env!
        """
        return get_env(execution_key=self.execution_key)

    def restore(self, serial_obj):
        self.from_json(serial_obj)

    def to_json(self):
        return {"name": self.name,
                "type": self.type,
                "duration": self.duration,
                "pos": self.pos,
                "attrs": self.attrs,
                "active": self.active,
                "prim_group": self.prim_group,
                "neighbors": None,
                "action_key": self.action_key
                }

    def from_json(self, serial_agent):
        from registry.run_dict import action_dict
        self.action = None
        if serial_agent["action_key"] is not None:
            self.action = action_dict[serial_agent["action_key"]]
        self.action_key = serial_agent["action_key"]
        self.active = serial_agent["active"]
        self.attrs = serial_agent["attrs"]
        if not serial_agent["pos"]:
            self.pos = None
        else:
            self.pos = tuple(serial_agent["pos"])
        self.duration = int(serial_agent["duration"])
        self.name = serial_agent["name"]
        self.neighbors = None  # these must be re-created every run
        self.prim_group = serial_agent["prim_group"]
        self.type = serial_agent["type"]

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def primary_group(self):
        return get_group(self.prim_group, execution_key=self.execution_key)

    def group_name(self):
        return self.prim_group

    def is_located(self):
        return self.pos is not None

    def check_null_pos(fn):
        """
        Should be used to decorate any function that uses pos[X] or pos[Y]
        """

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # args[0] is self!
            if args[0].pos is None:
                user_log_err("Using the pos of an unlocated agent: "
                             + args[0].name + " in function "
                             + fn.__name__)
                return 0
            return fn(*args, **kwargs)

        return wrapper

    def set_pos(self, locator, x, y):
        self.pos = (x, y)

    def get_pos(self):
        return self.pos

    @check_null_pos
    def get_x(self):
        return self.pos[X]

    @check_null_pos
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

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def set_attr(self, key, val):
        self.attrs[key] = val

    def get_attr(self, key, default=None):
        if key in self.attrs:
            return self.attrs[key]
        else:
            return default

    def get(self, key, default=None):
        """
        This is a call to get_attr() to not break existing code
        that calls get().
        """
        self.get_attr(key, default=default)

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
            elif DEBUG2:
                user_log_notif("I'm " + self.name
                               + " and I have no action!")
        else:
            self.active = False
        return acted, moved

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
                if DEBUG2:
                    user_log_notif("Using angled move")
                new_xy = self.locator.point_from_vector(angle,
                                                        max_move, self.pos)
            self.locator.place_member(self, max_move=max_move, xy=new_xy)

    def is_active(self):
        return self.active

    def die(self):
        self.duration = 0
        self.pos = None
        self.active = False

    def del_group(self, group):
        if str(group) == self.prim_group:
            self.prim_group = None
            return True
        else:
            return False

    def add_group(self, group):
        if not self.prim_group:
            self.prim_group = str(group)
        return True

    def switch_groups(self, g1, g2):
        if not self.del_group(g1):
            user_log_notif("Could not delete ", str(g1))
        if not self.add_group(g2):
            user_log_notif("Could not add agent to ", str(g2))
