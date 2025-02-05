import numpy as np
import openstl
from scipy.stats import norm
from scipy.spatial import Delaunay
# x = np.linspace(-10,10,10)
# y = np.linspace(-10,10,10)
# print(np.concatenate((x,y)))
# Define vertices and faces
n = 100
# Parameters for the normal distributions
mu1, sigma1 = 0, 1
mu2, sigma2 = 0, 1

xlen = 5 * sigma1
ylen = 5 * sigma2
zlen = 1.0

vertices = [
    [xlen, ylen, 0.0],
    [xlen, -ylen, 0.0],
    [-xlen, -ylen, 0.0],
    [-xlen, ylen, 0.0],

    [xlen, ylen, zlen],
    [xlen, -ylen, zlen],
    [-xlen, -ylen, zlen],
    [-xlen, ylen, zlen],
]

faces = [
    [0, 1, 2],  # Face 1
    [2, 3, 0],
    #
    [3, 7, 2],
    [7, 6, 2],
    #
    [3, 7, 0],
    [4, 0, 7],
    #
    [5, 0, 4],
    [5, 0, 1],
    #
    [6, 2, 1],
    [5, 6, 1]
]
# Convert vertices and faces to triangles
triangles = openstl.convert.triangles(vertices, faces)
success = openstl.write("box.stl", triangles, openstl.format.binary)
if not success:
    raise Exception("Error: Failed to write to the specified file.")

# Create a 2D matrix with rows as x and columns as y
x = np.linspace(-xlen, xlen, n)
y = np.linspace(-ylen, ylen, n)
X, Y = np.meshgrid(x, y)
#
Z = norm.pdf(X, mu1, sigma1) * norm.pdf(Y, mu2, sigma2) * 10 + zlen

points = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T
tri = Delaunay(points[:, :2])
surface = openstl.convert.triangles(points, tri.simplices)
success = openstl.write("surface.stl", surface, openstl.format.binary)
if not success:
    raise Exception("Error: Failed to write to the specified file.")
