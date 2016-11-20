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
    An agent whose changeable state determines its action, type, or character.
    Being "Markov-like" an agent will have its next state determined by a 
    probablility distribution represented by a vector. This vector's value is dependent
    only on the agent's current state.

    Attributes:
        state_pre: a state vector prehension
        state: whatever state the agent is in, subject to change
    """
    def __init__(self, name, goal, vlen, init_state, max_detect=1):
        super().__init__(name, goal, max_move=1, max_detect=max_detect)
        self.state_pre = markov.from_matrix(markov.state_vector(vlen,
                                                                init_state))
        self.state = markov.get_state(markov.to_matrix(self.state_pre))

    def survey_env(self):
        """
        Look around and see what surrounds us.
        """
        n_census = self.env.neighborhood_census(self)  # Method found in markov_env.
        return self.env.get_pre(self, n_census)        # Also in markov_env.

    def eval_env(self, other_pre):
        """
        Use the results of surveying the env to decide what to do.
        """
        # print("self_pre before = " + str(self.state_pre))
        prob_pre = self.state_pre.prehend(other_pre)
        self.state_pre.matrix = markov.probvec_to_state(prob_pre.matrix)
        # print("self_pre after = " + str(self.state_pre))
        self.next_state = markov.get_state(self.state_pre.matrix)
