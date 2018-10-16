"""
Filename: height_model.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import indra.env as env
import logging
import random
import indra.display_methods as disp

REPRODUCE = "reproduce"
ENV_NM = "Schelling height model"
MIN_HEIGHT = .2
CHILD_HEIGHT_VAR = 10
RUNT_PCT = .67


class HeightAgent(ent.Agent):
    """
    An agent who reproduces and has offspring with
    a deviation around its height.
    """
    def __init__(self, name, height, parent_height):
        super().__init__(name, REPRODUCE)
        self.height = height
        self.alive = True
        self.mychild = None
        self.parent_height = parent_height

    def act(self):
        self.reproduce()
        self.alive = False

    def get_new_height(self):
        """
        Calculate the height of my child.
        We use parent_height to generate reversion to the mean.
        """
        mu = (self.height + self.parent_height) / 2
        new_height = random.gauss(mu, mu / CHILD_HEIGHT_VAR)
        return new_height

    def reproduce(self):
        """
        Produce offspring.
        """
        new_height = self.get_new_height()
        self.mychild = self.__class__(self.name + str(self.env.period),
                                      new_height, self.height)
        self.env.add_child(self.mychild)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["height"] = self.height
        safe_fields["alive"] = self.alive
        if self.mychild:
            safe_fields["mychild"] = self.mychild.to_json()
        safe_fields["parent_height"] = self.parent_height

        return safe_fields

    def from_json_preadd(self, json_input):
        self.alive = json_input["alive"]
        self.mychild = self.__class__(name=json_input["mychild"]["name"],
                                      height=json_input["mychild"]["height"],
                                      parent_height=json_input["mychild"]["parent_height"])


class HeightAgentEng(HeightAgent):

    def reproduce(self):
        """
        Produce offspring that are not under 'runt_height'.
        """
        super().reproduce()
        if self.mychild.height < self.env.runt_height:
            self.mychild.height = self.env.runt_height


class HeightEnv(env.Environment):
    """
    This class creates an environment for Schelling height agents
    """

    def __init__(self, model_nm=None, props=None):
        super().__init__("Height Environment", model_nm=model_nm, preact=True,
                        props=props)
        self.avg_height = {}
        self.runt_height = 0

    def census(self, disp=True, exclude_var=None):
        """
        Take a census of our pops.
        """
        for var in self.varieties_iter():
            total_height = 0
            num_agents = self.get_pop(var)

            # perhaps we should use reduce here:
            for agent in self.variety_iter(var):
                total_height += agent.height

            self.avg_height[var] = total_height / num_agents
            self.append_pop_hist(var, self.avg_height[var])
            if var == "HeightAgentEng":
                self.runt_height = RUNT_PCT * self.avg_height[var]
            self.user.tell("\nAverage %s height for period %i: %f" %
                           (var, self.period, self.avg_height[var]))

    def view_pop(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        (period, data) = self.line_data()
        self.line_graph = disp.LineGraph("Schelling's height model",
                                         data, period, anim=False)

    def preact_loop(self):
        for agent in reversed(self.agents):
            if not agent.alive:
                self.remove_agent(agent)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["avg_height"] = self.avg_height
        safe_fields["runt_height"] = self.runt_height

        return safe_fields

    def from_json(self, json_input):
        super().from_json(json_input)
        self.avg_height = json_input["avg_height"]
        self.runt_height = json_input["runt_height"]

    def restore_agent(self, agent_json):
        new_agent = self.get_agent_from_json(agent_json)

        if new_agent:
            self.add_agent_from_json(new_agent, agent_json)

    def restore_womb_agent(self, agent_json):
        new_agent = self.get_agent_from_json(agent_json)

        if new_agent:
            self.add_child(new_agent)

    @staticmethod
    def get_agent_from_json(agent_json):
        new_agent = None
        if agent_json["ntype"] == HeightAgent.__name__:
            new_agent = HeightAgent(name=agent_json["name"],
                                    height=agent_json["height"],
                                    parent_height=agent_json["parent_height"])

        elif agent_json["ntype"] in HeightAgentEng.__name__:
            new_agent = HeightAgentEng(name=agent_json["name"],
                                       height=agent_json["height"],
                                       parent_height=agent_json["parent_height"])

        else:
            logging.error("agent found whose NTYPE is neither "
                          "{} nor {}, but rather {}".format(HeightAgent.__name__,
                                                            HeightAgentEng.__name__,
                                                            agent_json["ntype"]))
        return new_agent

    def add_agent_from_json(self, agent, agent_json):
        """
        Add a restored agent to the env
        """
        agent.from_json_preadd(agent_json)
        self.add_agent(agent)
