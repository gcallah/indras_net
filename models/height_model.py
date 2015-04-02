"""
Filename: height_agent.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import indra.env as env
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
        #print('adding agent with name ' + self.name)

    def act(self):
        #super().act()
        self.reproduce()
        self.alive = False

    def reproduce(self):
        self.mychild = HeightAgent(self.name + str(self.env.period), random.gauss(self.height, self.height/4))

        self.env.add_child(self.mychild)
        #print('adding to womb ')

class HeightAgentEng(HeightAgent):

    def __init__(self, name, height):
        super().__init__(name, height)
    #def gen_height(self):
        #new_height = random.uniform(self.height-self.height/4,self.height+self.height/4)


    def reproduce(self):
        self.mychild = HeightAgentEng(self.name + str(self.env.period), random.gauss(self.height, self.height/4))

        self.env.add_child(self.mychild)

        #print(self.env.step(self.total_height))
        runt_height = .67 * self.env.cur_avg_height
        if self.mychild.height < runt_height:
            #print('changing agent ' + self.mychild.name + ' height from ' + str(self.mychild.height) + ' to ' + str(runt_height))
            self.mychild.height = runt_height

class HeightEnv(env.Environment):

    """ This class creates an environment for Schelling height agents """


    def __init__(self, model_nm = None):
        super().__init__( "Height Environment", model_nm=model_nm, preact=True)
        self.height_hist = []
        self.cur_avg_height = 0

    def preact_loop(self):
        total_height = 0
        for agent in reversed(self.agents):
            if agent.alive:
                total_height += agent.height
            else:
#                print ( agent.name + ' with a height of ' + str(agent.height))
                self.agents.remove(agent)
        self.cur_avg_height = total_height / len(self.agents)
        self.height_hist.append(self.cur_avg_height)
        print ('Average height period ' + str(self.period) + ' is: ' + str(self.cur_avg_height))
        print(self.height_hist)
#    def display(self):
#        
#        if self.period < 4:
#            self.user.tell("Too little data to display")
#            return
#
#        
#
#        disp.display_line_graph("Carl Menger's money model: "
#                                + "Trades per good ",
#                                self.height_hist,
#                                self.period)







