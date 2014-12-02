"""
Filename: spatial_agent.py
Author: Gene Callahan
"""

import math
import cmath
import time
import random
import logging
import pprint
import numpy as np
import matplotlib.pyplot as plt
import entity


def rand_complex(initPos, radius):
    """Generates a random complex number uniformly picked from a disk of radius."""
    radius = math.sqrt(radius * random.uniform(0.0, radius))
    theta  = random.random() * 2 * math.pi
    return initPos + cmath.rect(radius, theta)


def pos_to_str(pos):
    return str(int(pos.real)) + " , " + str(int(pos.imag))


class SpatialAgent(entity.Agent):

    """ This class is the parent of all entities that are located in space (and might or might not move in it) """

    @classmethod
    def add_new(cls):
        cls.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal)
        self.max_move   = max_move
        self.max_detect = max_detect
        self.pos = None


    def add_env(self, env):
        self.env = env


class SpatialEnvironment(entity.Environment):

    """ Extends the base Environment with entities located in the 
        complex plane """

    @staticmethod
    def get_distance(p1, p2):
        return abs(p1 - p2)


    def __init__(self, name, length, height,
	            preact=False, postact=False):
        super().__init__(name, preact, postact)
        self.length   = length
        self.height   = height
        self.max_dist = self.length * self.height


    def add_agent(self, agent):
        super().add_agent(agent)
        x = random.uniform(0, self.length - 1)
        y = random.uniform(0, self.height - 1)
        agent.pos = complex(x, y)


    def get_entity_pos(self, entity):
        for this_entity in self.agents:
            if entity == this_entity:
                return entity.pos
        return None


    def closest_x(self, pos, target_type):
        x = self.max_dist
        close_target = None
        for entity in self.agents:
            if isinstance(entity, target_type):
                p_pos = entity.pos
                d     = self.get_distance(pos, p_pos)
                if d < x:
                    x = d
                    close_target = entity
        return close_target


    def get_new_wander_pos(self, agent):
        new_pos = rand_complex(agent.pos, agent.get_max_move())
        len = new_pos.real
        ht  = new_pos.imag
        if len < 0.0:
            len = 0.0
        if ht  < 0.0:
            ht  = 0.0
        if len > self.length:
            len = self.length
        if ht  > self.height:
            ht  = self.height
        return complex(len, ht)


