"""
barter_market_model.py
An barter market model where several agents trade goods.
"""
import logging
import entity
import spatial_agent
import edgebox_model as ebm

TRADE = "trade"

WINE = "wine"
CHEESE = "cheese"
OLIVE_OIL = "olive oil"


def util_func(qty):
    """
    A default util func: we can pass in others
    """
    return 10 - .5 * qty


class BarterMarketAgent(ebm.EdgeboxAgent):
    """
    Agents who attempt to trade goods to achieve greater utility.
    """

    def __init__(self, name, goal=TRADE):
        super().__init__(name, goal=goal)


    def act(self):
        super().act()


class BartermarketEnv(ebm.EdgeboxEnv):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__(name, length, height,
                        model_nm=model_nm)


