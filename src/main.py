import numpy as np
from scipy.stats import norm

from mesh import Mesh

if __name__ == '__main__':
    m = Mesh()

    n = 50
    mu1, sigma1 = 0, 1
    mu2, sigma2 = 0, 1

    m.x = 7 * sigma1
    m.y = 7 * sigma2

    # x = np.linspace(-xlen, xlen, n)
    # y = np.linspace(-ylen, ylen, n)

    x = np.linspace(m._x_min, m._x_max, n)
    y = np.linspace(m._y_min, m._y_max, n)

    X, Y = np.meshgrid(x, y)

    Z = norm.pdf(X, mu1, sigma1) * norm.pdf(Y, mu2,
                                            sigma2) * 10  # scale height by 10 for visibility, not sure why this is required right now.
    m.sidewall_height = 0.5

    m.top_surface = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T
    m.bottom_surface = np.vstack((X.ravel(), Y.ravel(), -1 * Z.ravel())).T

    # m._get_corner_verts()
    m.generate()
    bottom = m.generate_bottom_surface()
    top = m.generate_top_surface()
    # m.validate()
    # m.render()
    # m.write_mesh(bottom, '../out/bottom.stl')
    # m.write_mesh(top,'../out/top.stl')
    m.write_mesh('../out/mesh.stl')
