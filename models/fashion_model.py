"""
fashion_model.py
A fashion model that includes followers and hipsters
changing fashions based on each other's choices.
"""
import logging
import operator as op
import indra.display_methods as disp
import indra.menu as menu
import indra.grid_env as ge
import indra.grid_agent as ga

fashions = ["blue", "red"]

BLUE = 0
RED = 1
INIT_FLWR = BLUE
INIT_HPST = RED

FSHN_TO_TRACK = BLUE


class Fashionista(ga.GridAgent):
    """
    An agent concerned with fashion.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move, max_detect=max_move)
        self.fashion = None
        self.adv_periods = 0
        self.other = None
        self.comp = None

    def act(self):
        """
        Try to adjust our fashion to our neighbor's
        """
        super().act()
        (has_my_fashion, not_my_fashion) = self.survey_env(self.my_view)
        self.evaluate_env(has_my_fashion, not_my_fashion)

    def evaluate_env(self, has_my_fashion, not_my_fashion):
        """
        See how we like the fashion scene.
        """
        if self.comp(not_my_fashion, has_my_fashion):
            self.respond_to_cond()

    def survey_env(self, this_view):
        """
        Look around and see what fashions surround us.
        """
        def my_filter(n): return isinstance(n, self.other)

        has_my_fashion = 0
        not_my_fashion = 0
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=my_filter):
            if other.fashion == self.fashion:
                has_my_fashion += 1
            else:
                not_my_fashion += 1

        return (has_my_fashion, not_my_fashion)

    def respond_to_cond(self):
        """
        What an agent does when he doesn't like the trend.
        """
        self.adv_periods += 1
        if self.adv_periods >= self.env.min_adv_periods:
            self.change_fashion()
            self.adv_periods = 0

    def change_fashion(self):
        """
        Switch my fashion.
        """
        if self.fashion == RED:
            self.fashion = BLUE
        else:
            self.fashion = RED
        self.env.record_fashion_change(self)
        logging.info(self.name + " is changing fashions")

    def postact(self):
        """
        After we are done acting, move to an empty cell.
        """
        self.move_to_empty(grid_view=self.my_view)


class Follower(Fashionista):
    """
    A fashion follower: tries to switch to hipsters' fashions.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_FLWR
        self.other = Hipster
        self.comp = op.gt


class Hipster(Fashionista):
    """
    A fashion hipster: tries to not look like followers.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_HPST
        self.other = Follower
        self.comp = op.lt


class Society(ge.GridEnv):
    """
    A society of hipsters and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True)
        self.agents.set_var_color('Hipster', disp.GREEN)
        self.agents.set_var_color('Follower', disp.MAGENTA)
        self.min_adv_periods = self.props.get("min_adv_periods",
                                              default=6)
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew fashions",
                                                   self.view_pop))

    def add_agent(self, agent):
        """
        Add a new fashion agent to the env.
        """
        super().add_agent(agent)
        var = agent.get_type()
        if agent.fashion == FSHN_TO_TRACK:
            self.agents.change_pop_data(var, 1)

    def record_fashion_change(self, agent):
        """
        Track the fashions in our env.
        """
        var = agent.get_type()
        if agent.fashion == FSHN_TO_TRACK:
            self.agents.change_pop_data(var, 1)
        else:
            self.agents.change_pop_data(var, -1)

    def census(self, disp=True):
        """
        Take a census of our pops.
        """
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       fashions[FSHN_TO_TRACK] + ":")
        for var in self.agents.varieties_iter():
            pop = self.agents.get_pop_data(var)
            self.user.tell(var + ": " + str(pop))
            self.agents.append_pop_hist(var, pop)

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
                                         % (self.name, fashions[FSHN_TO_TRACK]),
                                         data, period, anim=False,
                                         data_func=self.line_data)
