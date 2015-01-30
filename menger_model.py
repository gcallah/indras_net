"""
menger_model.py
The aim of this model is to get money to arise
in a barter economy.
"""
import entity
import barter_model as bm


class MengerAgent(bm.BarterAgent):
    """
    Agents who get continually endowed with goods (produce)
    and whom we hope will start to use money to trade them.
    """

    def __init__(self, name, goal):
        """
        A very basic init.
        """
        super().__init__(name, goal)


    def act(self):
        """
        Trade.
        """
        super().act()


class MengerEnv(bm.BarterEnv):
    """
    An env to host money-using agents.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__("Menger environment",
                         length, height,
                         model_nm=model_nm)

