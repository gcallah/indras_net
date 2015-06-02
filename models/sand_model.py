"""
sand_model.py
Abelian sand that has avalanches in interesting patterns.
"""
from math import floor
import indra.display_methods as disp
import indra.grid_agent as ga
import indra.grid_env as ge

X = 0
Y = 1

MAX_SAND = 4
FULL_NEIGHBORHOOD = 4


class SandAgent(ga.GridAgent):
    """
    An agent that collects sand particles until its stack collapses
    onto its neighbors.
    """
    def __init__(self, name, goal, cell):
        super().__init__(name, goal)
        self.cell = cell
        self.sand_amt = 0
        self.ntype = str(self.sand_amt)  # we get our color from our sand amount

    def act(self):
        """
        Our main action goes here, in this case,
        tumbling sand onto our neighbors.
        """
        if self.sand_amt >= MAX_SAND:
            (x, y) = self.pos
            i = 0
            for neighbor in self.neighbor_iter(moore=False):
                i += 1
                if self.sand_amt > 0:
                    neighbor.add_grains(1)
                    self.sand_amt -= 1
            if i < FULL_NEIGHBORHOOD:
                for j in range(i, FULL_NEIGHBORHOOD):
                    """
                    If at edge, sand tumbles off.
                    """
                    self.sand_amt -= 1

    def postact(self):
        """
        Here we are going to set our type.
        """
        new_type = str(self.sand_amt)
        if self.ntype != new_type:
            old_type = self.ntype
            self.set_type(new_type)
            self.env.change_agent_type(self, old_type, new_type)

    def add_grains(self, amt):
        """
        Get some sand.
        """
        self.sand_amt += amt


class SandEnv(ge.GridEnv):
    """
    An environment for spilling sand all over the place.
    """

    def __init__(self, name, height, width, model_nm=None):
        super().__init__(name, height, width, torus=False,
                         model_nm=model_nm, postact=True)

        self.center_agent = None
        self.agents.set_var_color('0', disp.BLACK)
        self.agents.set_var_color('1', disp.MAGENTA)
        self.agents.set_var_color('2', disp.BLUE)
        self.agents.set_var_color('3', disp.CYAN)
        self.agents.set_var_color('4', disp.GREEN)
        self.agents.set_var_color('5', disp.YELLOW)
        self.agents.set_var_color('6', disp.RED)
        center_x = floor(self.width / 2)
        center_y = floor(self.height / 2)
        print("center = %i, %i" % (center_x, center_y))

        for cell in self:
            (x, y) = cell.coords
            agent = SandAgent("Grainy", "Hold sand", cell)
            self.add_agent(agent, position=False)
            if x == center_x and y == center_y:
                self.center_agent = agent
                # (x1, y1) = self.center_agent.pos
                # print("Center agent is at: %i, %i" % (x1, y1))

    def step(self):
        super().step()
        self.center_agent.add_grains(1)
        # (x, y) = self.center_agent.pos
        # print("Center agent is at: %i, %i" % (x, y))
