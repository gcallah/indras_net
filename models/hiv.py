
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

NORMAL_TRANS =
INFECT_TRANS =

class Neg(ma.MarkovAgent):
    """
        An HIV-negative individual
    """
    def __init__(self, name, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner):
        super().__init__(name, 4, init_state, max_detect=max_detect)
        
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
            self.uncouple()

    def move(self, state):
        x = self.pos[0]
        y = self.pos[1]
        if state == 0:
            if self.env.is_cell_empty(x, y+1):
                self.env.move(self, x,y+1)
        elif state == 1:
            if self.env.is_cell_empty(x, y-1):
                self.env.move(self, x,y-1)
        elif state == 2:
            if self.env.is_cell_empty(x-1, y):
                self.env.move(self, x-1,y)
        else:
            if self.env.is_cell_empty(x+1, y):
                self.env.move(self, x+1,y)
            
    def uncouple(self):
        if (self.couple_length > self.commitment) || (self.couple_length > self.partner.commitment):
            self.coupled = False
            self.couple_length = 0
            self.partner.coupled = False
            self.partner.couple_length = 0
            self.partner.partner = None
            self.partner = None


class Poz(neg):
    """
        An HIV-positive individual
    """
    def __init__(self, name, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner, status_known, infection_length):
        super().__init__(name, init_state, max_detect=1, SPEED, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner)
        status_known = False
        infection_length = random.randint(0, symptoms_show - 1)

    def preact(self):
        self.infection_length++
        if self.infection_length > symptoms_show:
            self.status_known = True

    def postact(self):
        if self.coupled = Ture && self.status_known = False:
            self.infect()
        self.test()

    def infect(self):
        if (random.randint(0, 10) > self.condom_use) && (random.randint(0,10) > self.partner.condom_use && random.randint(0, 10) > infection_chance)
            self.partner.converse()

    def converse(self):
        pass

    def test(self):
        if (random.randint(0, 52) < self.test_frequency) && self.status_known == False:
            self.status_known = True

class Individual(ma.MarkovAgent):
    def __init__(self, name, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner):
        super().__init__(name, 4, init_state, max_detect=max_detect)
        
        self.coupling_tendency = avg_coupling_tendency
        self.commitment = avg_commitment
        self.condom_use = avg_condom_use
        self.test_frequency = avg_test_frequency
        
        self.coupled = False
        self.coupled_length = 0
        self.partner = None


class People(menv.MarkovEnv):
    """
        Individuals wander around randomly when they are not in couples. Upon coming into contact with a suitable partner, there is a chance the two individuals will couple together. When this happens, the two individuals no longer move around, they stand next to each other holding hands as a representation of two people in a sexual relationship.
    """
    
    def __init__(self, width, height, ini_ppl, avg_coup_tend, avg_test_freq, avg_commitment, avg_condom_use, torus=False, model_nm="HIV", preact=True, props=None)
        super().__init__("HIV", width, height, NORMAL_TRANS, torus=False, model_nm=model_nm, preact=preact, props=props)
        
        self.ini_ppl = ini_ppl
        self.avg_coup_tend = avg_coup_tend
        self.avg_test_freq = avg_test_freq
        self.avg_commitment = avg_commitment
        self.avg_condom_use = avg_condom_use

        self.normal = markov.MarkovPre(NORMAL_TRANS)
        self.infect = markov.MarkovPre(INFECT_TRANS)

    def get_pre(self, agent):
        trans_str = ""
        
        d, total = self.dir_info(agent)
        
        if(type(agent) == Poz):
            trans_str += self.poz_trans(d, total)
        else:
            trans_str += self.neg_trans(d, total)
        
        trans_matrix = markov.from_matrix(np.matrix(trans_str))
        return trans_matrix

    def dir_info(self, agent):
        pass

    def neg_trans(self, d, total):
        pass

    def poz_trans(self, d, total):
        pass

    
    def set_agent_color(self):
        self.set_var_color(BURNED_OUT, disp.BLACK)
        self.set_var_color(ON_FIRE, disp.RED)
        self.set_var_color(HEALTHY, disp.GREEN)
        self.set_var_color(NEW_GROWTH, disp.CYAN)
    
    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["density"] = self.density
        safe_fields["plot_title"] = self.plot_title
        safe_fields["normal"] = self.normal.to_json()
        safe_fields["fire"] = self.fire.to_json()
        
        return safe_fields
    
    def from_json(self, json_input):
        super().from_json(json_input)
        self.density = json_input["density"]
        self.plot_title = json_input["plot_title"]
        self.normal.from_json(json_input["normal"])
        self.fire.from_json(json_input["fire"])
    
    def restore_agent(self, agent_json):
        new_agent = Tree(name=agent_json["name"])
        self.add_agent_to_grid(new_agent, agent_json)
