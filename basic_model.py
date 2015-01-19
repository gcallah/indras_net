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

    def act(self):
        print("Agent " + self.name + " with a goal of " + self.goal)


class Gozer(BasicAgent):
    """
    A silly agent that destroys others, for demo purposes
    """

    def __init__(self):
        super().__init__(name="Gozer", goal="Destroy!")


    def postact(self):
        e = self.env
        if len(e.agents) == 1:
            print("Gozer the destructor has destroyed all!!")
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

