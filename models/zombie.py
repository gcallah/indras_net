import random
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import numpy as np
import operator as op
import math
import copy

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

STATE_MAP = { N: NORTH, S: SOUTH, E: EAST, W: WEST }
#col_dirs = {'N':0, 'S':0, 'E':0, 'W':0}

NEW_ZOMBS = 0
NEW_HUMANS = 0

#These need to be added to prop args
NEW_HUMAN_LIFEFORCE = 10
INFECTEDTIMER = 5
HUM_REPRO_TIMER_MAX = 10
HUM_REPRO_TIMER_MIN = 5

ZOMBIE_NTYPE = "Zombie"
HUMAN_NTYPE = "Human"



class Beings(ma.MarkovAgent): 
    '''
    A Creature moves around intelligently based on his
    prehension of the env.

    Attributes: 
        alive: boolean indicating if Creature should exist in the env 
        age: int keeps trak of how many steps Creature has been in existance; 
            used for controling periodic reproduction
        other: Wolf or Sheep object to be used by subclass to identify what
            Creature is different than itself
        repro_age: if age (mod repro_age) == 0, make a new Creature of same
            class.
        life_force: if this int goes to or below zero, Creature dies and is 
            removed from env.
        init_life_force: int 
        speed: an int amount of times a Creature may move per turn
        state: the direction the Creature is moving
    '''
    def __init__(self, name, goal, repro_age, life_force, init_state, max_detect=1,
                 rand_age=False, speed=1):
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
        '''
        Removes dead agent from grid.
        '''
        if self.alive:
            self.alive = False
            self.env.died(self)

    def act(self):
        '''
        The Creature moves either one unit north, south, east, 
        or west. For however many units of "speed" he has, he 
        can move that many times per action.
        '''
        for i in range(self.speed):
            super().act()
            self.state = self.next_state
            self.move(self.state)
            
    def move(self, state):
        '''
        Moves self one unit in a cardinal direction if
        that direction is empty and doesn't lead off the
        board.

        Args:
            self: the agent to be moved
            state: a cardinal direction
                North: N = 0
                South: S = 1
                East: E = 2
                West: W = 3
        '''
        x = self.pos[X]
        y = self.pos[Y]
        if state == N:
            if self.env.is_cell_empty(x, y+1):
                self.env.move(self, x,y+1)
        elif state == S:
            if self.env.is_cell_empty(x, y-1):
                self.env.move(self, x,y-1)
        elif state == E:
            if self.env.is_cell_empty(x-1, y):
                self.env.move(self, x-1,y)
        else:
            if self.env.is_cell_empty(x+1, y):
                self.env.move(self, x+1,y)
            
    def postact(self):
        '''
        Every step ages the Creature by 1. If the Creature 
        has not lifeforce, he dies. If the Creature happens to
        be in the right stage of life, he may reproduce.
        '''
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
    '''
    A zombie: moves around randomly and bites humans
    nearby, infecting them.

    Attributes: 
        other: the class of the other kind of Creature, Human
        ntype: "node type," variety of Beings,
            used for bookkeeping purposes by agent_pop.
            
    '''
    def __init__(self, name, goal, repro_age, life_force, max_detect=10,
                    rand_age=False, speed=2):
        init_state = random.randint(0,3)
        super().__init__(name, goal, repro_age, life_force, init_state,
                            max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Human
        self.ntype = "Zombie"
        #self.sleep = 0

    def preact(self):
        '''
        After (or before depending on how you view it) everything moves, 
        zombies eat nearby people.
        '''
        #if self.sleep != 0:
            #if self.goal != "Eating Human":
                #self.goal = "Eating Human"
        creatures = self.neighbor_iter()
        for creature in creatures:
            if type(creature) is Human:
                self.eat(creature)
        #else:
            #self.sleep -= 1

    def eat(self, human):
        '''
        Gains Humans's life force and infects Human, removing from env, and spawning a new zombie.
        '''
        self.life_force += human.life_force
        human.infected()


class Human(Beings):
    '''
    A Human: moves when Human is nearby and sometimes gets eaten.

    Attributes: 
        other: the class of the other kind of Being, Zombie
        ntype: variety of Being, used for bookkeeping purposes by agent_pop, not 
            an essential feature for the running of this program
    '''
    def __init__(self, name, goal, repro_age, life_force, max_detect=5,
                 rand_age=False, speed=1):
        init_state = random.randint(0,3)
        super().__init__(name, goal, repro_age, life_force, init_state,
                         max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Zombie
        self.ntype = "Human"
        self.reproTime = repro_age
        self.lifeTime = life_force
        #self.reproTime = random.randint(HUM_REPRO_TIMER_MIN,HUM_REPRO_TIMER_MAX+1)
                
    def infected(self):
        new_zom = ''
        creatures = self.neighbor_iter()
        
        for creature in creatures:  #  this loop gets all the attributes needed to spawn in new zombie
            if type(creature) is Zombie:
                new_zom = creature.__class__(creature.name + "x", creature.goal,
                                      creature.repro_age, creature.init_life_force)
            self.env.add_agent(new_zom)
            self.died()
        
    def naturalDeath(self):
        new_zom = ''
        creatures = self.neighbor_iter()
        
        if self.lifeTime == 0:
            for creature in creatures:  #same loop as in infected class
                if type(creature) is Zombie:
                    new_zom = creature.__class__(creature.name + "x", creature.goal,
                                          creature.repro_age, creature.init_life_force)
                self.env.add_agent(new_zom)
                self.died()
        else:
            self.lifeTime -= 1
            
    def reproduce(self):
        '''
        Adds a Creature of self's type to a random place in the env.
        '''
        
        if self.reproTime == 0:
            #self.reproTime = random.randint(0,HUM_REPRO_TIMER+1)
            if self.alive:
                creature = self.__class__(self.name + "x", self.goal,
                                          self.repro_age, self.init_life_force)
                #Make a new human and add him  :)
                self.env.add_agent(creature)
                
        else:
            self.reproTime -= 1
            
class Zone(menv.MarkovEnv):
    '''
    A meadow in which wolf eat sheep.
    '''

    def died(self, prey):
        '''
        Removes prey from env.
        '''
        self.remove_agent(prey)

    def get_pre(self, agent, n_census):
        '''
        Gathers and uses env info to make a prehension transition matrix

        Args: 
            self: the env
            agent: the agent acting in the env 
            n_census: unused
        Returns:
            prehesion based on what Creatures are North, South,
            East, and West of self, determining what direction
            the agent might come.
        '''

        trans_str = ""

        d, total = self.dir_info(agent)

        if(type(agent) == Zombie):
            trans_str += self.zombie_trans(d, total)
        else:
            trans_str += self.human_trans(d, total)
        
        trans_matrix = markov.from_matrix(np.matrix(trans_str))
        return trans_matrix

    def dir_info(self, agent):
        '''
        We count wolves and sheep that are North, South, East, West 
        of the agent in question. What quadrant they're in, and how
        far they are from the agent factors into the information returned.
        -----------------------------------
        | \                             / | Positive Diagonal Line: y = x + (ya-xa)
        |   \                         /   |                         x = y - (ya-xa)
        |     \          N          /     |
        |       \                 /       |
        |         \             /         |
        |           \         /           | 
        |             \     /             |
        |               \ /               |
        |     E   agent @ (xa,ya)   W     |
        |               / \               | 
        |             /     \             |
        |           /         \           |
        |         /             \         |
        |       /                 \       |
        |     /                     \     |
        |   /            S            \   |
        | /  other @ (othr[X],othr[Y])  \ | Negative Diagonal Line: y = -x + (ya+xa)
        -----------------------------------                         x = -y + (ya+xa)

        Args:
            self: the environment 
            agent: the agent surveying its environment 

        Returns:
            A dict maping cardinal directions to numbers representing
            both how far and how many agents of the opposite type are
            in that cardinal direciton.
        '''
        directions = {N: 0, S: 0, E: 0, W: 0}
        creatureCoords = (0,0)
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

    def zombie_trans(self, d, total):
        '''
        The wolf uses its survey of the environment to see which
        directions have the closest and most sheep. He'll probably
        go in the direction with the highest reward.

        Args:
            d: a dictionary containing information about where wolves are
             relative to the sheep 
            total: the sum of all the numerical elements of d; used in
             computation

        Returns:
            trans_str: the string representing the sheep's possibilities
            for movement
        '''
        trans_str = ""
        
        cols_dir = {"NN":0, "NS":0, "NE":0, "NW":0,
                   "SN":0, "SS":0, "SE":0, "SW":0,
                   "EN":0, "ES":0, "EE":0, "EW":0,
                   "WN":0, "WS":0, "WE":0, "WW":0}

        #NS, NE, NW, NN = 0,0,0,0
        #SN, SE, SW, SS = 0,0,0,0
        #EN, ES, EW, EE = 0,0,0,0
        #WN, WS, WE, WW = 0,0,0,0

        # Random movement if nothing is in view.
        if total == 0:
            for cd in cols_dir:
                cols_dir[cd] = 0.25
            #NS, NE, NW, NN = 0.25,0.25,0.25,0.25
            #SN, SE, SW, SS = 0.25,0.25,0.25,0.25
            #EN, ES, EW, EE = 0.25,0.25,0.25,0.25
            #WN, WS, WE, WW = 0.25,0.25,0.25,0.25
        else:
            cols_dir["NS"] = d[S]/total
            cols_dir["NE"] = d[E]/total
            cols_dir["NW"] = d[W]/total
            cols_dir["NN"] = 1 - cols_dir["NS"] - cols_dir["NE"] - cols_dir["NW"]

            cols_dir["SN"] = d[N]/total
            cols_dir["SE"] = d[E]/total
            cols_dir["SW"] = d[W]/total
            cols_dir["SS"] = 1 - cols_dir["SN"] - cols_dir["SE"] - cols_dir["SW"] 

            cols_dir["EN"] = d[N]/total
            cols_dir["ES"] = d[S]/total
            cols_dir["EW"] = d[W]/total
            cols_dir["EE"] = 1 - cols_dir["EN"] - cols_dir["ES"] - cols_dir["EW"]

            cols_dir["WN"] = d[N]/total
            cols_dir["WS"] = d[S]/total
            cols_dir["WE"] = d[E]/total
            cols_dir["WW"] = 1 - cols_dir["WN"] - cols_dir["WS"] - cols_dir["WE"]
            
        change_char = 3
        num_till_sign = 1

        trans_str = ""
        for x in cold_dir:
            trans_str += x

            if num_till_sign != change_char:
                trans_str += ", "
                num_till_sign += 1
            else:
                trans_str += ";"
                num_till_sign = 1

        #trans_str += str(NN) + " " + str(NS) + " " + str(NE) + " " + str(NW) + ";"
        #trans_str += str(SN) + " " + str(SS) + " " + str(SE) + " " + str(SW) + ";"
        #trans_str += str(EN) + " " + str(ES) + " " + str(EE) + " " + str(EW) + ";"
        #trans_str += str(WN) + " " + str(WS) + " " + str(WE) + " " + str(WW)

        return trans_str

    def human_trans(self, d, total):
        '''
        The sheep uses it's survey of the environment to determine which
        directions are the least dangerious. He'll go one of these directions.

        Args:
            d: a dictionary containing information about where wolves are
             relative to the sheep 
            total: the sum of all the numerical elements of d; used in
             computation

        Returns:
            trans_str: the string representing the probability a sheep will
                move in any cardinal direction
        '''
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

        trans_str += str(NN) + " " + str(NS) + " " + str(NE) + " " + str(NW) + ";"
        trans_str += str(SN) + " " + str(SS) + " " + str(SE) + " " + str(SW) + ";"
        trans_str += str(EN) + " " + str(ES) + " " + str(EE) + " " + str(EW) + ";"
        trans_str += str(WN) + " " + str(WS) + " " + str(WE) + " " + str(WW)

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


