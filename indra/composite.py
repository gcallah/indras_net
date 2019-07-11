"""
This file defines a Composite, which is composed
of one or more Agents (see agent.py).
(A group might have its membership reduced to one!)
"""
import json
from collections import OrderedDict
from random import choice
from copy import copy

from indra.agent import Agent, join, INF, AgentEncoder, is_composite

DEBUG = False


def grp_from_nm_dict(nm, dict):
    grp = Composite(nm)
    grp.members = dict
    return grp


class Composite(Agent):
    """
    This is the base class of all collections
    of entities. It itself is an agent.
    Its fundamental nature is that it is a set of vectors.

    Args:
        attrs: a dictionary of group properties
        members: a list of members, that will be turned
            into a dictionary
        member_creator: a function to create members
        num_members: how many to create
    """

    def __init__(self, name, attrs=None, members=None,
                 duration=INF, action=None, member_creator=None,
                 num_members=None):
        self.members = OrderedDict()
        super().__init__(name, attrs=attrs, duration=duration,
                         action=action)
        if members is not None:
            for member in members:
                join(self, member)
        if member_creator is not None:
            for i in range(num_members):
                self += member_creator(name, i)

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

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
        join(self, member)

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
        agents who acted in a particular call.
        """
        total_acts = 0
        del_list = []
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                self.action(self)

            for (key, member) in self.members.items():
                if member.isactive():
                    total_acts += member()
                else:
                    # delete agents but not composites:
                    if not is_composite(member):
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
        if other is None:
            return self

        new_dict = copy(self.members)
        if is_composite(other):
            new_dict.update(other.members)
        else:
            new_dict[other.name] = other
        new_grp = grp_from_nm_dict(self.name + "+" + other.name, new_dict)
        self.add_group(new_grp)
        other.add_group(new_grp)
        return new_grp

    def __iadd__(self, other):
        """
        Add other to set self.
        If other is a composite, add all its members.
        If other is an atom, add it.
        """
        if other is None:
            return self

        if is_composite(other):
            for key in other:
                join(self, other[key])
        else:
            join(self, other)
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
        return grp_from_nm_dict(self.name + "-" + other.name, new_dict)

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
        return grp_from_nm_dict(str(self) + "X" + str(other), new_dict)

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

    def add_member(self, member):
        """
        Should be called by join()
        """
        self.members[str(member)] = member

    def del_member(self, member):
        """
        Should be called by split()
        """
        if str(member) in self.members:
            del self.members[str(member)]

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
        return grp_from_nm_dict(name, new_dict)

    def isactive(self):
        """
        For now, composites just stay active.
        """
        return True
# we should look at bringing back this logic at some point,
# but the problem is it will block pending actions like deleting dead members
# from the group.
#        for member in self.members.values():
#            if member.isactive():
#                return True
#        return False

    def is_mbr_comp(self, mbr):
        return is_composite(self.members[mbr])

    def pop_count(self, mbr):
        if self.is_mbr_comp(mbr):
            return len(self.members[mbr])
        else:
            return 1

    def magnitude(self):
        pass

    def to_json(self):
        return {"name": self.name,
                "attrs": self.attrs_to_dict(),
                "members": self.members}

    def attrs_to_dict(self):
        if self.attrs is not None:
            return self.attrs
        else:
            return "No attrs"

    def has_color(self):
        return "color" in self.attrs

    def get_color(self):
        return self.attrs.get("color", None)

    def get_marker(self):
        return self.attrs.get("marker", None)
