"""
timer_model.py
An agent that does nothing to allow timing of other code portions
more accurately.
"""
import entity


class TimerAgent1(entity.Agent):
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
        Just pass.
        """
        pass


class TimerAgent2(entity.Agent):
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
        Just pass.
        """
        pass


class TimerAgent3(entity.Agent):
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
        Just pass.
        """
        pass


class TimerEnv(entity.Environment):
    """
    This environment doesn't really do anything.
    """

    def __init__(self, model_nm=None):
        super().__init__("Timer environment",
                         model_nm=model_nm)
 

    def act_loop(self):
        """
        We can change the looping behavior here to
        test the efficiency of various looping methods.
        """
        for agent in reversed(self.agents):
            agent.act()
