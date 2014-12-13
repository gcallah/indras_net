
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
from collections import deque

fashions = ["blue", "red"]

INIT_FLWR = 0
INIT_TRND = 1

FSHN_TO_TRACK = 0
FSHN_F_RATIO = 1.1
FSHN_T_RATIO = 1.8

RCNT_FLWR_HIST = 3
RCNT_TRND_HIST = 9


class Fashionista(prdpry.MobileCreature):

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal="", rand_age=False, recent_hist=3):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect, max_eat,
            goal, rand_age)

        self.fashion = None
        self.recent_focus = deque(maxlen=recent_hist)
        self.recent_hist = recent_hist


    def act(self):
        pass


    def respond_to_trends(self, gt, fshn_ratio):
        focus = self.focus
        if not focus in self.recent_focus:
            self.recent_focus.append(focus)
            logging.info(self.name + " just appended "
                    + focus.name
                    + " to recent; recent len = "
                    + str(len(self.recent_focus)))
        self.wandering = True
        self.focus = None
        if len(self.recent_focus) >= self.recent_hist:
            has_my_fashion = 0
            not_my_fashion = 0
            for recent in self.recent_focus:
                if recent.fashion == self.fashion:
                    has_my_fashion += 1
                else:
                    not_my_fashion += 1 
            if(gt == True and
                has_my_fashion > not_my_fashion * fshn_ratio):
                self.change_fashion()
            elif has_my_fashion * fshn_ratio < not_my_fashion:
                self.change_fashion()



    def change_fashion(self):
        if self.fashion == 1:
            self.fashion = 0
        else:
            self.fashion = 1
        self.env.record_fashion_change(self)
        logging.info(self.name + " is changing fashions")



class Follower(Fashionista, prdpry.Predator):

    """ This class describes the followers in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal=prdpry.EAT):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            max_eat, goal, recent_hist=RCNT_FLWR_HIST)

        self.fashion = INIT_FLWR


    def eat(self, prey):
        self.respond_to_trends(False, FSHN_F_RATIO)



class TrendSetter(Fashionista, prdpry.MobilePrey):

    """ This class describes the trendsetters in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=1.0, max_move=10.0, max_detect=10.0,
            goal=prdpry.AVOID):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            goal=goal, recent_hist=RCNT_TRND_HIST)

        self.fashion = INIT_TRND


    def avoid_predator(self):
        self.respond_to_trends(True, FSHN_T_RATIO)


class SocietyEnv(prdpry.PredPreyEnv):

    """ This is the society in which our fashionistas
        will adopt fashions """

    def __init__(self, name, length, height, logfile=None):
        super().__init__(name, length, height,
            preact=True, postact=False, logfile=logfile)

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
                                + self.name
                                + " adopting fashion "
                                + fashions[FSHN_TO_TRACK],
                                pop_hist,
                                self.period)

