"""
basic_model.py
You can clone this file and its companion basic_run.py to easily get started on a new model.
It also is a handy tool to have around for testing new features added to the base system.
"""
import entity


class BasicAgent(entity.Agent):
    """
    An agent that just prints that it is around when asked to act
    """

    def act(self):
        print("Agent " + self.name + " with a goal of " + self.goal)


class BasicEnv(entity.Environment):
    """
    This environment doesn't really do anything.
    """

    def __init__(self, model_nm=None):
        super().__init__("a basic environment to get you going", model_nm=model_nm)

