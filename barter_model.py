"""
barter_model.py
An barter market model where several agents trade goods.
"""
import logging
import csv
import networkx as nx
import entity as ent
import edgebox_model as ebm

TRADE = "trade"

STEP = 3


def util_func(qty):
    """
    A default util func: we can pass in others
    """
    return 10 - .5 * qty


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


class Market(ent.Entity):
    """
    A marketplace with goods and providers.
    """

    def __init__(self, name):
        super().__init__(name)
        self.goods = {}
        self.graph = nx.Graph()


    def keys(self): 
        """
        Return the goods in self.goods.
        """
        return self.goods.keys()


    def add_good(self, good):
        """
        Add a good to the market.
        """
        if good not in self.goods:
            self.goods[good] = []
            self.graph.add_edge(self, good)


    def add_vendor(self, good, vendor):
        """
        Add an agent who can supply this good.
        """
        self.add_good(good)
        self.goods[good].append(vendor)
        self.graph.add_edge(good, vendor)


class BarterEnv(ebm.EdgeboxEnv):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None,
                 preact=False):
        super().__init__(name, length, height,
                         model_nm=model_nm, preact=preact)
        self.market = Market("agora")
        self.graph.add_edge(self, self.market)
        self.menu.graph.add_menu_item("m", 
                                      ent.MenuLeaf("(m)arket",
                                      self.graph_market))


    def graph_market(self):
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
        print("Goods = " + str(self.market))


    def draw_graph(self):
        """
        Draw a graph!
        """
        choice = self.user.ask_for_ltr("Draw graph for "
                                       + "(a)gents; (e)nvironment; "
                                       + "(m)arket; (u)niversals?")
        if choice == "a":
            self.agents.draw()
        elif choice == "m":
            self.market.draw()
        elif choice == "u":
            node.universals.draw()
        else:
            self.draw()

