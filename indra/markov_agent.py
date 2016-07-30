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
        self.state_pre = markov.from_matrix(markov.state_vector(vlen,
                                                                init_state))
        self.state = markov.get_state(markov.to_matrix(self.state_pre))

    def survey_env(self):
        """
        Look around and see what surrounds us.
        """
        return self.env.get_pre()

    def eval_env(self, other_pre):
        """
        Use the results of surveying the env to decide what to do.
        """
        print("Called eval_env")
        print("other_pre = " + str(other_pre))
        prob_pre = self.state_pre.prehend(other_pre)
        self.state_pre.matrix = markov.probvec_to_state(prob_pre.matrix)
        print("self_pre = " + str(self.state_pre))
        self.next_state = markov.get_state(self.state_pre.matrix)
