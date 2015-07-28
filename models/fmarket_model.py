"""
fmarket_model.py
A financial market model that includes chart followers
and value investors.
"""
# import logging
import indra.menu as menu
import stance_model as sm

stances = ["buy", "sell"]


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
        self.stances = ["buy", "sell"]
        self.line_graph_title = \
            "Asset trading model: Populations in %s adopting stance %s"
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew traders",
                                                   self.view_pop))
