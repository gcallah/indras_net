"""
Filename: spatial_agent.py
Author: Gene Callahan
"""

import math
import cmath
import random
from collections import deque
import logging
import entity as ent
import node
import display_methods as disp

MAX_EXCLUDE = 10


def pos_msg(agent, pos):
    """
    A convenience function for displaying
    an entity's position.
    """
    x = pos.real
    y = pos.imag
    return("New position for " + 
           agent.name + " is "
           + str(int(x)) + ", "
           + str(int(y)))


def rand_complex(initPos, radius):
    """
    Generates a random complex number
    uniformly picked from a disk of radius 'radius'.
    """
    radius = math.sqrt(radius * random.uniform(0.0, radius))
    theta = random.random() * 2 * math.pi
    return initPos + cmath.rect(radius, theta)


def get_distance(p1, p2):
    """
    Return the distance between two complex numbers.
    """
    return abs(p1 - p2)


def pos_to_str(pos):
    """
    Convert a complex position to a string rep.
    """

    return str(int(pos.real)) + " , " + str(int(pos.imag))


class SpatialAgent(ent.Agent):
    """
    This class is the parent of all entities that are
    located in space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal)
        self.max_move = max_move
        self.max_detect = max_detect
        self.pos = None
        self.focus = None
        self.wandering = False
        self.exclude = deque(maxlen=MAX_EXCLUDE)


    def in_detect_range(self, prehended):
        """
        Can we see the prehended with our limited view?
        """
        return self.in_range(prehended, self.max_detect)


    def in_range(self, prey, dist):
        """
        Is one agent in range of another in some sense?
        """

        if prey == None:
            return False

        if get_distance(self.pos, prey.pos) < dist:
            return True
        else:
            return False


    def detect_behavior(self):
        """
        What to do on detecting a prehension.
        """
        pass


class MobileAgent(SpatialAgent):
    """
    Agents that can move in the env
    """

    def __init__(self, name, goal, max_move=20.0, max_detect=20.0):
        super().__init__(name, goal, 
                         max_move=max_move,
                         max_detect=max_detect)
        self.wandering = True


class SpatialEnvironment(ent.Environment):
    """
    Extends the base Environment with entities located in the 
    complex plane.
    """

    def __init__(self, name, length, height, preact=True,
                 postact=False, model_nm=None):

        super().__init__(name, preact=preact,
                         postact=postact, model_nm=model_nm)

        self.disp_census = True
        self.length = length
        self.height = height
        self.max_dist = self.length * self.height
# it only makes sense to plot agents in a spatial env, so add this here:
        plot = ent.MenuLeaf("(s)catter plot", self.plot)
        self.menu.view.add_menu_item("s", plot)


    def add_agent(self, agent):
        """
        Add a spatial agent to env
        """
        super().add_agent(agent)
        x = random.uniform(0, self.length - 1)
        y = random.uniform(0, self.height - 1)
        agent.pos = complex(x, y)

        v = node.get_node_type(agent)
        logging.debug("Adding " + agent.__str__()
                      + " of variety " + v)


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
                return self.address_prehensions(agent, prehensions)
            else:
                agent.detect_behavior()
                return None


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
            if seeker is not agent: # don't locate me!
                if((seeker.exclude == None)
                   or (not agent in seeker.exclude)):
                    p_pos = agent.pos
                    d = get_distance(pos, p_pos)
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
        y  = new_pos.imag
        if x < 0.0:
            x = 0.0
        if y  < 0.0:
            y  = 0.0
        if x > self.length:
            x = self.length
        if y  > self.height:
            y = self.height
        pos = complex(x, y)
        logging.debug(pos_msg(agent, pos))
        return pos


    def plot(self):
        """
        Show where agents are in graphical form.
        """
        data = {}
        for v in self.agents.varieties_iter():
            data[v] = {"x": [], "y": []}
            for a in self.agents.variety_iter(v):
                    pos = a.pos
                    x = pos.real
                    y = pos.imag
                    data[v]["x"].append(x)
                    data[v]["y"].append(y)
                
        disp.display_scatter_plot("Agent Positions", data)


