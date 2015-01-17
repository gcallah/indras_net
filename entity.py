"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
This module contains the base classes for agent-based modeling in Indra.
"""

from abc import ABCMeta, abstractmethod
import time
import logging
import pprint
import pdb
import random
import getpass
import IPython
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, OrderedDict
import prop_args as pa


UNIVERSAL = "universal"

pp = pprint.PrettyPrinter(indent=4)


indras_net = nx.Graph()


def get_class_name(genera):
    return genera.__name__


def get_agent_type(agent):
    return get_class_name(type(agent))


def get_prehensions(prehender, universal):
    return universals.get_prehensions(prehender, universal)


def add_prehension(prehender, universal, prehended):
    prnr_name = get_class_name(prehender)
    prnd_name = get_class_name(prehended)
    universals.add_prehension(prnr_name, universal, prnd_name)


class Node():

    def __init__(self, name):
        self.name = name
        self.graph = None

    def draw(self):
        if self.graph is not None:
            nx.draw_networkx(self.graph)
            plt.show()


class Universals(Node):

    def __init__(self):
        self.name = "Universals"
        self.unis = {}
        self.graph = nx.MultiDiGraph()


    def add_universal(self, uni):
        """
        We want to be able to view all
        univeral relationships at a glance,
        so we will store them here
        """
        self.unis[uni] = [] # a list of prehensions


    def add_prehension(self, prehender, uni, prehended):
        """
        Adds a universal relationship between two classes
        """

        if uni not in self.unis:
            self.add_universal(uni)
        self.unis[uni].append([prehender, prehended])
        self.graph.add_edge(prehender, prehended,
                            universal=uni)


    def get_prehensions(self, prehender, uni):
        prehensions = []
        logging.debug("edges = " + str(self.graph.edges()))
        for etuple in self.graph.edges_iter(data=True):
            prehender = etuple[0]
            prehended = etuple[1]
            edge_data = etuple[2]
            prehension = edge_data[UNIVERSAL]
            if uni == prehension:
                logging.debug("Found our universal: " + uni)
                prehensions.append(prehended)
        logging.debug("prehensions = " + str(prehensions))
        return prehensions


universals = Universals()


class Entity(Node):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    """

    def __init__(self, name):
        super().__init__(name)
        self.prehensions = []
        self.env = None
# every entity is potentially a graph itself
        self.graph = None


    def __str__(self):
        return self.name

        
    def add_env(self, env):
        self.env = env


    def walk_graph_breadth_first(self, func, top):
        if top:
            func(self)
        for prehension in self.prehensions:
            func(prehension.prehended_entity)
        for prehension in self.prehensions:
            prehension.prehended_entity.walk_graph_breadth_first(func, 
                                                  False)


    def print_prehensions(self):
        for prehension in self.prehensions:
            print(prehension.prehended_entity.name 
                + " is my " + prehension.name)


    def pprint(self):
        for key, value in self.__dict__.items():
            print(key + " = " + str(value))


class Agent(Entity):

    """
    This class adds a goal to an entity
    and is the base for all other agents.
    """

    def __init__(self, name, goal=None):
        super().__init__(name)
        self.goal = goal


    @abstractmethod
    def act(self):
        pass

    def preact(self):
        pass
    
    def postact(self):
        pass
    

class User(Entity):
    """
    We will represent the user to the system as another entity.
    """

    # user types
    TERMINAL = "terminal"
    IPYTHON = "iPython"
    IPYTHON_NB = "iPython Notebook"


    def __init__(self, nm, type):
        super().__init__(nm)
        self.type = type


    def tell(self, msg):
        if self.type in [User.TERMINAL, User.IPYTHON, User.IPYTHON_NB]:
            print(msg)

    def ask_for_ltr(self, msg):
        choice = self.ask(msg)
        return choice.strip()

    def ask(self, msg):
        if self.type in [User.TERMINAL, User.IPYTHON, User.IPYTHON_NB]:
            return(input(msg))


class AgentPop(Entity):

    """
    Holds our collection of agents and a sub-graph
    of their relationships.
    """

    def __init__(self, name):
        super().__init__(name)
        self.agents = []
        self.graph = nx.Graph()


    def __iter__(self):
        return iter(self.agents)


    def __len__(self):
        return len(self.agents)


    def __reversed__(self):
        return reversed(self.agents)


    def append(self, agent):
        self.agents.append(agent)
# we link each agent to the name
#  just so we can show their relationship 
#  to this object
        self.graph.add_edge(self, agent)


    def remove(self, agent):
        self.agents.remove(agent)
        self.graph.remove_edge(self, agent)
        logging.debug("Removing edge between AgentPop and "
                + agent.name)

    def join_agents(self, a1, a2):
        self.graph.add_edge(a1, a2)


    def random_loop(self):
        indices = list(range(len(self.agents)))
        random.shuffle(indices)
        for i in indices:
            self.agents[i].act()


class Environment(Entity):

    """
    A basic environment allowing starting, stopping,
    stepping, inspection and editing of key objects,  etc.
    """

    prev_period = 0  # in case we need to restore state


    def __init__(self, name, preact=False, 
                    postact=False, model_nm=None):
        super().__init__(name)
        self.graph = nx.Graph()
        indras_net.add_node(self)
        pop_name = ""
        if model_nm:
            pop_name += model_nm + " "
        pop_name += "Agents" 
        self.agents = AgentPop(pop_name)
        self.graph.add_edge(self, self.agents)
        self.womb = []
        self.period = 0
        self.preact = preact
        self.postact = postact
        self.model_nm = model_nm
        if model_nm is not None:
            self.props = pa.PropArgs.get_props(model_nm)
        else:
            self.props = None

        user_nm = getpass.getuser()
        self.props.set("user_name", user_nm)
        user_type = self.props.get("user_type", User.IPYTHON)
        self.user = User(user_nm, user_type)
        self.graph.add_edge(self, self.user)
        self.menu = Menu(self)
        self.graph.add_edge(self, self.menu)
#        self.graph.add_edge(self, univesals)


    def add_agent(self, agent):
        self.agents.append(agent)
        agent.add_env(self)
    
    
    def join_agents(self, a1, a2):
        self.agents.join_agents(a1, a2)


    def add_child(self, agent):
        self.womb.append(agent)
        agent.add_env(self)


    def find_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None


    def run(self, resume=False):
        """
        This is the main menu loop for all models
        """

        if resume: self.period = Environment.prev_period
        else:      self.period = 0

        self.user.tell("Welcome, " + self.user.name)
        self.user.tell("Running in " + self.name)
        msg = self.menu.display()
        while msg is None:
            msg = self.menu.display()

        Environment.prev_period = self.period

        self.user.tell(msg)


    def add_menu_item(self, submenu, letter, text, func):
        """
        This func exists to screen the menu class from outside objects:
        no need for them to know more than the env
        """
        self.menu.add_menu_item(submenu, letter, text, func)


    def debug(self):
        pdb.set_trace()


    def ipython(self):
        IPython.start_ipython(argv=[])


    def eval_code(self):
        eval(self.user.ask("Type a line of code to run: "))


    def list_agents(self):
        self.user.tell("Active agents in environment:")
        for agent in self.agents:
            self.user.tell(agent.name 
                        + " with a goal of " + agent.goal)


    def add(self):
        exec("import " + self.props.get("model") 
                + " as m")
        constr = self.user.ask(
                    "Enter constructor for agent to add: ")
        new_agent = eval("m." + constr)
        self.add_agent(new_agent)


    def agnt_inspect(self):
        name = self.user.ask(
            "Type the name of the agent to inspect: ")
        agent = self.find_agent(name.strip())
        if agent == None: self.user.tell("No such agent")
        else: agent.pprint()
        self.edit_field(agent)


    def env_inspect(self):
        self.pprint()
        self.edit_field(self)


    def edit_field(self, entity):
        y_n = self.user.ask("Change a field's value in " + entity.name
                + "? (y/n) ")
        if y_n in ["Y", "y"]:
            field = self.user.ask("Which field? ")
            nval = self.user.ask("Enter new value for " + field + ": ")
            entity.__dict__[field] = nval


    def cont_run(self):
        self.user.tell(
            "Running continously; press Ctrl-c to halt!")
        time.sleep(3)
        try:
            while self.keep_running():
                step_msg = self.step()
                if step_msg is not None:
                    self.user.tell(step_msg)
                    break
        except KeyboardInterrupt:
            pass


    def pwrite(self):
        file_nm = self.user.ask("Choose file name: ")
        if self.props is not None:
            self.props.write(file_nm)


    def disp_log(self):

        MAX_LINES = 16

        logfile = self.props.get_logfile()

        if logfile is None:
            self.user.tell("No log file to examine!")

        last_n_lines = deque(maxlen=MAX_LINES) # for now hard-coded

        with open(logfile, 'rt') as log:
            for line in log:
                last_n_lines.append(line)

        self.user.tell("Displaying the last " + str(MAX_LINES)
                + " lines of logfile " + logfile)
        for line in last_n_lines:
            self.user.tell(line.strip())


    def step(self):
        self.period += 1

# agents might be waiting to be born       
        if self.womb != None:
            for agent in self.womb:
                self.add_agent(agent)
            del self.womb[:]  

# there might be state-setting to do before acting
        if(self.preact):
            self.preact_loop()

# now have everyone act in random order
        self.act_loop()
        
# there might be cleanup to do after acting
        if(self.postact):
            self.postact_loop()
        
    
    def act_loop(self):
        self.agents.random_loop()


    def preact_loop(self):
        for agent in self.agents:
            agent.preact()


    def postact_loop(self):
        for agent in self.agents:
            agent.postact()


    def draw_graph(self):
        choice = self.user.ask_for_ltr(
                "Draw graph for (a)gents; (e)nvironment?")
        if choice == "a":
            self.agents.draw()
        else:
            self.draw()


    def keep_running(self):
        return True

    def display(self):
        self.user.tell("Visualize not implemented in this model")

    def plot(self):
        self.user.tell("Plot not implemented in this model")

    def quit(self):
        return "Returning to runtime environment."


class Prehension():

    def __init__(self, name, entity):
        self.name   = name
        self.weight = 1.0;
        self.prehended_entity = entity


ADD_MODE  = "a"
CODE_MODE = "c"
DBUG_MODE = "d"
ENV_MODE  = "e"
GRPH_MODE = "g"
INSP_MODE = "i"
LIST_MODE = "l"
PLOT_MODE = "p"
QUIT_MODE = "q"
RUN_MODE  = "r"
STEP_MODE = "s"
VISL_MODE = "v"
WRIT_MODE = "w"
EXMN_MODE = "x"
IPYN_MODE = "y"


class Menu(Entity):

    def __init__(self, env):
        super().__init__("Main Menu")
        self.env = env
        self.choices = {}
        self.submenus = OrderedDict()
        self.submenus["File"] = OrderedDict()
        self.submenus["Edit"] = OrderedDict()
        self.submenus["View"] = OrderedDict()
        self.submenus["Tools"] = OrderedDict()

        e = self.env

# add default menu items:
        self.add_menu_item("File", WRIT_MODE, "(w)rite properties",
                            e.pwrite)
        self.add_menu_item("File", EXMN_MODE, "e(x)amine log file",
                            e.disp_log)
        self.add_menu_item("File", QUIT_MODE, "(q)uit", e.quit)
        self.add_menu_item("Edit", ADD_MODE, "(a)dd agent to env",
                            e.add)
        self.add_menu_item("Edit", INSP_MODE, "(i)nspect agent",
                            e.agnt_inspect)
        self.add_menu_item("Edit", ENV_MODE, "inspect (e)nvironment",
                            e.env_inspect)
        self.add_menu_item("View", LIST_MODE, "(l)ist agents",
                            e.list_agents)
        self.add_menu_item("View", GRPH_MODE, "(g)raph components",
                            e.draw_graph)
        self.add_menu_item("View", VISL_MODE, "(v)isualize",
                            e.display)
        self.add_menu_item("Tools", STEP_MODE, "(s)tep (default)",
                            e.step)
        self.add_menu_item("Tools", RUN_MODE, "(r)un", e.run)
        self.add_menu_item("Tools", DBUG_MODE, "(d)ebug", e.debug)
        if e.user.type == User.TERMINAL:
            self.add_menu_item("Tools", IPYN_MODE, "iP(y)thon",
                                e.ipython)


    def add_menu_item(self, submenu, letter, text, func):
        if submenu in self.submenus:
            self.submenus[submenu][text] = {
                    "letter": letter,
                    "func": func
                }
            self.choices[letter] = func


    def display(self):
        for subm in self.submenus:
            disp = subm + ": "
            for item in self.submenus[subm]:
                disp = disp + item + " | "
# remove the final menu item separator:
            disp = disp.rstrip("| ")
            if self.env.user.type == User.IPYTHON_NB:
                pass
#                disp = "<strong>" + disp + "</strong>"
            self.env.user.tell(disp)

        choice = self.env.user.ask_for_ltr(
            "Choose one of the above and press Enter: ")
        if len(choice) == 0:
            choice = STEP_MODE
        ret = self.choices[choice]()
        return ret


