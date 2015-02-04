"""
basic_model.py
You can clone this file and its companion basic_run.py
to easily get started on a new model.
It also is a handy tool to have around
for testing new features added to the base system.
"""
import entity


class BasicAgent(entity.Agent):
    """
    An agent that just prints that it is around when asked to act
    """

    def __init__(self, name, goal):
        """
        A very basic init.
        """
        super().__init__(name, goal)


    def act(self):
        """
        Just print my name and goal!
        """
        print("Agent " + self.name + " with a goal of " + self.goal)


class Gozer(BasicAgent):
    """
    A silly agent that destroys others, for demo purposes
    """

    def __init__(self):
        """
        Init Gozer with slightly different params.
        """
        super().__init__(name="Gozer the Destructor", goal="Destroy!")


    def postact(self):
        """
        Check to see if we have wiped everyone out.
        """
        e = self.env
        if len(e.agents) == 1:
            print("Gozer the Destructor has destroyed all!!")
        else:
            for agent in e.agents:
                if agent is not self:
                    e.agents.remove(agent)
                    print("Gozer has destroyed "
                          + agent.name + "!")
                    return


class BasicEnv(entity.Environment):
    """
    This environment doesn't really do anything.
    """

    def __init__(self, model_nm=None):
        super().__init__("Basic environment",
                         model_nm=model_nm, postact=True)

