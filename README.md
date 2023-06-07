# bloch_plot

Simple package for plotting and animations with the Bloch sphere.

## Installation

`cd` into `bloch_plot` directory and run:

```
pip install -e .
```

## Usage

```python
import numpy as np
from matplotlib import pyplot as plt
from bloch_plot import to_bloch_coords, basic_bloch_sphere, plot_coords

states = np.array([[1, 0], [1/np.sqrt(2), 1/np.sqrt(2)]])
coords = np.array([to_bloch_coords(state) for state in states])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

basic_bloch_sphere(ax, show_equator=True)
plot_coords(ax, coords, colors=['r', 'b'])

plt.show()
```

See `examples/example_bloch_visualisation.py` for an animated example.
