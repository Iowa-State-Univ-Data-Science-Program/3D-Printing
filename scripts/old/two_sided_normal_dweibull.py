# TOP SURFACE: independent bivariate normal
# mean=0
# std_dev=1
# X domain=[-std_dev/2, std_dev/2]
# Y domain=[-std_dev/2, std_dev/2]
# BOTTOM SURFACE: LOG OF TOP

from pathlib import Path
import sys
import numpy as np

from mesh import Mesh


if __name__ == "__main__":

    # Define a function (X, Z) -> Y: X is width, Z is depth, Y is Height
    def norm(X, Z):
        # define imports for the distribution
        from scipy.stats import norm


        mu_x = 0
        mu_z = 0
        scale_factor = 10
        return norm.pdf(X, mu_x, 1) * norm.pdf(Z, mu_z, 1) * scale_factor

    # Define a function (X, Z) -> Y: X is width, Z is depth, Y is Height
    def dweibull_genhyperbolic(X, Z):
        # define imports for the distribution
        from scipy.stats import dweibull, genhyperbolic

        # Define the distribution parameters
        # dweibull
        c = 3
        # genhyperbolic
        p = 0.5
        a = 1.5
        b = -0.5

        scale_factor = 5  # TODO figure out why this is needed: without it the distribution is barely visible
        return dweibull.pdf(X, c) * genhyperbolic.pdf(Z, p, a, b) * scale_factor

    mu = 0
    std_dev = 1

    side_length = 5 * std_dev

    # width
    x_max = side_length / 2
    x_min = -x_max

    # depth
    z_max = side_length / 2
    z_min = -z_max

    n_verts = 600

    np.set_printoptions(threshold=sys.maxsize)
    mesh = Mesh(x_min, x_max, z_min, z_max, n_verts, norm, dweibull_genhyperbolic)

    # print(mesh.bottom_verts[:, 1])
    mesh.render_pcd()
    mesh.render_mesh()

    mesh.to_stl(Path(f'../out/two_sided_norm_norm_dweibull_genhyper.stl'))
