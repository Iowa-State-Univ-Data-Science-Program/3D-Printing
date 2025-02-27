import numpy as np
import openstl
import open3d as o3d
from scipy.stats import norm
from scipy.spatial import Delaunay

n = 100
# Parameters for the normal distributions
mu1, sigma1 = 0, 1
mu2, sigma2 = 0, 1

xlen = 3 * sigma1
ylen = 3 * sigma2
zlen = 1.0

box_vertices = [
    [xlen, ylen, 0.0],
    [xlen, -ylen, 0.0],
    [-xlen, -ylen, 0.0],
    [-xlen, ylen, 0.0],

    [xlen, ylen, zlen],
    [xlen, -ylen, zlen],
    [-xlen, -ylen, zlen],
    [-xlen, ylen, zlen],
]

box_faces = [
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

x = np.linspace(-xlen, xlen, n)
y = np.linspace(-ylen, ylen, n)
X, Y = np.meshgrid(x, y)

Z = norm.pdf(X, mu1, sigma1) * norm.pdf(Y, mu2, sigma2) * 10 + zlen

surface_vertices = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

# print(box_vertices, np.shape(box_vertices))
# print(surface_vertices, np.shape(surface_vertices))

combined_vertices = np.vstack((box_vertices, surface_vertices))
# print(combined_vertices, np.shape(combined_vertices))

triangulation = Delaunay(combined_vertices[:, :2])

combined_faces = np.vstack((triangulation.simplices, box_faces))

mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(combined_vertices)
mesh.triangles = o3d.utility.Vector3iVector(triangulation.simplices)
o3d.visualization.draw_geometries([mesh])
# stl = openstl.convert.triangles(combined_vertices, combined_faces)

# success = openstl.write("combined_surface.stl", stl, openstl.format.binary)
# if not success:
#     raise Exception("Error: Failed to write to the specified file.")

# print(triangulation.simplices, np.shape(triangulation.simplices))

# print(box_faces, np.shape(box_faces))


# print(combined_faces, np.shape(combined_faces))
