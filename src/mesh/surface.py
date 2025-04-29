from typing import Union

import numpy as np
import open3d as o3d
from narwhals import Boolean
from scipy.spatial import Delaunay


class Surface:
    def __init__(self, x_min, x_max, z_min, z_max, n_verts, sgf):
        self.zeroed = False
        self.x_min = x_min
        self.x_max = x_max
        self.z_min = z_min
        self.z_max = z_max
        self.n_verts = n_verts
        self.sgf = sgf
        self.vertices = []
        self.simplices = []
        self.mesh = None
        self.pcd = None
        self.current_scale = 1

        # Generate Vertices
        x = np.linspace(self.x_min, self.x_max, self.n_verts)
        z = np.linspace(self.z_min, self.z_max, self.n_verts)
        X, Z = np.meshgrid(x, z)
        Y = self.sgf(X, Z)

        self.vertices = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

    def compute(self, flip=False):
        """
        Compute the Surface
        """
        # Generate Triangles
        self.simplices = []
        for tri in Delaunay(self.vertices[:, [0, 2]]).simplices:
            self.simplices.append(np.flip(tri))

        # Flip the triangles if needed: the direction of the normal is found using the right hand rule through each point in a triangle
        if flip:
            flipped_simplices = []
            for tri in self.simplices:
                flipped_simplices.append(np.flip(tri))
            self.simplices = flipped_simplices

        # Generate the Mesh
        self.mesh = o3d.geometry.TriangleMesh()
        self.mesh.vertices = o3d.utility.Vector3dVector(self.vertices)
        self.mesh.triangles = o3d.utility.Vector3iVector(self.simplices)
        self.mesh.compute_vertex_normals()

        # Generate the PointCloud
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(self.vertices)

    def scale(self, factor: Union[int, float], reset: Boolean = False) -> None:
        """
        Scale the vertical axis. If reset is True, set the scale back to 1 before applying the new scale factor
        :param factor:
        :param reset:
        :return:
        """
        if reset:
            self.vertices[:, 1] *= 1 / self.current_scale  #
        self.vertices[:, 1] *= factor
        self.current_scale *= factor

    def zeroize_edge(self):
        for coord in self.vertices:
            if (coord[0] == self.x_min or coord[0] == self.x_max or coord[2] == self.z_min or coord[2] == self.z_max):
                coord[1] = 0
        self.zeroed = True

    def render(self, render_type='pcd'):
        """
        Render the Mesh or PCD
        """
        if render_type == 'mesh':
            o3d.visualization.draw_geometries([self.mesh])
        elif render_type == 'pcd':
            o3d.visualization.draw_geometries([self.pcd])
        else:
            raise ValueError('Invalid render type')

    def get_surface_specs(self):
        pass


class TableTopModel:
    """
    A class which represents a tabletop model. It can be used to combine two mathematical surfaces into a printable model
    """

    def __init__(self, top_surface: Surface, bottom_surface: Surface, min_offset: int = 0.2):
        self.mesh = None
        self.pcd = None
        self.min_offset = min_offset
        self.top_surface = top_surface
        self.bottom_surface = bottom_surface
        self._validate_surface_domains()

        self.x_min = self.top_surface.x_min
        self.x_max = self.top_surface.x_max
        self.z_min = self.top_surface.z_min
        self.z_max = self.top_surface.z_max
        self.vertical_offset = None

        self.SIDE_LAYERS = 5
        self._construct_model()

    def _validate_surface_domains(self):
        """
        Assert that both surfaces have the same X and Z domain
        """
        assert self.top_surface.x_min == self.bottom_surface.x_min, "Top surface x_min must be equal to bottom surface x_min"
        assert self.top_surface.x_max == self.bottom_surface.x_max, "Top surface x_max must be equal to bottom surface x_max"
        assert self.top_surface.z_min == self.bottom_surface.z_min, "Top surface z_min must be equal to bottom surface z_min"
        assert self.top_surface.z_max == self.bottom_surface.z_max, "Top surface z_max must be equal to bottom surface z_max"

    def _construct_model(self):
        """
        Construct the TableTopModel Mesh.
        """
        # Verify that both surfaces are zeroed
        assert self.top_surface.zeroed, "Top surface must be zeroed"
        assert self.bottom_surface.zeroed, "Bottom surface must be zeroed"

        # Translate bottom surface above y=0
        bottom_diff = np.zeros_like(self.bottom_surface.vertices[:, 1]) - self.bottom_surface.vertices[:, 1]
        bottom_offset = np.max(bottom_diff)
        self.bottom_surface.vertices[:, 1] += bottom_offset

        # Compute the minimum vertical offset (height of the sidewalls)
        diff = self.bottom_surface.vertices[:, 1] - self.top_surface.vertices[:, 1]
        if np.max(diff) < self.min_offset:
            self.vertical_offset = self.min_offset
        else:
            self.vertical_offset = np.max(diff)
        print(self.vertical_offset)

        # Translate top surface upwards by self.vertical_offset
        self.top_surface.vertices[:, 1] = self.top_surface.vertices[:, 1] + self.vertical_offset

        # Recompute surfaces
        self.top_surface.compute()
        self.bottom_surface.compute(flip=True)

        # generate the 4 sidewalls(each is a Surface())
        self._generate_side_walls()  # Combine them into a single mesh and pcd.

    def _generate_side_walls(self):
        self.front = self._gen_front()
        self.back = self._gen_back()
        self.right = self._gen_right()
        self.left = self._gen_left()
        pass

    def _gen_front(self):
        """
        Generate Front sidewall
        """

        x = np.linspace(self.x_min, self.x_max, 5)
        y = np.linspace(0, self.vertical_offset, self.SIDE_LAYERS)

        X, Y = np.meshgrid(x, y)
        Z = np.full(shape=(len(x) * len(y)), fill_value=self.z_max)
        verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T
        tris = Delaunay(verts[:, :2]).simplices

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(tris)
        mesh.compute_vertex_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(verts)
        return {'mesh': mesh, 'pcd': pcd}

    def _gen_back(self):
        """
        Generate B side verts and Tris
        """
        x = np.linspace(self.x_min, self.x_max, 5)
        y = np.linspace(0, self.vertical_offset, self.SIDE_LAYERS)

        X, Y = np.meshgrid(x, y)
        Z = np.full(shape=(len(x) * len(y)), fill_value=self.z_min)
        verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        simplices = Delaunay(verts[:, :2]).simplices

        flipped_simplices = []
        for tri in simplices:
            flipped_simplices.append(np.flip(tri))
        tris = flipped_simplices

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(tris)
        mesh.compute_vertex_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(verts)
        return {'mesh': mesh, 'pcd': pcd}

    def _gen_right(self):
        """
        Generate C side verts and Tris
        """
        z = np.linspace(self.z_min, self.z_max, 5)
        y = np.linspace(0, self.vertical_offset, self.SIDE_LAYERS)

        Z, Y = np.meshgrid(z, y)
        X = np.full(shape=(len(z) * len(y)), fill_value=self.x_min)
        verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        simplices = Delaunay(verts[:, [1, 2]]).simplices

        flipped_simplices = []
        for tri in simplices:
            flipped_simplices.append(np.flip(tri))
        tris = flipped_simplices
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(tris)
        mesh.compute_vertex_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(verts)
        return {'mesh': mesh, 'pcd': pcd}

    def _gen_left(self):
        """
        Generate D side verts and Tris
        """
        z = np.linspace(self.z_min, self.z_max, 5)
        y = np.linspace(0, self.vertical_offset, self.SIDE_LAYERS)

        Z, Y = np.meshgrid(z, y)
        X = np.full(shape=(len(z) * len(y)), fill_value=self.x_max)
        verts = np.vstack((X.ravel(), Y.ravel(), Z.ravel())).T

        tris = Delaunay(verts[:, [1, 2]]).simplices
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(tris)
        mesh.compute_vertex_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(verts)
        return {'mesh': mesh, 'pcd': pcd}

    def get_model_specs(self):
        pass

    def render(self, render_type='pcd'):
        """
        Render the Mesh or PCD
        """
        if render_type == 'mesh':
            o3d.visualization.draw_geometries(
                [self.top_surface.mesh, self.bottom_surface.mesh, self.front['mesh'], self.back['mesh'],
                 self.right['mesh'], self.left['mesh']])
        elif render_type == 'pcd':
            o3d.visualization.draw_geometries(
                [self.top_surface.pcd, self.bottom_surface.pcd, self.front['pcd'], self.back['pcd'], self.right['pcd'],
                 self.left['pcd']])
        else:
            raise ValueError('Invalid render type')


class STLWriter:
    pass
