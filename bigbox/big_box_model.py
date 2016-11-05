"""
big_box_model.py

Simulates a small town with consumers.

The consumers may shop at either "Mom and Pop" and chain "Big Box" stores.
The town's consumers prefer the local stores, but will shot at the big box
retailer when convenient. The major difference between Mom and Pops and Big
Boxes is the larger endowment Big Boxes have initially. Initially there are
only local stores, but later the big box stores come in and change the
population dynamic.
"""

import math
import random
import indra.display_methods as disp
import indra.grid_agent as ga
import indra.grid_env as genv
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

X = 0
Y = 1

NSTATES = 2

CONSUMER = "consumer"
MOM_AND_POP = "mom_and_pop"
BIGBOX = "big_box"

MP = 0
BB = 1

STATE_MAP = { MP: MOM_AND_POP, BB: BIGBOX }

class Consumer(ma.MarkovAgent):
    """
    Everyday consumer of EverytownUSA. He has a preference for the cosy
    Mom_And_Pop stores, but will buy occasionally from Big_Box.
    Attributes:
        ntype: node type in graph
        state: Does agent want to buy from Big_Box or Mom_And_Pop?
        allowance: The amount the agent will buy from a store.
        hunger: increments each step; when maxed, consumer spends allowance
        max_hunger: maximum hunger, when reached, consumer spends allowance
    """

    def __init__(self, name, goal, init_state, allowance, max_hunger):
        super().__init__(name, goal, NSTATES, init_state)
        self.ntype = CONSUMER
        self.state = init_state
        self.allowance = allowance
        self.hunger = random.randint(0,max_hunger)
        self.max_hunger = max_hunger

    def buy_from(self, store, amount):
        """
        Consumer adds to store's funds.
        """
        store.funds += amount

    def act(self):
        """
        Decide which store to buy from (mom and pop or big box?),
        go there, and make a purchase.
        """
        if(self.hunger >= self.max_hunger):
            store = self.find_nearby_store(Mom_And_Pop)
            self.move(store)
            self.buy_from(store, self.allowance)
            self.hunger = 0
        else:
            self.hunger += 1
            self.move_to_empty()
        
    def find_nearby_store(self, preference):
        """
        Looks for store (of preferred type) closest to
        the agent.
        Arguments:
            preference: either Mom_and_Pop or Big_Box
        Returns:
            Store: the particular store he'll move to.
        """
        filt_func = lambda x: type(x) is preference
        whole_map_range = max(self.env.height, self.env.width)
        view = self.env.get_square_view(self.pos, whole_map_range)
        stores = self.neighbor_iter(view=view, filt_func=filt_func)

        close_store = None
        max_dist = self.env.get_max_dist()
        for store in stores:
            dist = self.env.dist(self,store)
            if(dist < max_dist):
                close_store = store
                max_dist = dist

        return close_store
        
    def move(self, store):
        """
        Moves as close as possible to the store.
        """
        open_spot = self.env.free_spot_near(store)
        if(open_spot == None): # Safegaurd: If nowhere to move, stay put.
            open_spot = self.pos

        self.env.move(self, open_spot[X], open_spot[Y])

class Store(ga.GridAgent):
    """
    A store. Occupying a spot on the grid, it uses it's funds to pay
    rent. If the funds vanish, it is removed from the env. Consumers
    increase its pool of funds if they decide to visit.
    
    Attributes:
        ntype: The kind of store it is.
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
        self.pay_bills(self.rent)
        if(self.funds <= 0):
            self.declare_bankruptcy()

    def declare_bankruptcy(self):
        """
        Removes the business from the town.
        """
        self.env.foreclose(self)

    def pay_bills(self, amount):
        """
        Lose funds.
        """
        self.funds -= amount


class Mom_And_Pop(Store):
    """
    A small mom and pop store. It has a much smaller initial endowment than the
    Big Box store.
    Attributes:
        ntype: The kind of store it is.
        funds: If less than zero, the business disappears.
        rent: how much is decremented from funds every step.
    """

    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal, endowment, rent)
        self.ntype = MOM_AND_POP


class Big_Box(Store):
    """
    A large big box store. It has a much larger initial endowment than the
    little Mom and Pop store.
    Attributes:
        ntype: The kind of store it is.
        funds: If less than zero, the business disappears.
        rent: how much is decremented from funds every step.
    """

    def __init__(self, name, goal, endowment, rent):
        super().__init__(name, goal, endowment, rent)
        self.ntype = BIGBOX


class EverytownUSA(menv.MarkovEnv):
    """
    Just your typical town: filled with businesses and consumers.
    The city management will remove businesses that cannot pay rent!
    """

    def __init__(self, width, height, torus=False,
                model_nm="Big Box Model"):
        super().__init__(width=width, height=height, torus=torus, name=model_nm)

        self.set_var_color(CONSUMER, disp.YELLOW)
        self.set_var_color(MOM_AND_POP, disp.GREEN)
        self.set_var_color(BIGBOX, disp.RED)

    def foreclose(self, business):
        """
        Removes business from town.
        """
        self.remove_agent(business)
