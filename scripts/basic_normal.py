"""
Filename: basic_normal.py
Author: Dhruv Dole
Email: dsdole@iastate.edu
Date: 2025/05/07
Description: An example of how to generate a basic TableTopModel with a normal-normal on top, and a flat bottom.
"""

from src.math_surfaces import *


def norm(X, Z):
    # Any modules and objects needed inside the function should be imported here
    from scipy.stats import norm

    # Define the distribution parameters
    mu = 0
    sigma = 1

    return norm.pdf(X, mu, sigma) * norm.pdf(Z, mu, sigma)


def flat(X, Z):
    from numpy import zeros_like
    return zeros_like(X * Z)


mu = 0
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

n_verts = 100  # Higher the number, the smoother the surface is.

# Generate top surface
top_surface = Surface(x_min, x_max, z_min, z_max, n_verts, norm)
top_surface.scale(10)
top_surface.zeroize_edge() # Flattens the edge of the surface so it's flush with the sidewalls increasing n_verts will decrease visibility of zeroed edge

top_surface.compute() # Must be called before rendering or attempting to pass to STLWriter


top_surface.render() # Renders a single surface, default mode is pcd(point cloud)

bottom_surface = Surface(x_min, x_max, z_min, z_max, n_verts, flat)
bottom_surface.scale(10)
bottom_surface.zeroize_edge()
bottom_surface.compute(flip=True)
bottom_surface.render('pcd')

model = TableTopModel(top_surface, bottom_surface)
model.render('mesh') # renders the complete model as a mesh

model_writer = STLWriter(print_progress=True)

model_writer.save(model.get_mesh(), 'basic_normal.stl')
