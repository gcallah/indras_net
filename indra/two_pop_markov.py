"""
two_pop_model.py
Models two classes of agents: one tries to follow the other,
the other tries to avoid the first.
"""

# pylint: disable=E731

import logging
import indra.display_methods as disp
import indra.menu as menu
import indra.markov as m
import indra.markov_agent as ma
import indra.markov_env as menv

# We represent one stance by a vector pointing along the x-axis, the other
#  by one pointing along the y-axis:
X = 0
Y = 1

# STANCE_TRACKED = INIT_FLWR
# STANCE_TINDEX = 0  # the index of the tracked stance in an array of stances


class TwoPopAgent(ma.MarkovAgent):
    """
    An agent taking a stance depending on others' stance.
    variability: controls how self-directed the agent is. The higher the
        variability, the more the agent is influenced by others.
    """
    def __init__(self, name, goal, vlen=2, init_state=0):
        super().__init__(name, goal, vlen, init_state)

    def respond_to_cond(self, env_vars=None):
        """
        Over-riding our parent method to do nothing.
        """
        pass

    def postact(self):
        """
        After we are done acting, adopt our new stance.
        If the stance changes our direction, we adopt the extreme
        of the new direction.
        Then move to an empty cell.
        """
        self.state = self.next_state

        """
        new_direct = self.new_stance.direction()
        curr_direct = self.stance.direction()
        logging.info("For %s: stance = %s, new stance = %s"
                     % (self.name, str(self.stance), str(self.new_stance)))
        if not new_direct.equals(curr_direct):
            self.direction_changed(curr_direct, new_direct)
            # if adopting a new stance direction, we go to the extreme
            self.new_stance = new_direct
        else:
            self.new_stance = self.new_stance.normalize()
        self.stance = self.new_stance
        self.move_to_empty(grid_view=self.my_view)
        """
        pass

    def direction_changed(self, curr_direct, new_direct):
        """
        Some models may need to do something when the direction of an
        agent changes. But in the base class, we don't.
        """
        pass

    def public_stance(self):
        """
        My stance as seen from outside. Filters out internal conflict.
        """
        # return self.stance.direction()
        pass


class Follower(TwoPopAgent):
    """
    A trend follower: tries to switch to leader's stance
    """
    def __init__(self, name, goal, vlen=2, init_state=0):
        super().__init__(name, goal, vlen=2, init_state=0)



class Leader(TwoPopAgent):
    """
    A leader: avoids follower's stance.
    """
    def __init__(self, name, goal, vlen=2, init_state=1):
        super().__init__(name, goal, vlen=2, init_state=1)


class TwoPopEnv(menv.MarkovEnv):
    """
    A society of leaders and followers.
    Most of the code here is bookkeeping: setting up a census,
        adding menu items, drawing a graph.
    """
    def __init__(self, name, width, height, preact, postact,
                trans_str=None, model_nm=None, torus=False):

        super().__init__(name, width, height, trans_str=trans_str, torus=False,
                        matrix_dim=2, model_nm=None, preact=preact, postact=postact)

        # sub-models will override these vague names with something
        # meaningful in those models
        # self.state = [X: "sO", Y: "s1"]
        self.line_graph_title = "StanceAgents in %s adopting stance %s"
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew populations",
                                                   self.view_pop))

    def census(self, disp=True):
        """
        Take a census of our pops.
        Return the total adopting STANCE_TRACKED.
        """

        """
        total_w_stance = 0
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       self.stances[STANCE_TINDEX] + ":")
        for var in self.varieties_iter():
            pop = 0
            for agent in self.get_agents_of_var(var):
                if agent.public_stance().equals(STANCE_TRACKED):
                    pop += 1
            total_w_stance += pop
            self.user.tell(var + ": " + str(pop))
            self.append_pop_hist(var, pop)
        return total_w_stance
        """
        pass

    def view_pop(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
        #    return

        # (period, data) = self.line_data()
        #self.line_graph = disp.LineGraph(self.line_graph_title
        #                                 % (self.name,
        #                                    self.stances[STANCE_TINDEX]),
        #                                 data, period)
