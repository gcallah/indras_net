"""
fashion_model.py
A fashion model that includes followers and hipsters
changing fashions based on each other's choices.
"""
# import logging
import indra.display_methods as disp
import indra.menu as menu
import stance_model as sm

stances = ["blue", "red"]

BLUE = 0
RED = 1
INIT_FLWR = BLUE
INIT_LDR = RED

STANCE_TRACKED = BLUE


class Follower(sm.Follower):
    """
    A fashion follower: tries to switch to hipsters' fashions.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = Hipster


class Hipster(sm.Leader):
    """
    A fashion hipster: tries to not look like followers.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.other = Follower


class Society(sm.StanceEnv):
    """
    A society of hipsters and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True)
        self.agents.set_var_color('Hipster', disp.GREEN)
        self.agents.set_var_color('Follower', disp.MAGENTA)
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew fashions",
                                                   self.view_pop))

    def view_pop(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        (period, data) = self.line_data()
        self.line_graph = disp.LineGraph("A. Smith's fashion model: Populations"
                                         + " in %s adopting fashion %s"
                                         % (self.name, stances[STANCE_TRACKED]),
                                         data, period, anim=False,
                                         data_func=self.line_data)
