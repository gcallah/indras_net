"""
You can clone this file and its companion two_pop_m_run.py
to easily get started on a new two pop markov model.

It also is a handy tool to have around for testing
new features added to the base system. The agents
don't move. They have 50% chance of changing color
from red to blue, or from blue to red.
"""
import indra.two_pop_markov as itpm

R = 0
B = 1

STATE_MAP = { R: "Red", B: "Blue" }


class TestFollower(itpm.Follower):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: defaut behavior
    from our ancestor.
    
    Attributes:
        state: Red or Blue ... whichever it is the agent
            will appear to be this on the scatter plot.
        ntype: node type
        next_state: the next color the agent will be
    """

    def __init__(self, name, goal):
        super().__init__(name, goal)
        self.state = R
        self.ntype = STATE_MAP[R]
        self.next_state = None
 
    def postact(self):
        """
        Set our type to next_state.
        """
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None

        return self.pos

    def set_state(self, new_state):
        """
        Set agent's new type.
        """
        old_type = self.ntype
        self.state = new_state
        self.ntype = STATE_MAP[new_state]
        self.env.change_agent_type(self, old_type, self.ntype)
