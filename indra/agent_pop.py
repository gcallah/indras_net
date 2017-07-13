"""
agent_pop.py

Manages agent information.
The AgentPop class implements a flexible data structure
that allows the user of the class to access agents
from multiple perspectives.
"""

from collections import OrderedDict
import random
import itertools
import json
import networkx as nx
import logging
import indra.node as node
import indra.entity as ent

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
        all_agents = self.all_agents_list()
        return reversed(all_agents)

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

    def all_agents_list(self):
        all_agents = []
        for var in self.varieties_iter():
            all_agents += self.vars[var]["agents"]
        return all_agents

    def agent_random_iter(self):
        """
        Loop through agents in random order.
        """
        all_agents = self.all_agents_list()
        random.shuffle(all_agents)
        return iter(all_agents)

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

    def get_var_color(self, var):
        """
        Get the display color for this variety.
        """
        return self.vars[var]["disp_color"]

    def set_var_color(self, var, color):
        """
        Set the display color for this var.
        """
        self.add_variety(var)
        self.vars[var]["disp_color"] = color

    def add_variety(self, var):
        """
        Sometimes, we may know a variety is coming, and want to
        add it even before any agents of that variety are created,
        for census or graphing purposes.
        """
        if var not in self.vars:
            self.vars[var] = {"agents": [],
                              # some arbitrary data to track for pop:
                              "pop_data": 0,
                              "pop_hist": [],
                              "my_periods": 0,
                              "disp_color": None}

    def append(self, agent, v=None):
        """
        Appends to agent list.
        """
        if v is None:
            var = agent.get_type()
        else:
            var = v
        logging.info("Adding %s of variety %s" % (agent.name, var))

        if var not in self.vars:
            self.add_variety(var)
            self.graph.add_edge(self, var)

        self.vars[var]["agents"].append(agent)

# we link each agent to the variety
# so we can show their relationship
        self.graph.add_edge(var, agent)

    def remove(self, agent, v=None):
        """
        Removes from agent list.
        """
        logging.debug("Removing " + agent.name + " from agents")
        if v is None:
            var = agent.get_type()
        else:
            var = v
        self.vars[var]["agents"].remove(agent)
        self.graph.remove_node(agent)  # also removes edges!

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

    def get_randagent_of_var(self, var):
        return random.choice(self.vars[var]["agents"])

    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return len(self.vars[var]["agents"])

    def get_total_pop(self):
        total_pop = 0
        for var in self.varieties_iter():
            total_pop += self.get_pop(var)
        return total_pop

    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        var = agent.get_type()
        return self.get_pop(var)

    def get_var_pop_hist(self, var):
        return self.vars[var]["pop_hist"]

    def get_pop_hist(self):
        """
        Make a list containing the population history
        for each var in vars, if var is None.
        We should merge this with display_methods
        assemble data when we can.
        """
        pop_hist = {}
        for var in self.varieties_iter():
            pop_hist[var] = {}
            pop_hist[var]["data"] = self.vars[var]["pop_hist"]
            pop_hist[var]["color"] = self.vars[var]["disp_color"]
            logging.debug("Setting color for %s to %s"
                          % (var, pop_hist[var]["color"]))
        return pop_hist

    def get_pop_data(self, var):
        """
        Return the value of pop_data for 'var'.
        """
        return self.vars[var]["pop_data"]

    def change_pop_data(self, var, change):
        """
        Change the value of pop_data by 'change.'
        """
        self.vars[var]["pop_data"] += change

    def change_agent_type(self, agent, old_type, new_type):
        self.remove(agent, v=old_type)
        self.append(agent, v=new_type)

    def append_pop_hist(self, var, pop):
        """
        Add the most recent pop to pop_hist.
        """
        self.vars[var]["pop_hist"].append(pop)

    def census(self, exclude_var=None):
        """
        Take a census of agents by variety.
        Return a string of results for possible display.
        """
        ret = ""
        for v in self.varieties_iter():
            if v != exclude_var:
                pop = self.get_pop(v)
                ret += v + ": " + str(pop) + "\n"
                var = self.vars[v]
                var["pop_hist"].append(pop)
                # a type might enter the env after period 0!
                # so we track that in my_periods
                var["my_periods"] += 1
        return ret

    def jsondump(self, obj):
        if type(obj) == nx.Graph:
            return "Graph"
        elif isinstance(obj, ent.Entity):
            return obj.to_json()
        else:
            return obj.__dict__

    def record_results(self, file_nm):
        json.dump(self, open(file_nm, 'w'), indent=4,
                  default=self.jsondump)
