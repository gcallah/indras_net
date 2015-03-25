"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
plt.ion()


colors = ['b', 'r', 'g', 'y', 'm', 'c', 'k']
NUM_COLORS = 7
X = 0
Y = 1


def display_line_graph(title, data, data_points):
    """
    Display a simple matplotlib line graph.
    The data is a dictionary with the label
    as the key and a list of numbers as the
    thing to graph.
    data_points is the length of the x-axis.
    """

    _fig, ax = plt.subplots()
    x = np.arange(0, data_points)

    for lbl, nums in data.items():
        y = np.array(nums)
        ax.plot(x, y, linewidth=2, label=lbl, alpha=1.0)

    ax.legend()
    ax.set_title(title)
    plt.show()


class ScatterPlot():
    """
    We are going to use a class here to save state for our animation
    """

    def __init__(self, title, varieties, width, height,
                 anim=True, data_func=None):
        """
        Setup a scatter plot.
        varieties contains the different types of
        entities to show in the plot, which
        will get assigned different colors
        """
        self.scats = None
        self.anim = anim
        self.data_func = data_func

        fig, ax = plt.subplots()
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        self.create_scats(varieties)
        ax.legend()
        ax.set_title(title)
        plt.grid(True)

        if anim:
            animation.FuncAnimation(fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    def show(self):
        """
        Display the plot.
        """
        plt.show()

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

    def get_arrays(self, varieties, var):
        x_array = np.array(varieties[var][X])
        y_array = np.array(varieties[var][Y])
        return (x_array, y_array)

    def create_scats(self, varieties):
        self.scats = []
        i = 0
        for var in varieties:
            color = varieties[var]["color"]
            if color is None:
                color = colors[i % NUM_COLORS]
            (x_array, y_array) = self.get_arrays(varieties, var)
            if len(x_array) <= 0:  # no data to graph!
                next
            elif len(x_array) != len(y_array):
                logging.debug("Array length mismatch in scatter plot")
                next
            scat = plt.scatter(x_array, y_array,
                               c=color, label=var,
                               alpha=1.0, marker="8",
                               edgecolors='none', s=32)
            self.scats.append(scat)
            i += 1
