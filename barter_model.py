"""
barter_model.py
An barter market model where several agents trade goods.
"""
import logging
import csv
import entity
import spatial_agent
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
        super().__init__(name, goal=goal, max_detect=max_detect)


    def act(self):
        super().act()


class BarterEnv(ebm.EdgeboxEnv):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__(name, length, height,
                        model_nm=model_nm)


    def fetch_agents_from_file(self, filenm):
        max_detect = self.props.get("max_detect",
                                ebm.GLOBAL_KNOWLEDGE)
        print("max detect = " + str(max_detect))
        with open(filenm) as f:
            reader = csv.reader(f)
            for row in reader:
                agent = BarterAgent(row[0], max_detect=max_detect)
                self.add_agent(agent)
                for i in range(1, len(row) - 2, STEP):
                    agent.endow(row[i], 
                                int(row[i + 1]),
                                eval("lambda qty: "
                                    + row[i + 2]))

