"""
This file defines an Env, which is a collection
of agents that share a timeline and a Space.
"""
import getpass
import json
import os
from types import FunctionType

# we mean to add logging soon!
# import logging
import indra.display_methods as disp
import registry.registry as regis
from registry.execution_registry import execution_registry, \
    EXEC_KEY, CLI_EXEC_KEY
from registry.registry import get_prop
from indra.agent import join, switch, Agent, AgentEncoder
from indra.space import Space
import traceback
from indra.user import TEST, TestUser, USER_EXIT, APIUser
from indra.user import TermUser, TERMINAL, API
from indra.user import user_log_notif

DEBUG = False
DEBUG2 = False
DEF_USER = "User"
DEF_TIME = 10

UNLIMITED = 1000

X = 0
Y = 1

CENSUS_FUNC = "census_func"

POP_HIST_HDR = "PopHist for "
POP_SEP = ", "

color_num = 0


def agent_by_name(agent):
    return agent if isinstance(agent, str) else agent.name


class PopHist:
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
        return str(self)  # for now!

    def __iter__(self):
        return iter(self.pops)

    def __getitem__(self, key):
        return self.pops[key]

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
        return {"periods": self.periods, "pops": self.pops}


class Env(Space):
    """
    A collection of entities that share a space and time.
    An env *is* a space and *has* a timeline (PopHist).
    That makes the inheritance work out as we want it to.
    There are four functions possibly passed in here:

        - census
        - line_data_func
        - pop_hist_func

    These will all be cutover to be attributes of the env:
    the handy new way to support serialization.
    """

    def __init__(self, name, action=None, random_placing=True,
                 serial_obj=None,
                 exclude_member=None,
                 census=None,
                 line_data_func=None,
                 pop_hist_setup=None,
                 pop_hist_func=None,
                 members=None,
                 reg=True,
                 **kwargs):
        super().__init__(name, action=action,
                         random_placing=random_placing, serial_obj=serial_obj,
                         reg=False, members=members, **kwargs)
        self.execution_key = CLI_EXEC_KEY
        if EXEC_KEY in kwargs:
            self.execution_key = kwargs[EXEC_KEY]
        self.type = type(self).__name__
        self.user_type = os.getenv("user_type", TERMINAL)
        # this func is only used once, so no need to restore it
        self.pop_hist_setup = pop_hist_setup

        self.num_switches = 0
        if serial_obj is not None:
            # are we restoring env from json?
            self.restore_env(serial_obj)
        else:
            self.construct_anew(line_data_func, exclude_member,
                                census, pop_hist_func)

        self.set_menu_excludes()
        # now we set our global singleton:
        execution_registry.set_env(self.execution_key, self)
        # regis.set_env(self)

    def set_menu_excludes(self):
        if not get_prop('use_line', True, execution_key=self.execution_key):
            self.exclude_menu_item("line_graph")
        if not get_prop('use_scatter', True, execution_key=self.execution_key):
            self.exclude_menu_item("scatter_plot")

    def construct_anew(self, line_data_func=None, exclude_member=None,
                       census=None, pop_hist_func=None):
        self.pop_hist = PopHist()  # this will record pops across time
        # Make sure varieties are present in the history
        if self.pop_hist_setup is not None:
            self.pop_hist_setup(self.pop_hist)
        else:
            for mbr in self.members:
                self.pop_hist.record_pop(mbr, self.pop_count(mbr))

        self.plot_title = self.name
        self.user = None
        # these funcs will be stored as attrs...
        # but only if they're really funcs!
        # cause we're gonna try to call them
        if isinstance(census, FunctionType):
            print("Adding custom census func")
            self.attrs[CENSUS_FUNC] = census
        if isinstance(pop_hist_func, FunctionType):
            self.attrs["pop_hist_func"] = pop_hist_func
        if isinstance(line_data_func, FunctionType):
            self.attrs["line_data_func"] = line_data_func
        self.exclude_member = exclude_member
        self.womb = []  # for agents waiting to be born
        self.switches = []  # for agents waiting to switch groups
        self.handle_user_type()

    def handle_user_type(self):
        if self.user_type == TERMINAL:
            self.user = TermUser(getpass.getuser(), self,
                                 execution_key=self.execution_key)
            self.user.tell("Welcome to Indra, " + str(self.user) + "!")
        elif self.user_type == TEST:
            self.user = TestUser(getpass.getuser(), self,
                                 execution_key=self.execution_key)
        elif self.user_type == API:
            self.user = APIUser(getpass.getuser(), self,
                                execution_key=self.execution_key)

    def from_json(self, serial_obj):
        super().from_json(serial_obj)
        self.pop_hist = PopHist(serial_pops=serial_obj["pop_hist"])
        self.plot_title = serial_obj["plot_title"]
        nm = serial_obj["user"]["name"]
        msg = serial_obj["user"]["user_msgs"]
        self.user = APIUser(nm, self, execution_key=self.execution_key)
        self.user.tell(msg)
        self.name = serial_obj["name"]
        self.switches = serial_obj["switches"]
        self.womb = serial_obj["womb"]
        self.num_members_ever = serial_obj["num_members_ever"]

    def to_json(self):
        rep = super().to_json()
        rep["type"] = self.type
        rep["user"] = self.user.to_json()
        rep["plot_title"] = self.plot_title
        rep["pop_hist"] = self.pop_hist.to_json()
        rep["womb"] = self.womb
        rep["switches"] = self.switches
        rep["num_members_ever"] = self.num_members_ever
        return rep

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4,
                          sort_keys=True)

    def restore_env(self, serial_obj):
        self.from_json(serial_obj)

    def exclude_menu_item(self, to_exclude):
        """
        Just a pass-through call to our user object.
        """
        self.user.exclude_menu_item(to_exclude)

    def get_periods(self):
        return self.pop_hist.periods

    def __call__(self, **kwargs):
        """
        Calling the env makes it run. If we are on a terminal, we ask the user
        to put up a menu and choose. For tests, we just run N (default) turns.
        """
        if (self.user is None) or (self.user_type == TEST):
            self.runN(execution_key=self.execution_key)
        else:
            while True:
                # run until user exit!
                if self.user() == USER_EXIT:
                    break

    def add_member(self, member):
        """
        Don't think we really need this here!
        It is just a pass-through call at present.
        Must examine further: eliminate if not needed.
        """
        return super().add_member(member)

    def add_child(self, group):
        """
        Put a child agent in the womb.
        group: which group will add new agent
        """
        if isinstance(group, str):
            grp_nm = group
        else:
            grp_nm = agent_by_name(group)
        self.womb.append(grp_nm)
        if DEBUG:
            user_log_notif("An agent was added to the womb for "
                           + grp_nm)

    def pending_switches(self):
        return str(len(self.switches))

    def rpt_switches(self):
        return "# switches = " + self.pending_switches() + "; id: " \
               + str(id(self.switches))

    def add_switch(self, agent, from_grp, to_grp):
        """
        Switch agent from 1 grp to another
        We allow the parameters to be passed as the names of the agents,
        or as the agents themselves.
        In the future, it should be just names.
        """
        agent_nm = agent_by_name(agent)
        from_grp_nm = agent_by_name(from_grp)
        to_grp_nm = agent_by_name(to_grp)
        self.switches.append((agent_nm, from_grp_nm, to_grp_nm))

    def handle_womb(self):
        """
        The womb just contains group names -- they will be repeated
        as many times as that group needs to add members.
        We name the new members in the `member_creator()` method.
        This should be re-written as dict with:
            {"group_name": #agents_to_create}
        """
        if self.womb is not None:
            for group_nm in self.womb:
                group = regis.get_group(group_nm,
                                        execution_key=self.execution_key)
                if group is not None and group.member_creator is not None:
                    group.num_members_ever += 1
                    agent = group \
                        .member_creator("", group.num_members_ever,
                                        execution_key=self.execution_key)
                    regis.register(agent.name, agent,
                                   execution_key=self.execution_key)
                    join(group, agent)
                if self.random_placing:
                    self.place_member(agent, None)
            self.womb.clear()

    def handle_switches(self):
        if self.switches is not None:
            for (agent_nm, from_grp_nm, to_grp_nm) in self.switches:
                switch(agent_nm, from_grp_nm, to_grp_nm, self.execution_key)
                self.num_switches += 1
            self.switches.clear()

    def handle_pop_hist(self):
        self.pop_hist.add_period()
        if "pop_hist_func" in self.attrs:
            self.attrs["pop_hist_func"](self.pop_hist,
                                        execution_key=self.execution_key)
        else:
            for mbr in self.pop_hist.pops:
                if mbr in self.members and self.is_mbr_comp(mbr):
                    self.pop_hist.record_pop(mbr, self.pop_count(mbr))
                else:
                    self.pop_hist.record_pop(mbr, 0)

    def runN(self, periods=DEF_TIME, execution_key=CLI_EXEC_KEY):
        """
            Run our model for N periods.
            Return the total number of actions taken.
        """
        user_log_notif("Running env " + self.name + " for "
                       + str(periods) + " periods.")
        num_acts = 0
        num_moves = 0
        for i in range(periods):
            # these things need to be done before action loop:
            self.handle_womb()
            self.handle_switches()
            self.handle_pop_hist()

            (a, m) = super().__call__(execution_key=self.execution_key)
            num_acts += a
            num_moves += m
            census_rpt = self.get_census(num_moves)
            self.user.tell(census_rpt)
            self.num_switches = 0
        return num_acts

    def get_census(self, num_moves):
        """
        Gets the census data for all the agents stored
        in the member dictionary.

        Takes in how many agent has moved from one place to another
        and how many agent has switched groups and returns
        a string of these census data.

        census_func overrides the default behavior.
        """
        if CENSUS_FUNC in self.attrs:
            return self.attrs[CENSUS_FUNC](self,
                                           execution_key=self.execution_key)
        else:
            SEP_STR = "==================\n"
            census_str = ("\nTotal census for period "
                          + str(self.get_periods()) + ":\n"
                          + SEP_STR
                          + "Group census:\n"
                          + SEP_STR)
            for name in self.members:
                grp = self.members[name]
                population = len(grp)
                census_str += ("  " + name + " (id: "
                               + str(id(grp)) + "): "
                               + str(population) + "\n")
            census_str += (SEP_STR
                           + "Agent census:\n"
                           + SEP_STR
                           + "  Agents who moved: "
                           + str(num_moves) + "\n"
                           + "  Agents who switched groups: "
                           + str(self.num_switches))
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
                                           is_headless=self.headless(),
                                           attrs=self.attrs)
                line_plot.show()
                return line_plot
            except Exception as e:
                self.user.tell("Error when drawing line graph: " + str(e))
        else:
            return None

    def bar_graph(self):
        """
        show the movements of population
        """
        if self.has_disp():
            try:
                # TODO: improve implementation of the iterator of composite?
                periods, data = self.bar_data()
                if periods is None:
                    self.user.tell("No data to display.")
                    return None

                bar_graph = disp.BarGraph(self.plot_title,
                                          data, periods,
                                          is_headless=self.headless())
                bar_graph.show()
                return bar_graph
            except Exception as e:
                self.user.tell("Error when drawing bar graph:" + str(e))
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
                    attrs=self.attrs)
                scatter_plot.show()
                return scatter_plot
            except ValueError as e:  # Exception as e:
                self.user.tell("Error when drawing scatter plot: " + str(e))
                traceback.print_stack()
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
        period = None
        if self.exclude_member is not None:
            exclude = self.exclude_member
        else:
            exclude = None
        if "line_data_func" in self.attrs:
            (period, data) = self.attrs["line_data_func"](self)
        else:
            data = {}
            for var in self.pop_hist.pops:
                if var != exclude:
                    data[var] = {}
                    data[var]["data"] = self.pop_hist.pops[var]
                    data[var]["color"] = self.get_color(var)
                    if not period:
                        period = len(data[var]["data"])
        return period, data

    def bar_data(self):
        """
        This is the data for our scatter plot.
        This code assumes the env holds groups, and the groups
        hold agents with positions.
        This assumption is dangerous, and we should address it.
        """
        period = None
        if self.exclude_member is not None:
            exclude = self.exclude_member
        else:
            exclude = None

        data = {}
        for var in self.pop_hist.pops:
            if var != exclude:
                data[var] = {}
                data[var]["data"] = self.pop_hist.pops[var]
                data[var]["color"] = self.get_color(var)
                if not period:
                    period = len(data[var]["data"])
        return period, data

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
