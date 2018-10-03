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
        isSitting: returns a boolean. Checks whether agent is sitting
        setState: takes a boolean state as an argument. Sets agent state to the new state
        reaction: Checks whether the performance was up to the agent's standards
    """

    def __init__(self, name, goal, sitting = True, noise = 0.95, standard = 0.2):
        super().__init__(name, goal, sitting, noise)
        self.name = name
        self.goal = goal
        self.sitting = sitting
        self.noise = noise
        self.standard = standard

    def isSitting(self):
        return self.sitting == True

    def setState(self, new_state):
        self.sitting = new_state

    # Initial reaction to the performance
    # If the performance falls within the member's standards, the member will stand
    def reaction(self, performance):
        if (performance >= self.standard):
            setState(False)
            # Member is confronted with the pressure of his neighbors' states. If the choice falls within the noise range

    #Generate the choice value. If the choice value falls within the noise range,
    #the audience member chooses to copy what its neighbors are doing.
        #still haven't implemented confrontation yet
    def confront(self, neighbor_status):
        choice = random.uniform(0.0, 1.0)
        if (choice <= noise):
            self.sitting = neighbor_status

    def preact(self):
        print("I am agent" + self.name + "and I am preacting")

    #Generate the performance value. The higher it is, the likelier it is for audience members to stand up
    #After that, see how the audience member reacts
    def act(self):
        performance = random.uniform(0.0, 1.0)
        reaction(performance)
        print("I am agent" + self.name + "and I am acting")

    def postact(self):
        print("I am agent" + self.name + "and I am postacting")

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


class AudienceEnv(menv.MarkovEnv):
    """
    This environment represents the entire audience
    Arguments:
        width: int
        height: int
    """

    def __init__(self, width, height, model_nm=None, props=None):
        super().__init__("St Ovation Env",
                         width,
                         height,
                         preact=True,
                         postact=True,
                         model_nm=model_nm,
                         props=props)

        self.plot_title = "The Audience"

    def preact_loop(self):
        print("Preact loop: demonstrating backwards looping")
        for agent in reversed(self.agents): ##What is self.agents? Where does it come from?
            print("Agent: " + agent.name + "agent sitting:" + agent.sitting)

    def restore_agents(self, json_input):
        for agent in json_input["agents"]:
            self.add_agent(AudienceAgent(agent["name"],
                                      agent["goal"],
                                      agent[True],
                                      agent[0.95],
                                      agent[0.2]))
