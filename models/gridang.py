import indra.grid_agent as ga
import indra.grid_env as env
from indra.grid_env import get_angle

class TestGridAgent(ga.GridAgent):
    def preact(self):
        for neighbor in self.neighbor_iter():
            angle = env.get_angle(self, neighbor)
            print("angle: " + angle)

