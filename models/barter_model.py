"""
barter_model.py
An barter market model where several agents trade goods.
"""
import logging
import csv
import networkx as nx
import indra.menu as menu
import indra.entity as ent
import indra.display_methods as disp
import edgebox_model as ebm

TRADE = "trade"

STEP = 3


class BarterAgent(ebm.EdgeboxAgent):
    """
    Agents who attempt to trade goods to achieve greater utility.
    """

    def __init__(self, name, goal=TRADE,
                 max_detect=ebm.GLOBAL_KNOWLEDGE):
        """
        A call to our super's init.
        """
        super().__init__(name, goal=goal, max_detect=max_detect)

    def act(self):
        """
        Just call our super's act!
        """
        super().act()

    def postact(self):
        """
        Move to a random cell.
        """
        self.move_to_empty()

    def trade(self, my_good, my_amt, counterparty, his_good, his_amt):
        """
        Call our super's trade and then record
        this trade in the market.
        """
        super().trade(my_good, my_amt, counterparty, his_good, his_amt)
        self.env.traded(my_good, his_good)


class Market(ent.Entity):
    """
    A marketplace with goods and providers.
    """

    def __init__(self, name):
        super().__init__(name)
        self.goods = {}
        self.graph = nx.Graph()

    def goods_iter(self):
        """
        Return the goods in self.goods.
        """
        return self.goods.keys()

    def add_good(self, good):
        """
        Add a good to the market.
        """
        if good not in self.goods:
            self.goods[good] = {}
            self.goods[good]["vendors"] = []
            self.goods[good]["trades"] = 0
            self.goods[good]["trade_hist"] = []
            self.graph.add_edge(self, good)

    def add_vendor(self, good, vendor):
        """
        Add an agent who can supply this good.
        """
        self.add_good(good)
        self.goods[good]["vendors"].append(vendor)
        self.graph.add_edge(good, vendor)

    def has_vendor(self, good):
        """
        Does this good have any vendors?
        """
        return len(self.goods[good]["vendors"]) > 0

    def traded(self, g1, g2):
        """
        Record trades for each good: since every
        trade has two sides, record both with one call.
        """
        good1 = self.goods[g1]
        good2 = self.goods[g2]
        good1["trades"] += 1
        good2["trades"] += 1

    def set_trade_hist(self):
        for g in self.goods_iter():
            good = self.goods[g]
            good["trade_hist"].append(good["trades"])

    def get_trades(self, good):
        return self.goods[good]["trades"]

    def get_trade_hist(self):
        """
        Make a list containing the population history
        for each var in vars.
        """
        trade_hist = {}
        for good in self.goods_iter():
            trade_hist[good] = {}
            trade_hist[good]["data"] = self.goods[good]["trade_hist"]
        return trade_hist


class BarterEnv(ebm.EdgeboxEnv):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None,
                 preact=False, postact=True):
        super().__init__(name, length, height,
                         model_nm=model_nm, preact=preact,
                         postact=postact)
        self.market = Market("agora")
        self.graph.add_edge(self, self.market)
        self.menu.graph.add_menu_item("m",
                                      menu.MenuLeaf("(m)arket",
                                                    self.graph_market))

    def step(self):
        super().step()
        self.market.set_trade_hist()

    def traded(self, good1, good2):
        """
        Record that these goods have been traded.
        """
        self.market.traded(good1, good2)

    def graph_market(self):
        """
        Graphs market relationships
        """
        self.market.draw()

    def fetch_agents_from_file(self, filenm, agent_type):
        """
        Read in a list of bartering agents from a csv file
        """

        max_detect = self.props.get("max_detect",
                                    ebm.GLOBAL_KNOWLEDGE)
        with open(filenm) as f:
            reader = csv.reader(f)
            for row in reader:
                agent = agent_type(row[0], max_detect=max_detect)
                self.add_agent(agent)
                for i in range(1, len(row) - 2, STEP):
                    good = row[i]
                    self.market.add_good(good)
                    agent.endow(good,
                                int(row[i + 1]),
                                eval("lambda qty: "
                                     + row[i + 2]))
        logging.info("Goods = " + str(self.market))

    def display(self):
        """
        Draw a graph of trades per good.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        trade_hist = self.market.get_trade_hist()

        disp.display_line_graph("Carl Menger's money model: "
                                + "Trades per good ",
                                trade_hist,
                                self.period)
