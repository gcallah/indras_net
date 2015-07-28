"""
stance_model.py
Models two classes of agents: one tries to follow the other,
the other tries to avoid the first.
"""
import logging
import operator as op
import indra.display_methods as disp
import indra.menu as menu
import indra.grid_env as ge
import indra.grid_agent as ga


YES = 0
NO = 1
INIT_FLWR = YES
INIT_LDR = NO

STANCE_TRACKED = YES


class StanceAgent(ga.GridAgent):
    """
    An agent trading financial assets.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move, max_detect=max_move)
        self.stance = None
        self.adv_periods = 0
        self.other = None
        self.comp = None

    def act(self):
        """
        Try to adjust our stance to our neighbor's
        """
        super().act()
        (has_my_stance, not_my_stance) = self.survey_env(self.my_view)
        self.evaluate_env(has_my_stance, not_my_stance)

    def evaluate_env(self, has_my_stance, not_my_stance):
        """
        See how we like the stance scene.
        """
        if self.comp(not_my_stance, has_my_stance):
            self.respond_to_cond()

    def survey_env(self, this_view):
        """
        Look around and see what stances surround us.
        """
        def my_filter(n): return isinstance(n, self.other)

        has_my_stance = 0
        not_my_stance = 0
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=my_filter):
            if other.stance == self.stance:
                has_my_stance += 1
            else:
                not_my_stance += 1

        return (has_my_stance, not_my_stance)

    def respond_to_cond(self):
        """
        What an agent does when he doesn't like the trend.
        """
        self.adv_periods += 1
        if self.adv_periods >= self.env.min_adv_periods:
            self.change_stance()
            self.adv_periods = 0

    def change_stance(self):
        """
        Switch my fashion.
        """
        if self.stance == NO:
            self.stance = YES
        else:
            self.stance = NO
        self.env.record_stance_change(self)
        logging.info(self.name + " is changing stance")

    def postact(self):
        """
        After we are done acting, move to an empty cell.
        """
        self.move_to_empty(grid_view=self.my_view)


class Follower(StanceAgent):
    """
    A trend follower: tries to switch to value investor' stance.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.comp = op.gt
        self.other = Leader
        self.stance = INIT_FLWR


class Leader(StanceAgent):
    """
    A value investor: tries to buy assets out of favor
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.comp = op.lt
        self.other = Follower
        self.stance = INIT_LDR


class StanceEnv(ge.GridEnv):
    """
    A society of leaders and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False,
                 postact=True):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=postact)
        # sub-models will override these vague names with something
        # meaningful in those models
        self.stances = ["yes", "no"]
        self.line_graph_title = "StanceAgents in %s adopting stance %s"
        self.min_adv_periods = self.props.get("min_adv_periods",
                                              default=6)
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew populations",
                                                   self.view_pop))

    def census(self, disp=True):
        """
        Take a census of our pops.
        """
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       self.stances[STANCE_TRACKED] + ":")
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
        self.line_graph = disp.LineGraph(self.line_graph_title
                                         % (self.name,
                                            self.stances[STANCE_TRACKED]),
                                         data, period, anim=False,
                                         data_func=self.line_data)

    def add_agent(self, agent):
        """
        Add a new financial agent to the env.
        """
        super().add_agent(agent)
        var = agent.get_type()
        if agent.stance == STANCE_TRACKED:
            self.agents.change_pop_data(var, 1)

    def record_stance_change(self, agent):
        """
        Track the stances in our env.
        """
        var = agent.get_type()
        if agent.stance == STANCE_TRACKED:
            self.agents.change_pop_data(var, 1)
        else:
            self.agents.change_pop_data(var, -1)
