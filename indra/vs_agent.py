"""
vs_agent.py
An agent that use vector space Prehensions to understand its environment.
"""
import indra.grid_agent as ga
import indra.vector_space as vs
import indra.prehension_agent as pa


class VSAgent(pa.PrehensionAgent):
    """
    An agent that use Prehensions to understand its environment.
    """
    def __init__(self, name, goal, max_move=1, max_detect=1):
        super().__init__(name, goal, max_move, max_detect)
        self.my_filter = None
        self.stance = vs.VectorSpace()

    def survey_env(self):
        """
        Look around and see what surrounds us.
        """
        super().survey_env()
        other_pre = vs.VectorSpace()
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=self.my_filter):
            # accumulate prehensions:
            other_pre = other.visible_stance().prehend(other_pre)
        return other_pre
