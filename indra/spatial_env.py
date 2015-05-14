"""
spatial_env.py
The base environment for envs that incorporate space.
"""

from abc import abstractmethod
import logging
import indra.menu as menu
import indra.env as env
import indra.display_methods as disp

X = 0
Y = 1


class SpatialEnv(env.Environment):
    """
    Extends the base Environment with entities located in the
    complex plane.
    """
    def __init__(self, name, width, height, preact=True,
                 postact=False, model_nm=None):

        super().__init__(name, preact=preact,
                         postact=postact, model_nm=model_nm)

        self.disp_census = True
        self.width = width
        self.height = height
        self.max_dist = self.width * self.height
        self.scatter_plot = None
        self.plot_title = "Agent Positions"
# it only makes sense to plot agents in a spatial env, so add this here:
        self.menu.view.add_menu_item("s",
                                     menu.MenuLeaf("(s)catter plot",
                                                   self.plot))

    def add_agent(self, agent, position=True):
        """
        Add a spatial agent to env
        """
        super().add_agent(agent)
        if position:
            self.position_item(agent)

        logging.debug("Adding " + agent.__str__()
                      + " of variety " + agent.get_type())

    @abstractmethod
    def position_item(self, agent):
        """
        This must be implemented by descendents.
        """

    def preact_loop(self):
        """
        Before acting, get agent's new location.
        """
        logging.debug("Calling preact_loop()")
        for agent in self.agents:
            if agent.wandering:
                agent.pos = self.get_new_wander_pos(agent)
                logging.debug("We are about to survey the "
                              "env for "
                              + agent.name + " which has a goal of "
                              + agent.goal)
                prehensions = agent.survey_env(agent.goal)
                self.address_prehensions(agent, prehensions)
            else:
                agent.detect_behavior()

    def address_prehensions(self, agent, prehensions):
        """
        Process prehensions list if needed.
        """
        if len(prehensions) > 0:
            agent.focus = self.closest_x(agent, prehensions)
            logging.debug("Targ = " + str(agent.focus))
            agent.wandering = False
        return [agent.focus]

    def closest_x(self, seeker, prehensions):
        """
        What is the closest entity of target_type?
        To be implemented by descendents.
        """
        pass

    def get_new_wander_pos(self, agent):
        """
        Should be implemented in descendents.
        """
        pass

    def get_pos_components(self, agent):
        return agent.get_pos()

    def plot(self):
        """
        Show where agents are in graphical form.
        """
        data = self.plot_data()
        # system = self.props.get("OS")
        # anim_val = (system != "Windows")
        anim_val = True
        self.scatter_plot = disp.ScatterPlot(
            self.plot_title, data,
            int(self.width), int(self.height),
            anim=anim_val, data_func=self.plot_data)
        self.scatter_plot.show()

    def plot_data(self):
        data = {}
        for var in self.agents.varieties_iter():
            data[var] = {}
            data[var][X] = []
            data[var][Y] = []
            data[var]["color"] = self.agents.get_var_color(var)
            for agent in self.agents.variety_iter(var):
                (x, y) = self.get_pos_components(agent)
                data[var][X].append(x)
                data[var][Y].append(y)
        return data
