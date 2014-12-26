"""
edgebox_model.py
An Edgeworth Box model where two agents trade goods.
"""
import entity

TRADE = "trade"


class EdgeboxAgent(entity.Agent):
    """
    Agents who attempt to trade goods to achieve greater utility
    """

    def __init__(self, name, goal=TRADE):
        super().__init__(name, goal)


    def act(self):
        print("Agent " + self.name + " with a goal of " + self.goal)


class EdgeboxEnv(entity.Environment):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, model_nm="edgebox_model"):
        super().__init__("An Edgeworth Box", model_nm=model_nm)

