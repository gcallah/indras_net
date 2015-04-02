"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
This module contains the base classes for agent-based modeling in Indra.
"""

from abc import abstractmethod
import logging
import indra.node as node


class Entity(node.Node):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    """

    def __init__(self, name):
        super().__init__(name)
        self.prehensions = []
        self.env = None

    def add_env(self, env):
        """
        Note our environment.
        """
        self.env = env

    def pprint(self):
        """
        Print out me in a nice format.
        """
        for key, value in self.__dict__.items():
            print(key + " = " + str(value))


class Agent(Entity):

    """
    This class adds a goal to an entity
    and is the base for all other agents.
    """

    def __init__(self, name, goal=None):
        super().__init__(name)
        self.goal = goal

    @abstractmethod
    def act(self):
        """
        What agents do.
        """
        pass

    def preact(self):
        """
        What agents do before they act.
        """
        pass

    def postact(self):
        """
        What agents do after they act.
        """
        pass

    def survey_env(self, universal):
        """
        Return a list of all prehended entities
        in env.
        """
        logging.debug("scanning env for " + universal)
        prehended = []
        prehends = node.get_prehensions(prehender=self.get_type(),
                                        universal=universal)
        if prehends is not None:
            for pre_type in prehends:
                some_pres = self.env.get_agents_of_var(pre_type)
                prehended.extend(some_pres)
        return prehended

    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!
        """
        safe_fields = super().to_json()
        safe_fields["goal"] = self.goal
        return safe_fields
