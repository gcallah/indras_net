"""
forestfire_model.py
Adapted from the George Mason mesa project.
This model shows the spread of a forest fire through a forest.
"""

import random

import indra.spatial_agent as sa
import indra.grid_env as grid


X = 0
Y = 1

HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"


class Tree(sa.SpatialAgent):
    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    '''
    def __init__(self, x, y):
        '''
        Create a new tree.
        Args:
            x, y: The tree's coordinates on the grid.
        '''
        name = "Tree at %i %i" % (x, y)
        super().__init__(name, "burn")
        self.pos = (x, y)
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
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if self.is_burning():
            for neighbor in self.env.neighbor_iter(self.pos[X], self.pos[Y]):
                if neighbor.is_healthy():
                    #  print("Setting next state to ON_FIRE")
                    neighbor.next_state = ON_FIRE
#                    neighbor.set_type(ON_FIRE)
            self.set_type(BURNED_OUT)

    def postact(self):
        if self.next_state is not None:
            print("Setting type to: " + self.next_state)
            self.set_type(self.next_state)
            self.next_state = None

    def get_pos(self):
        return self.pos


class ForestEnv(grid.GridEnv):
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, height, width, density, model_nm="ForestFire",
                 postact=True):
        '''
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        super().__init__("Forest Fire", height, width, model_nm=model_nm,
                         postact=postact)
        self.density = density

        # Place a tree in each cell with Prob = density
        for cell in self.coord_iter():
            x = cell[1]
            y = cell[2]
            if random.random() < self.density:
                # Create a tree
                new_tree = Tree(x, y)
                self.add_agent(new_tree)
                self.position_agent(new_tree, x, y)
                if x == 0:
                    # all trees in col 0 start on fire
                    new_tree.set_type(ON_FIRE)
        # since we start with no burned out agents, let's add the var:
        self.agents.add_variety(BURNED_OUT)
        self.agents.set_var_color(BURNED_OUT, 'k')
        self.agents.set_var_color(ON_FIRE, 'r')
        self.agents.set_var_color(HEALTHY, 'g')

    def step(self):
        super().step()
        # Halt if no more fire
        if self.get_pop(ON_FIRE) == 0:
            return "The fire is out!"
