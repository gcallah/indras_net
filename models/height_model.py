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
        #print(self.height)
       

        self.mychild = HeightAgent(self.name + str(self.env.period),
                                   random.uniform(self.height - 1, self.height + 1))
        #print(new_height)                           
        self.env.add_child(self.mychild)
        #print('adding to womb ')
        

class HeightAgentEng(HeightAgent):

    def __init__(self, name, height):
        super().__init__(name, height)
    #def gen_height(self):
        #new_height = random.uniform(self.height-self.height/4,self.height+self.height/4)

    def reproduce(self):
        self.mychild = HeightAgentEng(self.name + str(self.env.period),
                                      random.uniform(self.height - 1, self.height + 1))

        self.env.add_child(self.mychild)

        if self.mychild.height < self.env.runt_height:
            self.mychild.height = self.env.runt_height
            print('work')



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
        self.user.tell("Average heights in period " + str(self.period))                        
        for var in self.agents.varieties_iter():                                        
            total_height = 0                                                              
            num_agents = self.get_pop(var)
                                                                            
            for agent in self.agents.variety_iter(var):                                 
                total_height += agent.height
              
            self.avg_height[var] = total_height / num_agents 
            self.agents.append_pop_hist(var, self.avg_height[var])   
            if var == "HeightAgentEng":
                self.runt_height = .8 * self.avg_height[var]   
                print(self.runt_height)      
        self.user.tell(var + ": " + str(self.avg_height))
                                                
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
            else:
#                print ( agent.name + ' with a height of ' + str(agent.height))
                pass
       








