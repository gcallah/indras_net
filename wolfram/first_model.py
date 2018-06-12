"""
grid_model.py
You can clone this file and its companion grid_run.py
to easily get started on a new grid model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.grid_agent as ga

black = 0
white = 1

class TestGridAgent(ga.GridAgent):
    """
    An agent that prints its neighbors in preact
    and also jumps to an empty cell: default behavior
    from our ancestor.
    """
    def __init__(self, name, goal, max_move=1, max_detect=1, cell=None):
        super().__init__(name, goal, max_move=1, max_detect=1, cell=None)
        self.state = None
        self.next_state = None

    def preact(self):
        (x, y) = self.pos
        print("With " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        print(self.name + " has neighbors: ")
        for neighbor in self.neighbor_iter():
            (x1, y1) = neighbor.pos
            print("    %i, %i" % (x1, y1))
            if

    def set_color(self, new_color):
        old_type = self.state
        self.state = new_color
        self.env.change_agent_type(self, old_type, self.ntype)

    def postact(self):
        print("Agent %s postacting" % (self.name))
        if self.next_state is not None and self.next_state != self.state:
            # print("Setting state to " + str(self.next_state))
            self.set_state(self.next_state)
            self.next_state = None
