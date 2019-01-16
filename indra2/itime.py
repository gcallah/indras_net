"""
This file defines Time, which is a collection
of entities that share a timeline.
"""
# import json

from composite import Composite

DEF_TIME = 100  # arbitrary: change as we explore!


class Time(Composite):
    """
    A collection of entities that share a timeline.
    """

    def __init__(self, name, attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)

    def __call__(self, periods=DEF_TIME):
        """
        __call__ calls the members' functions `periods` times.
        """
        acts = 0
        for i in range(periods):
            print("\nIn period " + str(i) + ":\n")
            acts += super().__call__()
        return acts
