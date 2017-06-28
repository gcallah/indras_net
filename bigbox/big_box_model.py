"""
big_box_model.py
Simulates a small town with consumers.

The consumers may shop at either "Mom and Pop" and chain "Big Box" stores. The
town's consumers prefer the local stores, but will shot at the 
big box retailer when convenient. The major difference between Mom and 
Pops and Big Boxes is the larger endowment Big Boxes have initially.

Initially there are only local stores, but later the big box stores come in and 
change the population dynamic.
"""

import random
import collections
import math
import indra.utils as utils
import numpy as np
import indra.grid_agent as ga
import indra.grid_env as ge

MODEL_NM = "big_box_model"

pa = utils.read_props(MODEL_NM)

X = 0
Y = 1

NA = -1.0    # good not available

MOM_POP = 0
BIG_BOX = 1
NUM_STATES = 2

BB_MULT = 1000

# types of goods sold
HARDWARE = 0
HAIRCUT = 1
GROCERIES = 2
BOOKS = 3
COFFEE = 4
NUM_GOODS = 5

GOODS_MAP = {0: "Hardware", 1: "Haircut", 2: "Groceries",
             3: "Books", 4: "Coffee"}


class MarketParticipant(ga.GridAgent):
    """
    All agents in the small town participate in the economy. Only some
    sell goods of any type.
    """

    def __init__(self, name, goal, init_state=0):
        super().__init__(name, goal, NUM_STATES, init_state)

    def sells(self, good):
        """
        Does this participant sell this good?
        """
        return False


class Consumer(MarketParticipant):
    """
    Everyday consumer of EverytownUSA. He has a preference for the cosy
    small shops stores, but will buy occasionally from big boxes.

    Attributes:
        state: the number describing the agent's preference 
        for a type of marketparticipant 
        allowance: The amount the agent will buy from a store.
    """

    def __init__(self, name, goal, init_state, allowance):
        super().__init__(name, goal, init_state)
        self.state = init_state
        self.allowance = allowance
        self.last_util = 0.0       # what statisfaction did they get from
                                   # previous purchase?
        self.view = None

    def survey_env(self):
        """
        We survey the whole environment to see what 
        stores sell the good we want.

        Args: self
        Returns: 
            store_count: a list of all the marketparticipants in agent's travel
                distance that sell the good he wants.
        """
        if self.view is None:
            self.view = self.env.get_square_view(center=self.pos,
                distance=math.sqrt(self.env.width**2 + self.env.height**2))
        sellers = []
        sellers.extend(self.neighbor_iter(view=self.view,
                                  filt_func=lambda x: x.sells(self.goal)))
        return sellers

    def eval_env(self, sellers):
        """
        The Consumer determines who, of those who sell the good he desires,
        he will buy from.

        Args:
            n_census: a list of stores selling the agent's desired good
        Returns:
            a store selling that good
        """
        top_seller = None
        max_util = 0.0
        for seller in sellers:
            this_util = seller.utils_from_good(self.goal)
            if this_util > max_util:
                max_util = this_util
                top_seller = seller
        self.last_util = max_util
        return top_seller


    def respond_to_cond(self, store):
        """
        The agent moves to a store and buys from it.

        Args:
            store: the store to which we should move and buy from
        Returns:
            None
        """
        if store is not None:
            # print(self.name + " heading to " + store.name)
            self.move(store)
            store.buy_from(self.allowance)

    def move(self, store):
        """
        Moves as close as possible to the store.

        Arg:
            store: retailer to which we move
        """
        open_spot = self.env.free_spot_near(store)
        if(open_spot is not None):
            self.env.move(self, open_spot[X], open_spot[Y])

    def postact(self):
        """
        We cycle through the good the agent wants each turn.
        """
        self.goal = (self.goal + 1) % NUM_GOODS


class Retailer(MarketParticipant):
    """
    A Retailer is a MarketParticipant, who not only sells goods, but who
    is also responsible for paying bills and maintianing sufficent funds
    for operation.

    Attributes:
        funds: If less than zero, the business disappears.
        rent: how much is decremented from funds every step.
    """

    def __init__(self, name, goal, endowment, rent, adj=0.0):
        super().__init__(name, goal)
        self.funds = endowment
        self.rent = rent
        self.util_adj = adj

    def act(self):
        """
        Loses money. If it goes bankrupt, the business goes away.
        """
        print(self.funds)
        self.pay_bills(self.rent)
        if(self.funds <= 0):
            self.declare_bankruptcy()

    def buy_from(self, amt):
        """
        Agent buys from self, adding amt to self's funds.
        """
        self.funds += amt

    def declare_bankruptcy(self):
        """
        Removes the business from the town.
        """
        self.env.foreclose(self)

    def pay_bills(self, amt):
        """
        Lose funds.
        """
        self.funds -= amt

    def utils_from_good(self, good):
        if not self.sells(good):
            return NA
        else:
            return random.random() + self.util_adj

class MomAndPop(Retailer):
    """
    A small mom and pop store. It sells only one kind of good.

    Attributes:
        ntype: what it sells is its kind of store (e.g. if it sells groceries it is
            called "groceries")
    """

    def __init__(self, name, goal, endowment, rent, adj=0.0):
        super().__init__(name, goal, endowment, rent, adj)
        self.ntype = GOODS_MAP[goal]

    def sells(self, good):
        """
        Does this retailer sell this good?
        """
        return self.goal == good


class BigBox(Retailer):
    """
    A BigBox store. It sells all goods.
    """

    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal, endowment, rent)

    def sells(self, good):
        """
        Does this retailer sell this good?
        The big box retailer sells everything!
        """
        return True


class EverytownUSA(ge.GridEnv):
    """
    Just your typical city: filled with businesses and consumers.
    The city management will remove businesses that cannot pay rent!
    """

    def __init__(self, width, height, torus=False,
                 model_nm="Big Box Model"):
        super().__init__(width=width, name=model_nm, height=height, torus=torus,
                         model_nm=model_nm, postact=True)

    def postact_loop(self):
        """
        After all postactions, we add a BigBox store once we reach the 
        period the User determines during runtime.
        """
        super().postact_loop()
        # add big box store if right time.
        if self.period == self.props.get("bb_start_period"):
            self.add_agent(BigBox("Big Box", goal="Dominance",
                        endowment=(self.props.get("endowment") * BB_MULT),
                        rent=(self.props.get("rent") * BB_MULT)))

    def foreclose(self, business):
        """
        Removes business from town.
        """
        self.remove_agent(business)
