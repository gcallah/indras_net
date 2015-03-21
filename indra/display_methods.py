"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.ion()


colors = ['b', 'r', 'g', 'y', 'm', 'c']
NUM_COLORS = 6
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


def display_scatter_plot(title, varieties, width, height,
                         anim=False,
                         data_func=None):
    """
    Display a scatter plot.
    varieties contains the different types of
    entities to show in the plot, which
    will get assigned different colors
    """

    def get_arrays(varieties, var):
        x_array = np.array(varieties[var][X])
        y_array = np.array(varieties[var][Y])
        return (x_array, y_array)

    def create_scats(varieties):
        new_scats = []
        i = 0
        for var in varieties:
            color = colors[i % NUM_COLORS]
            (x_array, y_array) = get_arrays(varieties, var)
            scat = plt.scatter(x_array, y_array,
                               c=color, label=var,
                               alpha=1.0, marker="8",
                               edgecolors='none', s=32)
            new_scats.append(scat)
            i += 1
        return new_scats

    fig, ax = plt.subplots()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    scats = create_scats(varieties)
    ax.legend()
    ax.set_title(title)
    plt.grid(True)

    def update_plot(i):
        """
        This is our animation function.
        """
        #  plt.clf()
        if scats is not None:
            for scat in scats:
                scat.remove()
        varieties = data_func()
        scats = create_scats(varieties)
        return scats

    if anim:
        animation.FuncAnimation(fig,
                                update_plot,
                                frames=1000,
                                interval=500,
                                blit=False)

    plt.show()
