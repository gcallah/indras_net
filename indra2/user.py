"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json

from indra2.agent import Agent

TERMINAL = "terminal"
WEB = "web"
GUI = "gui"


class TermUser(Agent):
    """
    A representation of the user in the system.
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def __call__(self):
        self.tell("What would you like to do?")

    def tell(self, msg):
        print(msg)
