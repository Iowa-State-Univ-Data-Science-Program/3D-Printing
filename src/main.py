import numpy as np
from scipy.stats import norm

from mesh import Mesh

if __name__ == '__main__':
    m = Mesh(250, 250, 250)

    n = 100
    mu1, sigma1 = 0, 1
    mu2, sigma2 = 0, 1

    xlen = 3 * sigma1
    ylen = 3 * sigma2

    x = np.linspace(-xlen, xlen, n)
    y = np.linspace(-ylen, ylen, n)

    X, Y = np.meshgrid(x, y)

    Z = norm.pdf(X, mu1, sigma1) * norm.pdf(Y, mu2, sigma2) * 10 # scale height by 10 for visibility, not sure why this is required right now.

    m.top_surface = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T
    # m.bottom_surface = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T


    m.generate()
    m.render()
    # print(m)
