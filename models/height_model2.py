"""
Filename: height_agent.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import random

REPRODUCE = "reproduce"
ENV_NM = "Schelling height model"
DEF_HEIGHT = 1.0


class HeightAgent(ent.Agent):

    def __init__(self, name, height):
        super().__init__(name, REPRODUCE)
        self.height = height
        self.alive = True
        self.mychild = None
        # print('adding agent with name ' + self.name)

    def act(self):
        self.reproduce()
        self.alive = False

    def reproduce(self):
        self.mychild = HeightAgent(self.name + str(self.env.period),
                                   random.gauss(self.height,
                                                self.height / 4))

        self.env.add_child(self.mychild)
        # print('adding to womb ')


class HeightAgentEng(HeightAgent):

    def __init__(self, name, height):
        super().__init__(name, height)
    # def gen_height(self):
        # new_height = random.uniform(self.height-self.height/4,
        #                             self.height+self.height/4)

    def reproduce(self):
        self.mychild = HeightAgentEng(self.name + str(self.env.period),
                                      random.gauss(self.height,
                                                   self.height/4))

        self.env.add_child(self.mychild)

        # print(self.env.step(self.total_height))
        runt_height = .67 * self.env.cur_avg_height
        if self.mychild.height < runt_height:
            # print('changing agent ' + self.mychild.name
            # + ' height from ' + str(self.mychild.height)
            # + ' to ' + str(runt_height))
            self.mychild.height = runt_height


class HeightEnv(ent.Environment):

    """ This class creates an environment for Schelling height agents """

    def __init__(self, model_nm=None):
        super().__init__("Height Environment", model_nm=model_nm,
                         preact=True)
        self.height_hist = []
        self.cur_avg_height = 0

    def preact_loop(self):
        total_height = 0
        for agent in reversed(self.agents):
            total_height += agent.height
            if not agent.alive:
                print('agent ' + agent.name
                      + ' with a height of ' + str(agent.height))
                self.agents.remove(agent)
            else:
                print('agent ' + agent.name +
                      ' with a height of ' + str(agent.height))

        self.cur_avg_height = total_height / len(self.agents)
        print('Average height period '
              + str(self.period) + ' is: '
              + str(self.cur_avg_height))
