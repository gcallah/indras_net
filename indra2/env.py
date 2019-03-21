"""
This file defines an Env, which is a collection
of agents that share a timeline and a Space.
"""
# import json
import os
import getpass
import indra2.display_methods as disp
from indra2.agent import join, switch
from indra2.space import Space
from indra2.user import TermUser, TERMINAL, WEB, TEST

DEBUG = True
DEBUG2 = False
DEF_USER = "User"
DEF_TIME = 10

X = 0
Y = 1

POP_HIST_HDR = "PopHist for "
POP_SEP = ", "


class PopHist():
    """
        Data structure to record the fluctuating numbers of various agent
        types.
    """
    def __init__(self):
        self.pops = {}

    def __str__(self):
        s = POP_HIST_HDR
        for mbr in self.pops:
            s += mbr + POP_SEP
        return s

    def __repr__(self):
        return(str(self))  # for now!

    def record_pop(self, mbr, count):
        if mbr not in self.pops:
            self.pops[mbr] = []
        self.pops[mbr].append(count)


class Env(Space):
    """
    A collection of entities that share a space and time.
    An env *is* a space and *has* a timeline.
    That makes the inheritance work out as we want it to.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.pop_hist = PopHist()  # this will record pops across time
        # Make sure variesties are present in the history
        for mbr in self.members:
            self.pop_hist.record_pop(mbr, self.pop_count(mbr))

        self.womb = []  # for agents waiting to be born
        self.switches = []  # for agents waiting to switch groups

        # Attributes for plotting
        self.plot_title = self.name

        self.user = None
        self.user_type = os.getenv("user_type", TERMINAL)
        if (self.user_type == TERMINAL) or (self.user_type == TEST):
            self.user = TermUser(getpass.getuser(), self)
            self.user.tell("Welcome to Indra, " + str(self.user) + "!")

    def __call__(self):
        if (self.user is None) or (self.user_type == TEST):
            self.runN()
        else:
            while True:
                # run until user exit!
                self.user()

    def add_child(self, agent, group):
        """
        Put a child agent in the womb.
        agent: child to add
        group: which group child will join
        """
        self.womb.append((agent, group))
        if DEBUG:
            self.user.tell("{} added to the womb".format(agent.name))
        # do we need to connect agent to env (self)?

    def add_switch(self, agent, grp1, grp2):
        """
        Put a child agent in the womb.
        agent: child to add
        group: which group child will join
        """
        self.switches.append((agent, grp1, grp2))
        if DEBUG:
            self.user.tell("{} added to switches".format(str(agent)))
        # do we need to connect agent to env (self)?

    def runN(self, periods=DEF_TIME):
        """
            Run our model for N periods.
            Return the total number of actions taken.
        """
        acts = 0
        for i in range(periods):
            # before members act, give birth to new agents
            # we will have tuple of agent and group
            # do group += agent

            if self.womb is not None:
                for (agent, group) in self.womb:
                    join(group, agent)
                del self.womb[:]
            if self.switches is not None:
                for (agent, grp1, grp2) in self.switches:
                    switch(agent, grp1, grp2)
                del self.switches[:]

            for mbr in self.pop_hist.pops:
                if mbr in self.members and self.is_mbr_comp(mbr):
                    self.pop_hist.record_pop(mbr, self.pop_count(mbr))
                else:
                    self.pop_hist.record_pop(mbr, 0)

            curr_acts = super().__call__()
            acts += curr_acts
        return acts

    def has_disp(self):
        if not disp.plt_present:
            self.user.tell("ERROR: No graphing package installed")
            return False
        else:
            return True

    def line_graph(self):
        """
        Show agent populations.
        """
        if self.has_disp():
            try:
                # TODO: improve implementation of the iterator of composite?
                period, data = self.line_data()
                if period is None:
                    self.user.tell("No data to display.")
                    return None

                line_plot = disp.LineGraph(self.plot_title,
                                           data, period,
                                           is_headless=self.headless())
                line_plot.show()
                return line_plot
            except Exception as e:
                self.user.tell("Error when drawing graph: " + str(e))
        else:
            return None

    def scatter_graph(self):
        """
        Show agent locations.
        """
        if self.has_disp():
            try:
                data = self.plot_data()
                scatter_plot = disp.ScatterPlot(
                    self.plot_title, data,
                    int(self.width), int(self.height),
                    anim=True, data_func=self.plot_data,
                    is_headless=self.headless())
                scatter_plot.show()
                return scatter_plot
            except Exception as e:
                self.user.tell("Error when drawing graph: " + str(e))
        else:
            return None

    def line_data(self):
        data = {}
        # TODO: implement period?
        period = None
        for var in self.pop_hist.pops:
            data[var] = {}
            data[var]["data"] = self.pop_hist.pops[var]
            # TODO: define colors in env?
            if not period:
                period = len(data[var]["data"])
        return (period, data)

    def plot_data(self):
        if not disp.plt_present:
            self.user.tell("ERROR: No graphing package installed")
            return

        data = {}
        for var in self.members:
            data[var] = {}
            # matplotlib wants a list of x coordinates, and a list of y
            # coordinates:
            data[var][X] = []
            data[var][Y] = []
            # TODO: define colors in env?
            # data[var]["color"] = self.agents.get_var_color(var)
            current_var = self.members[var]
            for agent in current_var:
                current_agent_pos = current_var[agent].pos
                if current_agent_pos is not None:
                    (x, y) = current_agent_pos
                    data[var][X].append(x)
                    data[var][Y].append(y)
        return data

    def headless(self):
        return (self.user_type == WEB) or (self.user_type == TEST)
