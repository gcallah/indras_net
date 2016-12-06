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
import numpy as np
import indra.vector_space as vs
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
        state: the number describing the agent's preference for a type of marketparticipant 
        allowance: The amount the agent will buy from a store.
        preference: The marketparticipant the agent will buy from
    """

    def __init__(self, name, goal, init_state, allowance):
        super().__init__(name, goal, init_state)
        self.state = init_state
        self.allowance = allowance
        self.preference = MomAndPop        

    def survey_env(self):
        """
        We survey the whole environment to see what stores sell the good we want.

        Args: self
        Returns: 
            store_count: a list of all the marketparticipants in agent's travel distance
                that sell the good he wants.
        """
        view = self.env.get_square_view(center=self.pos,
                                        distance=math.sqrt(self.env.width**2 + self.env.height**2))
        n_census = []
        n_census.extend(self.neighbor_iter(view=view,
                                  filt_func=lambda x:
                                  x.sells(self.goal)))
        return n_census

    def eval_env(self, n_census):
        """
            Args:
                self: the agent himself
                n_census: a list of stores selling the agent's desired good
            Returns: a store of the preferred type
        """
        self.state_pre = self.env.get_pre(self, n_census)
        self.state_vec = markov.probvec_to_state(self.state_pre.matrix)
        self.state = markov.get_state(self.state_vec)
        
        if(self.state == 0):
            self.preference = MomAndPop
        if(self.state == 1):
            self.preference = BigBox

        for store in n_census:
            if type(store) is self.preference:
                return store
                
    def respond_to_cond(self, store):
        """
            Args:
                store: the store to which we should move and buy from
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
            Arg:
                store: marketparticipant to which we move
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
    A small mom and pop store. It sells only one kind of good.

    Attributes:
        ntype: what it sells is its kind of store (e.g. if it sells groceries it is
            called "groceries")
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

    def get_pre(self, agent, n_census):
        """
        Args:
            self: the env 
            agent: the agent who is considering where to go 
            n_census: a list of stores to which the agent may go
        Returns:
            a state vector prehension giving the probablility the
            agent will go to a kind of marketparticipant
        """
        
        trans_str = ""

        if(self.there_is(n_census, MomAndPop)):
                # Test ... to un-hardcode later
            trans_str += "0.7 " 
        else:
            trans_str += "0.0 "

        if(self.there_is(n_census, BigBox)):
            trans_str += "0.3"
        else:
            trans_str += "0.0"

        state_pre = markov.from_matrix(np.matrix(trans_str))
        state_pre.matrix = vs.normalize(state_pre.matrix)
        return state_pre

    def there_is(self, n_census, vendor_type):
        """
        Is there this type of store in the area?
        Args:
            n_census: the complete list of stores
            vendor_type: the type of marketparticipant 
            we are looking to see is in the area
        """
        for store in n_census:
            if type(store) is vendor_type:
                return True
        return False
