# -*- coding: utf-8 -*-

import os
import indra.display_methods as disp
import indra.grid_agent as ga
import indra.grid_env as ge
from math import floor
import ast
import logging

X = 0
Y = 1

# agent condition strings
BLACK = "Black"
WHITE = "White"

# states
B = 1
W = 0

STATE_MAP = { B: BLACK, W: WHITE }
        
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

#Convert tuples to strings
new_dic = {}
for i in RULE30:
    new_dic[str(i)] = RULE30[i]
RULE30 = new_dic

class WolframAgent(ga.GridAgent):
    """
    An agent that looks at agents above it and reacts
    """
    def __init__(self, name, goal, cell=None):
        super().__init__(name, goal, cell=cell)
        self.state = W
        self.ntype = STATE_MAP[self.state]
        self.is_active = False

    def act(self):
        #make sure we only update the row we need to
        (x, y) = self.pos
        if y == self.env.height - 1 - self.env.period:
            self.is_active = True
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
            
    def to_json(self):
        safe_fields = super().to_json()

        safe_fields["state"] = self.state
        safe_fields["is_active"] = self.is_active
        
        return safe_fields
    
    def from_json(self, json_input):
        super().from_json(json_input)
        
        self.state = json_input["state"]
        self.is_active = json_input["is_active"]

class WolframEnv(ge.GridEnv):
    """
    An environment for updating agents from the top to the bottom.
    """

    def __init__(self, name, width, height, model_nm=None, props=None, 
                 rule_id=30):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, postact=True, props=props)
        
        try:
            base_dir = props["base_dir"]
        except:
            base_dir = ""
        
        path = os.path.join(base_dir, "wolfram/wolfram_rules.txt")
        
        try:
            self.rules = self.read_wolfram_rules(path)[rule_id]
        except:
            self.rules = RULE30
            logging.info("Rule dictionary not found. Using the default rule.")
                    
        self.set_agent_color()

        center_x = floor(self.width // 2)
        top_y = self.height-1
        print("center top = %i, %i" % (center_x, top_y))

        for cell in self:
            (x, y) = cell.coords
            agent = WolframAgent("Cell" + str((x, y)), "Show color", cell)
            self.add_agent(agent, position=False)
            if x == center_x and y == top_y:
                agent.state = B
                agent.postact()
                agent.is_active = False
        
    def check_rules(self, combo):
        return self.rules[str(combo)]

    def step(self):
        super().step()
        
    def read_wolfram_rules(self,file):
        rules_sets = []
        with open(file,"r") as f:
            all_rules = f.readlines()
            for i in all_rules:
                rules_sets.append(ast.literal_eval(i))

        return rules_sets
    
    def to_json(self):
        safe_fields = super().to_json()
        
        safe_fields["rules"] = self.rules
        
        return safe_fields
    
    def from_json(self, json_input):
        super().from_json(json_input)
        self.rules = json_input["rules"]
        
        self.set_agent_color()
    
    def restore_agent(self, agent_json):
        new_agent = WolframAgent(agent_json["name"], agent_json["goal"])
        self.add_agent_to_grid(new_agent, agent_json)
            
    def add_agent_to_grid(self, agent, agent_json):
        super().add_agent_to_grid(agent, agent_json)
        agent.postact()
        
    def print_env(self):
        for row in self.grid:
            for cell in row:
                print(cell.contents, end="")
            print()
            
    def set_agent_color(self):
        self.set_var_color(BLACK, disp.BLACK)
        self.set_var_color(WHITE, disp.WHITE)