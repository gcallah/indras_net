import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

import random

X = 0
Y = 1

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

NEG_NTYPE = "HIV- uncoupled"
POZ_NTYPE = "HIV+ uncoupled"
UKP_NTYPE = "HIV? uncoupled"

NEG_NTYPE_C = "HIV- coupled"
POZ_NTYPE_C = "HIV+ coupled"
UKP_NTYPE_C = "HIV? coupled"

TRANS = ".25 .25 .25 .25; .25 .25 .25 .25; .25 .25 .25 .25; .25 .25 .25 .25"

INFECTION_CHANCE = 100
SYMPTOMS_SHOW = 200
SYMPTOMS_SHOW_PROB = .05

class Person(ma.MarkovAgent):
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
        test_frequency: frequency that this person checks HIV status in times per year (0-4)
        commitment: how long sexual relationships lasts for this person in weeks (1-200)
        """
    def __init__(self, name, infected, infection_length, coupling_tendency, condom_use, test_frequency, commitment, coupled=False, coupled_length=0, known=False):
        init_state = random.randint(0, 3)
        super().__init__(name, "wandering around", NSTATES, init_state)
        self.coupled = coupled
        self.couple_length = coupled_length
        self.partner = None
        self.infected = infected
        self.known = known
        self.infection_length = infection_length
        self.coupling_tendency = coupling_tendency
        self.condom_use = condom_use
        self.test_frequency = test_frequency
        self.commitment = commitment
        self.state = init_state
        self.update_ntype()

    def update_ntype(self):
        old_type = self.ntype
        if self.coupled is False:
            if self.infected:
                if self.known:
                    self.ntype = POZ_NTYPE
                else:
                    self.ntype = UKP_NTYPE
            else:
                self.ntype = NEG_NTYPE
        else:
            if self.infected:
                if self.known:
                    self.ntype = POZ_NTYPE_C
                else:
                    self.ntype = UKP_NTYPE_C
            else:
                self.ntype = NEG_NTYPE_C
        if old_type is not 'Person':
            self.env.change_agent_type(self, old_type, self.ntype)
        # print(self.name, "has ntype", self.ntype)

    def couple(self):
        for person in self.neighbor_iter():
            if person.coupled is False:
                if random.randint(0, 10) < person.coupling_tendency:
                    self.coupled = True
                    self.partner = person
                    person.coupled = True
                    person.partner = self
                    # print(self.name, "has been coupled with", person.name)
                    break
    
    def infect(self):
        if self.coupled is True and self.infected is True and self.known is False:
            if random.randint(0, 10) > self.condom_use or random.randint(0, 10) > self.partner.condom_use:
                if random.randint(0, 99) < INFECTION_CHANCE:
                    self.partner.infected = True
                    print(self.name, "has infected", self.partner.name)

    def preact(self):
        if self.coupled is False:
            if random.randint(0, 10) < self.coupling_tendency:
                self.couple()
            self.infect()
        # update partner after restored
        elif self.partner is not None:
            self.partner.partner = self

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
                if random.random() <= SYMPTOMS_SHOW_PROB:
                    self.known = True

    def uncouple(self):
        if self.coupled is True:
            if self.couple_length > self.commitment or self.couple_length > self.partner.commitment:
                self.coupled = False
                self.couple_length = 0
                self.partner.coupled = False
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
        self.update_ntype()
        #print(self.name, "has ntype", self.ntype)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["ntype"] = self.ntype
        safe_fields["coupled"] = self.coupled
        safe_fields["coupled_length"] = self.couple_length
        if self.partner:
            safe_fields["partner"] = self.partner.name
        else:
            safe_fields["partner"] = "None"
        safe_fields["infected"] = self.infected
        safe_fields["known"] = self.known
        safe_fields["infection_length"] = self.infection_length
        safe_fields["coupling_tendency"] = self.coupling_tendency
        safe_fields["condom_use"] = self.condom_use
        safe_fields["test_frequency"] = self.test_frequency
        safe_fields["commitment"] = self.commitment

        return safe_fields


class People(menv.MarkovEnv):
    """
        Individuals wander around randomly when they are not in couples. Upon coming into contact with a suitable partner, there is a chance the two individuals will couple together. When this happens, the two individuals no longer move around, they stand next to each other holding hands as a representation of two people in a sexual relationship.
        """
    def get_pre(self, agent, n_census):
        return markov.MarkovPre(TRANS)

    def restore_agent(self, agent_json):
        new_agent = Person(name=agent_json["name"], infected=agent_json["infected"], infection_length=agent_json["infection_length"], coupling_tendency=agent_json["coupling_tendency"], test_frequency=agent_json["test_frequency"], commitment=agent_json["commitment"], condom_use=agent_json["condom_use"], coupled=agent_json["coupled"], coupled_length=agent_json["coupled_length"], known=agent_json["known"])
        self.add_agent_to_grid(new_agent, agent_json)

