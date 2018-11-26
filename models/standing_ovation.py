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
        name: name of the agent (agent1, agent2, etc.)
        goal: the current goal of each member, useful for testing their states but useless otherwise
        state: a string indicating whether the member is sitting ("SITTING") or standing ("STANDING")
        standard: a double that determines whether an audience member is impressed by the performance or not
        changed: a boolean that is True whenever an agent caves in to peer pressure and changes their state
        pressure: a double representing the amount of pressure felt by the agent, pressure being how many neighbors have a different state
    Functions:
        reaction: Checks whether the performance was up to the agent's standards and changes state accordingly
        isSitting: returns a boolean. Checks whether agent is sitting
        cycleState: changes agent state from sitting->standing or vice versa
        confront: checks agent's pressure and changes state if the pressure is too great
        wasPressured: prints out whether the agent changed states during that step. Useful for debugging.
    """
    def __init__(self, name, goal):
        super().__init__(name, goal, NSTATES, SITTING)
        self.name = name
        self.goal = goal
        self.state = SITTING
        self.standard = random.uniform(0.0, 1.0)
        self.ntype = self.state
        self.next_state = STANDING
        self.changed = False
        self.pressure = 0
        self.reaction()

    #Initial impression of the show
    def reaction(self):
        if (performance >= self.standard):
            self.cycleState()
            #print(self.name, "I liked the performance")

    def isSitting(self):
        return self.state == SITTING

    def cycleState(self):
        prev_state = self.state
        self.state = self.next_state
        self.ntype = self.state
        self.next_state = prev_state

    def confront(self):
        if (self.pressure > 0.5):
            self.cycleState()
            self.changed = True

    def wasPressured(self):
        if (self.changed):
            print("I was pressured into changing my state")
        else:
            print("I resisted the pressure!")
        self.goal = self.state

    def preact(self):
        diff_num = 0
        neighbors_num = 0
        for neighbor in self.neighbor_iter():
            if(neighbor.state != self.state):
                diff_num += 1
            neighbors_num += 1
        if(neighbors_num != 0):
            self.pressure = diff_num / neighbors_num

    def act(self):
        self.preact()   #This really shouldn't be here but I'm not able to get the preact to run.
                        #Ideally the preact would trigger by itself before the act, but I can only get the preact()
                        #to run by calling it from act()
        self.changed = False
        self.confront()
        self.wasPressured()

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["state"] = self.state
        safe_fields["ntype"] = self.ntype
        safe_fields["next_state"] = self.next_state

        return safe_fields

    def from_json_preadd(self, json_input):
        super().from_json_preadd(json_input)
        self.state = json_input["state"]
        self.ntype = json_input["ntype"]
        self.next_state = json_input["next_state"]

class Auditorium(menv.MarkovEnv):
    def __init__(self, width, height, #noise,
                 torus=False, model_nm="standing_ovation", act=True,
                 props=None):
        """
                Create a new Auditorium where the audience will exist.
                Args:
                    width, height: The grid dimensions (keep in mind number of audience members = width * height)
         """
        super().__init__("Auditorium", width, height,
                         torus=False, model_nm=model_nm,
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