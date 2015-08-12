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

# tree conditions: NEW_GROWTH and HEALTHY both return True
#  when tested with is_healthy()
NEW_GROWTH = "New Growth"
HEALTHY = "Healthy"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"


class Tree(ga.GridAgent):
    '''
    A tree cell.

    Attributes:
        condition: Can be "New Growth", "Healthy", "On Fire", or "Burned Out"

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
        return self.ntype == HEALTHY or self.ntype == NEW_GROWTH

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
        If this tree is HEALTHY and a neighbor is on fire,
         this tree catches on fire.
        If this tree is on fire, set its next state to BURNED_OUT.
        If the tree is burned out, after regen_period it grows back.
        '''
        if self.is_burning():
            self.next_state = BURNED_OUT
        elif self.is_healthy():
            self.next_state = self.survey_env()
        elif self.is_burnt:
            self.dead_periods += 1
            if self.dead_periods >= self.env.regen_period:
                self.next_state = NEW_GROWTH
                self.dead_periods = 0

    def survey_env(self, this_view=None):
        """
        Look around and see what our env holds for us.
        We will want to try views > 1 in the future.
        We set save_hood=True, because the trees don't move,
        so no need to keep fetching their neighborhood.
        """
        for neighbor in self.neighbor_iter(save_hood=True):
            if neighbor.is_burning():
                return ON_FIRE
        return HEALTHY

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
    def __init__(self, width, height, density, strike_freq, regen_period,
                 torus=False, model_nm="ForestFire", postact=True):
        '''
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        super().__init__("Forest Fire", width, height, torus=False,
                         model_nm=model_nm, postact=postact)
        self.density = density
        self.strike_freq = strike_freq
        self.regen_period = regen_period
        self.plot_title = "A Forest Fire"

        # setting our colors adds varieties as well!
        self.set_var_color(BURNED_OUT, disp.BLACK)
        self.set_var_color(ON_FIRE, disp.RED)
        self.set_var_color(HEALTHY, disp.GREEN)
        self.set_var_color(NEW_GROWTH, disp.CYAN)

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
