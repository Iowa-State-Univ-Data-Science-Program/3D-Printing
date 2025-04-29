from mesh.surface import Surface, render, generate_mesh, generate_pcd


def norm(X, Z):
    # define imports for the distribution
    from scipy.stats import norm

    # Define the distribution parameters
    mu = 0
    sigma = 1

    return norm.pdf(X, mu, sigma) * norm.pdf(Z, mu, sigma)


def lognorm(X, Z):
    # define imports for the distribution
    from scipy.stats import multivariate_normal, norm

    # Define the distribution parameters
    mu_x = 0
    mu_z = 0
    var_x = 1
    var_z = 1

    # pos = np.empty(X.shape + (2,))
    # pos[:, :, 0] = X; pos[:, :, 1] = Z
    # rv = multivariate_normal([mu_x, mu_z], [[var_x, 0], [0, var_z]])
    # return rv.pdf(pos)
    return norm.logpdf(X, mu_x, 1) * norm.logpdf(Z, mu_z, 1)

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

top = Surface(x_min, x_max, z_min, z_max, n_verts, norm)

# mesh = generate_mesh(surf)

# render([mesh])
# render([generate_pcd(top)])

top.zeroize()
top.scale(10)
render([generate_pcd(top)])

side_length = side_length / 20

bottom = Surface(0, side_length, 0, side_length, n_verts, lognorm)
bottom.zeroize()
# bottom.scale(10)
render([generate_pcd(bottom)])
