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
        logging.debug("scanning env for " + universal)
        prehended = []
        prehends = node.get_prehensions(prehender=node.get_node_type(self),
                                        universal=universal)
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

    
    def set_num_zombies(self, num):
        self.num_zombies = num


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


    class AgentRandomIter:
        """
        Iterate randomly through our agents.
        Eventually this should be made generic so it can 
        randomly iterate through anything.
        """
        def __init__(self, agents):
            self.i = 0
            self.agents = agents
            self.indices = list(range(len(agents)))
            random.shuffle(self.indices)


        def __iter__(self):
            return self


        def __next__(self):
            """
            Return the next element or raise exception.
            """
            if self.i < len(self.indices):
                # get an agent!
                agent = self.agents.element_at(self.indices[self.i])
                self.i += 1
                return agent
            else:
                raise StopIteration()


    def agent_random_iter(self):
        """
        Loop through agents in random order.
        """
        return AgentPop.AgentRandomIter(self)


    def element_at(self, i):
        """
        Another way to treat the AgentPop as if it were really
        one big list.
        """
        if i < 0 or i > len(self):
            raise IndexError()
        else:
            for var in self.varieties_iter():
                l = len(self.varieties[var]["agents"])
                if i < l:
                    return self.varieties[var]["agents"][i]
                else:
                     i -= l


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
                while len(self.varieties[var]["zombies"]) < self.num_zombies:
                    agent = random.choice(self.varieties[var]["agents"])
                    self.varieties[var]["zombies"].append(copy.copy(agent))


    def remove(self, agent):
        """
        Removes from agent list.
        """
        logging.debug("Removing " + agent.name + " from agents")
        var = node.get_node_type(agent)
        self.varieties[var]["agents"].remove(agent)
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
        Return a string of results for possible display.
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
        self.disp_census = False
        self.model_nm = model_nm
        if model_nm is not None:
            self.props = pa.PropArgs.get_props(model_nm)
        else:
            self.props = None

        user_nm = getpass.getuser()
        self.props.set("user_name", user_nm)
        user_type = self.props.get("user_type", User.TERMINAL)
        self.user = User(user_nm, user_type)
        self.graph.add_edge(self, self.user)
        self.menu = MainMenu("Main Menu", self)
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
            self.user.tell("\nMain Menu; Period: " + str(self.period))

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
        self.census(disp=self.disp_census)

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

    def graph_agents(self):
        """
        Draw a graph of the agent relationships.
        """
        self.agents.draw()


    def graph_env(self):
        """
        Draw a graph of the env's relationships.
        """
        self.draw()


    def graph_unv(self):
        """
        Draw a graph of the universal relationships.
        """
        node.universals.draw()


    def keep_running(self):
        """
        Placeholder
        """
        return True


    def view_pop(self):
        """
        Graph our population levels.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
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
        self.user.tell("Returning to runtime environment.")
        exit(0)


    def contains(self, agent_type):
        """
        Do we have this sort of thing in our env?
        """
        return self.agents.contains(agent_type)


    def census(self, disp=True):
        """
        Take a census of what is in the env.
        """
        results = self.agents.census()
        if disp:
            self.user.tell("Populations in period "
                           + str(self.period) + ":")
            self.user.tell(results)


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


class Menu(Entity):
    """
    Menu items off the main menu or a sub-menu.
    """

    def __init__(self, name, env):
        super().__init__(name)
        self.env = env
        self.choices = {}
        self.menu_items = OrderedDict()
        self.def_act = None
    

    def add_menu_item(self, letter, item, default=False):
        """
        Add an item to the this menu.
        """
        self.menu_items[item.name] = item
        self.choices[letter] = item.act
        if default:
            self.def_act = item.act


    def act(self):
        return self.display()


    def display(self):
        """
        Display the menu.
        """
        disp_text = ""
        for item in self.menu_items:
            disp_text += item + " | "
        disp_text = disp_text.rstrip(" | ")
        self.env.user.tell(disp_text)

        choice = self.env.user.ask_for_ltr(
            "Choose one of the above and press Enter: ")
        if choice in self.choices:
            self.choices[choice]()
        elif self.def_act is not None:
            self.def_act()
        else:
            pass


class MenuLeaf(Entity):
    """
    A leaf on the menu tree.
    """

    def __init__(self, name, func):
        super().__init__(name)
        self.func = func


    def act(self):
        return self.func()


class MainMenu(Menu):
    """
    Test out new menu.
    """

    def __init__(self, name, env):
        super().__init__(name, env)
        e = self.env

# file menu
        self.file = Menu("(f)ile", e)
        self.add_menu_item("f", self.file)
        self.file.add_menu_item("w", MenuLeaf("(w)rite props", e.pwrite))
        self.file.add_menu_item("e", MenuLeaf("(e)xamine log", e.disp_log))
        self.file.add_menu_item("q", MenuLeaf("(q)uit", e.quit))

# edit menu
        self.edit = Menu("(e)dit", e)
        self.add_menu_item("e", self.edit)
        self.edit.add_menu_item("a", MenuLeaf("(a)dd agent", e.add))
        self.edit.add_menu_item("i", MenuLeaf("(i)nspect agent", e.agnt_inspect))
        self.edit.add_menu_item("e", MenuLeaf("inspect (e)nv", e.env_inspect))

# view menu
        self.view = Menu("(v)iew", e)
        self.add_menu_item("v", self.view)
        self.view.add_menu_item("l", MenuLeaf("(l)ist agents", e.list_agents))
        self.view.add_menu_item("p", MenuLeaf("(p)roperties", e.disp_props))
        self.view.add_menu_item("v", MenuLeaf("(v)iew populations", e.view_pop))
# graph submenu
        self.graph = Menu("(g)raph", e)
        self.view.add_menu_item("g", self.graph)
        self.graph.add_menu_item("a", MenuLeaf("(a)gents", e.graph_agents))
        self.graph.add_menu_item("e", MenuLeaf("(e)nvironment", e.graph_env))
        self.graph.add_menu_item("u", MenuLeaf("(u)niversals", e.graph_unv))

# tools menu
        self.tools = Menu("(t)ools", e)
        self.add_menu_item("t", self.tools, default=True)
        self.tools.add_menu_item("s", MenuLeaf("(s)tep", e.step), default=True)
        self.tools.add_menu_item("r", MenuLeaf("(r)un", e.run))
        self.tools.add_menu_item("d", MenuLeaf("(d)ebug", e.debug))
        if e.user.utype == User.TERMINAL:
            self.tools.add_menu_item("i", MenuLeaf("(i)Python", e.ipython))


