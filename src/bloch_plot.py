import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib import rcParams

rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'text.latex.preamble': r'\usepackage{amsmath} \usepackage{amssymb} \usepackage{braket}'       
})

def to_bloch_coords(statevector):
    """Converts statevector to (u, v, w) Bloch basis coords
    
    Args:
        statevector (np.array): statevector of qubit

    Returns:
        list: [u, v, w] Bloch basis coords
    """
    rho = np.outer(statevector, statevector.conj())
    # print(rho)
    u = rho[1, 0] + rho[0, 1]
    v = 1j * (rho[0, 1] - rho[1, 0])
    w = rho[0, 0] - rho[1, 1]

    # print(np.sqrt(u**2 + v**2 + w**2))
    # print(u, v, w)
    return np.array([np.real(u), np.real(v), np.real(w)])

def basic_bloch_sphere(ax, show_equator=False):
    """Plots basic Bloch sphere with axes and unit sphere

    Args:
        ax (matplotlib.axes): axes to plot on (must have 3D projection)
        show_equator (bool, optional): whether to show equator. Defaults to False.

    Returns:
        matplotlib.axes: axes with Bloch sphere
    """

    # Set axes aspect and limits
    ax.set_box_aspect([1,1,1])
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)

    # Plot axes
    ax.plot([-1, 1], [0, 0], [0, 0], color='k', linewidth=1, alpha=0.5)
    ax.plot([0, 0], [-1, 1], [0, 0], color='k', linewidth=1, alpha=0.5)
    ax.plot([0, 0], [0, 0], [-1, 1], color='k', linewidth=1, alpha=0.5)
    ax.text(1, 0, 0, r'$\hat{x}$', fontsize=10)
    ax.text(0, 1, 0, r'$\hat{y}$', fontsize=10)
    ax.text(0, 0, 1, r'$\hat{z}$', fontsize=10)

    # Plot unit sphere
    phi, theta = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    ax.plot_wireframe(x, y, z, color="r", linewidth=0.5, alpha=0.5)
    ax.text(-0.05, 0, 1.2, r"$\ket{0}$")
    ax.text(-0.05, 0, -1.45, r"$\ket{1}$")

    # Plot equator
    if show_equator:
        r = np.linspace(0, 1, 100)
        th = np.linspace(0, 2*np.pi, 100)
        R, TH = np.meshgrid(r, th)
        Z = np.zeros_like(R)
        X = R*np.cos(TH)
        Y = R*np.sin(TH)
        ax.plot_surface(X, Y, Z, color="k", alpha=0.2)

    # Hide background
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Hide grid
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.set_axis_off()

    return ax


def plot_coords(ax, coords, colors=None, alpha=0.5):
    """Plots all N sets of coordinates in `coords` on Bloch sphere
    
    Args:
        ax (matplotlib.axes): axes to plot on (must have 3D projection)
        coords np.array: coordinates to plot (N, 3)
        colors (list, optional): colors for each coordinate. Defaults to None.
        alpha (float, optional): alpha value for coordinates. Defaults to 0.5.

    Returns:
        None (plots on ax inplace)
    """

    if len(coords.shape) == 1:
        coords = np.array([coords])

    for coord, c in zip(coords, colors):
        ax.quiver(
            0, 0, 0,
            coord[0], coord[1], coord[2],
            color=c, alpha=alpha, arrow_length_ratio=0.1
        )

    return


def animate_coords(fig, ax, coords, show_equator=False, colors=None, alpha=0.5, label_steps=True, show_initial=False, loop=True):
    """Animates N sets of coordinates on Bloch sphere

    Args:
        fig (matplotlib.figure): figure to plot on
        ax (matplotlib.axes): axes to plot on (must have 3D projection)
        coords (np.array): coordinates to plot (N, steps, 3)
        show_equator (bool, optional): whether to show equator. Defaults to False.
        colors (list, optional): colors for each coordinate. Defaults to None.
        alpha (float, optional): alpha value for coordinates. Defaults to 0.5.
        show_steps (bool, optional): whether to show step number. Defaults to True.
        show_initial (bool, optional): whether to show initial coordinates. Defaults to False.
        loop (bool, optional): whether to loop animation. Defaults to True.

    Returns:
        matplotlib.animation.FuncAnimation: animation object
    """

    if colors == None:
        # Get matplotlib default color cycle
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color'][:coords.shape[0]]
    else:
        assert len(colors) == coords.shape[0]


    def update(frame):
        ax.clear()
        basic_bloch_sphere(ax, show_equator=show_equator)
        if show_initial:
            plot_coords(ax, coords[:,0,:], colors=colors, alpha=0.5)
            
        plot_coords(ax, coords[:,frame,:], colors=colors, alpha=alpha)
        if label_steps:
            ax.set_title("Frame {}".format(frame))
        return ax
    
    anim = FuncAnimation(fig, update, frames=coords.shape[1], interval=100, repeat=loop)

    return anim