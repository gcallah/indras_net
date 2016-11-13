"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
This module contains the base classes for agent-based modeling in Indra.
"""

# import logging
from abc import abstractmethod
import indra.node as node


class Entity(node.Node):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    
    Attribute:
        env: the environment the agent lives within
    """

    def __init__(self, name):
        super().__init__(name)
        self.env = None

    def add_env(self, env):
        """
        Note our environment.
        """
        self.env = env


class Agent(Entity):

    """
    This class adds a goal to an entity
    and is the base for all other agents.
    
    All agents act. For reasons of clarity
    they *may* also act before or after this
    action.
    
    Attribute:
        goal: Often, this is a string which helps
            the user understand what the agent
            is "up to." It might also be used to
            inform the env what kind of action
            the agent will take.
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
        Empty for the moment.
        """
        return None

    def debug_info(self):
        """
        Relevant debugging info.
        """
        s = super().debug_info() + "\ngoal: " + str(self.goal)
        return s

    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!)
        """
        safe_fields = super().to_json()
        safe_fields["goal"] = self.goal
        return safe_fields
