"""
menger_model.py
The aim of this model is to get money to arise
in a barter economy.
"""
import logging
import random
import entity as ent
import edgebox_model as ebm
import barter_model as bm


class MengerAgent(bm.BarterAgent):
    """
    Agents who get continually endowed with goods (produce)
    and whom we hope will start to use money to trade them.
    """

    def __init__(self, name, goal=bm.TRADE,
                 max_detect=ebm.GLOBAL_KNOWLEDGE ):
        super().__init__(name, goal=goal, max_detect=max_detect)
        self.prod_good = None
        self.prod_amt = 1


    def act(self):
        """
        Trade, but first, produce our good..
        """
        if self.prod_good is not None:
            print("Endowing da agent "
                  + self.name + " wid some " + self.prod_good)
            self.endow(self.prod_good, self.prod_amt)
        super().act()


class MengerEnv(bm.BarterEnv):
    """
    An env to host money-using agents.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__("Menger environment",
                         length, height,
                         model_nm=model_nm,
                         preact=True)


    def add_prod_goods(self):
        """
        Add who produces which good, and
        make them a vendor of that good in the market.
        """
        print("In add_prod_goods")
        for agent in self.agents:
            print("Adding prod goods to agents")
            good = random.choice(list(self.market.keys()))
            agent.prod_good = good
            self.market.add_vendor(good, agent)
        print("Market = " + str(self.market))

