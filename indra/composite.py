"""
This file defines a Composite, which is composed
of one or more Agents (see agent.py).
(A group might have its membership reduced to one!)
"""
import json
from collections import OrderedDict
from copy import copy
from random import choice

from indra.agent import Agent, join, INF, is_composite, AgentEncoder
from registry.execution_registry import EXEC_KEY, \
    CLI_EXEC_KEY
from registry.registry import add_group
from indra.utils import get_func_name

DEBUG = False


def grp_from_nm_dict(nm, dictionary, execution_key=CLI_EXEC_KEY):
    grp = Composite(nm, execution_key=execution_key)
    grp.members = dictionary
    return grp


class Composite(Agent):
    """
    This is the base class of all collections
    of entities. It itself is an agent.
    Args:
        attrs: a dictionary of group properties
        members: a list of members, that will be turned
            into a dictionary
        member_creator: a function to create members
        num_members: how many to create
    """

    def __init__(self, name, attrs=None, members=None,
                 duration=INF, action=None, member_creator=None,
                 num_members=None, serial_obj=None,
                 reg=True, **kwargs):

        self.num_members_ever = 0
        self.members = OrderedDict()
        self.execution_key = CLI_EXEC_KEY

        if EXEC_KEY in kwargs:
            self.execution_key = kwargs[EXEC_KEY]

        super().__init__(name, attrs=attrs, duration=duration,
                         action=action, serial_obj=serial_obj,
                         reg=False, **kwargs)
        self.type = type(self).__name__

        if serial_obj is not None:
            self.restore(serial_obj)
        else:
            if members is not None:
                for member in members:
                    join(self, member)
            if num_members is None:
                num_members = 1  # A default if they forgot to pass this.
            self.num_members_ever = num_members
            self.member_creator = None
            if member_creator is not None:
                self.member_creator = member_creator
                # If we have a member creator function, call it
                # `num_members` times to create group members.
                for i in range(num_members):
                    join(self, member_creator(self.name, i, **kwargs))
        if reg:
            add_group(self.name, self, execution_key=self.execution_key)

    def restore(self, serial_obj):
        """
        Here we restore a composite from a serialized object.
        """
        self.from_json(serial_obj)

    def to_json(self):
        """
        Here we turn a composite into a serialized object.
        """
        rep = super().to_json()
        rep["num_members_ever"] = self.num_members_ever
        rep["type"] = self.type
        rep["members"] = self.members
        rep["member_creator"] = get_func_name(self.member_creator)
        return rep

    def from_json(self, serial_obj):
        from registry.run_dict import member_creator_dict
        super().from_json(serial_obj)
        self.num_members_ever = serial_obj["num_members_ever"]
        # we loop through the members of this composite
        for nm in serial_obj["members"]:
            member = serial_obj["members"][nm]
            if member["type"] == "Agent":
                self.members[nm] = Agent(name=nm, serial_obj=member,
                                         execution_key=self.execution_key)
            elif member["type"] == "Composite":
                self.members[nm] = Composite(name=nm, serial_obj=member,
                                             execution_key=self.execution_key)
        mem_create_nm = serial_obj["member_creator"]
        if mem_create_nm in member_creator_dict:
            self.member_creator = member_creator_dict[mem_create_nm]
        else:
            # if it's not in the above dict, we don't need the func,
            # we can just store its name:
            self.member_creator = mem_create_nm

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
        We are going to return the 'key' member
        of our member dictionary.
        """
        return self.members[key]

    def __setitem__(self, key, member):
        """
        In contrast to agent, which sets a val
        for setitem, for composites, we are going to set
        the 'key' member.
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

    def __call__(self, **kwargs):
        """
        Call the members' functions, and the composite's
        action func if it has one.
        This should return the total of all
        agents who acted in a particular call.
        """
        total_acts = 0
        total_moves = 0
        del_list = []
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                self.action(self, **kwargs)

            for (key, member) in self.members.items():
                if member.is_active():
                    (acted, moved) = member(**kwargs)
                    total_acts += acted
                    total_moves += moved
                else:
                    # delete agents but not composites:
                    if not is_composite(member):
                        del_list.append(key)
        for key in del_list:
            del self.members[key]
        return total_acts, total_moves

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
        new_grp = grp_from_nm_dict(self.name + "+" + other.name, new_dict,
                                   execution_key=self.execution_key)
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
        return True

    def del_member(self, member):
        """
        Should be called by split()
        """
        if str(member) in self.members:
            del self.members[str(member)]
            if member.primary_group() is self:
                member.set_prim_group(None)
        else:
            print("Attempt to del non-existent mbr: " + str(member))

    def rand_member(self):
        if len(self) > 0:
            # this is expensive: maybe we can speed it up
            # by not going to list somehow
            key = choice(list(self.members.keys()))
            return self[key]
        else:
            return None

    def subset(self, predicate, *args, name=None):  # noqa E999
        new_dict = OrderedDict()
        for mbr in self:
            if predicate(self[mbr], *args):
                new_dict[mbr] = self[mbr]
        return grp_from_nm_dict(name, new_dict)

    def is_active(self):
        """
        For now, composites just stay active.
        """
        return True
        # we should look at bringing back this logic at some point,
        # but the problem is it will block pending
        # actions like deleting dead members from the group.
        #        for member in self.members.values():
        #            if member.is_active():
        #                return True
        #        return False

    def ismember(self, agent):
        return str(agent) in self.members

    def is_mbr_comp(self, mbr):
        return is_composite(self.members[mbr])

    def pop_count(self, mbr):
        if self.is_mbr_comp(mbr):
            return len(self.members[mbr])
        else:
            return 1

    def magnitude(self):
        pass

    def has_color(self):
        return "color" in self.attrs

    def get_color(self):
        return self.attrs.get("color", None)

    def get_marker(self):
        return self.attrs.get("marker", None)

    def get_members(self):
        return self.members
