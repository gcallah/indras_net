"""
The default main menu for our ABMs.
"""

import networkx as nx
from indra.menu import Menu, MenuLeaf

class MainMenu(Menu):
    """
    Our basic menu.
    """

    def __init__(self, name, env):
        super().__init__(name, env.user)
        self.env = env
        e = self.env  # just a shorthand to make the following lines shorter
        self.graph = nx.Graph()

# file menu
        self.file = Menu("(f)ile", e.user, level=1)
        self.add_menu_item("f", self.file)
        self.file.add_menu_item("e", MenuLeaf("(e)xamine log", e.disp_log))
        self.file.add_menu_item("p", MenuLeaf("(p)opulation report", e.pop_report))
        self.file.add_menu_item("q", MenuLeaf("(q)uit", e.quit))
        self.file.add_menu_item("w", MenuLeaf("(w)rite props", e.pwrite))

# edit menu
        self.edit = Menu("(e)dit", e.user, level=1)
        self.add_menu_item("e", self.edit)
        self.edit.add_menu_item("a", MenuLeaf("(a)dd agent", e.add))
        self.edit.add_menu_item("i",
                                MenuLeaf("(i)nspect agent",
                                         e.agnt_inspect))
        self.edit.add_menu_item("e",
                                MenuLeaf("inspect (e)nv", e.env_inspect))

# view menu
        self.view = Menu("(v)iew", e.user, level=1)
        self.add_menu_item("v", self.view)
        self.view.add_menu_item("l", MenuLeaf("(l)ist agents",
                                              e.list_agents))
        self.view.add_menu_item("p", MenuLeaf("(p)roperties", e.disp_props))
        self.view.add_menu_item("v", MenuLeaf("(v)iew populations",
                                              e.view_pop))
# graph submenu
        self.graph = Menu("(g)raph", e.user, level=1)
        self.view.add_menu_item("g", self.graph)
        self.graph.add_menu_item("a", MenuLeaf("(a)gents", e.graph_agents))
        self.graph.add_menu_item("c", MenuLeaf("(c)lasses",
                                               e.graph_class_tree))
        self.graph.add_menu_item("e", MenuLeaf("(e)nvironment",
                                               e.graph_env))

# tools menu
        self.tools = Menu("(t)ools", e.user, level=1)
        self.add_menu_item("t", self.tools, default=True)
        self.tools.add_menu_item("s", MenuLeaf("(s)tep", e.step),
                                 default=True)
        self.tools.add_menu_item("n", MenuLeaf("run (n) steps", e.n_steps))
        self.tools.add_menu_item("d", MenuLeaf("(d)ebug", e.debug))
