"""
emp_model.py
A simple text of creating a heirarchical network.
"""
import networkx as nx
#import pygraphviz as pgv
import entity as ent

EMPLOYS = "employs"


class EmpAgent(ent.Agent):
    """
    An agent that exists in an heirarchical organization.
    """

    def act(self):
        """
        An act() method that just announces the agent.
        """

        print("Agent " + self.name + " with a goal of "
                + self.goal)


class EmpEnv(ent.Environment):
    """
    An environment for creating a heirarchical graph
    and sisplaying it.
    """

    def __init__(self, model_nm=None):
        super().__init__("Employee environment",
                    model_nm=model_nm)


    def employs(self, employer, employee):
        ent.add_ent_prehension(employer, EMPLOYS, employee)


    def draw(self):
        if self.graph is not None:
            nx.draw_networkx(self.graph)
            plt.show()



