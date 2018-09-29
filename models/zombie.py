import random
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import numpy as np
import operator as op
import math

X = 0
Y = 1

humanTot = 0
zombieTot = 0

# agent condition strings
NORTH = "North"
SOUTH = "South"
EAST = "East"
WEST = "West"

HEALTHY = "Healthy"
INFECTED = "Infected"
ZOMBIFIED = "Zombified"
DECAYED = "Decayed"

#variables used for movement==========================================
NSTATES = 4

N = 0
S = 1
E = 2
W = 3

STATE_MAP = { N: NORTH, S: SOUTH, E: EAST, W: WEST }
#==================================================================

#variables used for determining the condition of a being===========
NCOND = 4

H = 0
I = 1
Z = 2
D = 3

COND_MAP = {H: HEALTHY, I: INFECTED, Z: ZOMBIFIED, D: DECAYED}
#==================================================================

class Beings(ma.MarkovAgent): 
    
    def __init__(self, name, goal, repro_age, life_force, init_state, max_detect=1,
                 rand_age=False, speed=1):
        super().__init__(name, goal, NSTATES, NCOND, init_state, init_cond, max_detect=max_detect)
        if not rand_age:
            self.age = 0
        else:
            self.age = random.randint(0, repro_age - 2)
        self.alive = True
        self.other = None
        self.repro_age = repro_age
        self.life_force = life_force
        self.init_life_force = life_force
        self.speed = speed
        self.state = init_state
        self.cond = init_cond

    def decayed(self):
        
        if self.alive:
            self.alive = False
            self.env.decayed(self)

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
        
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        elif self.age % self.repro_age == 0:
            self.reproduce()
    '''
    def reproduce(self):
        allGroups = 
        for 
        
        if self.alive:
            creature = self.__class__(self.name + "x", self.goal,
                                      self.repro_age, self.init_life_force)
            self.env.add_agent(creature)
    '''

class Human(Beings):
    
    def __init__(self, name, goal, repro_age, life_force, max_detect=5,
                 rand_age=False, speed=2):
        init_state = random.randint(0,3)
        super().__init__(name, goal, repro_age, life_force, init_state,
                         max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Zombie
        self.ntype = "Human"

class Zombie(Beings):
    
    def __init__(self, name, goal, repro_age, life_force, max_detect=10,
                    rand_age=False, speed=2):
        init_state = random.randint(0,3)
        super().__init__(name, goal, repro_age, life_force, init_state,
                            max_detect=max_detect, rand_age=rand_age, speed=speed)
        self.other = Human
        self.ntype = "Zombie"

    def preact(self):
        
        creatures = self.neighbor_iter()
        for creature in creatures:
            if type(creature) is Human:
                self.eat(creature)

    def eat(self, human):
        
        self.life_force += human.life_force
        sheep.died()


class Zone(menv.MarkovEnv):
    
    def decayed(self, prey):
        """
        Removes decayed zombies from env.
        """
        self.remove_agent(prey)

    def get_pre(self, agent, n_census):
        """
        Gathers and uses env info to make a prehension transition matrix
        Args: 
            self: the env
            agent: the agent acting in the env 
            n_census: unused
        Returns:
            prehesion based on what Creatures are North, South,
            East, and West of self, determining what direction
            the agent might come.
        """

        trans_str = ""

        d, total = self.dir_info(agent)

        if(type(agent) == Zombie):
            trans_str += self.zombie_trans(d, total)
        else:
            trans_str += self.human_trans(d, total)
        
        trans_matrix = markov.from_matrix(np.matrix(trans_str))
        return trans_matrix

    def dir_info(self, agent):
        """
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
        """
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
        """
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
        """
        trans_str = ""

        NS, NE, NW, NN = 0,0,0,0
        SN, SE, SW, SS = 0,0,0,0
        EN, ES, EW, EE = 0,0,0,0
        WN, WS, WE, WW = 0,0,0,0

        # Random movement if nothing is in view.
        if total == 0:
            NS, NE, NW, NN = 0.25,0.25,0.25,0.25
            SN, SE, SW, SS = 0.25,0.25,0.25,0.25
            EN, ES, EW, EE = 0.25,0.25,0.25,0.25
            WN, WS, WE, WW = 0.25,0.25,0.25,0.25
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

    def human_trans(self, d, total):
        """
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
        """
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