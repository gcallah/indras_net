"""
two_pop_model.py
Models two classes of agents: one tries to follow the other,
the other tries to avoid the first.
"""

# pylint: disable=E731

import logging
import indra.display_methods as disp
import indra.menu as menu
import indra.grid_env as ge
import indra.vs_agent as va
import indra.vector_space as vs

# We represent one stance by a vector pointing along the x-axis, the other
#  by one pointing along the y-axis:
INIT_FLWR = vs.VectorSpace.X_PRE
INIT_LEDR = vs.VectorSpace.Y_PRE

STANCE_TRACKED = INIT_FLWR
STANCE_TINDEX = 0  # the index of the tracked stance in an array of stances


class TwoPopAgent(va.VSAgent):
    """
    An agent taking a stance depending on others' stance.
    variability: controls how self-directed the agent is. The higher the
        variability, the more the agent is influenced by others.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, max_detect=max_move)

        self.my_filter = lambda n: isinstance(n, self.other)

        self.new_stance = vs.VectorSpace()
        self.other = None
        self.variability = variability

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
        return self.stance.direction()


class Follower(TwoPopAgent):
    """
    A trend follower: tries to switch to leader's stance
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = Leader
        self.stance = INIT_FLWR

    def eval_env(self, other_pre):
        """
        See how we respond to the stance scene.
        """
        self.new_stance = self.stance.prehend(
            other_pre.intensify(self.variability))
        return self.new_stance


class Leader(TwoPopAgent):
    """
    A leader: avoids follower's stance.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = Follower
        self.stance = INIT_LEDR

    def eval_env(self, other_pre):
        """
        See how we respond to the stance scene.
        For a leader, we reverse what the followers are doing.
        """
        self.new_stance = self.stance.prehend(other_pre.reverse())
        return self.new_stance


class TwoPopEnv(ge.GridEnv):
    """
    A society of leaders and followers.
    Most of the code here is bookkeeping: setting up a census,
        adding menu items, drawing a graph.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False,
                 postact=True, props=None):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=postact, props=props)
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
                                            self.stances[STANCE_TINDEX]),
                                         data, period)
