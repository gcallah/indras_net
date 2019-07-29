"""
This file defines an Env, which is a collection
of agents that share a timeline and a Space.
"""
from propargs.propargs import PropArgs as pa
import os
import getpass
# import logging
import indra.display_methods as disp
from indra.agent import join, switch, Agent, AgentEncoder
from indra.space import Space
from indra.user import TermUser, TERMINAL, API
from indra.user import TEST, TestUser, USER_EXIT, APIUser
import json

DEBUG = False
DEBUG2 = False
DEF_USER = "User"
DEF_TIME = 10

X = 0
Y = 1

POP_HIST_HDR = "PopHist for "
POP_SEP = ", "

color_num = 0


class PopHist():
    """
        Data structure to record the fluctuating numbers of various agent
        types.
    """
    def __init__(self, serial_pops=None):
        self.pops = {}
        self.periods = 0
        if serial_pops is not None:
            self.from_json(serial_pops)

    def __str__(self):
        s = POP_HIST_HDR
        for mbr in self.pops:
            s += mbr + POP_SEP
        return s

    def __repr__(self):
        return(str(self))  # for now!

    def add_period(self):
        self.periods += 1

    def record_pop(self, mbr, count):
        if mbr not in self.pops:
            self.pops[mbr] = []
        self.pops[mbr].append(count)

    def from_json(self, pop_data):
        self.periods = pop_data['periods']
        self.pops = pop_data['pops']

    def to_json(self):
        rep = {}
        rep["periods"] = self.periods
        rep["pops"] = self.pops
        return rep


class Env(Space):
    """
    A collection of entities that share a space and time.
    An env *is* a space and *has* a timeline (PopHist).
    That makes the inheritance work out as we want it to.
    """
    def __init__(self, name, action=None, random_placing=True,
                 props=None, serial_obj=None, census=None,
                 change_grid_spacing=0, hide_xy_labels=False,
                 **kwargs):
        super().__init__(name, action=action,
                         random_placing=random_placing, serial_obj=serial_obj,
                         **kwargs)

        if serial_obj is not None:
            self.restore_env(serial_obj)
        else:
            self.props = props
            self.census_func = census
            self.pop_hist = PopHist()  # this will record pops across time
            # Make sure varieties are present in the history
            for mbr in self.members:
                self.pop_hist.record_pop(mbr, self.pop_count(mbr))
            # Attributes for plotting
            self.plot_title = self.name
            self.user = None
            self.registry = {}

        self.type = "env"
        self.womb = []  # for agents waiting to be born
        self.switches = []  # for agents waiting to switch groups
        self.user_type = os.getenv("user_type", TERMINAL)
        self.change_grid_spacing = change_grid_spacing
        self.hide_xy_labels = hide_xy_labels
        self.num_acts = 0
        self.num_moves = 0
        self.num_switches = 0
        if (self.user_type == TERMINAL):
            self.user = TermUser(getpass.getuser(), self)
            self.user.tell("Welcome to Indra, " + str(self.user) + "!")
        elif (self.user_type == TEST):
            self.user = TestUser(getpass.getuser(), self)
        elif (self.user_type == API):
            self.user = APIUser(getpass.getuser(), self)

    def from_json(self, serial_obj):
        super().from_json(serial_obj)
        model_prop = json.loads(json.dumps(serial_obj["props"],
                                indent=4))
        self.props = pa.create_props("basic",
                                     prop_dict=model_prop)
        self.pop_hist = PopHist(serial_pops=serial_obj["pop_hist"])
        self.plot_title = serial_obj["pop_hist"]
        # self.user = APIUser(serial_obj["user"])
        self.name = serial_obj["name"]
        self.womb = serial_obj["womb"]
        self.switches = serial_obj["switches"]
        # construct self.registry
        self.registry = {}
        for nm in self.members:
            self.add_mbr_to_regis(self.members[nm])
        print(self.registry)
        # construct self.groups
        # for nm in self.registry:
        #     if self.registry[nm].groups != {}:
        #         for gnm in self.registry[nm].groups:
        #             if gnm != "env":
        #                 self.registry[nm].add_group(self.registry[gnm])
        #                 self.registry[nm].groups[gnm] = self.registry[gnm]

    def to_json(self):
        rep = super().to_json()
        rep["type"] = self.type
        rep["plot_title"] = self.plot_title
        rep["props"] = self.props.to_json()
        rep["pop_hist"] = self.pop_hist.to_json()
        rep["womb"] = self.womb
        rep["switches"] = self.switches
        ret_mbrs = {}
        for mnm in rep["members"]:
            ret_mbrs[mnm] = rep["members"][mnm]
        rep["members"] = ret_mbrs
        rep["registry"] = self.registry
        return rep

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def __init_unrestorables(self):
        pass

    def restore_env(self, serial_obj):
        self.from_json(serial_obj)
        self.__init_unrestorables()

    def add_mbr_to_regis(self, member):
        if member.type == "agent":
            self.registry[member.name] = member
        else:
            self.registry[member.name] = member
            for mbrnm in member.members:
                self.add_mbr_to_regis(member.members[mbrnm])

    def get_periods(self):
        return self.pop_hist.periods

    def __call__(self):
        """
        Calling the env makes it run. If we are on a terminal, we ask the user
        to put up a menu and choose. For tests, we just run N (default) turns.
        """
        if self.action is not None:
            # the action was defined outside this class, so pass self:
            self.action(self)
        if (self.user is None) or (self.user_type == TEST):
            self.runN()
        else:
            while True:
                # run until user exit!
                if self.user() == USER_EXIT:
                    break

    def add_member(self, member):
        super().add_member(member)
        # self.registry[member.name] = member

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
        # do we need to connect agent to env (self)?

    def now_switch(self, agent, grp1, grp2):
        """
        Switches the groups of the agent now
        instead of at the end of period
        unlike add_switch.
        """
        switch(agent, grp1, grp2)
        self.num_switches += 1

    def runN(self, periods=DEF_TIME):
        """
            Run our model for N periods.
            Return the total number of actions taken.
        """
        num_acts = 0
        for i in range(periods):
            # before members act, give birth to new agents
            # we will have tuple of agent and group
            # do group += agent
            # self.user.tell("In period ", i)
            if self.womb is not None:
                for (agent, group) in self.womb:
                    # add the agent into the registry
                    self.registry[agent.name] = agent
                    join(group, agent)
                del self.womb[:]
            if self.switches is not None:
                for (agent, grp1, grp2) in self.switches:
                    switch(agent, grp1, grp2)
                    self.num_switches += 1
                del self.switches[:]

            self.pop_hist.add_period()
            for mbr in self.pop_hist.pops:
                if mbr in self.members and self.is_mbr_comp(mbr):
                    self.pop_hist.record_pop(mbr, self.pop_count(mbr))
                else:
                    self.pop_hist.record_pop(mbr, 0)

            (a, m) = super().__call__()
            num_acts += a
            self.num_moves += m
            census_rpt = self.get_census()
            self.user.tell(census_rpt)
        return num_acts

    def get_census(self):
        """
        Gets the census data for all the agents stored
        in the member dictionary.

        Takes in how many agent has moved from one place to another
        and how many agent has switched groups and returns
        a string of these census data.

        census_func (to be added) overrides the default behavior.
        """
        if self.census_func:
            return self.census_func(self)
        else:
            census_str = ("\nCensus for period " + str(self.get_periods())
                          + ":\n")
            for composite_str in self.members:
                population = len(self.members[composite_str])
                census_str += (composite_str + ": " + str(population) + "\n")
            census_str += ("\tTotal agents moved: " + str(self.num_moves)
                           + "\n" + "\tTotal agents who switched groups: "
                           + str(self.num_switches))
        self.num_acts = 0
        self.num_moves = 0
        self.num_switches = 0
        return census_str

    def has_disp(self):
        if not disp.plt_present:
            self.user.tell("ERROR: Graphing package encounters a problem: "
                           + disp.plt_present_error_message)
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
                    is_headless=self.headless(),
                    change_grid_spacing=self.change_grid_spacing,
                    hide_xy_labels=self.hide_xy_labels)
                scatter_plot.show()
                return scatter_plot
            except Exception as e:
                self.user.tell("Error when drawing graph: " + str(e))
        else:
            return None

    def get_color(self, variety):
        if variety in self.members and self.members[variety].has_color():
            return self.members[variety].get_color()
        else:
            global color_num
            color_num += 1
            return disp.get_color(variety, color_num)

    def get_marker(self, variety):
        if variety in self.members:
            return self.members[variety].get_marker()
        else:
            return None

    def line_data(self):
        data = {}
        period = None
        for var in self.pop_hist.pops:
            data[var] = {}
            data[var]["data"] = self.pop_hist.pops[var]
            data[var]["color"] = self.get_color(var)
            if not period:
                period = len(data[var]["data"])
        return (period, data)

    def plot_data(self):
        """
        This is the data for our scatter plot.
        This code assumes the env holds groups, and the groups
        hold agents with positions.
        This assumption is dangerous, and we should address it.
        """
        if not disp.plt_present:
            self.user.tell("ERROR: Graphing package encountered a problem: "
                           + disp.plt_present_error_message)
            return

        data = {}
        for variety in self.members:
            data[variety] = {}
            # matplotlib wants a list of x coordinates, and a list of y
            # coordinates:
            data[variety][X] = []
            data[variety][Y] = []
            data[variety]["color"] = self.members[variety].get_color()
            data[variety]["marker"] = self.members[variety].get_marker()
            current_variety = self.members[variety]
            for agent_nm in current_variety:
                # temp fix for one of the dangers mentioned above:
                # we might not be at the level of agents!
                if isinstance(current_variety[agent_nm], Agent):
                    current_agent_pos = current_variety[agent_nm].pos
                    if current_agent_pos is not None:
                        (x, y) = current_agent_pos
                        data[variety][X].append(x)
                        data[variety][Y].append(y)
        return data

    def headless(self):
        return (self.user_type == API) or (self.user_type == TEST)
