import indra.markov as markov
import indra.markov_agent as ma
import indra.markov_env as me

class Person(ma.MarkovAgent):
    """
    A person wanders around the environment when not coupled.
    
    Attributes:
        infected: true if a person is infected with HIV
        known: true if the infection is known (and the infected must also be true)
        infection_length: how long the person has been infected
        coupled: true if sexually coupled
        coupled_length: how long the person has been coupled
        commitment: how long the person will stay coupled
        coupling_tendency: how likely the person is to be coupled
        condom_use: the percent chance the person uses protection
        test_frequence: number of times the person gets tested per year
        partner: with whom the person is coupled with
    """

    def __init__(self, infected, known, infection_length, coupled, coupled_length, commitment, coupling_tendency, condom_use, test_frequence, partner):



