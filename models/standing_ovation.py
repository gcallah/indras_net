"""
standing_ovation.py
This model simulates how a standing ovation spreads
across an audience. It'll first model whether
a performance gets a standing ovation from at least a
few individual first, and then model how the pressure to
stand or sit affects the rest of the audience.
"""
import random
import indra.display_methods as disp
import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as menv

SITTING = "Sitting"
STANDING = "Standing"
NSTATES = 2

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
    def __init__(self, name, goal, noise
                 #, standard = 0.2 #standard could be set by user maybe?
                 ):
        super().__init__(name, goal, NSTATES, SITTING)
        self.name = name
        self.goal = goal
        self.state = SITTING #Everyone starts off sitting
        self.next_state = STANDING
        self.ntype = self.state #Might have to keep this one and delete self.state, they're redundant
        self.noise = 0.75
        self.standard = 0.2
        self.pressure = 0

        self.changed = False #temp var to easily see whether agent changed state

        self.initial() #Agent must have a first impression

    # Initial reaction to the performance, which will elicit a reaction.
    def initial(self):
        ##maybe performance should be defined elsewhere?
        performance = random.uniform(0.0, 1.0)
        self.reaction(performance)

    def isSitting(self):
        return self.state == SITTING

    def cycleState(self):
        prev_state = self.state
        self.state = self.next_state
        self.ntype = self.state
        self.next_state = prev_state

        #print("self.env",self.env)
        #self.env.change_agent_type(self, prev_state, self.ntype)


    # Initial reaction to the performance
        # If the performance falls within the member's standard, the member will stand
    def reaction(self, performance):
        if (performance >= self.standard):
            self.cycleState()

    #Confront the audience member with a decision.
        #If pressure to stand exceeds 50%:
        #Generate a choice value
        #If choice value <= noise
        #the audience member chooses to copy what its neighbors are doing.
    def confront(self):
        choice = random.uniform(0.0, 1.0)
        if(self.pressure > 0.5): #If the pressure is to great, you have a choice
            if (choice <= self.noise): #If the agent is likely to follow the status quo
                self.cycleState()
                self.changed = True ##Delete later

    #I can't get the neighborhood to work, I have to get it implemented aaaaah
    def preact(self):
        different_tot = 0
        neighbors_tot = 0
        print("neighborhood:",self.neighborhood) ##for testing
        for neighbor in self.neighbor_iter():
            print("I am iterating through my neighbors") ##for testing
            if(neighbor.state != self.state):
                different_tot += 1
            neighbors_tot += 1
        print("neighbors_tot:", neighbors_tot)
        self.pressure = 0.75 ##Temp
        if(neighbors_tot != 0):
            self.pressure = different_tot / neighbors_tot
        print("I am agent " + self.name + " and I am " + self.state + " [preact]")

    #With the audience member now having some type of pressure
    #Confront the audience member with the choice of sitting or standing
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

    # def postact(self):
    #     print("I am agent" + st
        #self.name + "and sitting = ", self.sitting)

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
    """
    This environment represents the entire audience
    Arguments:
        width: int
        height: int
    """

    def __init__(self, width, height, model_nm="standing_ovation", props=None):
        #print("I'm in super init")
        super().__init__("Auditorium",
                         width,
                         height,
                         model_nm=model_nm,
                         props=props)
        self.plot_title = "The Audience"

    # def preact_loop(self):
    #     print("Preact loop: demonstrating backwards looping")
    #     for agent in reversed(self.agents): ##What is self.agents? Where does it come from?
    #         print("Agent: " + agent.name + "agent sitting:" + str(agent.sitting))
    def set_agent_color(self):
        # setting our colors adds varieties as well!
        self.set_var_color(SITTING, disp.BLACK)
        self.set_var_color(STANDING, disp.RED)

    def to_json(self):
        safe_fields = super().to_json()
        #safe_fields["state"] = self.state
        #safe_fields["ntype"] = self.ntype
        safe_fields["plot_title"] = self.plot_title
        #safe_fields["next_state"] = self.next_state

        return safe_fields

    def from_json(self, json_input):
        super().from_json(json_input)
        #self.state = json_input["state"]
        #self.ntype = json_input["ntype"]
        self.plot_title = json_input["plot_title"]
        #self.next_state = json_input["next_state"]

    def restore_agent(self, agent_json):
        new_agent = AudienceAgent(name=agent_json["name"],
                                  goal=agent_json["goal"],
                                  noise=agent_json["noise"])
        self.add_agent_to_grid(new_agent, agent_json)


