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
            i = 0
            for neighbor in self.neighbor_iter(moore=False, save_hood=True):
                i += 1
                if self.sand_amt > 0:
                    neighbor.add_grains(1)
                    self.sand_amt -= 1
            if self.sand_amt > 0 and i < FULL_NEIGHBORHOOD:
                for j in range(i, FULL_NEIGHBORHOOD):
                    """
                    If at edge, sand "tumbles off."
                    """
                    if self.sand_amt > 0:
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

    def __init__(self, name, width, height, model_nm=None, props=None):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, postact=True, props=props)

        self.center_agent = None
        self.set_var_color('0', disp.BLACK)
        self.set_var_color('1', disp.MAGENTA)
        self.set_var_color('2', disp.BLUE)
        self.set_var_color('3', disp.CYAN)
        self.set_var_color('4', disp.RED)
        self.set_var_color('5', disp.YELLOW)
        self.set_var_color('6', disp.GREEN)
        center_x = floor(self.width // 2)
        center_y = floor(self.height // 2)
        print("center = %i, %i" % (center_x, center_y))

        for cell in self:
            (x, y) = cell.coords
            agent = SandAgent("Grainy", "Hold sand", cell)
            self.add_agent(agent, position=False)
            if x == center_x and y == center_y:
                self.center_agent = agent

    def step(self):
        super().step()
        self.center_agent.add_grains(1)
