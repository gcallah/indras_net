"""
spatial_env.py
An environment with a complex plane for agent's to move in.
"""

import math
import cmath
import random
import logging
import indra.node as node
import indra.menu as menu
import indra.env as env
import indra.display_methods as disp


def rand_complex(initPos, radius):
    """
    Generates a random complex number
    uniformly picked from a disk of radius 'radius'.
    """
    radius = math.sqrt(radius * random.uniform(0.0, radius))
    theta = random.random() * 2 * math.pi
    return initPos + cmath.rect(radius, theta)


def pos_msg(agent, pos):
    """
    A convenience function for displaying
    an entity's position.
    """
    return("New position for " +
           agent.name + " is "
           + pos_to_str(pos))


def pos_to_str(pos):
    """
    Convert a complex position to a string rep.
    """
    return str(int(pos.real)) + " , " + str(int(pos.imag))


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
# it only makes sense to plot agents in a spatial env, so add this here:
        self.menu.view.add_menu_item("s",
                                     menu.MenuLeaf("(s)catter plot",
                                                   self.plot))

    def add_agent(self, agent):
        """
        Add a spatial agent to env
        """
        super().add_agent(agent)
        self.position_agent(agent)

        v = node.get_node_type(agent)
        logging.debug("Adding " + agent.__str__()
                      + " of variety " + v)

    def position_agent(self, agent):
        x = random.uniform(0, self.width - 1)
        y = random.uniform(0, self.height - 1)
        agent.pos = complex(x, y)

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
        """
        pos = seeker.pos
        x = self.max_dist
        closest_target = None
        logging.debug("About to search for closest, among "
                      + str(len(prehensions)))
        for agent in prehensions:
            if seeker is not agent:  # don't locate me!
                if(seeker.exclude is None
                   or (agent not in seeker.exclude)):
                    p_pos = agent.pos
                    d = abs(pos - p_pos)
                    if d < x:
                        x = d
                        closest_target = agent
        logging.debug("Going to return closest = " + str(closest_target))
        return closest_target

    def get_new_wander_pos(self, agent):
        """
        If an agent is wandering in the env,
        this assigns it a new, random position
        based on its current position
        """
        new_pos = rand_complex(agent.pos, agent.max_move)
        x = new_pos.real
        y = new_pos.imag
        if x < 0.0:
            x = 0.0
        if y < 0.0:
            y = 0.0
        if x > self.width:
            x = self.width
        if y > self.height:
            y = self.height
        pos = complex(x, y)
        logging.debug(pos_msg(agent, pos))
        return pos

    def get_pos_components(self, agent):
        x = agent.pos.real
        y = agent.pos.imag
        return [x, y]

    def plot(self):
        """
        Show where agents are in graphical form.
        """
        data = self.plot_data()
        # disp.display_scatter_plot("Agent Positions", data)
        disp.display_scatter_plot("Agent Positions", data,
                                  int(self.width), int(self.height),
                                  anim=True,
                                  data_func=self.plot_data)

    def plot_data(self):
        data = {}
        for var in self.agents.varieties_iter():
            data[var] = []
            for agent in self.agents.variety_iter(var):
                # x_y is a list
                x_y = self.get_pos_components(agent)
                data[var].append(x_y)
        return data
