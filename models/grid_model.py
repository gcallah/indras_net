"""
grid_model.py
You can clone this file and its companion grid_run.py
to easily get started on a new grid model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.spatial_agent as sa

X = 0
Y = 1

class TestGridAgent(sa.SpatialAgent):
    """
    An agent that prints its neighbors when asked to act
    and also jumps to an empty cell.
    """

    def act(self):
        # print(ge.pos_msg(self))
        x = self.pos[X]
        y = self.pos[Y]
        print("With " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        print(self.name + " has neighbors: ")
        for neighbor in self.env.neighbor_iter(x, y):
            print("    " + neighbor.name)

    def postact(self):
        self.env.move_to_empty(self)
