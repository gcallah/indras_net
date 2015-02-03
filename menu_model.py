"""
menu_model.py
You can clone this file and its companion menu_run.py
to easily get started on a new model.
It also is a handy tool to have around
for testing new features added to the base system.
"""
import entity as ent


class MenuAgent(ent.Agent):
    """
    An agent that just prints that it is around when asked to act
    """

    def __init__(self, name, goal):
        """
        A very menu init.
        """
        super().__init__(name, goal)


    def act(self):
        """
        Just print my name and goal!
        """
        print("Agent " + self.name + " with a goal of " + self.goal)


class MenuEnv(ent.Environment):
    """
    This environment is to test menu features
    """

    def __init__(self, model_nm=None):
        super().__init__("Menu test",
                         model_nm=model_nm, postact=True)
        self.menu = ent.TestMainMenu("Test menu", self)

