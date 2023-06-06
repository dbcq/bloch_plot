"""Bloch sphere visualisation example using bloch_plot.py"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from bloch_plot import to_bloch_coords, basic_bloch_sphere, plot_coords, animate_coords

# Define statevector
statevector_1 = np.array([0, 1])

# Plot one statevector
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax = basic_bloch_sphere(ax, show_equator=True)

plot_coords(ax, to_bloch_coords(statevector_1), colors=['k'])
ax.view_init(elev=10., azim=-45, )

plt.savefig('bloch_sphere.png')

# Clear figure
plt.clf()

## Animate two sets of statevectors
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=10., azim=-45, )
ax = basic_bloch_sphere(ax, show_equator=True)

# Define two sets of statevectors
init_1 = np.array([1, 1]) / np.sqrt(2)
init_2 = np.array([2, 1]) / np.sqrt(5)

rotation_statevectors_1 = np.array([
    init_1 * [1, np.exp(1j * theta)] for theta in np.linspace(0, 2 * np.pi, 100)
])

rotation_statevectors_2 = np.array([
    init_2 * [1, np.exp(1j * theta)] for theta in np.linspace(0, 2 * np.pi, 100)
])

bloch_coords_1 = np.array([to_bloch_coords(statevector) for statevector in rotation_statevectors_1])
bloch_coords_2 = np.array([to_bloch_coords(statevector) for statevector in rotation_statevectors_2])

both_coords = np.array([bloch_coords_1, bloch_coords_2])

# Animate
ani = animate_coords(
    fig, 
    ax, 
    both_coords, 
    show_equator=True, 
    show_initial=True,
    label_steps=True, 
    colors=['r', 'g'],
    loop=True
)

f = 'animation.gif'
writerGif = PillowWriter(fps=20)
ani.save(f, writer=writerGif)
