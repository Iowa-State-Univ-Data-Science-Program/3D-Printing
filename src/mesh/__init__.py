# class Printer:
#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z
import numpy as np
import openstl
import open3d as o3d
from scipy.spatial import Delaunay


class Mesh:
    def __init__(self, x, y, z):
        self._mesh = None
        self._bottom_surface = None
        self._top_surface = None
        self._resolution = None
        self._x = x
        self._y = y
        self._z = z

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
        if value < 100:
            raise ValueError("x must be greater than 100mm")
        elif value > 250:
            raise ValueError("x must be less than 250mm")
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value < 100:
            raise ValueError("y must be greater than 100mm")
        elif value > 250:
            raise ValueError("y must be less than 250mm")
        else:
            self._y = value

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
        self._top_surface = top_surface

    def define_bottom_surface(self):
        """
        Define a zero-thickness mathematical bottom surface
        """
        pass

    def _combine_surfaces(self):
        """
        combine two zero-thickness mathematical surfaces (top & bottom) in a closed mesh
        """
        pass

    def generate(self):
        verticies = np.vstack(self._top_surface) # add box and bottom mesh here
        triangles = Delaunay(verticies[:, :2])
        self._mesh = o3d.geometry.TriangleMesh()
        self._mesh.vertices = o3d.utility.Vector3dVector(verticies)
        self._mesh.triangles = o3d.utility.Vector3iVector(triangles.simplices)
        
    def render(self):
        o3d.visualization.draw_geometries([self._mesh])

    def validate(self):
        """
        Verify that the mesh is closed and without error
        """
        pass

    def get_top_surface_specs(self):
        """
        Get the top surface specifications
        """
        pass

    def get_bottom_surface_specs(self):
        """
        Get the bottom surface specifications
        """
        pass

    def write_mesh(self):
        """
        Write the mesh to disk as an STL
        """
        pass

    def generate_print_instructions(self):
        """
        Verify that the mesh can be printed at 100% scale on Bambu X1C
        """
        pass

    def render_top_surface(self):
        pass

    def render_bottom_surface(self):
        pass

    def render_mesh(self):
        pass

    def simplify(self):
        """
        Return a copy of the mesh object with a reduced number of faces
        """
        pass
