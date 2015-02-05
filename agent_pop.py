"""
agent_pop.py

Manages agent information.
The AgentPop class implements a flexible data structure
that allows the user of the class to access agents
from multiple perspectives.
"""

from collections import OrderedDict
import copy
import random
import itertools
import networkx as nx
import logging
import node

MAX_ZERO_PER = 8


class AgentPop(node.Node):
    """
    Holds our collection of agents and a sub-graph
    of their relationships.
    This should implement list functions.
    """

    def __init__(self, name):
        super().__init__(name)
        self.vars = OrderedDict()
        self.graph = nx.Graph()
        self.num_zombies = 0


    def __iter__(self):
        alists = []
        for var in self.varieties_iter():
            alists.append(self.vars[var]["agents"])
        # create an iterator that chains the lists together as if one:
        return itertools.chain(*alists)


    def __len__(self):
        l = 0
        for var in self.varieties_iter():
            l += len(self.vars[var]["agents"])
        return l


    def __reversed__(self):
        return AgentPop.ReverseIter(self)

    
    def set_num_zombies(self, num):
        self.num_zombies = num


    def varieties_iter(self):
        """
        Allows iteration over the varieties of agents.
        """
        return iter(self.vars)


    def variety_iter(self, var):
        """
        Allows iteration over the agents of one variety
        """
        return iter(self.vars[var]["agents"])


    class AgentIter:
        """
        The __next__() func is shared among several other iters,
        as well as some other code bits.
        """
        def __init__(self, agents):
            self.i = 0
            self.agents = agents


        def __iter__(self):
            return self


        def __next__(self):
            """
            Return the next element or raise exception to stop iterating.
            """
            if self.i < len(self.indices):
                # get an agent!
                agent = self.agents.element_at(self.indices[self.i])
                self.i += 1
                return agent
            else:
                raise StopIteration()


    class ReverseIter(AgentIter):
        """
        Iterate backwards through our agents.
        Eventually this should be made generic so it can 
        backwards iterate through anything that implements
        an element_at() method.
        """
        def __init__(self, agents):
            super().__init__(agents)
            self.indices = list(range(len(agents) - 1, -1, -1))


    class RandomIter(AgentIter):
        """
        Iterate randomly through our agents.
        Eventually this should be made generic so it can 
        randomly iterate through anything that implements
        an element_at() method.
        """
        def __init__(self, agents):
            super().__init__(agents)
            self.indices = list(range(len(agents)))
            random.shuffle(self.indices)


    def agent_random_iter(self):
        """
        Loop through agents in random order.
        """
        return AgentPop.RandomIter(self)


    def element_at(self, i):
        """
        Another way to treat the AgentPop as if it were really
        one big list.
        """
        if i < 0 or i > len(self):
            raise IndexError()
        else:
            for var in self.varieties_iter():
                l = len(self.vars[var]["agents"])
                logging.debug("Looking for element from "
                              + var + " at position "
                              + str(i) + " and var has len "
                              + str(l))
                if i < l:
                    # that means the agent is in this list
                    return self.vars[var]["agents"][i]
                else:
                    # otherwise, the agent lies in one of the 
                    # remaining lists, so subtract the length 
                    # of this one from i and continue.
                     i -= l


    def append(self, agent):
        """
        Appends to agent list.
        """
        var = node.get_node_type(agent)
        logging.debug("Adding " + agent.__str__()
                      + " of variety " + var)

        if var in self.vars:
            self.vars[var]["agents"].append(agent)
        else:
            self.vars[var] = {"agents": [agent],
                                   "pop_of_note": 0,
                                   "pop_hist": [],
                                   "zombies": [],
                                   "zero_per": 0}
            self.graph.add_edge(self, var)

# we link each agent to the variety
# so we can show their relationship
        self.graph.add_edge(var, agent)


    def create_zombies(self):
        """
        Choose a random batch of agents from each var
        for possible revivial later.
        """
        if self.num_zombies > 0:
            for var in self.varieties_iter():
                while len(self.vars[var]["zombies"]) < self.num_zombies:
                    agent = random.choice(self.vars[var]["agents"])
                    self.vars[var]["zombies"].append(copy.copy(agent))


    def remove(self, agent):
        """
        Removes from agent list.
        """
        logging.debug("Removing " + agent.name + " from agents")
        var = node.get_node_type(agent)
        self.vars[var]["agents"].remove(agent)
        self.graph.remove_node(agent) # also removes edges!


    def join_agents(self, a1, a2):
        """
        Add a graph edge between agents.
        """
        self.graph.add_edge(a1, a2)


    def contains(self, var):
        """
        Do we have this sort of thing in our env?
        """
        return var in self.vars


    def get_agents_of_var(self, var):
        """
        Return all agents of type var.
        """
        if var in self.vars:
            return self.vars[var]["agents"]
        else:
            return None


    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return len(self.vars[var]["agents"])


    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        var = node.get_node_type(agent)
        return self.get_pop(var)


    def get_pop_hist(self):
        """
        Make a list containing the population history
        for each var in vars.
        """
        pop_hist = {}
        for var in self.varieties_iter():
            pop_hist[var] = self.vars[var]["pop_hist"]
        return pop_hist


    def get_pop_of_note(self, var):
        """
        Return the value of pop_of_note for 'var'.
        """
        return self.vars[var]["pop_of_note"]


    def change_pop_of_note(self, var, change):
        """
        Change the value of pop_of_note by 'change.'
        """
        self.vars[var]["pop_of_note"] += change


    def append_pop_hist(self, var, pop):
        """
        Add the most recent pop to pop_hist.
        """
        self.vars[var]["pop_hist"].append(pop)


    def census(self):
        """
        Take a census of agents by variety.
        Return a string of results for possible display.
        """
        ret = ""
        for v in self.varieties_iter():
            pop = self.get_pop(v)
            ret += v + ": " + str(pop) + "\n"
            var = self.vars[v]
            var["pop_hist"].append(pop)
            if pop == 0:
                var["zero_per"] += 1
                if var["zero_per"] >= MAX_ZERO_PER:
                    for agent in var["zombies"]:
                        self.append(copy.copy(agent))
                    var["zero_per"] = 0
        return ret


