"""
stance_model.py
Models two classes of agents: one tries to follow the other,
the other tries to avoid the first.
"""
# import numpy as np
# import logging
import operator as op
import indra.display_methods as disp
import indra.menu as menu
import indra.grid_env as ge
import indra.grid_agent as ga
import indra.prehension as pre


INIT_FLWR = pre.X_VEC
INIT_LEDR = pre.Y_VEC

STANCE_TRACKED = INIT_FLWR


class TwoPopAgent(ga.GridAgent):
    """
    An agent taking a stance depending on others' stance.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move, max_detect=max_move)
        self.stance = pre.Prehension()
        self.adv_periods = 0
        self.other = None
        self.comp = None

    def survey_env(self):
        """
        Look around and see what stances surround us.
        """
        def my_filter(n): return isinstance(n, self.other)

        super().survey_env()
        other_pre = pre.Prehension()
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=my_filter):
            other_pre = other.stance.prehend(other_pre)
        return other_pre

    def eval_env(self, other_pre):
        """
        See how we respond to the stance scene.
        """
        self.stance = self.stance.prehend(other_pre)

    def postact(self):
        """
        After we are done acting, move to an empty cell.
        """
        self.move_to_empty(grid_view=self.my_view)


class Follower(TwoPopAgent):
    """
    A trend follower: tries to switch to value investor' stance.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.comp = op.gt
        self.other = Leader
        self.stance = INIT_FLWR


class Leader(TwoPopAgent):
    """
    A value investor: tries to buy assets out of favor
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.comp = op.lt
        self.other = Follower
        self.stance = INIT_LEDR


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
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew populations",
                                                   self.view_pop))

    def census(self, disp=True):
        """
        Take a census of our pops.
        Return the total adopting STANCE_TRACKED.
        """
        total_w_stance = 0
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       self.stances[STANCE_TRACKED] + ":")
        for var in self.varieties_iter():
            pop = self.get_pop_data(var)
            total_w_stance += pop
            self.user.tell(var + ": " + str(pop))
            self.append_pop_hist(var, pop)
        return total_w_stance

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
                                         data, period)

    def add_agent(self, agent):
        """
        Add a new financial agent to the env.
        """
        super().add_agent(agent)
        var = agent.get_type()
        if agent.stance == STANCE_TRACKED:
            self.change_pop_data(var, 1)

    def record_stance_change(self, agent):
        """
        Track the stances in our env.
        """
        var = agent.get_type()
        if agent.stance == STANCE_TRACKED:
            self.change_pop_data(var, 1)
        else:
            self.change_pop_data(var, -1)
