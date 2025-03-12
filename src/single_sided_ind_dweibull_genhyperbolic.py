from pathlib import Path

from mesh import Mesh

if __name__ == "__main__":

    # Define a function (X, Z) -> Y: X is width, Z is depth, Y is Height
    def surface_function(X, Z):
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


    # Parameters
    side_length = 5
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


    n_verts = 500  # Higher the number, the smoother the surface is.

    mesh = Mesh(surface_function, x_min, x_max, z_min, z_max, side_height, n_verts)
    mesh.render_pcd()
    mesh.render_mesh()

    mesh.to_stl(Path(f'../out/single_sided_ind_dweibull_genhyperbolic.stl'))
