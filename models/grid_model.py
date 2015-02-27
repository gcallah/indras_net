"""
grid_model.py
You can clone this file and its companion grid_run.py
to easily get started on a new grid model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.spatial_agent as sa


class TestGridAgent(sa.SpatialAgent):
    """
    An agent that prints its neighbors when asked to act
    """

    def act(self):
        # print(ge.pos_msg(self))
        x = self.pos[0]
        y = self.pos[1]
        print("With agent " + self.name
              + " we are looking around "
              + " x = " + str(x)
              + " y = " + str(y))
        naybs = self.env.get_neighbors(x, y, True)
        if len(naybs) == 0:
            print(self.name + " has no neighbors.")
        else:
            print(self.name + " has neighbors: ")
            for nayb in naybs:
                print("    " + nayb.name)
