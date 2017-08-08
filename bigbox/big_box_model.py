"""
big_box_model.py
Simulates a small town with consumers.

The consumers may shop at either "Mom and Pop" and
chain "Big Box" stores. The
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
import indra.utils as utils
import indra.menu as menu
import indra.grid_agent as ga
import indra.grid_env as ge
import indra.display_methods as disp
import indra.data_methods as data

MODEL_NM = "big_box_model"

pa = utils.read_props(MODEL_NM)

X = 0
Y = 1

NA = -1.0    # good not available

MOM_POP = 0
BIG_BOX = 1
NUM_STATES = 2

BB_MULT = 1000
BB_DIV = 200

MIN_ADJ = 0.01  # never offer 0 utils for a purchase

# types of goods sold
HARDWARE = 0
HAIRCUT = 1
GROCERIES = 2
BOOKS = 3
COFFEE = 4
NUM_GOODS = 5

GOODS_MAP = {0: "Hardware", 1: "Barber", 2: "Grocery",
             3: "Book Store", 4: "Coffee Shop"}


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
        self.last_utils = 0.0      # what statisfaction did they get from
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
        sellers.extend(self.neighbor_iter(
                       view=self.view,
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
        self.last_utils = max_util
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
            store.purchase(self.allowance)

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
    is also responsible for paying bills and maintianing sufficent capital
    for operation.

    Attributes:
        capital: If less than zero, the business disappears.
        expenses: how much is decremented from capital every step.
    """

    def __init__(self, name, goal, endowment, expenses, adj=MIN_ADJ):
        super().__init__(name, goal)
        self.capital = endowment
        self.expenses = expenses
        self.util_adj = adj

    def act(self):
        """
        Loses money. If it goes bankrupt, the business goes away.
        """
        self.env.user.tell(self.name + " has capital of: "
                           + str(self.capital)
                           + " and is paying expenses of "
                           + str(self.expenses))
        self.pay_bills(self.expenses)
        if(self.capital <= 0):
            self.declare_bankruptcy()

    def purchase(self, amt):
        """
        Agent buys from retailer, adding amt to retailer's capital.
        """
        self.capital += amt

    def declare_bankruptcy(self):
        """
        Removes the business from the town.
        """
        self.env.foreclose(self)

    def pay_bills(self, amt):
        """
        Lose capital.
        """
        self.capital -= amt

    def utils_from_good(self, good):
        if not self.sells(good):
            return NA
        else:
            return random.random() + self.util_adj

class MomAndPop(Retailer):
    """
    A small mom and pop store. It sells only one kind of good.

    Attributes:
        ntype: what it sells is its kind of store
    """

    def __init__(self, name, goal, endowment, expenses, adj=MIN_ADJ):
        # name them after what good they sell:
        type = GOODS_MAP[goal]
        super().__init__(type, goal, endowment, expenses, adj)
        self.ntype = type

    def sells(self, good):
        """
        Does this retailer sell this good?
        """
        return self.goal == good


class BigBox(Retailer):
    """
    A BigBox store. It sells all goods.
    """

    def __init__(self, name, goal, endowment, expenses):
        super().__init__(name, goal, endowment, expenses)

    def sells(self, good):
        """
        Does this retailer sell this good?
        The big box retailer sells everything!
        """
        return True


class EverytownUSA(ge.GridEnv):
    """
    Just your typical city: filled with businesses and consumers.
    The city management will remove businesses that cannot pay expenses!
    """

    def __init__(self, width, height, torus=False,
                 model_nm="Big Box Model", props=None):
        super().__init__(width=width, name=model_nm,
                         height=height, torus=torus,
                         model_nm=model_nm, postact=True,
                         props=props)
        self.utils = 0.0
        self.menu.view.add_menu_item("v", menu.MenuLeaf("(v)iew utility",
                                     self.view_util))
        self.add_variety("BigBox")
        self.mom_pop_pop = []
        self.util_hist = []

    def assemble_util_vars(self):
        varieties = None
        varieties = disp.assemble_lgraph_data("Mom and Pops", self.mom_pop_pop,
                                         disp.MAGENTA)
        varieties = disp.assemble_lgraph_data("Consumer Utils", self.util_hist,
                                         disp.GREEN, data=varieties)
        varieties = disp.assemble_lgraph_data("Big Boxes",
                                         self.agents.get_var_pop_hist("BigBox"),
                                         disp.BLUE, data=varieties)
        return varieties

    def view_util(self):
        """
        Graph population of stores versus consumer utility.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        self.line_graph = disp.LineGraph("Consumer Utility vs. # Retailers",
                                         self.assemble_util_vars(),
                                         self.period)

    def pop_report(self):
        """
        Write CSV file with utility versus retail pop data.
        """
        file_nm = self.user.ask("Choose file name: ")
        varieties = self.assemble_util_vars()
        data.pop_report(file_nm, varieties)

    def postact_loop(self):
        """
        After all postactions, we add a BigBox store once we reach the 
        period the User determines during runtime.
        """
        super().postact_loop()
        # add big box store if right time.
        if self.period == self.props.get("bb_start_period"):
            self.add_agent(BigBox("Big Box Store",
                        goal="Dominance",
                        endowment=(self.props.get("endowment") * BB_MULT),
                        expenses=((self.props.get("expenses") * BB_MULT)
                              // BB_DIV)))
            # div BB_DIV sets the expense / capital ratio

    def foreclose(self, business):
        """
        Removes business from town.
        """
        self.remove_agent(business)

    def census(self, disp=True):
        """
        Take a census of our pops: here we want consumer util
        graphed against numbers of other types.
        """
        super().census(exclude_var="Consumer") # usual census for retailers
        utils = 0
        for shopper in self.variety_iter("Consumer"):
            utils += shopper.last_utils
        self.util_hist.append(utils)
        self.user.tell("Consumer utility gained this period: "
                       + str(int(utils)))
        mp_count = 0
        for agent in self.agents:
            if isinstance(agent, MomAndPop):
                mp_count += 1
        self.mom_pop_pop.append(mp_count)
