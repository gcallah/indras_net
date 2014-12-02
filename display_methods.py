"""
Filename: display_methods.py
Author: Gene Callahan
"""

import numpy as np
import matplotlib.pyplot as plt


def display_line_graph(title, data, data_points):

    fig, ax = plt.subplots()
    x = np.arange(0, data_points)

    for lbl, nums in data.items():
        y = np.array(nums)
        al = len(y)
        ax.plot(x, y, linewidth=2, label=lbl, alpha=0.6)

    ax.legend()
    ax.set_title(title)
    plt.show()

