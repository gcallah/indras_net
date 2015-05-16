"""
grid_model.py
You can clone this file and its companion grid_run.py
to easily get started on a new grid model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.grid_agent as ga

X = 0
Y = 1


class TestGridAgent(ga.GridAgent):
    """
    An agent that prints its neighbors when asked to act
    and also jumps to an empty cell.
    """

    def act(self):
        (x, y) = self.pos
        print("With " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        print(self.name + " has neighbors: ")
        for neighbor in self.env.neighbor_iter(x, y):
            (x1, y1) = neighbor.pos
            print("    %i, %i" % (x1, y1))

    def postact(self):
        self.env.move_to_empty(self)
