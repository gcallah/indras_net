"""
Filename: height_model.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import indra.env as env
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

    def census(self, disp=True):
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
