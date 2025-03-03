import numpy as np
from scipy.spatial import Delaunay

import open3d as o3d


class Mesh:
    def __init__(self, func, x_min, x_max, z_min, z_max, side_height, n_verts):
        # function which returns func
        self.surface_function = func
        # x domain (width
        self.x_min = x_min
        self.x_max = x_max

        # z domain( depth
        self.z_min = z_min
        self.z_max = z_max
        self.y_max = side_height
        self.y_min = 0
        self.n_verts = n_verts
        self.SIDE_LAYERS = 5

        self._gen_a()
        self._gen_b()
        self._gen_c()
        self._gen_d()
        self._gen_e()
        self._gen_top()

        self.mesh = self.compute()

    @property
    def length(self):
        return self._length

    @property
    def wall_height(self):
        return self._wall_height

    @property
    def resolution(self):
        return self._resolution

    def _gen_a(self):
        """
        Generate A side Verts and Tris
        """

        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        y = np.linspace(self.y_min, self.y_max, self.SIDE_LAYERS)

        X, Y = np.meshgrid(x, y)
        Z = np.full(shape=(len(x) * len(y)), fill_value=self.z_max)
        self.a_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        self.a_tris = Delaunay(self.a_verts[:, :2]).simplices

    def _gen_b(self):
        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        y = np.linspace(self.y_min, self.y_max, self.SIDE_LAYERS)

        X, Y = np.meshgrid(x, y)
        Z = np.full(shape=(len(x) * len(y)), fill_value=self.z_min)
        self.b_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        simplices = Delaunay(self.b_verts[:, :2]).simplices

        flipped_simplices = []
        for tri in simplices:
            flipped_simplices.append(np.flip(tri))
        self.b_tris = flipped_simplices

    def _gen_c(self):
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        y = np.linspace(self.y_min, self.y_max, self.SIDE_LAYERS)

        Z, Y = np.meshgrid(z, y)
        X = np.full(shape=(len(z) * len(y)), fill_value=self.x_min)
        self.c_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        simplices = Delaunay(self.c_verts[:, [1, 2]]).simplices

        flipped_simplices = []
        for tri in simplices:
            flipped_simplices.append(np.flip(tri))
        self.c_tris = flipped_simplices

    def _gen_d(self):
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        y = np.linspace(self.y_min, self.y_max, self.SIDE_LAYERS)

        Z, Y = np.meshgrid(z, y)
        X = np.full(shape=(len(z) * len(y)), fill_value=self.x_max)
        self.d_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        self.d_tris = Delaunay(self.d_verts[:, [1, 2]]).simplices

    def _gen_e(self):
        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        X, Z = np.meshgrid(x, z)
        Y = np.zeros(len(x) * len(z))
        self.e_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        self.e_tris = Delaunay(self.e_verts[:, [0, 2]]).simplices

    def _gen_top(self):
        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        X, Z = np.meshgrid(x, z)
        Y = self.surface_function(X, Z)

        top_verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        # zeroize edges
        for coord in top_verts:
            if coord[0] == x_min or coord[0] == x_max or coord[2] == z_min or coord[2] == z_max:
                coord[1] = 0

        top_verts[:, 1] = top_verts[:, 1] + side_height
        self.top_verts = top_verts

        simplices = []
        for tri in Delaunay(self.top_verts[:, [0, 2]]).simplices:
            simplices.append(np.flip(tri))
        self.top_tris = simplices

    def _validate_mesh(self):
        pass

    def compute(self):
        self.a_mesh = o3d.geometry.TriangleMesh()
        self.a_mesh.vertices = o3d.utility.Vector3dVector(self.a_verts)
        self.a_mesh.triangles = o3d.utility.Vector3iVector(self.a_tris)
        self.a_mesh.compute_vertex_normals()

        self.b_mesh = o3d.geometry.TriangleMesh()
        self.b_mesh.vertices = o3d.utility.Vector3dVector(self.b_verts)
        self.b_mesh.triangles = o3d.utility.Vector3iVector(self.b_tris)
        self.b_mesh.compute_vertex_normals()

        self.c_mesh = o3d.geometry.TriangleMesh()
        self.c_mesh.vertices = o3d.utility.Vector3dVector(self.c_verts)
        self.c_mesh.triangles = o3d.utility.Vector3iVector(self.c_tris)
        self.c_mesh.compute_vertex_normals()

        self.d_mesh = o3d.geometry.TriangleMesh()
        self.d_mesh.vertices = o3d.utility.Vector3dVector(self.d_verts)
        self.d_mesh.triangles = o3d.utility.Vector3iVector(self.d_tris)
        self.d_mesh.compute_vertex_normals()

        self.e_mesh = o3d.geometry.TriangleMesh()
        self.e_mesh.vertices = o3d.utility.Vector3dVector(self.e_verts)
        self.e_mesh.triangles = o3d.utility.Vector3iVector(self.e_tris)
        self.e_mesh.compute_vertex_normals()

        self.top_mesh = o3d.geometry.TriangleMesh()
        self.top_mesh.vertices = o3d.utility.Vector3dVector(self.top_verts)
        self.top_mesh.triangles = o3d.utility.Vector3iVector(self.top_tris)
        self.top_mesh.compute_vertex_normals()

    def render_pcd(self):
        meshes = [self.a_mesh, self.b_mesh, self.c_mesh, self.d_mesh, self.e_mesh, self.top_mesh]
        center = o3d.geometry.PointCloud()
        center.points = o3d.utility.Vector3dVector(np.array([[0, 0, 0]]))
        pcds = []
        pcds.append(center)
        for mesh in meshes:
            pcd = o3d.geometry.PointCloud()
            pcd.points = mesh.vertices
            pcds.append(pcd)
        o3d.visualization.draw_geometries(pcds)

    def render_mesh(self):
        meshes = [self.a_mesh, self.b_mesh, self.c_mesh, self.d_mesh, self.e_mesh, self.top_mesh]
        o3d.visualization.draw_geometries(meshes)


    def validate(self):
        pass

    def to_stl(self):
        pass


# instantiate obj
# set length, wall_height, resolution
# create a function like norm()
# func must d

if __name__ == "__main__":
    def norm(X, Z):
        from scipy.stats import norm
        mu = 0
        sigma = 1
        scale_factor = 10
        return norm.pdf(X, mu, sigma) * norm.pdf(Z, mu, sigma) * scale_factor


    sigma = 1
    side_length = 5 * sigma
    side_height = side_length / 20
    # define number of verts per side
    n_verts = 20

    x_max = side_length / 2
    x_min = -x_max
    z_max = side_length / 2
    z_min = -z_max
    y_max = side_height
    y_min = 0

    mesh = Mesh(norm, x_min, x_max, z_min, z_max, side_height, n_verts)
    # mesh.render_pcd()
    mesh.render_mesh()

    n_verts = 40
    mesh = Mesh(norm, x_min, x_max, z_min, z_max, side_height, n_verts)
    # mesh.render_pcd()
    mesh.render_mesh()

    n_verts = 100
    mesh = Mesh(norm, x_min, x_max, z_min, z_max, side_height, n_verts)
    # mesh.render_pcd()
    mesh.render_mesh()
