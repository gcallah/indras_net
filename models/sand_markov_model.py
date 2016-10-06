"""
sand_model.py
Abelian sand that has avalanches in interesting patterns.
"""
from math import floor
import numpy as np
import indra.display_methods as disp
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

MAX_SAND = 1
FULL_NEIGHBORHOOD = 4


class SandAgent(ma.MarkovAgent):
    """
    An agent that collects sand particles until its stack collapses
    onto its neighbors.
    """
    def __init__(self, name, goal, vlen, init_state, cell):
        super().__init__(name, goal, vlen, init_state)
        self.cell = cell
        self.state = init_state
        self.next_state = None
        self.ntype = str(self.state)

    def act(self):
        super().act()

        difference = self.next_state - self.state
        if(difference > 0):
            for i in range(difference):
                for neighbor in self.neighbor_iter(moore=False, save_hood=True):
                    if self.state > 0 and neighbor.state < self.state:
                        neighbor.add_grains(1)
                        self.state -= 1

    def postact(self):
        """
        Set our type to next_state.
        """
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None

    def set_state(self, new_state):
        """
        Set tree's new type.
        """
        old_type = self.ntype
        self.state = new_state
        self.ntype = str(self.state)
        #self.env.change_agent_type(self, old_type, self.ntype)

    def add_grains(self, amt):
        """
        Get some sand.
        """
        self.state += amt
        self.ntype += str(self.state)


class SandEnv(menv.MarkovEnv):
    """
    An environment for spilling sand all over the place.
    """

    def __init__(self, name, width, height, model_nm, max_pile_size):
        super().__init__(name, width, height, torus=False, matrix_dim=max_pile_size,
                         model_nm=model_nm, postact=True)

        self.max_pile_size = max_pile_size
        self.center_agent = None
        self.set_var_color('0', disp.BLACK)
        self.set_var_color('1', disp.MAGENTA)
        self.set_var_color('2', disp.BLUE)
        self.set_var_color('3', disp.CYAN)
        self.set_var_color('4', disp.RED)
        self.set_var_color('5', disp.YELLOW)
        self.set_var_color('6', disp.GREEN)

        center_x = floor(self.width // 2)
        center_y = floor(self.height // 2)
        print("center = %i, %i" % (center_x, center_y))

        for cell in self:
            (x, y) = cell.coords
            #       vLen contains the state of the agent
            #       the state is the number of grains of sand 
            #       in the SandAgent.
            agent = SandAgent("Grainy", "Hold sand", vlen=self.max_pile_size, init_state=0, cell=cell)
            self.add_agent(agent, position=False)
            if x == center_x and y == center_y:
                self.center_agent = agent

    def step(self):
        super().step()
        self.center_agent.add_grains(1)

    def get_pre(self, agent, n_census):
        
        """
        See documentation for how this is built,
        what effect it produces, and why it 
        produces it.
        """

        trans_matrix = markov.create_iden_matrix(self.max_pile_size)

        i=2
        j=i
        count=0.0

        """
        These while loops aren't a big drag.
        It makes a lower triangular matrix of size ~vlen**2,
        and we ony cycle through at most 4 times in the
        innermost loop.
        """
        while(i<self.max_pile_size):
            while(1<=j):
                if(str(j) in n_census):
                    while(n_census(str(j))>0):
                        count+=1
                        n_census[str(j)]-=1
                    trans_matrix[i,j] = (count/4)**(i+1/j)
                j-=1
            trans_matrix[i,i]= 1 - (count/4)
            i+=1
            j=i
            count=0

        return markov.from_matrix(trans_matrix)