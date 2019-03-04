"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json
import os
import getpass
import display_methods as disp
from itime import Time, DEF_TIME
from space import Space, DEBUG
from user import TermUser, TERMINAL, WEB


DEF_USER = "User"

# Constant for plotting
SC = "SC" # Scatter plot
LN = "LN" # Line plot
X = 0
Y = 1

class PopHist():
    """
        Data structure to record the fluctuating numbers of various agent
        types.
    """
    def __init__(self):
        self.pops = {}

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
        self.time = Time(name, **kwargs)
        self.pop_hist = PopHist()   # this will record pops across time
        
        # Attributes for plotting
        # TODO: feed values in constructor?  
        self.plot_type = SC
        self.plot_title = "Environment Plot"
        
        user_type = os.getenv("user_type", TERMINAL)
        if user_type == TERMINAL:
            # self.user = TermUser(os.getenv("USERNAME", DEF_USER), self)
            self.user = TermUser(getpass.getuser(), self)
            self.user.tell("Welcome to Indra, " + str(self.user) + "!")

    def __call__(self):
        if self.user is not None:
            while True:
                # run until user exit!
                self.user()

    def runN(self, periods=DEF_TIME):
        for mbr in self.members:
            if self.is_mbr_comp(mbr):
                self.pop_hist.record_pop(mbr, self.pop_count(mbr))

        self.time.members = self.members  # so members are always in sync
        if DEBUG:
            # ensure we aren't getting a copy!
            assert self.time.members is self.members
        self.time(periods)
        
    def plot(self):
        """
        Show where agents are in graphical form.
        """
        plot_type = self.plot_type
        
        #TODO: implement line graph
        if plot_type == "LN":
            pass #return super().plot()
        elif plot_type == "SC":
            data = self.plot_data()
            self.scatter_plot = disp.ScatterPlot(
                self.plot_title, data,
                int(self.width), int(self.height),
                anim=True, data_func=self.plot_data,
                # TODO: hardcode is_headless to False for now
                is_headless=self.headless()
                )
            self.image_bytes = self.scatter_plot.show()
            return self.image_bytes
        
    def plot_data(self):
        data = {}
        for var in self.members:
            data[var] = {}
            # matplotlib wants a list of x coordinates, and a list of y
            # coordinates:
            data[var][X] = []
            data[var][Y] = []
            # TODO: define colors in env?
            #data[var]["color"] = self.agents.get_var_color(var)
            current_var = self.members[var]
            for agent in current_var:
                current_agent_pos = current_var[agent].pos
                if current_agent_pos is not None:
                    (x, y) = current_agent_pos
                    data[var][X].append(x)
                    data[var][Y].append(y)
        return data
    
    def headless(self):
        if not disp.plt_present:
            self.user.tell("ERROR: No graphing package installed")
            return
        headless = False
        user_type = os.getenv("user_type", TERMINAL)
        if user_type == WEB:
            headless = True
        return headless