import indra.grid_agent as ga
import indra.grid_env as env

class TestGridAgent(ga.GridAgent):
    def act(self):
        for neighbor in self.neighbor_iter():
            angle = env.get_angle(self, neighbor)
            print("angle: " + angle)
            

    
