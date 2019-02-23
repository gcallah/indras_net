"""
This file defines a Composite, which is composed
of one or more Agents (see agent.py).
(A group might have its membership reduced to one!)
"""
import json
from collections import OrderedDict
from random import choice
from copy import copy

import indra2.agent as agt

DEBUG = False


def is_composite(thing):
    return hasattr(thing, 'members')


def grp_from_nmdict(nm, dict):
    grp = Composite(nm)
    grp.members = dict
    return grp


class Composite(agt.Agent):
    """
    This is the base class of all collections
    of entities. It itself is an agent.
    Its fundamental nature is that it is a set of vectors.

    Args:
        attrs: a dictionary of group properties
        members: a list of members, that will be turned
            into a dictionary
    """

    def __init__(self, name, attrs=None, members=None,
                 duration=agt.INF):
        self.members = OrderedDict()
        super().__init__(name, attrs=attrs, duration=duration)
        if members is not None:
            for member in members:
                member.join_group(self)
                # use member's str() val (usually name)
                # as the key to place it in our dict:
                self.members[str(member)] = member

    def __repr__(self):
        return json.dumps(self.to_json(), cls=agt.AgentEncoder, indent=4)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        # now check the unique fields here:
        for mbr in self:
            if mbr not in other:
                return False
            else:
                if self[mbr] != other[mbr]:
                    return False
        return True

    def __len__(self):
        return len(self.members)

    def __getitem__(self, key):
        """
        In contrast to agent, which returns a double val
        for getitem, for composites, we are going to return
        the 'key'th member.
        """
        return self.members[key]

    def __setitem__(self, key, member):
        """
        In contrast to agent, which sets a double val
        for setitem, for composites, we are going to set
        the 'key'th member.
        """
        self.members[key] = member

    def __delitem__(self, key):
        """
        This will delete a member from this composite.
        """
        del self.members[key]

    def __contains__(self, item):
        """
        A test whether item is a member of this set.
        """
        return item in self.members

    def __iter__(self):
        return iter(self.members)

    def __reversed__(self):
        return reversed(self.members)

    def __call__(self):
        """
        Call the members' functions.
        Later, this will just call agents' funcs.
        This should return the total of all
        agents who did, in fact, act in a
        particular call.
        """
        total_acts = 0
        del_list = []
        self.duration -= 1
        if self.duration > 0:
            for (key, member) in self.members.items():
                if member.isactive():
                    total_acts += member()
                else:
                    if DEBUG:
                        print("Marking " + key + " for deletion.")
                    del_list.append(key)
        for key in del_list:
            del self.members[key]
        return total_acts

    def __add__(self, other):
        """
        This implements set union and returns
        a new Composite that is self union other.
        If other is an atomic agent, just add it to
        this group.
        """
        new_dict = copy(self.members)
        if is_composite(other):
            new_dict.update(other.members)
        else:
            new_dict[other.name] = other
        new_grp = grp_from_nmdict(self.name + "+" + other.name, new_dict)
        self.join_group(new_grp)
        other.join_group(new_grp)
        return new_grp

    def __iadd__(self, other):
        """
        Add other to set self.
        If other is a composite, add all its members.
        If other is an atom, add it.
        """
        if is_composite(other):
            self.members.update(other.members)
        else:
            self[other.name] = other
            other.join_group(self)
        return self

    def __sub__(self, other):
        """
        This implements set difference and returns
        a new Composite that is self - other.
        """
        new_dict = copy(self.members)
        if is_composite(other):
            for mem in other.members:
                if mem in self.members:
                    del new_dict[mem]
        else:
            if other.name in self:
                del new_dict[other.name]
        return grp_from_nmdict(self.name + "-" + other.name, new_dict)

    def __isub__(self, other):
        """
        Remove item(s) in other if there, otherwise do nothing.
        """
        if is_composite(other):
            for member in other.members:
                self.members.pop(member, None)
        else:
            if other.name in self.members:
                del self[other.name]
        return self

    def __mul__(self, other):
        """
        This implements set intersection and returns
        a new Composite that is self intersect other.
        This has no useful meaning if `other` is an
        atom.
        """
        new_dict = copy(self.members)
        for mbr in self.members:
            if mbr not in other.members:
                del new_dict[mbr]
        return grp_from_nmdict(str(self) + "X" + str(other), new_dict)

    def __imul__(self, other):
        """
        When `other` is a Composite,
        this implements set intersection and makes the current
        Composite equal to self intersect other.
        """
        del_list = []
        for mbr in self.members:
            if mbr not in other.members:
                del_list.append(mbr)
        for mbr in del_list:
            del self.members[mbr]
        return self

    def rand_member(self):
        if len(self) > 0:
            # this is expensive: maybe we can speed it up
            # by not going to list somehow
            key = choice(list(self.members.keys()))
            return self[key]
        else:
            return None

    def subset(self, predicate, *args, name=None):
        new_dict = OrderedDict()
        for mbr in self:
            if predicate(self[mbr], *args):
                new_dict[mbr] = self[mbr]
        new_grp = Composite(name)
        new_grp.members = new_dict
        return new_grp

    def isactive(self):
        """
        A composite is active if any of its members are active;
        otherwise, it is inactive.
        """
        for member in self.members.values():
            if member.isactive():
                return True
        return False

    def magnitude(self):
        pass

    def to_json(self):
        return {"name": self.name,
                "attrs": self.attrs_to_dict(),
                "members": self.members}
