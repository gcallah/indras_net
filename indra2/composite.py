"""
This file defines a Composite, which is composed
of two (?) or more Entities (see entity.py).
"""
import numpy as np
import json
from random import uniform
from collections import OrderedDict

from entity import Entity, empty_dict, EntEncoder


class Composite(Entity):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """

    def __init__(self, name, attrs=empty_dict, members=None):
        self.members = OrderedDict()
        if members is not None:
            self.members = members
        super().__init__(name, attrs=attrs)

    def __repr__(self):
        return json.dumps(self.to_json(), cls=EntEncoder)

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
        for member in self.members.values():
            member()

    def __iadd__(self, scalar):
        for member in self.members.values():
            member += scalar
        return self

    def __isub__(self, scalar):
        for member in self.members.values():
            member -= scalar
        return self

    def __imul__(self, scalar):
        for member in self.members.values():
            member *= scalar
        return self

# numpy doesn't implement this! must investigage.
#    def __idiv__(self, scalar):
#        self.val_vect /= scalar
#        return self

    def magnitude(self):
        pass

    def to_json(self):
        return {"name": self.name, "attrs": self.attrs_to_dict(),
                "members": self.members}
