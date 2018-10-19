# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@authors: Brandon Logan
    Gene Callahan
Implements Thomas Schelling's segregation model.
An agent moves when she finds herself to be "too small"
of a minority in a particular neighborhood.
"""


import indra.vector_space as vs
import indra.vs_agent as va
import indra.grid_env as grid

MOVE = True
STAY = False
FEMALE = vs.X
MALE = vs.Y
FEM_PRE = vs.VectorSpace.X_PRE
MALE_PRE = vs.VectorSpace.Y_PRE
FEM_AGENT = "Woman"
MALE_AGENT = "Man"
AGENT_TYPES = {FEMALE: FEM_AGENT, MALE: MALE_AGENT}
TOL=0.5

class PartyAgent(va.VSAgent):
    """
    An agent that moves location based on its neighbors' types
    """
    def __init__(self, name, goal, tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, max_move=max_move, max_detect=max_detect)
        self.tolerance = tol
        self.stance = None
        self.orientation = None
        self.visible_pre = None
        self.happy = True
        self.timesWillingToMove = 100

    def eval_env(self, other_pre):
        """
        Use the results of surveying the env to decide what to do.
        """
        # no neighbors, we move:
        if other_pre.equals(vs.VectorSpace.NULL_PRE):
            self.happy = False
            return MOVE

        # otherwise, see how we like the hood
        # count the percentage of opposite sex
        num_opp_sex = 0
        total_people = 1
        for agent in self.neighbor_iter():
            total_people += 1
            if type(agent) != type(self):
                num_opp_sex += 1
        opp_sex_percentage = num_opp_sex / total_people

        if opp_sex_percentage <= self.tolerance:
            self.happy = True
            return STAY
        else:
            self.happy = False
            return MOVE

    def respond_to_cond(self, eval_vars=None):
        """
        If we don't like the neighborhood, we jump to a random empty cell.
        """
        numMoves = 0
        while not self.happy and numMoves < self.timesWillingToMove:
            self.move_to_empty()
            numMoves += 1
            num_opp_sex = 0
            total_people = 1
            for agent in self.neighbor_iter():
                total_people += 1
                if type(agent) != type(self):
                    num_opp_sex += 1
            opp_sex_percentage = num_opp_sex / total_people
            if opp_sex_percentage <= self.tolerance:
                self.happy = True
            else:
                continue


    def visible_stance(self):
        """
        Our visible stance differs from our internal one.
        It is just our "color."
        """
        return self.visible_pre
    
    def to_json(self):
        safe_fields = super().to_json()
        
        safe_fields["orientation"] = self.orientation
        safe_fields["visible_pre"] = self.visible_pre.to_json()
        safe_fields["tolerance"] = self.tolerance
        
        return safe_fields
        
    def from_json_preadd(self, agent_json):
        super().from_json_preadd(agent_json)
        
        self.orientation = agent_json["orientation"]
        self.visible_pre.from_json(agent_json["visible_pre"])
        self.tolerance = agent_json["tolerance"]


class Man(PartyAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, tol=TOL, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, tol,
                         max_move=max_move, max_detect=max_detect)
        self.orientation = MALE
        self.visible_pre = MALE_PRE
        self.stance = vs.stance_pct_to_pre(self.tolerance, MALE)
        
    def to_json(self):
        safe_fields = super().to_json()
        
        safe_fields["color"] = "Blue"
        
        return safe_fields


class Woman(PartyAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, tol=TOL, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, tol,
                         max_move=max_move, max_detect=max_detect)
        self.orientation = FEMALE
        self.visible_pre = FEM_PRE
        self.stance = vs.stance_pct_to_pre(self.tolerance, FEMALE)
        
    def to_json(self):
        safe_fields = super().to_json()
        
        safe_fields["color"] = "Red"
        
        return safe_fields


class PartyEnv(grid.GridEnv):
    """
    The segregation model environment, mostly concerned with bookkeeping.
    """

    def __init__(self, name, width, height, torus=False,
                 model_nm="party", props=None):

        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, props=props)
        self.plot_title = name
        # setting our colors adds varieties as well!
        self.set_agent_color()
        
        self.num_moves = 0
        self.move_hist = []
        self.menu.view.del_menu_item("v")  # no line graph in this model

    def move_to_empty(self, agent, grid_view=None):
        super().move_to_empty(agent, grid_view)
        self.num_moves += 1

    def census(self, disp=True):
        """
        Take a census recording the number of moves.
        """
        self.move_hist.append(self.num_moves)
        self.user.tell("Moves per turn: " + str(self.move_hist))
        self.num_moves = 0

    def record_results(self, file_nm):
        """
        """
        f = open(file_nm, 'w')
        for num_moves in self.move_hist:
            f.write(str(num_moves) + '\n')
        f.close()

    def set_agent_color(self):
        self.set_var_color(AGENT_TYPES[MALE], 'b')
        self.set_var_color(AGENT_TYPES[FEMALE], 'r')
        
    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["plot_title"] = self.plot_title
        safe_fields["move_hist"] = self.move_hist
        
        return safe_fields
        
    def from_json(self, json_input):
        super().from_json(json_input)
        self.plot_title = json_input["plot_title"]
        self.move_hist = json_input["move_hist"]
        
    def restore_agent(self, agent_json):     
        color = agent_json["color"]
        if color == "Blue":            
            new_agent = Man(agent_json["name"],
                                 agent_json["goal"],
                                 max_move=agent_json["max_move"], 
                                 max_detect=agent_json["max_detect"])
        if color == "Red":            
            new_agent = Woman(agent_json["name"],
                                 agent_json["goal"],
                                 max_move=agent_json["max_move"], 
                                 max_detect=agent_json["max_detect"])
            
        self.add_agent_to_grid(new_agent, agent_json)
