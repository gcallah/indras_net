"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
This module contains the base classes for agent-based modeling in Indra.
"""

from abc import abstractmethod
from collections import deque, OrderedDict
import itertools
import copy
import time
import logging
import pdb
import random
import getpass
import IPython
import networkx as nx
import node
import prop_args as pa
import display_methods as disp

MAX_ZERO_PER = 8


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
        """
        Note our environment.
        """
        self.env = env


    def pprint(self):
        """
        Print out me in a nice format.
        """
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


    def survey_env(self, universal):
        """
        Return a list of all prehended entities
        in env.
        """
        #logging.debug("scanning env for " + universal)
        print("scanning env for " + universal)
        prehended = []
        prehends = node.get_prehensions(prehender=node.get_node_type(self),
                                        universal=universal)
        print("Got prehends of: " + str(prehends))
        if not prehends == None:
            for pre_type in prehends:
                some_pres = self.env.get_agents_of_var(pre_type)
                prehended.extend(some_pres)
        return prehended


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
        if(self.utype in [User.TERMINAL, User.IPYTHON,
                          User.IPYTHON_NB]):
            return input(msg)


class AgentPop(Entity):

    """
    Holds our collection of agents and a sub-graph
    of their relationships.
    This should implement list functions.
    """

    def __init__(self, name):
        super().__init__(name)
        self.varieties = OrderedDict()
        self.graph = nx.Graph()
        self.num_zombies = 0


    def __iter__(self):
        alists = []
        for var in self.varieties_iter():
            alists.append(self.varieties[var]["agents"])
        return itertools.chain(*alists)


    def __len__(self):
        l = 0
        for var in self.varieties_iter():
            l += len(self.varieties[var]["agents"])
        return l


    def __reversed__(self):
        return reversed(list(self.__iter__()))


    def varieties_iter(self):
        """
        Allows iteration over the varieties of agents.
        """
        return iter(self.varieties)


    def variety_iter(self, var):
        """
        Allows iteration over the agents of one variety
        """
        return iter(self.varieties[var]["agents"])


    def append(self, agent):
        """
        Appends to agent list.
        """
        var = node.get_node_type(agent)
        logging.debug("Adding " + agent.__str__()
                      + " of variety " + var)

        if var in self.varieties:
            self.varieties[var]["agents"].append(agent)
        else:
            self.varieties[var] = {"agents": [agent],
                                   "pop_of_note": 0,
                                   "pop_hist": [],
                                   "zombies": [],
                                   "zero_per": 0}
            self.graph.add_edge(self, var)

        if len(self.varieties[var]["zombies"]) < self.num_zombies:
            self.varieties[var]["zombies"].append(copy.copy(agent))
# we link each agent to the variety
# so we can show their relationship
        self.graph.add_edge(var, agent)


    def remove(self, agent):
        """
        Removes from agent list.
        """
        logging.debug("Removing edge between AgentPop and "
                      + agent.name)
        var = node.get_node_type(agent)
        self.varieties[var]["agents"].remove(agent)
        self.graph.remove_edge(var, agent)


    def join_agents(self, a1, a2):
        """
        Add a graph edge between agents.
        """
        self.graph.add_edge(a1, a2)


    def agent_random_iter(self):
        """
        Loop through agents in random order.
        """
        agents = list(self.__iter__())
        random.shuffle(agents)
        return iter(agents)
        

    def contains(self, var):
        """
        Do we have this sort of thing in our env?
        """
        return var in self.varieties


    def get_agents_of_var(self, var):
        """
        Return all agents of type var.
        """
        if var in self.varieties:
            return self.varieties[var]["agents"]
        else:
            return None


    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return len(self.varieties[var]["agents"])


    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        var = node.get_node_type(agent)
        return self.get_pop(var)


    def get_pop_hist(self):
        """
        Make a list containing the population history
        for each var in varieties.
        """
        pop_hist = {}
        for var in self.varieties:
            pop_hist[var] = self.varieties[var]["pop_hist"]
        return pop_hist


    def get_pop_of_note(self, var):
        """
        Return the value of pop_of_note for 'var'.
        """
        return self.varieties[var]["pop_of_note"]


    def change_pop_of_note(self, var, change):
        """
        Change the value of pop_of_note by 'change.'
        """
        self.varieties[var]["pop_of_note"] += change


    def append_pop_hist(self, var, pop):
        """
        Add the most recent pop to pop_hist.
        """
        self.varieties[var]["pop_hist"].append(pop)


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
                        self.append(copy.copy(agent))
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
        """
        Find an agent by name.
        """
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None


    def get_agents_of_var(self, var):
        """
        Return all agents of type 'var'.
        """
        return self.agents.get_agents_of_var(var)


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
        """
        Invoke the python debugger.
        """
        pdb.set_trace()


    def ipython(self):
        """
        Kick off iPython.
        """
        IPython.start_ipython(argv=[])


    def eval_code(self):
        """
        Evaluate a line of code.
        """
        eval(self.user.ask("Type a line of code to run: "))


    def list_agents(self):
        """
        List all agents in env.
        """
        self.user.tell("Active agents in environment:")
        for agent in self.agents:
            self.user.tell(agent.name
                           + " with a goal of "
                           + agent.goal)


    def add(self):
        """
        Add a new agent to the env.
        """
        exec("import " + self.props.get("model")
             + " as m")
        constr = self.user.ask("Enter constructor for agent to add: ")
        new_agent = eval("m." + constr)
        self.add_agent(new_agent)


    def agnt_inspect(self):
        """
        View (and possibly alter) an agent's data.
        """
        name = self.user.ask(
            "Type the name of the agent to inspect: ")
        agent = self.find_agent(name.strip())
        if agent == None:
            self.user.tell("No such agent")
        else:
            agent.pprint()
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
            y_n = self.user.ask("Change a field's value in "
                                + entity.name
                                + "? (y/n) "
                                + "(Only str, float, and int supported.)")
            if y_n in ["Y", "y"]:
                field = self.user.ask("Which field? ")
                nval = self.user.ask("Enter new value for "
                                     + field + ": ")
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
        """
        Step period-by-period through agent actions.
        """
        self.period += 1

# agents might be waiting to be born
        if self.womb != None:
            for agent in self.womb:
                self.add_agent(agent)
            del self.womb[:]

# there might be state-setting to do before acting
        if self.preact:
            self.preact_loop()

# now have everyone act in random order
        self.act_loop()

# there might be cleanup to do after acting
        if self.postact:
            self.postact_loop()
 

    def act_loop(self):
        """
        Loop through randomly through agents calling their act() func.
        """
        for agent in self.agents.agent_random_iter():
            agent.act()


    def preact_loop(self):
        """
        Loop through agents calling their preact() func.
        """
        for agent in self.agents:
            agent.preact()


    def postact_loop(self):
        """
        Loop through agents calling their postact() func.
        """
        for agent in self.agents:
            agent.postact()


    def draw_graph(self):
        """
        Draw a graph!
        """
        choice = self.user.ask_for_ltr("Draw graph for "
                                       + "(a)gents; (e)nvironment; "
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

        pop_hist = self.agents.get_pop_hist()

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
        return self.agents.get_pop(var)


    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        return self.agents.get_my_pop(agent)


ADD_MODE = "a"
CODE_MODE = "c"
DBUG_MODE = "d"
ENV_MODE = "e"
GRPH_MODE = "g"
INSP_MODE = "i"
LIST_MODE = "l"
PROP_MODE = "o"
PLOT_MODE = "p"
QUIT_MODE = "q"
RUN_MODE = "r"
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
            disp_text = subm + ": "
            for item in self.submenus[subm]:
                disp_text = disp_text + item + " | "
# remove the final menu item separator:
            disp_text = disp_text.rstrip("| ")
            if self.env.user.utype == User.IPYTHON_NB:
                pass
#                disp_text = "<strong>" + disp_text + "</strong>"
            self.env.user.tell(disp_text)

        choice = self.env.user.ask_for_ltr(
            "Choose one of the above and press Enter: ")
        if len(choice) == 0:
            choice = STEP_MODE
        ret = self.choices[choice]()
        return ret


