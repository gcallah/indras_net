"""
forestfire_model.py
Adapted from the George Mason mesa project.
This model shows the spread of a forest fire through a forest.
"""

import indra.grid_agent as ga
import indra.grid_env as grid


X = 0
Y = 1

HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"


class Tree(ga.GridAgent):
    '''
    A tree cell.

    Attributes:
        condition: Can be "Fine", "On Fire", or "Burned Out"

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    '''
    def __init__(self, name):
        '''
        Create a new tree.
        '''
        super().__init__(name, "burn")
        self.ntype = HEALTHY
        self.next_state = None

    def is_healthy(self):
        return self.ntype == HEALTHY

    def is_burning(self):
        return self.ntype == ON_FIRE

    def is_burnt(self):
        return self.ntype == BURNED_OUT

    def set_type(self, new_type):
        """
        Set tree's new type.
        """
        old_type = self.ntype
        self.ntype = new_type
        self.env.change_agent_type(self, old_type, new_type)

    def act(self):
        '''
        If the tree is on fire, spread it to healthy trees nearby.
        '''
        if self.is_burning():
            (x, y) = self.pos
            for neighbor in self.env.neighbor_iter(x, y):
                if neighbor.is_healthy():
                    neighbor.next_state = ON_FIRE
            self.set_type(BURNED_OUT)

    def postact(self):
        if self.next_state is not None:
            self.set_type(self.next_state)
            self.next_state = None

        return self.pos


class ForestEnv(grid.GridEnv):
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, height, width, density, torus=False,
                 model_nm="ForestFire", postact=True):
        '''
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        super().__init__("Forest Fire", height, width, torus=False,
                         model_nm=model_nm, postact=postact)
        self.density = density
        self.plot_title = "A Forest Fire"

        # setting our colors adds varieties as well!
        self.agents.set_var_color(BURNED_OUT, 'k')
        self.agents.set_var_color(ON_FIRE, 'r')
        self.agents.set_var_color(HEALTHY, 'g')

    def add_agent(self, tree):
        super().add_agent(tree)
        (x, y) = tree.pos
        if x == 0:
            tree.set_type(ON_FIRE)

    def step(self):
        super().step()
        # Halt if no more fire
        if self.get_pop(ON_FIRE) == 0:
            return "The fire is out!"
