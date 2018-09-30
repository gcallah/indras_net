
import random
import indra.markov_agent as ma
import indra.markov_env as menv

NSTATES = 4

avg_coupling_tendency = 5 # 0-10
avg_commitment = 20 # 0-200
avg_condom_use = 5 # 0-10
avg_test_frequency = 1 # 0-2

infection_chance = 50 # 0-100
symptoms_show = 200

class neg(ma,MarkovAgent):
    """
        An HIV-negative individual
    """
    def __init__(self, name, goal, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner):
        super().__init__(name, goal, NSTATES, init_state, max_detect=max_detect)
        
        self.coupling_tendency = avg_coupling_tendency
        self.commitment = avg_commitment
        self.condom_use = avg_condom_use
        self.test_frequency = avg_test_frequency

        self.coupled = False
        self.coupled_length = 0
        self.partner = None
    
    def preact(self):
        if self.coupled = True:
            self.coupled_length++

    def act(self):
        if self.coupled = False:
            super().act()
            self.state = self.next_state
            self.move(self.state)
        else:
            # uncouple

    def move(self, state):
        


class poz(neg):
    """
        An HIV-positive individual
    """
    def __init__(self, name, goal, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner, status_known, infection_length):
        super().__init__(name, goal, init_state, max_detect=1, SPEED, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner)
        status_known = False
        infection_length = random.randint(0, symptoms_show - 1)

    def preact(self):
        self.infection_length++

class People(menv.MarkovEnv):
    """
        Individuals wander around randomly when they are not in couples. Upon coming into contact with a suitable partner, there is a chance the two individuals will couple together. When this happens, the two individuals no longer move around, they stand next to each other holding hands as a representation of two people in a sexual relationship.
    """
    def get_pre(self, agent)
        trans_str = ""

