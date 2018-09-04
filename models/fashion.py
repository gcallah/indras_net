"""
fashion_model.py
A fashion model that includes followers and hipsters
changing fashions based on each other's choices.
"""
import logging
import indra.display_methods as disp
import indra.menu as menu
import indra.two_pop_model as tp


class Follower(tp.Follower):
    """
    A fashion follower: tries to switch to hipsters' fashions.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = Hipster


class Hipster(tp.Leader):
    """
    A fashion hipster: tries to not look like followers.
    """
    def __init__(self, name, goal, max_move, variability=.5):
        super().__init__(name, goal, max_move, variability)
        self.other = Follower


class Society(tp.TwoPopEnv):
    """
    A society of hipsters and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False,
                props=None):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=True, props=props)
        self.stances = ["blue", "red"]
        self.line_graph_title = \
            "A. Smith's fashion model: Populations in %s adopting fashion %s"
        self.set_var_color('Hipster', disp.GREEN)
        self.set_var_color('Follower', disp.MAGENTA)
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew fashions",
                                                   self.view_pop))

    def restore_agent(self, agent_json):
        new_agent = None
        if agent_json["ntype"] == Hipster.__name__:
            new_agent = Hipster(name=agent_json["name"],
                                goal=agent_json["goal"],
                                max_move=agent_json["max_move"])

        elif agent_json["ntype"] == Follower.__name__:
            new_agent = Follower(name=agent_json["name"],
                                 goal=agent_json["goal"],
                                 max_move=agent_json["max_move"])

        else:
            logging.error("agent found whose NTYPE is neither "
                          "{} nor {}, but rather {}".format(Hipster.__name__,
                                                            Follower.__name__,
                                                            agent_json["ntype"]))

        if new_agent:
            self.add_agent_to_grid(new_agent, agent_json)
