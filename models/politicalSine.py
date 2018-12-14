"""
politicalSine.py
A mathematical model to show the general polarization of an Oligarchy
pretending to be a representative republic.
"""
import indra.entity as ent
import indra.env as env

import math
import numpy as np

POLARIZATION_UP = 1.1
POLARIZATION_DN = 0.9
POLAR_THRESHHOLD = 2.5

NUM_NEG = 0
NUM_POS = 0
NUM_CORRUPT = 0

POLAR = False

PRESIDENT = False

class Citizen(ent.Agent):
    """
    An agent for citizens
    """
    def __init__(self, name, goal, political, wealth):
        """
        -A very basic init. (self, name, political, wealth)
        -political is a number between -5 and 5 representative of
        the political views of the citizen (negative vs positive)
        -wealth is the wealth of the citizen (because oligarchy)
        """
        self.goal = goal
        self.political = political
        self.wealth = wealth
        super().__init__(name, "voting")

    def act(self):
        pass

    def postact(self):
        global POLAR

        if POLAR:
            self.political *= POLARIZATION_UP
        else:
            self.political *= POLARIZATION_DN

class President():
    """
    A representative of a president
    """
    def __init__(self, agents):
        self.political = 0
        for i in agents:
            self.political += i.political
        self.political = 5* self.sigmoid(self.political)

        if self.political < 0:
            global NUM_NEG
            NUM_NEG += 1
        else:
            global NUM_POS
            NUM_POS += 1

        self.oligarchy = 0
        for i in agents:
            self.oligarchy += (i.political + i.wealth)
        self.oligarchy = 5* self.sigmoid(self.oligarchy)

        self.tooPolar = (abs(self.political - self.oligarchy) >= POLAR_THRESHHOLD)
        global POLAR
        if self.tooPolar:
            global NUM_CORRUPT
            NUM_CORRUPT += 1
            POLAR = True
        else:
            POLAR = False

    def sigmoid(self, a): #numerically stable sigmoid function
        return math.exp(-np.logaddexp(0, -a)) -0.5 #compresses values from 0 to 1 and is reduced by 0.5 to get between -1/2 and 1/2

    def polar(self):
        return self.tooPolar

class BasicEnv(env.Environment):
    """
    This environment exists
    """
    def __init__(self, model_nm=None, props=None):
        super().__init__("Citizens environment",
                         preact=True,
                         postact=True,
                         model_nm=model_nm,
                         props=props)

    def preact_loop(self):
        global PRESIDENT
        PRESIDENT = President(self.agents)
        global NUM_NEG
        global NUM_POS
        global NUM_CORRUPT
        print("Negative Presidents: "+str(NUM_NEG)+"\nPositive Presidents: "+str(NUM_POS))

        print("Number of presidents that betray popular opinion: "+str(NUM_CORRUPT)
              +"  ("+str((NUM_CORRUPT/(NUM_POS+NUM_NEG))*100) + "%)")

    def restore_agents(self, json_input):
        temp = 0
        for agent in json_input["agents"]:
            self.add_agent(Citizen(agent["name"+temp],
                                   agent["Voting"]))
            temp += 1
