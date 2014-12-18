"""
Filename: econ_agent.py
Author: Gene Callahan
"""

import entity


def print_econ_agent(agent):
    print(agent.__str__())


class EconAgent(entity.Entity):
    roles = ("capitalist", "banker", "worker", "manager", "entrepreneur", "regulator")

    def __init__(self, role, endowment, name):
        super().__init__(name)
        self.role      = role
        self.endowment = endowment

    def __str__(self):
        return "I am " +self.name + " a " + self.role + " with " + str(self.endowment) + " dollars"

    def reassign(self):
        self.role = random.choice(Agent.roles)

    def get_role(self):
        return self.role

    def get_endowment(self):
        return self.endowment

    def add_employee(self, emp):
        entity.join_entities(self, "employee", emp)


