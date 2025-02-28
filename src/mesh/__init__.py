# class Printer:
#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z
from pathlib import Path

import numpy as np
import open3d as o3d
from scipy.spatial import Delaunay


class Mesh:
    def __init__(self):
        self._top_mesh = None
        self._bottom_mesh = None
        self.sidewall_height = None
        self._resolution = None
        self._x_min = None
        self._x_max = None
        self._y_min = None
        self._y_max = None
        self._mesh = None
        self._bottom_surface = None
        self._top_surface = None
        self._x = None
        self._y = None
        self._z = None

    def __str__(self):
        return str({
            "x": self._x,
            "y": self._y,
            "z": self._z,
            "resolution": self._resolution,
            "top surface": self._top_surface,
            "bottom surface": self._bottom_surface,
        })

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        # if value < 100:
        #     raise ValueError("x must be greater than 100mm")
        # elif value > 250:
        #     raise ValueError("x must be less than 250mm")
        # else:
        self._x = value
        mid = np.floor(value / 2)
        self._x_min = -mid
        self._x_max = mid

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        # if value < 100:
        #     raise ValueError("y must be greater than 100mm")
        # elif value > 250:
        #     raise ValueError("y must be less than 250mm")
        # else:
        self._y = value
        mid = np.floor(value / 2)
        self._y_min = -mid
        self._y_max = mid

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if value < 100:
            raise ValueError("z must be greater than 100mm")
        elif value > 250:
            raise ValueError("z must be less than 250mm")
        else:
            self._z = value

    @property
    def top_surface(self):
        return self._top_surface

    @top_surface.setter
    def top_surface(self, top_surface):
        """
        Define a zero-thickness mathematical top surface
        """
        for coord in top_surface:
            coord[2] = coord[2] + self.sidewall_height
        self._top_surface = top_surface

    @property
    def bottom_surface(self):
        return self._bottom_surface

    @bottom_surface.setter
    def bottom_surface(self, bottom_surface):
        """
        Define a zero-thickness mathematical top surface
        """
        self._bottom_surface = bottom_surface

    def _get_corner_verts(self):
        corners = [
            (self._x_min, self._y_min),
            (self._x_min, self._y_max),
            (self._x_max, self._y_min),
            (self._x_max, self._y_max),
        ]
        top_corners = []
        for idx, coord in enumerate(self._top_surface):
            if (coord[0], coord[1]) in corners:
                # print(coord)
                top_corners.append(coord)

        bottom_corners = []
        for idx, coord in enumerate(self._bottom_surface):
            if (coord[0], coord[1]) in corners:
                # print(coord)
                bottom_corners.append(coord)
        corners = np.array(top_corners)
        corners = np.vstack([np.array(bottom_corners), corners])
        print(corners.astype(int))
        return corners
        # print(top_corners)
        # print(np.array(bottom_corners) + len(self._top_surface))

    # def generate(self):
    #
    #
    #     self._zeroize()
    #     verticies = np.vstack([self._bottom_surface, self._top_surface])  # add box and bottom mesh here
    #     triangles = np.vstack([
    #         Delaunay(self._bottom_surface[:, :2]).simplices,
    #         # sidewall_faces,
    #         Delaunay(self._top_surface[:, :2]).simplices
    #     ])
    #     # print(self.top_surface[:,:])
    #     # print(self.top_surface[:,:2])
    #
    #     # verticies = self._top_surface  # add box and bottom mesh here
    #     # triangles = Delaunay(self._top_surface[:, :2]).simplices
    #
    #     self._mesh = o3d.geometry.TriangleMesh()
    #     self._mesh.vertices = o3d.utility.Vector3dVector(verticies)
    #     self._mesh.triangles = o3d.utility.Vector3iVector(triangles)
    #     self._mesh.compute_vertex_normals()
    #     # self._mesh.compute_triangle_normals()
    def generate(self):
        self._zeroize()
        bottom = self.generate_bottom_surface()
        top = self.generate_top_surface()
        self._mesh = bottom + top

    def generate_bottom_surface(self):
        triangles = Delaunay(self._bottom_surface[:, :2]).simplices
        self._bottom_mesh = o3d.geometry.TriangleMesh()
        self._bottom_mesh.vertices = o3d.utility.Vector3dVector(self._bottom_surface)
        self._bottom_mesh.triangles = o3d.utility.Vector3iVector(triangles)
        self._bottom_mesh.compute_vertex_normals()

        return self._bottom_mesh

    def generate_top_surface(self):
        triangles = Delaunay(self._top_surface[:, :2]).simplices
        self._top_mesh = o3d.geometry.TriangleMesh()
        self._top_mesh.vertices = o3d.utility.Vector3dVector(self._top_surface)
        self._top_mesh.triangles = o3d.utility.Vector3iVector(triangles)
        self._top_mesh.compute_vertex_normals()
        return self._top_mesh

    def generate_sidewalls(self):
        sidewall_faces = np.array([
            [0, 99, 10099],
            [0, 10099, 10000],
            [99, 9999, 19999],
            [99, 19999, 10099],
            [9999, 9900, 19900],
            [9999, 19900, 19999],
            [9900, 0, 10000],
            [9900, 10000, 19900],
        ])
        corners = self._get_corner_verts()
        print(corners)

    def _zeroize(self, ):
        for vert in self._top_surface:
            if vert[0] == self._x_min or vert[0] == self._x_max:
                vert[2] = self.sidewall_height
            elif vert[1] == self._y_min or vert[1] == self._y_max:
                vert[2] = self.sidewall_height
        for vert in self._bottom_surface:
            if vert[0] == self._x_min or vert[0] == self._x_max:
                vert[2] = 0
            elif vert[1] == self._y_min or vert[1] == self._y_max:
                vert[2] = 0

    def render(self):
        o3d.visualization.draw_geometries([self._bottom_mesh + self._top_mesh])

    def validate(self):
        print({
            "is_edge_manifold": self._mesh.is_edge_manifold(),
            "is_vertex_manifold": self._mesh.is_vertex_manifold(),
            "is_self_intersecting": self._mesh.is_self_intersecting(),
            "is_watertight": self._mesh.is_watertight(),
            "is_orientable": self._mesh.is_orientable(),
        })

    def get_top_surface_specs(self):
        """
        Get the top surface specifications
        """
        pass



    def write_mesh(self, path):
        """
        Write the mesh to disk as an STL
        """
        path = Path(path)
        o3d.io.write_triangle_mesh(path, self._mesh, print_progress=True)

    def get_bottom_surface_specs(self):
        """
        Get the bottom surface specifications
        """
        pass

    def generate_print_instructions(self):
        """
        Verify that the mesh can be printed at 100% scale on Bambu X1C
        """
        pass

    def simplify(self):
        """
        Return a copy of the mesh object with a reduced number of faces
        """
        pass
