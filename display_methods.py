"""
Filename: display_methods.py Author: Gene Callahan
"""

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt


colors = ['b', 'r', 'g', 'y', 'm', 'c']
NUM_COLORS = 6


def display_line_graph(title, data, data_points):

    fig, ax = plt.subplots()
    x = np.arange(0, data_points)

    for lbl, nums in data.items():
        y = np.array(nums)
        al = len(y)
        ax.plot(x, y, linewidth=2, label=lbl, alpha=0.8)

    ax.legend()
    ax.set_title(title)
    plt.show()


def display_scatter_plot(title, varieties):

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


