"""
edgebox_model.py
An Edgeworth Box model where two agents trade goods.
"""
import spatial_agent

TRADE = "trade"


class EdgeboxAgent(spatial_agent.SpatialAgent):
    """
    Agents who attempt to trade goods to achieve greater utility
    """

    def __init__(self, name, goal=TRADE):
        super().__init__(name, goal, max_detect=1000.0)


    def act(self):
        potential_traders = self.survey_env(TRADE)        
        for t in potential_traders:
            print("Potential trader for " + self.name + ": " + t.name)


class EdgeboxEnv(spatial_agent.SpatialEnvironment):
    """
    Contains goods and agents who exchange them.
    """

    def __init__(self, length, height, model_nm=None):
        super().__init__("An Edgeworth Box", length, height, model_nm=model_nm)
        self.census = False


    def step(self, delay=0):
        super().step(delay=delay)

