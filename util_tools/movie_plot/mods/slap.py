"""

Developers: whitemanatee > francisco.branco@tecnico.ulisboa.pt

Description: SLAP mod file to plot specific information about the
             algorithm

===========================================================
|               _.-----.._                 __________     |
|             -'    .     ``:--.          (o(' ^ ') o)    |
|           .'.         '  '    \,                        |
|          /       .    `  .  (* \                        |
|         : .  `.  :  ,)  .::../  k                       |
|        ) ..aaa8Y88aP/ <d888aaL_::)                      |
|      .'a888Y8888888b\  )  `^88: "                       |
|    .'.a8888)  ""     `'    d88                          |
|   (a888888/                "`                           |
|   `Y888PP'                                              |
===========================================================
Protect the manatees!
"""


import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def get_correlated_dataset(n, dependency, mu, scale):
    latent = np.random.randn(n, 2)
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    scaled_with_offset = scaled + mu
    # return x and y of the new, correlated dataset
    return scaled_with_offset[:, 0], scaled_with_offset[:, 1]

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if kwargs["edgecolor"] == "red":
        facecolor = "pink"
    elif kwargs["edgecolor"] == "black":
        facecolor = "gray"
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def plot_ellipse(covariance, ax, position, color):
    # scale = 0.00001, 0.00001
    scale = 2.5, 2.5
    norm_covariance = covariance / np.linalg.norm(covariance)
    x, y = get_correlated_dataset(1000, norm_covariance, position, scale)
    confidence_ellipse(x, y, ax, edgecolor=color, label='_nolegend_')
    ax.scatter(x, y, color="tab:blue", alpha=0.2, linewidths=0.01, s=5, label="_nolegend_")