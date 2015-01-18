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

    fig, ax = plt.subplots()
    x = np.arange(0, data_points)

    for lbl, nums in data.items():
        y = np.array(nums)
        al = len(y)
        ax.plot(x, y, linewidth=2, label=lbl, alpha=0.8)

    ax.legend()
    ax.set_title(title)
    plt.show()


def display_scatter_plot(title, varieties, anim=False,
                            anim_func=None):
    """
    Display a scatter plot. We plan to
    add animation soon, thus the unused
    anim params.
    varieties is the different types of 
    entities to show in the plot, which
    will get assigned different colors
    """

    fig, ax = plt.subplots()
    
    i = 0
    for var in varieties:
        color = colors[i % NUM_COLORS]
        i += 1
        x = np.array(varieties[var]["x"])
        y = np.array(varieties[var]["y"])
        plt.scatter(x, y, c=color, label=var,
                       alpha=0.8, edgecolors='none')
    
    ax.legend()
    ax.set_title(title)
    plt.grid(True)
    
    plt.show(block=False)


