"""
forestfire_model.py
Adapted from the George Mason mesa project.
This model shows the spread of a forest fire through a forest.
"""

import indra.display_methods as disp
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
        condition: Can be "Healthy", "On Fire", or "Burned Out"

    '''
    def __init__(self, name):
        '''
        Create a new tree.
        '''
        super().__init__(name, "burn")
        self.ntype = HEALTHY
        self.next_state = None
        self.dead_periods = 0

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
        If a neighbor is on fire, this tree catches on fire.
        If this tree is on fire, set its next state to BURNED_OUT.
        '''
        if self.is_burning():
            self.next_state = BURNED_OUT
        elif self.is_healthy():
            # at some point, we may want to try bigger neighborhoods
            # than size 1
            for neighbor in self.neighbor_iter():
                if neighbor.is_burning():
                    self.next_state = ON_FIRE
                    break
        elif self.is_burnt:
            self.dead_periods += 1
            if self.dead_periods >= self.env.regen_period:
                self.next_state = HEALTHY
                self.dead_periods = 0

    def postact(self):
        """
        Set our type to next_state.
        """
        if self.next_state is not None:
            self.set_type(self.next_state)
            self.next_state = None

        return self.pos


class ForestEnv(grid.GridEnv):
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, height, width, density, strike_freq, regen_period,
                 torus=False, model_nm="ForestFire", postact=True):
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
        self.strike_freq = strike_freq
        self.regen_period = regen_period
        self.plot_title = "A Forest Fire"

        # setting our colors adds varieties as well!
        self.agents.set_var_color(BURNED_OUT, disp.BLACK)
        self.agents.set_var_color(ON_FIRE, disp.RED)
        self.agents.set_var_color(HEALTHY, disp.GREEN)

    def step(self):
        """
        We strike a tree with lightning every self.strike_freq
        turns.
        """
        if self.period % self.strike_freq == 0:
            target = self.get_randagent_of_var(HEALTHY)
            if target is not None:
                target.set_type(ON_FIRE)
        super().step()
