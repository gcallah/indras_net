"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
"""

import time
import logging
import pprint
import pdb
import random


RUN_MODE  = 0
STEP_MODE = 1
INSP_MODE = 2
VISL_MODE = 3
CODE_MODE = 4
DBUG_MODE = 5
LIST_MODE = 6
QUIT_MODE = 7
PASS_MODE = 8


pp = pprint.PrettyPrinter(indent=4)

def join_entities(prehender, rel, prehended):
    prehender.add_prehension(Prehension(rel, prehended))


class Entity:

    universals  = {}
    
    
    @classmethod
    def create_first_prehension(cls, prehended):
        vals = []
        vals.append(prehended)
        return vals


    @classmethod
    def get_class_name(cls, genera):
        return genera.__name__


    @classmethod
    def add_universal(cls, prehender, universal, prehended):
        prehender_type_name = cls.get_class_name(prehender)
        prehended_type_name = cls.get_class_name(prehended)
        print("Trying to add a universal!")
        if universal not in cls.universals:
            cls.universals[universal] = \
                {prehender_type_name: cls.create_first_prehension(prehended)}
            logging.info(pp.pformat(cls.universals))
        elif prehender not in cls.universals[universal]:
            cls.universals[universal][prehender_type_name] = \
                cls.create_first_prehension(prehended)
            logging.info(pp.pformat(cls.universals))
        else:
            cls.universals[universal][prehender_type_name].append(prehended)


    @classmethod
    def get_universal_instances(cls, prehender, universal):
        if universal in cls.universals:
            prehnder_cls = cls.get_class_name(prehender)
            if prehnder_cls in cls.universals[universal]:
                return cls.universals[universal][prehnder_cls]
            else:
                return None
        else:
            return None


    def __init__(self, name):
        self.name        = name
        self.prehensions = []
        self.env = None
        
    def add_env(self, env):
        self.env = env


    def __str__(self):
        return self.name


    def walk_graph_breadth_first(self, func, top):
        if top:
            func(self)
        for prehension in self.prehensions:
            func(prehension.prehended_entity)
        for prehension in self.prehensions:
            prehension.prehended_entity.walk_graph_breadth_first(func, 
                                                  False)


    def add_prehension(self, pre):
        self.prehensions.append(pre)


    def print_prehensions(self):
        for prehension in self.prehensions:
            print(prehension.prehended_entity.name 
                + " is my " + prehension.name)


    def pprint(self):
        for key, value in self.__dict__.items():
            print(key + " = " + str(value))


class Agent(Entity):

    """ This class adds a goal to an entity 
        and is the base for all other agents. """

    def __init__(self, name, goal=None):
        super().__init__(name)
        self.goal = goal

    def act(self):
        print("Agent " + self.name + " trying to achieve " + self.goal)

    def preact(self):
        pass
    
    def postact(self):
        pass
    

class Environment(Entity):

    """ A basic environment allowing starting, stopping, stepping, etc. """

    prev_period = 0  # in case we need to restore state

    keymap = { "r": RUN_MODE,
               "s": STEP_MODE,
               "i": INSP_MODE,
               "l": LIST_MODE,
               "v": VISL_MODE,
               "c": CODE_MODE,
               "d": DBUG_MODE,
               "q": QUIT_MODE,
               "p": PASS_MODE}


    def __init__(self, name, preact = False, postact = False):
        super().__init__(name)
        self.agents   = []
        self.womb = []
        self.period = 0
        self.preact = preact
        self.postact = postact

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.add_env(self)
    
    def add_child(self, agent):
        self.womb.append(agent)
        agent.add_env(self)

    def find_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None


    def list_agents(self):
        for agent in self.agents:
            print(agent.name + " with a goal of " + agent.goal)
   

    def menu(self):
        print("Running in " + self.name + ".")
        print("Choose one and press Enter:")
        choice = input(
            "(r)un; (s)tep; (v)isualize; (i)nspect agent; (l)ist agents; (c)ode; (d)ebug; (q)uit: ")
        return self.keymap.get(choice.strip(), STEP_MODE)


    def run(self, resume=False):
        if resume: self.period = Environment.prev_period
        else:      self.period = 0

        mode = self.menu()
        while mode != QUIT_MODE:
            if mode == RUN_MODE:
                print("Running continously; press Ctrl-c to halt!")
                time.sleep(3)
                try:
                    while self.keep_running():
                        self.period += 1
                        self.step(delay=.3)
                except KeyboardInterrupt:
                    pass
            elif mode == STEP_MODE:
                self.period += 1
                self.step(delay=0)
            elif mode == INSP_MODE:
                name = input("Type the name of the agent to inspect: ")
                entity = self.find_agent(name.strip())
                if entity == None: print("No such agent")
                else: entity.pprint()
            elif mode == VISL_MODE:
                self.display()
            elif mode == LIST_MODE:
                print("Active agents in environment:")
                self.list_agents()
            elif mode == CODE_MODE:
                code = eval(input("Type a line of code to run: "))
            elif mode == DBUG_MODE:
                pdb.set_trace()
            elif mode == PASS_MODE:
                pass

            mode = self.menu()

        Environment.prev_period = self.period

        print("Returning to run-time environment")


    def step(self, delay=0):
        if delay > 0: time.sleep(delay)

# agents might be waiting to be born       
        if self.womb != None:
            for agent in self.womb:
                self.add_agent(agent)
            del self.womb[:]  

# there might be state-setting to do before acting
        if(self.preact):
            self.pre_act_loop()

# now have everyone act in random order
        self.act_loop()
        
# there might be cleanup to do after acting
        if(self.postact):
            self.post_act_loop()
        
    
    def act_loop(self):
        indices = list(range(len(self.agents)))
        random.shuffle(indices)
        for i in indices:
            self.agents[i].act()


    def pre_act_loop(self):
        for agent in self.agents:
            agent.preact()


    def post_act_loop(self):
        for agent in self.agents:
            agent.postact()


    def keep_running(self):
        return False


    def display(self):
        pass


class Prehension():

    def __init__(self, name, entity):
        self.name   = name
        self.weight = 1.0;
        self.prehended_entity = entity



