"""
plane_model.py
You can clone this file and its companion plan_run.py
to easily get started on a new spatial model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import indra.plane_agent as pa
import indra.plane_env as pe


class TestPlaneAgent(pa.MobileAgent):
    """
    An agent that just prints where it is when asked to act
    """

    def act(self):
        print(pe.pos_msg(self, self.pos))
