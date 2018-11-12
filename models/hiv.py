import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

import random

NSTATES = 4

NORTH = "North"
SOUTH = "South"
EAST = "East"
WEST = "West"

N = 0
S = 1
E = 2
W = 3

STATE_MAP = { N: NORTH, S: SOUTH, E: EAST, W: WEST }

INFECTION_CHANCE = 50
SYMPTOMS_SHOW = 200
SYMPTOMS_SHOW_PROB = .05

class Person(ma.MarkpvAgent):
    """
        Attributes:
        coupled: boolean indicating if a person is coupled
        couple_length: int indicating how long this person has been coupled
        partner: pointing to the partner if coupled
        infected: boolean indicating if a person is infected with HIV
        known: boolean indicating if a person is aware of the HIV infection
        infection_length: int indicating how long this person has been infected with HIV
        coupling_tendency: likelihood that this person has sex (0-10)
        condom_use: chance that this person uses a condom (0-10)
        test_frequency: frequency that this person checks HIV status in a 1-year time period (0-4)
        commitment: how long sexual relationships lasts for this person (0-200)
        """
    def __init__(self, name, infected, infection_length, coupling_tendency, condom_use, test_frequency, commitment):
        init_state = random.randint(0, 3)
        super().__init__(name, "wandering around", NSTATES, init_state)
        self.coupled = False
        self.couple_length = 0
        self.partner = None
        self.infected = infected
        self.known = False
        self.infection_length = infection_length
        self.coupling_tendency = coupling_tendency
        self.condom_use = condom_use
        self.test_frequency = test_frequency
        self.commitment = commitment
        self.state = init_state
    
    def couple(self):
        for person in self.neighbor_iter():
            if person.coupled is False:
                if random.randint(0, 10) < person.coupling_tendency:
                    self.coupled = True
                    self.partner = person
                    person.coupled = True
                    person.partner = self
    
    def infect(self):
        if self.coupled is True and self.infected is True and self.known is False:
            if random.randint(0, 10) > self.condom_use or random.randint(0, 10) > self.partner.condom_use:
                if random.randint(0, 99) < INFECTION_CHANCE:
                    self.partner.infected = True

def preact(self):
    if self.coupled is False:
        if random.randint(0, 10) < self.coupling_tendency:
            self.couple()
        self.infect()

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

def act(self):
    if self.coupled is False:
        super().act()
        self.state = self.next_state
            self.move(self.state)

def test(self):
    if random.randint(0, 4) < self.test_frequency and self.infected is True:
        self.known = True
        if self.infection_length > SYMPTOMS_SHOW:
            if random.rand() <= SYMPTOMS_SHOW_PROB:
                self.known = True

def uncouple(self):
    if self.coupled is True:
        if self.couple_length > self.commitment or self.couple_length > self.partner.commitment:
            self.coupled = False
                self.couple_length = 0
                self.partner.coupled False
                self.partner.couple_length = 0
                self.partner.partner = None
                self.partner = None

def postact(self):
    if self.infected is True:
        self.infection_length += 1
        if self.coupled is True:
            self.couple_length += 1
    self.test()
        self.uncouple()


class People(menv.MarkovEnv):
    """
        Individuals wander around randomly when they are not in couples. Upon coming into contact with a suitable partner, there is a chance the two individuals will couple together. When this happens, the two individuals no longer move around, they stand next to each other holding hands as a representation of two people in a sexual relationship.
        """


