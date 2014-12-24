
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
import prop_args
import entity
import spatial_agent as spagnt
import predprey_model as prdpry
import display_methods as disp

fashions = ["blue", "red"]

INIT_FLWR = 0
INIT_TRND = 1

FSHN_TO_TRACK = 0


class Fashionista(prdpry.MobileCreature):


    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=0.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal="", rand_age=False):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect, max_eat,
            goal, rand_age)

        self.fashion = None
        self.adv_periods = 0


    def act(self):
        return self.survey_env(self.goal)


    def survey_env(self, goal):
        return spagnt.SpatialAgent.survey_env(self, goal)


    def respond_to_trends(self, prehended, gt, fshn_ratio,
                            min_others):
        if len(prehended) >= min_others:
            has_my_fashion = 0
            not_my_fashion = 0
            for preh in prehended:
                if preh.fashion == self.fashion:
                    has_my_fashion += 1
                else:
                    not_my_fashion += 1 
            if(gt == True and
                has_my_fashion > not_my_fashion * fshn_ratio):
                self.adverse_response()
            elif has_my_fashion * fshn_ratio < not_my_fashion:
                self.adverse_response()


    def adverse_response(self):
        self.adv_periods += 1
        if self.adv_periods >= self.env.min_adv_periods:
            self.adv_periods = 0
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
            decay_rate=0.0, max_move=10.0, max_detect=10.0,
            max_eat=10.0, goal=prdpry.EAT):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            max_eat, goal)

        self.fashion = INIT_FLWR

    
    def act(self):
        prehended = super().act()
        if(prehended != None and len(prehended) > 0):
            self.respond_to_trends(prehended, False,
                    self.env.fshn_f_ratio, self.env.flwr_others)


class TrendSetter(Fashionista, prdpry.MobilePrey):

    """ This class describes the trendsetters in Adam Smith's
        fashion model """

    def __init__(self, name, life_force=20, repro_age=1000,
            decay_rate=0.0, max_move=10.0, max_detect=10.0,
            goal=prdpry.AVOID):

        super().__init__(name, life_force, repro_age,
            decay_rate, max_move, max_detect,
            goal=goal)

        self.fashion = INIT_TRND

    
    def act(self):
        prehended = super().act()
        if(prehended != None and len(prehended) > 0):
            self.respond_to_trends(prehended,
                    True, self.env.fshn_t_ratio,
                    self.env.trnd_others)



class SocietyEnv(spagnt.SpatialEnvironment):

    """ This is the society in which our fashionistas
        will adopt fashions """

    def __init__(self, name, length, height, logfile=None, model_nm=None):
        super().__init__(name, length, height,
            preact=True, postact=False, logfile=logfile, model_nm=model_nm)

        self.varieties = {}

        self.fshn_f_ratio = self.props.get("fshn_f_ratio",
                                default = 1.3)
        self.fshn_t_ratio = self.props.get("fshn_t_ratio",
                                default = 1.5)
        
        self.flwr_others = self.props.get("flwr_others",
                                default = 3)
        self.trnd_others = self.props.get("trnd_others",
                                default = 5)

        self.min_adv_periods = self.props.get("min_adv_periods",
                                default = 6)


    def add_agent(self, agent):
        spagnt.SpatialEnvironment.add_agent(self, agent)

        a = self.get_agent_type(agent)

        if agent.fashion == FSHN_TO_TRACK:
            self.varieties[a]["pop_of_note"] += 1

    
    def record_fashion_change(self, agent):
        a = self.get_agent_type(agent)
        if agent.fashion == FSHN_TO_TRACK:
            self.varieties[a]["pop_of_note"] += 1
        else:
            self.varieties[a]["pop_of_note"] -= 1        


    def census(self):
        print("Populations in period " + str(self.period) +
                " adopting " + 
                fashions[FSHN_TO_TRACK] + ":")
        for a in self.varieties:
            pop = self.varieties[a]["pop_of_note"]
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

