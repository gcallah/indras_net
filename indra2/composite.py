"""
This file defines a Composite, which is composed
of two (?) or more Entities (see entity.py).
"""
import json
from collections import OrderedDict

from entity import Entity, EntEncoder, INF


class Composite(Entity):
    """
    This is the base class of all collections
    of entities. It itself is an entity.
    """

    def __init__(self, name, attrs=None, members=None,
                 duration=INF):
        self.members = OrderedDict()
        if members is not None:
            self.members = members
        super().__init__(name, attrs=attrs, duration=duration)

    def __repr__(self):
        return json.dumps(self.to_json(), cls=EntEncoder, indent=4)

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
        return self.members[key]

    def __setitem__(self, key, member):
        self.members[key] = member

    def __contains__(self, item):
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
        new_dict = OrderedDict()
        if isinstance(other, Composite):
            new_dict.update(self.members)
            new_dict.update(other.members)
        # else must be written!
        return Composite(self.name + "+" + other.name,
                         members=new_dict)

    def __sub__(self, other):
        new_dict = OrderedDict()
        new_dict.update(self.members)
        for mem in other.members:
            new_dict.__delitem__(mem)
        return Composite("new group", members=new_dict)

    def __iadd__(self, other):
        if isinstance(other, Composite):
            self.members.update(other.members)
        elif isinstance(other, Entity):
            self.members[other.name] = other
        return self

    def __isub__(self, other):
        """
        Remove item(s) if there, otherwise do nothing.
        """
        if isinstance(other, Composite):
            for member in other.members:
                self.members.pop(member, None)
        elif isinstance(other, Entity):
            self.members.pop(other.name, None)
        return self

    def __imul__(self, scalar):
        # must think through what this should do!
        return self

    def isactive(self):
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
