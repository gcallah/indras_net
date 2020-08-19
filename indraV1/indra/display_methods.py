"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""
from functools import wraps
from math import ceil
import numpy as np
import networkx as nx
import logging
import io
from indra.prop_args2 import user_type
plt_present = True

try:
    import matplotlib as mpl
    if user_type == "Web browser":  # you can change this to right value!
        mpl.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    plt.ion()
except ImportError:
    plt_present = False

global imageIO

anim_func = None

BLUE = 'b'
RED = 'r'
GREEN = 'g'
YELLOW = 'y'
MAGENTA = 'm'
CYAN = 'c'
BLACK = 'k'
WHITE = 'w'
colors = [BLUE, RED, GREEN, YELLOW, MAGENTA, CYAN, BLACK, WHITE]
NUM_COLORS = len(colors)
X = 0
Y = 1

def expects_plt(fn):
    """
    Should be used to decorate any function that uses matplotlib's pyplot.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not plt_present:
            print(f"cannot plot with {fn.__qualname__}: matplotlib's pyplot is not installed")
            return
        return fn(*args, **kwargs)
    return wrapper


def hierarchy_pos(graph, root, width=1., vert_gap=0.2, vert_loc=0,
                  xcenter=0.5, pos=None, parent=None):
        """
        This is an attempt to get a tree graph from networkx.
        If there is a cycle that is reachable from root, then this will
        infinitely recurse.
        graph: the graph
        root: the root node of current branch
        width: horizontal space allocated for this branch
                - avoids overlap with other branches
        vert_gap: gap between levels of hierarchy
        vert_loc: vertical location of root
        xcenter: horizontal location of root
        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch.
        """
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = graph.neighbors(root)
        if parent is not None:
            neighbors.remove(parent)
        n_len = len(neighbors)
        dx = 0
        if n_len != 0:
            dx = width / n_len
            nextx = xcenter - width / 2 + dx / 2
            for neighbor in neighbors:
                pos = hierarchy_pos(graph, neighbor, width=dx,
                                    vert_gap=vert_gap,
                                    vert_loc=vert_loc-vert_gap,
                                    xcenter=nextx, pos=pos, parent=root)
                nextx += dx
        return pos


@expects_plt
def draw_graph(graph, title, hierarchy=False, root=None):
    """
    Drawing networkx graphs.
    graph is the graph to draw.
    hierarchy is whether we should draw it as a tree.
    """
    pos = None
    plt.title(title)
    if hierarchy:
        pos = hierarchy_pos(graph, root)
    nx.draw(graph, pos=pos, with_labels=True)
    plt.show()


def get_color(var, i):
    color = None
    if "color" in var:
        color = var["color"]
    if color is None:
        color = colors[i % NUM_COLORS]
    return color


def assemble_lgraph_data(key, values, color, data=None):
    # put our data in right form for line graph
    if data is None:
        data = {}
    data[key] = {}
    data[key]["data"] = values
    data[key]["color"] = color
    return data

class BarGraph():
    def __init__(self, title, varieties, data_points,
                 anim=False, data_func=None, is_headless=False, legend_pos=4):
        
        global anim_func
        self.title = title
        self.anim = anim
        self.data_func = data_func
        for i in varieties:
            data_points = len(varieties[i]["data"])
            break
        self.draw_graph(data_points, varieties)
        self.headless = is_headless

        if anim and not self.headless:
            anim_func = animation.FuncAnimation(self.fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    @expects_plt
    def draw_graph(self, data_points, varieties):
        """
        Draw all elements of the graph.
        """

        self.fig, self.ax = plt.subplots()
        
        x = np.arange(1, len(data_points) + 1)

        self.create_bars(x, self.ax, varieties)
        self.ax.legend()
        self.ax.set_title(self.title)
    
    @expects_plt
    def create_bars(self,x,ax,varieties):
        bar_coordinates = 0;
        for i, var in enumerate(varieties):
            data = varieties[var]["data"]
            color = get_color(varieties[var], i)
            y = np.array(data), 
            ax.bar(x + bar_coordinates, label=var, c=color, width=0.25)
            bar_coordinates += 0.25

    @expects_plt
    def show(self):
        """
        Display the barGraph.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    @expects_plt
    def update_plot(self, i):
        """
        This is our animation function.
        For line graphs, redraw the whole thing.
        """
        plt.clf()
        (data_points, varieties) = self.data_func()
        self.draw_graph(data_points, varieties)
        self.show()


class LineGraph():
    """
    We create a class here to save state for animation.
    Display a simple matplotlib line graph.
    The data is a dictionary with the label
    as the key and a list of numbers as the
    thing to graph.
    data_points is the length of the x-axis.
    """

    def __init__(self, title, varieties, data_points,
                 anim=False, data_func=None, is_headless=False, legend_pos=4):
        global anim_func

        self.title = title
        self.anim = anim
        self.data_func = data_func
        for i in varieties:
            data_points = len(varieties[i]["data"])
            break
        self.draw_graph(data_points, varieties)
        self.headless = is_headless

        if anim and not self.headless:
            anim_func = animation.FuncAnimation(self.fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    @expects_plt
    def draw_graph(self, data_points, varieties):
        """
        Draw all elements of the graph.
        """
        self.fig, self.ax = plt.subplots()
        x = np.arange(0, data_points)
        self.create_lines(x, self.ax, varieties)
        self.ax.legend()
        self.ax.set_title(self.title)

    def create_lines(self, x, ax, varieties):
        """
        Draw just the data portion.
        """
        self.lines = []
        for i, var in enumerate(varieties):
            data = varieties[var]["data"]
            color = get_color(varieties[var], i)
            y = np.array(data)
            ax.plot(x, y, linewidth=2, label=var, alpha=1.0, c=color)

    @expects_plt
    def show(self):
        """
        Display the plot.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    @expects_plt
    def update_plot(self, i):
        """
        This is our animation function.
        For line graphs, redraw the whole thing.
        """
        plt.clf()
        (data_points, varieties) = self.data_func()
        self.draw_graph(data_points, varieties)
        self.show()


class ScatterPlot():
    """
    We are going to use a class here to save state for our animation
    """

    def update_plot(self, i):
        """
        This is our animation function.
        """
        if self.scats is not None:
            for scat in self.scats:
                if scat is not None:
                    scat.remove()
        varieties = self.data_func()
        self.create_scats(varieties)
        return self.scats

    @expects_plt
    def __init__(self, title, varieties, width, height,
                 anim=True, data_func=None, is_headless=False, legend_pos=4):
        """
        Setup a scatter plot.
        varieties contains the different types of
        entities to show in the plot, which
        will get assigned different colors
        """
        global anim_func

        self.scats = None
        self.anim = anim
        self.data_func = data_func
        self.s = ceil(4096 / width)
        self.headless = is_headless

        fig, ax = plt.subplots()
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        self.create_scats(varieties)
        ax.legend(loc = legend_pos)
        ax.set_title(title)
        plt.grid(True)

        if anim and not self.headless:
            anim_func = animation.FuncAnimation(fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    @expects_plt
    def show(self):
        """
        Display the plot.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    def get_arrays(self, varieties, var):
        x_array = np.array(varieties[var][X])
        y_array = np.array(varieties[var][Y])
        return (x_array, y_array)

    @expects_plt
    def create_scats(self, varieties):
        self.scats = []
        for i, var in enumerate(varieties):
            (x_array, y_array) = self.get_arrays(varieties, var)
            if len(x_array) <= 0:  # no data to graph!
                next
            elif len(x_array) != len(y_array):
                logging.debug("Array length mismatch in scatter plot")
                next
            color = get_color(varieties[var], i)
            scat = plt.scatter(x_array, y_array,
                               c=color, label=var,
                               alpha=1.0, marker="8",
                               edgecolors='none', s=self.s)
            self.scats.append(scat)
