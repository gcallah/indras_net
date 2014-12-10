
"""
Filename: fashion.py
Author: Gene Callahan
"""

import copy
import math
import cmath
import time
import random
import logging
import pprint
import numpy as np
import matplotlib.pyplot as plt
import entity
import spatial_agent as spagnt
import predator_prey as prdpry
import display_methods as disp


fashions = ["blue", "red"]

INIT_FLWR = 0
INIT_TRND = 1

FSHN_TO_TRACK = 0


class Fashionista(prdpry.MobileCreature):

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal="", rand_age=False):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect, max_eat,
            goal, rand_age)

        self.fashion = None

    def act(self):
        pass



class Follower(Fashionista, prdpry.Predator):

    """ This class describes the followers in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal=prdpry.EAT):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            max_eat, goal)

        self.fashion = INIT_FLWR

    def eat(self, prey):
        if self.fashion != prey.fashion:
            logging.info("About to eat: my fashion is " 
                + fashions[self.fashion] +
                " my fashion will be " + fashions[prey.fashion])
            logging.info("Eating: " + fashions[prey.fashion])
            self.fashion = prey.fashion
            self.env.record_fashion_change(self)


class TrendSetter(Fashionista, prdpry.MobilePrey):

    """ This class describes the trendsetters in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            goal=prdpry.AVOID):

        print("Creating trend setter with goal of "
                + goal)

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            goal=goal)

        self.fashion = INIT_TRND


    def avoid_predator(self):
        print("Avoiding predator")


class SocietyEnv(prdpry.PredPreyEnv):

    """ This is the society in which our fashionistas
        will adopt fashions """

    def __init__(self, name, length, height):
        super().__init__(name, length, height,
            preact=True, postact=False)

        self.varieties = {}
    

    def get_agent_type(self, agent):
        return(self.get_class_name(type(agent)))


            
    def add_agent(self, agent):
        spagnt.SpatialEnvironment.add_agent(self, agent)

        a = self.get_agent_type(agent)
        logging.info("Adding " + agent.__str__()
                + " of type " + a)

        if a in self.varieties:
            if agent.fashion == FSHN_TO_TRACK:
                self.varieties[a]["pop"] += 1
            else:
                self.varieties[a]["pop"] = 0        
        else:
            if agent.fashion == FSHN_TO_TRACK:
                self.varieties[a] = {"pop": 1, "pop_hist": []}
            else:
                self.varieties[a] = {"pop": 0, "pop_hist": []}

    
    def record_fashion_change(self, agent):
        a = self.get_agent_type(agent)
        if agent.fashion == FSHN_TO_TRACK:
            self.varieties[a]["pop"] += 1
        else:
            self.varieties[a]["pop"] -= 1        


    def census(self):
        print("Populations in period " + str(self.period) +
                " adopting " + 
                fashions[FSHN_TO_TRACK] + ":")
        for a in self.varieties:
            pop = self.varieties[a]["pop"]
            print(a + ": " +  str(pop))
            self.varieties[a]["pop_hist"].append(pop)


    def display(self):
        if self.period < 4:
            print("Too little data to display")
            return

        pop_hist = {}
        for a in self.varieties:
            pop_hist[a] = self.varieties[a]["pop_hist"]

        disp.display_line_graph('Populations in '
                                + self.name,
                                pop_hist,
                                self.period)

