'''
fashion_markov_model.py
A fashion model that includes followers and hipsters
changing fasions based on each other's choices.

Concieved as a Markov process.
'''

import indra.display_methods as disp
import indra.menu as menu
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import numpy as np

X = 0
Y = 1

# agent condition strings
REDHIPSTER = "Red-Wearing Hipster"
BLUEHIPSTER = "Blue-Wearing Hipster"
REDFOLLOWER = "Red-Wearing Follower"
BLUEFOLLOWER = "Blue-Wearing Follower"

HR = 0
HB = 1
FR = 2
FB = 3

STATE_MAP = { HR: REDHIPSTER, HB: BLUEHIPSTER, FR: REDFOLLOWER, FB: BLUEFOLLOWER }

NSTATES = 4
'''
Default response is not seeing any agent about cell.
No change in fashion.
'''
DEF_TRANS = "1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1"

class Hipster(ma.MarkovAgent):
    '''
    Hipsters begin red.
    '''
    def __init__(self, name, goal, max_move,var):
        super().__init__(name, "Don't look like Follower!", NSTATES, HR)
        self.state = HR
        self.ntype = STATE_MAP[HR]
        self.next_state = None

        # Effect of eval_env.
    def set_state(self, new_state):
        '''
        Set Hipster's new type.
        '''
        old_type = self.ntype
        self.state = new_state
        self.ntype = STATE_MAP[new_state]
        self.env.change_agent_type(self, old_type, self.ntype)
            # Unlike the forest fire model, we don't here update environment's cell's
            # transition matrices. This is because the cell's transition matrix depends
            # on all the agents near it, not just one.

    def postact(self):
        '''
        Set our type to next_state.
        '''
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None

        return self.pos

class Follower(ma.MarkovAgent):
    '''
    Followers begin blue.
    '''
    def __init__(self, name, goal, max_move,var):
        super().__init__(name, "Look like Hipster!", NSTATES, FB)
        self.state = FB
        self.ntype = STATE_MAP[FB]
        self.next_state = None

    def set_state(self, new_state):
        '''
        Set Hipster's new type.
        '''
        old_type = self.ntype
        self.state = new_state
        self.ntype = STATE_MAP[new_state]
        self.env.change_agent_type(self, old_type, self.ntype)
            # Unlike the forest fire model, we don't here update environment's cell's
            # transition matrices. This is because the cell's transition matrix depends
            # on all the agents near it, not just one.

    def postact(self):
        '''
        Set our type to next_state.
        '''
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None

        return self.pos


class Society(menv.MarkovEnv):
    def __init__(self, name, width, height, torus=False,
                model_nm="FashionModel", preact=False, postact=True):
        '''
        Create a new markov env
        '''
        super().__init__("Fashion Model", width, height, DEF_TRANS, torus=False, model_nm=model_nm, preact=False, postact=True)
        self.plot_title = "Metropolitan Fashion Scene"

        self.set_var_color(REDHIPSTER, disp.RED)
        self.set_var_color(BLUEHIPSTER, disp.BLUE)
        self.set_var_color(REDFOLLOWER, disp.GREEN)
        self.set_var_color(BLUEFOLLOWER, disp.CYAN)

    def get_pre(self, agent):
        cell = self._get_cell(agent.pos[X], agent.pos[Y])
        neighborhood = self.neighbor_iter(x=agent.pos[X],y=agent.pos[Y],distance=1, moore=True, view=None)

        numRH, numBH = 0, 0
        numRF, numBF = 0, 0
        for agent in neighborhood:
            if agent.state == HR:
                numRH +=1
            elif agent.state == HB:
                numBH +=1
            elif agent.state == FR:
                numRF +=1
            else:
                numBF +=1
        total = numRH + numBH + numRF + numBF

            # If neighborhood is empty, we don't want to divide by zero!
        if total == 0:
            total = 1

        rh = float(numRH/total)
        bh = float(numBH/total)

        rf = float(numRF/total)
        bf = float(numBF/total)

            # THE TRANSITION MATRIX
            # See documentation if this is confusing
        str_trans = str(1-bf) + " " + str(bf) + " 0 0;" + str(rf) + " " + str(1-rf) + " 0 0;" + "0 0 " + str(rh) + " " + str(1-rh) + ";" + "0 0 " + str(1-bh) + " " + str(bh)

        coords = (agent.pos[X],agent.pos[Y])
        super().set_trans(coords, markov.from_matrix(np.matrix(str_trans)))
        return cell.trans_matrix
