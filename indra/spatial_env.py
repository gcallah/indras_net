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
import indra.spatial_agent as sa
import io

X = 0
Y = 1

RANDOM = -1

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
        self.image_bytes = io.BytesIO()

    def add_agent(self, agent, x=RANDOM, y=RANDOM, position=True):
        """
        Add a spatial agent to env
        """
        super().add_agent(agent)
        if position:
            self.position_item(agent, x, y)

        logging.debug("Adding " + agent.__str__()
                      + " of variety " + agent.get_type())

    @abstractmethod
    def position_item(self, agent, x, y):
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
        plot_type = self.props.get("plot_type", "SC")
        if plot_type == "LN":
            return super().plot()
        elif plot_type == "SC":       
            data = self.plot_data()
            self.scatter_plot = disp.ScatterPlot(
                self.plot_title, data,
                int(self.width), int(self.height),
                anim=True, data_func=self.plot_data,
                is_headless=self.if_headless()
                )
            self.image_bytes = self.scatter_plot.show()
            return self.image_bytes

    def plot_data(self):
        data = {}
        for var in self.agents.varieties_iter():
            data[var] = {}
            # matplotlib wants a list of x coordinates, and a list of y
            # coordinates:
            data[var][X] = []
            data[var][Y] = []
            data[var]["color"] = self.agents.get_var_color(var)
            for agent in self.agents.variety_iter(var):
                if agent.pos is not None:
                    (x, y) = agent.pos
                    data[var][X].append(x)
                    data[var][Y].append(y)
        return data
    
    def to_json(self):
        #Serialize the env itself
        safe_fields = super().to_json()
        safe_fields["disp_census"] = self.disp_census
        safe_fields["width"] = self.width
        safe_fields["height"] = self.height
        safe_fields["max_dist"] = self.max_dist
        safe_fields["plot_title"] = self.plot_title
            
        return safe_fields
    
    def from_json(self, json_input):
        super().from_json(json_input)
        
        self.disp_census = json_input["disp_census"]
        self.width = json_input["width"]
        self.height = json_input["height"]
        self.max_dist = json_input["max_dist"]
        self.plot_title = json_input["plot_title"]

    def restore_agent(self, agent_json):
        """
        Restore the states of one agent
        """
        agent = sa.SpatialAgent(agent_json["name"], 
                                   agent_json["goal"],
                                   agent_json["max_move"],
                                   agent_json["max_detect"])
        self.add_agent_from_json(agent)
        
    def add_agent_from_json(self, agent, agent_json):
        """
        Add a restored agent to the env
        """
        agent.from_json_preadd(agent_json)
        self.add_agent(agent)
        agent.from_json_postadd(agent_json)
