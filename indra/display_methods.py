"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


colors = ['b', 'r', 'g', 'y', 'm', 'c']
NUM_COLORS = 6


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
        ax.plot(x, y, linewidth=2, label=lbl, alpha=0.8)

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

    def update_plot(i):
        """
        This is our animation function.
        """
        varieties = data_func()
        for var, scat in zip(varieties, scats):
            data_array = get_array(varieties, var)
            scat.set_offsets(data_array)
        return scats

    def get_array(varieties, var):
        x_arr = np.array(varieties[var]["x"])
        y_arr = np.array(varieties[var]["y"])
        return {"x": x_arr, "y": y_arr}

    fig, ax = plt.subplots()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    scats = []
    i = 0
    for var in varieties:
        color = colors[i % NUM_COLORS]
        data_array = get_array(varieties, var)
        scat = plt.scatter(data_array,
                           c=color, label=var,
                           alpha=1.0, marker="8",
                           edgecolors='none')
        scats.append(scat)
        i += 1

    ax.legend()
    ax.set_title(title)
    plt.grid(True)

    if anim:
        animation.FuncAnimation(fig,
                                update_plot,
                                frames=1000,
                                interval=1000,
                                blit=False)

    plt.show(block=False)
