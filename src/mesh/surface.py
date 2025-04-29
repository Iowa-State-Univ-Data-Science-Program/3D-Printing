import numpy as np
from scipy.spatial import Delaunay

import open3d as o3d


class Surface:
    def __init__(self, x_min, x_max, z_min, z_max, n_verts, function):
        self.x_min = x_min
        self.x_max = x_max
        self.z_min = z_min
        self.z_max = z_max
        self.n_verts = n_verts
        self.function = function

        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        X, Z = np.meshgrid(x, z)
        Y = self.function(X, Z)

        self.verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        self.tris = []
        for tri in Delaunay(self.verts[:, [0, 2]]).simplices:
            self.tris.append(np.flip(tri))

    def zeroize(self):
        for coord in self.verts:
            if (coord[0] == self.x_min or
                    coord[0] == self.x_max or
                    coord[2] == self.z_min or
                    coord[2] == self.z_max):
                coord[1] = 0

    def flip_normals(self):
        pass

    def invert(self):
        pass

    def scale(self, factor):
        self.verts[:, 1] *= factor


def generate_pcd(surface):
    center = o3d.geometry.PointCloud()
    center.points = o3d.utility.Vector3dVector(np.array([[0, 0, 0]]))
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(surface.verts)
    return pcd


def generate_mesh(surface):
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(surface.verts)
    mesh.triangles = o3d.utility.Vector3iVector(surface.tris)
    mesh.compute_vertex_normals()
    return mesh


def render(meshes):
    o3d.visualization.draw_geometries(meshes)


def write_to_stl(mesh, path):
    return None
