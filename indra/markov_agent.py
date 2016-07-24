"""
markov_agent.py
An agent that use markov chain space Prehensions to understand its environment.
"""
import indra.grid_agent as ga
import indra.markov as markov
import indra.markov_env as markov_env
import indra.prehension_agent as pa


class MarkovAgent(pa.PrehensionAgent):
    """
    An agent that use Prehensions to understand its environment.
    """
    def __init__(self, name, goal, vlen, init_state):
        super().__init__(name, goal, max_move=1, max_detect=1)
        self.state = markov.state_vector(vlen, init_state)

    def survey_env(self):
        """
        Look around and see what surrounds us.
        """
        return self.env.get_pre()

    def get_state(self):
        """
        This method assumes we have a state vector.
        It then return the index of the element that is "on."
        """
        i = 0
        for s in self.state.flat:
            if s == 1:
                return i
            i += 1
