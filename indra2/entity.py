"""
This file defines an Entity.
"""
import json
from collections import OrderedDict

NAME_ID = 'Name'
SEP = ': '

empty_dict = OrderedDict()


def type_hash(attrs):
    """
    type_hash() will return an ID that identifies
    the ABM type of an entity.
    """
    return len(attrs)  # temp solution!


class Entity:
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """

    def __init__(self, name, attrs=empty_dict):
        self.name = name
        self.attrs = attrs
        self.type_sig = type_hash(attrs)

    def __eq__(self, other):
        if self.type_sig != other.type_sig:
            print("Failing because type sigs are diff.")
            return False
        else:
            for key in self.attrs:
                if self.attrs[key] != other.attrs[key]:
                    return False
            return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(self.to_json())

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __contains__(self, item):
        return item in self.attrs

    def same_type(self, other):
        return self.type_sig == other.type_sig

    def to_json(self):
        return {"name": self.name, "attrs": self.attrs}
