"""
This file defines a Composite, which is composed
of two (?) or more Entities (see entity.py).
"""
import numpy as np
import json
from random import uniform
from collections import OrderedDict

from entity import Entity, empty_dict


class Composite(Entity):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """

    def __init__(self, name, attrs=empty_dict, members=None):
        super().__init__(name, attrs=attrs)
        self.members = [] if members is None else members

    def __eq__(self, other):
        if self.type_sig != other.type_sig:
            return False
        else:
            return True

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __reversed__(self):
        return reversed(self.members)

    def __call__(self):
        """
        """
        for member in self.members:
            member()

    def __iadd__(self, scalar):
        pass

    def __isub__(self, scalar):
        pass

    def __imul__(self, scalar):
        pass

# numpy doesn't implement this! must investigage.
#    def __idiv__(self, scalar):
#        self.val_vect /= scalar
#        return self

    def magnitude(self):
        pass

    def to_json(self):
        return {"name": self.name, "attrs": self.attrs_to_dict(),
                "members": self.members}
