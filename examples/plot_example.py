"""Bloch sphere visualisation example using bloch_plot.py"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from bloch_plot import to_bloch_coords, basic_bloch_sphere, plot_coords, animate_coords

## Plot one statevector
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax = basic_bloch_sphere(ax, show_equator=True)

# Define statevector
statevector_1 = np.array([0, 1])

plot_coords(ax, to_bloch_coords(statevector_1), colors=["k"])
ax.view_init(
    elev=10.0,
    azim=-45,
)

plt.savefig("imgs/bloch_sphere.png", bbox_inches="tight")
