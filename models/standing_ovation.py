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

import indra.entity as ent
import indra.env as env

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
                 #, standard = 0.2 #standard could be set by user
                 ):
        super().__init__(name, goal)
        self.name = name
        self.goal = goal
        self.sitting = True #Everyone starts off sitting
        self.noise = 0.95
        self.standard = 0.2
        self.pressure = 0
        #Agent must have a first impression
        self.initial()

    # Initial reaction to the performance, which will elicit a reaction.
    def initial(self):
        ##maybe performance should be defined elsewhere?
        performance = random.uniform(0.0, 1.0)
        self.reaction(performance)

    def isSitting(self):
        return self.sitting == True

    def setState(self, new_state):
        self.sitting = new_state

    # Initial reaction to the performance
    # If the performance falls within the member's standards, the member will stand
    def reaction(self, performance):
        if (performance >= self.standard):
            self.setState(False)
            # Member is confronted with the pressure of his neighbors' states. If the choice falls within the noise range

    #Confront the audience member with a decision.
    #If pressure to stand exceeds 50%:
    #Generate a choice value
    #If choice value <= noise
    #the audience member chooses to copy what its neighbors are doing.
    def confront(self):
        if(pressure > 0.5):
            choice = random.uniform(0.0, 1.0)
            if (choice <= noise):
                self.sitting = neighbor_status

    def preact(self):
        standing_tot = 0
        neighbors_tot = 0
        for neighbor in self.neighbor_iter():
            standing_tot += 1
            neighbors_tot += 1
        self.pressure = total_stand / neighbors_tot

        print("I am agent" + self.name + "and I am preacting")

    #With the audience member now having some type of pressure
    #Confront the audience member with the choice of sitting or standing
    def act(self):
        self.confront()
        print("I am agent" + self.name + "and I am reacting to the performance")

    # def postact(self):
    #     print("I am agent" + self.name + "and sitting = ", self.sitting)

# Maybe I'll use something like this later? Maybe a paid audience member
# class Gozer(BasicAgent):
#     """
#     A silly agent that destroys others, for demo purposes
#     """
#
#     def __init__(self):
#         """
#         Init Gozer with slightly different params.
#         """
#         super().__init__(name="Gozer the Destructor", goal="Destroy!")
#
#     def postact(self):
#         """
#         Check to see if we have wiped everyone out.
#         """
#         e = self.env
#         if len(e.agents) == 1:
#             print("Gozer the Destructor has destroyed all!!")
#         else:
#             for agent in e.agents:
#                 if agent is not self:
#                     e.agents.remove(agent)
#                     print("Gozer has destroyed "
#                           + agent.name + "!")
#                     return


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

    def restore_agents(self, json_input):
        for agent in json_input["agents"]:
            self.add_agent(AudienceAgent(agent["name"],
                                      agent["goal"],
                                      agent["noise_level"]))
