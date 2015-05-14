"""
Filename: height_agent.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import indra.env as env
import random
import indra.display_methods as disp

REPRODUCE = "reproduce"
ENV_NM = "Schelling height model"
MIN_HEIGHT = .2


class HeightAgent(ent.Agent):

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
        mu = (self.height + self.parent_height) / 2
        new_height = random.gauss(mu, mu / 10)
        if new_height < MIN_HEIGHT:
            new_height = MIN_HEIGHT
        return new_height
        
    
    def reproduce(self):
        #print(self.height)
        new_height = self.get_new_height()
        self.mychild = self.__class__(self.name + str(self.env.period),
                                       new_height, self.height)                         
        self.env.add_child(self.mychild)   
        

class HeightAgentEng(HeightAgent):

    def reproduce(self):
        super().reproduce()
        if self.mychild.height < self.env.runt_height:
            self.mychild.height = self.env.runt_height


class HeightEnv(env.Environment):

    """ This class creates an environment for Schelling height agents """

    def __init__(self, model_nm = None):
        super().__init__( "Height Environment", model_nm=model_nm, preact=True)
        self.avg_height = {}
        self.runt_height = 0
        
    def census(self, disp=True):                                                        
        """                                                                             
        Take a census of our pops.                                                      
        """
        for var in self.agents.varieties_iter():                                        
            total_height = 0                                                              
            num_agents = self.get_pop(var)
                                                                            
            for agent in self.agents.variety_iter(var):                                 
                total_height += agent.height
              
            self.avg_height[var] = total_height / num_agents 
            self.agents.append_pop_hist(var, self.avg_height[var])   
            if var == "HeightAgentEng":
                self.runt_height = .67 * self.avg_height[var]   
        self.user.tell("\nAverage Heights for Period " + str(self.period) + ": \n" + str(self.avg_height))
                                                
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
                self.agents.remove(agent)
       








