"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json

from itime import Time
from space import Space  # , DEF_WIDTH, DEF_HEIGHT


class Env(Time, Space):
    """
    A collection of entities that share a space and time.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
