from mesh.surface import Surface, TableTopModel

def norm(X, Z):
    # define imports for the distribution
    from scipy.stats import norm

    # Define the distribution parameters
    mu = 0
    sigma = 1

    return norm.pdf(X, mu, sigma) * norm.pdf(Z, mu, sigma)


def flat(X, Z):
    from numpy import zeros_like
    return zeros_like(X * Z)


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

top_surface = Surface(x_min, x_max, z_min, z_max, n_verts, norm)
top_surface.scale(10)
top_surface.zeroize_edge()

top_surface.compute()
# top_surface.render('mesh')

bottom_surface = Surface(x_min, x_max, z_min, z_max, n_verts, flat)
bottom_surface.scale(10)
bottom_surface.zeroize_edge()
bottom_surface.compute(flip=True)
# bottom_surface.render('mesh')

model = TableTopModel(top_surface, bottom_surface,)
model.render('mesh')
