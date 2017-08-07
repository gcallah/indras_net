"""
spatial_env.py
The base environment for envs that incorporate space.
"""

from abc import abstractmethod
import logging
import indra.menu as menu
import indra.env as env
import indra.user as user
import indra.display_methods as disp

X = 0
Y = 1


class SpatialEnv(env.Environment):
    """
    Extends the base Environment with entities located in the
    complex plane.
    """
    def __init__(self, name, width, height, preact=True,
                 postact=False, model_nm=None, props=None):

        super().__init__(name, preact=preact,
                         postact=postact, model_nm=model_nm,
                         props=props)

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

    def closest_x(self, seeker, prehensions):
        """
        What is the closest entity of target_type?
        To be implemented by descendents.
        """
        pass

    def plot(self):
        """
        Show where agents are in graphical form.
        """
        if not disp.plt_present:
            self.user.tell("No graphing package installed", type=user.ERROR)
            return

        data = self.plot_data()
        self.scatter_plot = disp.ScatterPlot(
            self.plot_title, data,
            int(self.width), int(self.height),
            anim=True, data_func=self.plot_data)
        self.scatter_plot.show()

    def plot_data(self):
        data = {}
        for var in self.agents.varieties_iter():
            data[var] = {}
            data[var][X] = []
            data[var][Y] = []
            data[var]["color"] = self.agents.get_var_color(var)
            for agent in self.agents.variety_iter(var):
                if agent.pos is not None:
                    (x, y) = agent.pos
                    data[var][X].append(x)
                    data[var][Y].append(y)
        return data
