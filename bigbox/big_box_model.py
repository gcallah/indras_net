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

import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

X = 0
Y = 1

MP = 0
BB = 1
NUM_STATES = 2

# types of goods sold
HARDWARE = 0
HAIRCUT = 1
GROCERIES = 2
BOOKS = 3
COFFEE = 4
NUM_GOODS = 5

GOODS_MAP = {0: "Hardware", 1: "Haircut", 2: "Groceries",
             3: "Books", 4: "Coffee"}

class MarketParticipant(ma.MarkovAgent):

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
        state: Does agent want to buy from big boxes or small shops?
        allowance: The amount the agent will buy from a store.
    """

    def __init__(self, name, goal, init_state, allowance):
        super().__init__(name, goal, init_state)
        self.state = init_state
        self.allowance = allowance
        self.preference = MomAndPop
        self.max_dist = None

    def survey_env(self):
        """
            Args: self
            Returns: stores
        """
        if not self.max_dist:
            self.max_dist = self.env.get_max_dist()
        view = self.env.get_square_view(self.pos, self.max_dist)
        return self.neighbor_iter(view=view,
                                  filt_func=lambda x:
                                  x.sells(self.goal))

    def eval_env(self, stores):
        """
            Args:
                stores: a list of stores selling the agent's desired good
            Returns: a store of the preferred type
        """
        state_pre = self.env.get_pre(self)
        state_vec = markov.probvec_to_state(state_pre.matrix)
        state = markov.get_state(state_vec)
        self.assess_preference(state)
        for store in stores:
            if(type(store) is self.preference):
                return store

    def assess_preference(self, state):
        if(state == 0):
            self.preference = MomAndPop
        else:
            self.preference = BigBox

    def respond_to_cond(self, store):
        """
            Args:
                close_store: the store to which we should move.
            Returns: None
        """
        # if we need to test that consumers are moving between stores,
        # uncomment the following line:
        # print(self.name + " heading to " + store.name)
        self.move(store)
        store.buy_from(self.allowance)

    def move(self, store):
        """
        Moves as close as possible to the store.
        """
        open_spot = self.env.free_spot_near(store)
        if(open_spot is not None):
            self.env.move(self, open_spot[X], open_spot[Y])


    def postact(self):
        self.goal = (self.goal + 1) % NUM_GOODS


class Retailer(MarketParticipant):
    """
    Attributes:
        funds: If less than zero, the business disappears.
        rent: how much is decremented from funds every step.
    """

    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal)
        self.funds = endowment
        self.rent = rent

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
        Args:
            amt: amount to buy
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


class MomAndPop(Retailer):
    """
    A small mom and pop store. It has a much smaller initial endowment than the
    Big Box store.

    Attributes:
    """

    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal, endowment, rent)
        self.ntype = GOODS_MAP[goal]

    def sells(self, good):
        """
        Does this retailer sell this good?
        """
        return self.goal == good


class BigBox(Retailer):
    """
    """
    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal, endowment, rent)

    def sells(self, good):
        """
        Does this retailer sell this good?
        The big box retailer sells everything!
        """
        return True


class EverytownUSA(menv.MarkovEnv):
    """
    Just your typical city: filled with businesses and consumers.
    The city management will remove businesses that cannot pay rent!
    """

    def __init__(self, width, height, torus=False,
                model_nm="Big Box Model"):
        super().__init__(width=width, height=height, torus=torus, name=model_nm, postact=True)


    def foreclose(self, business):
        """
        Removes business from town.
        """
        self.remove_agent(business)

    def get_pre(self, agent):
        """
        Returns a vector prehension describing
        the chance an agent will prefer to go to
        a mom and pop or big box store.
        """
        return markov.MarkovPre("0.7 0.3")
