"""
prehension_agent.py
An agent that use Prehensions to understand its environment.
"""
import indra.grid_agent as ga
import indra.prehension as pre


class PrehensionAgent(ga.GridAgent):
    """
    An agent that use Prehensions to understand its environment.
    """
    def __init__(self, name, goal, max_move=1, max_detect=1):
        super().__init__(name, goal, max_move, max_detect)
        self.my_filter = None
        self.stance = pre.Prehension()

    def survey_env(self):
        """
        Look around and see what stances surround us.
        """
        super().survey_env()
        other_pre = pre.Prehension()
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=self.my_filter):
            other_pre = other.stance.prehend(other_pre)
        return other_pre
