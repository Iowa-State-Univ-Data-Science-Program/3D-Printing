from pathlib import Path

import numpy as np
import open3d as o3d

if __name__ == "__main__":
    support_path = Path('../out/support.stl')
    support_mesh = o3d.io.read_triangle_mesh(support_path)
    print(support_mesh)
    support_mesh.compute_vertex_normals()

    o3d.visualization.draw_geometries([support_mesh])

    verts = np.asarray(support_mesh.vertices)
    tris = np.asarray(support_mesh.triangles)


    for axis in verts:
        print((np.max(axis[0]), np.max(axis[1]), np.max(axis[2])))

    # print(verts)
    # print(tris)
