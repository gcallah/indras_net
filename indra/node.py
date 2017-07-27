"""
node.py
A very basic class implementing some thing at the bottom of our
net of objects, such as being a node in a graph.
"""

# import logging
import inspect
import networkx as nx
import indra.display_methods as disp

UNIVERSAL = "universal"

indras_net = nx.Graph()


def get_class_name(genera):
    return genera.__name__


class Node():
    """
    Contains a name and a graph.
    """

    class_graph = nx.Graph()  # we are going to graph our class hierarchy
    node_added = False

    @classmethod
    def class_draw(cls):
        """
        This draws our class hierarchy.
        """
        if not disp.plt_present:
            return

        if cls.class_graph is not None:
            disp.draw_graph(cls.class_graph, "Class Hierarchy",
                            hierarchy=True, root=Node.__name__)

    @classmethod
    def connect_to_class_tree(cls):
        for c in inspect.getmro(cls):
            if c != cls:
                if c.__name__ not in Node.class_graph:
                    c.connect_to_class_tree()
                    break
                else:
                    Node.class_graph.add_edge(get_class_name(c),
                                              get_class_name(cls))
                    return
        cls.connect_to_class_tree()  # call until all upper classes are in

    def __init__(self, name):
        self.name = name
# every node is potentially a graph itself
        self.graph = None
        self.ntype = self.__class__.__name__
        if not Node.node_added:
            Node.class_graph.add_node(Node.__name__)
        if self.ntype not in Node.class_graph:
            self.__class__.connect_to_class_tree()

    def __str__(self):
        return self.name

    def draw(self):
        """
        Every node should have some way to draw itself.
        The default is to draw a graph.
        Other types of nodes will need different draw functions.
        """
        if not disp.plt_present:
            return

        if self.graph is not None:
            disp.draw_graph(self.graph, self.name)

    def display(self):
        """
        Every node should have some way to display itself.
        The difference between draw and display:
        Display makes the object show up on screen.
        Draw reveals the object's structure (such
        as graphing its components).
        """
        pass

    def debug_info(self):
        """
        Relevant debugging info.
        """
        s = "name: " + self.name + "\nntype: " + self.ntype
        return s

    def get_type(self):
        """
        Returns node's type.
        By default, this is its class name.
        """
        return self.ntype

    def set_type(self, new_type):
        """
        Change node's type.
        Use caution: A lot depends on this field!
        In particular, AgentPop uses it to sort agents.
        """
        self.ntype = new_type

    def to_json(self):
        return {"name": self.name}


class Universals(Node):
    """
    Our universals, the things which relate instances or classes.
    This is not implemented at the moment.
    """

    universals_graphed = False

    def __init__(self):
        super().__init__("Universals")
        self.unis = {}
        self.graph = nx.MultiDiGraph()
        if not Universals.universals_graphed:
            pass

    def add_universal(self, uni):
        """
        We want to be able to view all
        univeral relationships at a glance,
        so we will store them here
        """
        self.unis[uni] = []

universals = Universals()
