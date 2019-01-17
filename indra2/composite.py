"""
This file defines a Composite, which is composed
of one or more Entities (see entity.py).
(A group might have its membership reduced to one!)
"""
import json
from collections import OrderedDict

import indra2.entity as ent


class Composite(ent.Entity):
    """
    This is the base class of all collections
    of entities. It itself is an entity.
    Its fundamental nature is that it is a set of vectors.
    """

    def __init__(self, name, attrs=None, members=None,
                 duration=ent.INF):
        self.members = OrderedDict()
        if members is not None:
            self.members = members
        super().__init__(name, attrs=attrs, duration=duration)

    def __repr__(self):
        return json.dumps(self.to_json(), cls=ent.EntEncoder, indent=4)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        # now check the unique fields here:
        for m in self:
            if m not in other:
                return False
            else:
                if self[m] != other[m]:
                    return False
        return True

    def __len__(self):
        return len(self.members)

    def __getitem__(self, key):
        """
        In contrast to entity, which returns a double val
        for getitem, for composites, we are going to return
        the 'key'th member.
        """
        return self.members[key]

    def __setitem__(self, key, member):
        """
        In contrast to entity, which sets a double val
        for getitem, for composites, we are going to return
        the 'key'th member.
        """
        self.members[key] = member

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
                    del_list.append(key)
        for key in del_list:
            print("Deleting key %s" % (key))
            del self.members[key]
        return total_acts

    def __add__(self, other):
        """
        This implements set union and returns
        a new Composite that is self union other.
        """
        new_dict = OrderedDict()
        new_dict.update(self.members)
        new_dict.update(other.members)
        return Composite(self.name + "+" + other.name,
                         members=new_dict)

    def __iadd__(self, other):
        """
        Add other to set self.
        """
        self.members.update(other.members)
        return self

    def __sub__(self, other):
        """
        This implements set difference and returns
        a new Composite that is self - other.
        """
        new_dict = self.members
        for mem in other.members:
            del(new_dict[mem])
        return Composite("new group", members=new_dict)

    def __isub__(self, other):
        """
        Remove item(s) in other if there, otherwise do nothing.
        """
        for member in other.members:
            self.members.pop(member, None)
        return self

    def __mul__(self, other):
        """
        This implements set intersection and returns
        a new Composite that is self intersect other.
        """
        new_dict = OrderedDict()
        new_dict.update(self.members)
        for mem in self.members:
            if mem not in other.members:
                del(new_dict[mem])
        return Composite("new group", members=new_dict)

    def __imul__(self, other):
        """
        When `other` is a Composite,
        this implements set intersection and makes the current
        Composite equal to self intersect other.
        """
        del_list = []
        for mem in self.members:
            if mem not in other.members:
                del_list.append(mem)
        for mem in del_list:
            del(self.members[mem])
        return self

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
