"""
grid_model.py
You can clone this file and its companion grid_run.py
to easily get started on a new grid model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.spatial_agent as sa
import indra.grid_env as ge


class TestGridAgent(sa.SpatialAgent):
    """
    An agent that just prints where it is when asked to act
    """

    def act(self):
        print(ge.pos_msg(self))


