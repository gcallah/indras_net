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
import node
from collections import deque, OrderedDict
import prop_args as pa


class Entity(node.Node):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    """

    def __init__(self, name):
        super().__init__(name)
        self.prehensions = []
        self.env = None

        
    def add_env(self, env):
        self.env = env


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
        """
        What agents do.
        """
        pass

    def preact(self):
        """
        What agents do before they act.
        """
        pass
    
    def postact(self):
        """
        What agents do after they act.
        """
        pass
    

class User(Entity):
    """
    We will represent the user to the system as another entity.
    """

    # user types
    TERMINAL = "terminal"
    IPYTHON = "iPython"
    IPYTHON_NB = "iPython Notebook"


    def __init__(self, nm, utype):
        super().__init__(nm)
        self.utype = utype


    def tell(self, msg):
        """
        Screen the details of output from models.
        """
        if self.utype in [User.TERMINAL, User.IPYTHON,
                        User.IPYTHON_NB]:
            print(msg)

    def ask_for_ltr(self, msg):
        """
        Screen the details of input from models.
        """
        choice = self.ask(msg)
        return choice.strip()

    def ask(self, msg):
        """
        Screen the details of input from models.
        """
        if self.utype in [User.TERMINAL, User.IPYTHON, User.IPYTHON_NB]:
            return(input(msg))


class AgentPop(Entity):

    """
    Holds our collection of agents and a sub-graph
    of their relationships.
    This should implement list functions.
    """

    def __init__(self, name):
        super().__init__(name)
        self.agents = []
        self.varieties = {}
        self.graph = nx.Graph()
        self.num_zombies = 0


    def __iter__(self):
        return iter(self.agents)


    def __len__(self):
        return len(self.agents)


    def __reversed__(self):
        return reversed(self.agents)


    def varieties_iter(self):
        """
        Allows iteration over the varieties of agents.
        """
        return iter(self.varieties)


    def append(self, agent):
        """
        Appends to agent list.
        """
        self.agents.append(agent)
        v = node.get_node_type(agent)
        logging.debug("Adding " + agent.__str__()
                + " of variety " + v)

        if v in self.varieties:
            self.varieties[v]["pop"] += 1
        else:
            self.varieties[v] = {"pop": 1,
                           "pop_of_note": 0,
                           "pop_hist": [],
                           "zombies": [],
                           "zero_per": 0}
        if len(self.varieties[v]["zombies"]) < self.num_zombies:
            self.varieties[v]["zombies"].append(copy.copy(agent))
# we link each agent to the name
#  just so we can show their relationship 
#  to this object
        self.graph.add_edge(self, agent)


    def remove(self, agent):
        """
        Removes from agent list.
        """
        self.agents.remove(agent)
        self.graph.remove_edge(self, agent)
        logging.debug("Removing edge between AgentPop and "
                + agent.name)
        s = node.get_node_type(agent)
        assert self.varieties[s]["pop"] > 0
        self.varieties[s]["pop"] -= 1


    def join_agents(self, a1, a2):
        """
        Add a graph edge between agents.
        """
        self.graph.add_edge(a1, a2)


    def random_loop(self):
        """
        Loop through agents in random order.
        """
        indices = list(range(len(self.agents)))
        random.shuffle(indices)
        for i in indices:
            self.agents[i].act()


    def contains(self, agent_type):
        """
        Do we have this sort of thing in our env?
        """
        return agent_type in self.varieties


    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return self.varieties[var]["pop"]


    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        var = node.get_node_type(agent)
        return self.get_pop(var)


    def get_pop_hist(pop_hist):
        for s in self.varieties:
            pop_hist[s] = self.varieties[s]["pop_hist"]


    def census(self):
        """
        Take a census of agents by variety.
        """
        ret = ""
        for v in self.varieties:
            pop = self.get_pop(v)
            ret += v + ": " + str(pop) + "\n"
            var = self.varieties[v]
            var["pop_hist"].append(pop)
            if pop == 0:
                var["zero_per"] += 1
                if var["zero_per"] >= MAX_ZERO_PER:
                    for agent in var["zombies"]:
                        self.add_agent(copy.copy(agent))
                    var["zero_per"] = 0
        return ret


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
        self.graph.add_edge(self, self.props)
        self.graph.add_edge(self, node.universals)


    def add_agent(self, agent):
        """
        Add an agent to pop.
        """
        self.agents.append(agent)
        agent.add_env(self)
    
    
    def join_agents(self, a1, a2):
        """
        Relate two agents.
        """
        self.agents.join_agents(a1, a2)


    def add_child(self, agent):
        """
        Put a child agent in the womb.
        """
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

        if resume:
            self.period = Environment.prev_period
        else:
            self.period = 0

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
        """
        View (and possibly alter) an agent's data.
        """
        name = self.user.ask(
            "Type the name of the agent to inspect: ")
        agent = self.find_agent(name.strip())
        if agent == None: self.user.tell("No such agent")
        else: agent.pprint()
        self.edit_field(agent)


    def env_inspect(self):
        """
        Have a look at (and possibly alter) the environment.
        """
        self.pprint()
        self.edit_field(self)


    def edit_field(self, entity):
        """
        Edit a field in an entity.
        """
        while True:
            y_n = self.user.ask(
                    "Change a field's value in " 
                    + entity.name
                    + "? (y/n) "
                    + "(Only str, float, and int supported.)")
            if y_n in ["Y", "y"]:
                field = self.user.ask("Which field? ")
                nval = self.user.ask(
                        "Enter new value for " + field + ": ")
                fld_type = type(entity.__dict__[field])
                if fld_type is int:
                    entity.__dict__[field] = int(nval)
                elif fld_type is float:
                    entity.__dict__[field] = float(nval)
                else:
                    entity.__dict__[field] = nval
            else:
                break


    def cont_run(self):
        """
        Run continuously.
        """
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
        """
        Write out the properties to a file.
        """
        file_nm = self.user.ask("Choose file name: ")
        if self.props is not None:
            self.props.write(file_nm)


    def disp_props(self):
        """
        Display current system properties.
        """
        self.user.tell(self.props.display())


    def disp_log(self):
        """
        Display last 16 lines of log file.
        """

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
        """
        Draw a graph!
        """
        choice = self.user.ask_for_ltr(
                "Draw graph for (a)gents; (e)nvironment; "
                + "(u)niversals?")
        if choice == "a":
            self.agents.draw()
        elif choice == "u":
            node.universals.draw()
        else:
            self.draw()


    def keep_running(self):
        """
        Placeholder
        """
        return True

        
    def display(self):
        """
        Default: Graph our population levels.
        """
        if self.period < 4:
            print("Too little data to display")
            return

        pop_hist = {}
        agents.get_pop_hist(pop_hist)

        disp.display_line_graph('Populations in '
                                + self.name,
                                pop_hist,
                                self.period)


    def plot(self):
        """
        Placeholder
        """
        self.user.tell("Plot not implemented in this model")


    def quit(self):
        """
        Leave this run.
        """
        return "Returning to runtime environment."


    def contains(self, agent_type):
        """
        Do we have this sort of thing in our env?
        """
        return self.agents.contains(agent_type)


    def census(self):
        """
        Take a census of what is in the env.
        """
        self.user.tell("Populations in period "
                        + str(self.period) + ":")
        self.user.tell(self.agents.census())


    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return self.agents.get_pop()


    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        return self.agents.get_my_pop()


ADD_MODE  = "a"
CODE_MODE = "c"
DBUG_MODE = "d"
ENV_MODE  = "e"
GRPH_MODE = "g"
INSP_MODE = "i"
LIST_MODE = "l"
PROP_MODE = "o"
PLOT_MODE = "p"
QUIT_MODE = "q"
RUN_MODE  = "r"
STEP_MODE = "s"
VISL_MODE = "v"
WRIT_MODE = "w"
EXMN_MODE = "x"
IPYN_MODE = "y"


class Menu(Entity):
    """
    Implements our basic menu: intended for text or GUI
    use.
    """

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
        self.add_menu_item("View", VISL_MODE, "(v)isualize data",
                            e.display)
        self.add_menu_item("Tools", STEP_MODE, "(s)tep (default)",
                            e.step)
        self.add_menu_item("View", PROP_MODE, "view pr(o)perties",
                            e.disp_props)
        self.add_menu_item("Tools", RUN_MODE, "(r)un", e.run)
        self.add_menu_item("Tools", DBUG_MODE, "(d)ebug", e.debug)
        if e.user.utype == User.TERMINAL:
            self.add_menu_item("Tools", IPYN_MODE, "iP(y)thon",
                                e.ipython)


    def add_menu_item(self, submenu, letter, text, func):
        """
        Add an item to the main menu.
        """
        if submenu in self.submenus:
            self.submenus[submenu][text] = {
                    "letter": letter,
                    "func": func
                }
            self.choices[letter] = func


    def display(self):
        """
        Display the menu.
        """
        for subm in self.submenus:
            disp = subm + ": "
            for item in self.submenus[subm]:
                disp = disp + item + " | "
# remove the final menu item separator:
            disp = disp.rstrip("| ")
            if self.env.user.utype == User.IPYTHON_NB:
                pass
#                disp = "<strong>" + disp + "</strong>"
            self.env.user.tell(disp)

        choice = self.env.user.ask_for_ltr(
            "Choose one of the above and press Enter: ")
        if len(choice) == 0:
            choice = STEP_MODE
        ret = self.choices[choice]()
        return ret


