import numpy as np
from scipy.spatial import Delaunay
from scipy.stats import norm, dweibull, genhyperbolic
import open3d as o3d

mean = 0
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

n_verts = 100

x = np.linspace(x_min, x_max, n_verts)
z = np.linspace(z_min, z_max, n_verts)
X, Z = np.meshgrid(x, z)



#dweibull
c = 3
# genhyperbolic
p = 0.5
a = 1.5
b = -0.5
# gen bottom surface
y_bottom = dweibull.pdf(X, c) * genhyperbolic.pdf(Z, p, a, b) * 5
bottom_verts = np.vstack((X.ravel(), y_bottom.ravel(), Z.ravel())).T

# zeroize bottom edges
for coord in bottom_verts:
    if coord[0] == x_min or coord[0] == x_max or coord[2] == z_min or coord[2] == z_max:
        coord[1] = 0


# gen top surface
Y_top = norm.pdf(X, mean, std_dev) * norm.pdf(Z, mean, std_dev) * 10

top_verts = np.vstack((X.ravel(), Y_top.ravel(), Z.ravel())).T
# zeroize top edges
for coord in top_verts:
    if coord[0] == x_min or coord[0] == x_max or coord[2] == z_min or coord[2] == z_max:
        coord[1] = 0

## TODO FIX VERTICAL OFFSET TO AVOID SURFACE INTERSECTION
# diff = top_verts[:, 1] - bottom_verts[:, 1]
diff = bottom_verts[:, 1] - top_verts[:, 1]
print(np.min(diff))
top_verts[:, 1] = top_verts[:, 1] + np.max(diff)


top_pcd = o3d.geometry.PointCloud()
top_pcd.points = o3d.utility.Vector3dVector(top_verts)

bottom_pcd = o3d.geometry.PointCloud()
bottom_pcd.points = o3d.utility.Vector3dVector(bottom_verts)

o3d.visualization.draw_geometries([bottom_pcd, top_pcd])
# simplices = []
# for tri in Delaunay(top_verts[:, [0, 2]]).simplices:
#     simplices.append(np.flip(tri))
# top_tris = simplices
#
# top_mesh = o3d.geometry.TriangleMesh()
# top_mesh.vertices = o3d.utility.Vector3dVector(top_verts)
# top_mesh.triangles = o3d.utility.Vector3iVector(top_tris)
# top_mesh.compute_vertex_normals()
# combined_mesh = top_mesh
# o3d.visualization.draw_geometries([combined_mesh])
