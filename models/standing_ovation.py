"""
standing_ovation.py
This model simulates how a standing ovation spreads
across an audience. It'll first model whether
a performance gets a standing ovation from at least a
few individual first, and then model how the pressure to
stand or sit affects the rest of the audience.
"""
import indra.display_methods as disp
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv
import random

#Audience states
SITTING = "Sitting"
STANDING = "Standing"
NSTATES = 2

performance = random.uniform(0.0, 1.0)
class AudienceAgent(ma.MarkovAgent):
    """
    A member of an audience that will decide whether to remain sitting or stand

    Attributes:
        sitting: a boolean indicating whether the member is sitting (T) or standing (F)
        noise: a double that determines the odds of the member following the crowd once
            confronted to make a choice
        standard: a double that determines the odds of the member enjoying the
            performance
    Functions:
        initial: initial reaction to performance. Makes the agent react to the performance
        isSitting: returns a boolean. Checks whether agent is sitting
        setState: takes a boolean state as an argument. Sets agent state to the new state
        reaction: Checks whether the performance was up to the agent's standards
        confront: Forces the agent to react to perceived pressure, will change state if pressure is too much
    """
    def __init__(self, name, goal):
        super().__init__(name, goal, NSTATES, SITTING)
        self.name = name
        self.goal = goal
        self.state = SITTING
        # how hard to please the agent is aka how high their standards are
        self.standard = random.uniform(0.0, 1.0)
        #self.ntype = self.state
        self.next_state = STANDING

        self.changed = False
        #Agent's first impression of the show
        self.reaction()

    def reaction(self):
        if (performance >= self.standard):
            self.cycleState()

    def isSitting(self):
        return self.state == SITTING

    def cycleState(self):
        prev_state = self.state
        self.state = self.next_state
        self.ntype = self.state
        self.next_state = prev_state

    # Confront the audience member with a decision.
        # If pressure to stand exceeds 50%:
        # the audience member chooses to copy what its neighbors are doing.
    def confront(self):
        if (self.pressure > 0.5):  # If the pressure is to great, you have a choice
            self.cycleState()
            self.changed = True  ##Delete later

    def preact(self):
        diff_num = 0
        neighbors_num = 0

        for neighbor in self.neighbor_iter():
            #print("I am iterating through my neighbors") ##for testing
            if(neighbor.state != self.state):
                diff_num += 1
            neighbors_num += 1
        print("neighbors_tot:", neighbors_num)
        self.pressure = 0.75 ##Temp
        if(neighbors_num != 0):
            self.pressure = diff_num / neighbors_num
        print("I am agent " + self.name + " and I am " + self.state + " [preact]")

    def act(self):
        self.preact()   #This really shouldn't be here but I'm not able to get the preact to run.
                        #Ideally the preact would trigger by itself before the act, but I can only get the preact()
                        #to run by calling it from act()
        self.changed = False ##For testing
        self.confront()
        print("I am agent " + self.name + " and I am " + self.state + " [act]")
        if(self.changed): ##For testing
            print("I was pressured into changing my state")
        else:
            print("I resisted the pressure!")

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["state"] = self.state
        #safe_fields["ntype"] = self.ntype
        safe_fields["next_state"] = self.next_state

        return safe_fields

    def from_json_preadd(self, json_input):
        super().from_json_preadd(json_input)
        self.state = json_input["state"]
        #self.ntype = json_input["ntype"]
        self.next_state = json_input["next_state"]

class Auditorium(menv.MarkovEnv):
    def __init__(self, width, height, #noise,
                 torus=False, model_nm="standing_ovation", act=True,
                 props=None):
        # Initialize model parameters
        super().__init__("Auditorium", width, height,
                         torus=False, model_nm=model_nm, #act=act,
                         props=props)
        #self.noise = noise
        self.plot_title = "An Auditorium"

    def set_agent_color(self):
        self.set_var_color(SITTING, disp.BLACK)
        self.set_var_color(STANDING, disp.RED)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["plot_title"] = self.plot_title

        return safe_fields

    def from_json(self, json_input):
        super().from_json(json_input)
        self.plot_title = json_input["plot_title"]

    def restore_agent(self, agent_json):
        new_agent = AudienceAgent(name=agent_json["name"])
        self.add_agent_to_grid(new_agent, agent_json)