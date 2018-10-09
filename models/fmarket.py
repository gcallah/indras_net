"""
fmarket_model.py
A financial market model that includes chart followers
and value investors.
"""
import logging
import indra.menu as menu
import indra.display_methods as disp
import indra.two_pop_model as tp

INIT_PRICE = 10.0
INIT_ENDOW = INIT_PRICE * 10.0
BUY = tp.INIT_FLWR
SELL = tp.INIT_LEDR


class FinancialAgent(tp.TwoPopAgent):
    """
    A financial agent who trades an asset.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.profit = 0.0
        self.funds = INIT_ENDOW

    def direction_changed(self, curr_direct, new_direct):
        if not new_direct.equals(curr_direct):
            logging.info("For type %s, new_direct = %s, curr_direct = %s"
                         % (type(self).__name__, str(new_direct),
                            str(curr_direct)))
            if new_direct.equals(BUY):
                self.funds -= self.env.asset_price
            else:
                self.funds += self.env.asset_price
            self.calc_profit()

    def calc_profit(self):
        self.profit = self.funds - INIT_ENDOW
        logging.debug("for a = %s, profit (%f) = funds (%f) - INIT_ENDOW (%f)"
                      % (self.name, self.profit, self.funds, INIT_ENDOW))
        self.env.record_profit(self, self.profit)

    def add_env(self, env):
        super().add_env(env)
        if self.stance == BUY:
            self.funds -= self.env.asset_price
            self.calc_profit()

    def to_json(self):
        safe_json = super().to_json()
        safe_json["funds"] = self.funds

        return safe_json

    def from_json_preadd(self, agent_json):
        super().from_json_preadd(agent_json)

        self.funds = agent_json["funds"]


class ChartFollower(FinancialAgent, tp.Follower):
    """
    A trend follower: buys what others are buying.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = ValueInvestor


class ValueInvestor(FinancialAgent, tp.Leader):
    """
    A value investor: buys what others are not buying.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = ChartFollower


class FinMarket(tp.TwoPopEnv):
    """
    A society of value investors and chart followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False,
                props=None):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True, props=props)
        self.total_pop = 0  # to be set once we add agents
        self.asset_price = INIT_PRICE  # an arbitrary starting point
        self.price_hist = []
        self.max_abs_pmove = .5
        self.stances = ["buy", "sell"]
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew asset price",
                                                   self.plot))
        self.follower_profit = 0.0
        self.value_profit = 0.0

    def record_profit(self, agent, profit):
        if isinstance(agent, ChartFollower):
            self.follower_profit += profit
        else:
            self.value_profit += profit

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
        self.user.tell("The chart followers have a net profit of %f."
                       % (self.follower_profit))
        self.user.tell("The value investors have a net profit of %f."
                       % (self.value_profit))
        # these profits are reported anew every exchange, so we have to
        # zero them out after reporting
        self.follower_profit = 0.0
        self.value_profit = 0.0

    def adj_asset_price(self, total_buyers):
        buy_ratio = total_buyers / self.total_pop
        move = self.max_abs_pmove * ((2.0 * buy_ratio) - 1.0)
        if move < 0:  # limit downward moves
            max_move = self.asset_price * .10
            if abs(move) > max_move:
                move = -max_move
        self.asset_price += move

    def plot(self):
        """
        Draw a graph of our changing asset price.
        """
        # put our data in right form for line graph
        data = disp.assemble_lgraph_data("asset price", self.price_hist,
                                         disp.MAGENTA)

        self.line_graph = disp.LineGraph("Asset price history", data,
                                         self.period, is_headless=self.headless())
        self.image_bytes = self.line_graph.show()
        return self.image_bytes

    def to_json(self):
        safe_json = super().to_json()
        safe_json["total_pop"] = self.total_pop
        safe_json["asset_price"] = self.asset_price
        safe_json["price_hist"] = self.price_hist
        safe_json["max_abs_pmove"] = self.max_abs_pmove

        return safe_json

    def from_json(self, json_input):
        super().from_json(json_input)
        self.total_pop = json_input["total_pop"]
        self.asset_price = json_input["asset_price"]
        self.price_hist = json_input["price_hist"]
        self.max_abs_pmove = json_input["max_abs_pmove"]

    def restore_agent(self, agent_json):
        new_agent = None
        if agent_json["ntype"] == ChartFollower.__name__:
            new_agent = ChartFollower(name=agent_json["name"],
                                      goal=agent_json["goal"],
                                      max_move=agent_json["max_move"],
                                      variability=agent_json["variability"])

        elif agent_json["ntype"] == ValueInvestor.__name__:
            new_agent = ValueInvestor(name=agent_json["name"],
                                      goal=agent_json["goal"],
                                      max_move=agent_json["max_move"],
                                      variability=agent_json["variability"])

        else:
            logging.error("agent found whose NTYPE is neither "
                          "{} nor {}, but rather {}".format(ChartFollower.__name__,
                                                            ValueInvestor.__name__,
                                                            agent_json["ntype"]))

        if new_agent:
            self.add_agent_from_json(new_agent, agent_json)
