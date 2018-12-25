"""
Entity will be the base class for all "things"
in the Indra world.
It's most basic appearance is as a vector.
"""

NAME_ID = 'Name'
SEP = ': '

class Entity:
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    """

    def __init__(self, name, attrs={}):
        self.name = name
        self.attrs = attrs

    def __str__(self):
        return self.name

    def __repr__(self):
        rep = NAME_ID + SEP + self.name + '\n'
        for attr in self.attrs:
            rep += attr + SEP + str(self.attrs[attr]) + '\n'
        return rep

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value
