
"""
Filename: fashion_model.py
Author: Gene Callahan
Implements Adam Smith's fashion model of
trend-setters and followers.
"""

import logging
import indra.node as node
import indra.menu as menu
import indra.entity as ent
import indra.spatial_env as se
import indra.display_methods as disp
import predprey_model as prdpry

fashions = ["blue", "red"]

INIT_FLWR = 0
INIT_TRND = 1

FSHN_TO_TRACK = 0


class Fashionista(prdpry.MobileCreature):

    """
    The base class for trend-setters and followers.
    """

    def __init__(self, name, life_force=20, repro_age=1000,
                 decay_rate=0.0, max_move=20.0, max_detect=20.0,
                 max_eat=10.0, goal="", rand_age=False):

        super().__init__(name, life_force, repro_age,
                         decay_rate, max_move, max_detect,
                         max_eat, goal, rand_age)

        self.fashion = None
        self.adv_periods = 0

    def act(self):
        """
        Take a look around and see who is wearing what!
        """
        return self.survey_env(self.goal)

    def survey_env(self, goal):
        """
        Take a look around and see who is wearing what!
        """
        return ent.Agent.survey_env(self, goal)

    def respond_to_trends(self, prehended, gt, fshn_ratio,
                          min_others):
        """
        What an agent does based on trends around her,
        """
        if len(prehended) >= min_others:
            has_my_fashion = 0
            not_my_fashion = 0
            for preh in prehended:
                if preh.fashion == self.fashion:
                    has_my_fashion += 1
                else:
                    not_my_fashion += 1
            if(gt is True and
               has_my_fashion > not_my_fashion * fshn_ratio):
                self.adverse_response()
            elif has_my_fashion * fshn_ratio < not_my_fashion:
                self.adverse_response()

    def adverse_response(self):
        """
        What an agent does when he doesn't like the trend.
        """
        self.adv_periods += 1
        if self.adv_periods >= self.env.min_adv_periods:
            self.adv_periods = 0
            self.change_fashion()

    def change_fashion(self):
        """
        Switch my fashion.
        """
        if self.fashion == 1:
            self.fashion = 0
        else:
            self.fashion = 1
        self.env.record_fashion_change(self)
        logging.info(self.name + " is changing fashions")


class Follower(Fashionista, prdpry.Predator):

    """ This class describes the followers in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
                 decay_rate=0.0, max_move=20.0, max_detect=20.0,
                 max_eat=10.0, goal=prdpry.EAT):

        super().__init__(name, life_force, repro_age,
                         decay_rate, max_move, max_detect,
                         max_eat, goal)

        self.fashion = INIT_FLWR

    def act(self):
        prehended = super().act()
        if prehended is not None and len(prehended) > 0:
            self.respond_to_trends(prehended, False,
                                   self.env.fshn_f_ratio,
                                   self.env.flwr_others)


class TrendSetter(Fashionista, prdpry.MobilePrey):
    """
    This class describes the trendsetters in Adam Smith's
    fashion model
    """

    def __init__(self, name, life_force=20, repro_age=1000,
                 decay_rate=0.0, max_move=20.0, max_detect=20.0,
                 goal=prdpry.AVOID):

        super().__init__(name, life_force, repro_age,
                         decay_rate, max_move, max_detect,
                         goal=goal)

        self.fashion = INIT_TRND

    def act(self):
        prehended = super().act()
        if prehended is not None and len(prehended) > 0:
            self.respond_to_trends(prehended,
                                   True,
                                   self.env.fshn_t_ratio,
                                   self.env.trnd_others)


class SocietyEnv(se.SpatialEnv):
    """
    This is the society in which our fashionistas
    will adopt fashions
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__(name, length, height,
                         preact=True, postact=False,
                         model_nm=model_nm)

        self.fshn_f_ratio = self.props.get("fshn_f_ratio",
                                           default=1.3)
        self.fshn_t_ratio = self.props.get("fshn_t_ratio",
                                           default=1.5)

        self.flwr_others = self.props.get("flwr_others",
                                          default=3)
        self.trnd_others = self.props.get("trnd_others",
                                          default=5)

        self.min_adv_periods = self.props.get("min_adv_periods",
                                              default=6)
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew fashions",
                                                   self.display))

    def add_agent(self, agent):
        """
        Add a new fashion agent to the env.
        """
        super().add_agent(agent)

        var = node.get_node_type(agent)

        if agent.fashion == FSHN_TO_TRACK:
            self.agents.change_pop_of_note(var, 1)

    def record_fashion_change(self, agent):
        """
        Track the fashions in our env.
        """
        var = node.get_node_type(agent)
        if agent.fashion == FSHN_TO_TRACK:
            self.agents.change_pop_of_note(var, 1)
        else:
            self.agents.change_pop_of_note(var, -1)

    def census(self, disp=True):
        """
        Take a census of our pops.
        """
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       fashions[FSHN_TO_TRACK] + ":")
        for var in self.agents.varieties_iter():
            pop = self.agents.get_pop_of_note(var)
            self.user.tell(var + ": " + str(pop))
            self.agents.append_pop_hist(var, pop)

    def address_prehensions(self, agent, prehensions):
        """
        Process prehensions list if needed.
        Here we don't have to.
        """
        return prehensions

    def display(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        pop_hist = self.agents.get_pop_hist()

        disp.display_line_graph("Adam Smith's fashion model: "
                                + "Populations in "
                                + self.name
                                + " adopting fashion "
                                + fashions[FSHN_TO_TRACK],
                                pop_hist,
                                self.period)
