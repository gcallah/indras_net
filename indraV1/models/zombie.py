import random
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import indra.grid_env as env
from indra.grid_env import GridEnv

import numpy as np
import math

X = 0
Y = 1

# agent condition strings
NORTH = "North"
SOUTH = "South"
EAST = "East"
WEST = "West"

NSTATES = 4

N = 0
S = 1
E = 2
W = 3

STATE_MAP = {N: NORTH, S: SOUTH, E: EAST, W: WEST}

NEW_ZOMBS = 0
NEW_HUMANS = 0

# These need to be added to prop args
NEW_HUMAN_LIFEFORCE = 10
INFECTEDTIMER = 5
HUM_REPRO_TIMER_MAX = 10
HUM_REPRO_TIMER_MIN = 5

ZOMBIE_NTYPE = "Zombie"
HUMAN_NTYPE = "Human"

# The class that contains functions both agents use
class Beings(ma.MarkovAgent):
    def __init__(self, name, goal, repro_age,
                 life_force, init_state, max_detect=1, rand_age=False, speed=1):
        super().__init__(name, goal, NSTATES, init_state, max_detect=max_detect)

        if not rand_age:
            self.age = 0
        else:
            self.age = random.randint(0, repro_age)
        self.alive = True
        self.other = None
        self.repro_age = repro_age
        self.life_force = life_force
        self.init_life_force = life_force
        self.speed = speed
        self.state = init_state

    def died(self):
        if self.alive:
            self.alive = False
            self.env.died(self)
    
    def act(self):
        """
        Handles the movement of both agents
        """
        super().act()
        if (self.ntype == "Zombie"):
            self.zomMove()
        if (self.ntype == "Human"):
            self.humMove()
        
    def postact(self):
        """
        Handles dying and reproducing
        """
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        else:
            if(self.ntype == "Human"):
                self.reproduce()
        
        
    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["ntype"] = self.ntype
        safe_fields["repro_age"] = self.repro_age
        safe_fields["life_force"] = self.life_force
        safe_fields["max_detect"] = self.max_detect
        safe_fields["age"] = self.age
        safe_fields["speed"] = self.speed

        return safe_fields

class Zombie(Beings):
    def __init__(self, name, goal, repro_age, life_force, max_detect=10,
    rand_age=False, speed=3):
        
        init_state = random.randint(0, 3)

        super().__init__(name, goal, repro_age, life_force, init_state,
                         max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Human
        self.ntype = "Zombie"

    # Chooses which human to eat
    def preact(self):
        creatures = self.neighbor_iter()
        for creature in creatures:
            if type(creature) is Human:
                self.eat(creature)
                
    def zomMove(self):
        """
        Moves zombie towards nearest
        Human
        """
        creatures = self.neighbor_iter()
        smalldist = 100000
        for creature in creatures:
            followAgent = creature 
            if type(creature) is Human:
                currDist = self.env.dist(self, creature)
                #makes sure the nearest agent isn't itself
                if (currDist < smalldist and self.pos[X] != self.pos[X]
                and self.pos[Y] != self.pos[Y]):
                    smalldist = currDist
                    self.env.move_to_agent(self, followAgent, 3)
                    
    def infected(self):
        creature = self.__class__(self.name + "x", self.goal,
                                          self.repro_age, self.init_life_force)

        self.env.add_agent(creature)
    
    # Zombie eats some of human and extends life force
    # It also infects a human
    def eat(self, human):
        self.life_force += human.life_force
        self.infected()
        human.died()


class Human(Beings):

    def __init__(self, name, goal, repro_age, life_force, max_detect=5,
                 rand_age=False, speed=1):

        init_state = random.randint(0, 3)
        super().__init__(name, goal, repro_age, life_force, init_state,
                         max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Zombie
        self.ntype = "Human"
        self.reproTime = repro_age
        self.lifeTime = life_force

    # Human who has been bit becomes a zombie
    def infected(self):
        self.ntype = "Zombie"
        new_zom = ''
        creatures = self.neighbor_iter()

        for creature in creatures: #this loop gets all the attributes needed to spawn in new zombie

            if type(creature) is Zombie:
                new_zom = creature.__class__(creature.name + "x", creature.goal,
                                             creature.repro_age, creature.init_life_force)

        self.died()
        
    def humMove(self):
        """
        Moves human away from nearest
        Zombie
        """
        creatures = self.neighbor_iter()
        fearAgent = None 
        smalldist = 100000
        for creature in creatures:
            fearAgent = creature 
            if type(creature) is Human:
                currDist = self.env.dist(self, creature)
                #makes sure the nearest agent isn't itself
                if (currDist < smalldist and self.pos[X] != self.pos[X]
                and self.pos[Y] != self.pos[Y]):
                    smalldist = currDist
                    self.env.move_from_agent(self, fearAgent, self.speed)
    
    # add a new human to the zone after certain num of turns
    def reproduce(self):

        if self.reproTime == 0:
            if self.alive:
                creature = self.__class__(self.name + "x", self.goal,
                                          self.repro_age, self.init_life_force)

                self.env.add_agent(creature)

        else:
            self.reproTime -= 1

# Area where humans and zombies interact
class Zone(menv.MarkovEnv):

    # gets rid of dead agents from the Zone
    def died(self, prey):
        self.remove_agent(prey)
           
    # what will happen in the Zone first
    def get_pre(self, agent, n_census):

        trans_str = ""

        d, total = self.dir_info(agent)

        if type(agent) == Zombie:
            trans_str += self.zombie_trans(d, total)
        else:
            trans_str += self.human_trans(d, total)

        trans_matrix = markov.from_matrix(np.matrix(trans_str))
        return trans_matrix
       
    # Finds out which direction (NORTH, SOUTH, EAST, WEST) as more of the 
    # opposite agent type depending on what agent we are dealing with
    # CAN'T GET RID OF OLD METHOD OF MOVEMENT DUE TO ERRORS
    # IN OTHER SCRIPTS
    def dir_info(self, agent):
        directions = {N: 0, S: 0, E: 0, W: 0}
        total = 0
        creatures = agent.neighbor_iter(sq_v=10)
        for creature in creatures:
            if type(creature) == agent.other:
                othr = creature.pos
                xa = agent.pos[X]
                ya = agent.pos[Y]
                # North constitutes upper quadrant and positive diagonal line
                if(-othr[X]+(ya+xa) < othr[Y] and othr[Y] >= othr[X] + (ya-xa)):
                    dist = math.sqrt((ya-othr[Y])**2 + (xa-othr[X])**2)
                    directions[N] += 1/dist
                    total += 1/dist
                # South constitutes lower quadrant and negative diagonal line
                elif(othr[X]+(ya-xa) >= othr[Y] and othr[Y] < -othr[X]+(ya+xa)):
                    dist = math.sqrt((ya-othr[Y])**2 + (xa-othr[X])**2)
                    directions[S] += 1/dist
                    total += 1/dist
                # East constitutes left quadrant and negative diagonal line
                elif(othr[Y]-(ya-xa) > othr[X] and othr[X] <= -othr[Y]+(ya+xa)):
                    dist = math.sqrt((ya-othr[Y])**2 + (xa-othr[X])**2)
                    directions[E] += 1/dist
                    total += 1/dist
                # West constitutes right quadrant and positive diagonal line
                else:
                    dist = math.sqrt((ya-othr[Y])**2 + (xa-othr[X])**2)
                    directions[W] += 1/dist
                    total += 1/dist

        return directions, total
    
    # figures out where all the humans are and moves zombies towards them
    def zombie_trans(self, d, total):
        trans_str = ""

        cols_dir = {"NN":0, "NS":0, "NE":0, "NW":0,
                    "SN":0, "SS":0, "SE":0, "SW":0,
                    "EN":0, "ES":0, "EE":0, "EW":0,
                    "WN":0, "WS":0, "WE":0, "WW":0}

        # Random movement if nothing is in view.
        if total == 0:
            for cd in cols_dir: # set every value in cols_dir to 0.25
                cols_dir[cd] = 0.25
        else:
            cols_dir["NS"] = d[S]/total
            cols_dir["NE"] = d[E]/total
            cols_dir["NW"] = d[W]/total
            cols_dir["NN"] = (1 - cols_dir["NS"] - cols_dir["NE"]
                              - cols_dir["NW"])

            cols_dir["SN"] = d[N]/total
            cols_dir["SE"] = d[E]/total
            cols_dir["SW"] = d[W]/total
            cols_dir["SS"] = (1 - cols_dir["SN"] - cols_dir["SE"]
                              - cols_dir["SW"])

            cols_dir["EN"] = d[N]/total
            cols_dir["ES"] = d[S]/total
            cols_dir["EW"] = d[W]/total
            cols_dir["EE"] = (1 - cols_dir["EN"] - cols_dir["ES"]
                              - cols_dir["EW"])

            cols_dir["WN"] = d[N]/total
            cols_dir["WS"] = d[S]/total
            cols_dir["WE"] = d[E]/total
            cols_dir["WW"] = (1 - cols_dir["WN"] - cols_dir["WS"]
                              - cols_dir["WE"])

        trans_str += (str(cols_dir["NN"]) + " " + str(cols_dir["NS"]) +
                      " " + str(cols_dir["NE"]) + " " + str(cols_dir["NW"]) + ";")
        trans_str += (str(cols_dir["SN"]) + " " + str(cols_dir["SS"]) +
                      " " + str(cols_dir["SE"]) + " " + str(cols_dir["SW"]) + ";")
        trans_str += (str(cols_dir["EN"]) + " " + str(cols_dir["ES"]) +
                      " " + str(cols_dir["EE"]) + " " + str(cols_dir["EW"]) + ";")
        trans_str += (str(cols_dir["WN"]) + " " + str(cols_dir["WS"]) +
                      " " + str(cols_dir["WE"]) + " " + str(cols_dir["WW"]))

        return trans_str


    # figures out where all the zombies are and moves humans away from them
    def human_trans(self, d, total):
        best_dir = min(d, key=d.get)

        num_close = 0

        hum_col_dir = {"col_N":0, "col_S":0, "col_E":0, "col_W":0}

        if d[N] == d[best_dir]:
            num_close += 1
            hum_col_dir["col_N"] = 1
        if d[S] == d[best_dir]:
            num_close += 1
            hum_col_dir["col_S"] = 1
        if d[E] == d[best_dir]:
            num_close += 1
            hum_col_dir["col_E"] = 1
        if d[W] == d[best_dir] :
            num_close += 1
            hum_col_dir["col_W"] = 1

        NN = hum_col_dir["col_N"]/num_close
        SN = hum_col_dir["col_N"]/num_close
        EN = hum_col_dir["col_N"]/num_close
        WN = hum_col_dir["col_N"]/num_close

        NS = hum_col_dir["col_S"]/num_close
        SS = hum_col_dir["col_S"]/num_close
        ES = hum_col_dir["col_S"]/num_close
        WS = hum_col_dir["col_S"]/num_close

        NE = hum_col_dir["col_E"]/num_close
        SE = hum_col_dir["col_E"]/num_close
        EE = hum_col_dir["col_E"]/num_close
        WE = hum_col_dir["col_E"]/num_close

        NW = hum_col_dir["col_W"]/num_close
        SW = hum_col_dir["col_W"]/num_close
        EW = hum_col_dir["col_W"]/num_close
        WW = hum_col_dir["col_W"]/num_close

        trans_str = ""


        trans_str += (str(NN) + " " + str(NS) + " "
                      + str(NE) + " " + str(NW) + ";")
        trans_str += (str(SN) + " " + str(SS) + " "
                      + str(SE) + " " + str(SW) + ";")
        trans_str += (str(EN) + " " + str(ES) + " "
                      + str(EE) + " " + str(EW) + ";")
        trans_str += (str(WN) + " " + str(WS) + " "
                      + str(WE) + " " + str(WW))


        return trans_str
   
    def from_json(self, json_input):
        super().from_json(json_input)
        self.add_variety("Zombie")
        self.add_variety("Human")

    def restore_agent(self, agent_json):
        new_agent = None
        if agent_json["ntype"] == ZOMBIE_NTYPE:
            new_agent = Zombie(name=agent_json["name"],
                               goal=agent_json["goal"],
                               repro_age=agent_json["repro_age"],
                               life_force=agent_json["life_force"],
                               max_detect=agent_json["max_detect"],
                               rand_age=agent_json["age"],
                               speed=agent_json["speed"])

        elif agent_json["ntype"] == HUMAN_NTYPE:
            new_agent = Human(name=agent_json["name"],
                              goal=agent_json["goal"],
                              repro_age=agent_json["repro_age"],
                              life_force=agent_json["life_force"],
                              max_detect=agent_json["max_detect"],
                              rand_age=agent_json["age"],
                              speed=agent_json["speed"])

        else:
            logging.error("agent found whose NTYPE is neither "
                          "{} nor {}, but rather {}".format(ZOMBIE_NTYPE,
                                                            HUMAN_NTYPE,
                                                            agent_json["ntype"]))

        if new_agent:
            self.add_agent_to_grid(new_agent, agent_json)
