"""
fmarket_model.py
A financial market model that includes chart followers
and value investors.
"""
# import logging
import indra.menu as menu
import indra.display_methods as disp
import stance_model as sm

INIT_PRICE = 10.0
INIT_ENDOW = INIT_PRICE * 10.0
BUY = sm.INIT_FLWR
SELL = sm.INIT_LDR


class FinancialAgent(sm.StanceAgent):
    """
    A financial agent who trades an asset.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.profit = 0.0
        self.funds = INIT_ENDOW

    def change_stance(self):
        super().change_stance()
        if self.stance == BUY:
            self.funds -= self.env.asset_price
        else:
            self.funds += self.env.asset_price
        self.profit = self.funds - INIT_ENDOW


class ChartFollower(FinancialAgent, sm.Follower):
    """
    A trend follower: buys what others are buying.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = ValueInvestor


class ValueInvestor(FinancialAgent, sm.Leader):
    """
    A value investor: buys what others are not buying.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = ChartFollower


def get_profits(a):
    return a.profit


class FinMarket(sm.StanceEnv):
    """
    A society of value investors and chart followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True)
        self.total_pop = 0  # to be set once we add agents
        self.asset_price = INIT_PRICE  # an arbitrary starting point
        self.price_hist = []
        self.max_abs_pmove = .5
        self.stances = ["buy", "sell"]
        self.line_graph_title = \
            "Asset trading model: Populations in %s adopting stance %s"
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew asset price",
                                                   self.view_price))

    def census(self, disp=True):
        """
        Take a census of our pops.
        Here we add to our parent an adjustment of the asset price.
        """
        total_buyers = super().census(disp, census_func=get_profits)
        self.user.tell("asset price = %f" % (self.asset_price))
        if self.total_pop == 0:
            # we should only need to do this once, as the model doesn't add
            # agents mid-stream.
            self.total_pop = self.get_total_pop()
        self.adj_asset_price(total_buyers)
        self.price_hist.append(self.asset_price)
        for v in self.varieties_iter():
            p = self.get_pop_data(v)
            self.user.tell("Group %s has a net profit of %f." % (v, p))

    def adj_asset_price(self, total_buyers):
        buy_ratio = total_buyers / self.total_pop
        self.asset_price += self.max_abs_pmove * ((2.0 * buy_ratio) - 1.0)

    def view_price(self):
        """
        Draw a graph of our changing asset price.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        # put our data in right form for line graph
        data = disp.assemble_lgraph_data("asset price", self.price_hist,
                                         disp.MAGENTA)

        self.line_graph = disp.LineGraph("Asset price history", data,
                                         self.period)
