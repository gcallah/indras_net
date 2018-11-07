import random
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv


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
        for i in range(self.speed):
            super().act()
            self.state = self.next_state
            self.move(self.state)

    def move(self, state):
        x = self.pos[X]
        y = self.pos[Y]
        if state == N:
            if self.env.is_cell_empty(x, y+1):
                self.env.move(self, x, y+1)
        elif state == S:
            if self.env.is_cell_empty(x, y-1):
                self.env.move(self, x, y-1)
        elif state == E:
            if self.env.is_cell_empty(x-1, y):
                self.env.move(self, x-1, y)
        else:
            if self.env.is_cell_empty(x+1, y):
                self.env.move(self, x+1, y)
            
    def postact(self):
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        
        elif (self.ntype == "Human"):
            self.reproduce()
            self.naturalDeath()
        
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
    rand_age=False, speed=2):
        
        init_state = random.randint(0,3)
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
    
    # Zombie eats some of human and extends life force
    # It also infects a human
    def eat(self, human):
        self.life_force += human.life_force
        human.infected()


class Human(Beings):
    
    def __init__(self, name, goal, repro_age, life_force, max_detect=5,
    rand_age=False, speed=1):
        
        init_state = random.randint(0,3)
        super().__init__(name, goal, repro_age, life_force, init_state,
        max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Zombie
        self.ntype = "Human"
        self.reproTime = repro_age
        self.lifeTime = life_force
    
    # Human who has been bit becomes a zombie
    def infected(self):
        new_zom = ''
        creatures = self.neighbor_iter()
        
        for creature in creatures:  #  this loop gets all the attributes needed to spawn in new zombie
            if type(creature) is Zombie:
                new_zom = creature.__class__(creature.name + "x", creature.goal,
                creature.repro_age, creature.init_life_force)
        
            self.env.add_agent(new_zom)
            self.died()
    
    # human dies of natural causes
    def naturalDeath(self):
        new_zom = ''
        creatures = self.neighbor_iter()
        
        if self.lifeTime == 0:
            for creature in creatures:  # same loop as in infected class
                if type(creature) is Zombie:
                    new_zom = creature.__class__(creature.name + "x", creature.goal,
                    creature.repro_age, creature.init_life_force)
        
                self.env.add_agent(new_zom)
                self.died()
        else:
            self.lifeTime -= 1
    
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

        if(type(agent) == Zombie):
            trans_str += self.zombie_trans(d, total)
        else:
            trans_str += self.human_trans(d, total)
        
        trans_matrix = markov.from_matrix(np.matrix(trans_str))
        return trans_matrix
    
    # Finds out which direction (NORTH, SOUTH, EAST, WEST) as more of the 
    # opposite agent type depending on what agent we are dealing with
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

        NS, NE, NW, NN = 0, 0, 0, 0
        SN, SE, SW, SS = 0, 0, 0, 0
        EN, ES, EW, EE = 0, 0, 0, 0
        WN, WS, WE, WW = 0, 0, 0, 0

        # Random movement if nothing is in view.
        if total == 0:
            NS, NE, NW, NN = 0.25, 0.25, 0.25, 0.25
            SN, SE, SW, SS = 0.25, 0.25, 0.25, 0.25
            EN, ES, EW, EE = 0.25, 0.25, 0.25, 0.25
            WN, WS, WE, WW = 0.25, 0.25, 0.25, 0.25
        else:
            NS = d[S]/total
            NE = d[E]/total
            NW = d[W]/total
            NN = 1 - NS - NE - NW

            SN = d[N]/total
            SE = d[E]/total
            SW = d[W]/total
            SS = 1 - SN - SE - SW 

            EN = d[N]/total
            ES = d[S]/total
            EW = d[W]/total
            EE = 1 - EN - ES - EW

            WN = d[N]/total
            WS = d[S]/total
            WE = d[E]/total
            WW = 1 - WN - WS - WE

        trans_str += str(NN) + " " + str(NS) + " " + str(NE) + " " + str(NW) + ";"
        trans_str += str(SN) + " " + str(SS) + " " + str(SE) + " " + str(SW) + ";"
        trans_str += str(EN) + " " + str(ES) + " " + str(EE) + " " + str(EW) + ";"
        trans_str += str(WN) + " " + str(WS) + " " + str(WE) + " " + str(WW)

        return trans_str

    # figures out where all the zombies are and moves humans away from them
    def human_trans(self, d, total):
        best_dir = min(d, key=d.get)

        num_close = 0

        col_N = 0
        col_S = 0
        col_E = 0
        col_W = 0
        if(d[N]==d[best_dir]):
            num_close += 1
            col_N = 1
        if(d[S]==d[best_dir]):
            num_close += 1
            col_S = 1
        if(d[E]==d[best_dir]):
            num_close += 1
            col_E = 1
        if(d[W]==d[best_dir]):
            num_close += 1
            col_W = 1

        NN = col_N/num_close
        SN = col_N/num_close
        EN = col_N/num_close
        WN = col_N/num_close

        NS = col_S/num_close
        SS = col_S/num_close
        ES = col_S/num_close
        WS = col_S/num_close

        NE = col_E/num_close
        SE = col_E/num_close
        EE = col_E/num_close
        WE = col_E/num_close

        NW = col_W/num_close
        SW = col_W/num_close
        EW = col_W/num_close
        WW = col_W/num_close

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
            HUMAN_NTYPE, agent_json["ntype"]))

        if new_agent:
            self.add_agent_to_grid(new_agent, agent_json)


