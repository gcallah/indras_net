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
import indra.markov_agent as ma
import indra.markov_env as menv

SITTING = "Sitting"
STANDING = "Standing"
NSTATES = 2


class Member(ma.MarkovAgent):
    """
    #     A member of an audience that will decide whether to remain sitting or stand
    #     Attributes:
    #         name: name of the agent (agent1, agent2, etc.)
    #         goal: the current goal of each member,
    #             useful for testing their states but useless otherwise
    #         noise: a double representing how good the performance was
    #         state: a string indicating whether the member is
    #             sitting ("SITTING") or standing ("STANDING")
    #         standard: a double that determines whether an audience member is
    #             impressed by the performance or not. Subject to change as
    #             there currently might be too much variance.
    #         next_state: always equal to the state the agent doesn't have
    #         changed: a boolean that is True whenever an agent caves in to
    #             peer pressure and changes their state
    #         pressure: a double representing the amount of pressure felt by
    #             the agent, pressure being how many neighbors have a different state
    #     Functions:
    #         reaction: Checks whether the performance was up to
    #             the agent's standards and changes state accordingly
    #         is_sitting: returns a boolean. Checks whether agent is sitting
    #         cycle_state: changes agent state from sitting->standing or vice versa
    #         set_state: lets the environment know that the agent changed states
    #         confront: checks agent's pressure and changes state
    #             if the pressure is too great
    #         was_pressured: prints out whether the agent changed states
    #             during that step. Useful for debugging.
    #     """
    def __init__(self, name, goal, noise):
        super().__init__(name, goal, 2, SITTING)
        self.name = name
        self.goal = goal
        self.noise = noise
        self.state = SITTING
        self.standard = random.uniform(0.4, 1.0)
        self.ntype = self.state
        self.next_state = STANDING
        self.changed = False
        self.pressure = 0

        self.reaction()

    def reaction(self):
        if (self.noise >= self.standard):
                self.cycle_state()
                # print(self.name, "I liked the performance")

    def is_sitting(self):
        return self.state == SITTING

    def cycle_state(self):
        prev_state = self.state
        self.state = self.next_state
        self.ntype = self.state
        self.next_state = prev_state

    def set_state(self):
        self.cycle_state()
        self.env.change_agent_type(self, self.next_state, self.state)

    def confront(self):
        if (self.pressure > 0.5):
            self.set_state()
            self.changed = True

    def was_pressured(self):
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
        self.changed = False
        self.confront()
        # self.was_pressured()

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["ntype"] = self.ntype

        return safe_fields


class Auditorium(menv.MarkovEnv):
    def __init__(self, name, width, height, torus=False,
                 model_nm="standing_ovation", preact=True, props=None):
        """
        Create a new Auditorium where the audience will exist.
        Args:
            width, height: The grid dimensions
            (# of audience members = width * height)
        """
        super().__init__("Auditorium", width=int(width), height=int(height), torus=False,
                         model_nm=model_nm, preact=preact, props=props)
        self.plot_title = "An Auditorium"

    def set_agent_color(self):
        self.set_var_color(SITTING, disp.BLACK)
        self.set_var_color(STANDING, disp.RED)

    def from_json(self, json_input):
        super().from_json(json_input)
        self.add_variety(STANDING)
        self.add_variety(SITTING)
