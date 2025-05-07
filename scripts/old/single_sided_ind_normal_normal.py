# TOP SURFACE: independent bivariate normal
# mean=0
# std_dev=1
# X domain=[-std_dev/2, std_dev/2]
# Y domain=[-std_dev/2, std_dev/2]

from pathlib import Path

from mesh import Mesh

if __name__ == "__main__":

    # Define a function (X, Z) -> Y: X is width, Z is depth, Y is Height
    def norm(X, Z):
        # define imports for the distribution
        from scipy.stats import norm

        # Define the distribution parameters
        mu = 0
        sigma = 1
        scale_factor = 10  # TODO figure out why this is needed: without it the distribution is barely visible

        return norm.pdf(X, mu, sigma) * norm.pdf(Z, mu, sigma) * scale_factor

    # Parameters
    mu = 0
    std_dev = 1

    side_length = 5 * std_dev
    side_height = side_length / 20

    # width
    x_max = side_length / 2
    x_min = -x_max

    # depth
    z_max = side_length / 2
    z_min = -z_max

    # sidewall height
    y_max = side_height
    y_min = 0

    n_verts = 600  # Higher the number, the smoother the surface is.

    mesh = Mesh(x_min, x_max, z_min, z_max, n_verts, norm)
    mesh.render_pcd()
    mesh.render_mesh()

    mesh.to_stl(Path(f'../out/single_sided_ind_normal_normal.stl'))
