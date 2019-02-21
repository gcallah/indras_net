"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json

from itime import Time, DEF_TIME
from space import Space


class Env(Space):
    """
    A collection of entities that share a space and time.
    An env *is* a space and *has* a timeline.
    That makes the inheritance work out as we want it to.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.time = Time(name, **kwargs)
        self.time.members = self.members

    def __call__(self, periods=DEF_TIME):
        self.time(periods)
