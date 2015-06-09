"""
wolfsheep_model.py
Wolves and sheep roaming a meadow, with wolves eating sheep
that get near them.
"""
import logging
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
    A creature: moves around randomly.
    Reproduction to be added.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal)
        self.max_move = max_move
        self.fashion = None

    def act(self):
        move_view = self.get_square_view(self.max_move)
        self.env.move_to_empty(self, grid_view=move_view)

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


class Follower(Fashionista):
    """
    A fashion follower: tries to switch to hipsters' fashions.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_FLWR

    def act(self):
        super().act()
        has_my_fashion = 0
        not_my_fashion = 0
        for hipster in filter(lambda a: isinstance(a, Hipster),
                              self.neighbor_iter()):
            if hipster.fashion == self.fashion:
                has_my_fashion += 1
            else:
                not_my_fashion += 1
        if not_my_fashion > has_my_fashion:
            self.change_fashion()


class Hipster(Fashionista):
    """
    A fashion hipster: tries to not look like followers.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_HPST

    def act(self):
        super().act()
        has_my_fashion = 0
        not_my_fashion = 0
        for follower in filter(lambda a: isinstance(a, Follower),
                               self.neighbor_iter()):
            if follower.fashion == self.fashion:
                has_my_fashion += 1
            else:
                not_my_fashion += 1
        if not_my_fashion < has_my_fashion:
            self.change_fashion()


class Society(ge.GridEnv):
    """
    A society of hipsters and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False):
        super().__init__(name, length, height, model_nm=model_nm, torus=False)
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
