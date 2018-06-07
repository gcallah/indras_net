# -*- coding: utf-8 -*-

import indra.display_methods as disp
import indra.grid_agent as ga
import indra.grid_env as ge
import indra.user as user
from math import floor

X = 0
Y = 1

# agent condition strings
BLACK = "Black"
WHITE = "White"

# states
B = 0
W = 1

STATE_MAP = { B: BLACK, W: WHITE }

MAX_SAND = 4
FULL_NEIGHBORHOOD = 4

NSTATES = 2
        
# Some rule dictionaries:
RULE30 = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

class WolframAgent(ga.GridAgent):
    """
    An agent that looks agents above it and react
    """
    def __init__(self, name, goal, cell, mark = False):
        super().__init__(name, goal)
        self.cell = cell
        self.state = W
        self.ntype = STATE_MAP[self.state]
        self.marked = mark
        self.is_active = False

    def act(self):
        #make sure we only update the row we need to
        (x, y) = self.pos
        if y == self.env.height - 1 - self.env.period:
            self.is_active = True
        #Trace the marked agents
        if self.marked:
            self.show_stats()
        if not self.is_active:
            return
        #Find the information needed
        check_list = [(x - 1, y + 1),(x, y + 1), (x + 1, y + 1)]
        result = [W, W, W]
        for i in range(len(check_list)):
            for neighbor in self.neighbor_iter(moore=False, save_hood=True):
                if neighbor.pos == check_list[i]:
                    result[i] = neighbor.state
                    break
        
        #Make change
        self.state = self.env.check_rules(tuple(result))
        self.is_active = False

    def postact(self):
        """
        Here we are going to set our type.
        """
        new_type = STATE_MAP[self.state]
        if self.ntype != new_type:
            old_type = self.ntype
            self.set_type(new_type)
            self.env.change_agent_type(self, old_type, new_type)
            
    def show_stats(self):
        print("-----------------")
        print("Period: ", self.env.period)
        print("Position: ", self.pos)
        print("State: ", self.state)
        print("Type: ", self.ntype)
        print("Active: ", self.is_active)
        print("-----------------")


class WolframEnv(ge.GridEnv):
    """
    An environment for updating agents from the top to the bottom.
    """

    def __init__(self, name, width, height, model_nm=None, props=None, 
                 rules=RULE30):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, postact=True, props=props)
        
        self.rules = rules
#        for i in STATE_MAP:
#            for j in STATE_MAP:
#                for k in STATE_MAP:
#                    self.rules[(i,j,k)] = None
                    
        self.set_var_color(BLACK, disp.BLACK)
        self.set_var_color(WHITE, disp.WHITE)

        center_x = floor(self.width // 2)
        top_y = self.height-1
        print("center top = %i, %i" % (center_x, top_y))

        #self.set_rules()

        for cell in self:
            (x, y) = cell.coords
            agent = WolframAgent("Grid", "Show color", cell)
            self.add_agent(agent, position=False)
            if x == center_x and y == top_y:
                agent.state = B
                new_type = STATE_MAP[agent.state]
                old_type = agent.ntype
                agent.set_type(new_type)
                self.change_agent_type(agent, old_type, new_type)
                #agent.marked = True
                agent.is_active = False
#            if x == center_x - 1 and y == top_y - 1:
#                agent.marked = True
#            if x == center_x and y == top_y - 1:
#                agent.marked = True
#            if x == center_x + 1 and y == top_y - 1:
#                agent.marked = True        
        
    def check_rules(self, combo):
        return self.rules[combo]

    def step(self):
        super().step()
