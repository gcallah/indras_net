"""
menu.py
A menuing class.
The intention is that eventually this menu can be text or GUI based,
depending upon the user's environment.
It allows the addition of submenus at any depth available
memory will allow.
"""

# import logging
from collections import OrderedDict
import indra.node as node


class Menu(node.Node):
    """
    Menu items off the main menu or a sub-menu.
    """

    def __init__(self, name, env):
        super().__init__(name)
        self.env = env
        self.menu_items = OrderedDict()
        self.def_act = None

    def add_menu_item(self, letter, item, default=False):
        """
        Add an item to the this menu.
        """
        self.menu_items[letter] = item
        if default:
            self.def_act = item.act

    def act(self):
        """
        What to do when menu is selected.
        """
        return self.display()

    def display(self):
        """
        Display the menu.
        """
        disp_text = ""
        for _ltr, item in self.menu_items.items():
            disp_text += str(item) + " | "
        disp_text = disp_text.rstrip(" | ")
        self.env.user.tell(disp_text)

        choice = self.env.user.ask_for_ltr(
            "Choose one of the above and press Enter: ")
        if choice in self.menu_items:
            self.menu_items[choice].act()
        elif self.def_act is not None:
            self.def_act()
        else:
            pass


class MenuLeaf(node.Node):
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
    Our basic menu.
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
        self.edit.add_menu_item("i",
                                MenuLeaf("(i)nspect agent",
                                         e.agnt_inspect))
        self.edit.add_menu_item("e",
                                MenuLeaf("inspect (e)nv", e.env_inspect))

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
        self.tools.add_menu_item("r", MenuLeaf("(r)un", e.cont_run))
        self.tools.add_menu_item("d", MenuLeaf("(d)ebug", e.debug))
        self.tools.add_menu_item("i", MenuLeaf("(i)Python", e.ipython))
