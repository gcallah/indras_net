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
import indra.user as user

MENU_INDENT = 4


class Menu(node.Node):
    """
    Menu items off the main menu or a sub-menu.
    """

    def __init__(self, name, user, level=0):
        super().__init__(name)
        self.user = user
        self.menu_items = OrderedDict()
        self.def_act = None
        self.level = level

    def add_menu_item(self, letter, item, default=False):
        """
        Add an item to this menu.
        """
        self.menu_items[letter] = item
        if default:
            self.def_act = item.act

    def del_menu_item(self, letter):
        """
        Delete an item from this menu.
        """
        if letter in self.menu_items:
            del self.menu_items[letter]

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
        self.user.tell(disp_text, type=user.MENU,
                           indnt=MENU_INDENT * self.level)

        choice = self.user.ask_for_ltr(
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
