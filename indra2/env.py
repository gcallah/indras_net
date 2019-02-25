"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json
import os

from itime import Time, DEF_TIME
from space import Space, DEBUG
from user import TermUser, TERMINAL


class Env(Space):
    """
    A collection of entities that share a space and time.
    An env *is* a space and *has* a timeline.
    That makes the inheritance work out as we want it to.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.time = Time(name, **kwargs)
        user_type = os.getenv("user_type", TERMINAL)
        if user_type == TERMINAL:
            self.user = TermUser(os.getenv("USER"), self)
            self.user.tell("Welcome to Indra, " + str(self.user) + "!")

    def __call__(self):
        if self.user is not None:
            while True:
                # run until user exit!
                self.user()

    def runN(self, periods=DEF_TIME):
        self.time.members = self.members  # so members are always in sync
        if DEBUG:
            # ensure we aren't getting a copy!
            assert self.time.members is self.members
        self.time(periods)
