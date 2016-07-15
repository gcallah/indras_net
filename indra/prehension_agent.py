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
        Look around and see what surrounds us.
        """
        super().survey_env()
        return None

    def visible_stance(self):
        """
        By default, just our stance. But we may override this.
        For instance, perhaps just our direction is visible to others.
        """
        return self.stance

    def debug_info(self):
        """
        Relevant debugging info.
        """
        s = super().debug_info() + "\nstance: " + str(self.stance)
        return s
