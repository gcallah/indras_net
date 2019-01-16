"""
This file defines a Composite, which is composed
of two (?) or more Entities (see entity.py).
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
        """
        del_list = []
        self.duration -= 1
        if self.duration > 0:
            for (key, member) in self.members.items():
                if member.isactive():
                    member()
                else:
                    del_list.append(key)
        for key in del_list:
            print("Deleting key %s" % (key))
            del self.members[key]

    def __add__(self, other):
        """
        This implements set union and returns
        a new Composite that is self union other.
        """
        new_dict = OrderedDict()
        if isinstance(other, Composite):
            new_dict.update(self.members)
            new_dict.update(other.members)
        # else must be written!
        return Composite(self.name + "+" + other.name,
                         members=new_dict)

    def __iadd__(self, other):
        """
        Add other to set self.
        """
        if isinstance(other, Composite):
            self.members.update(other.members)
        elif isinstance(other, ent.Entity):
            self.members[other.name] = other
        else:
            print("Don't know what to iadd; type(other) = ")
            print(type(other))
        return self

    def __sub__(self, other):
        """
        This implements set difference and returns
        a new Composite that is self - other.
        """
        new_dict = self.members
        if isinstance(other, Composite):
            for mem in other.members:
                new_dict.__delitem__(mem)
        elif isinstance(other, ent.Entity):
            new_dict.pop(other.name, None)
        else:
            print("Don't know what to sub; type(other) = ")
            print(type(other))
        return Composite("new group", members=new_dict)

    def __isub__(self, other):
        """
        Remove item(s) in other if there, otherwise do nothing.
        """
        if isinstance(other, Composite):
            for member in other.members:
                self.members.pop(member, None)
        elif isinstance(other, ent.Entity):
            self.members.pop(other.name, None)
        else:
            print("Don't know what to isub; type(other) = ")
            print(type(other))
        return self

    def __mul__(self, other):
        """
        This implements set intersection and returns
        a new Composite that is self intersect other.
        """
        new_dict = OrderedDict()
        if isinstance(other, Composite):
            new_dict.update(self.members)
            for mem in self.members:
                if mem not in other.members:
                    new_dict.__delitem__(mem)
        elif isinstance(other, ent.Entity):
            if other in self.members:
                new_dict[other.name] = other
        else:
            print("Don't know what to mul; type(other) = ")
            print(type(other))
        return Composite("new group", members=new_dict)

    def __imul__(self, other):
        """
        This implements set intersection and makes the current
        Composite equal to self intersect other.
        """
        del_list = []
        if isinstance(other, Composite):
            for mem in self.members:
                if mem not in other.members:
                    del_list.append(mem)
        for mem in del_list:
            self.members.__delitem__(mem)
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
