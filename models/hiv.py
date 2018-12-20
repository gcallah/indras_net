import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import indra.display_methods as disp
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

STATE_MAP = {N: NORTH, S: SOUTH, E: EAST, W: WEST}

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
        initiative: int, only the person with smaller value takes initiative
            to couple
        infected: boolean indicating if a person is infected with HIV
        known: boolean indicating if a person is aware of the HIV infection
        infection_length: int indicating how long this person has been
            infected with HIV
        coupling_tendency: likelihood that this person has sex (0-10)
        condom_use: chance that this person uses a condom (0-10)
        test_frequency: frequency that this person checks HIV status (0-2)
        commitment: how long sexual relationships lasts for this person
            (1-200)
        """
    def __init__(self, name, infected, infection_length, initiative,
                 coupling_tendency, condom_use, test_frequency, commitment,
                 coupled=False, coupled_length=0, known=False):
        init_state = random.randint(0, 3)
        super().__init__(name, "wandering around", NSTATES, init_state)
        self.coupled = coupled
        self.couple_length = coupled_length
        self.partner = None
        self.initiative = initiative
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
            if self.infected is True:
                if self.known is True:
                    self.ntype = POZ_NTYPE
                else:
                    self.ntype = UKP_NTYPE
            else:
                self.ntype = NEG_NTYPE
        else:
            if self.infected is True:
                if self.known is True:
                    self.ntype = POZ_NTYPE_C
                else:
                    self.ntype = UKP_NTYPE_C
            else:
                self.ntype = NEG_NTYPE_C
        if old_type is not 'Person' and self.ntype != old_type:
            self.env.change_agent_type(self, old_type, self.ntype)
        # print(self.name, "has ntype", self.ntype)

    def couple(self):
        for person in self.neighbor_iter():
            if person.coupled is False and person.initiative > self.initiative:
                if 10 * random.random() < person.coupling_tendency:
                    self.coupled = True
                    self.partner = person
                    person.coupled = True
                    person.partner = self
                    # print(self.name, "has been coupled with", person.name)
                    break

    def infect(self):
        if (self.coupled is True and self.infected is True and
                self.known is False and self.partner.infected is False):
            if (10 * random.random() > self.condom_use or
                    10 * random.random() > self.partner.condom_use):
                if 100 * random.random() < INFECTION_CHANCE:
                    self.partner.infected = True
                    # print(self.name, "has infected", self.partner.name)

    def preact(self):
        # print(self.name, "is preacting")
        if self.coupled is False:
            if 10 * random.random() < self.coupling_tendency:
                self.couple()
        if self.coupled is True:
            # update partner after restored
            if self.partner is not None:
                self.partner.partner = self
            self.infect()
            self.partner.infect()

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

    def act(self):
        # print(self.name, "is acting")
        if self.coupled is False:
            super().act()
            self.state = self.next_state
            self.move(self.state)

    def test(self):
        if (2 * random.random() < self.test_frequency and
                self.infected is True and self.known is False):
            self.known = True
            # print(self.name, "has been tested positive")
            if self.infection_length > SYMPTOMS_SHOW:
                if random.random() <= SYMPTOMS_SHOW_PROB:
                    self.known = True
                    # print(self.name, "has developed symptoms")

    def uncouple(self):
        if self.coupled is True:
            if (self.couple_length > self.commitment or
                    self.couple_length > self.partner.commitment):
                # print(self.name, "has been uncoupled with", self.partner.name)
                self.coupled = False
                self.couple_length = 0
                self.partner.coupled = False
                self.partner.couple_length = 0
                self.partner.partner = None
                self.partner = None

    def postact(self):
        # print(self.name, "is postacting")
        if self.infected is True:
            self.infection_length += 1
        if self.coupled is True:
            self.couple_length += 1
        self.test()
        self.uncouple()
        self.update_ntype()
        # print(self.name, "has ntype", self.ntype)
        
    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["ntype"] = self.ntype
        safe_fields["coupled"] = self.coupled
        safe_fields["coupled_length"] = self.couple_length
        safe_fields["initiative"] = self.initiative
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
        Individuals wander around randomly when they are not in couples.
        Upon coming into contact with a suitable partner, there is a chance
        the two individuals will couple together. When this happens, the
        two individuals no longer move around, they stand next to each other
        holding hands as a representation of two people in a sexual
        relationship.
        """
    def get_pre(self, agent, n_census):
        return markov.MarkovPre(TRANS)

    def set_agent_color(self):
        self.set_var_color(NEG_NTYPE, disp.MAGENTA)
        self.set_var_color(POZ_NTYPE, disp.BLACK)
        self.set_var_color(UKP_NTYPE, disp.YELLOW)
        self.set_var_color(NEG_NTYPE_C, disp.GREEN)
        self.set_var_color(POZ_NTYPE_C, disp.BLUE)
        self.set_var_color(UKP_NTYPE_C, disp.RED)
    
    def restore_agent(self, agent_json):
        new_agent = Person(name=agent_json["name"],
                           infected=agent_json["infected"],
                           infection_length=agent_json["infection_length"],
                           initiative=agent_json["initiative"],
                           coupling_tendency=agent_json["coupling_tendency"],
                           test_frequency=agent_json["test_frequency"],
                           commitment=agent_json["commitment"],
                           condom_use=agent_json["condom_use"],
                           coupled=agent_json["coupled"],
                           coupled_length=agent_json["coupled_length"],
                           known=agent_json["known"])
        self.add_agent_to_grid(new_agent, agent_json)
