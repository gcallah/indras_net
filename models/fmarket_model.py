"""
fmarket_model.py
A financial market model that includes chart followers
and value investors.
"""
# import logging
import indra.menu as menu
import indra.display_methods as disp
import stance_model as sm


class ChartFollower(sm.Follower):
    """
    A trend follower: buys what others are buying.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = ValueInvestor


class ValueInvestor(sm.Leader):
    """
    A value investor: buys what others are not buying.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = ChartFollower


class FinMarket(sm.StanceEnv):
    """
    A society of hipsters and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True)
        self.total_pop = 0  # to be set once we add agents
        self.asset_price = 10.0  # an arbitrary starting point
        self.price_hist = []
        self.max_abs_pmove = .5
        self.stances = ["buy", "sell"]
        self.line_graph_title = \
            "Asset trading model: Populations in %s adopting stance %s"
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew asset price",
                                                   self.view_pop))

    def census(self, disp=True):
        """
        Take a census of our pops.
        Here we add to our parent an adjustment of the asset price.
        """
        total_buyers = super().census(disp)
        self.user.tell("asset price = %f" % (self.asset_price))
        if self.total_pop == 0:
            # we should only need to do this once, as the model doesn't add
            # agents mid-stream.
            self.total_pop = self.get_total_pop()
        self.adj_asset_price(total_buyers)
        self.price_hist.append(self.asset_price)

    def adj_asset_price(self, total_buyers):
        buy_ratio = total_buyers / self.total_pop
        self.asset_price += self.max_abs_pmove * ((2.0 * buy_ratio) - 1.0)

    def view_pop(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        # put our data in right form for line graph
        data = {}
        data["asset price"] = {}
        data["asset price"]["data"] = self.price_hist
        data["asset price"]["color"] = disp.MAGENTA

        self.line_graph = disp.LineGraph("Asset price.", data, self.period)
