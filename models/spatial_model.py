"""
spatial_model.py
You can clone this file and its companion spatial_run.py
to easily get started on a new spatial model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.spatial_agent as sa
import indra.spatial_env as se


class TestSpatialAgent(sa.MobileAgent):
    """
    An agent that just prints where it is when asked to act
    """

    def act(self):
        print(se.pos_msg(self, self.pos))
