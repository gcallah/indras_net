"""
This file defines Time, which is a collection
of entities that share a timeline.
"""
# import json

from entity import empty_dict
from composite import Composite

MAX_TIME = 1000  # arbitrary: change as we explore!


class Time(Composite):
    """
    A collection of entities that share a timeline.
    """

    def __init__(self, name, attrs=empty_dict, members=None,
                 periods=MAX_TIME):
        super().__init__(name, attrs=attrs, members=members)
        self.periods = periods

    def __call__(self):
        """
        Call the members' functions `period` times.
        """
        for i in range(self.periods):
            print("\nIn period " + str(i) + ":\n")
            super().__call__()
