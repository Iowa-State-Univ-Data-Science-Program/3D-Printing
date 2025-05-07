# TOP SURFACE: independent bivariate normal
# mean=0
# std_dev=1
# X domain=[-std_dev/2, std_dev/2]
# Y domain=[-std_dev/2, std_dev/2]

from pathlib import Path

from mesh import Mesh

if __name__ == "__main__":

    # Define a function (X, Z) -> Y: X is width, Z is depth, Y is Height
    def lognorm(X, Z):
        # define imports for the distribution
        from scipy.stats import multivariate_normal, norm

        # Define the distribution parameters
        mu_x = 0
        var_x = 1
        mu_z = 0
        var_z = 1

        # pos = np.empty(X.shape + (2,))
        # pos[:, :, 0] = X; pos[:, :, 1] = Z
        # rv = multivariate_normal([mu_x, mu_z], [[var_x, 0], [0, var_z]])
        # print(rv.logpdf(pos))
        # return rv.pdf(pos) * 10
        return norm.logpdf(X, mu_x, 1) * norm.logpdf(Z, mu_z, 1)

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

    n_verts = 100  # Higher the number, the smoother the surface is.

    mesh = Mesh(x_min, x_max, z_min, z_max, n_verts, lognorm)
    mesh.render_pcd()
    mesh.render_mesh()

    mesh.to_stl(Path(f'../out/single_sided_ind_normal_normal.stl'))
