from pathlib import Path
from typing import Any, Union

import numpy as np
from numpy import ndarray, dtype
from scipy.stats import norm
from stl import mesh

n = 1000
# Parameters for the normal distributions
mu1, sigma1 = 0, 1
mu2, sigma2 = 0, 1


# Create a 2D matrix with rows as x and columns as y
x = np.linspace(-3 * sigma1, 3 * sigma1, n)
y = np.linspace(-3 * sigma2, 3 * sigma2, n)
X, Y = np.meshgrid(x, y)

surface = norm.pdf(X, mu1, sigma1) * norm.pdf(Y, mu2, sigma2) * 10  # the *10 is just to scale the height

def construct_mesh(surface):
    num_rows, num_cols = surface.shape
    vertices = []
    faces = []

    for i in range(num_rows - 1):
        for j in range(num_cols - 1):
            v0 = [X[i, j], Y[i, j], surface[i, j]]
            v1 = [X[i + 1, j], Y[i + 1, j], surface[i + 1, j]]
            v2 = [X[i + 1, j + 1], Y[i + 1, j + 1], surface[i + 1, j + 1]]
            v3 = [X[i, j + 1], Y[i, j + 1], surface[i, j + 1]]

            vertices.append(v0)
            vertices.append(v1)
            vertices.append(v2)
            vertices.append(v3)

            faces.append([len(vertices) - 4, len(vertices) - 3, len(vertices) - 2])
            faces.append([len(vertices) - 4, len(vertices) - 2, len(vertices) - 1])

    vertices = np.array(vertices)
    faces = np.array(faces)

    output_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            output_mesh.vectors[i][j] = vertices[f[j], :]
    return output_mesh


# Triangulation
# num_rows, num_cols = surface.shape
# vertices = []
# faces = []
#
# for i in range(num_rows - 1):
#     for j in range(num_cols - 1):
#         v0 = [X[i, j], Y[i, j], surface[i, j]]
#         v1 = [X[i + 1, j], Y[i + 1, j], surface[i + 1, j]]
#         v2 = [X[i + 1, j + 1], Y[i + 1, j + 1], surface[i + 1, j + 1]]
#         v3 = [X[i, j + 1], Y[i, j + 1], surface[i, j + 1]]
#
#         vertices.append(v0)
#         vertices.append(v1)
#         vertices.append(v2)
#         vertices.append(v3)
#
#         faces.append([len(vertices) - 4, len(vertices) - 3, len(vertices) - 2])
#         faces.append([len(vertices) - 4, len(vertices) - 2, len(vertices) - 1])
#
# vertices = np.array(vertices)
# faces = np.array(faces)
#
# pdf_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
# for i, f in enumerate(faces):
#     for j in range(3):
#         pdf_mesh.vectors[i][j] = vertices[f[j], :]

pdf_mesh = construct_mesh(surface)

stl_dir = Path("../stls")

file = stl_dir / "bivariate_normal_scaled.stl"
pdf_mesh.save(file)
